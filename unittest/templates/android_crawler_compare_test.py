from urllib3 import PoolManager
import json
from airflow.utils.timezone import datetime, parse as parse_datetime, utcnow
from datetime import timedelta

from unittest.templates.helper import get_conf
from utils import AirflowRestClient

if __name__ == '__main__':
    DAG_ID = 'android_crawler_compare'
    execution_on_date = '2020-02-11T04:13:50'
    rest = AirflowRestClient()
    execution_date = utcnow() + timedelta(minutes=1)
    datetime_string = execution_date.isoformat()
    conf = get_conf(obj_id="5f9f7ca367a9cd0001e8c928")
    data = json.dumps({
        'conf': conf
    })
    # data = json.dumps({
    #     'conf': {
    #         'collectionName': 'test_result',
    #         'Level': '1',
    #         'HKPerms': ['hk10'],
    #         'roundIntervalSec': '3',
    #         'tag': [['release-20200414-0.0.2', '7ee476fdb9f915d9f97bc529d4a72e4c3249b4f3']],
    #         'run_times': '1',
    #         'quote_detail': '1',
    #         "AirflowMethod": [
    #             {
    #                 'testcaseID': 'CRAWLER_CHARTV2TEST_2',
    #                 'paramStrs': [
    #                     {
    #                         'CODE_A': '600000.sh',
    #                         'CODE_P': '600000.sh',
    #                         'SUBTYPE': 'SH1001',
    #                         'TYPE': 'ChartTypeBeforeData',
    #                         'DURATION_SECONDS': 60,
    #                     },
    #                 ]}
    #         ],
    #         'server': [
    #             {
    #                 'serverSites1': [
    #                     ["sh", "http://114.80.155.134:22016"],
    #                     ["tcpsh", "http://114.80.155.134:22017"],
    #                 ]
    #             },
    #             {
    #                 'serverSites2': []
    #             }
    #         ]
    #     },
    #     #'execution_date': '2020-04-06 02:58:16'
    #     #'execution_date': datetime_string
    # })
    res = rest.trigger_dag(DAG_ID=DAG_ID, data=data)
    print(execution_date)
    print(res)
