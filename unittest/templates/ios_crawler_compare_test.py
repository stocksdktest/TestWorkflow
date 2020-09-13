from urllib3 import PoolManager
import json
from airflow.utils.timezone import datetime, parse as parse_datetime, utcnow
from datetime import timedelta

from utils import AirflowRestClient

if __name__ == '__main__':
    DAG_ID = 'ios_crawler_compare'
    execution_on_date = '2020-02-11T04:13:50'
    rest = AirflowRestClient()
    execution_date = utcnow() + timedelta(minutes=1)
    datetime_string = execution_date.isoformat()
    data = json.dumps({
        'conf': {
            'collectionName': 'test_result',
            'Level': '1',
            'HKPerms': ['hk10'],
            'roundIntervalSec': '3',
            'tag': [['release-20200324-0.0.2', '9175a6e9a1147c9b82ccaa57b484b2ba906a8363']],
            'run_times': '1',
            'quote_detail': '1',
            "AirflowMethod": [
                {
                    'testcaseID': 'CRAWLER_CHARTV2TEST_2',
                    'paramStrs': [
                        {
                            'CODE_A': '600000.sh',
                            'CODE_P': '600000.sh',
                            'SUBTYPE': 'SH1001',
                            'TYPE': 'ChartTypeBeforeData',
                            'DURATION_SECONDS': 60,
                        },
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
                    'serverSites2': []
                }
            ]
        },
        #'execution_date': '2020-04-06 02:58:16'
        'execution_date': datetime_string
    })
    res = rest.trigger_dag(DAG_ID=DAG_ID, data=data)
    print(execution_date)
    print(res)
