import json

import airflow
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator

from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig
from operators.android_runner_operator import AndroidRunnerOperator
from operators.android_release_operator import AndroidReleaseOperator

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

    android_release = AndroidReleaseOperator(
        task_id='android_release',
        provide_context=False,
        repo_name='stocksdktest/AndroidTestRunner',
        tag_id='release-20191016-0.0.3',
        tag_sha='16a5ad8d128df1b55f962b52e87bac481f98475f',
        runner_conf=runner_conf
    )

    android_tc = AndroidRunnerOperator(
        task_id='adb_shell',
        provide_context=False,
        apk_id='com.chi.ssetest',
        apk_version='release-20191016-0.0.3',
        runner_conf=runner_conf
    )

    android_release >> android_tc >> run_this_last

if __name__ == "__main__":
    dag.cli()
