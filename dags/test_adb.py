import json

import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator

from operators.data_compare_operator import DataCompareOperator
from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig, Site
from operators.android_runner_operator import AndroidRunnerOperator
from operators.android_release_operator import AndroidReleaseOperator

# TODO init RunnerConfig
def initRunnerConfig():
	runner_conf_list = []

	for i in range(2):
		runner_conf = RunnerConfig()

		runner_conf.sdkConfig.appKeyIOS = 'VVW0Fno7BEZt1a/y6KLM36uj9qcjw7CAHDwWZKDlWDs='
		runner_conf.sdkConfig.appKeyAndroid = 'J6IPlk5AEU+2/Yi59rfYnsFQtdtOgAo9GAzysx8ciOM='
		runner_conf.sdkConfig.marketPerm.Level = "2"
		runner_conf.sdkConfig.marketPerm.HKPerms.extend(["hk10", "hka1"])

		if i == 0:
			runner_conf.sdkConfig.serverSites["sh"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
		else:
			runner_conf.sdkConfig.serverSites["sh"].CopyFrom(Site(ips=["http://114.80.155.58:8601"]))

		case_list = []

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
		print('i,case_list.length is ',case_list.__len__())
		runner_conf_list.append(runner_conf)

	return runner_conf_list

with DAG(
		dag_id='android_test',
		default_args={
			'owner': 'airflow',
			'start_date': airflow.utils.dates.days_ago(0)
		},
		schedule_interval='@once',
) as dag:
	run_this_last = DummyOperator(
		task_id='run_this_last',
		queue='android'
	)

	runner_conf_list = initRunnerConfig()
	task_id_to_cmp_list = ['adb_shell_cmp_a','adb_shell_cmp_b']

	android_release = AndroidReleaseOperator(
		task_id='android_release',
		provide_context=False,
		repo_name='stocksdktest/AndroidTestRunner',
		tag_id='release-20191028-0.0.1',
		tag_sha='83eab8326e7901d744599bff60defaea135f7bf0',
		runner_conf=runner_conf_list[0]
	)

	android_a = AndroidRunnerOperator(
		task_id=task_id_to_cmp_list[0],
		provide_context=False,
		apk_id='com.chi.ssetest',
		apk_version='release-20191028-0.0.1',
		runner_conf=runner_conf_list[0]
	)

	android_b = AndroidRunnerOperator(
		task_id=task_id_to_cmp_list[1],
		provide_context=False,
		apk_id='com.chi.ssetest',
		apk_version='release-20191028-0.0.1',
		runner_conf=runner_conf_list[1]
	)

	android_cmp = DataCompareOperator(
		task_id='data_compare',
		task_id_list=task_id_to_cmp_list,
		retries=3,
		provide_context=False,
		runner_conf=RunnerConfig,
		dag=dag
	)

	android_release >> [android_a, android_b] >> android_cmp >> run_this_last

if __name__ == "__main__":
	dag.cli()
