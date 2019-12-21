import json
from datetime import timedelta

import airflow
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.timezone import datetime

from operators.data_compare_operator import DataCompareOperator, generate_id
from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig, Site
from operators.android_runner_operator import AndroidRunnerOperator
from operators.android_release_operator import AndroidReleaseOperator
from gen_testcase import get_case1


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
		# 增加一行试试
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
			runner_conf.sdkConfig.serverSites["sh"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
			runner_conf.sdkConfig.serverSites["sz"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
			runner_conf.sdkConfig.serverSites["bj"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
			runner_conf.sdkConfig.serverSites["cf"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
			runner_conf.sdkConfig.serverSites["nf"].CopyFrom(Site(ips=["http://114.80.155.134:22013"]))
			runner_conf.sdkConfig.serverSites["gf"].CopyFrom(Site(ips=["http://114.80.155.134:22013"]))
			runner_conf.sdkConfig.serverSites["pb"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
			runner_conf.sdkConfig.serverSites["hk1"].CopyFrom(Site(ips=["http://114.80.155.58:8601"]))
			runner_conf.sdkConfig.serverSites["hk5"].CopyFrom(Site(ips=["http://114.80.155.58:8601"]))
			runner_conf.sdkConfig.serverSites["hk10"].CopyFrom(Site(ips=["http://114.80.155.58:8601"]))
			runner_conf.sdkConfig.serverSites["hka1"].CopyFrom(Site(ips=["http://114.80.155.58:8601"]))
			runner_conf.sdkConfig.serverSites["hkd1"].CopyFrom(Site(ips=["http://114.80.155.58:8601"]))
			runner_conf.sdkConfig.serverSites["hkaz"].CopyFrom(Site(ips=["http://114.80.155.58:8601"]))
			runner_conf.sdkConfig.serverSites["hkdz"].CopyFrom(Site(ips=["http://114.80.155.58:8601"]))
		case_list = []

		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'OHLCTEST_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'stk': '00700.hk',
				'type': 'dayk'
			})
		])
		case_list.append(case_conf)

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

		# 历史K线方法五
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'OHLCV3_5'
		case_conf.continueWhenFailed = False
		case_conf.roundIntervalSec = 3
		case_conf.paramStrs.extend([
			json.dumps({
				'CODES': '00700.hk',
				'TYPES': 'dayk',
				'FqTypes': '2',
				'Dates': 'null',
				'Numbers': '300'
			})
		])
		case_list.append(case_conf)

		runner_conf.casesConfig.extend(case_list)
		print('i,case_list.length is ', case_list.__len__())
		runner_conf_list.append(runner_conf)

	return runner_conf_list


def gen2confict_1():
	runner_conf_list = []
	for i in range(2):
		runner_conf = RunnerConfig()
		runner_conf.jobID = 'TJ-1'
		runner_conf.runnerID = generate_id('RUN-A')
		runner_conf.sdkConfig.appKeyIOS = 'VVW0Fno7BEZt1a/y6KLM36uj9qcjw7CAHDwWZKDlWDs='
		runner_conf.sdkConfig.appKeyAndroid = 'J6IPlk5AEU+2/Yi59rfYnsFQtdtOgAo9GAzysx8ciOM='
		runner_conf.sdkConfig.marketPerm.Level = "1"
		runner_conf.sdkConfig.marketPerm.HKPerms.extend(["hk10"])

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
			runner_conf.sdkConfig.serverSites["sh"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
			runner_conf.sdkConfig.serverSites["sz"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
			runner_conf.sdkConfig.serverSites["bj"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
			runner_conf.sdkConfig.serverSites["cf"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
			runner_conf.sdkConfig.serverSites["nf"].CopyFrom(Site(ips=["http://114.80.155.134:22013"]))
			runner_conf.sdkConfig.serverSites["gf"].CopyFrom(Site(ips=["http://114.80.155.134:22013"]))
			runner_conf.sdkConfig.serverSites["pb"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
			runner_conf.sdkConfig.serverSites["hk1"].CopyFrom(Site(ips=["http://114.80.155.58:8601"]))
			runner_conf.sdkConfig.serverSites["hk5"].CopyFrom(Site(ips=["http://114.80.155.58:8601"]))
			runner_conf.sdkConfig.serverSites["hk10"].CopyFrom(Site(ips=["http://114.80.155.58:8601"]))
			runner_conf.sdkConfig.serverSites["hka1"].CopyFrom(Site(ips=["http://114.80.155.58:8601"]))
			runner_conf.sdkConfig.serverSites["hkd1"].CopyFrom(Site(ips=["http://114.80.155.58:8601"]))
			runner_conf.sdkConfig.serverSites["hkaz"].CopyFrom(Site(ips=["http://114.80.155.58:8601"]))
			runner_conf.sdkConfig.serverSites["hkdz"].CopyFrom(Site(ips=["http://114.80.155.58:8601"]))

		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'OHLCTEST_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'stk': '00700.hk',
				'type': 'dayk'
			})
		])
		runner_conf.casesConfig.extend([case_conf])
		runner_conf_list.append(runner_conf)
	return runner_conf_list


def gen2confict_2():
	runner_conf_list = []
	for i in range(2):
		runner_conf = RunnerConfig()
		runner_conf.jobID = 'TJ-1'
		runner_conf.runnerID = generate_id('RUN-A')
		runner_conf.sdkConfig.appKeyIOS = 'VVW0Fno7BEZt1a/y6KLM36uj9qcjw7CAHDwWZKDlWDs='
		runner_conf.sdkConfig.appKeyAndroid = 'J6IPlk5AEU+2/Yi59rfYnsFQtdtOgAo9GAzysx8ciOM='
		runner_conf.sdkConfig.marketPerm.Level = "1"
		runner_conf.sdkConfig.marketPerm.HKPerms.extend(["hk10"])
		# mongoDB位置，存储的数据库位置
		runner_conf.storeConfig.mongoUri = "mongodb://221.228.66.83:30617"
		runner_conf.storeConfig.dbName = "stockSdkTest"

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

		runner_conf.casesConfig.extend([case_conf])

		runner_conf_list.append(runner_conf)
	return runner_conf_list


with DAG(
		dag_id='android_mongo_test',
		default_args={
			'owner': 'airflow',
			'start_date': airflow.utils.dates.days_ago(0),
		},
		schedule_interval='@once',
) as dag:
	runner_conf_list1 = initRunnerConfig()
	task_id_to_cmp_list1 = ['adb_cmp_pro_a1', 'adb_cmp_pro_b1']

    

	android_1 = AndroidRunnerOperator(
		task_id=task_id_to_cmp_list1[0],
		provide_context=False,
		apk_id='com.chi.ssetest',
		apk_version='release-20191210-0.0.2',
		runner_conf=runner_conf_list1[0]
	)

	android_2 = AndroidRunnerOperator(
		task_id=task_id_to_cmp_list1[1],
		provide_context=False,
		apk_id='com.chi.ssetest',
		apk_version='release-20191210-0.0.2',
		runner_conf=runner_conf_list1[1]
	)

	android_cmp1 = DataCompareOperator(
		task_id='data_compare',
		task_id_list=task_id_to_cmp_list1,
		retries=3,
		provide_context=False,
		runner_conf=runner_conf_list1[1],
		dag=dag
	)

	[android_1, android_2] >> android_cmp1

if __name__ == "__main__":
	dag.cli()