import json

import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
from operators.data_compare_operator import DataCompareOperator
from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig, Site
from operators.android_runner_operator import AndroidRunnerOperator
from operators.android_release_operator import AndroidReleaseOperator
#.a测试，b生产
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
		runner_conf.storeConfig.collectionName = "F10_1219"
		# runner_conf.storeConfig.collectionName = "debug"
		if i == 0:
			runner_conf.sdkConfig.serverSites["sh"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
			runner_conf.sdkConfig.serverSites["shl2"].CopyFrom(Site(ips=["http://114.80.155.62:22016"]))
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
			runner_conf.sdkConfig.serverSites["hkd1"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
			runner_conf.sdkConfig.serverSites["hkaz"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
			runner_conf.sdkConfig.serverSites["hkdz"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
		else:
			runner_conf.sdkConfig.serverSites["sh"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
			runner_conf.sdkConfig.serverSites["shl2"].CopyFrom(Site(ips=["http://114.80.155.50:22016"]))
			runner_conf.sdkConfig.serverSites["sz"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
			runner_conf.sdkConfig.serverSites["bj"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
			runner_conf.sdkConfig.serverSites["cf"].CopyFrom(Site(ips=["http://114.80.155.61:22016"]))
			runner_conf.sdkConfig.serverSites["nf"].CopyFrom(Site(ips=["http://58.63.252.23:22013"]))
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
		#最新指标
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_NEWINDEX_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'code': '00810.hk',
				'src': 'd',
			}),
			json.dumps({
				'code': '00700.hk',
				'src': 'd',
			}),
				json.dumps({
				'code': '08292.hk',
				'src': 'd',
			}),
			json.dumps({
				'code': '00001.hk',
				'src': 'd',
			}),
				json.dumps({
				'code': '00885.hk',
				'src': 'd',
			}),
			json.dumps({
				'code': '00033.hk',
				'src': 'd',
			}),
		])
		case_list.append(case_conf)
		#分红配送
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_BONUSFINANCE_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'code': '00670.hk',
				'src': 'd',
			}),
			json.dumps({
				'code': '00700.hk',
				'src': 'd',
			}),
				json.dumps({
				'code': '00498.hk',
				'src': 'd',
			}),
			json.dumps({
				'code': '00001.hk',
				'src': 'd',
			}),
				json.dumps({
				'code': '00885.hk',
				'src': 'd',
			}),
			json.dumps({
				'code': '01133.hk',
				'src': 'd',
			}),
		])
		case_list.append(case_conf)
		# #融资融券
		# case_conf = TestcaseConfig()
		# case_conf.testcaseID = 'F10_TRADEDETAIL_1'
		# case_conf.roundIntervalSec = 3
		# case_conf.continueWhenFailed = False
		# case_conf.paramStrs.extend([
		# 	json.dumps({
		# 		'code': '600000.sh',
		# 		'src': 'd',
		# 	}),
		# 	json.dumps({
		# 		'code': '000001.sz',
		# 		'src': 'd',
		# 	}),
		# 	json.dumps({
		# 		'code': '601010.sh ',
		# 		'src': 'd',
		# 	}),
		# 	json.dumps({
		# 		'code': '600936.sh',
		# 		'src': 'd',
		# 	}),
		# 	json.dumps({
		# 		'code': '300194.sz',
		# 		'src': 'd',
		# 	}),
		# ])
		# case_list.append(case_conf)
		#基本情况
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_COMPANYINFO_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'code': '00670.hk',
				'src': 'd',
			}),
			json.dumps({
				'code': '00700.hk',
				'src': 'd',
			}),
				json.dumps({
				'code': '00498.hk',
				'src': 'd',
			}),
			json.dumps({
				'code': '00001.hk',
				'src': 'd',
			}),
				json.dumps({
				'code': '00885.hk',
				'src': 'd',
			}),
			json.dumps({
				'code': '01133.hk',
				'src': 'd',
			}),
		])
		case_list.append(case_conf)
		#管理层
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_LEADERPERSONINFO_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'code': '00670.hk',
				'src': 'd',
			}),
			json.dumps({
				'code': '00700.hk',
				'src': 'd',
			}),
				json.dumps({
				'code': '00498.hk',
				'src': 'd',
			}),
			json.dumps({
				'code': '00001.hk',
				'src': 'd',
			}),
				json.dumps({
				'code': '00885.hk',
				'src': 'd',
			}),
			json.dumps({
				'code': '01133.hk',
				'src': 'd',
			}),
		])
		case_list.append(case_conf)
		#财务报表
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_MAINFINADATANASS_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([            
			json.dumps({
				'stockId': '00670.hk',
				'dataSourceType': 'd',
			}),
			json.dumps({
				'stockId': '00700.hk',
				'dataSourceType': 'd',
			}),
				json.dumps({
				'stockId': '00498.hk',
				'dataSourceType': 'd',
			}),
			json.dumps({
				'stockId': '00001.hk',
				'dataSourceType': 'd',
			}),
				json.dumps({
				'stockId': '00885.hk',
				'dataSourceType': 'd',
			}),
			json.dumps({
				'stockId': '01133.hk',
				'dataSourceType': 'd',
			}),
		])
		case_list.append(case_conf)
		# #财务报表--仅用于港股
		# case_conf = TestcaseConfig()
		# case_conf.testcaseID = 'F10_MAINFINADATANASS_2'
		# case_conf.roundIntervalSec = 3
		# case_conf.continueWhenFailed = False
		# case_conf.paramStrs.extend([
		# 	json.dumps({
		# 		'stockId': '04508.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'null',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00700.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'null',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00810.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'null',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00001.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'null',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '04508.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'N',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00700.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'N',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00810.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'N',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00001.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'N',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '04508.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_0',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00700.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_0',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00810.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_0',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00001.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_0',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '04508.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_1',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00700.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_1',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00810.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_1',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00001.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_1',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '04508.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_2',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00700.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_2',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00810.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_2',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00001.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_2',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '04508.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_3',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00700.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_3',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00810.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_3',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00001.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_3',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '04508.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_4',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00700.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_4',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00810.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_4',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00001.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_4',
		# 	}),
		# ])
		# case_list.append(case_conf)
		# #财务指标
		# case_conf = TestcaseConfig()
		# case_conf.testcaseID = 'F10_MAINFINAINDEXNAS_1'
		# case_conf.roundIntervalSec = 3
		# case_conf.continueWhenFailed = False
		# case_conf.paramStrs.extend([
		# 	json.dumps({
		# 		'stockId': '04508.hk',
		# 		'dataSourceType': 'd',
		# 	}), 
		# 	json.dumps({
		# 		'stockId': '00810.hk',
		# 		'dataSourceType': 'd',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00001.hk',
		# 		'dataSourceType': 'd',
		# 	}),
		# ])
		# case_list.append(case_conf)
		# #财务指标--仅用于港股
		# case_conf = TestcaseConfig()
		# case_conf.testcaseID = 'F10_MAINFINAINDEXNAS_2'
		# case_conf.roundIntervalSec = 3
		# case_conf.continueWhenFailed = False
		# case_conf.paramStrs.extend([
		# 	json.dumps({
		# 		'stockId': '04508.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'null',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00700.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'null',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00810.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'null',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00001.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'null',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '04508.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'N',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00700.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'N',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00810.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'N',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00001.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'N',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '04508.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_0',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00700.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_0',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00810.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_0',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00001.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_0',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '04508.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_1',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00700.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_1',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00810.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_1',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00001.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_1',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '04508.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_2',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00700.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_2',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00810.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_2',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00001.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_2',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '04508.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_3',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00700.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_3',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00810.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_3',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00001.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_3',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '04508.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_4',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00700.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_4',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00810.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_4',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '00001.hk',
		# 		'dataSourceType': 'd',
		# 		'cueryContent':'BASICEPS_4',
		# 	}),
		# ])
		# case_list.append(case_conf)
		#股本变动
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_STOCKSHARECHANGEINFO_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([      
			json.dumps({
				'code': '00670.hk',
				'src': 'd',
			}),
			json.dumps({
				'code': '00700.hk',
				'src': 'd',
			}),
				json.dumps({
				'code': '00498.hk',
				'src': 'd',
			}),
			json.dumps({
				'code': '00001.hk',
				'src': 'd',
			}),
				json.dumps({
				'code': '00885.hk',
				'src': 'd',
			}),
			json.dumps({
				'code': '01133.hk',
				'src': 'd',
			}),
		])
		case_list.append(case_conf)
		#股东变动
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_SHAREHOLDERHISTORYINFO_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'code': '00670.hk',
				'src': 'd',
			}),
			json.dumps({
				'code': '00700.hk',
				'src': 'd',
			}),
				json.dumps({
				'code': '00498.hk',
				'src': 'd',
			}),
			json.dumps({
				'code': '00001.hk',
				'src': 'd',
			}),
				json.dumps({
				'code': '00885.hk',
				'src': 'd',
			}),
			json.dumps({
				'code': '01133.hk',
				'src': 'd',
			}),
		])
		case_list.append(case_conf)
		#最新十大流通股股东
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_TOPLIQUIDSHAREHOLDER_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'code': '00969.hk',
				'src': 'd',
			}),
			json.dumps({
				'code': '00810.hk',
				'src': 'd',
			}),
		])
		case_list.append(case_conf)
		#最新十大股东
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_TOPSHAREHOLDER_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'code': '00119.hk',
				'src': 'd',
			}),
			json.dumps({
				'code': '00810.hk',
				'src': 'd',
			}),
				json.dumps({
				'code': '00969.hk',
				'src': 'd',
			}),
			json.dumps({
				'code': '00700.hk',
				'src': 'd',
			}),
				json.dumps({
				'code': '00001.hk',
				'src': 'd',
			}),
			json.dumps({
				'code': '01133.hk',
				'src': 'd',
			}),
		])
		case_list.append(case_conf)
		#个股/自选公告1
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_STOCKBULLETINLIST_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'stockId': '603722.sh',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '002654.sz',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '900921.sh',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '200625.sz',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '512720.sh',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '150146.sz',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '113549.sh',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '128029.sz',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '204003.sh',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '131806.sz',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}), 
			json.dumps({
				'stockId': '00969.hk',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '832001.bj',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '603722.sh',
				'updateType': '5',
				'newsID': '603722.sh_567932',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '002654.sz',
				'updateType': '5',
				'newsID': '002654.sz_5710440',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '900921.sh',
				'updateType': '5',
				'newsID': '900921.sh_5783631',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '200625.sz',
				'updateType': '5',
				'newsID': '200625.sz_567786',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '512720.sh',
				'updateType': '5',
				'newsID': '512720.sh_1570647',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '150146.sz',
				'updateType': '5',
				'newsID': '150146.sz_1729191',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '113549.sh',
				'updateType': '5',
				'newsID': '113549.sh_12793420',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '128029.sz',
				'updateType': '5',
				'newsID': '128029.sz_11699269',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '204003.sh',
				'updateType': '5',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '131806.sz',
				'updateType': '5',
				'newsID': 'null',
				'src': 'd',
			}), 
			json.dumps({
				'stockId': '00969.hk',
				'updateType': '5',
				'newsID': '00969.hk_1406236',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '832001.bj',
				'updateType': '5',
				'newsID': '832001.bj_5520624',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '603722.sh',
				'updateType': '6',
				'newsID': '603722.sh_567932',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '002654.sz',
				'updateType': '6',
				'newsID': '002654.sz_5710440',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '900921.sh',
				'updateType': '6',
				'newsID': '900921.sh_5783631',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '200625.sz',
				'updateType': '6',
				'newsID': '200625.sz_567786',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '512720.sh',
				'updateType': '6',
				'newsID': '512720.sh_1570647',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '150146.sz',
				'updateType': '6',
				'newsID': '150146.sz_1729191',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '113549.sh',
				'updateType': '6',
				'newsID': '113549.sh_12793420',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '128029.sz',
				'updateType': '6',
				'newsID': '128029.sz_11699269',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '204003.sh',
				'updateType': '6',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '131806.sz',
				'updateType': '6',
				'newsID': 'null',
				'src': 'd',
			}), 
			json.dumps({
				'stockId': '00969.hk',
				'updateType': '6',
				'newsID': '00969.hk_1406236',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '832001.bj',
				'updateType': '6',
				'newsID': '832001.bj_5520624',
				'src': 'd',
			}),
		])
		case_list.append(case_conf)
		#个股/自选公告2
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_STOCKBULLETINLIST_2'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'stockId': '603722.sh',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '002654.sz',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '900921.sh',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '200625.sz',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '512720.sh',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '150146.sz',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '113549.sh',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '128029.sz',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '204003.sh',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '131806.sz',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}), 
			json.dumps({
				'stockId': '00969.hk',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '832001.bj',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '603722.sh',
				'updateType': '5',
				'newsID': '603722.sh_5658294',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '002654.sz',
				'updateType': '5',
				'newsID': '002654.sz_5710440',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '900921.sh',
				'updateType': '5',
				'newsID': '900921.sh_5783634',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '200625.sz',
				'updateType': '5',
				'newsID': '200625.sz_5677867',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '512720.sh',
				'updateType': '5',
				'newsID': '512720.sh_1629178',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '150146.sz',
				'updateType': '5',
				'newsID': '150146.sz_1686502',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '113549.sh',
				'updateType': '5',
				'newsID': '113549.sh_12724352',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '128029.sz',
				'updateType': '5',
				'newsID': '128029.sz_11925667',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '204003.sh',
				'updateType': '5',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '131806.sz',
				'updateType': '5',
				'newsID': 'null',
				'count':'10',
				'src': 'd',
			}), 
			json.dumps({
				'stockId': '00969.hk',
				'updateType': '5',
				'newsID': '00969.hk_142948',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '832001.bj',
				'updateType': '5',
				'newsID': '832001.bj_5548641',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '603722.sh',
				'updateType': '6',
				'newsID': '603722.sh_5658294',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '002654.sz',
				'updateType': '6',
				'newsID': '002654.sz_5710440',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '900921.sh',
				'updateType': '6',
				'newsID': '900921.sh_5783634',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '200625.sz',
				'updateType': '6',
				'newsID': '200625.sz_5677867',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '512720.sh',
				'updateType': '6',
				'newsID': '512720.sh_1629178',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '150146.sz',
				'updateType': '6',
				'newsID': '150146.sz_1686502',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '113549.sh',
				'updateType': '6',
				'newsID': '113549.sh_12724352',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '128029.sz',
				'updateType': '6',
				'newsID': '128029.sz_11925667',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '204003.sh',
				'updateType': '6',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '131806.sz',
				'updateType': '6',
				'newsID': 'null',
				'count':'10',
				'src': 'd',
			}), 
			json.dumps({
				'stockId': '00969.hk',
				'updateType': '6',
				'newsID': '00969.hk_142948',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '832001.bj',
				'updateType': '6',
				'newsID': '832001.bj_5548641',
				'count':'50',
				'src': 'd',
			}),
		])
		case_list.append(case_conf)
		#个股公告内文
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_STOCKBULLETIN_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
			'bulletinID': '603722.sh_5788845',
			'src': 'd',
		    }),	
		    json.dumps({
				'bulletinID': '603722.sh_5658294',
				'src': 'd',
			}),
			json.dumps({
				'bulletinID': '002654.sz_5710440',
				'src': 'd',
			}),
			json.dumps({
				'bulletinID': '900921.sh_5783634',
				'src': 'd',
			}),
			json.dumps({
				'bulletinID': '200625.sz_5677867',
				'src': 'd',
			}),
			json.dumps({
				'bulletinID': '512720.sh_1629178',
				'src': 'd',
			}),
			json.dumps({
				'bulletinID': '150146.sz_1686502',
				'src': 'd',
			}),
			json.dumps({
				'bulletinID': '113549.sh_12724352',
				'src': 'd',
			}),
			json.dumps({
				'bulletinID': '128029.sz_11925667',
				'src': 'd',
			}), 
			json.dumps({
				'bulletinID': '00969.hk_142948',
				'src': 'd',
			}),
			json.dumps({
				'bulletinID': '832001.bj_5548641',
				'src': 'd',
			}),
		])
		case_list.append(case_conf)
		#个股/自选新闻1
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_STOCKNEWSLIST_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'stockId': '603722.sh',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '002654.sz',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '900921.sh',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '200625.sz',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '512720.sh',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '150146.sz',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '113549.sh',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '128029.sz',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '204003.sh',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '131806.sz',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}), 
			json.dumps({
				'stockId': '00969.hk',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '832001.bj',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '603722.sh',
				'updateType': '5',
				'newsID': '603722.sh_20190827020009234661',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '002654.sz',
				'updateType': '5',
				'newsID': '002654.sz_20191108030001134306',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '900921.sh',
				'updateType': '5',
				'newsID': '900921.sh_20191030020009741980',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '200625.sz',
				'updateType': '5',
				'newsID': '200625.sz_20191212020010166369',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '512720.sh',
				'updateType': '5',
				'newsID': '512720.sh_20191211020010158655',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '150146.sz',
				'updateType': '5',
				'newsID': '150146.sz_20191209020010131595',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '113549.sh',
				'updateType': '5',
				'newsID': '113549.sh_20191031020009754315',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '128029.sz',
				'updateType': '5',
				'newsID': '128029.sz_20191115030001138080',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '204001.sh',
				'updateType': '5',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '131806.sz',
				'updateType': '5',
				'newsID': 'null',
				'src': 'd',
			}), 
			json.dumps({
				'stockId': '00700.hk',
				'updateType': '5',
				'newsID': '00700.hk_20191219020010237181',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '832001.bj',
				'updateType': '5',
				'newsID': '832001.bj_20190912030001093778',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '603722.sh',
				'updateType': '6',
				'newsID': '603722.sh_20190827020009234661',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '002654.sz',
				'updateType': '6',
				'newsID': '002654.sz_20191108030001134306',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '900921.sh',
				'updateType': '6',
				'newsID': '900921.sh_20191030020009741980',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '200625.sz',
				'updateType': '6',
				'newsID': '200625.sz_20191212020010166369',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '512720.sh',
				'updateType': '6',
				'newsID': '512720.sh_20191211020010158655',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '150146.sz',
				'updateType': '6',
				'newsID': '150146.sz_20191209020010131595',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '113549.sh',
				'updateType': '6',
				'newsID': '113549.sh_20191031020009754315',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '128029.sz',
				'updateType': '6',
				'newsID': '128029.sz_20191115030001138080',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '204001.sh',
				'updateType': '6',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '131806.sz',
				'updateType': '6',
				'newsID': 'null',
				'src': 'd',
			}), 
			json.dumps({
				'stockId': '00969.hk',
				'updateType': '6',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '832001.bj',
				'updateType': '6',
				'newsID': '832001.bj_20190912030001093778',
				'src': 'd',
			}),
		])
		case_list.append(case_conf)
		#个股/自选新闻2
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_STOCKNEWSLIST_2'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'stockId': '603722.sh',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '002654.sz',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '900921.sh',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '200625.sz',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '512720.sh',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '150146.sz',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '113549.sh',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '128029.sz',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '204003.sh',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '131806.sz',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}), 
			json.dumps({
				'stockId': '00969.hk',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '832001.bj',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '603722.sh',
				'updateType': '5',
				'newsID': '603722.sh_20190827020009234661',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '002654.sz',
				'updateType': '5',
				'newsID': '002654.sz_20191108030001134306',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '900921.sh',
				'updateType': '5',
				'newsID': '900921.sh_20191030020009741980',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '200625.sz',
				'updateType': '5',
				'newsID': '200625.sz_20191212020010166369',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '512720.sh',
				'updateType': '5',
				'newsID': '512720.sh_20191211020010158655',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '150146.sz',
				'updateType': '5',
				'newsID': '150146.sz_20191209020010131595',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '113549.sh',
				'updateType': '5',
				'newsID': '113549.sh_20191031020009754315',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '128029.sz',
				'updateType': '5',
				'newsID': '128029.sz_20191115030001138080',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '204001.sh',
				'count':'50',
				'updateType': '5',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '131806.sz',
				'count':'50',
				'updateType': '5',
				'newsID': 'null',
				'src': 'd',
			}), 
			json.dumps({
				'stockId': '00969.hk',
				'updateType': '5',
				'newsID': '00969.hk_20190920020009407023',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '00700.hk',
				'updateType': '5',
				'newsID': '00700.hk_20191219020010232886',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '832001.bj',
				'updateType': '5',
				'newsID': '832001.bj_20190912030001093778',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '603722.sh',
				'updateType': '6',
				'newsID': '603722.sh_20190827020009234661',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '002654.sz',
				'updateType': '6',
				'newsID': '002654.sz_20191108030001134306',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '900921.sh',
				'updateType': '6',
				'newsID': '900921.sh_20191030020009741980',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '200625.sz',
				'updateType': '6',
				'newsID': '200625.sz_20191212020010166369',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '512720.sh',
				'updateType': '6',
				'newsID': '512720.sh_20191211020010158655',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '150146.sz',
				'updateType': '6',
				'newsID': '150146.sz_20191209020010131595',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '113549.sh',
				'updateType': '6',
				'newsID': '113549.sh_20191031020009754315',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '128029.sz',
				'updateType': '6',
				'newsID': '128029.sz_20191115030001138080',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '204001.sh',
				'updateType': '6',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '131806.sz',
				'updateType': '6',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}), 
			json.dumps({
				'stockId': '00969.hk',
				'updateType': '6',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '00700.hk',
				'updateType': '6',
				'newsID': '00700.hk_20191219020010232886',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '832001.bj',
				'updateType': '6',
				'newsID': '832001.bj_20190912030001093778',
				'count':'50',
				'src': 'd',
			}),
		])
		case_list.append(case_conf)
		# #个股新闻内文
		# case_conf = TestcaseConfig()
		# case_conf.testcaseID = 'F10_STOCKNEWS_1'
		# case_conf.roundIntervalSec = 3
		# case_conf.continueWhenFailed = False
		# case_conf.paramStrs.extend([
		# 	json.dumps({
		# 		'bulletinID': '603722.sh_20191122030001142539',
		# 	'src': 'd',
		# 	}),	
		# 	json.dumps({
		# 		'bulletinID': '603722.sh_20190827020009234661',
		# 		'src': 'd',
		# 	}),
		# 	json.dumps({
		# 		'bulletinID': '002654.sz_20191108030001134306',
		# 		'src': 'd',
		# 	}),
		# 	json.dumps({
		# 		'bulletinID': '900921.sh_20191030020009741980',
		# 		'src': 'd',
		# 	}),
		# 	json.dumps({
		# 		'bulletinID': '200625.sz_20191212020010166369',
		# 		'src': 'd',
		# 	}),
		# 	json.dumps({
		# 		'bulletinID': '512720.sh_20191211020010158655',
		# 		'src': 'd',
		# 	}),
		# 	json.dumps({
		# 		'bulletinID': '150146.sz_20191209020010131595',
		# 		'src': 'd',
		# 	}),
		# 	json.dumps({
		# 		'bulletinID': '113549.sh_20191031020009754315',
		# 		'src': 'd',
		# 	}),
		# 	json.dumps({
		# 		'bulletinID': '128029.sz_20191115030001138080',
		# 		'src': 'd',
		# 	}),
		# 	json.dumps({
		# 		'bulletinID': '00700.hk_20191219020010237181',
		# 		'src': 'd',
		# 	}),
		# 	json.dumps({
		# 		'bulletinID': '832001.bj_20190912030001093778',
		# 		'src': 'd',
		# 	}),
		# ])
		# case_list.append(case_conf)
		#个股/自选研报1
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_STOCKREPORTLIST_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'stockId': '603722.sh',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '002654.sz',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '900921.sh',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '200625.sz',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '512720.sh',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '150146.sz',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '113549.sh',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '128029.sz',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '204003.sh',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '131806.sz',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}), 
			json.dumps({
				'stockId': '00969.hk',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '832001.bj',
				'updateType': '-1',
				'newsID': 'null',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '600000.sh',
				'updateType': '5',
				'newsID': '600000.sh_4634313',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '002654.sz',
				'updateType': '5',
				'newsID': '000001.sz_4608862',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '00700.hk',
				'updateType': '5',
				'newsID': '00700.hk_4679847',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '600000.sh',
				'updateType': '6',
				'newsID': '600000.sh_4634313',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '002654.sz',
				'updateType': '6',
				'newsID': '000001.sz_4608862',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '00700.hk',
				'updateType': '6',
				'newsID': '00700.hk_4679847',
				'src': 'd',
			}),
		])
		case_list.append(case_conf)
		#个股/自选研报2
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_STOCKREPORTLIST_2'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'stockId': '603722.sh',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '002654.sz',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '900921.sh',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '200625.sz',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '512720.sh',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '150146.sz',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '113549.sh',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '128029.sz',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '204003.sh',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '131806.sz',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}), 
			json.dumps({
				'stockId': '00969.hk',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '832001.bj',
				'updateType': '-1',
				'newsID': 'null',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '600000.sh',
				'updateType': '5',
				'newsID': '600000.sh_4634313',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '002654.sz',
				'updateType': '5',
				'newsID': '000001.sz_4608862',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '00700.hk',
				'updateType': '5',
				'newsID': '00700.hk_4679847',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '600000.sh',
				'updateType': '6',
				'newsID': '600000.sh_4634313',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '002654.sz',
				'updateType': '6',
				'newsID': '000001.sz_4608862',
				'count':'50',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '00700.hk',
				'updateType': '6',
				'newsID': '00700.hk_4679847',
				'count':'50',
				'src': 'd',
			}),
		])
		case_list.append(case_conf)
		# #个股研报内文
		# case_conf = TestcaseConfig()
		# case_conf.testcaseID = 'F10_STOCKREPORT_1'
		# case_conf.roundIntervalSec = 3
		# case_conf.continueWhenFailed = False
		# case_conf.paramStrs.extend([
		# 	json.dumps({
		# 		'bulletinID': '603722.sh_4760155',
		# 	'src': 'd',
		# 	}),	
		# 	json.dumps({
		# 		'bulletinID': '600000.sh_4634313',
		# 		'src': 'd',
		# 	}),
		# 	json.dumps({
		# 		'bulletinID': '000001.sz_4608862',
		# 		'src': 'd',
		# 	}),
		# 	json.dumps({
		# 		'bulletinID': '00700.hk_4679847',
		# 		'src': 'd',
		# 	}),
		# ])
		# case_list.append(case_conf)
		# #新股日历
		# case_conf = TestcaseConfig()
		# case_conf.testcaseID = 'F10_CALENDAR_1'
		# case_conf.roundIntervalSec = 3
		# case_conf.continueWhenFailed = False
		# case_conf.paramStrs.extend([
		# 	json.dumps({
		# 		'src': 'd',	
		# 	}),
		# ])
		# case_list.append(case_conf)	
		#基金净值（五日）
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_FUNDVALUE_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'stockId': '512870.sh',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '150151.sz',
				'src': 'd',
			}),
		])
		case_list.append(case_conf)
		#基金概况
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_FUNDBASIC_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'stockId': '512480.sh',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '150238.sz',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '512760.sh',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '512870.sh',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '150151.sz',
				'src': 'd',
			}),
		])
		case_list.append(case_conf)	
		#基金净值（12月）
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_FNDNAVINDEX_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'stockId': '512480.sh',
				'src': 'd',
				'type':'12',
			}),
			json.dumps({
				'stockId': '150238.sz',
				'src': 'd',
				'type':'12',
			}),
			json.dumps({
				'stockId': '512760.sh',
				'src': 'd',
				'type':'12',
			}),
			json.dumps({
				'stockId': '512870.sh',
				'src': 'd',
				'type':'12',
			}),
			json.dumps({
				'stockId': '150151.sz',
				'src': 'd',
				'type':'12',
			}),
		])
		case_list.append(case_conf)
		#资产配置
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_ASSETALLOCATION_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'stockId': '512480.sh',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '150238.sz',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '512760.sh',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '512870.sh',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '150151.sz',
				'src': 'd',
			}),
		])
		case_list.append(case_conf)	
		#行业组合
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_INDUSTRYPORTFOLIO_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'stockId': '512480.sh',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '150238.sz',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '512760.sh',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '512870.sh',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '150151.sz',
				'src': 'd',
			}),
		])
		case_list.append(case_conf)
		#股票组合
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_STOCKPORTFOLIO_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'stockId': '512480.sh',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '150238.sz',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '512760.sh',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '512870.sh',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '150151.sz',
				'src': 'd',
			}),
		])
		case_list.append(case_conf)	
		#///////////////////////////2222///////////////////////////////
		#份额结构
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_SHARESTRUCTURE_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'stockId': '512480.sh',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '150238.sz',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '512760.sh',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '512870.sh',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '150151.sz',
				'src': 'd',
			}),
		])
		case_list.append(case_conf)	
		#基金财务
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_FNDFINANCE_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'stockId': '512870.sh',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '150151.sz',
				'src': 'd',
			}),
		])
		case_list.append(case_conf)
		#基金分红
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_FNDDIVIDEEND_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'stockId': '512870.sh',
				'src': 'd',
			}),
			json.dumps({
				'stockId': '150151.sz',
				'src': 'd',
			}),
		])
		case_list.append(case_conf)
		# #债券概况
		# case_conf = TestcaseConfig()
		# case_conf.testcaseID = 'F10_BONDBASIC_1'
		# case_conf.roundIntervalSec = 3
		# case_conf.continueWhenFailed = False
		# case_conf.paramStrs.extend([
		# 	json.dumps({
		# 		'stockId': '204001.sh',
		# 		'src': 'd',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '131809.sz',
		# 		'src': 'd',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '204091.sh',
		# 		'src': 'd',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '131801.sz',
		# 		'src': 'd',
		# 	}), 
		# 		json.dumps({
		# 		'stockId': '124176.sh',
		# 		'src': 'd',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '118515.sz',
		# 		'src': 'd',
		# 	}), 
		# ])
		# case_list.append(case_conf)
		# #付息情况
		# case_conf = TestcaseConfig()
		# case_conf.testcaseID = 'F10_BNDINTERESTPAY_1'
		# case_conf.roundIntervalSec = 3
		# case_conf.continueWhenFailed = False
		# case_conf.paramStrs.extend([
		# 			json.dumps({
		# 		'stockId': '204001.sh',
		# 		'src': 'd',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '131809.sz',
		# 		'src': 'd',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '204091.sh',
		# 		'src': 'd',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '131801.sz',
		# 		'src': 'd',
		# 	}), 
		# 		json.dumps({
		# 		'stockId': '124176.sh',
		# 		'src': 'd',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '118515.sz',
		# 		'src': 'd',
		# 	}), 
		# ])
		# case_list.append(case_conf)
		# #债券回购
		# case_conf = TestcaseConfig()
		# case_conf.testcaseID = 'F10_BNDBUYBACKS_1'
		# case_conf.roundIntervalSec = 3
		# case_conf.continueWhenFailed = False
		# case_conf.paramStrs.extend([
		# 		json.dumps({
		# 		'stockId': '136295.sh',
		# 		'src': 'd',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '113526.sh',
		# 		'src': 'd',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '136670.sh',
		# 		'src': 'd',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '113523.sh',
		# 		'src': 'd',
		# 	}), 
		# 		json.dumps({
		# 		'stockId': '124176.sh',
		# 		'src': 'd',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '112575.sz',
		# 		'src': 'd',
		# 	}), 
		# 		json.dumps({
		# 		'stockId': '128048.sz',
		# 		'src': 'd',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '128072.sz',
		# 		'src': 'd',
		# 	}), 
		# 		json.dumps({
		# 		'stockId': '123009.sz',
		# 		'src': 'd',
		# 	}),
		# 	json.dumps({
		# 		'stockId': '128044.sz',
		# 		'src': 'd',
		# 	}), 
		# ])
		# case_list.append(case_conf)
		#分级基金
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_STRUCTUREDFUND_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'requestType': '/fndclassinfo',
				'stockId': '502056.sh',
				'src': 'd',
			}),
			json.dumps({
				'requestType': '/fndclassinfo',
				'stockId': '150174.sz',
				'src': 'd',
			}),
			json.dumps({
				'requestType': '/fndclassforcast',
				'stockId': '502054.sh',
				'src': 'd',
			}),
			json.dumps({
				'requestType': '/fndclassforcast',
				'stockId': '150195.sz',
				'src': 'd',
			}),
			json.dumps({
				'requestType': '/fndclassconverted',
				'stockId': '502058.sh',
				'src': 'd',
			}),
			json.dumps({
				'requestType': '/fndclassconverted',
				'stockId': '150323.sz',
				'src': 'd',
			}),
		])
		case_list.append(case_conf)
		#大宗交易
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_BLOCKTRADE_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'send': '601633.sh',
				'src': 'd',
			}),
			json.dumps({
				'send': '002761.sz',
				'src': 'd',
			}),
			json.dumps({
				'send': '832028.bj',
				'src': 'd',
			}),
		])
		case_list.append(case_conf)
		#沪深---融资融券--分市场提供最近交易日
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_FINANCEMRGNIN_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			#SH
			json.dumps({
				'code': 'TRADEDATE_sh_0',
				'src': 'd',
				'param': '1,10',
				'part': 'TRADEDATE,TRADING,FINBALANCE,FINBUYAMT,FINREPAYAMT,FINROEBUY,MRGGBAL,MRGNRESQTY,MRGNSELLAMT,MRGNREPAYAMT,'
			}),
			json.dumps({
				'code': 'TRADING_sh_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'FINBALANCE_sh_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'FINBUYAMT_sh_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'FINREPAYAMT_sh_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'FINROEBUY_sh_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'MRGGBAL_sh_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'MRGNRESQTY_sh_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),json.dumps({
				'code': 'MRGNSELLAMT_sh_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'MRGNREPAYAMT_sh_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),json.dumps({
				'code': 'MRGNROESELL_sh_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'FINMRGHBAL_sh_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),json.dumps({
				'code': 'FINMRGNBAL_sh_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),	
			json.dumps({
				'code': 'TRADEDATE_sh_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'TRADING_sh_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'FINBALANCE_sh_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'FINBUYAMT_sh_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'FINREPAYAMT_sh_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'FINROEBUY_sh_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'MRGGBAL_sh_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'MRGNRESQTY_sh_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),json.dumps({
				'code': 'MRGNSELLAMT_sh_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'MRGNREPAYAMT_sh_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),json.dumps({
				'code': 'MRGNROESELL_sh_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'FINMRGHBAL_sh_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),json.dumps({
				'code': 'FINMRGNBAL_sh_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),	
			#sz
			json.dumps({
				'code': 'TRADEDATE_sz_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'TRADING_sz_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'FINBALANCE_sz_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'FINBUYAMT_sz_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'FINREPAYAMT_sz_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'FINROEBUY_sz_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'MRGGBAL_sz_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'MRGNRESQTY_sz_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),json.dumps({
				'code': 'MRGNSELLAMT_sz_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'MRGNREPAYAMT_sz_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),json.dumps({
				'code': 'MRGNROESELL_sz_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'FINMRGHBAL_sz_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),json.dumps({
				'code': 'FINMRGNBAL_sz_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),	
			json.dumps({
				'code': 'TRADEDATE_sz_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'TRADING_sz_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'FINBALANCE_sz_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'FINBUYAMT_sz_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'FINREPAYAMT_sz_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'FINROEBUY_sz_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'MRGGBAL_sz_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'MRGNRESQTY_sz_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),json.dumps({
				'code': 'MRGNSELLAMT_sz_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'MRGNREPAYAMT_sz_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),json.dumps({
				'code': 'MRGNROESELL_sz_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'FINMRGHBAL_sz_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),json.dumps({
				'code': 'FINMRGNBAL_sz_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			#sh_sz
			json.dumps({
				'code': 'TRADEDATE_sh_sz_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'TRADING_sh_sz_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'FINBALANCE_sh_sz_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'FINBUYAMT_sh_sz_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'FINREPAYAMT_sh_sz_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'FINROEBUY_sh_sz_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'MRGGBAL_sh_sz_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'MRGNRESQTY_sh_sz_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),json.dumps({
				'code': 'MRGNSELLAMT_sh_sz_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'MRGNREPAYAMT_sh_sz_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),json.dumps({
				'code': 'MRGNROESELL_sh_sz_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'FINMRGHBAL_sh_sz_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),json.dumps({
				'code': 'FINMRGNBAL_sh_sz_0',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),	
			json.dumps({
				'code': 'TRADEDATE_sh_sz_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'TRADING_sh_sz_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'FINBALANCE_sh_sz_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'FINBUYAMT_sh_sz_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'FINREPAYAMT_sh_sz_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'FINROEBUY_sh_sz_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'MRGGBAL_sh_sz_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'MRGNRESQTY_sh_sz_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),json.dumps({
				'code': 'MRGNSELLAMT_sh_sz_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'MRGNREPAYAMT_sh_sz_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),json.dumps({
				'code': 'MRGNROESELL_sh_sz_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'FINMRGHBAL_sh_sz_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),json.dumps({
				'code': 'FINMRGNBAL_sh_sz_1',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
		])
		case_list.append(case_conf)
		#沪深股api----融资融券--融资融券差额接口(最近90天)
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_FINANCEMRGNIN_2'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'code': 'sh',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'sz',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': 'sh_sz',
				'src': 'd',
				'param': '1,20',
				'part': 'null'
			}),
		])
		case_list.append(case_conf)
		#:沪深股api----融资融券--个股融资融券接口（最近90天）
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_FINANCEMRGNIN_3'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'code': '600037.sh',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': '688021.sh',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': '515300.sh',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': '000665.sz',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': '159920.sz',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),
			json.dumps({
				'code': '300009.sz',
				'src': 'd',
				'param': '1,10',
				'part': 'null'
			}),	
		])	
		case_list.append(case_conf)
		#新债日历
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_BONDTRADINGDAY_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'src': 'd',
			}),
		])
		case_list.append(case_conf)
		#当日新债
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_BNDNEWSHARESCAL_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'date': '2019-12-12', 
				'src': 'd',
			}),
				json.dumps({
				'date': '2019-12-13', 
				'src': 'd',
			}),		
		])
		case_list.append(case_conf)
		
		#当日新股列表
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10_NEWSHARELIST_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			json.dumps({
				'date': '2019-12-12',
				'src': 'd',
			}),
			json.dumps({
				'date': '2019-12-13',
				'src': 'd',
			}),
		])
		case_list.append(case_conf)

		#財汇沪深盘后接口1
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10V2TEST_1'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			#重要指标
			json.dumps({
				'code': '601633.sh',
				'src': 'd',
				'apiType': '/importantindex',
			}),
			json.dumps({
				'code': '002761.sz',
				'src': 'd',
				'apiType': '/importantindex',
			}),
			json.dumps({
				'code': '900934.sh',
				'src': 'd',
				'apiType': '/importantindex',
			}),
			json.dumps({
				'code': '200055.sz',
				'src': 'd',
				'apiType': '/importantindex',
			}),
			json.dumps({
				'code': '502005.sh',
				'src': 'd',
				'apiType': '/importantindex',
			}),
			json.dumps({
				'code': '159951.sz',
				'src': 'd',
				'apiType': '/importantindex',
			}),
			json.dumps({
				'code': '113548.sh',
				'src': 'd',
				'apiType': '/importantindex',
			}),
			json.dumps({
				'code': '128061.sz',
				'src': 'd',
				'apiType': '/importantindex',
			}),
			json.dumps({
				'code': '113551.sh',
				'src': 'd',
				'apiType': '/importantindex',
			}),
			json.dumps({
				'code': '131809.sz',
				'src': 'd',
				'apiType': '/importantindex',
			}),
			json.dumps({
				'code': '832028.bj',
				'src': 'd',
				'apiType': '/importantindex',
			}),
			#主营构成
			json.dumps({
				'code': '601633.sh',
				'src': 'd',
				'apiType': '/businessinfo',
			}),
			json.dumps({
				'code': '002761.sz',
				'src': 'd',
				'apiType': '/businessinfo',
			}),
			json.dumps({
				'code': '900934.sh',
				'src': 'd',
				'apiType': '/businessinfo',
			}),
			json.dumps({
				'code': '200055.sz',
				'src': 'd',
				'apiType': '/businessinfo',
			}),
			json.dumps({
				'code': '502005.sh',
				'src': 'd',
				'apiType': '/businessinfo',
			}),
			json.dumps({
				'code': '159951.sz',
				'src': 'd',
				'apiType': '/businessinfo',
			}),
			json.dumps({
				'code': '113548.sh',
				'src': 'd',
				'apiType': '/businessinfo',
			}),
			json.dumps({
				'code': '128061.sz',
				'src': 'd',
				'apiType': '/businessinfo',
			}),
			json.dumps({
				'code': '113551.sh',
				'src': 'd',
				'apiType': '/businessinfo',
			}),
			json.dumps({
				'code': '131809.sz',
				'src': 'd',
				'apiType': '/businessinfo',
			}),
			json.dumps({
				'code': '832028.bj',
				'src': 'd',
				'apiType': '/businessinfo',
			}),
			#龙虎榜-买入前5营业部
			json.dumps({
				'code': '601633.sh',
				'src': 'd',
				'apiType': '/charts5buys',
			}),
			json.dumps({
				'code': '002761.sz',
				'src': 'd',
				'apiType': '/charts5buys',
			}),
			json.dumps({
				'code': '900934.sh',
				'src': 'd',
				'apiType': '/charts5buys',
			}),
			json.dumps({
				'code': '200055.sz',
				'src': 'd',
				'apiType': '/charts5buys',
			}),
			json.dumps({
				'code': '502005.sh',
				'src': 'd',
				'apiType': '/charts5buys',
			}),
			json.dumps({
				'code': '159951.sz',
				'src': 'd',
				'apiType': '/charts5buys',
			}),
			json.dumps({
				'code': '113548.sh',
				'src': 'd',
				'apiType': '/charts5buys',
			}),
			json.dumps({
				'code': '128061.sz',
				'src': 'd',
				'apiType': '/charts5buys',
			}),
			json.dumps({
				'code': '113551.sh',
				'src': 'd',
				'apiType': '/charts5buys',
			}),
			json.dumps({
				'code': '131809.sz',
				'src': 'd',
				'apiType': '/charts5buys',
			}),
			json.dumps({
				'code': '832028.bj',
				'src': 'd',
				'apiType': '/charts5buys',
			}),
			#龙虎榜-卖出前5营业部
			json.dumps({
				'code': '601633.sh',
				'src': 'd',
				'apiType': '/charts5sells',
			}),
			json.dumps({
				'code': '002761.sz',
				'src': 'd',
				'apiType': '/charts5sells',
			}),
			json.dumps({
				'code': '900934.sh',
				'src': 'd',
				'apiType': '/charts5sells',
			}),
			json.dumps({
				'code': '200055.sz',
				'src': 'd',
				'apiType': '/charts5sells',
			}),
			json.dumps({
				'code': '502005.sh',
				'src': 'd',
				'apiType': '/charts5sells',
			}),
			json.dumps({
				'code': '159951.sz',
				'src': 'd',
				'apiType': '/charts5sells',
			}),
			json.dumps({
				'code': '113548.sh',
				'src': 'd',
				'apiType': '/charts5sells',
			}),
			json.dumps({
				'code': '128061.sz',
				'src': 'd',
				'apiType': '/charts5sells',
			}),
			json.dumps({
				'code': '113551.sh',
				'src': 'd',
				'apiType': '/charts5sells',
			}),
			json.dumps({
				'code': '131809.sz',
				'src': 'd',
				'apiType': '/charts5sells',
			}),
			json.dumps({
				'code': '832028.bj',
				'src': 'd',
				'apiType': '/charts5sells',
			}),
			#沪深api---机构观点-机构评级
			json.dumps({
				'code': '601633.sh',
				'src': 'd',
				'apiType': '/exptskinvrating',
			}),
			json.dumps({
				'code': '002761.sz',
				'src': 'd',
				'apiType': '/exptskinvrating',
			}),
			json.dumps({
				'code': '900934.sh',
				'src': 'd',
				'apiType': '/exptskinvrating',
			}),
			json.dumps({
				'code': '200055.sz',
				'src': 'd',
				'apiType': '/exptskinvrating',
			}),
			json.dumps({
				'code': '502005.sh',
				'src': 'd',
				'apiType': '/exptskinvrating',
			}),
			json.dumps({
				'code': '159951.sz',
				'src': 'd',
				'apiType': '/exptskinvrating',
			}),
			json.dumps({
				'code': '113548.sh',
				'src': 'd',
				'apiType': '/exptskinvrating',
			}),
			json.dumps({
				'code': '128061.sz',
				'src': 'd',
				'apiType': '/exptskinvrating',
			}),
			json.dumps({
				'code': '113551.sh',
				'src': 'd',
				'apiType': '/exptskinvrating',
			}),
			json.dumps({
				'code': '131809.sz',
				'src': 'd',
				'apiType': '/exptskinvrating',
			}),
			json.dumps({
				'code': '832028.bj',
				'src': 'd',
				'apiType': '/exptskinvrating',
			}),
			#机构观点-一致预测
			json.dumps({
				'code': '601633.sh',
				'src': 'd',
				'apiType': '/exptskstatn',
			}),
			json.dumps({
				'code': '002761.sz',
				'src': 'd',
				'apiType': '/exptskstatn',
			}),
			json.dumps({
				'code': '900934.sh',
				'src': 'd',
				'apiType': '/exptskstatn',
			}),
			json.dumps({
				'code': '200055.sz',
				'src': 'd',
				'apiType': '/exptskstatn',
			}),
			json.dumps({
				'code': '502005.sh',
				'src': 'd',
				'apiType': '/exptskstatn',
			}),
			json.dumps({
				'code': '159951.sz',
				'src': 'd',
				'apiType': '/exptskstatn',
			}),
			json.dumps({
				'code': '113548.sh',
				'src': 'd',
				'apiType': '/exptskstatn',
			}),
			json.dumps({
				'code': '128061.sz',
				'src': 'd',
				'apiType': '/exptskstatn',
			}),
			json.dumps({
				'code': '113551.sh',
				'src': 'd',
				'apiType': '/exptskstatn',
			}),
			json.dumps({
				'code': '131809.sz',
				'src': 'd',
				'apiType': '/exptskstatn',
			}),
			json.dumps({
				'code': '832028.bj',
				'src': 'd',
				'apiType': '/exptskstatn',
			}),
			#公司简介
			json.dumps({
				'code': '601633.sh',
				'src': 'd',
				'apiType': '/companyinfo',
			}),
			json.dumps({
				'code': '002761.sz',
				'src': 'd',
				'apiType': '/companyinfo',
			}),
			json.dumps({
				'code': '900934.sh',
				'src': 'd',
				'apiType': '/companyinfo',
			}),
			json.dumps({
				'code': '200055.sz',
				'src': 'd',
				'apiType': '/companyinfo',
			}),
			json.dumps({
				'code': '502005.sh',
				'src': 'd',
				'apiType': '/companyinfo',
			}),
			json.dumps({
				'code': '159951.sz',
				'src': 'd',
				'apiType': '/companyinfo',
			}),
			json.dumps({
				'code': '113548.sh',
				'src': 'd',
				'apiType': '/companyinfo',
			}),
			json.dumps({
				'code': '128061.sz',
				'src': 'd',
				'apiType': '/companyinfo',
			}),
			json.dumps({
				'code': '113551.sh',
				'src': 'd',
				'apiType': '/companyinfo',
			}),
			json.dumps({
				'code': '131809.sz',
				'src': 'd',
				'apiType': '/companyinfo',
			}),
			json.dumps({
				'code': '832028.bj',
				'src': 'd',
				'apiType': '/companyinfo',
			}),
			#分红扩股
			json.dumps({
				'code': '601633.sh',
				'src': 'd',
				'apiType': '/sharebonus',
			}),
			json.dumps({
				'code': '002761.sz',
				'src': 'd',
				'apiType': '/sharebonus',
			}),
			json.dumps({
				'code': '900934.sh',
				'src': 'd',
				'apiType': '/sharebonus',
			}),
			json.dumps({
				'code': '200055.sz',
				'src': 'd',
				'apiType': '/sharebonus',
			}),
			json.dumps({
				'code': '502005.sh',
				'src': 'd',
				'apiType': '/sharebonus',
			}),
			json.dumps({
				'code': '159951.sz',
				'src': 'd',
				'apiType': '/sharebonus',
			}),
			json.dumps({
				'code': '113548.sh',
				'src': 'd',
				'apiType': '/sharebonus',
			}),
			json.dumps({
				'code': '128061.sz',
				'src': 'd',
				'apiType': '/sharebonus',
			}),
			json.dumps({
				'code': '113551.sh',
				'src': 'd',
				'apiType': '/sharebonus',
			}),
			json.dumps({
				'code': '131809.sz',
				'src': 'd',
				'apiType': '/sharebonus',
			}),
			json.dumps({
				'code': '832028.bj',
				'src': 'd',
				'apiType': '/sharebonus',
			}),
			#公司高管
			json.dumps({
				'code': '601633.sh',
				'src': 'd',
				'apiType': '/companymanager',
			}),
			json.dumps({
				'code': '002761.sz',
				'src': 'd',
				'apiType': '/companymanager',
			}),
			json.dumps({
				'code': '900934.sh',
				'src': 'd',
				'apiType': '/companymanager',
			}),
			json.dumps({
				'code': '200055.sz',
				'src': 'd',
				'apiType': '/companymanager',
			}),
			json.dumps({
				'code': '502005.sh',
				'src': 'd',
				'apiType': '/companymanager',
			}),
			json.dumps({
				'code': '159951.sz',
				'src': 'd',
				'apiType': '/companymanager',
			}),
			json.dumps({
				'code': '113548.sh',
				'src': 'd',
				'apiType': '/companymanager',
			}),
			json.dumps({
				'code': '128061.sz',
				'src': 'd',
				'apiType': '/companymanager',
			}),
			json.dumps({
				'code': '113551.sh',
				'src': 'd',
				'apiType': '/companymanager',
			}),
			json.dumps({
				'code': '131809.sz',
				'src': 'd',
				'apiType': '/companymanager',
			}),
			json.dumps({
				'code': '832028.bj',
				'src': 'd',
				'apiType': '/companymanager',
			}),
			#十大流通股东
			json.dumps({
				'code': '601633.sh',
				'src': 'd',
				'apiType': '/otsholder10',
			}),
			json.dumps({
				'code': '002761.sz',
				'src': 'd',
				'apiType': '/otsholder10',
			}),
			json.dumps({
				'code': '900934.sh',
				'src': 'd',
				'apiType': '/otsholder10',
			}),
			json.dumps({
				'code': '200055.sz',
				'src': 'd',
				'apiType': '/otsholder10',
			}),
			json.dumps({
				'code': '502005.sh',
				'src': 'd',
				'apiType': '/otsholder10',
			}),
			json.dumps({
				'code': '159951.sz',
				'src': 'd',
				'apiType': '/otsholder10',
			}),
			json.dumps({
				'code': '113548.sh',
				'src': 'd',
				'apiType': '/otsholder10',
			}),
			json.dumps({
				'code': '128061.sz',
				'src': 'd',
				'apiType': '/otsholder10',
			}),
			json.dumps({
				'code': '113551.sh',
				'src': 'd',
				'apiType': '/otsholder10',
			}),
			json.dumps({
				'code': '131809.sz',
				'src': 'd',
				'apiType': '/otsholder10',
			}),
			json.dumps({
				'code': '832028.bj',
				'src': 'd',
				'apiType': '/otsholder10',
			}),
			#十大股东
			json.dumps({
				'code': '601633.sh',
				'src': 'd',
				'apiType': '/shareholder10',
			}),
			json.dumps({
				'code': '002761.sz',
				'src': 'd',
				'apiType': '/shareholder10',
			}),
			json.dumps({
				'code': '900934.sh',
				'src': 'd',
				'apiType': '/shareholder10',
			}),
			json.dumps({
				'code': '200055.sz',
				'src': 'd',
				'apiType': '/shareholder10',
			}),
			json.dumps({
				'code': '502005.sh',
				'src': 'd',
				'apiType': '/shareholder10',
			}),
			json.dumps({
				'code': '159951.sz',
				'src': 'd',
				'apiType': '/shareholder10',
			}),
			json.dumps({
				'code': '113548.sh',
				'src': 'd',
				'apiType': '/shareholder10',
			}),
			json.dumps({
				'code': '128061.sz',
				'src': 'd',
				'apiType': '/shareholder10',
			}),
			json.dumps({
				'code': '113551.sh',
				'src': 'd',
				'apiType': '/shareholder10',
			}),
			json.dumps({
				'code': '131809.sz',
				'src': 'd',
				'apiType': '/shareholder10',
			}),
			json.dumps({
				'code': '832028.bj',
				'src': 'd',
				'apiType': '/shareholder10',
			}),
			#股本信息
			json.dumps({
				'code': '601633.sh',
				'src': 'd',
				'apiType': '/shareinfo',
			}),
			json.dumps({
				'code': '002761.sz',
				'src': 'd',
				'apiType': '/shareinfo',
			}),
			json.dumps({
				'code': '900934.sh',
				'src': 'd',
				'apiType': '/shareinfo',
			}),
			json.dumps({
				'code': '200055.sz',
				'src': 'd',
				'apiType': '/shareinfo',
			}),
			json.dumps({
				'code': '502005.sh',
				'src': 'd',
				'apiType': '/shareinfo',
			}),
			json.dumps({
				'code': '159951.sz',
				'src': 'd',
				'apiType': '/shareinfo',
			}),
			json.dumps({
				'code': '113548.sh',
				'src': 'd',
				'apiType': '/shareinfo',
			}),
			json.dumps({
				'code': '128061.sz',
				'src': 'd',
				'apiType': '/shareinfo',
			}),
			json.dumps({
				'code': '113551.sh',
				'src': 'd',
				'apiType': '/shareinfo',
			}),
			json.dumps({
				'code': '131809.sz',
				'src': 'd',
				'apiType': '/shareinfo',
			}),
			json.dumps({
				'code': '832028.bj',
				'src': 'd',
				'apiType': '/shareinfo',
			}),
			#股东户数
			json.dumps({
				'code': '601633.sh',
				'src': 'd',
				'apiType': '/shareholdernum',
			}),
			json.dumps({
				'code': '002761.sz',
				'src': 'd',
				'apiType': '/shareholdernum',
			}),
			json.dumps({
				'code': '900934.sh',
				'src': 'd',
				'apiType': '/shareholdernum',
			}),
			json.dumps({
				'code': '200055.sz',
				'src': 'd',
				'apiType': '/shareholdernum',
			}),
			json.dumps({
				'code': '502005.sh',
				'src': 'd',
				'apiType': '/shareholdernum',
			}),
			json.dumps({
				'code': '159951.sz',
				'src': 'd',
				'apiType': '/shareholdernum',
			}),
			json.dumps({
				'code': '113548.sh',
				'src': 'd',
				'apiType': '/shareholdernum',
			}),
			json.dumps({
				'code': '128061.sz',
				'src': 'd',
				'apiType': '/shareholdernum',
			}),
			json.dumps({
				'code': '113551.sh',
				'src': 'd',
				'apiType': '/shareholdernum',
			}),
			json.dumps({
				'code': '131809.sz',
				'src': 'd',
				'apiType': '/shareholdernum',
			}),
			json.dumps({
				'code': '832028.bj',
				'src': 'd',
				'apiType': '/shareholdernum',
			}),
			#主要指标
			json.dumps({
				'code': '601633.sh',
				'src': 'd',
				'apiType': '/profinmainindex',
			}),
			json.dumps({
				'code': '002761.sz',
				'src': 'd',
				'apiType': '/profinmainindex',
			}),
			json.dumps({
				'code': '900934.sh',
				'src': 'd',
				'apiType': '/profinmainindex',
			}),
			json.dumps({
				'code': '200055.sz',
				'src': 'd',
				'apiType': '/profinmainindex',
			}),
			json.dumps({
				'code': '502005.sh',
				'src': 'd',
				'apiType': '/profinmainindex',
			}),
			json.dumps({
				'code': '159951.sz',
				'src': 'd',
				'apiType': '/profinmainindex',
			}),
			json.dumps({
				'code': '113548.sh',
				'src': 'd',
				'apiType': '/profinmainindex',
			}),
			json.dumps({
				'code': '128061.sz',
				'src': 'd',
				'apiType': '/profinmainindex',
			}),
			json.dumps({
				'code': '113551.sh',
				'src': 'd',
				'apiType': '/profinmainindex',
			}),
			json.dumps({
				'code': '131809.sz',
				'src': 'd',
				'apiType': '/profinmainindex',
			}),
			json.dumps({
				'code': '832028.bj',
				'src': 'd',
				'apiType': '/profinmainindex',
			}),
			#利润表
			json.dumps({
				'code': '601633.sh',
				'src': 'd',
				'apiType': '/proincstatementnew',
			}),
			json.dumps({
				'code': '002761.sz',
				'src': 'd',
				'apiType': '/proincstatementnew',
			}),
			json.dumps({
				'code': '900934.sh',
				'src': 'd',
				'apiType': '/proincstatementnew',
			}),
			json.dumps({
				'code': '200055.sz',
				'src': 'd',
				'apiType': '/proincstatementnew',
			}),
			json.dumps({
				'code': '502005.sh',
				'src': 'd',
				'apiType': '/proincstatementnew',
			}),
			json.dumps({
				'code': '159951.sz',
				'src': 'd',
				'apiType': '/proincstatementnew',
			}),
			json.dumps({
				'code': '113548.sh',
				'src': 'd',
				'apiType': '/proincstatementnew',
			}),
			json.dumps({
				'code': '128061.sz',
				'src': 'd',
				'apiType': '/proincstatementnew',
			}),
			json.dumps({
				'code': '113551.sh',
				'src': 'd',
				'apiType': '/proincstatementnew',
			}),
			json.dumps({
				'code': '131809.sz',
				'src': 'd',
				'apiType': '/proincstatementnew',
			}),
			json.dumps({
				'code': '832028.bj',
				'src': 'd',
				'apiType': '/proincstatementnew',
			}),
			#资产负债表
			json.dumps({
				'code': '601633.sh',
				'src': 'd',
				'apiType': '/probalsheetnew',
			}),
			json.dumps({
				'code': '002761.sz',
				'src': 'd',
				'apiType': '/probalsheetnew',
			}),
			json.dumps({
				'code': '900934.sh',
				'src': 'd',
				'apiType': '/probalsheetnew',
			}),
			json.dumps({
				'code': '200055.sz',
				'src': 'd',
				'apiType': '/probalsheetnew',
			}),
			json.dumps({
				'code': '502005.sh',
				'src': 'd',
				'apiType': '/probalsheetnew',
			}),
			json.dumps({
				'code': '159951.sz',
				'src': 'd',
				'apiType': '/probalsheetnew',
			}),
			json.dumps({
				'code': '113548.sh',
				'src': 'd',
				'apiType': '/probalsheetnew',
			}),
			json.dumps({
				'code': '128061.sz',
				'src': 'd',
				'apiType': '/probalsheetnew',
			}),
			json.dumps({
				'code': '113551.sh',
				'src': 'd',
				'apiType': '/probalsheetnew',
			}),
			json.dumps({
				'code': '131809.sz',
				'src': 'd',
				'apiType': '/probalsheetnew',
			}),
			json.dumps({
				'code': '832028.bj',
				'src': 'd',
				'apiType': '/probalsheetnew',
			}),
			#现金流量表
			json.dumps({
				'code': '601633.sh',
				'src': 'd',
				'apiType': '/procfstatementnew',
			}),
			json.dumps({
				'code': '002761.sz',
				'src': 'd',
				'apiType': '/procfstatementnew',
			}),
			json.dumps({
				'code': '900934.sh',
				'src': 'd',
				'apiType': '/procfstatementnew',
			}),
			json.dumps({
				'code': '200055.sz',
				'src': 'd',
				'apiType': '/procfstatementnew',
			}),
			json.dumps({
				'code': '502005.sh',
				'src': 'd',
				'apiType': '/procfstatementnew',
			}),
			json.dumps({
				'code': '159951.sz',
				'src': 'd',
				'apiType': '/procfstatementnew',
			}),
			json.dumps({
				'code': '113548.sh',
				'src': 'd',
				'apiType': '/procfstatementnew',
			}),
			json.dumps({
				'code': '128061.sz',
				'src': 'd',
				'apiType': '/procfstatementnew',
			}),
			json.dumps({
				'code': '113551.sh',
				'src': 'd',
				'apiType': '/procfstatementnew',
			}),
			json.dumps({
				'code': '131809.sz',
				'src': 'd',
				'apiType': '/procfstatementnew',
			}),
			json.dumps({
				'code': '832028.bj',
				'src': 'd',
				'apiType': '/procfstatementnew',
			}),
			#股东深度挖掘数据
			json.dumps({
				'code': '80007241',
				'src': 'd',
				'apiType': '/iinvholdchg',
			}),
			json.dumps({
				'code': '80008357',
				'src': 'd',
				'apiType': '/iinvholdchg',
			}),
			json.dumps({
				'code': '80043020',
				'src': 'd',
				'apiType': '/iinvholdchg',
			}),
			json.dumps({
				'code': '76125492',
				'src': 'd',
				'apiType': '/iinvholdchg',
			}),
			json.dumps({
				'code': '80525226',
				'src': 'd',
				'apiType': '/iinvholdchg',
			}),
			json.dumps({
				'code': '80188285',
				'src': 'd',
				'apiType': '/iinvholdchg',
			}),
			json.dumps({
				'code': '76124290',
				'src': 'd',
				'apiType': '/iinvholdchg',
			}),
			json.dumps({
				'code': '80563694',
				'src': 'd',
				'apiType': '/iinvholdchg',
			}),
			json.dumps({
				'code': '70304145',
				'src': 'd',
				'apiType': '/iinvholdchg',
			}),
			json.dumps({
				'code': '80553146',
				'src': 'd',
				'apiType': '/iinvholdchg',
			}),
			json.dumps({
				'code': '82177701',
				'src': 'd',
				'apiType': '/iinvholdchg',
			}),
			#沪深股api----大事提醒---按时间
			json.dumps({
				'code': '601633.sh',
				'src': 'd',
				'apiType': '/importnoticedate',
			}),
			json.dumps({
				'code': '002761.sz',
				'src': 'd',
				'apiType': '/importnoticedate',
			}),
			json.dumps({
				'code': '900934.sh',
				'src': 'd',
				'apiType': '/importnoticedate',
			}),
			json.dumps({
				'code': '200055.sz',
				'src': 'd',
				'apiType': '/importnoticedate',
			}),
			json.dumps({
				'code': '502005.sh',
				'src': 'd',
				'apiType': '/importnoticedate',
			}),
			json.dumps({
				'code': '159951.sz',
				'src': 'd',
				'apiType': '/importnoticedate',
			}),
			json.dumps({
				'code': '113548.sh',
				'src': 'd',
				'apiType': '/importnoticedate',
			}),
			json.dumps({
				'code': '128061.sz',
				'src': 'd',
				'apiType': '/importnoticedate',
			}),
			json.dumps({
				'code': '113551.sh',
				'src': 'd',
				'apiType': '/importnoticedate',
			}),
			json.dumps({
				'code': '131809.sz',
				'src': 'd',
				'apiType': '/importnoticedate',
			}),
			json.dumps({
				'code': '832028.bj',
				'src': 'd',
				'apiType': '/importnoticedate',
			}),
			#沪深股api----大事提醒---按标题
			json.dumps({
				'code': '601633.sh',
				'src': 'd',
				'apiType': '/importnoticetitle',
			}),
			json.dumps({
				'code': '002761.sz',
				'src': 'd',
				'apiType': '/importnoticetitle',
			}),
			json.dumps({
				'code': '900934.sh',
				'src': 'd',
				'apiType': '/importnoticetitle',
			}),
			json.dumps({
				'code': '200055.sz',
				'src': 'd',
				'apiType': '/importnoticetitle',
			}),
			json.dumps({
				'code': '502005.sh',
				'src': 'd',
				'apiType': '/importnoticetitle',
			}),
			json.dumps({
				'code': '159951.sz',
				'src': 'd',
				'apiType': '/importnoticetitle',
			}),
			json.dumps({
				'code': '113548.sh',
				'src': 'd',
				'apiType': '/importnoticetitle',
			}),
			json.dumps({
				'code': '128061.sz',
				'src': 'd',
				'apiType': '/importnoticetitle',
			}),
			json.dumps({
				'code': '113551.sh',
				'src': 'd',
				'apiType': '/importnoticetitle',
			}),
			json.dumps({
				'code': '131809.sz',
				'src': 'd',
				'apiType': '/importnoticetitle',
			}),
			json.dumps({
				'code': '832028.bj',
				'src': 'd',
				'apiType': '/importnoticetitle',
			}),
			#董秘问答
			json.dumps({
				'code': '601633.sh',
				'src': 'd',
				'apiType': '/newsinteractive',
			}),
			json.dumps({
				'code': '002761.sz',
				'src': 'd',
				'apiType': '/newsinteractive',
			}),
			json.dumps({
				'code': '900934.sh',
				'src': 'd',
				'apiType': '/newsinteractive',
			}),
			json.dumps({
				'code': '200055.sz',
				'src': 'd',
				'apiType': '/newsinteractive',
			}),
			json.dumps({
				'code': '502005.sh',
				'src': 'd',
				'apiType': '/newsinteractive',
			}),
			json.dumps({
				'code': '159951.sz',
				'src': 'd',
				'apiType': '/newsinteractive',
			}),
			json.dumps({
				'code': '113548.sh',
				'src': 'd',
				'apiType': '/newsinteractive',
			}),
			json.dumps({
				'code': '128061.sz',
				'src': 'd',
				'apiType': '/newsinteractive',
			}),
			json.dumps({
				'code': '113551.sh',
				'src': 'd',
				'apiType': '/newsinteractive',
			}),
			json.dumps({
				'code': '131809.sz',
				'src': 'd',
				'apiType': '/newsinteractive',
			}),
			json.dumps({
				'code': '832028.bj',
				'src': 'd',
				'apiType': '/newsinteractive',
			}),
			#大事提醒-业绩预告
			json.dumps({
				'code': '601633.sh',
				'src': 'd',
				'apiType': '/exptperformance',
			}),
			json.dumps({
				'code': '002761.sz',
				'src': 'd',
				'apiType': '/exptperformance',
			}),
			json.dumps({
				'code': '900934.sh',
				'src': 'd',
				'apiType': '/exptperformance',
			}),
			json.dumps({
				'code': '200055.sz',
				'src': 'd',
				'apiType': '/exptperformance',
			}),
			json.dumps({
				'code': '502005.sh',
				'src': 'd',
				'apiType': '/exptperformance',
			}),
			json.dumps({
				'code': '159951.sz',
				'src': 'd',
				'apiType': '/exptperformance',
			}),
			json.dumps({
				'code': '113548.sh',
				'src': 'd',
				'apiType': '/exptperformance',
			}),
			json.dumps({
				'code': '128061.sz',
				'src': 'd',
				'apiType': '/exptperformance',
			}),
			json.dumps({
				'code': '113551.sh',
				'src': 'd',
				'apiType': '/exptperformance',
			}),
			json.dumps({
				'code': '131809.sz',
				'src': 'd',
				'apiType': '/exptperformance',
			}),
			json.dumps({
				'code': '832028.bj',
				'src': 'd',
				'apiType': '/exptperformance',
			}),
			#沪深股api----大事提醒—业绩公告	
			json.dumps({
				'code': '601633.sh',
				'src': 'd',
				'apiType': '/proindicdata',
			}),
			json.dumps({
				'code': '002761.sz',
				'src': 'd',
				'apiType': '/proindicdata',
			}),
			json.dumps({
				'code': '900934.sh',
				'src': 'd',
				'apiType': '/proindicdata',
			}),
			json.dumps({
				'code': '200055.sz',
				'src': 'd',
				'apiType': '/proindicdata',
			}),
			json.dumps({
				'code': '502005.sh',
				'src': 'd',
				'apiType': '/proindicdata',
			}),
			json.dumps({
				'code': '159951.sz',
				'src': 'd',
				'apiType': '/proindicdata',
			}),
			json.dumps({
				'code': '113548.sh',
				'src': 'd',
				'apiType': '/proindicdata',
			}),
			json.dumps({
				'code': '128061.sz',
				'src': 'd',
				'apiType': '/proindicdata',
			}),
			json.dumps({
				'code': '113551.sh',
				'src': 'd',
				'apiType': '/proindicdata',
			}),
			json.dumps({
				'code': '131809.sz',
				'src': 'd',
				'apiType': '/proindicdata',
			}),
			json.dumps({
				'code': '832028.bj',
				'src': 'd',
				'apiType': '/proindicdata',
			}),
		])
		case_list.append(case_conf)
		#財汇沪深盘后接口2
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10V2TEST_2'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			#沪深股api----大事提醒---按时间
			json.dumps({
				'code': '601633.sh',
				'src': 'd',
				'param':'0,10',
				'apiType': '/importnoticedate',
			}),
			json.dumps({
				'code': '002761.sz',
				'src': 'd',
				'param':'0,10',
				'apiType': '/importnoticedate',
			}),
			json.dumps({
				'code': '900934.sh',
				'src': 'd',
				'param':'0,10',
				'apiType': '/importnoticedate',
			}),
			json.dumps({
				'code': '200055.sz',
				'src': 'd',
				'param':'0,10',
				'apiType': '/importnoticedate',
			}),
			json.dumps({
				'code': '502005.sh',
				'src': 'd',
				'param':'0,10',
				'apiType': '/importnoticedate',
			}),
			json.dumps({
				'code': '159951.sz',
				'src': 'd',
				'param':'0,10',
				'apiType': '/importnoticedate',
			}),
			json.dumps({
				'code': '113548.sh',
				'src': 'd',
				'param':'0,10',
				'apiType': '/importnoticedate',
			}),
			json.dumps({
				'code': '128061.sz',
				'src': 'd',
				'param':'0,10',
				'apiType': '/importnoticedate',
			}),
			json.dumps({
				'code': '113551.sh',
				'src': 'd',
				'param':'0,10',
				'apiType': '/importnoticedate',
			}),
			json.dumps({
				'code': '131809.sz',
				'src': 'd',
				'param':'0,10',
				'apiType': '/importnoticedate',
			}),
			json.dumps({
				'code': '832028.bj',
				'src': 'd',
				'param':'0,10',
				'apiType': '/importnoticedate',
			}),
			#沪深股api----大事提醒---按标题
			json.dumps({
				'code': '601633.sh',
				'src': 'd',
				'param':'0,10',
				'apiType': '/importnoticetitle',
			}),
			json.dumps({
				'code': '002761.sz',
				'src': 'd',
				'param':'0,10',
				'apiType': '/importnoticetitle',
			}),
			json.dumps({
				'code': '900934.sh',
				'src': 'd',
				'param':'0,10',
				'apiType': '/importnoticetitle',
			}),
			json.dumps({
				'code': '200055.sz',
				'src': 'd',
				'param':'0,10',
				'apiType': '/importnoticetitle',
			}),
			json.dumps({
				'code': '502005.sh',
				'src': 'd',
				'param':'0,10',
				'apiType': '/importnoticetitle',
			}),
			json.dumps({
				'code': '159951.sz',
				'src': 'd',
				'param':'0,10',
				'apiType': '/importnoticetitle',
			}),
			json.dumps({
				'code': '113548.sh',
				'src': 'd',
				'param':'0,10',
				'apiType': '/importnoticetitle',
			}),
			json.dumps({
				'code': '128061.sz',
				'src': 'd',
				'param':'0,10',
				'apiType': '/importnoticetitle',
			}),
			json.dumps({
				'code': '113551.sh',
				'src': 'd',
				'param':'0,10',
				'apiType': '/importnoticetitle',
			}),
			json.dumps({
				'code': '131809.sz',
				'src': 'd',
				'param':'0,10',
				'apiType': '/importnoticetitle',
			}),
			json.dumps({
				'code': '832028.bj',
				'src': 'd',
				'param':'0,10',
				'apiType': '/importnoticetitle',
			}),
			#大事提醒-业绩预告
			json.dumps({
				'code': 'null',
				'src': 'd',
				'param':'0,10',
				'apiType': '/exptperformance',
			}),		
		])
		case_list.append(case_conf)
		#財汇沪深盘后接口4
		case_conf = TestcaseConfig()
		case_conf.testcaseID = 'F10V2TEST_4'
		case_conf.roundIntervalSec = 3
		case_conf.continueWhenFailed = False
		case_conf.paramStrs.extend([
			#董秘问答
			json.dumps({
				'code': '600234.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'QUESTIONTIME_1'
			}),
			json.dumps({
				'code': '300810.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'QUESTIONTIME_1'
			}),
			json.dumps({
				'code': '900924.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'QUESTIONTIME_1'
			}),
			json.dumps({
				'code': '200026.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'QUESTIONTIME_1'
			}),json.dumps({
				'code': '512870.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'QUESTIONTIME_1'
			}),
			json.dumps({
				'code': '150151.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'QUESTIONTIME_1'
			}),
			json.dumps({
				'code': '136894.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'QUESTIONTIME_1'
			}),
			json.dumps({
				'code': '106127.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'QUESTIONTIME_1'
			}),
			json.dumps({
				'code': '204091.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'QUESTIONTIME_1'
			}),
			json.dumps({
				'code': '131801.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'QUESTIONTIME_1'
			}),
			json.dumps({
				'code': '830862.bj',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'QUESTIONTIME_1'
			}),
			json.dumps({
				'code': 'null',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'QUESTIONTIME_1'
			}),		
			json.dumps({
				'code': '600234.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'QUESTIONTIME_0'
			}),
			json.dumps({
				'code': '300810.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'QUESTIONTIME_0'
			}),
			json.dumps({
				'code': '900924.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'QUESTIONTIME_0'
			}),
			json.dumps({
				'code': '200026.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'QUESTIONTIME_0'
			}),json.dumps({
				'code': '512870.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'QUESTIONTIME_0'
			}),
			json.dumps({
				'code': '150151.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'QUESTIONTIME_0'
			}),
			json.dumps({
				'code': '136894.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'QUESTIONTIME_0'
			}),
			json.dumps({
				'code': '106127.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'QUESTIONTIME_0'
			}),
			json.dumps({
				'code': '204091.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'QUESTIONTIME_0'
			}),
			json.dumps({
				'code': '131801.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'QUESTIONTIME_0'
			}),
			json.dumps({
				'code': '830862.bj',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'QUESTIONTIME_0'
			}),
			json.dumps({
				'code': 'null',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'QUESTIONTIME_0'
			}),
			json.dumps({
				'code': '600234.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'ANSWERTIME_1'
			}),
			json.dumps({
				'code': '300810.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'ANSWERTIME_1'
			}),
			json.dumps({
				'code': '900924.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'ANSWERTIME_1'
			}),
			json.dumps({
				'code': '200026.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'ANSWERTIME_1'
			}),json.dumps({
				'code': '512870.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'ANSWERTIME_1'
			}),
			json.dumps({
				'code': '150151.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'ANSWERTIME_1'
			}),
			json.dumps({
				'code': '136894.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'ANSWERTIME_1'
			}),
			json.dumps({
				'code': '106127.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'ANSWERTIME_1'
			}),
			json.dumps({
				'code': '204091.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'ANSWERTIME_1'
			}),
			json.dumps({
				'code': '131801.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'ANSWERTIME_1'
			}),
			json.dumps({
				'code': '830862.bj',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'ANSWERTIME_1'
			}),
			json.dumps({
				'code': 'null',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'ANSWERTIME_1'
			}),
			json.dumps({
				'code': '600234.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'ANSWERTIME_0'
			}),
			json.dumps({
				'code': '300810.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'ANSWERTIME_0'
			}),
			json.dumps({
				'code': '900924.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'ANSWERTIME_0'
			}),
			json.dumps({
				'code': '200026.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'ANSWERTIME_0'
			}),json.dumps({
				'code': '512870.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'ANSWERTIME_0'
			}),
			json.dumps({
				'code': '150151.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'ANSWERTIME_0'
			}),
			json.dumps({
				'code': '136894.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'ANSWERTIME_0'
			}),
			json.dumps({
				'code': '106127.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'ANSWERTIME_0'
			}),
			json.dumps({
				'code': '204091.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'ANSWERTIME_0'
			}),
			json.dumps({
				'code': '131801.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'ANSWERTIME_0'
			}),
			json.dumps({
				'code': '830862.bj',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'ANSWERTIME_0'
			}),
			json.dumps({
				'code': 'null',
				'src': 'd',
				'param': '0,10',
				'apiType': '/newsinteractive',
				'part': 'null',
				'type': 'ANSWERTIME_0'
			}),
			#大事提醒-按时间
			json.dumps({
				'code': '600234.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticedate',
				'part': 'null',
				'type': 'null'
			}),
			json.dumps({
				'code': '300810.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticedate',
				'part': 'null',
				'type': 'null'
			}),
			json.dumps({
				'code': '900924.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticedate',
				'part': 'null',
				'type': 'null'
			}),
			json.dumps({
				'code': '200026.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticedate',
				'part': 'null',
				'type': 'null'
			}),json.dumps({
				'code': '512870.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticedate',
				'part': 'null',
				'type': 'null'
			}),
			json.dumps({
				'code': '150151.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticedate',
				'part': 'null',
				'type': 'null'
			}),
			json.dumps({
				'code': '136894.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticedate',
				'part': 'null',
				'type': 'null'
			}),
			json.dumps({
				'code': '106127.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticedate',
				'part': 'null',
				'type': 'null'
			}),
			json.dumps({
				'code': '204091.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticedate',
				'part': 'null',
				'type': 'null'
			}),
			json.dumps({
				'code': '131801.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticedate',
				'part': 'null',
				'type': 'null'
			}),
			json.dumps({
				'code': '830862.bj',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticedate',
				'part': 'null',
				'type': 'null'
			}),
			json.dumps({
				'code': '600234.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticedate',
				'part': 'null',
				'type': 'new'
			}),
			json.dumps({
				'code': '300810.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticedate',
				'part': 'null',
				'type': 'new'
			}),
			json.dumps({
				'code': '900924.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticedate',
				'part': 'null',
				'type': 'new'
			}),
			json.dumps({
				'code': '200026.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticedate',
				'part': 'null',
				'type': 'new'
			}),json.dumps({
				'code': '512870.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticedate',
				'part': 'null',
				'type': 'new'
			}),
			json.dumps({
				'code': '150151.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticedate',
				'part': 'null',
				'type': 'new'
			}),
			json.dumps({
				'code': '136894.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticedate',
				'part': 'null',
				'type': 'new'
			}),
			json.dumps({
				'code': '106127.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticedate',
				'part': 'null',
				'type': 'new'
			}),
			json.dumps({
				'code': '204091.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticedate',
				'part': 'null',
				'type': 'new'
			}),
			json.dumps({
				'code': '131801.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticedate',
				'part': 'null',
				'type': 'new'
			}),
			json.dumps({
				'code': '830862.bj',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticedate',
				'part': 'null',
				'type': 'new'
			}),
			#大事提醒--按标题
			json.dumps({
				'code': '600234.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticetitle',
				'part': 'null',
				'type': 'null'
			}),
			json.dumps({
				'code': '300810.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticetitle',
				'part': 'null',
				'type': 'null'
			}),
			json.dumps({
				'code': '900924.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticetitle',
				'part': 'null',
				'type': 'null'
			}),
			json.dumps({
				'code': '200026.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticetitle',
				'part': 'null',
				'type': 'null'
			}),json.dumps({
				'code': '512870.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticetitle',
				'part': 'null',
				'type': 'null'
			}),
			json.dumps({
				'code': '150151.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticetitle',
				'part': 'null',
				'type': 'null'
			}),
			json.dumps({
				'code': '136894.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticetitle',
				'part': 'null',
				'type': 'null'
			}),
			json.dumps({
				'code': '106127.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticetitle',
				'part': 'null',
				'type': 'null'
			}),
			json.dumps({
				'code': '204091.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticetitle',
				'part': 'null',
				'type': 'null'
			}),
			json.dumps({
				'code': '131801.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticetitle',
				'part': 'null',
				'type': 'null'
			}),
			json.dumps({
				'code': '830862.bj',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticetitle',
				'part': 'null',
				'type': 'null'
			}),
			json.dumps({
				'code': '600234.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticetitle',
				'part': 'null',
				'type': 'new'
			}),
			json.dumps({
				'code': '300810.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticetitle',
				'part': 'null',
				'type': 'new'
			}),
			json.dumps({
				'code': '900924.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticetitle',
				'part': 'null',
				'type': 'new'
			}),
			json.dumps({
				'code': '200026.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticetitle',
				'part': 'null',
				'type': 'new'
			}),json.dumps({
				'code': '512870.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticetitle',
				'part': 'null',
				'type': 'new'
			}),
			json.dumps({
				'code': '150151.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticetitle',
				'part': 'null',
				'type': 'new'
			}),
			json.dumps({
				'code': '136894.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticetitle',
				'part': 'null',
				'type': 'new'
			}),
			json.dumps({
				'code': '106127.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticetitle',
				'part': 'null',
				'type': 'new'
			}),
			json.dumps({
				'code': '204091.sh',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticetitle',
				'part': 'null',
				'type': 'new'
			}),
			json.dumps({
				'code': '131801.sz',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticetitle',
				'part': 'null',
				'type': 'new'
			}),
			json.dumps({
				'code': '830862.bj',
				'src': 'd',
				'param': '0,10',
				'apiType': '/importnoticetitle',
				'part': 'null',
				'type': 'new'
			}),	
		])
		case_list.append(case_conf)
		runner_conf.casesConfig.extend(case_list)
		print('i,case_list.length is ',case_list.__len__())
		runner_conf_list.append(runner_conf)

	return runner_conf_list

with DAG(
		dag_id='android_test_F10_3.2',
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
		tag_id='release-20191212-0.0.3',
		tag_sha='5a363eca5ababbb839b43856596ef978964e5513',
		runner_conf=runner_conf_list[0]
	)

	android_a = AndroidRunnerOperator(
		task_id=task_id_to_cmp_list[0],
		provide_context=False,
		apk_id='com.chi.ssetest',
		apk_version='release-20191212-0.0.3',
		runner_conf=runner_conf_list[0]
	)

	android_b = AndroidRunnerOperator(
		task_id=task_id_to_cmp_list[1],
		provide_context=False,
		apk_id='com.chi.ssetest',
		apk_version='release-20191212-0.0.3',
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
