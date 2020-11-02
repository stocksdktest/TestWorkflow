import json
from datetime import timedelta

import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator

from operators.android_runner_operator import AndroidRunnerOperator
from operators.data_compare_operator import DataCompareOperator, generate_id
from operators.ios_release_operator import IOSReleaseOperator
from operators.ios_runner_operator import IOSRunnerOperator
from operators.android_release_operator import AndroidReleaseOperator
from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig, Site
from init_config import initRunnerConfig, init_dag_tags, init_dag_params
from init_config import initRunConf
#import pymongo

params = {'Level_tmp':"1", 'HKPerms_tmp':["hk10"], 'collectionName_tmp':"test_result", 'roundIntervalSec_tmp':3, 'AirflowMethod':[
                {
                    'testcaseID': 'CHARTV2TEST_1',
                    'paramStrs': [
                        {
                            'CODE': '600000.sh',
                            'TYPE': 'ChartTypeOneDay',
                            'SUBTYPE': '1001'
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
        dag_id='android_ios_compare',
        default_args={
            'owner': 'jsj',
            'start_date': airflow.utils.dates.days_ago(0),
        },
        schedule_interval='@once',
) as dag:
    conf = dag.get_dagrun(execution_date=dag.latest_execution_date).conf

    start_task = DummyOperator(
        task_id='run_this_first',
        queue='worker'
    )

    release_ok = DummyOperator(
        task_id='release_ok',
        queue='worker'
    )

    run_this_last = DummyOperator(
        task_id='run_this_last',
        queue='worker'
    )

    runner_conf_list = initRunnerConfig(conf, params)
    task_id_to_cmp_list = ['android_cmp', 'android_cmpios_cmp']

    # sdk版本配置
    default_tag = [
            ['release-20200324-0.0.2', '9175a6e9a1147c9b82ccaa57b484b2ba906a8363'],
            ['release-20200323-0.0.3', 'c5a5455c0060b286171cea7e4509a42a31351d1f']
        ]
    tag_id_1, tag_id_2, tag_sha_1, tag_sha_2 = init_dag_tags(conf, default_tag)

    # dag参数配置
    run_times_tmp, quote_detail_tmp, tcp_times_tmp = init_dag_params(conf)

    android_release = AndroidReleaseOperator(
        task_id='android_release',
        provide_context=False,
        repo_name='stocksdktest/AndroidTestRunner',
        tag_id=tag_id_1,
        tag_sha=tag_sha_1,
        runner_conf=runner_conf_list[0]
    )

    ios_release = IOSReleaseOperator(
        task_id='ios_release',
        provide_context=False,
        repo_name='stocksdktest/IOSTestRunner',
        tag_id=tag_id_2,
        tag_sha=tag_sha_2,
        runner_conf=runner_conf_list[1]
    )

    android = AndroidRunnerOperator(
        task_id=task_id_to_cmp_list[0],
        provide_context=False,
        apk_id='com.chi.ssetest',
        apk_version=tag_id_1,
        runner_conf=runner_conf_list[0],
        config_file=True,
        run_times=run_times_tmp
    )

    ios = IOSRunnerOperator(
        task_id=task_id_to_cmp_list[1],
        provide_context=False,
        app_version=tag_id_2,
        runner_conf=runner_conf_list[1],
        config_file=True,
        run_times=run_times_tmp
    )

    runner_conf_cmp = runner_conf_list[0]

    android_ios_cmp = DataCompareOperator(
        task_id='data_compare',
        task_id_list=task_id_to_cmp_list,
        retries=3,
        provide_context=False,
        runner_conf=runner_conf_cmp,
        run_times=run_times_tmp,
        quote_detail=quote_detail_tmp,
        dag=dag
    )

    start_task >> [android_release, ios_release] >> release_ok >> [android, ios] >> android_ios_cmp >> run_this_last

if __name__ == "__main__":
    dag.cli()

