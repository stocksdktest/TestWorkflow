import time
from collections import defaultdict

from utils.compare_record import StockResultTypes

def is_empty(obj, key):
  return key not in obj or len(obj[key]) == 0 

def is_ref_id(obj):
  return str(type(obj)) == "<class 'bson.objectid.ObjectId'>"

class SdkMongoWriter(object):
    """
    将比对结果拆分后写入MongoDB，比对结果大致可以分成以下5种类型
    1. 普通对比
    2. 行情对比
    3. 跟帐对比
    4. 排序结果
    5. 对比+排序

    Quote   
    result: ref in big_data
    error & mismatch & empty: ref in big_data

    Sort
    result: ref in big_data
    error & mismatch & empty: ref in test_result

    Default
    result: ref in big_data
    error & mismatch & empty: ref in big_data 

    DefaultSort
    result: ref in big_data
    error & mismatch & empty: ref in test_result 
    """
    def __init__(self, client, db_name='stockSdkTest') -> None:
        """
        @param client: 传入一个Mongodb的client
        """
        super().__init__()
        self.__client = client
        self.__db = client[db_name]

    def __create_ref_object(self, collection, raw_object):
        """
        :return reference ObjectId in collection
        """
        try:
            result = collection.insert_one(raw_object)
            return result.inserted_id
        except Exception as e:
            print('insert error: %s' % raw_object)
            return None

    def __find_ref_object(self, collection, raw_object):
        """
        :return reference ObjectId in collection
        """
        try:
            result = collection.find_one(raw_object)
            return result['_id']
        except Exception as e:
            return None

    def __docs_to_inserted_refs(self, collection, docs):
        refs = list()
        if docs is None or len(docs) == 0:
            return refs
        inserted_count = 0
        for doc in docs:
            if is_ref_id(doc):
                refs.append(doc)
                continue
            ref = self.__create_ref_object(collection, doc)
            if ref is None:
                refs.append(doc)
            else:
                inserted_count += 1
                refs.append(ref)
        if inserted_count > 0:
            print('inserted %d items to %s' % (inserted_count, collection.name))
        return refs

    def __docs_to_found_refs(self, collection, docs, build_query_func):
        refs = list()
        if docs is None or len(docs) == 0:
            return refs
        found_count = 0
        for doc in docs:
            if is_ref_id(doc):
                refs.append(doc)
                continue
            ref = self.__find_ref_object(collection, (doc if build_query_func is None else build_query_func(doc)))
            if ref is None:
                refs.append(doc)
            else:
                found_count += 1
                refs.append(ref)
        if found_count > 0:
            print('find %d items at %s' % (found_count, collection.name))
        return refs

    def write_record(self, record, collection_name):
        new_record = dict(record)
        rtype = record['type']

        final_col = self.__db[collection_name]
        col_big_data = self.__db['big_data']
        col_test_result = self.__db['test_result']

        def build_query_by_record_id(item):
            if not is_empty(item, 'recordID'):
                return dict({ 'recordID': item.get('recordID') })
            else:
                query = dict(item)
                del query['_id']
                return query

        if rtype == 'Quote':
            new_record['result'] = dict({ 
                'true': self.__docs_to_inserted_refs(collection=col_big_data, docs=record.get('result', {}).get('true', [])), 
                'false': self.__docs_to_inserted_refs(collection=col_big_data, docs=record.get('result', {}).get('false', [])), 
                'unknown': self.__docs_to_inserted_refs(collection=col_big_data, docs=record.get('result', {}).get('unknown', []))
            })

            new_record['error'] = self.__docs_to_inserted_refs(collection=col_big_data, docs=record.get('error', []))
            new_record['mismatch'] = self.__docs_to_inserted_refs(collection=col_big_data, docs=record.get('mismatch', []))
            new_record['empty'] = self.__docs_to_inserted_refs(collection=col_big_data, docs=record.get('empty', []))
        elif rtype == 'Sort':
            new_record['result'] = dict({ 
                'true': self.__docs_to_inserted_refs(collection=col_big_data, docs=record.get('result', {}).get('true', [])), 
                'false': self.__docs_to_inserted_refs(collection=col_big_data, docs=record.get('result', {}).get('false', [])), 
                'unknown': self.__docs_to_inserted_refs(collection=col_big_data, docs=record.get('result', {}).get('unknown', []))
            })

            new_record['error'] = self.__docs_to_found_refs(collection=col_test_result, docs=record.get('error', []), build_query_func=build_query_by_record_id)
            new_record['mismatch'] = self.__docs_to_found_refs(collection=col_test_result, docs=record.get('mismatch', []), build_query_func=build_query_by_record_id)
            new_record['empty'] = self.__docs_to_found_refs(collection=col_test_result, docs=record.get('empty', []), build_query_func=build_query_by_record_id)
        elif rtype == 'Default':
            new_record['result'] = dict({ 
                'true': self.__docs_to_inserted_refs(collection=col_big_data, docs=record.get('result', {}).get('true', [])), 
                'false': self.__docs_to_inserted_refs(collection=col_big_data, docs=record.get('result', {}).get('false', [])), 
                'unknown': self.__docs_to_inserted_refs(collection=col_big_data, docs=record.get('result', {}).get('unknown', []))
            })

            new_record['error'] = self.__docs_to_inserted_refs(collection=col_big_data, docs=record.get('error', []))
            new_record['mismatch'] = self.__docs_to_inserted_refs(collection=col_big_data, docs=record.get('mismatch', []))
            new_record['empty'] = self.__docs_to_inserted_refs(collection=col_big_data, docs=record.get('empty', []))
        elif rtype == 'DefaultSort':
            new_record['result'] = dict({ 
                'true': self.__docs_to_inserted_refs(collection=col_big_data, docs=record.get('result', {}).get('true', [])), 
                'false': self.__docs_to_inserted_refs(collection=col_big_data, docs=record.get('result', {}).get('false', [])), 
                'unknown': self.__docs_to_inserted_refs(collection=col_big_data, docs=record.get('result', {}).get('unknown', [])),
                'sort1': {
                    'true': self.__docs_to_inserted_refs(collection=col_big_data, docs=record.get('result', {}).get('sort1', {}).get('true', [])),
                    'false': self.__docs_to_inserted_refs(collection=col_big_data, docs=record.get('result', {}).get('sort1', {}).get('false', [])),
                    'unknown': self.__docs_to_inserted_refs(collection=col_big_data, docs=record.get('result', {}).get('sort1', {}).get('unknown', []))
                },
                'sort2': {
                    'true': self.__docs_to_inserted_refs(collection=col_big_data, docs=record.get('result', {}).get('sort2', {}).get('true', [])),
                    'false': self.__docs_to_inserted_refs(collection=col_big_data, docs=record.get('result', {}).get('sort2', {}).get('false', [])),
                    'unknown': self.__docs_to_inserted_refs(collection=col_big_data, docs=record.get('result', {}).get('sort2', {}).get('unknown', []))
                }
            })

            new_record['error'] = self.__docs_to_found_refs(collection=col_test_result, docs=record.get('error', []), build_query_func=build_query_by_record_id)
            new_record['mismatch'] = self.__docs_to_found_refs(collection=col_test_result, docs=record.get('mismatch', []), build_query_func=build_query_by_record_id)
            new_record['empty'] = self.__docs_to_found_refs(collection=col_test_result, docs=record.get('empty', []), build_query_func=build_query_by_record_id)
        else:
            raise Exception('unsupported type %s' % rtype)

        result = final_col.insert_one(new_record)
        print('Final record inserted in %s _id is: %s' % (final_col.name, result.inserted_id))


    def write_file_result_record(self, result):
        pass
