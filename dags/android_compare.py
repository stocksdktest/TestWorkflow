import json

import airflow
from airflow import AirflowException
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
from operators.data_compare_operator import DataCompareOperator
from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig, Site
from operators.android_runner_operator import AndroidRunnerOperator
from operators.android_release_operator import AndroidReleaseOperator
from sqlalchemy import Column, PickleType
from init_config import initRunnerConfig, init_dag_params, init_dag_tags
from init_config import initRunConf

params = {'CffLevel_tmp':"1", 'DceLevel_tmp':"2", 'CzceLevel_tmp':"2", 'FeLevel_tmp':"2", 'GILevel_tmp':"2", 'ShfeLevel_tmp':"2",
            'IneLevel_tmp':"2", 'Level_tmp':"2", 'HKPerms_tmp':["hk10"], 'collectionName_tmp':"test_result",
            'roundIntervalSec_tmp':3,
            'AirflowMethod':[{'testcaseID': 'L2TICKDETAILV2_1', 'paramStrs': [{'CODE': '000100.sz', 'SUBTYPE': '1001'},{'CODE': '000078.sz','SUBTYPE': '1001'},{'CODE': '002429.sz','SUBTYPE': '1001'}]}],
            'server':[{'serverSites1':[["sh", "http://114.80.155.134:22016"],["tcpsh", "http://114.80.155.134:22017"],["shl2", "http://114.80.155.62:22016"]]},{'serverSites2':[["sh", "http://114.80.155.134:22016"], ["tcpsh", "http://114.80.155.134:22017"], ["shl2", "http://114.80.155.62:22016"]]}],
            'testcaseID':'L2TICKDETAILV2_1'}

with DAG(
        dag_id='android_compare',  # 测试计划名称
        default_args={
            'owner': 'jsj',
            'start_date': airflow.utils.dates.days_ago(0)
        },
        schedule_interval='@once',
) as dag:
    conf = dag.get_dagrun(execution_date=dag.latest_execution_date).conf
    print("Get conf :", conf)

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

    # 测试用例配置
    runner_conf_list = initRunnerConfig(conf, params)

    task_id_to_cmp_list = ['android_cmp_a', 'android_cmp_b']
    # sdk版本配置
    default_tag = [['release-20200103-0.0.3', '53fcc717d954e01d88bc9bd70eaab9ac9a0acb67']]
    tag_id_1, tag_id_2, tag_sha_1, tag_sha_2 = init_dag_tags(conf, default_tag)

    # dag参数配置
    run_times_tmp, quote_detail_tmp, tcp_times_tmp = init_dag_params(conf)

    android_release_a = AndroidReleaseOperator(
        task_id='android_release_a',
        provide_context=False,
        repo_name='stocksdktest/AndroidTestRunner',
        tag_id=tag_id_1,
        tag_sha=tag_sha_1,
        runner_conf=runner_conf_list[0],
        release_xcom_key = "android_release_a"
    )
    android_release_b = AndroidReleaseOperator(
        task_id='android_release_b',
        provide_context=False,
        repo_name='stocksdktest/AndroidTestRunner',
        tag_id=tag_id_2,
        tag_sha=tag_sha_2,
        runner_conf=runner_conf_list[1],
        release_xcom_key = "android_release_b"
    )

    android_a = AndroidRunnerOperator(
        task_id=task_id_to_cmp_list[0],
        provide_context=False,
        apk_id='com.chi.ssetest',
        apk_version=tag_id_1,
        config_file=True,
        runner_conf=runner_conf_list[0],
        tcp_times=tcp_times_tmp,
        run_times=run_times_tmp,
        release_xcom_key = "android_release_a"
    )

    android_b = AndroidRunnerOperator(
        task_id=task_id_to_cmp_list[1],
        provide_context=False,
        apk_id='com.chi.ssetest',
        apk_version=tag_id_2,
        config_file=True,
        runner_conf=runner_conf_list[1],
        tcp_times=tcp_times_tmp,
        run_times=run_times_tmp,
        release_xcom_key = "android_release_b"
    )

    runner_conf_cmp = runner_conf_list[0]

    android_cmp = DataCompareOperator(
        task_id='data_compare',
        task_id_list=task_id_to_cmp_list,
        retries=3,
        provide_context=False,
        runner_conf=runner_conf_cmp,
        run_times=run_times_tmp,
        quote_detail=quote_detail_tmp,
        dag=dag
    )
    start_task >> [android_release_a, android_release_b] >> release_ok >> [android_a,android_b] >> android_cmp >> run_this_last
if __name__ == "__main__":
    dag.cli()