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

    for i in range(2):
        runner_conf = RunnerConfig()

        runner_conf.sdkConfig.appKeyIOS = 'VVW0Fno7BEZt1a/y6KLM36uj9qcjw7CAHDwWZKDlWDs='
        runner_conf.sdkConfig.appKeyAndroid = 'J6IPlk5AEU+2/Yi59rfYnsFQtdtOgAo9GAzysx8ciOM='
        runner_conf.sdkConfig.marketPerm.Level = "2"
        runner_conf.sdkConfig.marketPerm.HKPerms.extend(["hk10"])
        # mongoDB位置，存储的数据库位置
        runner_conf.storeConfig.mongoUri = "mongodb://221.228.66.83:30617"
        runner_conf.storeConfig.dbName = "stockSdkTest"
        runner_conf.storeConfig.collectionName = "sort"

        if i == 0:
            runner_conf.sdkConfig.serverSites["sh"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
            runner_conf.sdkConfig.serverSites["tcpsh"].CopyFrom(Site(ips=["http://114.80.155.134:22017"]))
            runner_conf.sdkConfig.serverSites["shl2"].CopyFrom(Site(ips=["http://114.80.155.62:22016"]))
            runner_conf.sdkConfig.serverSites["tcpshl2"].CopyFrom(Site(ips=["http://114.80.155.62:22017"]))
            runner_conf.sdkConfig.serverSites["sz"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
            runner_conf.sdkConfig.serverSites["szl2"].CopyFrom(Site(ips=["http://114.80.155.47:22016"]))
            runner_conf.sdkConfig.serverSites["tcpsz"].CopyFrom(Site(ips=["http://114.80.155.134:22017"]))
            runner_conf.sdkConfig.serverSites["tcpszl2"].CopyFrom(Site(ips=["http://114.80.155.47:22017"]))
            runner_conf.sdkConfig.serverSites["bj"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
            runner_conf.sdkConfig.serverSites["cf"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
            runner_conf.sdkConfig.serverSites["nf"].CopyFrom(Site(ips=["http://114.80.155.134:22013"]))
            runner_conf.sdkConfig.serverSites["gf"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
            runner_conf.sdkConfig.serverSites["pb"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
            runner_conf.sdkConfig.serverSites["hk1"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hk5"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hk10"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["tcphk10"].CopyFrom(Site(ips=["http://114.80.155.133:22017"]))
            runner_conf.sdkConfig.serverSites["hka1"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hkd1"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hkaz"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hkdz"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
        else:
            # 生产站点
            runner_conf.sdkConfig.serverSites["sh"].CopyFrom(Site(ips=["http://117.184.225.151:22016"]))
            runner_conf.sdkConfig.serverSites["sz"].CopyFrom(Site(ips=["http://117.184.225.151:22016"]))
            runner_conf.sdkConfig.serverSites["bj"].CopyFrom(Site(ips=["http://117.184.225.151:22016"]))
            runner_conf.sdkConfig.serverSites["cf"].CopyFrom(Site(ips=["http://117.184.225.151:22016"]))
            runner_conf.sdkConfig.serverSites["nf"].CopyFrom(Site(ips=["http://140.207.241.197:22013"]))
            runner_conf.sdkConfig.serverSites["gf"].CopyFrom(Site(ips=["http://117.184.225.151:22016"]))
            runner_conf.sdkConfig.serverSites["pb"].CopyFrom(Site(ips=["http://117.184.225.151:22016"]))
            runner_conf.sdkConfig.serverSites["hk1"].CopyFrom(Site(ips=["http://58.63.252.56:22016"]))
            runner_conf.sdkConfig.serverSites["hk5"].CopyFrom(Site(ips=["http://58.63.252.56:22016"]))
            runner_conf.sdkConfig.serverSites["hk10"].CopyFrom(Site(ips=["http://58.63.252.56:22016"]))
            runner_conf.sdkConfig.serverSites["hka1"].CopyFrom(Site(ips=["http://58.63.252.56:22016"]))
            runner_conf.sdkConfig.serverSites["hkd1"].CopyFrom(Site(ips=["http://114.80.155.139:22016"]))
            runner_conf.sdkConfig.serverSites["hkaz"].CopyFrom(Site(ips=["http://58.63.252.56:22016"]))
            runner_conf.sdkConfig.serverSites["hkdz"].CopyFrom(Site(ips=["http://114.80.155.139:22016"]))
        case_list = []

        # 排序接口 测试样例
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'CATESORTING_2'
        case_conf.continueWhenFailed = True
        case_conf.roundIntervalSec = 3
        case_conf.paramStrs.extend([
            json.dumps({
                'CateType': 'SH1001',
                'param': '0,100,7,0,1',  # 最新价正序排
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1001',
                'param': '0,100,7,1,1',  # 最新价倒序排
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1001',
                'param': '0,100,8,0,1',  # 最高价正序排
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1001',
                'param': '0,100,8,1,1',
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1001',
                'param': '0,100,9,0,1',  # 最低价正序排
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1001',
                'param': '0,100,9,1,1',
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1001',
                'param': '0,100,10,0,1',  # 今开价正序排
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1001',
                'param': '0,100,10,1,1',
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1001',
                'param': '0,100,11,0,1',  # 昨收价正序排
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1001',
                'param': '0,100,11,1,1',
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1001',
                'param': '0,100,12,0,1',  # 涨跌比率正序排
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1001',
                'param': '0,100,12,1,1',
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1001',
                'param': '0,100,13,0,1',  # 总手正序排
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1001',
                'param': '0,100,13,1,1',
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1001',
                'param': '0,100,14,0,1',  # 当前成交量正序排
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
            json.dumps({
                'CateType': 'SH1001',
                'param': '0,100,14,1,1',
                'STOCKFIELDS': '-1',
                'ADDVALUEFIELDS': '-1'
            }),
        ])
        runner_conf.casesConfig.extend([case_conf])

        # 板块排序测试样例
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'BANKUAISORTING_1'
        case_conf.continueWhenFailed = True
        case_conf.roundIntervalSec = 3
        case_conf.paramStrs.extend([
            json.dumps({
                'SYMBOL': 'Trade',
                'param': '0,10,hsl,1'  # 按照换手率排序
            }),
            json.dumps({
                'SYMBOL': 'Trade',
                'param': '0,10,zgj,1'  # 按照最高价排序
            }),
            json.dumps({
                'SYMBOL': 'Notion',
                'param': '0,10,zxj,1'  # 按照最新价排序
            }),
            json.dumps({
                'SYMBOL': 'Notion',
                'param': '0,10,zdj,1'  # 按照最低价排序
            }),
            json.dumps({
                'SYMBOL': 'Area',
                'param': '0,10,hsl,1'  # 按照换手率排序
            }),
            json.dumps({
                'SYMBOL': 'Area',
                'param': '0,10,zf,1'  # 按照振幅排序
            }),
        ])
        runner_conf.casesConfig.extend([case_conf])

        print('i,case_list.length is ', case_list.__len__())
        runner_conf_list.append(runner_conf)
    return runner_conf_list


with DAG(
        dag_id='android_sort_test',
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

    android_release = AndroidReleaseOperator(
        task_id='test_android',
        provide_context=False,
        repo_name='stocksdktest/AndroidTestRunner',
        tag_id='release-20200103-0.0.3',
        tag_sha='53fcc717d954e01d88bc9bd70eaab9ac9a0acb67',
        runner_conf=runner_conf_list[0]
    )

    android_a = AndroidRunnerOperator(
        task_id=task_id_to_sort_list[0],
        provide_context=False,
        apk_id='com.chi.ssetest',
        apk_version='release-20200103-0.0.3',
        runner_conf=runner_conf_list[0]
    )

    android_b = AndroidRunnerOperator(
        task_id=task_id_to_sort_list[1],
        provide_context=False,
        apk_id='com.chi.ssetest',
        apk_version='release-20200103-0.0.3',
        runner_conf=runner_conf_list[1]
    )


    android_sort_a = DataSortingOperator(
        task_id='android_sort_a',
        from_task=task_id_to_sort_list[0],
        retries=3,
        provide_context=False,
        runner_conf=runner_conf_default,
        dag=dag
    )

    android_sort_b = DataSortingOperator(
        task_id='android_sort_b',
        from_task=task_id_to_sort_list[1],
        retries=3,
        provide_context=False,
        runner_conf=runner_conf_default,
        dag=dag
    )

    start_task >> android_release >> [android_a, android_b]
    android_a >> android_sort_a
    android_b >> android_sort_b
    [android_sort_a, android_sort_b]>> run_this_last

if __name__ == "__main__":
    dag.cli()
