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


# .a测试，b生产
# TODO init RunnerConfig
def initRunnerConfig():
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
        runner_conf.storeConfig.collectionName = "test_result"

        if i == 0:
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
        else:
            # 生产站点
            runner_conf.sdkConfig.serverSites["sh"].CopyFrom(Site(ips=["http://27.151.2.87:22016"]))
            runner_conf.sdkConfig.serverSites["shl2"].CopyFrom(Site(ips=["http://27.151.2.88:22016"]))
            runner_conf.sdkConfig.serverSites["sz"].CopyFrom(Site(ips=["http://27.151.2.87:22016"]))
            runner_conf.sdkConfig.serverSites["szl2"].CopyFrom(Site(ips=["http://27.151.2.89:22016"]))
            runner_conf.sdkConfig.serverSites["bj"].CopyFrom(Site(ips=["http://27.151.2.87:22016"]))
            runner_conf.sdkConfig.serverSites["cf"].CopyFrom(Site(ips=["http://27.151.2.87:22016"]))
            runner_conf.sdkConfig.serverSites["nf"].CopyFrom(Site(ips=["http://58.63.252.23:22013"]))
            runner_conf.sdkConfig.serverSites["gf"].CopyFrom(Site(ips=["http://27.151.2.87:22016"]))
            runner_conf.sdkConfig.serverSites["pb"].CopyFrom(Site(ips=["http://27.151.2.87:22016"]))
            runner_conf.sdkConfig.serverSites["hk1"].CopyFrom(Site(ips=["http://58.63.252.56:22016"]))
            runner_conf.sdkConfig.serverSites["hk5"].CopyFrom(Site(ips=["http://58.63.252.56:22016"]))
            runner_conf.sdkConfig.serverSites["hk10"].CopyFrom(Site(ips=["http://58.63.252.56:22016"]))
            runner_conf.sdkConfig.serverSites["hka1"].CopyFrom(Site(ips=["http://58.63.252.56:22016"]))
            runner_conf.sdkConfig.serverSites["hkd1"].CopyFrom(Site(ips=["http://58.63.252.56:22016"]))
            runner_conf.sdkConfig.serverSites["hkaz"].CopyFrom(Site(ips=["http://58.63.252.56:22016"]))
            runner_conf.sdkConfig.serverSites["hkdz"].CopyFrom(Site(ips=["http://58.63.252.56:22016"]))
        case_list = []

        # 接口 测试样例
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'CATESORTING_2'
        case_conf.continueWhenFailed = True
        case_conf.roundIntervalSec = 3
        case_conf.paramStrs.extend([
            json.dumps({
                'CateType': 'SH1133',
                'param': '0,50,0,0,1',
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1133',
                'param': '0,50,0,1,1',
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1133',
                'param': '0,50,1,0,1',
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1133',
                'param': '0,50,1,1,1',
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1133',
                'param': '0,50,2,0,1',
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1133',
                'param': '0,50,2,1,1',
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1133',
                'param': '0,50,7,0,1',
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1133',
                'param': '0,50,7,1,1',
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1133',
                'param': '0,50,8,0,1',
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1133',
                'param': '0,50,8,1,1',
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1133',
                'param': '0,50,9,0,1',
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1133',
                'param': '0,50,9,1,1',
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1133',
                'param': '0,50,10,0,1',
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1133',
                'param': '0,50,10,1,1',
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1133',
                'param': '0,50,11,0,1',
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1133',
                'param': '0,50,11,1,1',
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1133',
                'param': '0,50,12,0,1',
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1133',
                'param': '0,50,12,1,1',
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1133',
                'param': '0,50,13,0,1',
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1133',
                'param': '0,50,13,1,1',
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
        ])
        runner_conf.casesConfig.extend([case_conf])

        print('i,case_list.length is ', case_list.__len__())
        runner_conf_list.append(runner_conf)
    return runner_conf_list


with DAG(
        dag_id='example_android_sort_compare',
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
    task_id_to_sort_list = ['adb_sort_a', 'adb_sort_b']
    sort_id_to_compare_list = ['android_sort_a', 'android_sort_b']

    android_release = AndroidReleaseOperator(
        task_id='test_android',
        provide_context=False,
        repo_name='stocksdktest/AndroidTestRunner',
        tag_id='release-20200310-0.0.5',
        tag_sha='9e2d1a04b6dba6e800cafadd5046b777326c8bfd',
        runner_conf=runner_conf_list[0]
    )

    android_a = AndroidRunnerOperator(
        task_id=task_id_to_sort_list[0],
        provide_context=False,
        apk_id='com.chi.ssetest',
        apk_version='release-20200310-0.0.5',
        runner_conf=runner_conf_list[0],
        config_file=True

    )

    android_b = AndroidRunnerOperator(
        task_id=task_id_to_sort_list[1],
        provide_context=False,
        apk_id='com.chi.ssetest',
        apk_version='release-20200310-0.0.5',
        runner_conf=runner_conf_list[1],
        config_file=True

    )

    android_sort_a = DataSortingOperator(
        task_id=sort_id_to_compare_list[0],
        from_task=task_id_to_sort_list[0],
        sort_and_comprae=True,
        retries=3,
        provide_context=False,
        runner_conf=runner_conf_default,
        dag=dag
    )

    android_cmp = DataCompareOperator(
        task_id='data_compare',
        task_id_list=task_id_to_sort_list,
        sort_id_list=sort_id_to_compare_list,
        sort_and_comprae=True,
        retries=3,
        provide_context=False,
        runner_conf=runner_conf_default,
        dag=dag
    )

    android_sort_b = DataSortingOperator(
        task_id=sort_id_to_compare_list[1],
        from_task=task_id_to_sort_list[1],
        sort_and_comprae=True,
        retries=3,
        provide_context=False,
        runner_conf=runner_conf_default,
        dag=dag
    )

    # [android_a, android_b] >> android_cmp

    start_task >> android_release >> [android_a, android_b] >> android_cmp
    android_a >> android_sort_a
    android_b >> android_sort_b
    [android_sort_a, android_sort_b] >> android_cmp >> run_this_last

if __name__ == "__main__":
    dag.cli()