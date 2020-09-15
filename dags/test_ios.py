import json
from datetime import timedelta

import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator

from operators.data_compare_operator import DataCompareOperator, generate_id
from operators.ios_release_operator import IOSReleaseOperator
from operators.ios_runner_operator import IOSRunnerOperator
from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig, Site


def gen2iOSCaseList():
	res = []
	for i in range(2):
		runner_conf = RunnerConfig()

		runner_conf.sdkConfig.appKeyIOS = 'VVW0Fno7BEZt1a/y6KLM36uj9qcjw7CAHDwWZKDlWDs='
		runner_conf.sdkConfig.appKeyAndroid = 'J6IPlk5AEU+2/Yi59rfYnsFQtdtOgAo9GAzysx8ciOM='
		runner_conf.sdkConfig.marketPerm.Level = "1"
		runner_conf.sdkConfig.marketPerm.HKPerms.extend(["hk10"])
		# mongoDB位置，存储的数据库位置
		runner_conf.storeConfig.mongoUri = 'mongodb://221.228.66.83:30617'
		runner_conf.storeConfig.dbName = 'stockSdkTest'
		runner_conf.storeConfig.collectionName = 'test_result'
		runner_conf.storeConfig.restEndpoint = 'http://mongo-python-eve.sdk-test.svc.cluster.local:80'
		if i == 0:
			runner_conf.sdkConfig.serverSites["sh"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
			runner_conf.sdkConfig.serverSites["shl2"].CopyFrom(Site(ips=["http://114.80.155.62:22016"]))
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
			runner_conf.sdkConfig.serverSites["sh"].CopyFrom(Site(ips=["http://27.151.2.87:22016"]))
			runner_conf.sdkConfig.serverSites["shl2"].CopyFrom(Site(ips=["http://114.80.155.50:22016"]))
			runner_conf.sdkConfig.serverSites["sz"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
			runner_conf.sdkConfig.serverSites["bj"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
			runner_conf.sdkConfig.serverSites["cf"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
			runner_conf.sdkConfig.serverSites["nf"].CopyFrom(Site(ips=["http://114.80.155.58:22013"]))
			runner_conf.sdkConfig.serverSites["gf"].CopyFrom(Site(ips=["http://114.80.155.61:22013"]))
			runner_conf.sdkConfig.serverSites["pb"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
			runner_conf.sdkConfig.serverSites["hk1"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
			runner_conf.sdkConfig.serverSites["hk5"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
			runner_conf.sdkConfig.serverSites["hk10"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
			runner_conf.sdkConfig.serverSites["hka1"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
			runner_conf.sdkConfig.serverSites["hkd1"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
			runner_conf.sdkConfig.serverSites["hkaz"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
			runner_conf.sdkConfig.serverSites["hkdz"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
		#
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10V2CLSTEST_1'
		case_conf.continueWhenFailed = True
		case_conf.roundIntervalSec = 3
		case_conf.paramStrs.extend([
			json.dumps({
				'SYMBOL': '0',
				'REQUESTTYPE': '/clsimportantnewslist',
				'PARAMS': '0,200'
			}),
			json.dumps({
				'SYMBOL': '10',
				'REQUESTTYPE': '/clsimportantnewslist',
				'PARAMS': '0,200'
			}),
			json.dumps({
				'SYMBOL': '13',
				'REQUESTTYPE': '/clsimportantnewslist',
				'PARAMS': '0,200'
			}),
			json.dumps({
				'SYMBOL': '15',
				'REQUESTTYPE': '/clsimportantnewslist',
				'PARAMS': '0,200'
			}),
			json.dumps({
				'SYMBOL': '0',
				'REQUESTTYPE': '/clstelegramlist',
				'PARAMS': '0,200'
			}),
			json.dumps({
				'SYMBOL': '523463',
				'REQUESTTYPE': '/clsimportantnews',
				'PARAMS': '0,200'
			}),
			json.dumps({
				'SYMBOL': '0',
				'REQUESTTYPE': '/clsviplist',
				'PARAMS': '0,200'
			}),
			json.dumps({
				'SYMBOL': '522495',
				'REQUESTTYPE': '/clsvip',
				'PARAMS': '0,200'
			}),
			json.dumps({
				'SYMBOL': '0',
				'REQUESTTYPE': '/clsinparamslist',
				'PARAMS': '0,200'
			}),
			json.dumps({
				'SYMBOL': '512448',
				'REQUESTTYPE': '/clsinparams',
				'PARAMS': '0,200'
			}),
			json.dumps({
				'SYMBOL': '0',
				'REQUESTTYPE': '/clsrecommendlist',
				'PARAMS': '0,200'
			}),
			json.dumps({
				'SYMBOL': '522723',
				'REQUESTTYPE': '/clsrecommend',
				'PARAMS': '0,200'
			}),
			json.dumps({
				'SYMBOL': '600000.sh',
				'REQUESTTYPE': '/clsnewslist',
				'PARAMS': '-1'
			}),
			json.dumps({
				'SYMBOL': '510013_1',
				'REQUESTTYPE': '/clsnews',
				'PARAMS': '-1'
			}),
			json.dumps({
				'SYMBOL': '600000.sh',
				'REQUESTTYPE': '/clsreportlist',
				'PARAMS': '-1'
			}),
			json.dumps({
				'SYMBOL': '819663',
				'REQUESTTYPE': '/clsreport',
				'PARAMS': '-1'
			}),
			json.dumps({
				'SYMBOL': '600000.sh',
				'REQUESTTYPE': '/clsbulletinlist',
				'PARAMS': '-1'
			}),
			json.dumps({
				'SYMBOL': '597804',
				'REQUESTTYPE': '/clsbulletin',
				'PARAMS': '-1'
			}),
		])
		runner_conf.casesConfig.extend([case_conf])

		res.append(runner_conf)
	return res


with DAG(
		dag_id='ios_test',
		default_args={
			'owner': 'airflow',
			'start_date': airflow.utils.dates.days_ago(0),
		},
		schedule_interval='@once',
) as dag:
	start_task = DummyOperator(
		task_id='run_this_first',
		queue='worker'
	)

	run_this_last = DummyOperator(
		task_id='run_this_last',
		queue='android'
	)

	task_id_to_cmp_list1 = ['ios_cmp_a1', 'ios_cmp_a2']

	runner_conf_list = gen2iOSCaseList()

	ios_release = IOSReleaseOperator(
		task_id='ios_release1',
		provide_context=False,
		repo_name='stocksdktest/IOSTestRunner',
		tag_id='release-20200628-0.0.1',
		tag_sha='d3a671a10e46a0b86eb01801328bcfc73e9c8996',
		runner_conf=runner_conf_list[0]
	)

	ios_1 = IOSRunnerOperator(
		task_id=task_id_to_cmp_list1[0],
		provide_context=False,
		app_version='release-20200628-0.0.1',
		runner_conf=runner_conf_list[0],
		config_file=True,
		#run_times=10
	)

	ios_2 = IOSRunnerOperator(
		task_id=task_id_to_cmp_list1[1],
		provide_context=False,
		app_version='release-20200628-0.0.1',
		runner_conf=runner_conf_list[1],
		config_file=True,
		#run_times=10
	)

	ios_cmp1 = DataCompareOperator(
		task_id='data_compare',
		task_id_list=task_id_to_cmp_list1,
		retries=3,
		provide_context=False,
		runner_conf=runner_conf_list[0],
		#quote_detail=True,
		#run_times=10,
		dag=dag
	)

	start_task >> ios_release >> [ios_1, ios_2] >> ios_cmp1 >> run_this_last

if __name__ == "__main__":
	dag.cli()
