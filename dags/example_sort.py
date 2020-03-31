import json

import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
from operators.data_sorting_operator import DataSortingOperator
from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig, Site
from operators.android_runner_operator import AndroidRunnerOperator
from operators.android_release_operator import AndroidReleaseOperator


# .a测试，b生产
# TODO init RunnerConfig
def initRunnerConfig():
    runner_conf_list = []
    runner_conf_list.append(RunnerConfig())
    runner_conf_list.append(RunnerConfig())
    return runner_conf_list


with DAG(
        dag_id='example_sort',
        default_args={
            'owner': 'ouyang',
            'start_date': airflow.utils.dates.days_ago(0)
        },
        schedule_interval='@once',
) as dag:
    start_task = DummyOperator(
        task_id='run_this_first',
        queue='worker'
    )

    run_this_last = DummyOperator(
        task_id='run_this_lastok',
        queue='worker'
    )

    runner_conf_list = initRunnerConfig()
    runner_conf_default = runner_conf_list[0]
    release_task_list = ['ReleaseOperator1', 'ReleaseOperator2']
    runner_task_list = ['RunnerOperator1', 'RunnerOperator2']

    android_release1 = AndroidReleaseOperator(
        task_id=release_task_list[0],
        provide_context=False,
        repo_name='stocksdktest/AndroidTestRunner',
        tag_id='release-20200310-0.0.3',
        tag_sha='2c0596339fdf5d09d0954efc7eb567fbeb70be3d',
        runner_conf=runner_conf_list[0]
    )

    android_release2 = AndroidReleaseOperator(
        task_id=release_task_list[1],
        provide_context=False,
        repo_name='stocksdktest/AndroidTestRunner',
        tag_id='release-20200310-0.0.3',
        tag_sha='2c0596339fdf5d09d0954efc7eb567fbeb70be3d',
        runner_conf=runner_conf_list[0]
    )

    android_runner1 = AndroidRunnerOperator(
        task_id=runner_task_list[0],
        provide_context=False,
        apk_id='com.chi.ssetest',
        apk_version='release-20200310-0.0.3',
        runner_conf=runner_conf_list[0],
        config_file=True,
        run_times=100
    )

    android_runner2 = AndroidRunnerOperator(
        task_id=runner_task_list[1],
        provide_context=False,
        apk_id='com.chi.ssetest',
        apk_version='release-20200310-0.0.3',
        runner_conf=runner_conf_list[1],
        config_file=True,
        run_times=100
    )

    android_sort_1 = DataSortingOperator(
        task_id='SortOperator1',
        from_task=runner_task_list[0],
        retries=3,
        provide_context=False,
        runner_conf=runner_conf_default,
        dag=dag
    )

    android_sort_2 = DataSortingOperator(
        task_id='SortOperator2',
        from_task=runner_task_list[1],
        retries=3,
        provide_context=False,
        runner_conf=runner_conf_default,
        dag=dag
    )

    start_task >> [android_release1, android_release2]
    android_release1 >> android_runner1 >> android_sort_1
    android_release2 >> android_runner2 >> android_sort_2
    [android_sort_1, android_sort_2] >> run_this_last

if __name__ == "__main__":
    dag.cli()
