import json

import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

from operators.crawler.runner_operator import CrawlerRunnerOperator
from operators.data_sorting_operator import DataSortingOperator
from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig, Site
from operators.ios_runner_operator import IOSRunnerOperator
from operators.ios_release_operator import IOSReleaseOperator
from operators.data_compare_operator import DataCompareOperator
from init_config import initRunnerConfig, init_dag_tags, init_dag_params
from init_config import initRunConf

params = {'Level_tmp':"1", 'HKPerms_tmp':["hk10"], 'collectionName_tmp':"test_result", 'roundIntervalSec_tmp':3, 'AirflowMethod':[
                {
                    'testcaseID': 'CATESORTING_2',
                    'paramStrs': [
                    {
                        'testcaseID': 'CRAWLER_CHARTV2TEST_2',
                        'paramStrs': [
                            {
                                'CODE_A': '600000.sh',
                                'CODE_P': '600000.sh',
                                'SUBTYPE': 'SH1001',
                                'TYPE': 'ChartTypeBeforeData',
                                'DURATION_SECONDS': 60,
                            }
                        ]
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
                    'serverSites2':[]
                }
            ], 'testcaseID':"L2TICKDETAILV2_1"}


with DAG(
        dag_id='ios_crawler_compare',
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
    #     'tag': [['release-20200324-0.0.2', '9175a6e9a1147c9b82ccaa57b484b2ba906a8363']],
    #     'run_times': '1',
    #     'quote_detail': '1',
    #     "AirflowMethod": [
    #         {
    #             'testcaseID': 'CRAWLER_CHARTV2TEST_2',
    #             'paramStrs': [
    #                 {
    #                     'CODE_A': '600000.sh',
    #                     'CODE_P': '600000.sh',
    #                     'SUBTYPE': 'SH1001',
    #                     'TYPE': 'ChartTypeBeforeData',
    #                     'DURATION_SECONDS': 60,
    #                 },
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
    #             'serverSites2': []
    #         }
    #     ]
    # }

    start_task = DummyOperator(
        task_id='run_this_first',
        queue='worker'
    )

    run_this_last = DummyOperator(
        task_id='run_this_lastok',
        queue='worker'
    )

    runner_config = initRunnerConfig(conf, params)
    task_id_to_compare = ['ios', 'crawler']


    # sdk版本配置
    default_tag = [['release-20200414-0.0.2', '7ee476fdb9f915d9f97bc529d4a72e4c3249b4f3']]
    tag_id_1, tag_id_2, tag_sha_1, tag_sha_2 = init_dag_tags(conf, default_tag)

    # dag参数配置
    run_times_tmp, quote_detail_tmp, tcp_times_tmp = init_dag_params(conf)

    ios_release = IOSReleaseOperator(
        task_id='test_ios',
        provide_context=False,
        repo_name='stocksdktest/IOSTestRunner',
        tag_id=tag_id_1,
        tag_sha=tag_sha_1,
        runner_conf=runner_config
    )

    ios = IOSRunnerOperator(
        task_id=task_id_to_compare[0],
        provide_context=False,
        app_version=tag_id_1,
        runner_conf=runner_config,
        config_file=True,
        run_times=run_times_tmp,
    )

    crawler = CrawlerRunnerOperator(
        task_id=task_id_to_compare[1],
        provide_context=False,
        runner_conf=runner_config,
        run_times=run_times_tmp,
    )

    ios_cmp = DataCompareOperator(
        task_id='data_compare',
        task_id_list=task_id_to_compare,
        retries=3,
        provide_context=False,
        runner_conf=runner_config,
        run_times=run_times_tmp,
        quote_detail=quote_detail_tmp,
        dag=dag,
    )

    start_task >> ios_release >> [ios, crawler] >> ios_cmp >> run_this_last

if __name__ == "__main__":
    dag.cli()
