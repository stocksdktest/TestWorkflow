import json

import airflow
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator

from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig, SDKPermissions
from operators.android_operator import AndroidStockOperator

# TODO init RunnerConfig
runner_conf = RunnerConfig()

runner_conf.sdkConfig.appKey = 'J6IPlk5AEU+2/Yi59rfYnsFQtdtOgAo9GAzysx8ciOM='
runner_conf.sdkConfig.sdkLevel = SDKPermissions.LEVEL_2
runner_conf.sdkConfig.sdkSseLevel = SDKPermissions.LEVEL_2
runner_conf.sdkConfig.hkPerms.extend([SDKPermissions.HK10])

case_conf = TestcaseConfig()
case_conf.testcaseID = 'TESTCASE_0'
case_conf.executionTimes = 1
case_conf.continueWhenFailed = False
case_conf.paramStr = json.dumps({
	'QUOTE_NUMBERS': '600028.sh,600000.sh,688001.sh'
})

case_conf_2 = TestcaseConfig()
case_conf_2.testcaseID = 'TESTCASE_1'
case_conf_2.executionTimes = 1
case_conf_2.continueWhenFailed = False
case_conf_2.paramStr = json.dumps({
	'QUOTE_NUMBERS': '600028.sh'
})

runner_conf.casesConfig.extend([case_conf, case_conf_2])

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
