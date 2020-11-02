from urllib3 import PoolManager
import json
from airflow.utils.timezone import datetime, parse as parse_datetime, utcnow
from datetime import timedelta

from init_config import init_dag_tags, initRunnerConfig
from unittest.templates.helper import get_conf
from utils import AirflowRestClient

default_conf =  {
    'collectionName': 'test_result',
    'Level': '1',
    'HKPerms': ['hk10'],
    'roundIntervalSec': '3',
    'tag': [['release-20200310-0.0.5', '9e2d1a04b6dba6e800cafadd5046b777326c8bfd']],
    "AirflowMethod": [
        {
            'testcaseID': 'CATESORTING_2',
            'paramStrs': [
                {
                    'CateType': 'SH1133',
                    'param': '0,50,0,0,1',
                    'STOCKFIELDS': '-1',
                    'ADDVALUEFIELDS': '-1'
                },
                {
                    'CateType': 'SH1133',
                    'param': '0,50,0,1,1',
                    'STOCKFIELDS': '-1',
                    'ADDVALUEFIELDS': '-1'
                },
                {
                    'CateType': 'SH1133',
                    'param': '0,50,1,0,1',
                    'STOCKFIELDS': '-1',
                    'ADDVALUEFIELDS': '-1'
                }
            ]}
    ],
    'server': [
        {
            'serverSites1': [
                ["sh", "http://114.80.155.134:22016"],
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
    DAG_ID = 'ios_sort'
    #execution_on_date = '2020-02-11T04:13:50'
    rest = AirflowRestClient()
    #execution_date = utcnow() + timedelta(minutes=1)
    execution_date = utcnow()
    datetime_string = execution_date.isoformat()

    conf = get_conf(obj_id="5f9fc63367a9cd0001e8c9c3")
    data = json.dumps({
        'conf': conf
    })
    res = rest.trigger_dag(DAG_ID=DAG_ID, data=data)
    print(execution_date)
    print(res)


