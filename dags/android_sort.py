import json

import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
from operators.data_sorting_operator import DataSortingOperator
from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig, Site
from operators.android_runner_operator import AndroidRunnerOperator
from operators.android_release_operator import AndroidReleaseOperator
from operators.data_compare_operator import DataCompareOperator
from init_config import initRunnerConfig, init_dag_tags
from init_config import initRunConf


params = {'Level_tmp':"1", 'HKPerms_tmp':["hk10"], 'collectionName_tmp':"test_result", 'roundIntervalSec_tmp':3, 'AirflowMethod':[
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
                        }
                    ]
                }
            ], 'server':[
                {
                    'serverSites1': [
                        ["sh", "http://114.80.155.134:22016"],
                        ["tcpsh", "http://114.80.155.134:22017"],
                        ["shl2", "http://114.80.155.62:22016"],
                    ]
                },
                {
                    'serverSites2': [
                        ["sh", "http://114.80.155.134:22016"],
                        ["tcpsh", "http://114.80.155.134:22017"],
                        ["shl2", "http://114.80.155.62:22016"],
                    ]
                }
            ], 'testcaseID':"CHARTV2TEST_1"}



with DAG(
        dag_id='android_sort',
        default_args={
            'owner': 'jsj',
            'start_date': airflow.utils.dates.days_ago(0)
        },
        schedule_interval='@once',
) as dag:
    conf = dag.get_dagrun(execution_date=dag.latest_execution_date).conf
    print("Get conf :", conf)

    # sdk版本配置
    default_tag = [['release-20200324-0.0.2', '9175a6e9a1147c9b82ccaa57b484b2ba906a8363']]
    tag_id_1, tag_id_2, tag_sha_1, tag_sha_2 = init_dag_tags(conf, default_tag)

    start_task = DummyOperator(
        task_id='run_this_first',
        queue='worker'
    )

    run_this_last = DummyOperator(
        task_id='run_this_lastok',
        queue='worker'
    )

    runner_conf_list = initRunnerConfig(conf, params)
    runner_conf_default = runner_conf_list[0]
    release_task_list = ['ReleaseOperator1', 'ReleaseOperator2']
    runner_task_list = ['RunnerOperator1', 'RunnerOperator2']
    sort_task_list = ['SortOperator1', 'SortOperator2']

    android_release1 = AndroidReleaseOperator(
        task_id=release_task_list[0],
        provide_context=False,
        repo_name='stocksdktest/AndroidTestRunner',
        tag_id=tag_id_1,
        tag_sha=tag_sha_1,
        runner_conf=runner_conf_list[0],
        release_xcom_key = "android_release_a"
    )

    android_release2 = AndroidReleaseOperator(
        task_id=release_task_list[1],
        provide_context=False,
        repo_name='stocksdktest/AndroidTestRunner',
        tag_id=tag_id_2,
        tag_sha=tag_sha_2,
        runner_conf=runner_conf_list[1],
        release_xcom_key = "android_release_b"
    )

    android_runner1 = AndroidRunnerOperator(
        task_id=runner_task_list[0],
        provide_context=False,
        apk_id='com.chi.ssetest',
        apk_version=tag_id_1,
        runner_conf=runner_conf_list[0],
        config_file=True,
        release_xcom_key = "android_release_a"
    )

    android_runner2 = AndroidRunnerOperator(
        task_id=runner_task_list[1],
        provide_context=False,
        apk_id='com.chi.ssetest',
        apk_version=tag_id_2,
        runner_conf=runner_conf_list[1],
        config_file=True,
        release_xcom_key = "android_release_b"
    )

    android_sort_a = DataSortingOperator(
        task_id=sort_task_list[0],
        from_task=runner_task_list[0],
        sort_and_comprae=True,
        retries=3,
        provide_context=False,
        runner_conf=runner_conf_default,
        dag=dag,
        release_xcom_key = "android_release_a"
    )

    android_sort_b = DataSortingOperator(
        task_id=sort_task_list[1],
        from_task=runner_task_list[1],
        sort_and_comprae=True,
        retries=3,
        provide_context=False,
        runner_conf=runner_conf_default,
        dag=dag,
        release_xcom_key = "android_release_b"
    )

    android_cmp = DataCompareOperator(
        task_id='data_compare',
        task_id_list=runner_task_list,
        sort_id_list=sort_task_list,
        sort_and_comprae=True,
        retries=3,
        provide_context=False,
        runner_conf=runner_conf_default,
        dag=dag
    )

    start_task >> [android_release1, android_release2]
    android_release1 >> android_runner1 >> android_sort_a
    android_release2 >> android_runner2 >> android_sort_b
    [android_sort_a, android_sort_b] >> android_cmp >> run_this_last

if __name__ == "__main__":
    dag.cli()
