import json
from datetime import timedelta

import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator

from operators.data_compare_operator import DataCompareOperator, generate_id
from operators.ios_runner_operator import IOSRunnerOperator
from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig, Site


def gen2iOSCaseList():
	res = []
	for i in range(2):
		runner_conf = RunnerConfig()
		runner_conf.jobID = 'TJ-1'
		runner_conf.runnerID = generate_id('RUN-A')

		runner_conf.sdkConfig.appKeyIOS = 'VVW0Fno7BEZt1a/y6KLM36uj9qcjw7CAHDwWZKDlWDs='
		runner_conf.sdkConfig.appKeyAndroid = 'J6IPlk5AEU+2/Yi59rfYnsFQtdtOgAo9GAzysx8ciOM='

		runner_conf.sdkConfig.marketPerm.Level = "1"
		runner_conf.sdkConfig.marketPerm.HKPerms.extend(["hk10", "hka1"])
		# runner_conf.sdkConfig.serverSites["sh"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
		# runner_conf.sdkConfig.serverSites["sz"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
		# runner_conf.sdkConfig.serverSites["cf"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
		# runner_conf.sdkConfig.serverSites["nf"].CopyFrom(Site(ips=["http://114.80.155.134:22013"]))
		# runner_conf.sdkConfig.serverSites["pb"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
		# runner_conf.sdkConfig.serverSites["hk10"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
		# runner_conf.sdkConfig.serverSites["bj"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))

		runner_conf.sdkConfig.serverSites["sh"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
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
		
		runner_conf.storeConfig.mongoUri = 'mongodb://221.228.66.83:30617'
		runner_conf.storeConfig.dbName = 'stockSdkTest'
		runner_conf.storeConfig.collectionName = 'test_result'
		runner_conf.storeConfig.restEndpoint = 'http://mongo-python-eve.sdk-test.svc.cluster.local:80'

		# case_conf = TestcaseConfig()
		# case_conf.testcaseID = 'SnapQuoteTestCase'
		# case_conf.continueWhenFailed = False
		# case_conf.roundIntervalSec = 3
		# case_conf.paramStrs.extend([
		# 	json.dumps({
		# 		'CODE': '839806.bj',
		# 		'TICKCOUNT': '10',
		# 		'FIELDS': '',
		# 		'STOCKFIELDS': ''
		# 	})
		# ])
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
		queue='worker',
		task_id='run_this_first',
	)

	run_this_last = DummyOperator(
		task_id='run_this_last',
		queue='worker'
	)

	task_id_to_cmp_list1 = ['ios_cmp_a1', 'ios_cmp_a2']

	runner_conf_list = gen2iOSCaseList()

	ios_1 = IOSRunnerOperator(
		task_id=task_id_to_cmp_list1[0],
		provide_context=False,
		app_id="2",
		project_path="",
		runner_conf=runner_conf_list[0]
	)

	ios_2 = IOSRunnerOperator(
		task_id=task_id_to_cmp_list1[1],
		provide_context=False,
		app_id="2",
		project_path="",
		runner_conf=runner_conf_list[0]
	)

	ios_cmp1 = DataCompareOperator(
		task_id='data_compare',
		task_id_list=task_id_to_cmp_list1,
		retries=3,
		provide_context=False,
		runner_conf=runner_conf_list[0],
		dag=dag
	)

	start_task >> [ios_1, ios_2] >> ios_cmp1 >> run_this_last
	# start_task >> ios_1 >> ios_2 >> ios_cmp1 >> run_this_last

if __name__ == "__main__":
	dag.cli()
