import json

import airflow
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator

from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig
from operators.android_operator import AndroidStockOperator

# TODO init RunnerConfig
runner_conf = RunnerConfig()

runner_conf.sdkConfig.appKeyIOS = 'VVW0Fno7BEZt1a/y6KLM36uj9qcjw7CAHDwWZKDlWDs='
runner_conf.sdkConfig.appKeyAndroid = 'J6IPlk5AEU+2/Yi59rfYnsFQtdtOgAo9GAzysx8ciOM='
runner_conf.sdkConfig.marketPerm.Level = "2"

case_conf = TestcaseConfig()
case_conf.testcaseID = 'TESTCASE_0'
case_conf.continueWhenFailed = False
case_conf.roundIntervalSec = 3
case_conf.paramStrs.extend([
    json.dumps({
        'QUOTE_NUMBERS': '600028.sh'
    })
])

runner_conf.casesConfig.extend([case_conf])

with DAG(
    dag_id='android_test',
    default_args={
        'owner': 'airflow',
        'start_date': airflow.utils.dates.days_ago(0)
    },
    schedule_interval='@once',
) as dag:
    run_this_last = DummyOperator(
        task_id='run_this_last',
        queue='android'
    )

    run_this = AndroidStockOperator(
        task_id='adb_shell',
        provide_context=False,
        runner_conf=runner_conf
    )

    run_this >> run_this_last

if __name__ == "__main__":
    dag.cli()
