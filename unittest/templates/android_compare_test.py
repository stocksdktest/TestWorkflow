from urllib3 import PoolManager
import json
from airflow.utils.timezone import datetime, parse as parse_datetime, utcnow
from datetime import timedelta

from unittest.templates.helper import get_conf
from utils import AirflowRestClient

default_conf = {
    'collectionName': 'Test_Android_quote_20200316',
    'Level': '2',
    'CffLevel':'1',
    'DceLevel':'2',
    'CzceLevel':'2',
    'FeLevel':'2',
    'GILevel':'2',
    'ShfeLevel':'2',
    'IneLevel':'2',
    'HKPerms': ['hk10'],
    'roundIntervalSec': '3',
    'tag': [['release-20200103-0.0.3', '53fcc717d954e01d88bc9bd70eaab9ac9a0acb67']],
    'run_times': '1',
    'quote_detail': '1',
    "AirflowMethod": [
        {
            'testcaseID': 'L2TICKDETAILV2_1',
            'paramStrs': [
                {
                    'CODE': '000100.sz',
                    'SUBTYPE': '1001'
                },
                {
                    'CODE': '000078.sz',
                    'SUBTYPE': '1001'
                },
                {
                    'CODE': '002429.sz',
                    'SUBTYPE': '1001'
                }
            ]}
    ],
    'server': [
        {
            'serverSites1': [
                ["sh", "http://114.80.155.134:22016","tcp://114.80.155.134:22017"],
                ["tcpsh", "http://114.80.155.134:22017"],
            ]
        },
        {
            'serverSites2': [
                ["sh", "http://114.80.155.134:22016"],
                ["shl2", "http://114.80.155.62:22016"],
            ]
        }
    ]
}

if __name__ == '__main__':
    DAG_ID = 'android_compare'
    execution_on_date = '2020-02-11T04:13:50'
    rest = AirflowRestClient()
    execution_date = utcnow() + timedelta(minutes=1)
    datetime_string = execution_date.isoformat()

    conf = get_conf(obj_id="5f87e27867a9cd0001e8c04e")
    data = json.dumps({
        'conf': conf
    })

    # data = json.dumps({
    #     'conf': default_conf,
    #     #'execution_date': '2020-04-06 02:58:16'
    #     #'execution_date': datetime_string
    # })
    print("data is ", data)
    res = rest.trigger_dag(DAG_ID=DAG_ID, data=data)
    print(execution_date)
    print(res)

    print(conf)