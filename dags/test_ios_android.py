import json
from datetime import timedelta

import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator

from operators.android_runner_operator import AndroidRunnerOperator
from operators.data_compare_operator import DataCompareOperator, generate_id
from operators.ios_operator import IOSStockOperator
from operators.android_release_operator import AndroidReleaseOperator
from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig, Site


def gen2iOSCaseList():
	res = []
	for i in range(2):
		runner_conf = RunnerConfig()
		runner_conf.jobID = 'TJ-1'
		runner_conf.runnerID = generate_id('RUN-A')
		runner_conf.sdkConfig.appKeyIOS = 'VVW0Fno7BEZt1a/y6KLM36uj9qcjw7CAHDwWZKDlWDs='
		runner_conf.sdkConfig.appKeyAndroid = 'J6IPlk5AEU+2/Yi59rfYnsFQtdtOgAo9GAzysx8ciOM='
		# runner_conf.sdkConfig.marketPerm.Level = "1"
		# runner_conf.sdkConfig.marketPerm.HKPerms.extend(["hk10", "hka1"])
		# runner_conf.sdkConfig.serverSites["sh"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
		# runner_conf.sdkConfig.serverSites["sz"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
		# runner_conf.sdkConfig.serverSites["cf"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
		# runner_conf.sdkConfig.serverSites["nf"].CopyFrom(Site(ips=["http://114.80.155.134:22013"]))
		# runner_conf.sdkConfig.serverSites["pb"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
		# runner_conf.sdkConfig.serverSites["hk10"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))

		runner_conf.sdkConfig.marketPerm.Level = "1"
		runner_conf.sdkConfig.marketPerm.HKPerms.extend(["hk10", "hka1"])

		runner_conf.sdkConfig.serverSites["sh"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
		runner_conf.sdkConfig.serverSites["sz"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
		runner_conf.sdkConfig.serverSites["cf"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
		runner_conf.sdkConfig.serverSites["nf"].CopyFrom(Site(ips=["http://114.80.155.134:22013"]))
		runner_conf.sdkConfig.serverSites["pb"].CopyFrom(Site(ips=["http://114.80.155.58:22016"]))

		runner_conf.storeConfig.mongoUri = 'mongodb://221.228.66.83:30617'
		runner_conf.storeConfig.dbName = 'stockSdkTest'
		runner_conf.storeConfig.collectionName = 'test_result'
		runner_conf.storeConfig.restEndpoint = 'http://mongo-python-eve.sdk-test.svc.cluster.local:80'

		if i == 0:
			# iOS 样例
			case_conf = TestcaseConfig()
			case_conf.testcaseID = 'AHQuoteListTestCase1'
			case_conf.continueWhenFailed = False
			case_conf.roundIntervalSec = 3
			case_conf.paramStrs.extend([
				json.dumps({
					'PAGE_SIZE': '12',
					'PAGE_INDEX': '0',
					'ASC?': 'no',
					'FIELD': '2'
				})
			])
			# case_conf = TestcaseConfig()
			# case_conf.testcaseID = 'OfferQuoteTestCase'
			# case_conf.continueWhenFailed = False
			# case_conf.roundIntervalSec = 3
			# case_conf.paramStrs.extend([
			# 	json.dumps({
			# 		'CODE': '000048.sz',
			# 	})
			# ])			
			# case_conf = TestcaseConfig()
			# case_conf.testcaseID = 'HistoryChartTestCase'
			# case_conf.continueWhenFailed = False
			# case_conf.roundIntervalSec = 3
			# case_conf.paramStrs.extend([
			# 	json.dumps({
			# 		'CODE': '600000.sh',
			# 		'SUBTYPE': '1001',
			# 		'DATE': '20190826'
			# 	})
			# ])			
		else:
			# android 样例
			case_conf = TestcaseConfig()
			case_conf.testcaseID = 'AHLIST_1'
			case_conf.roundIntervalSec = 3
			case_conf.continueWhenFailed = False
			case_conf.paramStrs.extend([
				json.dumps({
					'param': '0,12,2,1'
				})
			])
			# case_conf = TestcaseConfig()
			# case_conf.testcaseID = 'OFFERQUOTE_1'
			# case_conf.roundIntervalSec = 3
			# case_conf.continueWhenFailed = False
			# case_conf.paramStrs.extend([
			# 	json.dumps({
			# 		'code': '000048.sz'
			# 	})
			# ])
			# case_conf = TestcaseConfig()
			# case_conf = TestcaseConfig()
			# case_conf.testcaseID = 'HISTORYCHART_1'
			# case_conf.roundIntervalSec = 3
			# case_conf.continueWhenFailed = False
			# case_conf.paramStrs.extend([
			# 	json.dumps({
			# 		'code': '600000.sh',
			# 		'date': '20190826'
			# 	})
			# ])

		runner_conf.casesConfig.extend([case_conf])
		res.append(runner_conf)

	return res


with DAG(
		dag_id='ia_test',
		default_args={
			'owner': 'airflow',
			'start_date': airflow.utils.dates.days_ago(0),
		},
		schedule_interval='@once',
) as dag:
	# start_task = DummyOperator(
	# 	task_id='run_this_first',
	# 	queue='worker'
	# )

	run_this_last = DummyOperator(
		task_id='run_this_last',
		queue='android'
	)

	task_id_to_cmp_list1 = ['ios_test', 'android_test']

	runner_conf_list = gen2iOSCaseList()

	android_release = AndroidReleaseOperator(
		task_id='android_release',
		provide_context=False,
		repo_name='stocksdktest/AndroidTestRunner',
		tag_id='release-20191211-0.0.1',
		tag_sha='f2d7516dbbf2d1dbc93fd28220e8ad693213141f',
		runner_conf=runner_conf_list[0]
	)

	ios = IOSStockOperator(
		task_id=task_id_to_cmp_list1[0],
		provide_context=False,
		app_id="2",
		project_path="",
		runner_conf=runner_conf_list[0]
	)

	android = AndroidRunnerOperator(
		task_id=task_id_to_cmp_list1[1],
		provide_context=False,
		apk_id='com.chi.ssetest',
		apk_version='release-20191211-0.0.1',
		runner_conf=runner_conf_list[1]
	)

	cmp_runner = runner_conf_list[1]

	ios_android_cmp = DataCompareOperator(
		task_id='data_compare',
		task_id_list=task_id_to_cmp_list1,
		retries=3,
		provide_context=False,
		runner_conf=cmp_runner,
		dag=dag
	)

	android_release >> [ios, android] >> ios_android_cmp >> run_this_last

if __name__ == "__main__":
	dag.cli()
