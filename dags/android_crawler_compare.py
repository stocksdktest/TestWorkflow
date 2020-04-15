import json

import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

from operators.crawler.runner_operator import CrawlerRunnerOperator
from operators.data_sorting_operator import DataSortingOperator
from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig, Site
from operators.android_runner_operator import AndroidRunnerOperator
from operators.android_release_operator import AndroidReleaseOperator
from operators.data_compare_operator import DataCompareOperator


# .a测试，b生产
# TODO init RunnerConfig
def initRunnerConfig():

    runner_conf = RunnerConfig()

    runner_conf.sdkConfig.appKeyIOS = 'VVW0Fno7BEZt1a/y6KLM36uj9qcjw7CAHDwWZKDlWDs='
    runner_conf.sdkConfig.appKeyAndroid = 'J6IPlk5AEU+2/Yi59rfYnsFQtdtOgAo9GAzysx8ciOM='
    runner_conf.sdkConfig.marketPerm.Level = "1"
    runner_conf.sdkConfig.marketPerm.HKPerms.extend(["hk10"])
    # mongoDB位置，存储的数据库位置
    runner_conf.storeConfig.mongoUri = "mongodb://221.228.66.83:30617"
    runner_conf.storeConfig.dbName = "stockSdkTest"
    runner_conf.storeConfig.collectionName = "test_result"

    runner_conf.sdkConfig.serverSites["sh"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
    runner_conf.sdkConfig.serverSites["tcpsh"].CopyFrom(Site(ips=["http://114.80.155.61:22017"]))
    runner_conf.sdkConfig.serverSites["shl2"].CopyFrom(Site(ips=["http://114.80.155.50:22016"]))
    runner_conf.sdkConfig.serverSites["tcpshl2"].CopyFrom(Site(ips=["http://114.80.155.50:22017"]))
    runner_conf.sdkConfig.serverSites["sz"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
    runner_conf.sdkConfig.serverSites["szl2"].CopyFrom(Site(ips=["http://114.80.155.57:22016"]))
    runner_conf.sdkConfig.serverSites["tcpsz"].CopyFrom(Site(ips=["http://114.80.155.61:22017"]))
    runner_conf.sdkConfig.serverSites["tcpszl2"].CopyFrom(Site(ips=["http://114.80.155.61:22017"]))
    runner_conf.sdkConfig.serverSites["bj"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
    runner_conf.sdkConfig.serverSites["cf"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
    runner_conf.sdkConfig.serverSites["nf"].CopyFrom(Site(ips=["http://114.80.155.61:22013"]))
    runner_conf.sdkConfig.serverSites["gf"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
    runner_conf.sdkConfig.serverSites["pb"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
    runner_conf.sdkConfig.serverSites["hk1"].CopyFrom(Site(ips=["http://114.80.155.58:8601"]))
    runner_conf.sdkConfig.serverSites["hk5"].CopyFrom(Site(ips=["http://114.80.155.58:8601"]))
    runner_conf.sdkConfig.serverSites["hk10"].CopyFrom(Site(ips=["http://114.80.155.58:8601"]))
    runner_conf.sdkConfig.serverSites["hka1"].CopyFrom(Site(ips=["http://114.80.155.58:8601"]))
    runner_conf.sdkConfig.serverSites["hkd1"].CopyFrom(Site(ips=["http://114.80.155.61:7710"]))
    runner_conf.sdkConfig.serverSites["hkaz"].CopyFrom(Site(ips=["http://114.80.155.58:8601"]))
    runner_conf.sdkConfig.serverSites["hkdz"].CopyFrom(Site(ips=["http://114.80.155.61:7710"]))


    # 接口 测试样例
    case_conf = TestcaseConfig()
    case_conf.testcaseID = 'CRAWLER_QUOTEDETAIL_1'
    case_conf.continueWhenFailed = True
    case_conf.roundIntervalSec = 3
    case_conf.paramStrs.extend([
        json.dumps({
            'CODE_A': '688001.sh',
            'CODE_P': '688001.sh',
            'SUBTYPE': 'SH1006',
            'SHSC': 'KCB',
            'DURATION_SECONDS': 60,
            'STARTDATE': '2020-03-01-13-10-00',
            'ENDDATE': '2020-04-03-10-10-00',
        })
    ])
    runner_conf.casesConfig.extend([case_conf])

    return runner_conf


with DAG(
        dag_id='example_android_crawler_compare',
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

    runner_config = initRunnerConfig()
    task_id_to_compare = ['android', 'crawler']

    android_release = AndroidReleaseOperator(
        task_id='test_android',
        provide_context=False,
        repo_name='stocksdktest/AndroidTestRunner',
        tag_id='release-20200414-0.0.2',
        tag_sha='7ee476fdb9f915d9f97bc529d4a72e4c3249b4f3',
        runner_conf=runner_config
    )

    android = AndroidRunnerOperator(
        task_id=task_id_to_compare[0],
        provide_context=False,
        apk_id='com.chi.ssetest',
        apk_version='release-20200414-0.0.2',
        runner_conf=runner_config,
        config_file=True

    )

    crawler = CrawlerRunnerOperator(
        task_id=task_id_to_compare[1],
        provide_context=False,
        runner_conf=runner_config
    )

    android_cmp = DataCompareOperator(
        task_id='data_compare',
        task_id_list=task_id_to_compare,
        retries=3,
        provide_context=False,
        runner_conf=runner_config,
        dag=dag
    )


    start_task >> android_release >> [android, crawler] >> android_cmp >> run_this_last

if __name__ == "__main__":
    dag.cli()
