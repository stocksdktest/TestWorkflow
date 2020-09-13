from urllib3 import PoolManager
import json
from airflow.utils.timezone import datetime, parse as parse_datetime, utcnow
from datetime import timedelta

from utils import AirflowRestClient

if __name__ == '__main__':
    DAG_ID = 'ios_compare4'
    #execution_on_date = '2020-02-11T04:13:50'
    rest = AirflowRestClient()
    # res = rest.get_dag_runs(DAG_ID=DAG_ID)
    # res = rest.get_dag_runs_instance(DAG_ID=DAG_ID,exeution_on_date=execution_on_date)
    # res = rest.get_dag_task_instance(DAG_ID=DAG_ID, exeution_on_date=execution_on_date, TASK_ID='push_by_returning')
    # res = rest.get_server_status()
    # res = rest.pause_dag(DAG_ID=DAG_ID, paused=True)
    # res = rest.get_lastest_runs()
    # res = rest.get_pools()

    #execution_date = utcnow() + timedelta(minutes=1)
    execution_date = utcnow()
    datetime_string = execution_date.isoformat()
    data = json.dumps({
        'conf': {
            'collectionName': 'test_result',
            'Level': '1',
            'HKPerms': ['hk10', 'hk1'],
            'roundIntervalSec': '3',
            'tag': [['release-20200407-0.0.0', '3c675c4f051324a0d460080d77e0f447cfeb8539']],
            'run_times': '1',
            'quote_detail': '0',
            "AirflowMethod": [{'testcaseID': ' OHLCV3_1', 'paramStrs': [{'SUBTYPE': '1001', 'CODE': '601558.sh', 'PERIOD': 'dayk'}, {'SUBTYPE': '1001', 'CODE': '600313.sh', 'PERIOD': 'dayk'}, {'SUBTYPE': '1001', 'CODE': '600108.sh', 'PERIOD': 'dayk'}, {'SUBTYPE': '1001', 'CODE': '601777.sh', 'PERIOD': 'dayk'}, {'SUBTYPE': '1001', 'CODE': '603993.sh', 'PERIOD': 'dayk'}, {'SUBTYPE': '1001', 'CODE': '600410.sh', 'PERIOD': 'dayk'}, {'SUBTYPE': '1001', 'CODE': '600191.sh', 'PERIOD': 'dayk'}, {'SUBTYPE': '1001', 'CODE': '600467.sh', 'PERIOD': 'dayk'}, {'SUBTYPE': '1001', 'CODE': '600438.sh', 'PERIOD': 'dayk'}, {'SUBTYPE': '1001', 'CODE': '601857.sh', 'PERIOD': 'dayk'}]}],
            'server': [{'serverSites1': [['sh', 'http://114.80.155.134:22016'], ['sz', 'http://114.80.155.134:22016'], ['bj', 'http://114.80.155.134:22016'], ['cf', 'http://114.80.155.134:22016'], ['nf', 'http://114.80.155.134:22013'], ['gf', 'http://114.80.155.134:22013'], ['pb', 'http://114.80.155.134:22016'], ['hk10', 'http://114.80.155.133:22016'], ['hk1', 'http://114.80.155.133:22016'], ['hk5', 'http://114.80.155.133:22016']]}, {'serverSites2': [['sh', 'http://27.151.2.87:22016'], ['sz', 'http://27.151.2.87:22016'], ['bj', 'http://27.151.2.87:22016'], ['cf', 'http://27.151.2.87:22016'], ['nf', 'http://58.63.252.23:22013'], ['gf', 'http://27.151.2.87:22016'], ['pb', 'http://27.151.2.87:22016'], ['hk10', 'http://58.63.252.56:22016']]}],
        },
        'execution_date': datetime_string
    })
    res = rest.trigger_dag(DAG_ID=DAG_ID, data=data)
    print(execution_date)
    print(res)
