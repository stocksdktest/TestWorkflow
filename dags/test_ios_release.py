import json

import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator

from operators.data_compare_operator import DataCompareOperator
from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig, Site
from operators.ios_runner_operator import IOSRunnerOperator
from operators.ios_release_operator import IOSReleaseOperator

def initRunnerConfig():
    runner_conf_list = []
    # init runner conf list
    runner_conf_list = []

    for i in range(2):
        runner_conf = RunnerConfig()

        runner_conf.sdkConfig.appKeyIOS = 'VVW0Fno7BEZt1a/y6KLM36uj9qcjw7CAHDwWZKDlWDs='
        runner_conf.sdkConfig.appKeyAndroid = 'J6IPlk5AEU+2/Yi59rfYnsFQtdtOgAo9GAzysx8ciOM='
        runner_conf.sdkConfig.marketPerm.Level = "1"
        runner_conf.sdkConfig.marketPerm.HKPerms.extend(["hk10"])
        # mongoDB位置，存储的数据库位置
        runner_conf.storeConfig.mongoUri = "mongodb://221.228.66.83:30617"
        runner_conf.storeConfig.dbName = "stockSdkTest"
        runner_conf.storeConfig.collectionName = "debug"
        
        if i == 0:
            runner_conf.sdkConfig.serverSites["sh"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
            runner_conf.sdkConfig.serverSites["sz"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
            runner_conf.sdkConfig.serverSites["bj"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
            runner_conf.sdkConfig.serverSites["cf"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
            runner_conf.sdkConfig.serverSites["nf"].CopyFrom(Site(ips=["http://114.80.155.134:22013"]))
            runner_conf.sdkConfig.serverSites["gf"].CopyFrom(Site(ips=["http://114.80.155.134:22013"]))
            runner_conf.sdkConfig.serverSites["pb"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
            runner_conf.sdkConfig.serverSites["hk1"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hk5"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hk10"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hka1"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hkd1"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hkaz"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hkdz"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
        else:
            runner_conf.sdkConfig.serverSites["sh"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
            runner_conf.sdkConfig.serverSites["sz"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
            runner_conf.sdkConfig.serverSites["bj"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
            runner_conf.sdkConfig.serverSites["cf"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
            runner_conf.sdkConfig.serverSites["nf"].CopyFrom(Site(ips=["http://114.80.155.61:22013"]))
            runner_conf.sdkConfig.serverSites["gf"].CopyFrom(Site(ips=["http://114.80.155.61:22013"]))
            runner_conf.sdkConfig.serverSites["pb"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
            runner_conf.sdkConfig.serverSites["hk1"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hk5"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hk10"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hka1"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hkd1"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hkaz"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hkdz"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))

        case_list = []

        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'CHARTSUB_2'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
            json.dumps({
                'quoteitem': '600000.sh',
                'type': 'ChartTypeOneDay',
                'begin': '0',
                'end': '100',
                'select': 'time,ddx,ddy,ddz'
            })
        ])
        case_list.append(case_conf)

        # 历史K线方法一
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'OHLCV3_1'
        case_conf.continueWhenFailed = False
        case_conf.roundIntervalSec = 3
        case_conf.paramStrs.extend([
            json.dumps({
                'CODES': '00700.hk',
                'TYPES': 'dayk'
            })
        ])
        case_list.append(case_conf)

        # 历史K线方法二
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'OHLCV3_2'
        case_conf.continueWhenFailed = False
        case_conf.roundIntervalSec = 3
        case_conf.paramStrs.extend([
            json.dumps({
                'CODES': '00700.hk',
                'TYPES': 'dayk',
                'FqTypes': '1',
                'DATES': 'null'
            })
        ])
        case_list.append(case_conf)

        runner_conf.casesConfig.extend(case_list)
        print('i,case_list.length is ', case_list.__len__())
        runner_conf_list.append(runner_conf)

    return runner_conf_list

# 对比了runner_conf_list数组中的前两项？
with DAG(
    dag_id='ios_test_release',
    default_args={
        'owner': 'lxjtest',
        'start_date': airflow.utils.dates.days_ago(0)
    },
    schedule_interval='@once',
) as dag:
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

    # 初始化
    runner_conf_list = initRunnerConfig()
    # 定义两个版本比较的task的名字
    task_id_to_cmp_list = ['ios_release_cmp_a', 'ios_release_cmp_b']

    ios_release1 = IOSReleaseOperator(
        task_id='ios_release1',
        release_xcom_key='android_release1',
        provide_context=False,
        repo_name='stocksdktest/IOSTestRunner',
        tag_id='release-20200107-0.0.1',
        tag_sha='94c20c5dcfd53dab6cb0d90f36bf2f719bd235f4',
        runner_conf=runner_conf_list[0]
    )

    ios_release2 = IOSReleaseOperator(
        task_id='ios_release2',
        release_xcom_key='android_release2',
        provide_context=False,
        repo_name='stocksdktest/IOSTestRunner',
        tag_id='release-20200110-0.0.3',
        tag_sha='f5e522fb1775c9edbe6871e9c28b210ba5510a61',
        runner_conf=runner_conf_list[1]
    )

    ios_a = IOSRunnerOperator(
        task_id=task_id_to_cmp_list[0],
        release_xcom_key='ios_release1',
        provide_context=False,
        app_version="1",
        apk_id='com.chi.ssetest',
        apk_version='release-20200107-0.0.1',
        runner_conf=runner_conf_list[0]
    )

    ios_b = IOSRunnerOperator(
        task_id=task_id_to_cmp_list[1],
        release_xcom_key='ios_release2',
        provide_context=False,
        app_version="2",
        apk_id='com.chi.ssetest',
        apk_version='release-20200110-0.0.3',
        runner_conf=runner_conf_list[1]
    )

    ios_cmp = DataCompareOperator(
        task_id='data_compare',
        task_id_list=task_id_to_cmp_list,
        retries=3,
        provide_context=False,
        runner_conf=RunnerConfig,
        dag=dag
    )
    
    start_task >> [ios_release1, ios_release2] >> release_ok >> [ios_a, ios_b] >> ios_cmp >> run_this_last

if __name__ == "__main__":
    dag.cli()