import json

import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
from operators.data_compare_operator import DataCompareOperator
from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig, Site
from operators.android_runner_operator import AndroidRunnerOperator
from operators.android_release_operator import AndroidReleaseOperator
#.全真和测试（新版SDK）对比
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
		runner_conf.storeConfig.collectionName = "debug"
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
			runner_conf.sdkConfig.serverSites["sh"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
			runner_conf.sdkConfig.serverSites["shl2"].CopyFrom(Site(ips=["http://114.80.155.50:22016"]))
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

		#测试样例
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'QUOTEDETAIL_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
		    #001
		    json.dumps({
				'CODES': '600000.sh',
			}),
		])
		case_list.append(case_conf)
		# 新债列表
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_BNDNEWSHARESCAL_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			#005 
			json.dumps({
				'date': '2019-11-13',
				'src': 'd'
			}),
			#006
			json.dumps({
				'date': '2019-11-13',
				'src': 'd'
			}),
		])
		case_list.append(case_conf)		
		# #新债详情
		# case_conf = TestcaseConfig()
		# case_conf.testcaseID = 'F10_BNDSHAREIPODETAI_1'
		# case_conf.roundIntervalSec = 3
		# case_conf.continueWhenFailed = False
		# case_conf.paramStrs.extend([
		# 	#007
		# 	json.dumps({
		# 		'code': '110061.sh',
		# 		'src': 'd'
		# 	}),
		# ])
		# case_list.append(case_conf)
		#.................................445....................................
		# #分量区间统计请求--L2,只支持沪深
		# case_conf = TestcaseConfig()
		# case_conf.testcaseID = 'MOREVOLUMETEST_1'
		# case_conf.roundIntervalSec = 3
		# case_conf.continueWhenFailed = False
		# case_conf.paramStrs.extend([
		# 	#001 
		# 	json.dumps({
		# 		'code': '600000.sh',
		# 		'subtype': '1001'
		# 	}),
		# 	#002 
		# 	json.dumps({
		# 		'code': '688001.sh',
		# 		'subtype': '1006'
		# 	}),
		# 	#003
		# 	json.dumps({
		# 		'code': '900903.sh',
		# 		'subtype': '1002'
		# 	}),
		# 	#004 
		# 	json.dumps({
		# 		'code': '000001.sh',
		# 		'subtype': '1400'
		# 	}),
		# 	#005 
		# 	json.dumps({
		# 		'code': '502058.sh',
		# 		'subtype': '1100'
		# 	}),
		# 	#006 
		# 	json.dumps({
		# 		'code': '513680.sh',
		# 		'subtype': '1120'
		# 	}),
		# 	#007 
		# 	json.dumps({
		# 		'code': '501311.sh',
		# 		'subtype': '1110'
		# 	}),
		# 	#008
		# 	json.dumps({
		# 		'code': '124418.sh',
		# 		'subtype': '1300'
		# 	}),
		# 	#009 
		# 	json.dumps({
		# 		'code': '204001.sh',
		# 		'subtype': '1311'
		# 	}),
		# 	#010
		# 	json.dumps({
		# 		'code': '113544.sh',
		# 		'subtype': '1312'
		# 	}),
		# 	#011
		# 	json.dumps({
		# 		'code': '10001910.sh',
		# 		'subtype': '3002'
		# 	}),
		# 	#012 
		# 	json.dumps({
		# 		'code': '600003.sh',
		# 		'subtype': '9800'
		# 	}),
		# 	#013 
		# 	json.dumps({
		# 		'code': '600610.sh',
		# 		'subtype': '1011'
		# 	}),
		# 	#014
		# 	json.dumps({
		# 		'code': '900951.sh',
		# 		'subtype': 'SHS'
		# 	}),
		# 	#015
		# 	json.dumps({
		# 		'code': '020322.sh',
		# 		'subtype': '1313'
		# 	}),
		# 	#016
		# 	json.dumps({
		# 		'code': '120702.sh',
		# 		'subtype': '1314'
		# 	}),
		# 	#017
		# 	json.dumps({
		# 		'code': '001979.sz',
		# 		'subtype': '1005'
		# 	}),
		# 	#018
		# 	json.dumps({
		# 		'code': '000001.sz',
		# 		'subtype': '1001'
		# 	}),
		# 	#019
		# 	json.dumps({
		# 		'code': '002524.sz',
		# 		'subtype': '1003'
		# 	}),
		# 	#020
		# 	json.dumps({
		# 		'code': '300484.sz',
		# 		'subtype': '1004'
		# 	}),
		# 	#021 
		# 	json.dumps({
		# 		'code': '200986.sz',
		# 		'subtype': '1002'
		# 	}),
		# 	#022 
		# 	json.dumps({
		# 		'code': '399001.sz',
		# 		'subtype': '1400'
		# 	}),
		# 	#023
		# 	json.dumps({
		# 		'code': '150258.sz',
		# 		'subtype': '1100'
		# 	}),
		# 	#024
		# 	json.dumps({
		# 		'code': '159955.sz',
		# 		'subtype': '1120'
		# 	}),
		# 	#025
		# 	json.dumps({
		# 		'code': '169301.sz',
		# 		'subtype': '1110'
		# 	}),
		# 	#026
		# 	json.dumps({
		# 		'code': '123007.sz',
		# 		'subtype': '1300'
		# 	}),
		# 	#027
		# 	json.dumps({
		# 		'code': '128074.sz',
		# 		'subtype': '1312'
		# 	}),
		# 	#028
		# 	json.dumps({
		# 		'code': '131810.sz',
		# 		'subtype': '1311'
		# 	}),
		# 	#029
		# 	json.dumps({
		# 		'code': '101988.sz',
		# 		'subtype': '1313'
		# 	}),
		# 	#030
		# 	json.dumps({
		# 		'code': '111924.sz',
		# 		'subtype': '1314'
		# 	}),
		# 	#031
		# 	json.dumps({
		# 		'code': '200168.sz',
		# 		'subtype': 'SZS'
		# 	}),
		# 	#032
		# 	json.dumps({
		# 		'code': '002070.sz',
		# 		'subtype': '9800'
		# 	}),
		# 	#033
		# 	json.dumps({
		# 		'code': '000995.sz',
		# 		'subtype': '1011'
		# 	}),
		# ])
		# case_list.append(case_conf)

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
	start_task = DummyOperator(
		task_id='run_this_first',
		queue='worker'
	)

	run_this_last = DummyOperator(
		task_id='run_this_last',
		queue='worker'
	)

	runner_conf_list = initRunnerConfig()
	task_id_to_cmp_list = ['adb_shell_cmp_a','adb_shell_cmp_b']

	android_release = AndroidReleaseOperator(
		task_id='android_release', 
		provide_context=False,
		repo_name='stocksdktest/AndroidTestRunner',
		tag_id='release-20191211-0.0.1',
		tag_sha='f2d7516dbbf2d1dbc93fd28220e8ad693213141f',
		runner_conf=runner_conf_list[0]
	)

	android_a = AndroidRunnerOperator(
		task_id=task_id_to_cmp_list[0],
		provide_context=False,
		apk_id='com.chi.ssetest',
		apk_version='release-20191211-0.0.1',
		runner_conf=runner_conf_list[0]
	)

	android_b = AndroidRunnerOperator(
		task_id=task_id_to_cmp_list[1],
		provide_context=False,
		apk_id='com.chi.ssetest',
		apk_version='release-20191211-0.0.1',
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

	# android_cmp2 = DataCompareOperator(
	# 	task_id='data_compare2',
	# 	task_id_list=task_id_to_cmp_list,
	# 	retries=3,
	# 	provide_context=False,
	# 	runner_conf=RunnerConfig,
	# 	dag=dag
	# )

	start_task >> android_release >> [android_a, android_b] >> android_cmp >> run_this_last
	# start_task >> android_release >> android_a >> android_cmp >> run_this_last

if __name__ == "__main__":
	dag.cli()
