import json

import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
from operators.data_compare_operator import DataCompareOperator
from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig, Site
from operators.android_runner_operator import AndroidRunnerOperator
from operators.android_release_operator import AndroidReleaseOperator

#F10测试和生产对比
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
        runner_conf.storeConfig.collectionName = "record"
        if i == 0:
            runner_conf.sdkConfig.serverSites["sh"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
            runner_conf.sdkConfig.serverSites["sz"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
            runner_conf.sdkConfig.serverSites["bj"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
            runner_conf.sdkConfig.serverSites["cf"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
            runner_conf.sdkConfig.serverSites["nf"].CopyFrom(Site(ips=["http://114.80.155.58:22013"]))
            runner_conf.sdkConfig.serverSites["gf"].CopyFrom(Site(ips=["http://114.80.155.134:22013"]))
            runner_conf.sdkConfig.serverSites["pb"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
            runner_conf.sdkConfig.serverSites["hk1"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hk5"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hk10"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hka1"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hkd1"].CopyFrom(Site(ips=["http://114.80.155.139:22016"]))
            runner_conf.sdkConfig.serverSites["hkaz"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
            runner_conf.sdkConfig.serverSites["hkdz"].CopyFrom(Site(ips=["http://114.80.155.139:22016"]))
        else:
			# runner_conf.sdkConfig.serverSites["sh"].CopyFrom(Site(ips=["http://117.184.225.151:22016"]))
			# runner_conf.sdkConfig.serverSites["sz"].CopyFrom(Site(ips=["http://117.184.225.151:22016"]))
			# runner_conf.sdkConfig.serverSites["bj"].CopyFrom(Site(ips=["http://117.184.225.151:22016"]))
			# runner_conf.sdkConfig.serverSites["cf"].CopyFrom(Site(ips=["http://117.184.225.151:22016"]))
			# runner_conf.sdkConfig.serverSites["nf"].CopyFrom(Site(ips=["http://140.207.241.197:22013"]))
			# runner_conf.sdkConfig.serverSites["gf"].CopyFrom(Site(ips=["http://117.184.225.151:22016"]))
			# runner_conf.sdkConfig.serverSites["pb"].CopyFrom(Site(ips=["http://117.184.225.151:22016"]))
			# runner_conf.sdkConfig.serverSites["hk1"].CopyFrom(Site(ips=["http://58.63.252.56:22016"]))
			# runner_conf.sdkConfig.serverSites["hk5"].CopyFrom(Site(ips=["http://58.63.252.56:22016"]))
			# runner_conf.sdkConfig.serverSites["hk10"].CopyFrom(Site(ips=["http://58.63.252.56:22016"]))
			# runner_conf.sdkConfig.serverSites["hka1"].CopyFrom(Site(ips=["http://58.63.252.56:22016"]))
			# runner_conf.sdkConfig.serverSites["hkd1"].CopyFrom(Site(ips=["http://114.80.155.139:22016"]))
			# runner_conf.sdkConfig.serverSites["hkaz"].CopyFrom(Site(ips=["http://58.63.252.56:22016"]))
			# runner_conf.sdkConfig.serverSites["hkdz"].CopyFrom(Site(ips=["http://114.80.155.139:22016"]))
            runner_conf.sdkConfig.serverSites["sh"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
            runner_conf.sdkConfig.serverSites["sz"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
            runner_conf.sdkConfig.serverSites["bj"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
            runner_conf.sdkConfig.serverSites["cf"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
            runner_conf.sdkConfig.serverSites["nf"].CopyFrom(Site(ips=["http://58.63.252.23:22013"]))
            runner_conf.sdkConfig.serverSites["gf"].CopyFrom(Site(ips=["http://114.80.155.61:22013"]))
            runner_conf.sdkConfig.serverSites["pb"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
            runner_conf.sdkConfig.serverSites["hk1"].CopyFrom(Site(ips=["http://114.80.155.58:8601"]))
            runner_conf.sdkConfig.serverSites["hk5"].CopyFrom(Site(ips=["http://114.80.155.58:8601"]))
            runner_conf.sdkConfig.serverSites["hk10"].CopyFrom(Site(ips=["http://114.80.155.58:8601"]))
            runner_conf.sdkConfig.serverSites["hka1"].CopyFrom(Site(ips=["http://114.80.155.58:8601"]))
            runner_conf.sdkConfig.serverSites["hkd1"].CopyFrom(Site(ips=["http://114.80.155.58:8601"]))
            runner_conf.sdkConfig.serverSites["hkaz"].CopyFrom(Site(ips=["http://114.80.155.58:8601"]))
            runner_conf.sdkConfig.serverSites["hkdz"].CopyFrom(Site(ips=["http://114.80.155.58:8601"]))
            
        case_list = []
		#F10
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'F10_STOCKNEWS_1'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
            json.dumps({
                'bulletinID': '603722.sh_20191212020010172374',
                'src': 'd',
            }),
			json.dumps({
                'bulletinID': '002654.sz_20191211030001155134',
                'src': 'd',
            }),
			json.dumps({
                'bulletinID': '900921.sh_20191211020010159012',
                'src': 'd',
            }),
			json.dumps({
                'bulletinID': '200625.sz_20191212020010171725',
                'src': 'd',
            }),
        ])
        case_list.append(case_conf)

        runner_conf.casesConfig.extend(case_list)
        print('i,case_list.length is ', case_list.__len__())
        runner_conf_list.append(runner_conf)

    return runner_conf_list


with DAG(
       dag_id='android_test_F10',
		default_args={
			'owner': 'airflow',
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

    runner_conf_list = initRunnerConfig()
    task_id_to_cmp_list = ['adb_release_cmp_a', 'adb_release_cmp_b']
    #全真-007
    android_release1 = AndroidReleaseOperator(
        task_id='android_release1',
        release_xcom_key='android_release1',
        provide_context=False,
        repo_name='stocksdktest/AndroidTestRunner',
        tag_id='release-20191211-0.0.1',
        tag_sha='f2d7516dbbf2d1dbc93fd28220e8ad693213141f',
        runner_conf=runner_conf_list[0]
    )
    #生产-004
    android_release2 = AndroidReleaseOperator(
        task_id='android_release2',
        release_xcom_key='android_release2',
        provide_context=False,
        repo_name='stocksdktest/AndroidTestRunner',
        tag_id='release-20191210-0.0.2',
        tag_sha='a7be31d3aa2d3fa488ec3e68e04532efeb202e57',
        runner_conf=runner_conf_list[0]
    )

    android_a = AndroidRunnerOperator(
        task_id=task_id_to_cmp_list[0],
        release_xcom_key='android_release1',
        provide_context=False,
        apk_id='com.chi.ssetest',
        apk_version='release-20191211-0.0.1',
        runner_conf=runner_conf_list[0]
    )

    android_b = AndroidRunnerOperator(
        task_id=task_id_to_cmp_list[1],
        release_xcom_key='android_release2',
        provide_context=False,
        apk_id='com.chi.ssetest',
        apk_version='release-20191210-0.0.2',
        runner_conf=runner_conf_list[1]
    )

    runner_conf_cmp = runner_conf_list[0]

    android_cmp = DataCompareOperator(
        task_id='data_compare',
        task_id_list=task_id_to_cmp_list,
        retries=3,
        provide_context=False,
        runner_conf=runner_conf_cmp,
        dag=dag
    )

    start_task >> [android_release1, android_release2] >> release_ok >> [android_a, android_b] >> android_cmp >> run_this_last


if __name__ == "__main__":
    dag.cli()