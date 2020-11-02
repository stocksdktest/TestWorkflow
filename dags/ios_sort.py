import json

import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
from operators.data_sorting_operator import DataSortingOperator
from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig, Site
from operators.ios_release_operator import IOSReleaseOperator
from operators.ios_runner_operator import IOSRunnerOperator
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
                    'serverSites1':[
                        ["sh", "http://114.80.155.134:22016"],
                        ["tcpsh", "http://114.80.155.134:22017"],
                        ["shl2", "http://114.80.155.62:22016"],
                    ]
                },
                {
                    'serverSites2':[
                        ["sh", "http://114.80.155.134:22016"],
                        ["tcpsh", "http://114.80.155.134:22017"],
                        ["shl2", "http://114.80.155.62:22016"],
                    ]
                }
            ], 'testcaseID':"CHARTV2TEST_1"}


with DAG(
        dag_id='ios_sort',
        default_args={
            'owner': 'jsj',
            'start_date': airflow.utils.dates.days_ago(0)
        },
        schedule_interval='@once',
) as dag:
    conf = dag.get_dagrun(execution_date=dag.latest_execution_date).conf
    print("Get conf :", conf)
    # conf = {
    #     'collectionName': 'test_result',
    #     'Level': '1',
    #     'HKPerms': ['hk10'],
    #     'roundIntervalSec': '3',
    #     'tag': [['release-20200310-0.0.5', '9e2d1a04b6dba6e800cafadd5046b777326c8bfd']],
    #     "AirflowMethod": [
    #         {
    #             'testcaseID': 'CATESORTING_2',
    #             'paramStrs': [
    #                 {
    #                     'CateType': 'SH1133',
    #                     'param': '0,50,0,0,1',
    #                     'STOCKFIELDS': '-1',
    #                     'ADDVALUEFIELDS': '-1'
    #                 },
    #                 {
    #                     'CateType': 'SH1133',
    #                     'param': '0,50,0,1,1',
    #                     'STOCKFIELDS': '-1',
    #                     'ADDVALUEFIELDS': '-1'
    #                 },
    #                 {
    #                     'CateType': 'SH1133',
    #                     'param': '0,50,1,0,1',
    #                     'STOCKFIELDS': '-1',
    #                     'ADDVALUEFIELDS': '-1'
    #                 }
    #             ]}
    #     ],
    #     'server': [
    #         {
    #             'serverSites1': [
    #                 ["sh", "http://114.80.155.134:22016"],
    #                 ["tcpsh", "http://114.80.155.134:22017"],
    #             ]
    #         },
    #         {
    #             'serverSites2': [
    #                 ["sh", "http://114.80.155.134:22016"],
    #                 ["shl2", "http://114.80.155.62:22016"],
    #             ]
    #         }
    #     ]
    # }
    # sdk版本配置
    default_tag = [['release-20200324-0.0.2', '9175a6e9a1147c9b82ccaa57b484b2ba906a8363']]
    tag_id_1, tag_id_2, tag_sha_1, tag_sha_2 = init_dag_tags(conf, default_tag)

    runner_conf_list = initRunnerConfig(conf, params)
    runner_conf_default = runner_conf_list[0]
    release_task_list = ['ReleaseOperator1', 'ReleaseOperator2']
    runner_task_list = ['RunnerOperator1', 'RunnerOperator2']

    start_task = DummyOperator(
        task_id='run_this_first',
        queue='worker'
    )

    run_this_last = DummyOperator(
        task_id='run_this_lastok',
        queue='worker'
    )

    ios_release1 = IOSReleaseOperator(
        task_id=release_task_list[0],
        provide_context=False,
        repo_name='stocksdktest/IOSTestRunner',
        tag_id=tag_id_1,
        tag_sha=tag_sha_1,
        runner_conf=runner_conf_list[0],
        release_xcom_key = "ios_release_a"
    )

    ios_release2 = IOSReleaseOperator(
        task_id=release_task_list[1],
        provide_context=False,
        repo_name='stocksdktest/IOSTestRunner',
        tag_id=tag_id_2,
        tag_sha=tag_sha_2,
        runner_conf=runner_conf_list[1],
        release_xcom_key = "ios_release_b"
    )

    ios_runner1 = IOSRunnerOperator(
        task_id=runner_task_list[0],
        provide_context=False,
        # apk_id='com.chi.ssetest',
        app_version=tag_id_1,
        runner_conf=runner_conf_list[0],
        config_file=True,
        run_times=100,
        release_xcom_key = "ios_release_a"
    )

    ios_runner2 = IOSRunnerOperator(
        task_id=runner_task_list[1],
        provide_context=False,
        # apk_id='com.chi.ssetest',
        app_version=tag_id_2,
        runner_conf=runner_conf_list[1],
        config_file=True,
        run_times=100,
        release_xcom_key = "ios_release_b"
    )

    ios_sort_1 = DataSortingOperator(
        task_id='SortOperator1',
        from_task=runner_task_list[0],
        retries=3,
        provide_context=False,
        runner_conf=runner_conf_default,
        dag=dag,
        release_xcom_key = "ios_release_a"
    )

    ios_sort_2 = DataSortingOperator(
        task_id='SortOperator2',
        from_task=runner_task_list[1],
        retries=3,
        provide_context=False,
        runner_conf=runner_conf_default,
        dag=dag,
        release_xcom_key = "ios_release_b"
    )

    start_task >> [ios_release1, ios_release2]
    ios_release1 >> ios_runner1 >> ios_sort_1
    ios_release2 >> ios_runner2 >> ios_sort_2
    [ios_sort_1, ios_sort_2] >> run_this_last

if __name__ == "__main__":
    dag.cli()
