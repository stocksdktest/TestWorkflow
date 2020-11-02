from urllib3 import PoolManager
import json
from airflow.utils.timezone import datetime, parse as parse_datetime, utcnow
from datetime import timedelta

from init_config import init_dag_tags, initRunnerConfig
from unittest.templates.helper import get_conf
from utils import AirflowRestClient

if __name__ == '__main__':
    DAG_ID = 'ios_sort'
    #execution_on_date = '2020-02-11T04:13:50'
    rest = AirflowRestClient()
    #execution_date = utcnow() + timedelta(minutes=1)
    execution_date = utcnow()
    datetime_string = execution_date.isoformat()

    conf = get_conf(obj_id="5f977a4167a9cd0001e8c8d8")
    data = json.dumps({
        'conf': conf
    })

    res = rest.trigger_dag(DAG_ID=DAG_ID, data=data)
    print(execution_date)
    print(res)


