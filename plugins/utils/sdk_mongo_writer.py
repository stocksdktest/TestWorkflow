import time
from collections import defaultdict

from utils.compare_record import StockResultTypes

DEFAULT_COLL = 'big_data'

class SdkMongoWriter(object):
    """
    将比对结果拆分后写入MongoDB，比对结果大致可以分成以下5种类型
    1. 普通对比
    2. 行情对比
    3. 跟帐对比
    4. 排序结果
    5. 对比+排序
    """
    def __init__(self, client) -> None:
        """
        @param client: 传入一个Mongodb的client
        """
        super().__init__()
        self.client = client

    def write_big_record(self, result:dict, keys:list, dbName='stockSdkTest', collectionName=DEFAULT_COLL):
        col = self.client[dbName][collectionName]
        for key in keys:
            values = result.get(key)
            if values is not None and len(values) != 0:
                try:
                    result[key] = col.insert_many(values).inserted_ids
                except Exception as e:
                    print("[DEBUG] Inserting Big Data of {} Error".format(key))

    def write_sort_result_record(self, result, dbName='stockSdkTest', collectionName=DEFAULT_COLL):
        self.write_big_record(
            result=result,
            keys=['true', 'false', 'unknown'],
            dbName=dbName,
            collectionName=collectionName
        )

    def write_result_record(self, result, dbName='stockSdkTest', collectionName=DEFAULT_COLL):
        rtype = result['type']
        compare = result['result']
        ''' :type: dict'''

        if rtype == StockResultTypes.Sort:
            self.write_sort_result_record(result=compare, dbName=dbName, collectionName=collectionName)
        elif rtype == StockResultTypes.File:
            pass
        else:
            if rtype.name.__contains__('Sort'):
                self.write_sort_result_record(result=compare['sort1'], dbName=dbName, collectionName=collectionName)
                self.write_sort_result_record(result=compare['sort2'], dbName=dbName, collectionName=collectionName)

            if rtype.name.__contains__('Default'):
                self.write_big_record(
                    result=compare,
                    keys=['true', 'false'],
                    dbName=dbName,
                    collectionName=collectionName
                )

            if rtype.name.__contains__('Quote'):
                self.write_big_record(
                    result=compare,
                    keys=['true'],
                    dbName=dbName,
                    collectionName=collectionName
                )
                for item in compare['false']:
                    self.write_big_record(
                        result=item,
                        keys=['result'],
                        dbName=dbName,
                        collectionName=collectionName
                    )

        return result






    def write_file_result_record(self, result):
        pass









