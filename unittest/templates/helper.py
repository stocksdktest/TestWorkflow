import pymongo
from bson import ObjectId

def get_conf(obj_id: str):
    client = pymongo.MongoClient("mongodb://221.228.66.83:30617")
    coll = client.get_database('stockSdkTest').get_collection('dagrun_record')
    id = ObjectId(obj_id)
    conf = coll.find_one({'_id':id}).get('conf')
    client.close()
    return conf
