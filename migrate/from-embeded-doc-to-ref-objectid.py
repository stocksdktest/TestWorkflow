import pymongo

def create_ref_object(collection, raw_object):
  '''
  :return reference ObjectId in collection
  '''
  try:
    result = collection.insert_one(raw_object)
    return result.inserted_id
  except Exception as e:
    print('insert error: %s' % raw_object)
    return None

def find_ref_object(collection, raw_object):
  '''
  :return reference ObjectId in collection
  '''
  try:
    result = collection.find_one(raw_object)
    return result['_id']
  except Exception as e:
    return None

def is_empty(obj, key):
  return key not in obj or len(obj[key]) == 0 

def is_ref_id(obj):
  return str(type(obj)) == "<class 'bson.objectid.ObjectId'>"

def embedded_doc_to_refs(collection, docs):
  refs = list()
  if docs is None:
    return refs
  inserted_count = 0
  for doc in docs:
    if is_ref_id(doc):
      refs.append(doc)
      continue
    ref = create_ref_object(collection, doc)
    if ref is None:
      refs.append(doc)
    else:
      inserted_count += 1
      refs.append(ref)
  if inserted_count > 0:
    print('inserted %d items to %s' % (inserted_count, collection.name))
  return refs

def find_embedded_doc_to_refs(collection, docs, query_func):
  refs = list()
  if docs is None:
    return refs
  find_count = 0
  for doc in docs:
    if is_ref_id(doc):
      refs.append(doc)
      continue
    ref = None
    if query_func is None:
      ref = find_ref_object(collection, doc)
    else:
      ref = find_ref_object(collection, query_func(doc))
    if ref is None:
      refs.append(doc)
    else:
      find_count += 1
      refs.append(ref)
  if find_count > 0:
    print('find %d items at %s' % (find_count, collection.name))
  return refs

def build_query_by_record_id(item):
  if not is_empty(item, 'recordID'):
    return dict({ 'recordID': item.get('recordID') })
  else:
    query = dict(item)
    del query['_id']
    return query

if __name__ == '__main__':
  conn = pymongo.MongoClient('mongodb://221.228.66.83:30617')
  db = conn['stockSdkTest']
  compare_result = db['compare_result']
  compare_result_migrate = db['compare_result_migrate']
  big_data = db['big_data']
  test_result = db['test_result']

  for src_item in compare_result.find():
    dst_item = dict(src_item)
    # dst_item['_id'] = None
    print('##########################')
    print('process item: %s, type: %s' % (src_item['_id'], src_item['type']))

    if find_ref_object(compare_result_migrate, { '_id': src_item['_id'] }) is not None:
      print('alreay processed, skip ...')
      continue

    if is_empty(src_item, 'result') and is_empty(src_item, 'error') \
      and is_empty(src_item, 'mismatch') and is_empty(src_item, 'empty'):
      compare_result_migrate.insert_one(dst_item)
      print('skip ...')
      continue

    item_type = src_item['type']

    if item_type == 'Quote':
      dst_item['result'] = dict({ 'true': [], 'false': [], 'unknown': [] })
      dst_item['result']['true'] = embedded_doc_to_refs(collection=big_data, docs=src_item.get('result', {}).get('true', []))
      dst_item['result']['false'] = embedded_doc_to_refs(collection=big_data, docs=src_item.get('result', {}).get('false', []))
      dst_item['result']['unknown'] = embedded_doc_to_refs(collection=big_data, docs=src_item.get('result', {}).get('unknown', []))

      dst_item['error'] = embedded_doc_to_refs(collection=big_data, docs=src_item.get('error'))
      dst_item['mismatch'] = embedded_doc_to_refs(collection=big_data, docs=src_item.get('mismatch'))
      dst_item['empty'] = embedded_doc_to_refs(collection=big_data, docs=src_item.get('empty'))
    elif item_type == 'Sort':
      dst_item['result'] = dict({ 'true': [], 'false': [], 'unknown': [] })
      dst_item['result']['true'] = embedded_doc_to_refs(collection=big_data, docs=src_item.get('result', {}).get('true', []))
      dst_item['result']['false'] = embedded_doc_to_refs(collection=big_data, docs=src_item.get('result', {}).get('false', []))
      dst_item['result']['unknown'] = embedded_doc_to_refs(collection=big_data, docs=src_item.get('result', {}).get('unknown', []))

      dst_item['error'] = find_embedded_doc_to_refs(collection=test_result, docs=src_item.get('error'), query_func=build_query_by_record_id)
      dst_item['mismatch'] = find_embedded_doc_to_refs(collection=test_result, docs=src_item.get('mismatch'), query_func=build_query_by_record_id)
      dst_item['empty'] = find_embedded_doc_to_refs(collection=test_result, docs=src_item.get('empty'), query_func=build_query_by_record_id)
    elif item_type == 'Default':
      dst_item['result'] = dict({ 'true': [], 'false': [], 'unknown': [] })
      dst_item['result']['true'] = embedded_doc_to_refs(collection=big_data, docs=src_item.get('result', {}).get('true', []))
      dst_item['result']['false'] = embedded_doc_to_refs(collection=big_data, docs=src_item.get('result', {}).get('false', []))
      dst_item['result']['unknown'] = embedded_doc_to_refs(collection=big_data, docs=src_item.get('result', {}).get('unknown', []))

      dst_item['error'] = embedded_doc_to_refs(collection=big_data, docs=src_item.get('error'))
      dst_item['mismatch'] = embedded_doc_to_refs(collection=big_data, docs=src_item.get('mismatch'))
      dst_item['empty'] = embedded_doc_to_refs(collection=big_data, docs=src_item.get('empty'))
    elif item_type == 'DefaultSort':
      dst_item['result'] = dict({ 
        'true': [], 'false': [], 'unknown': [], 
        'sort1': { 'true': [], 'false': [], 'unknown': [] }, 
        'sort2': { 'true': [], 'false': [], 'unknown': [] } 
      })
      dst_item['result']['true'] = embedded_doc_to_refs(collection=big_data, docs=src_item.get('result', {}).get('true', []))
      dst_item['result']['false'] = embedded_doc_to_refs(collection=big_data, docs=src_item.get('result', {}).get('false', []))
      dst_item['result']['unknown'] = embedded_doc_to_refs(collection=big_data, docs=src_item.get('result', {}).get('unknown', []))

      dst_item['result']['sort1']['true'] = embedded_doc_to_refs(collection=big_data, docs=src_item.get('result', {}).get('sort1', {}).get('true', []))
      dst_item['result']['sort1']['false'] = embedded_doc_to_refs(collection=big_data, docs=src_item.get('result', {}).get('sort1', {}).get('false', []))
      dst_item['result']['sort1']['unknown'] = embedded_doc_to_refs(collection=big_data, docs=src_item.get('result', {}).get('sort1', {}).get('unknown', []))

      dst_item['result']['sort2']['true'] = embedded_doc_to_refs(collection=big_data, docs=src_item.get('result', {}).get('sort2', {}).get('true', []))
      dst_item['result']['sort2']['false'] = embedded_doc_to_refs(collection=big_data, docs=src_item.get('result', {}).get('sort2', {}).get('false', []))
      dst_item['result']['sort2']['unknown'] = embedded_doc_to_refs(collection=big_data, docs=src_item.get('result', {}).get('sort2', {}).get('unknown', []))

      dst_item['error'] = find_embedded_doc_to_refs(collection=test_result, docs=src_item.get('error'), query_func=build_query_by_record_id)
      dst_item['mismatch'] = find_embedded_doc_to_refs(collection=test_result, docs=src_item.get('mismatch'), query_func=build_query_by_record_id)
      dst_item['empty'] = find_embedded_doc_to_refs(collection=test_result, docs=src_item.get('empty'), query_func=build_query_by_record_id)
    else:
      print('not supported type: %s' % item_type)
      continue
    compare_result_migrate.insert_one(dst_item)
