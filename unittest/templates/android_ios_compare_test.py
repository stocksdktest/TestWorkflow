from urllib3 import PoolManager
import json
from airflow.utils.timezone import datetime, parse as parse_datetime, utcnow
from datetime import timedelta

from unittest.templates.helper import get_conf
from utils import AirflowRestClient

default_conf = {
    'collectionName': 'test_result',
    'Level': '1',
    'HKPerms': ['hk10'],
    'roundIntervalSec': '3',
    'tag': [
         ['release-20200504-0.0.2', '6707f368f5612ecbcc0067752bb0d73aed923740'],
         ['release-20200525-0.0.0', '6394b5d191b18c1feb2d2519364141602af6b7cb']
    ],
    'run_times': '1',
    'quote_detail': '1',
    "AirflowMethod": [
        {
            'testcaseID': 'QUOTEDETAILTCPTEST_1',
            'paramStrs': [
                {
                    'CODE': '600000.sh',
                    'SECONDS': '100'
                }
            ]}
    ],
    'server': [
        {
            'serverSites1': [
                ["sh","http://114.80.155.134:22016","tcp://114.80.155.134:22017"],
                ["tcpsh", "http://114.80.155.134:22017"],
                ["sz", "http://114.80.155.134:22016"],
            ]
        },
        {
            'serverSites2': []
        }
    ]
}

if __name__ == '__main__':
    DAG_ID = 'android_ios_compare'
    #execution_on_date = '2020-02-11T04:13:50'
    rest = AirflowRestClient()
    #execution_date = utcnow() + timedelta(minutes=1)
    execution_date = utcnow()
    datetime_string = execution_date.isoformat()
    conf = get_conf(obj_id="5f8a403567a9cd0001e8c1e9")
    data = json.dumps({
        'conf': conf
    })
    # data = json.dumps({
    #     'conf': default_conf,
    #     'execution_date': datetime_string
    # })
    res = rest.trigger_dag(DAG_ID=DAG_ID, data=data)
    print(execution_date)
    print(res)
