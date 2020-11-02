from urllib3 import PoolManager
import json
from airflow.utils.timezone import datetime, parse as parse_datetime, utcnow
from datetime import timedelta
import pymongo
from bson import ObjectId
from utils import AirflowRestClient

if __name__ == '__main__':
    DAG_ID = 'sort_test'
    #execution_on_date = '2020-02-11T04:13:50'
    rest = AirflowRestClient()
    #execution_date = utcnow() + timedelta(minutes=1)
    execution_date = utcnow()
    datetime_string = execution_date.isoformat()
    client = pymongo.MongoClient("mongodb://221.228.66.83:30617")
    coll = client.get_database('stockSdkTest').get_collection('dagrun_record')
    id = ObjectId("5f87e1e767a9cd0001e8c04c")
    conf = coll.find_one({'_id':id}).get('conf')
    data = json.dumps({
        'conf': conf
    })
    # data = json.dumps({
    #     'conf': {
    #         'collectionName': 'test_result',
    #         'Level': '1',
    #         'HKPerms': ['hk10','hk1'],
    #         'roundIntervalSec': '3',
    #         'tag': [['release-20200414-0.0.2', '7ee476fdb9f915d9f97bc529d4a72e4c3249b4f3']],
    #         'AirflowMethod': [{
    #             'testcaseID': 'CATESORTING_2',
    #             'paramStrs': [
    #                 {
    #                 'CateType': 'SH1133',
    #                 'param': '0,50,0,0,1',
    #                 'STOCKFIELDS': '-1',
    #                 'ADDVALUEFIELDS': '0'
    #             }
    #         ]
    #         }],
    #         'server': [{'serverSites1': [['sh', 'http://114.80.155.61:22016'], ['sz', 'http://114.80.155.61:22016'], ['bj', 'http://114.80.155.61:22016'], ['cf', 'http://114.80.155.61:22016'], ['nf', 'http://114.80.155.58:22013'], ['gf', 'http://114.80.155.61:22016'], ['pb', 'http://114.80.155.61:22016'], ['hk1', 'http://114.80.155.58:8601'], ['hk5', 'http://114.80.155.58:8601'], ['hk10', 'http://114.80.155.58:8601'], ['hka1', 'http://114.80.155.58:8601'], ['hkd1', 'http://114.80.155.58:8601'], ['hkaz', 'http://114.80.155.58:8601'], ['hkdz', 'http://114.80.155.58:8601'], ['sh', 'http://114.80.155.61:22016'], ['sz', 'http://114.80.155.61:22016'], ['bj', 'http://114.80.155.61:22016'], ['cf', 'http://114.80.155.61:22016'], ['nf', 'http://114.80.155.58:22013'], ['gf', 'http://114.80.155.61:22016'], ['pb', 'http://114.80.155.61:22016'], ['hk1', 'http://114.80.155.58:8601'], ['hk5', 'http://114.80.155.58:8601'], ['hk10', 'http://114.80.155.58:8601'], ['hka1', 'http://114.80.155.58:8601'], ['hkd1', 'http://114.80.155.58:8601'], ['hkaz', 'http://114.80.155.58:8601'], ['hkdz', 'http://114.80.155.58:8601'], ['sh', 'http://114.80.155.61:22016'], ['sz', 'http://114.80.155.61:22016'], ['bj', 'http://114.80.155.61:22016'], ['cf', 'http://114.80.155.61:22016'], ['nf', 'http://114.80.155.58:22013'], ['gf', 'http://114.80.155.61:22016'], ['pb', 'http://114.80.155.61:22016'], ['hk1', 'http://114.80.155.58:8601'], ['hk5', 'http://114.80.155.58:8601'], ['hk10', 'http://114.80.155.58:8601'], ['hka1', 'http://114.80.155.58:8601'], ['hkd1', 'http://114.80.155.58:8601'], ['hkaz', 'http://114.80.155.58:8601'], ['hkdz', 'http://114.80.155.58:8601']]}, {'serverSites2': [['sh', 'http://114.80.155.134:22016'], ['sz', 'http://114.80.155.134:22016'], ['bj', 'http://114.80.155.134:22016'], ['cf', 'http://114.80.155.134:22016'], ['nf', 'http://114.80.155.134:22013'], ['gf', 'http://114.80.155.134:22013'], ['pb', 'http://114.80.155.134:22016'], ['hk10', 'http://114.80.155.133:22016'], ['hk1', 'http://114.80.155.133:22016'], ['hk5', 'http://114.80.155.133:22016'], ['sh', 'http://114.80.155.134:22016'], ['sz', 'http://114.80.155.134:22016'], ['bj', 'http://114.80.155.134:22016'], ['cf', 'http://114.80.155.134:22016'], ['nf', 'http://114.80.155.134:22013'], ['gf', 'http://114.80.155.134:22013'], ['pb', 'http://114.80.155.134:22016'], ['hk10', 'http://114.80.155.133:22016'], ['hk1', 'http://114.80.155.133:22016'], ['hk5', 'http://114.80.155.133:22016'], ['sh', 'http://114.80.155.134:22016'], ['sz', 'http://114.80.155.134:22016'], ['bj', 'http://114.80.155.134:22016'], ['cf', 'http://114.80.155.134:22016'], ['nf', 'http://114.80.155.134:22013'], ['gf', 'http://114.80.155.134:22013'], ['pb', 'http://114.80.155.134:22016'], ['hk10', 'http://114.80.155.133:22016'], ['hk1', 'http://114.80.155.133:22016'], ['hk5', 'http://114.80.155.133:22016']]}],
    #     },
    #     'execution_date': datetime_string
    # })
    res = rest.trigger_dag(DAG_ID=DAG_ID, data=data)
    print(execution_date)
    print(res)

