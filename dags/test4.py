import json

import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
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
        runner_conf.sdkConfig.marketPerm.Level = "1"
        runner_conf.sdkConfig.marketPerm.HKPerms.extend(["hkaz"])
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
            runner_conf.sdkConfig.serverSites["nf"].CopyFrom(Site(ips=["http://114.80.155.61:22013"]))
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
		#..................全真（新版SDK）和生产（现生产版本SDK）对比.........................
        #..........................................306........................................
		#要约回购，要约收购
        #历史k线 方法1 
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'OHLCV3_1'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
            #001
            json.dumps({
                'CODES': '430005.bj',
                'TYPES': 'dayk',
            }),
            #016
            json.dumps({
                'CODES': '899001.bj',
                'TYPES': 'm1',
            }),
        ])
        case_list.append(case_conf)
        #历史k线 方法2
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'OHLCV3_2'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
            #002
            json.dumps({
                'CODES': '839806.bj',
                'TYPES': 'dayk',
                'FqTypes': '0',
                'DATES': 'null',
            }),
            #017
            json.dumps({
                'CODES': '899001.bj',
                'TYPES': 'dayk',
                'FqTypes': '0',
                'DATES': 'null',
            }),
        ])
        case_list.append(case_conf)
        #历史k线 方法3
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'OHLCV3_3'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
            #003
            json.dumps({
                'CODES': '839806.bj',
				'DATES': '20191031150000',
				'TYPES': 'm1',
				'FqTypes': '0',		
            }),
            # #018
            # json.dumps({
            #     'CODES': '899001.bj',
			# 	'DATES': '20191001093000',
			# 	'TYPES': 'm1',
			# 	'FqTypes': '0',	
            # }),
        ])
        case_list.append(case_conf)
        #历史k线 方法4----------新三板不支持
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'OHLCV3_4'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
            # #004
            # json.dumps({
            #     'CODES': '430005.bj',
            #     'BeginDates': 'null',
            #     'EndDates': '20191028093000',
            #     'TYPES': 'm1',
            #     'FqTypes': '2',
            # }),
            # #019
            # json.dumps({
            #      'CODES': '899001.bj',
            #     'BeginDates': 'null',
            #     'EndDates': '20191028093000',
            #     'TYPES': 'm1',
            #     'FqTypes': '2',
            # }),
        ])
        case_list.append(case_conf)
        #历史k线 方法5
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'OHLCV3_5'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
            #005
            json.dumps({
                'CODES': '839806.bj',
                'TYPES': 'm1',
                'FqTypes': '0',
                'Dates': 'null',
                'Numbers': '300',
            }),
             #020
            json.dumps({
               'CODES': '899001.bj',
                'TYPES': 'm1',
                'FqTypes': '0',
                'Dates': 'null',
                'Numbers': '300',
            }),
        ])
        case_list.append(case_conf)
        #历史k线 方法6
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'OHLCV3_6'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
            #006
            json.dumps({
                'CODES': '839806.bj',
                'Dates': '20191118093000',
                'TYPES': 'm1',
                'FqTypes': '2',
                'Numbers': '20',
            }),
            #007
            json.dumps({
                'CODES': '839806.bj',
                'Dates': '20191118093000',
                'TYPES': 'm5',
                'FqTypes': '2',
                'Numbers': '20',
            }),
            #008
            json.dumps({
                'CODES': '430005.bj',
                'Dates': '20191118093000',
                'TYPES': 'm15',
                'FqTypes': '2',
                'Numbers': '20',
            }),
            #009
            json.dumps({
                'CODES': '839806.bj',
                'Dates': '20191118093000',
                'TYPES': 'm30',
                'FqTypes': '2',
                'Numbers': '20',
            }),
            #010
            json.dumps({
                'CODES': '430005.bj',
                'Dates': '20191118093000',
                'TYPES': 'm60',
                'FqTypes': '2',
                'Numbers': '20',
            }),
            #011
            json.dumps({
                'CODES': '430005.bj',
                'Dates': '20191118093000',
                'TYPES': 'm120',
                'FqTypes': '2',
                'Numbers': '20',
            }),
            #012
            json.dumps({
                'CODES': '430005.bj',
                'Dates': '20191118093000',
                'TYPES': 'dayk',
                'FqTypes': '2',
                'Numbers': '20',
            }),
            #013
            json.dumps({
                'CODES': '839806.bj',
                'Dates': '20191118093000',
                'TYPES': 'weekk',
                'FqTypes': '2',
                'Numbers': '20',
            }),
            #014
            json.dumps({
                'CODES': '839806.bj',
                'Dates': '20191118093000',
                'TYPES': 'monthk',
                'FqTypes': '2',
                'Numbers': '20',
            }),
            #015
            json.dumps({
                'CODES': '839806.bj',
                'Dates': '20191118093000',
                'TYPES': 'yeark',
                'FqTypes': '2',
                'Numbers': '20',
            }),
            #021
            json.dumps({
                'CODES': '899001.bj',
                'Dates': '20191118093000',
                'TYPES': 'm1',
                'FqTypes': '2',
                'Numbers': '20',
            }),
            #022
            json.dumps({
                'CODES': '899001.bj',
                'Dates': '20191118093000',
                'TYPES': 'm5',
                'FqTypes': '2',
                'Numbers': '20',
            }),
            #023
            json.dumps({
                'CODES': '899001.bj',
                'Dates': '20191118093000',
                'TYPES': 'm15',
                'FqTypes': '2',
                'Numbers': '20',
            }),
            #024
            json.dumps({
                'CODES': '899001.bj',
                'Dates': '20191118093000',
                'TYPES': 'm30',
                'FqTypes': '2',
                'Numbers': '20',
            }),
            #025
            json.dumps({
                'CODES': '899001.bj',
                'Dates': '20191118093000',
                'TYPES': 'm60',
                'FqTypes': '2',
                'Numbers': '20',
            }),
            #026
            json.dumps({
                'CODES': '899001.bj',
                'Dates': '20191118093000',
                'TYPES': 'm120',
                'FqTypes': '2',
                'Numbers': '20',
            }),
            #027
            json.dumps({
                'CODES': '899001.bj',
                'Dates': '20191118093000',
                'TYPES': 'dayk',
                'FqTypes': '2',
                'Numbers': '20',
            }),
            #028
            json.dumps({
                'CODES': '899001.bj',
                'Dates': '20191118093000',
                'TYPES': 'weekk',
                'FqTypes': '2',
                'Numbers': '20',
            }),
            #029
            json.dumps({
                'CODES': '899001.bj',
                'Dates': '20191118093000',
                'TYPES': 'monthk',
                'FqTypes': '2',
                'Numbers': '20',
            }),
            #030
            json.dumps({
                'CODES': '899001.bj',
                'Dates': '20191118093000',
                'TYPES': 'yeark',
                'FqTypes': '2',
                'Numbers': '20',
            }),
            # #031
            # json.dumps({
            #     'CODES': '.bj',
            #     'Dates': '20191118093000',
            #     'TYPES': 'm1',
            #     'FqTypes': '2',
            #     'Numbers': '20',
            # }),
            # #032
            # json.dumps({
            #     'CODES': '.bj',
            #     'Dates': '20191118093000',
            #     'TYPES': 'm5',
            #     'FqTypes': '2',
            #     'Numbers': '20',
            # }),
            # #033
            # json.dumps({
            #     'CODES': '.bj',
            #     'Dates': '20191118093000',
            #     'TYPES': 'm15',
            #     'FqTypes': '2',
            #     'Numbers': '20',
            # }),
            # #034
            # json.dumps({
            #     'CODES': '.bj',
            #     'Dates': '20191118093000',
            #     'TYPES': 'm30',
            #     'FqTypes': '2',
            #     'Numbers': '20',
            # }),
            # #035
            # json.dumps({
            #     'CODES': '.bj',
            #     'Dates': '20191118093000',
            #     'TYPES': 'm60',
            #     'FqTypes': '2',
            #     'Numbers': '20',
            # }),
            # #036
            # json.dumps({
            #     'CODES': '.bj',
            #     'Dates': '20191118093000',
            #     'TYPES': 'm120',
            #     'FqTypes': '2',
            #     'Numbers': '20',
            # }),
            # #037
            # json.dumps({
            #     'CODES': '.bj',
            #     'Dates': '20191118093000',
            #     'TYPES': 'dayk',
            #     'FqTypes': '2',
            #     'Numbers': '20',
            # }),
            # #38
            # json.dumps({
            #     'CODES': '.bj',
            #     'Dates': '20191118093000',
            #     'TYPES': 'weekk',
            #     'FqTypes': '2',
            #     'Numbers': '20',
            # }),
            # #039
            # json.dumps({
            #     'CODES': '.bj',
            #     'Dates': '20191118093000',
            #     'TYPES': 'monthk',
            #     'FqTypes': '2',
            #     'Numbers': '20',
            # }),
            # #040
            # json.dumps({
            #     'CODES': '.bj',
            #     'Dates': '20191118093000',
            #     'TYPES': 'yeark',
            #     'FqTypes': '2',
            #     'Numbers': '20',
            # }),
            # #041
            # json.dumps({
            #     'CODES': '841003.bj',
            #     'Dates': '20191118093000',
            #     'TYPES': 'm1',
            #     'FqTypes': '2',
            #     'Numbers': '20',
            # }),
            # #042
            # json.dumps({
            #     'CODES': '841003.bj',
            #     'Dates': '20191118093000',
            #     'TYPES': 'm5',
            #     'FqTypes': '2',
            #     'Numbers': '20',
            # }),
            # #043
            # json.dumps({
            #     'CODES': '841003.bj',
            #     'Dates': '20191118093000',
            #     'TYPES': 'm15',
            #     'FqTypes': '2',
            #     'Numbers': '20',
            # }),
            # #044
            # json.dumps({
            #     'CODES': '841003.bj',
            #     'Dates': '20191118093000',
            #     'TYPES': 'm30',
            #     'FqTypes': '2',
            #     'Numbers': '20',
            # }),
            # #045
            # json.dumps({
            #     'CODES': '841003.bj',
            #     'Dates': '20191118093000',
            #     'TYPES': 'm60',
            #     'FqTypes': '2',
            #     'Numbers': '20',
            # }),
            # #046
            # json.dumps({
            #     'CODES': '841003.bj',
            #     'Dates': '20191118093000',
            #     'TYPES': 'm120',
            #     'FqTypes': '2',
            #     'Numbers': '20',
            # }),
            # #047
            # json.dumps({
            #     'CODES': '841003.bj',
            #     'Dates': '20191118093000',
            #     'TYPES': 'dayk',
            #     'FqTypes': '2',
            #     'Numbers': '20',
            # }),
            # #48
            # json.dumps({
            #     'CODES': '841003.bj',
            #     'Dates': '20191118093000',
            #     'TYPES': 'weekk',
            #     'FqTypes': '2',
            #     'Numbers': '20',
            # }),
            # #049
            # json.dumps({
            #     'CODES': '841003.bj',
            #     'Dates': '20191118093000',
            #     'TYPES': 'monthk',
            #     'FqTypes': '2',
            #     'Numbers': '20',
            # }),
            # #050
            # json.dumps({
            #     'CODES': '841003.bj',
            #     'Dates': '20191118093000',
            #     'TYPES': 'yeark',
            #     'FqTypes': '2',
            #     'Numbers': '20',
            # }),
        ])
        case_list.append(case_conf)
        #行情快照
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'QUOTEDETAIL_2'
        case_conf.continueWhenFailed = False
        case_conf.roundIntervalSec = 3
        case_conf.paramStrs.extend([
            #001
        	json.dumps({
        		'CODES': '839806.bj',
        		'COUNTS': '10',
                'INTS1': 'null',
        		'INTS2': 'null',
        	}),
            #002
            json.dumps({
        		'CODES': '841003.bj',
        		'COUNTS': '10',
                'INTS1': 'null',
        		'INTS2': 'null',
        	}),
            #003
            json.dumps({
        		'CODES': '841004.bj',
        		'COUNTS': '10',
                'INTS1': 'null',
        		'INTS2': 'null',
        	}),
            #004
            json.dumps({
        		'CODES': '899001.bj',
        		'COUNTS': '10',
                'INTS1': 'null',
        		'INTS2': 'null',
        	}),
        ])
        case_list.append(case_conf)
        #排序
        case_conf = TestcaseConfig() 
        case_conf.testcaseID = 'CATESORTING_2'
        case_conf.continueWhenFailed = False
        case_conf.roundIntervalSec = 3
        case_conf.paramStrs.extend([
            #001代码
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,1,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #002
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,1,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #003名称
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,2,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #004
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,2,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #005昨收
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,11,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #006
           json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,11,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #007开盘
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,10,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #008
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,10,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #009最高
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,8,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #010
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,8,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #011最低
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,9,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #012
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,9,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #013最新
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,7,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #014
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,7,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #015均价
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,18,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #016
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,18,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #017涨跌
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #018
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #019涨跌幅
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,-3,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #020 
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,-3,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #021成交量
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,13,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #022
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,13,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #023成交额
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #024
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #025当前成交量
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,14,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #026
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,14,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #027内盘
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,25,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #028
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,25,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #029外盘
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,24,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #030
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,24,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #031交易日
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,119,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #032
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,119,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #033结算组代码
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,120,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #034
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,120,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #035结算编号
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,121,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #036
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,121,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #037昨结
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,68,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #038
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,68,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #039昨持仓
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,123,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #040
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,123,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #041持仓
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,124,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #042
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,124,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #043日增
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,125,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #044
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,125,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #045今收盘
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,126,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #046
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,126,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #047今结算
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,127,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #048
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,127,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #049涨停
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,16,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #050
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,16,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #051跌停
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,17,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #052
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,17,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #053昨虚
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,100,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #054
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,100,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #055今虚
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,101,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #056
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,101,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #057最后修改毫秒
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,102,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #058
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,102,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #059标的现价
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,103,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #060
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,103,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #061标的昨收
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,104,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #062
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,104,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #063标的涨跌
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,105,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #064
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,105,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #065交易状态
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,0,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #066
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #067change1
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,107,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #068
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,107,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #069振幅
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,37,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #070
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #071仓差
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,108,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #072
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,108,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #073期权类型
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,109,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #074
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,109,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #075行权价
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,110,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #076
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,110,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #077溢价率
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,111,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #078
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,111,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #079剩余天数
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,112,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #080
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,112,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #081隐含波动率
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,113,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #082
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,113,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #083无风险利率
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,114,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #084
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,114,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #085风险指标
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,115,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #086
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,115,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #087杠杆比率
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,116,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #088
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,116,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #089交割点数
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,117,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #090
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,117,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #091买一价
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,22,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #092
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,22,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #095卖一价
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,23,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #096
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,23,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #099委差
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,54,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #100
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,54,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #101委比
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,53,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #102
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,53,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #105仓差
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,108,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #106
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,108,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #要约回收购111
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,1,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #112
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #113
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,2,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #114
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,2,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #115
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,11,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #116
           json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,11,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #117
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,10,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #118
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,10,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #119
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,8,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #120
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,8,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #121
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,9,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #122
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,9,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #123
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,7,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #124
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,7,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #125
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,18,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #126
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,18,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #127
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,19,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #128
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,19,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #129
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,-3,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #130 
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,-3,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #131
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,13,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #132
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,13,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #133
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,20,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #134
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,20,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #135
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,14,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #136
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,14,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #137
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,25,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #138
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,25,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #139
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,24,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #140
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,24,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #141
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,119,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #142
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,119,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #143
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,120,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #144
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,120,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #145
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,121,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #146
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,121,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #147
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,68,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #148
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,68,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #149
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,123,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #150
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,123,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #151
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,124,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #152
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,124,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #153
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,125,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #154
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,125,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #155
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,126,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #156
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,126,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #157
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,127,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #158
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,127,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #159
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,16,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #160
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,16,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #161
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,17,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #162
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,17,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #163
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,100,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #164
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,100,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #165
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,101,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #166
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,101,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #167
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,102,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #168
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,102,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #169
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,103,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #170
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,103,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #171
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,104,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #172
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,104,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #173
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,105,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #174
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,105,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #175
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,0,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #176
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #177
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,107,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #178
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,107,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #179
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,37,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #180
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,37,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #181
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,108,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #182
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,108,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #183
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,109,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #184
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,109,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #185
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,110,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #186
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,110,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #187
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,111,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #188
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,111,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #189
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,112,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #190
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,112,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #191
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,113,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #192
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,113,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #193
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,114,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #194
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,114,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #195
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,115,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #196
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,115,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #197
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,116,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #198
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,116,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #199
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,117,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #200
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,117,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #201
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,22,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #202
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,22,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #205
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,23,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #206
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,23,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #209
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,54,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #210
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,54,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #211
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,53,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #212
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,53,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #215
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,108,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #216
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,100,108,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),      
            #要约收购221...............返回结果为空
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,1,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #222
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #223
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,2,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #224
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,2,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #225
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,11,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #226
           json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,11,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #227
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,10,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #228
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,10,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #229
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,8,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #230
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,8,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #231
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,9,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #232
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,9,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #233
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,7,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #234
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,7,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #235
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,18,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #236
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,18,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #237
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,19,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #238
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,19,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #239
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,-3,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #240 
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,-3,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #241
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,13,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #242
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,13,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #243
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,20,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #244
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,20,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #245
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,14,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #246
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,14,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #247
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,25,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #248
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,25,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #249
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,24,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #250
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,24,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #251
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,119,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #252
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,119,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #253
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,120,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #254
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,120,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #255
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,121,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #256
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,121,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #257
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,68,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #258
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,68,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #259
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,123,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #260
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,123,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #261
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,124,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #262
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,124,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #263
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,125,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #264
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,125,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #265
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,126,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #266
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,126,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #267
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,127,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #268
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,127,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #269
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,16,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #270
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,16,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #271
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,17,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #272
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,17,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #273
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,100,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #274
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,100,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #275
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,101,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #276
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,101,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #277
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,102,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #278
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,102,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #279
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,103,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #280
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,103,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #281
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,104,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #282
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,104,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #283
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,105,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #284
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,105,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #285
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,0,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #286
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #287
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,107,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #288
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,107,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #289
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,37,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #290
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,37,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #291
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,108,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #292
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,108,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #293
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,109,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #294
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,109,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #295
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,110,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #296
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,110,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #297
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,111,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #298
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,111,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #299
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,112,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #300
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,112,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #301
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,113,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #302
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,113,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #303
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,114,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #304
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,114,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #305
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,115,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #306
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,115,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #307
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,116,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #308
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,116,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #309
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,117,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #310
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,117,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #311
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,22,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #312
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,22,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #315
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,23,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #316
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,23,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #319
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,54,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #320
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,54,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #321
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,53,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #322
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,53,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #325
        	json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,108,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #326
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,100,108,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #要约回购331
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,1,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #332
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #333
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,2,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #334
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,2,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #335
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,11,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #336
           json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,11,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #337
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,10,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #338
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,10,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #339
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,8,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #340
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,8,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #341
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,9,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #342
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,9,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #343
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,7,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #344
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,7,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #345
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,18,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #346
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,18,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #347
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,19,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #348
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,19,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #349
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,-3,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #350 
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,-3,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #351
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,13,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #352
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,13,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #353
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,20,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #354
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,20,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #355
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,14,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #356
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,14,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #357
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,25,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #358
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,25,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #359
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,24,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #360
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,24,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #361
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,119,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #362
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,119,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #363
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,120,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #364
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,120,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #365
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,121,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #366
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,121,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #367
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,68,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #368
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,68,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #369
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,123,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #370
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,123,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #371
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,124,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #372
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,124,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #373
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,125,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #374
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,125,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #375
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,126,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #376
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,126,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #377
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,127,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #378
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,127,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #379
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,16,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #380
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,16,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #381
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,17,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #382
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,17,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #383
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,100,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #384
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,100,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #385
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,101,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #386
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,101,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #387
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,102,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #388
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,102,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #389
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,103,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #390
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,103,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #391
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,104,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #392
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,104,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #393
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,105,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #394
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,105,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #395
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,0,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #396
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #397
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,107,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #398
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,107,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #399
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,37,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #400
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,37,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #401
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,108,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #402
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,108,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #403
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,109,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #404
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,109,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #405
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,110,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #406
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,110,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #407
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,111,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #408
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,111,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #409
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,112,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #410
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,112,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #411
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,113,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #412
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,113,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #413
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,114,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #414
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,114,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #415
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,115,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #416
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,115,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #417
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,116,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #418
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,116,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #419
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,117,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #420
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,117,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #421
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,22,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #422
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,22,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #425
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,23,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #426
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,23,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #429
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,54,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #430
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,54,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #431
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,53,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #432
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,53,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #435
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,108,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #436
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,100,108,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #新三板指数441
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,1,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #442
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #443
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,2,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #444
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,2,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #445
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,11,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #446
           json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,11,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #447
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,10,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #448
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,10,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #449
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,8,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #450
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,8,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #451
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,9,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #452
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,9,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #453
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,7,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #454
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,7,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #455
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,18,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #456
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,18,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #457
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,19,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #458
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,19,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #459
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,-3,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #460 
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,-3,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #461
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,13,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #462
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,13,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #463
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,20,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #464
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,20,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #465
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,14,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #466
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,14,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #467
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,25,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #468
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,25,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #469
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,24,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #470
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,24,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #471
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,119,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #472
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,119,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #473
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,120,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #474
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,120,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #475
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,121,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #476
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,121,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #477
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,68,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #478
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,68,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #479
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,123,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #480
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,123,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #481
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,124,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #482
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,124,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #483
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,125,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #484
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,125,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #485
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,126,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #486
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,126,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #487
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,127,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #488
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,127,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #489
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,16,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #490
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,16,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #491
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,17,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #492
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,17,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #493
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,100,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #494
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,100,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #495
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,101,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #496
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,101,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #497
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,102,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #498
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,102,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #499
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,103,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #500
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,103,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #501
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,104,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #502
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,104,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #503
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,105,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #504
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,105,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #505
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,0,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #506
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #507
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,107,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #508
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,107,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #509
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,37,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #510
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,37,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #511
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,108,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #512
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,108,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #513
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,109,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #514
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,109,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #515
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,110,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #516
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,110,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #517
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,111,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #518
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,111,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #519
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,112,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #520
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,112,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #521
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,113,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #522
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,113,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #523
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,114,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #524
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,114,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #525
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,115,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #526
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,115,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #527
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,116,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #528
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,116,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #529
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,117,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #530
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,117,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #531
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,22,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #532
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,22,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #535
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,23,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #536
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,23,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #539
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,54,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #540
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,54,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #541
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,53,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #542
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,53,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #545
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,108,0',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #546
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,108,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
        ])
        case_list.append(case_conf)
		#走势数据
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'CHARTV2TEST_2'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
            #001
        	json.dumps({
        		'CODES': '831814.bj',
        		'Chart_Types': 'ChartTypeOneDay',       
        	}),
			#005
        	json.dumps({
        		'CODES': '841004.bj',
        		'Chart_Types': 'ChartTypeOneDay',       
        	}),
			#007
        	json.dumps({
        		'CODES': '899001.bj',
        		'Chart_Types': 'ChartTypeOneDay',       
        	}),
			#.........................................当日、五日，分开传
            #002
            json.dumps({
               'CODES': '831814.bj',
        	   'Chart_Types': 'ChartTypeFiveDay', 
            }),
			
            #006
            json.dumps({
               'CODES': '841004.bj',
        	   'Chart_Types': 'ChartTypeFiveDay', 
            }),
			
            #008
            json.dumps({
               'CODES': '899001.bj',
        	   'Chart_Types': 'ChartTypeFiveDay', 
            }),
        ])
        case_list.append(case_conf)
		#...........................................351.................................................
		#走势数据
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'CHARTV2TEST_1'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
            #001
            json.dumps({
				'CODES': '600000.sh',
				'Chart_Types': 'ChartTypeFiveDay',
				'SUBTYPES': '1010'
	        }),
			#002
            json.dumps({
				'CODES': '000001.sh',
				'Chart_Types': 'ChartTypeFiveDay',
				'SUBTYPES': '1010'
	        }),
			#003
            json.dumps({
				'CODES': '10002008.sh',
				'Chart_Types': 'ChartTypeFiveDay',
				'SUBTYPES': '1010'
	        }),
			#004
            json.dumps({
				'CODES': '204001.sh',
				'Chart_Types': 'ChartTypeFiveDay',
				'SUBTYPES': '1010'
	        }),
			#005
            json.dumps({
				'CODES': '113544.sh',
				'Chart_Types': 'ChartTypeFiveDay',
				'SUBTYPES': '1010'
	        }),
			#006
            json.dumps({
				'CODES': '688001.sh',
				'Chart_Types': 'ChartTypeFiveDay',
				'SUBTYPES': '1010'
	        }),
			# #007
            # json.dumps({
			# 	'CODES': '501006.sh',
			# 	'Chart_Types': 'ChartTypeFiveDay',
			# 	'SUBTYPES': '1010'
	        # }),
			#008
            json.dumps({
				'CODES': '000001.sz',
				'Chart_Types': 'ChartTypeFiveDay',
				'SUBTYPES': '1010'
	        }),
			#009
            json.dumps({
				'CODES': '200018.sz',
				'Chart_Types': 'ChartTypeFiveDay',
				'SUBTYPES': '1010'
	        }),
			#010
            json.dumps({
				'CODES': '150008.sz',
				'Chart_Types': 'ChartTypeFiveDay',
				'SUBTYPES': '1010'
	        }),
			#011
            json.dumps({
				'CODES': '131810.sz',
				'Chart_Types': 'ChartTypeFiveDay',
				'SUBTYPES': '1010'
	        }),
			#012
            json.dumps({
				'CODES': '128037.sz',
				'Chart_Types': 'ChartTypeFiveDay',
				'SUBTYPES': '1010'
	        }),
			#013
            json.dumps({
				'CODES': '399001.sz',
				'Chart_Types': 'ChartTypeFiveDay',
				'SUBTYPES': '1010'
	        }),
			#014....................................若无返回，更换港股环境
            json.dumps({
				'CODES': '02378.hk',
				'Chart_Types': 'ChartTypeFiveDay',
				'SUBTYPES': '1010'
	        }),
			#015
            json.dumps({
				'CODES': '08469.hk',
				'Chart_Types': 'ChartTypeFiveDay',
				'SUBTYPES': '1010'
	        }),
			#016
            json.dumps({
				'CODES': '03011.hk',
				'Chart_Types': 'ChartTypeFiveDay',
				'SUBTYPES': '1010'
	        }),
			#017
            json.dumps({
				'CODES': '05130.hk',
				'Chart_Types': 'ChartTypeFiveDay',
				'SUBTYPES': '1010'
	        }),
			#018
            json.dumps({
				'CODES': 'HSI.hk',
				'Chart_Types': 'ChartTypeFiveDay',
				'SUBTYPES': '1010'
	        }),
			#019
            json.dumps({
				'CODES': '57956.hk',
				'Chart_Types': 'ChartTypeFiveDay',
				'SUBTYPES': '1010'
	        }),
			#020
            json.dumps({
				'CODES': '20569.hk',
				'Chart_Types': 'ChartTypeFiveDay',
				'SUBTYPES': '1010'
	        }),
			#021
            json.dumps({
				'CODES': '02318.hk',
				'Chart_Types': 'ChartTypeFiveDay',
				'SUBTYPES': '1010'
	        }),
			#022
            json.dumps({
				'CODES': '02359.hk',
				'Chart_Types': 'ChartTypeFiveDay',
				'SUBTYPES': '1010'
	        }),
            #023
            json.dumps({
				'CODES': '00011.hk',
				'Chart_Types': 'ChartTypeFiveDay',
				'SUBTYPES': '1010'
	        }),
			#024
            json.dumps({
				'CODES': '02588.hk',
				'Chart_Types': 'ChartTypeFiveDay',
				'SUBTYPES': '1010'
	        }),
			#025
            json.dumps({
				'CODES': '02382.hk',
				'Chart_Types': 'ChartTypeFiveDay',
				'SUBTYPES': '1010'
	        }),
			#026
            json.dumps({
				'CODES': '00388.hk',
				'Chart_Types': 'ChartTypeFiveDay',
				'SUBTYPES': '1010'
	        }),
			#027
            json.dumps({
				'CODES': '01558.hk',
				'Chart_Types': 'ChartTypeFiveDay',
				'SUBTYPES': '1010'
	        }),
			#028
            json.dumps({
				'CODES': '00700.hk',
				'Chart_Types': 'ChartTypeFiveDay',
				'SUBTYPES': '1010'
	        }),
			# #029
            # json.dumps({
			# 	'CODES': '.hk',
			# 	'Chart_Types': 'ChartTypeFiveDay',
			# 	'SUBTYPES': '1010'
	        # }),
        ])
        case_list.append(case_conf)
        #行情快照
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'QUOTEDETAIL_1'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
            #001....................................若无返回，更换港股环境
            json.dumps({
				'CODES': '02378.hk',
	        }),
			#002
            json.dumps({
				'CODES': '08469.hk',
				
	        }),
			#003
            json.dumps({
				'CODES': '03011.hk',
				
	        }),
			#004
            json.dumps({
				'CODES': '05130.hk',
				
	        }),
			#005
            json.dumps({
				'CODES': 'HSI.hk',
				
	        }),
			#006
            json.dumps({
				'CODES': '57956.hk',
				
	        }),
			#007
            json.dumps({
				'CODES': '20569.hk',
				
	        }),
			#008
            json.dumps({
				'CODES': '02318.hk',
				
	        }),
			#009
            json.dumps({
				'CODES': '02359.hk',
				
	        }),
			#010
            json.dumps({
				'CODES': '00011.hk',
				
	        }),
			#011
            json.dumps({
				'CODES': '02588.hk',
				
	        }),
			#012
            json.dumps({
				'CODES': '02382.hk',
				
	        }),
			#013
            json.dumps({
				'CODES': '00388.hk',
				
	        }),
			#014
            json.dumps({
				'CODES': '01558.hk',
				
	        }),
			#015
            json.dumps({
				'CODES': '00700.hk',
				
	        }),
		])
        case_list.append(case_conf)
		#排序
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'CATESORTING_2'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([	
			#001
            json.dumps({
				'id': 'HK1010',
				'param': '0,50,21,1,1',
				'quoteCustom': '-1',
				'addvalueCustom': 'null',		
	        }),
			#002
            json.dumps({
				'id': 'HK1000',
				'param': '0,50,21,1,1',
				'quoteCustom': '-1',
				'addvalueCustom': 'null',		
	        }),
			#003
            json.dumps({
				'id': 'HK1004',
				'param': '0,50,21,1,1',
				'quoteCustom': '-1',
				'addvalueCustom': 'null',
	        }),
			#004
            json.dumps({
				'id': 'HK1100',
				'param': '0,50,21,1,1',
				'quoteCustom': '-1',
				'addvalueCustom': 'null',
	        }),
			#005
            json.dumps({
				'id': 'HK1300',
				'param': '0,50,21,1,1',
				'quoteCustom': '-1',
				'addvalueCustom': 'null',		
	        }),
			#006
            json.dumps({
				'id': 'HK1400',
				'param': '0,50,21,1,1',
				'quoteCustom': '-1',
				'addvalueCustom': 'null',	
	        }),
			#007
            json.dumps({
				'id': 'HK1500',
				'param': '0,50,21,1,1',
				'quoteCustom': '-1',
				'addvalueCustom': 'null',		
	        }),
			#008
            json.dumps({
				'id': 'HK1600',
				'param': '0,50,21,1,1',
				'quoteCustom': '-1',
				'addvalueCustom': 'null',
	        }),
			#009
            json.dumps({
				'id': 'HKAHG',
				'param': '0,50,21,1,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null',		
	        }),
			#010
            json.dumps({
				'id': 'HKGQ',
				'param': '0,50,21,1,1',
				'quoteCustom': '-1',
				'addvalueCustom': 'null',	
	        }),
			#011
            json.dumps({
				'id': 'HKLC',
				'param': '0,50,21,1,1',
				'quoteCustom': '-1',
				'addvalueCustom': 'null',	
	        }),
			#012
            json.dumps({
				'id': 'HKHC',
				'param': '0,50,21,1,1',
				'quoteCustom': '-1',
				'addvalueCustom': 'null',
	        }),
			#013
            json.dumps({
				'id': 'HSI',
				'param': '0,50,21,1,1',
				'quoteCustom': '-1',
				'addvalueCustom': 'null',		
	        }),
			#014
            json.dumps({
				'id': 'SHHGT',
				'param': '0,50,21,1,1',
				'quoteCustom': '-1',
				'addvalueCustom': 'null',	
	        }),
			#015
            json.dumps({
				'id': 'SZSGT',
				'param': '0,50,21,1,1',
				'quoteCustom': '-1',
				'addvalueCustom': 'null',	
	        }),
			#016
            json.dumps({
				'id': 'HKGGT',
				'param': '0,50,21,1,1',
				'quoteCustom': '-1',
				'addvalueCustom': 'null',
	        }),
		])
        case_list.append(case_conf)
		#历史k线
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'OHLCV3_6'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
            #001....................................若无返回，更换港股环境
        	json.dumps({
        		'CODES': '00700.hk',
				'Dates': '20190731',
				'TYPES': 'dayk',
				'FqTypes': '2',
				'Numbers': '100',
        	}),
			#002
        	json.dumps({
        		'CODES': '08635.hk',
				'Dates': '20190731',
				'TYPES': 'dayk',
				'FqTypes': '0',
				'Numbers': '100',
        	}),
			#003
        	json.dumps({
        		'CODES': '03011.hk',
				'Dates': '20190731',
				'TYPES': 'dayk',
				'FqTypes': '1',
				'Numbers': '100',
        	}),
			#004
        	json.dumps({
        		'CODES': '05130.hk',
				'Dates': '20190731',
				'TYPES': 'weekk',
				'FqTypes': '2',
				'Numbers': '100',
        	}),
			# #005
        	# json.dumps({
        	# 	'CODES': 'HSI.hk',
			# 	'Dates': '20190731',
			# 	'TYPES': 'weekk',
			# 	'FqTypes': '0',
			# 	'Numbers': '100',
        	# }),
			#006
        	json.dumps({
        		'CODES': '57956.hk',
				'Dates': '20190731',
				'TYPES': 'weekk',
				'FqTypes': '1',
				'Numbers': '100',
        	}),
			#007
        	json.dumps({
        		'CODES': '20569.hk',
				'Dates': '20190731',
				'TYPES': 'monthk',
				'FqTypes': '2',
				'Numbers': '100',
        	}),
			#008
        	json.dumps({
        		'CODES': '02318.hk',
				'Dates': '20190731',
				'TYPES': 'monthk',
				'FqTypes': '1',
				'Numbers': '100',
        	}),
			#009
        	json.dumps({
        		'CODES': '02359.hk',
				'Dates': '20190731',
				'TYPES': 'yeark',
				'FqTypes': '2',
				'Numbers': '100',
        	}),
			#010
        	json.dumps({
        		'CODES': '00011.hk',
				'Dates': '20190731',
				'TYPES': 'yeark',
				'FqTypes': '0',
				'Numbers': '100',
        	}),
			#011
        	json.dumps({
        		'CODES': '02588.hk',
				'Dates': '20190731',
				'TYPES': 'yeark',
				'FqTypes': '1',
				'Numbers': '100',
        	}),
			#012
        	json.dumps({
        		'CODES': '02382.hk',
				'Dates': '20190731',
				'TYPES': 'm1',
				'FqTypes': '2',
				'Numbers': '100',
        	}),
			#013
        	json.dumps({
        		'CODES': '00388.hk',
				'Dates': '20190731',
				'TYPES': 'm5',
				'FqTypes': '2',
				'Numbers': '100',
        	}),
			#014
        	json.dumps({
        		'CODES': '01558.hk',
				'Dates': '20190731',
				'TYPES': 'm15',
				'FqTypes': '2',
				'Numbers': '100',
        	}),
			#015
        	json.dumps({
        		'CODES': '00001.hk',
				'Dates': '20190731',
				'TYPES': 'm30',
				'FqTypes': '2',
				'Numbers': '100',
        	}),
			#016
        	json.dumps({
        		'CODES': '00700.hk',
				'Dates': '20190731',
				'TYPES': 'dayk',
				'FqTypes': '0',
				'Numbers': '100',
        	}),
			#017
        	json.dumps({
        		'CODES': '00700.hk',
				'Dates': '20190731',
				'TYPES': 'dayk',
				'FqTypes': '1',
				'Numbers': '100',
        	}),
			#018
        	json.dumps({
        		'CODES': '00700.hk',
				'Dates': '20190731',
				'TYPES': 'weekk',
				'FqTypes': '2',
				'Numbers': '100',
        	}),
			#019
        	json.dumps({
        		'CODES': '00700.hk',
				'Dates': '20190731',
				'TYPES': 'weekk',
				'FqTypes': '0',
				'Numbers': '100',
        	}),
			#020
        	json.dumps({
        		'CODES': '00700.hk',
				'Dates': '20190731',
				'TYPES': 'weekk',
				'FqTypes': '1',
				'Numbers': '100',
        	}),
			#021
        	json.dumps({
        		'CODES': '00700.hk',
				'Dates': '20190731',
				'TYPES': 'monthk',
				'FqTypes': '2',
				'Numbers': '100',
        	}),
			#022
        	json.dumps({
        		'CODES': '00700.hk',
				'Dates': '20190731',
				'TYPES': 'monthk',
				'FqTypes': '0',
				'Numbers': '100',
        	}),
			#023
        	json.dumps({
        		'CODES': '00700.hk',
				'Dates': '20190731',
				'TYPES': 'monthk',
				'FqTypes': '1',
				'Numbers': '100',
        	}),
			#024
        	json.dumps({
        		'CODES': '00700.hk',
				'Dates': '20190731',
				'TYPES': 'yeark',
				'FqTypes': '2',
				'Numbers': '100',
        	}),
			#025
        	json.dumps({
        		'CODES': '00700.hk',
				'Dates': '20190731',
				'TYPES': 'yeark',
				'FqTypes': '0',
				'Numbers': '100',
        	}),
			#026
        	json.dumps({
        		'CODES': '00700.hk',
				'Dates': '20190731',
				'TYPES': 'yeark',
				'FqTypes': '1',
				'Numbers': '100',
        	}),
			#027
        	json.dumps({
        		'CODES': '00700.hk',
				'Dates': '20190731',
				'TYPES': 'm1',
				'FqTypes': '2',
				'Numbers': '100',
        	}),
			#028
        	json.dumps({
        		'CODES': '00700.hk',
				'Dates': '20190731',
				'TYPES': 'm5',
				'FqTypes': '2',
				'Numbers': '100',
        	}),
			#029
        	json.dumps({
        		'CODES': '00700.hk',
				'Dates': '20190731',
				'TYPES': 'm15',
				'FqTypes': '2',
				'Numbers': '100',
        	}),
			#030
        	json.dumps({
        		'CODES': '00700.hk',
				'Dates': '20190731',
				'TYPES': 'm30',
				'FqTypes': '2',
				'Numbers': '100',
        	}),
			#031
        	json.dumps({
        		'CODES': '00700.hk',
				'Dates': '20190731',
				'TYPES': 'm60',
				'FqTypes': '2',
				'Numbers': '100',
        	}),
			#032
        	json.dumps({
        		'CODES': '00700.hk',
				'Dates': '20190731',
				'TYPES': 'm120',
				'FqTypes': '2',
				'Numbers': '100',
        	}),	
            #033
        	json.dumps({
        		'CODES': '688001.sh',
				'Dates': '20190731',
				'TYPES': 'dayk',
				'FqTypes': '2',
				'Numbers': '100',
        	}),		
            #034
        	json.dumps({
        		'CODES': '501006.sh',
				'Dates': '20190731',
				'TYPES': 'dayk',
				'FqTypes': '2',
				'Numbers': '100',
        	}),			
            #035
        	json.dumps({
        		'CODES': '000001.sz',
				'Dates': '20190731',
				'TYPES': 'm120',
				'FqTypes': '0',
				'Numbers': '100',
        	}),		
			#036
        	json.dumps({
        		'CODES': '200018.sz',
				'Dates': '20190731',
				'TYPES': 'm5',
				'FqTypes': '2',
				'Numbers': '100',
        	}),
			#037...........................k线接口
        	# json.dumps({
        	# 	'CODES': '03011.hk',
			# 	'TYPES': 'dayk',
			# 	'FqTypes': '1',
			# 	'Dates': 'null',
			# 	'Numbers': '300',
        	# }),
			# #038
        	# json.dumps({
        	# 	'CODES': '85744.hk',
			# 	'TYPES': 'weekk',
			# 	'FqTypes': '2',
			# 	'Dates': 'null',
			# 	'Numbers': '300',
        	# }),
			# #039
        	# json.dumps({
        	# 	'CODES': '57956.hk',
			# 	'TYPES': 'monthk',
			# 	'FqTypes': '2',
			# 	'Dates': 'null',
			# 	'Numbers': '300',
        	# }),
			# #040
        	# json.dumps({
        	# 	'CODES': '20569.hk',
			# 	'TYPES': 'm5',
			# 	'FqTypes': '2',
			# 	'Dates': 'null',
			# 	'Numbers': '300',
        	# }),
			# #041
        	# json.dumps({
        	# 	'CODES': '02318.hk',
			# 	'TYPES': 'm30',
			# 	'FqTypes': '2',
			# 	'Dates': 'null',
			# 	'Numbers': '300',
        	# }),
			# #042
        	# json.dumps({
        	# 	'CODES': '02359.hk',
			# 	'TYPES': 'm60',
			# 	'FqTypes': '2',
			# 	'Dates': 'null',
			# 	'Numbers': '300',
        	# }),
			# #043
        	# json.dumps({
        	# 	'CODES': '00011.hk',
			# 	'TYPES': 'm120',
			# 	'FqTypes': '2',
			# 	'Dates': 'null',
			# 	'Numbers': '300',
        	# }),
			# #044
        	# json.dumps({
        	# 	'CODES': '02588.hk',
			# 	'TYPES': 'dayk',
			# 	'FqTypes': '2',
			# 	'Dates': 'null',
			# 	'Numbers': '300',
        	# }),
			# #045
        	# json.dumps({
        	# 	'CODES': '02382.hk',
			# 	'TYPES': 'dayk',
			# 	'FqTypes': '01',
			# 	'Dates': 'null',
			# 	'Numbers': '300',
        	# }),
			# #046
        	# json.dumps({
        	# 	'CODES': '00388.hk',
			# 	'TYPES': 'dayk',
			# 	'FqTypes': '1',
			# 	'Dates': 'null',
			# 	'Numbers': '300',
        	# }),
			# #047
        	# json.dumps({
        	# 	'CODES': '01588.hk',
			# 	'TYPES': 'weekk',
			# 	'FqTypes': '2',
			# 	'Dates': 'null',
			# 	'Numbers': '300',
        	# }),
			# #048
        	# json.dumps({
        	# 	'CODES': '00001.hk',
			# 	'TYPES': 'monthk',
			# 	'FqTypes': '2',
			# 	'Dates': 'null',
			# 	'Numbers': '300',
        	# }),
			# #049
        	# json.dumps({
        	# 	'CODES': 'HSI.hk',
			# 	'TYPES': 'm15',
			# 	'FqTypes': '2',
			# 	'Dates': 'null',
			# 	'Numbers': '300',
        	# }),
			# #050
        	# json.dumps({
        	# 	'CODES': '83242.bj',
			# 	'TYPES': 'dayk',
			# 	'FqTypes': '2',
			# 	'Dates': 'null',
			# 	'Numbers': '300',
        	# }),
			# #051
        	# json.dumps({
        	# 	'CODES': '832422.bj',
			# 	'TYPES': 'dayk',
			# 	'FqTypes': '0',
			# 	'Dates': 'null',
			# 	'Numbers': '300',
        	# }),
			# #052
        	# json.dumps({
        	# 	'CODES': '832422.bj',
			# 	'TYPES': 'dayk',
			# 	'FqTypes': '1',
			# 	'Dates': 'null',
			# 	'Numbers': '300',
        	# }),
			# #053
        	# json.dumps({
        	# 	'CODES': '899002.bj',
			# 	'TYPES': 'weekk',
			# 	'FqTypes': '2',
			# 	'Dates': 'null',
			# 	'Numbers': '300',
        	# }),
			# #054
        	# json.dumps({
        	# 	'CODES': '688001.sh',
			# 	'TYPES': 'weekk',
			# 	'FqTypes': '2',
			# 	'Dates': 'null',
			# 	'Numbers': '300',
        	# }),
			# #055
        	# json.dumps({
        	# 	'CODES': '501006.sh',
			# 	'TYPES': 'dayk',
			# 	'FqTypes': '2',
			# 	'Dates': 'null',
			# 	'Numbers': '300',
        	# }),
			# #056
        	# json.dumps({
        	# 	'CODES': '000001.sz',
			# 	'TYPES': 'm5',
			# 	'FqTypes': '0',
			# 	'Dates': 'null',
			# 	'Numbers': '300',
        	# }),
			# #057
        	# json.dumps({
        	# 	'CODES': '200018.sz',
			# 	'TYPES': 'weekk',
			# 	'FqTypes': '1',
			# 	'Dates': 'null',
			# 	'Numbers': '300',
        	# }),
        ])
        case_list.append(case_conf)
		#........................................425.........................................	
		#板块排行
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'BANKUAISORTING_1'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
			json.dumps({
			#001
				'symbol': 'Trade',
				'param1': '0,12,zcje,1'
			}),
			#002
			json.dumps({
				'symbol': 'Notion',
				'param1': '0,12,hsl,0'
			}),
			#003
			json.dumps({
				'symbol': 'Area',
				'param1': '0,12,jzf,0'
			}),
			#004
			json.dumps({
				'symbol': 'Trade_sw',
				'param1': '0,12,zgj,0'
			}),
			#005
			json.dumps({
				'symbol': 'Trade_sw1',
				'param1': '0,12,zgj,0'
			}),
			#006
			json.dumps({
				'symbol': 'Trade_szyp',
				'param1': '0,12,zxj,0'
			}),
			#007
			json.dumps({
				'symbol': 'Area_szyp',
				'param1': '0,12,zdj,0'
			}),
			#008
			json.dumps({
				'symbol': 'Notion_szyp',
				'param1': '0,12,zsj,1'
			}),
        ])
        case_list.append(case_conf)
		#排行方法一
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'CATESORTING_1'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
			#009  
			json.dumps({
				'id': 'SH1001',
				'param': '0,12,1,0,1'
			}),
		])
        case_list.append(case_conf)
		#排行方法二
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'CATESORTING_2'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
			#010  
			json.dumps({
				'id': 'SH1001',
				'param': '0,100,1,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#011
			json.dumps({
				'id': 'SH1005',
				'param': '0,100,0,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#012
			json.dumps({
				'id': 'SH1006',
				'param': '0,100,2,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#013
			json.dumps({
				'id': 'SH1100',
				'param': '0,100,7,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#014
			json.dumps({
				'id': 'SH1110',
				'param': '0,100,1,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#015
			json.dumps({
				'id': 'SH1120',
				'param': '0,100,7,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#016
			json.dumps({
				'id': 'SH1140',
				'param': '0,100,8,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#017
			json.dumps({
				'id': 'SH1300',
				'param': '0,100,9,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#018
			json.dumps({
				'id': 'SH1311',
				'param': '0,100,10,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#019
			json.dumps({
				'id': 'SH1312',
				'param': '0,100,11,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#020
			json.dumps({
				'id': 'SH1400',
				'param': '0,100,-3,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#021
			json.dumps({
				'id': 'SH3002',
				'param': '0,100,1,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#022
			json.dumps({
				'id': 'SH1313',
				'param': '0,100,13,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#023
			json.dumps({
				'id': 'SH1314',
				'param': '0,100,14,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#024
			json.dumps({
				'id': 'SH1521',
				'param': '0,100,1,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#025
			json.dumps({
				'id': 'SH1520',
				'param': '0,100,1,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#026
			json.dumps({
				'id': 'SZ1001',
				'param': '0,100,20,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#027
			json.dumps({
				'id': 'SZ1003',
				'param': '0,100,21,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#028
			json.dumps({
				'id': 'SZ1004',
				'param': '0,100,1,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#029
			json.dumps({
				'id': 'SZ1100',
				'param': '0,100,13,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#030
			json.dumps({
				'id': 'SZ1120',
				'param': '0,100,14,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#031
			json.dumps({
				'id': 'SZ1300',
				'param': '0,100,27,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#032
			json.dumps({
				'id': 'SZ1312',
				'param': '0,100,28,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#033
			json.dumps({
				'id': 'SZ1000',
				'param': '0,100,0,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#034
			json.dumps({
				'id': 'SZ1313',
				'param': '0,100,30,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#036
			json.dumps({
				'id': 'SHSZ1001',
				'param': '0,100,32,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#037
			json.dumps({
				'id': 'SHSZ1313',
				'param': '0,100,32,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#038
			json.dumps({
				'id': 'SHSZ1400',
				'param': '0,100,1,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#039
			json.dumps({
				'id': 'BJ1000',
				'param': '0,100,13,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#040
			json.dumps({
				'id': 'BJ1400',
				'param': '0,100,27,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#041
			json.dumps({
				'id': 'SZHK',
				'param': '0,100,11,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#042
			json.dumps({
				'id': 'SHHGT',
				'param': '0,100,31,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#043
			json.dumps({
				'id': 'HKGGT',
				'param': '0,100,10,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#044
			json.dumps({
				'id': 'HK1010',
				'param': '0,100,1,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#045
			json.dumps({
				'id': 'HSI',
				'param': '0,100,25,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#046
			json.dumps({
				'id': 'HKAHG',
				'param': '0,100,1,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#047
			json.dumps({
				'id': 'HK1400',
				'param': '0,100,17,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#048
			json.dumps({
				'id': 'GB1400',
				'param': '0,100,16,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#049
			json.dumps({
				'id': 'GB1001',
				'param': '0,100,14,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#050
			json.dumps({
				'id': 'cff_all',
				'param': '0,100,18,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#051
			json.dumps({
				'id': 'cff_IC',
				'param': '0,100,13,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#052
			json.dumps({
				'id': 'dce_all',
				'param': '0,100,7,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#053
			json.dumps({
				'id': 'dce_bb',
				'param': '0,100,10,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#054
			json.dumps({
				'id': 'czce_all',
				'param': '0,100,9,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#055
			json.dumps({
				'id': 'shfe_all',
				'param': '0,100,9,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#056
			json.dumps({
				'id': 'shfe_fu',
				'param': '0,100,8,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#057
			json.dumps({
				'id': 'ine_all',
				'param': '0,100,1,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#058
			json.dumps({
				'id': 'ine_sc',
				'param': '0,100,7,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
			#059
			json.dumps({
				'id': 'SHSZ1132',
				'param': '0,100,1,0,1',
				'quoteCustom': 'null',
				'addvalueCustom': 'null'
			}),
        ])
        case_list.append(case_conf)
		#增值指标 方法三
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'ADDVALUE_3'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
			#061  
			json.dumps({
				'code': '600000.sh',
				'market':'sh',
				'subtype': '1001',
				'addValueColumns':'-1'
			}),
			#062
			json.dumps({
				'code': '900928.sh',
				'market':'sh',
				'subtype': '1002',
            	'addValueColumns': '-1'
			}),
			#063
			json.dumps({
				'code': '300799.sz',
				'market':'sz',
				'subtype': '1001',
            	'addValueColumns': '-1'
			}),
			#064
			json.dumps({
				'code': '200596.sz',
				'market':'sz',
				'subtype': '1002',
            	'addValueColumns': '-1'
			}),
			#065
			json.dumps({
				'code': '002509.sz',
				'market':'sz',
				'subtype': '1003',
            	'addValueColumns': '-1'
			}),
			#066
			json.dumps({
				'code': '300067.sz',
				'market':'sz',
				'subtype': '1004',
            	'addValueColumns': '-1'
			}),
			#067
			json.dumps({
				'code': '600634.sh',
				'market':'sh',
				'subtype': '1004',
            	'addValueColumns': '-1'
			}),
			#068
			json.dumps({
				'code': '600747.sh',
				'market':'sh',
				'subtype': 'SHP',
            	'addValueColumns': '-1'
			}),
			#069
			json.dumps({
				'code': '603610.sh',
				'market':'sh',
				'subtype': '1005',
            	'addValueColumns': '-1'
		    }),
		])
        case_list.append(case_conf)
		#......................................沪深....................
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'CATESORTING_2'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
			#001代码
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,1,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #002
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,1,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #003交易状态
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,0,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #004
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#005名称
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,2,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #006
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,2,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),			
            #007昨收
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,11,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #008
           json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,11,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #009开盘
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,10,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #010
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,10,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #011最高
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,8,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #012
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,8,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #013最低
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,9,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #014
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,9,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #015最新
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,7,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #016
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,7,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#017涨跌
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #018
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #019涨跌幅
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-3,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #020 
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-3,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #021成交量
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,13,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #022
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,13,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #023成交额
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #024
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #025当前成交量
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,14,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #026
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,14,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#027换手率
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,15,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #028
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,15,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#029量比
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,21,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #030
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#031内盘
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,25,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #032
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,25,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #033外盘
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,24,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #034
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,24,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#035总市值
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,26,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #036
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,26,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#037流通市值
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,27,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #038
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,27,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#039净资产
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,28,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #040
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,28,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#041动态市盈率
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,29,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #042
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,29,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),			
            #043市净率
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,30,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #044
           json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,30,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #045总股本
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,31,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #046
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,31,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #047流通股
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,32,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #048
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,32,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #049振幅比率
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,37,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #050
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #051动态每股收益
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,38,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #052
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#053委比
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,53,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #054
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,53,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #055静态市盈率
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,42,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #056 
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #057盘后成交量
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,72,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #058
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,72,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #059盘后成交额
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,73,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #060
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,73,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #061超大单净流入
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #062
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#063大单净流入
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #064
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#065中单净流入
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-21,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #066
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#067小单净流入
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-22,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #068
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-22,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #069大单净差
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-34,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #070
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-34,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#071五日大单净差
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-35,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #072
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-35,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#073十日大单净差
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-36,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #074
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-36,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),	
			#075主力动向
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-37,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #076
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#077五日主力动向
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-38,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #078
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#079十日主力动向
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-39,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #080
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-39,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #081涨跌动因
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-40,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #082
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-40,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#083五日涨跌动因
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-41,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #084
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-41,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#085十日涨跌动因
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-42,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #086
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#087主力净流入
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-47,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #088
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-47,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#089五分钟涨跌幅
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-48,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #090
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-48,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#0915日主力净流入
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-58,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #092
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-58,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#09310日主力净流入
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-59,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #094
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-59,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#9520日主力净流入
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-60,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #96
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-60,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#0975日主力净流入占比
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-61,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #098
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-61,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#09910日主力净流入占比
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-62,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #100
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-62,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#10120日主力净流入占比
        	json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-63,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #102
            json.dumps({
        		'id': 'SH1001',
        		'param': '0,100,-63,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#103代码
        	json.dumps({
        		'id': 'SH1002',
        		'param': '0,2000,1,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #104
            json.dumps({
        		'id': 'SH1002',
        		'param': '0,100,1,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #105交易状态
        	json.dumps({
        		'id': 'SH1002',
        		'param': '0,100,0,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #106
            json.dumps({
        		'id': 'SH1002',
        		'param': '0,100,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#107名称
        	json.dumps({
        		'id': 'SH1002',
        		'param': '0,100,2,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #108
            json.dumps({
        		'id': 'SH1002',
        		'param': '0,100,2,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),			
            #109昨收
        	json.dumps({
        		'id': 'SH1002',
        		'param': '0,100,11,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #110
            json.dumps({
        		'id': 'SH1002',
        		'param': '0,100,11,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #111开盘
        	json.dumps({
        		'id': 'SH1002',
        		'param': '0,100,10,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #112
            json.dumps({
        		'id': 'SH1002',
        		'param': '0,100,10,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #113最高
        	json.dumps({
        		'id': 'SH1100',
        		'param': '0,100,8,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #114
            json.dumps({
        		'id': 'SH1100',
        		'param': '0,100,8,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #115最低
        	json.dumps({
        		'id': 'SH1100',
        		'param': '0,100,9,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #116
            json.dumps({
        		'id': 'SH1100',
        		'param': '0,100,9,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #117最新
        	json.dumps({
        		'id': 'SH1300',
        		'param': '0,100,7,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #118
            json.dumps({
        		'id': 'SH1300',
        		'param': '0,100,7,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			 #119涨跌
        	json.dumps({
        		'id': 'SH1300',
        		'param': '0,100,19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #120
            json.dumps({
        		'id': 'SH1300',
        		'param': '0,100,19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #121涨跌幅
        	json.dumps({
        		'id': 'SH1300',
        		'param': '0,100,-3,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #122 
            json.dumps({
        		'id': 'SH1300',
        		'param': '0,100,-3,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #123成交量
        	json.dumps({
        		'id': 'SH1311',
        		'param': '0,100,13,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #124
            json.dumps({
        		'id': 'SH1311',
        		'param': '0,100,13,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #125成交额
        	json.dumps({
        		'id': 'SH1311',
        		'param': '0,100,20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #126
            json.dumps({
        		'id': 'SH1311',
        		'param': '0,100,20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #127当前成交量
        	json.dumps({
        		'id': 'SH1311',
        		'param': '0,100,14,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #128
            json.dumps({
        		'id': 'SH1311',
        		'param': '0,100,14,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#129换手率
        	json.dumps({
        		'id': 'SH1311',
        		'param': '0,100,15,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #130
            json.dumps({
        		'id': 'SH1311',
        		'param': '0,100,15,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#131量比
        	json.dumps({
        		'id': 'SH1312',
        		'param': '0,100,21,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #132
            json.dumps({
        		'id': 'SH1312',
        		'param': '0,100,21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#133内盘
        	json.dumps({
        		'id': 'SH1312',
        		'param': '0,100,25,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #134
            json.dumps({
        		'id': 'SH1312',
        		'param': '0,100,25,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #135外盘
        	json.dumps({
        		'id': 'SH3002',
        		'param': '0,100,24,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #136
            json.dumps({
        		'id': 'SH3002',
        		'param': '0,100,24,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#137总市值
        	json.dumps({
        		'id': 'SH3002',
        		'param': '0,100,26,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #138
            json.dumps({
        		'id': 'SH3002',
        		'param': '0,100,26,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#139流通市值
        	json.dumps({
        		'id': 'SH3002',
        		'param': '0,100,27,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #140
            json.dumps({
        		'id': 'SH3002',
        		'param': '0,100,27,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#141净资产
        	json.dumps({
        		'id': '000001.sh',
        		'param': '0,100,28,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #142
            json.dumps({
        		'id': '000001.sh',
        		'param': '0,100,28,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#143动态市盈率
        	json.dumps({
        		'id': '000001.sh',
        		'param': '0,100,29,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #144
            json.dumps({
        		'id': '000001.sh',
        		'param': '0,100,29,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			
            #145市净率
        	json.dumps({
        		'id': '000001.sh',
        		'param': '0,100,30,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #146
            json.dumps({
        		'id': '000001.sh',
        		'param': '0,100,30,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #147总股本
        	json.dumps({
        		'id': '000001.sh',
        		'param': '0,100,31,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #148
            json.dumps({
        		'id': '000001.sh',
        		'param': '0,100,31,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #149流通股
        	json.dumps({
        		'id': '000001.sh',
        		'param': '0,100,32,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #150
            json.dumps({
        		'id': '000001.sh',
        		'param': '0,100,32,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #151振幅比率
        	json.dumps({
        		'id': '000001.sh',
        		'param': '0,100,37,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #152
            json.dumps({
        		'id': '000001.sh',
        		'param': '0,100,37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #153动态每股收益
        	json.dumps({
        		'id': 'SH1006',
        		'param': '0,100,38,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #154
            json.dumps({
        		'id': 'SH1006',
        		'param': '0,100,38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#155委比
        	json.dumps({
        		'id': 'SH1006',
        		'param': '0,100,53,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #156
            json.dumps({
        		'id': 'SH1006',
        		'param': '0,100,53,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #157静态市盈率
        	json.dumps({
        		'id': 'SH1006',
        		'param': '0,100,42,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #158
            json.dumps({
        		'id': 'SH1006',
        		'param': '0,100,42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #159盘后成交量
        	json.dumps({
        		'id': 'SH1006',
        		'param': '0,100,72,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #160
            json.dumps({
        		'id': 'SH1006',
        		'param': '0,100,72,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #161盘后成交额
        	json.dumps({
        		'id': 'SH1006',
        		'param': '0,100,73,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #162
            json.dumps({
        		'id': 'SH1006',
        		'param': '0,100,73,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #163超大单净流入
        	json.dumps({
        		'id': 'SH1006',
        		'param': '0,100,-19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #164
            json.dumps({
        		'id': 'SH1006',
        		'param': '0,100,-19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#165大单净流入
        	json.dumps({
        		'id': 'SH1006',
        		'param': '0,100,-20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #166
            json.dumps({
        		'id': 'SH1006',
        		'param': '0,100,-20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#167中单净流入
        	json.dumps({
        		'id': 'SH1006',
        		'param': '0,100,-21,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #168
            json.dumps({
        		'id': 'SH1006',
        		'param': '0,100,-21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#169小单净流入
        	json.dumps({
        		'id': 'SH1006',
        		'param': '0,100,-22,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #170
            json.dumps({
        		'id': 'SH1006',
        		'param': '0,100,-22,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #171大单净差
        	json.dumps({
        		'id': 'SH1006',
        		'param': '0,100,-34,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #172
            json.dumps({
        		'id': 'SH1006',
        		'param': '0,100,-34,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#173五日大单净差
        	json.dumps({
        		'id': 'SH1006',
        		'param': '0,100,-35,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #174
            json.dumps({
        		'id': 'SH1006',
        		'param': '0,100,-35,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#175十日大单净差
        	json.dumps({
        		'id': 'SH1005',
        		'param': '0,100,-36,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #176
            json.dumps({
        		'id': 'SH1005',
        		'param': '0,100,-36,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),	
			#177主力动向
        	json.dumps({
        		'id': 'SH1005',
        		'param': '0,100,-37,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #178
            json.dumps({
        		'id': 'SH1005',
        		'param': '0,100,-37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#179五日主力动向
        	json.dumps({
        		'id': 'SH1005',
        		'param': '0,100,-38,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #180
            json.dumps({
        		'id': 'SH1005',
        		'param': '0,100,-38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#181十日主力动向
        	json.dumps({
        		'id': 'SH1005',
        		'param': '0,100,-39,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #182
            json.dumps({
        		'id': 'SH1005',
        		'param': '0,100,-39,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #183涨跌动因
        	json.dumps({
        		'id': 'SH1005',
        		'param': '0,100,-40,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #184
            json.dumps({
        		'id': 'SH1005',
        		'param': '0,100,-40,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#185五日涨跌动因
        	json.dumps({
        		'id': 'SH1005',
        		'param': '0,100,-41,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #186
            json.dumps({
        		'id': 'SH1005',
        		'param': '0,100,-41,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#187十日涨跌动因
        	json.dumps({
        		'id': 'SH1005',
        		'param': '0,100,-42,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #188
            json.dumps({
        		'id': 'SH1005',
        		'param': '0,100,-42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#189主力净流入
        	json.dumps({
        		'id': 'SH1005',
        		'param': '0,100,-47,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #190
            json.dumps({
        		'id': 'SH1005',
        		'param': '0,100,-47,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#191五分钟涨跌幅
        	json.dumps({
        		'id': 'SH1005',
        		'param': '0,100,-48,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #192
            json.dumps({
        		'id': 'SH1005',
        		'param': '0,100,-48,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#1935日主力净流入
        	json.dumps({
        		'id': 'SH1005',
        		'param': '0,100,-58,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #194
            json.dumps({
        		'id': 'SH1005',
        		'param': '0,100,-58,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#19510日主力净流入
        	json.dumps({
        		'id': 'SH1005',
        		'param': '0,100,-59,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #196
            json.dumps({
        		'id': 'SH1005',
        		'param': '0,100,-59,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#19720日主力净流入
        	json.dumps({
        		'id': 'SH1005',
        		'param': '0,100,-60,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #198
            json.dumps({
        		'id': 'SH1005',
        		'param': '0,100,-60,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#1995日主力净流入占比
        	json.dumps({
        		'id': 'SH1005',
        		'param': '0,100,-61,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #200
            json.dumps({
        		'id': 'SH1005',
        		'param': '0,100,-61,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#20110日主力净流入占比
        	json.dumps({
        		'id': 'SH1005',
        		'param': '0,100,-62,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #202
            json.dumps({
        		'id': 'SH1005',
        		'param': '0,100,-62,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#20320日主力净流入占比
        	json.dumps({
        		'id': 'SH1005',
        		'param': '0,100,-63,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #204
            json.dumps({
        		'id': 'SH1005',
        		'param': '0,100,-63,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#205代码
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,2000,1,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #206
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,1,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #207交易状态
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,0,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #208
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#209名称
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,2,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #210
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,2,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),			
            #211昨收
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,11,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #212
           json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,11,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #213开盘
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,10,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #214
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,10,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #215最高
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,8,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #216
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,8,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #217最低
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,9,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #218
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,9,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #219最新
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,7,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #220
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,7,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#221涨跌
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #222
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #223涨跌幅
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-3,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #224
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-3,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #225成交量
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,13,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #226
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,13,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #227成交额
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #228
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #229当前成交量
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,14,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #230
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,14,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#231换手率
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,15,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #232
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,15,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#233量比
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,21,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #234
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#235内盘
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,25,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #236
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,25,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #237外盘
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,24,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #238
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,24,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#239总市值
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,26,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #240
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,26,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#241流通市值
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,27,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #242
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,27,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#243净资产
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,28,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #244
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,28,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#245动态市盈率
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,29,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #246
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,29,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			
            #247市净率
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,30,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #248
           json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,30,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #249总股本
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,31,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #250
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,31,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #251流通股
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,32,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #252
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,32,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #253振幅比率
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,37,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #254
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #255动态每股收益
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,38,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #256
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			 #257委比
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,53,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #258
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,53,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #259静态市盈率
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,42,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #260
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #261超大单净流入
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #262
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#263大单净流入
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #264
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#265中单净流入
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-21,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #266
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#267小单净流入
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-22,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #268
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-22,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #269大单净差
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-34,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #270
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-34,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#271五日大单净差
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-35,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #272
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-35,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#273十日大单净差
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-36,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #274
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-36,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),	
			#275主力动向
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-37,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #276
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#277五日主力动向
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-38,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #278
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#279十日主力动向
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-39,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #280
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-39,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #281涨跌动因
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-40,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #282
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-40,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#283五日涨跌动因
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-41,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #284
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-41,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#285十日涨跌动因
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-42,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #286
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#287主力净流入
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-47,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #288
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-47,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#289五分钟涨跌幅
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-48,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #290
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-48,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#2915日主力净流入
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-58,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #292
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-58,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#29310日主力净流入
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-59,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #294
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-59,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#29520日主力净流入
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-60,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #296
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-60,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#2975日主力净流入占比
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-61,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #298
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-61,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#29910日主力净流入占比
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-62,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #300
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-62,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#30120日主力净流入占比
        	json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-63,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #302
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,-63,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#303代码
        	json.dumps({
        		'id': 'SZ1002',
        		'param': '0,2000,1,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #304
            json.dumps({
        		'id': 'SZ1002',
        		'param': '0,100,1,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #305交易状态
        	json.dumps({
        		'id': 'SZ1002',
        		'param': '0,100,0,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #306
            json.dumps({
        		'id': 'SZ1002',
        		'param': '0,100,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#307名称
        	json.dumps({
        		'id': 'SZ1002',
        		'param': '0,100,2,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #308
            json.dumps({
        		'id': 'SZ1002',
        		'param': '0,100,2,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),			
            #309昨收
        	json.dumps({
        		'id': 'SZ1002',
        		'param': '0,100,11,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #310
           json.dumps({
        		'id': 'SZ1002',
        		'param': '0,100,11,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #311开盘
        	json.dumps({
        		'id': 'SZ1002',
        		'param': '0,100,10,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #312
            json.dumps({
        		'id': 'SZ1002',
        		'param': '0,100,10,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #313最高
        	json.dumps({
        		'id': 'SZ1002',
        		'param': '0,100,8,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #314
            json.dumps({
        		'id': 'SZ1002',
        		'param': '0,100,8,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #315最低
        	json.dumps({
        		'id': 'SZ1002',
        		'param': '0,100,9,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #316
            json.dumps({
        		'id': 'SZ1002',
        		'param': '0,100,9,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #317最新
        	json.dumps({
        		'id': 'SZ1002',
        		'param': '0,100,7,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #318
            json.dumps({
        		'id': 'SZ1002',
        		'param': '0,100,7,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#319涨跌
        	json.dumps({
        		'id': 'SZ1002',
        		'param': '0,100,19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #320
            json.dumps({
        		'id': 'SZ1002',
        		'param': '0,100,19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #321涨跌幅
        	json.dumps({
        		'id': 'SZ1002',
        		'param': '0,100,-3,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #322
            json.dumps({
        		'id': 'SZ1003',
        		'param': '0,100,-3,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #323成交量
        	json.dumps({
        		'id': 'SZ1003',
        		'param': '0,100,13,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #324
            json.dumps({
        		'id': 'SZ1003',
        		'param': '0,100,13,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #325成交额
        	json.dumps({
        		'id': 'SZ1003',
        		'param': '0,100,20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #326
            json.dumps({
        		'id': 'SZ1003',
        		'param': '0,100,20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #327当前成交量
        	json.dumps({
        		'id': 'SZ1003',
        		'param': '0,100,14,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #328
            json.dumps({
        		'id': 'SZ1003',
        		'param': '0,100,14,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#329换手率
        	json.dumps({
        		'id': 'SZ1003',
        		'param': '0,100,15,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #330
            json.dumps({
        		'id': 'SZ1003',
        		'param': '0,100,15,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#331量比
        	json.dumps({
        		'id': 'SZ1003',
        		'param': '0,100,21,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #332
            json.dumps({
        		'id': 'SZ1003',
        		'param': '0,100,21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#333内盘
        	json.dumps({
        		'id': 'SZ1003',
        		'param': '0,100,25,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #334
            json.dumps({
        		'id': 'SZ1001',
        		'param': '0,100,25,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #335外盘
        	json.dumps({
        		'id': 'SZ1003',
        		'param': '0,100,24,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #336
            json.dumps({
        		'id': 'SZ1003',
        		'param': '0,100,24,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#337总市值
        	json.dumps({
        		'id': 'SZ1003',
        		'param': '0,100,26,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #338
            json.dumps({
        		'id': 'SZ1003',
        		'param': '0,100,26,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#339流通市值
        	json.dumps({
        		'id': 'SZ1003',
        		'param': '0,100,27,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #340
            json.dumps({
        		'id': 'SZ1003',
        		'param': '0,100,27,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#341净资产
        	json.dumps({
        		'id': 'SZ1003',
        		'param': '0,100,28,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #342
            json.dumps({
        		'id': 'SZ1003',
        		'param': '0,100,28,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#343动态市盈率
        	json.dumps({
        		'id': 'SZ1100',
        		'param': '0,100,29,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #344
            json.dumps({
        		'id': 'SZ1100',
        		'param': '0,100,29,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			
            #345市净率
        	json.dumps({
        		'id': 'SZ1100',
        		'param': '0,100,30,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #346
           json.dumps({
        		'id': 'SZ1100',
        		'param': '0,100,30,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #347总股本
        	json.dumps({
        		'id': 'SZ1100',
        		'param': '0,100,31,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #348
            json.dumps({
        		'id': 'SZ1100',
        		'param': '0,100,31,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #349流通股
        	json.dumps({
        		'id': 'SZ1300',
        		'param': '0,100,32,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #350
            json.dumps({
        		'id': 'SZ1300',
        		'param': '0,100,32,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #351振幅比率
        	json.dumps({
        		'id': 'SZ1300',
        		'param': '0,100,37,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #352
            json.dumps({
        		'id': 'SZ1300',
        		'param': '0,100,37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #353动态每股收益
        	json.dumps({
        		'id': 'SZ1300',
        		'param': '0,100,38,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #354
            json.dumps({
        		'id': 'SZ1300',
        		'param': '0,100,38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#355委比
        	json.dumps({
        		'id': 'SZ1300',
        		'param': '0,100,53,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #356
            json.dumps({
        		'id': 'SZ1300',
        		'param': '0,100,53,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #357静态市盈率
        	json.dumps({
        		'id': 'SZ1300',
        		'param': '0,100,42,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #358
            json.dumps({
        		'id': 'SZ1300',
        		'param': '0,100,42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #359超大单净流入
        	json.dumps({
        		'id': 'SZ1005',
        		'param': '0,100,-19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #360
            json.dumps({
        		'id': 'SZ1005',
        		'param': '0,100,-19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#361大单净流入
        	json.dumps({
        		'id': 'SZ1005',
        		'param': '0,100,-20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #362
            json.dumps({
        		'id': 'SZ1005',
        		'param': '0,100,-20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#363中单净流入
        	json.dumps({
        		'id': 'SZ1005',
        		'param': '0,100,-21,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #364
            json.dumps({
        		'id': 'SZ1005',
        		'param': '0,100,-21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#365小单净流入
        	json.dumps({
        		'id': 'SZ1005',
        		'param': '0,100,-22,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #366
            json.dumps({
        		'id': 'SZ1005',
        		'param': '0,100,-22,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #367大单净差
        	json.dumps({
        		'id': 'SZ1005',
        		'param': '0,100,-34,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #368
            json.dumps({
        		'id': 'SZ1005',
        		'param': '0,100,-34,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#369五日大单净差
        	json.dumps({
        		'id': 'SZ1005',
        		'param': '0,100,-35,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #370
            json.dumps({
        		'id': 'SZ1005',
        		'param': '0,100,-35,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#371十日大单净差
        	json.dumps({
        		'id': 'SZ1005',
        		'param': '0,100,-36,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #372
            json.dumps({
        		'id': 'SZ1005',
        		'param': '0,100,-36,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),	
			#373主力动向
        	json.dumps({
        		'id': 'SZ1005',
        		'param': '0,100,-37,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #374
            json.dumps({
        		'id': 'SZ1005',
        		'param': '0,100,-37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#375五日主力动向
        	json.dumps({
        		'id': 'SZ1005',
        		'param': '0,100,-38,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #376
            json.dumps({
        		'id': 'SZ1005',
        		'param': '0,100,-38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#377十日主力动向
        	json.dumps({
        		'id': 'SZ1005',
        		'param': '0,100,-39,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #378
            json.dumps({
        		'id': 'SZ1005',
        		'param': '0,100,-39,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #379涨跌动因
        	json.dumps({
        		'id': 'SZ1004',
        		'param': '0,100,-40,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #380
            json.dumps({
        		'id': 'SZ1004',
        		'param': '0,100,-40,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#381五日涨跌动因
        	json.dumps({
        		'id': 'SZ1004',
        		'param': '0,100,-41,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #382
            json.dumps({
        		'id': 'SZ1004',
        		'param': '0,100,-41,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#383十日涨跌动因
        	json.dumps({
        		'id': 'SZ1004',
        		'param': '0,100,-42,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #384
            json.dumps({
        		'id': 'SZ1004',
        		'param': '0,100,-42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#385主力净流入
        	json.dumps({
        		'id': 'SZ1004',
        		'param': '0,100,-47,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #386
            json.dumps({
        		'id': 'SZ1004',
        		'param': '0,100,-47,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#387五分钟涨跌幅
        	json.dumps({
        		'id': 'SZ1004',
        		'param': '0,100,-48,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #388
            json.dumps({
        		'id': 'SZ1004',
        		'param': '0,100,-48,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#3895日主力净流入
        	json.dumps({
        		'id': 'SZ1004',
        		'param': '0,100,-58,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #390
            json.dumps({
        		'id': 'SZ1004',
        		'param': '0,100,-58,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#39110日主力净流入
        	json.dumps({
        		'id': 'SZ1004',
        		'param': '0,100,-59,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #392
            json.dumps({
        		'id': 'SZ1004',
        		'param': '0,100,-59,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#39320日主力净流入
        	json.dumps({
        		'id': 'SZ1004',
        		'param': '0,100,-60,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #394
            json.dumps({
        		'id': 'SZ1004',
        		'param': '0,100,-60,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#3955日主力净流入占比
        	json.dumps({
        		'id': 'SZ1004',
        		'param': '0,100,-61,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #396
            json.dumps({
        		'id': 'SZ1004',
        		'param': '0,100,-61,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#39710日主力净流入占比
        	json.dumps({
        		'id': 'SZ1004',
        		'param': '0,100,-62,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #398
            json.dumps({
        		'id': 'SZ1004',
        		'param': '0,100,-62,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#39920日主力净流入占比
        	json.dumps({
        		'id': 'SZ1004',
        		'param': '0,100,-63,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #400
            json.dumps({
        		'id': 'SZ1004',
        		'param': '0,100,-63,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#401代码
        	json.dumps({
        		'id': 'SHSZ1001',
        		'param': '0,2000,1,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #402
            json.dumps({
        		'id': 'SHSZ1001',
        		'param': '0,100,1,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #403交易状态
        	json.dumps({
        		'id': 'SHSZ1001',
        		'param': '0,100,0,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #404
            json.dumps({
        		'id': 'SHSZ1001',
        		'param': '0,100,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#405名称
        	json.dumps({
        		'id': 'SHSZ1001',
        		'param': '0,100,2,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #406
            json.dumps({
        		'id': 'SHSZ1001',
        		'param': '0,100,2,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),			
            #407昨收
        	json.dumps({
        		'id': 'SHSZ1001',
        		'param': '0,100,11,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #408
           json.dumps({
        		'id': 'SHSZ1001',
        		'param': '0,100,11,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),	
        ])
        case_list.append(case_conf)
		#......................................港澳.....................
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'CATESORTING_2'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
			#001代码
        	json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,1,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #002
            json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,1,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #003交易状态
        	json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,0,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #004
            json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#005名称
        	json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,2,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #006
            json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,2,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),			
            #007昨收
        	json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,11,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #008
            json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,11,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #009开盘
        	json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,10,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #010
            json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,10,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #011最高
        	json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,8,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #012
            json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,8,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #013最低
        	json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,9,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #014
            json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,9,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #015最新
        	json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,7,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #016
            json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,7,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			 #017涨跌
        	json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #018
            json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #019涨跌幅
        	json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,-3,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #020 
            json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,-3,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #021成交量
        	json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,13,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #022
            json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,13,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #023成交额
        	json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #024
            json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #025当前成交量
        	json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,14,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #026
            json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,14,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#027换手率
        	json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,15,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #028
            json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,15,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#029量比
        	json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,21,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #030
            json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#031内盘
        	json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,25,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #032
            json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,25,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #033外盘
        	json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,24,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #034
            json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,24,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#035总市值
        	json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,26,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #036
            json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,26,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#037流通市值
        	json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,27,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #038
            json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,27,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#039净资产
        	json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,28,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #040
            json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,28,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#041动态市盈率
        	json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,29,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #042
            json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,29,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),			
            #043市净率
        	json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,30,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #044
            json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,30,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #045总股本
        	json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,31,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #046
            json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,31,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #047流通股
        	json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,32,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #048
            json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,32,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #049振幅比率
        	json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,37,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #050
            json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #051动态每股收益
        	json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,38,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #052
            json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			 #053委比
        	json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,53,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #054
            json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,53,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #055静态市盈率
        	json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,42,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #056 
            json.dumps({
        		'id': 'HK1010',
        		'param': '0,100,42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #057昨收
        	json.dumps({
        		'id': 'HK1000',
        		'param': '0,100,11,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #058
            json.dumps({
        		'id': 'HK1000',
        		'param': '0,100,11,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #059开盘
        	json.dumps({
        		'id': 'HK1000',
        		'param': '0,100,10,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #060
            json.dumps({
        		'id': 'HK1000',
        		'param': '0,100,10,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #061最高
        	json.dumps({
        		'id': 'HK1004',
        		'param': '0,100,8,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #062
            json.dumps({
        		'id': 'HK1004',
        		'param': '0,100,8,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #063最低
        	json.dumps({
        		'id': 'HK1004',
        		'param': '0,100,9,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #064
            json.dumps({
        		'id': 'HK1004',
        		'param': '0,100,9,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #065最新
        	json.dumps({
        		'id': 'HK1100',
        		'param': '0,100,7,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #066
            json.dumps({
        		'id': 'HK1100',
        		'param': '0,100,7,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			 #067涨跌
        	json.dumps({
        		'id': 'HK1100',
        		'param': '0,100,19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #068
            json.dumps({
        		'id': 'HK1100',
        		'param': '0,100,19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #069涨跌幅
        	json.dumps({
        		'id': 'HK1300',
        		'param': '0,100,-3,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #070 
            json.dumps({
        		'id': 'HK1300',
        		'param': '0,100,-3,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #071成交量
        	json.dumps({
        		'id': 'HK1300',
        		'param': '0,100,13,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #072
            json.dumps({
        		'id': 'HK1300',
        		'param': '0,100,13,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #073成交额
        	json.dumps({
        		'id': 'HK1300',
        		'param': '0,100,20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #074
            json.dumps({
        		'id': 'HK1300',
        		'param': '0,100,20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #075当前成交量
        	json.dumps({
        		'id': 'HSI.hk',
        		'param': '0,100,14,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #076
            json.dumps({
        		'id': 'HSI.hk',
        		'param': '0,100,14,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#077换手率
        	json.dumps({
        		'id': 'HSI.hk',
        		'param': '0,100,15,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #078
            json.dumps({
        		'id': 'HSI.hk',
        		'param': '0,100,15,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#079量比
        	json.dumps({
        		'id': 'HSI.hk',
        		'param': '0,100,21,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #080
            json.dumps({
        		'id': 'HSI.hk',
        		'param': '0,100,21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#081内盘
        	json.dumps({
        		'id': 'HK1500',
        		'param': '0,100,25,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #082
            json.dumps({
        		'id': 'HK1500',
        		'param': '0,100,25,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #083外盘
        	json.dumps({
        		'id': 'HK1500',
        		'param': '0,100,24,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #084
            json.dumps({
        		'id': 'HK1500',
        		'param': '0,100,24,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#085总市值
        	json.dumps({
        		'id': 'HK1500',
        		'param': '0,100,26,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #086
            json.dumps({
        		'id': 'HK1500',
        		'param': '0,100,26,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#087流通市值
        	json.dumps({
        		'id': 'HK1500',
        		'param': '0,100,27,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #088
            json.dumps({
        		'id': 'HK1500',
        		'param': '0,100,27,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#089净资产
        	json.dumps({
        		'id': 'HK1600',
        		'param': '0,100,28,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #090
            json.dumps({
        		'id': 'HK1600',
        		'param': '0,100,28,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#091动态市盈率
        	json.dumps({
        		'id': 'HK1600',
        		'param': '0,100,29,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #092
            json.dumps({
        		'id': 'HK1600',
        		'param': '0,100,29,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			
            #093市净率
        	json.dumps({
        		'id': 'HK1600',
        		'param': '0,100,30,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #094
            json.dumps({
        		'id': 'HK1600',
        		'param': '0,100,30,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #095总股本
        	json.dumps({
        		'id': 'HK1600',
        		'param': '0,100,31,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #096
            json.dumps({
        		'id': 'HK1600',
        		'param': '0,100,31,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #097流通股
        	json.dumps({
        		'id': 'HK1600',
        		'param': '0,100,32,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #098
            json.dumps({
        		'id': 'HK1600',
        		'param': '0,100,32,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #099振幅比率
        	json.dumps({
        		'id': 'HKAHG',
        		'param': '0,100,37,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #100
            json.dumps({
        		'id': 'HKAHG',
        		'param': '0,100,37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #101动态每股收益
        	json.dumps({
        		'id': 'HKGQ',
        		'param': '0,100,38,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #102
            json.dumps({
        		'id': 'HKGQ',
        		'param': '0,100,38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#103委比
        	json.dumps({
        		'id': 'HKLC',
        		'param': '0,100,53,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #104
            json.dumps({
        		'id': 'HKLC',
        		'param': '0,100,53,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #105静态市盈率
        	json.dumps({
        		'id': 'HKHC',
        		'param': '0,100,42,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #106
            json.dumps({
        		'id': 'HKHC',
        		'param': '0,100,42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#107成交额
        	json.dumps({
        		'id': 'HSI',
        		'param': '0,100,20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#108成交额
        	json.dumps({
        		'id': 'HSI',
        		'param': '0,100,20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#107成交额
        	json.dumps({
        		'id': 'SHHGT',
        		'param': '0,100,20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#108成交额
        	json.dumps({
        		'id': 'SHHGT',
        		'param': '0,100,20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#107成交额
        	json.dumps({
        		'id': 'SZSGT',
        		'param': '0,100,20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#108成交额
        	json.dumps({
        		'id': 'SZSGT',
        		'param': '0,100,20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#107成交额
        	json.dumps({
        		'id': 'HKGGT',
        		'param': '0,100,20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#108成交额
        	json.dumps({
        		'id': 'HKGGT',
        		'param': '0,100,20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
        ])
        case_list.append(case_conf)
        #......................................板块指数.....................
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'CATESORTING_2'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
			#001代码
        	json.dumps({
        		'id': 'E00104.bk',
        		'param': '0,2000,1,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #002
            json.dumps({
        		'id': 'E00104.bk',
        		'param': '0,100,1,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #003交易状态
        	json.dumps({
        		'id': 'E00104.bk',
        		'param': '0,100,0,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #004
            json.dumps({
        		'id': 'E00104.bk',
        		'param': '0,100,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#005名称
        	json.dumps({
        		'id': 'E00104.bk',
        		'param': '0,100,2,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #006
            json.dumps({
        		'id': 'E00104.bk',
        		'param': '0,100,2,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),			
            #007昨收
        	json.dumps({
        		'id': 'E00104.bk',
        		'param': '0,100,11,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #008
           json.dumps({
        		'id': 'E00104.bk',
        		'param': '0,100,11,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #009开盘
        	json.dumps({
        		'id': 'F10014.bk',
        		'param': '0,100,10,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #010
            json.dumps({
        		'id': 'F10014.bk',
        		'param': '0,100,10,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #011最高
        	json.dumps({
        		'id': 'F10014.bk',
        		'param': '0,100,8,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #012
            json.dumps({
        		'id': 'F10014.bk',
        		'param': '0,100,8,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #013最低
        	json.dumps({
        		'id': 'F10014.bk',
        		'param': '0,100,9,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #014
            json.dumps({
        		'id': 'F10014.bk',
        		'param': '0,100,9,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #015最新
        	json.dumps({
        		'id': 'F10014.bk',
        		'param': '0,100,7,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #016
            json.dumps({
        		'id': 'F10014.bk',
        		'param': '0,100,7,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#017涨跌
        	json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #018
            json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #019涨跌幅
        	json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-3,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #020 
            json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-3,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #021成交量
        	json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,13,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #022
            json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,13,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #023成交额
        	json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #024
            json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #025当前成交量
        	json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,14,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #026
            json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,14,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#027换手率
        	json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,15,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #028
            json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,15,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#029量比
        	json.dumps({
        		'id': 'D20085.bk',
        		'param': '0,100,21,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #030
            json.dumps({
        		'id': 'D20085.bk',
        		'param': '0,100,21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#031内盘
        	json.dumps({
        		'id': 'D20085.bk',
        		'param': '0,100,25,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #032
            json.dumps({
        		'id': 'D20085.bk',
        		'param': '0,100,25,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #033外盘
        	json.dumps({
        		'id': 'D20085.bk',
        		'param': '0,100,24,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #034
            json.dumps({
        		'id': 'D20085.bk',
        		'param': '0,100,24,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#035总市值
        	json.dumps({
        		'id': 'D20085.bk',
        		'param': '0,100,26,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #036
            json.dumps({
        		'id': 'D20085.bk',
        		'param': '0,100,26,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#037流通市值
        	json.dumps({
        		'id': 'D20085.bk',
        		'param': '0,100,27,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #038
            json.dumps({
        		'id': 'D20085.bk',
        		'param': '0,100,27,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#039净资产
        	json.dumps({
        		'id': 'D10010.bk',
        		'param': '0,100,28,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #040
            json.dumps({
        		'id': 'D10010.bk',
        		'param': '0,100,28,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#041动态市盈率
        	json.dumps({
        		'id': 'D10010.bk',
        		'param': '0,100,29,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #042
            json.dumps({
        		'id': 'D10010.bk',
        		'param': '0,100,29,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),			
            #043市净率
        	json.dumps({
        		'id': 'D10010.bk',
        		'param': '0,100,30,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #044
           json.dumps({
        		'id': 'D10010.bk',
        		'param': '0,100,30,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #045总股本
        	json.dumps({
        		'id': 'D10010.bk',
        		'param': '0,100,31,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #046
            json.dumps({
        		'id': 'D10010.bk',
        		'param': '0,100,31,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #047流通股
        	json.dumps({
        		'id': 'D10010.bk',
        		'param': '0,100,32,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #048
            json.dumps({
        		'id': 'D10010.bk',
        		'param': '0,100,32,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #049振幅比率
        	json.dumps({
        		'id': 'G10015.bk',
        		'param': '0,100,37,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #050
            json.dumps({
        		'id': 'G10015.bk',
        		'param': '0,100,37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #051动态每股收益
        	json.dumps({
        		'id': 'G10015.bk',
        		'param': '0,100,38,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #052
            json.dumps({
        		'id': 'G10015.bk',
        		'param': '0,100,38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#053委比
        	json.dumps({
        		'id': 'G10015.bk',
        		'param': '0,100,53,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #054
            json.dumps({
        		'id': 'G10015.bk',
        		'param': '0,100,53,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #055静态市盈率
        	json.dumps({
        		'id': 'G10015.bk',
        		'param': '0,100,42,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #056 
            json.dumps({
        		'id': 'G10015.bk',
        		'param': '0,100,42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #057盘后成交量
        	json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,72,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #058
            json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,72,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #059盘后成交额
        	json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,73,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #060
            json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,73,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #061超大单净流入
        	json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #062
            json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#063大单净流入
        	json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #064
            json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#065中单净流入
        	json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-21,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #066
            json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#067小单净流入
        	json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-22,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #068
            json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-22,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #069大单净差
        	json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-34,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #070
            json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-34,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#071五日大单净差
        	json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-35,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #072
            json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-35,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#073十日大单净差
        	json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-36,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #074
            json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-36,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),	
			#075主力动向
        	json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-37,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #076
            json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#077五日主力动向
        	json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-38,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #078
            json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#079十日主力动向
        	json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-39,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #080
            json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-39,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #081涨跌动因
        	json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-40,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #082
            json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-40,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#083五日涨跌动因
        	json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-41,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #084
            json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-41,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#085十日涨跌动因
        	json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-42,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #086
            json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#087主力净流入
        	json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-47,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #088
            json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-47,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#089五分钟涨跌幅
        	json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-48,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #090
            json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-48,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#0915日主力净流入
        	json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-58,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #092
            json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-58,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#09310日主力净流入
        	json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-59,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #094
            json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-59,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#9520日主力净流入
        	json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-60,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #96
            json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-60,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#0975日主力净流入占比
        	json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-61,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #098
            json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-61,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#09910日主力净流入占比
        	json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-62,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #100
            json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-62,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#10120日主力净流入占比
        	json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-63,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #102
            json.dumps({
        		'id': 'A20033.bk',
        		'param': '0,100,-63,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
        ])
        case_list.append(case_conf)
        #.....................................期货........................
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'CATESORTING_2'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
			#001代码
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,1,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #002
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,1,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#003交易状态
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,0,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #004
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #005名称
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,2,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #006
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,2,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #007昨收
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,11,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #008
           json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,11,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #009开盘
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,10,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #010
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,10,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #011最高
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,8,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #012
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,8,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #013最低
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,9,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #014
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,9,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #015最新
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,7,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #016
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,7,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #017均价
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,18,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #018
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,18,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #019涨跌
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #020
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #021涨跌幅
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,-3,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #022 
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,-3,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #023成交量
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,13,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #024
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,13,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #025成交额
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #026
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #027当前成交量
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,14,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #028
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,14,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#029换手率
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,15,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #030
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,15,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#031量比
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,21,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #032
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #033内盘
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,25,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #034
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,25,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #035外盘
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,24,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #036
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,24,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#037总市值
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,26,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #038
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,26,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#039流通市值
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,27,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #040
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,27,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#041净资产
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,28,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #042
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,28,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#043动态市盈率
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,29,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #044
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,29,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),			
            #045市净率
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,30,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #046
           json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,30,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #047总股本
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,31,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #048
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,31,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #049流通股
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,32,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #050
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,32,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #051振幅比率
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,37,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #052
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #053动态每股收益
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,38,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #054
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #055静态市盈率
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,42,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #056 
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #057交易日
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,119,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #058
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,119,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			 #059委比
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,53,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #060
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,53,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#061交易日
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,119,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #062
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,119,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #063结算组代码
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,120,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #064
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,120,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #065结算编号
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,121,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #066
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,121,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #067昨结
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,68,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #068
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,68,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #069昨持仓
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,123,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #070
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,123,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #071持仓
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,124,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #072
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,124,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #073日增
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,125,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #074
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,125,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #075今收盘
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,126,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #076
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,126,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #077今结算
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,127,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #078
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,127,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #079昨虚
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,100,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #080
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,100,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #081今虚
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,101,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #082
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,101,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #083最后修改毫秒
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,102,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #084
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,102,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			 #085涨停
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,16,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #086
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,16,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #087跌停
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,17,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #088
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,17,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#089买一价
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,22,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #090
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,22,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #091卖一价
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,23,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #092
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,23,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #093标的现价
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,103,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #094
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,103,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #095标的昨收
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,104,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #096
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,104,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #097标的涨跌
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,105,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #098
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,105,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #099标的名称
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,2,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #100
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,2,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #101change1
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,107,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #102
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,107,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #103仓差
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,108,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #104
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,108,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#105委买
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,108,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #106
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,108,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#107委卖
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,108,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #108
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,108,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),				
            #109委差
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,54,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #110
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,54,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),	
            #111交割点数
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,117,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #112
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,117,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),	
            #113行权价
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,110,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #114
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,110,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #115溢价率
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,111,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #116
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,111,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}), 
			#117剩余天数
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,112,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #118
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,112,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #119杠杆比率
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,116,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #120
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,116,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #121隐含波动率
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,113,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #122
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,113,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #123无风险利率
        	json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,114,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #124
            json.dumps({
        		'id': 'DCE_ALL',
        		'param': '0,100,114,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#125代码
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,1,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #126
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,1,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#127交易状态
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,0,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #128
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #129名称
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,2,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #130
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,2,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #131昨收
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,11,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #132
           json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,11,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #133开盘
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,10,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #134
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,10,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #135最高
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,8,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #136
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,8,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #137最低
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,9,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #138
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,9,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #139最新
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,7,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #140
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,7,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #141均价
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,18,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #142
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,18,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #143涨跌
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #144
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #145涨跌幅
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,-3,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #146 
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,-3,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #147成交量
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,13,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #148
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,13,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #149成交额
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #150
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #151当前成交量
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,14,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #152
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,14,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#153换手率
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,15,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #154
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,15,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#155量比
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,21,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #156
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #157内盘
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,25,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #158
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,25,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #159外盘
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,24,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #160
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,24,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#161总市值
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,26,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #162
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,26,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#163流通市值
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,27,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #164
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,27,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#165净资产
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,28,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #166
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,28,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#167动态市盈率
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,29,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #168
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,29,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),			
            #169市净率
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,30,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #170
           json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,30,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #171总股本
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,31,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #172
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,31,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #173流通股
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,32,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #174
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,32,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #175振幅比率
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,37,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #176
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #177动态每股收益
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,38,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #178
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #179静态市盈率
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,42,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #180
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #181交易日
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,119,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #182
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,119,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			 #183委比
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,53,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #184
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,53,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#185交易日
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,119,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #186
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,119,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #187结算组代码
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,120,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #188
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,120,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #189结算编号
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,121,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #190
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,121,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #191昨结
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,68,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #192
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,68,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #193昨持仓
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,123,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #194
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,123,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #195持仓
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,124,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #196
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,124,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #197日增
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,125,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #198
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,125,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #199今收盘
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,126,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #200
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,126,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #201今结算
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,127,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #202
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,127,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #203昨虚
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,100,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #204
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,100,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #205今虚
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,101,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #206
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,101,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #207最后修改毫秒
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,102,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #208
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,102,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			 #209涨停
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,16,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #210
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,16,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #211跌停
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,17,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #212
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,17,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#213买一价
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,22,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #214
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,22,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #215卖一价
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,23,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #216
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,23,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #217标的现价
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,103,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #218
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,103,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #219标的昨收
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,104,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #220
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,104,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #221标的涨跌
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,105,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #222
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,105,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #223标的名称
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,2,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #224
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,2,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #225change1
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,107,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #226
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,107,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #227仓差
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,108,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #228
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,108,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#229委买
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,108,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #230
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,108,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#231委卖
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,108,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #232
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,108,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),				
            #233委差
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,54,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #234
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,54,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),	
            #235交割点数
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,117,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #236
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,117,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),	
            #237行权价
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,110,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #238
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,110,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #239溢价率
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,111,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #240
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,111,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}), 
			#241剩余天数
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,112,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #242
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,112,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #243杠杆比率
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,116,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #244
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,116,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #245隐含波动率
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,113,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #246
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,113,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #247无风险利率
        	json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,114,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #248
            json.dumps({
        		'id': 'CZCE_ALL',
        		'param': '0,100,114,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#249代码
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,1,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #250
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,1,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#251交易状态
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,0,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #252
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #253名称
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,2,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #254
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,2,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #255昨收
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,11,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #256
           json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,11,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #257开盘
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,10,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #258
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,10,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #259最高
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,8,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #260
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,8,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #261最低
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,9,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #262
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,9,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #263最新
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,7,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #264
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,7,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #265均价
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,18,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #266
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,18,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #267涨跌
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #268
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #269涨跌幅
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,-3,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #270 
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,-3,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #271成交量
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,13,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #272
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,13,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #273成交额
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #274
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #275当前成交量
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,14,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #276
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,14,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#277换手率
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,15,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #278
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,15,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#279量比
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,21,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #280
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #281内盘
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,25,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #282
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,25,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #283外盘
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,24,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #284
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,24,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#285总市值
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,26,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #286
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,26,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#287流通市值
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,27,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #288
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,27,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#289净资产
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,28,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #290
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,28,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#291动态市盈率
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,29,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #292
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,29,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),			
            #293市净率
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,30,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #294
           json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,30,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #295总股本
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,31,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #296
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,31,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #297流通股
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,32,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #298
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,32,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #299振幅比率
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,37,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #300
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #301动态每股收益
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,38,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #302
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #303静态市盈率
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,42,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #304
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #305交易日
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,119,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #306
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,119,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#307委比
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,53,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #308
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,53,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#309交易日
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,119,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #310
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,119,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #311结算组代码
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,120,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #312
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,120,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #313结算编号
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,121,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #314
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,121,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #315昨结
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,68,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #316
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,68,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #317昨持仓
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,123,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #318
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,123,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #319持仓
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,124,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #320
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,124,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #321日增
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,125,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #322
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,125,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #323今收盘
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,126,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #324
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,126,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #325今结算
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,127,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #326
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,127,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #327昨虚
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,100,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #328
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,100,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #329今虚
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,101,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #330
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,101,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #331最后修改毫秒
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,102,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #332
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,102,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#333涨停
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,16,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #334
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,16,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #335跌停
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,17,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #336
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,17,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#337买一价
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,22,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #338
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,22,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #339卖一价
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,23,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #340
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,23,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #341标的现价
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,103,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #342
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,103,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #343标的昨收
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,104,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #344
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,104,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #345标的涨跌
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,105,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #346
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,105,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #347标的名称
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,2,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #348
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,2,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #349change1
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,107,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #350
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,107,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #351仓差
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,108,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #352
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,108,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#353委买
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,108,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #354
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,108,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#355委卖
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,108,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #356
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,108,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),				
            #357委差
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,54,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #358
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,54,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),	
            #359交割点数
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,117,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #360
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,117,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),	
            #361行权价
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,110,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #362
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,110,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #363溢价率
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,111,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #364
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,111,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}), 
			#365剩余天数
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,112,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #366
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,112,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #367杠杆比率
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,116,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #368
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,116,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #369隐含波动率
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,113,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #370
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,113,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #371无风险利率
        	json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,114,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #372
            json.dumps({
        		'id': 'SHFE_ALL',
        		'param': '0,100,114,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#373代码
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,1,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #374
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,1,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#375交易状态
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,0,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #376
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #377名称
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,2,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #378
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,2,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #379昨收
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,11,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #380
           json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,11,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #开盘
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,10,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,10,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #最高
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,8,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,8,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #最低
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,9,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,9,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #最新
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,7,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,7,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #389均价
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,18,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,18,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #涨跌
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #涨跌幅
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,-3,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            # 
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,-3,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #成交量
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,13,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #272
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,13,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #成交额
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #274
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #当前成交量
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,14,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #276
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,14,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#401换手率
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,15,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,15,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#量比
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,21,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #内盘
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,25,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,25,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #外盘
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,24,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,24,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#总市值
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,26,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,26,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#流通市值
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,27,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,27,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#净资产
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,28,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,28,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#415动态市盈率
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,29,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,29,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),			
            #市净率
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,30,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
           json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,30,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #总股本
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,31,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,31,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #流通股
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,32,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,32,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #振幅比率
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,37,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #动态每股收益
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,38,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #静态市盈率
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,42,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #交易日
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,119,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,119,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#委比
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,53,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,53,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#交易日
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,119,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,119,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #435结算组代码
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,120,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,120,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #结算编号
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,121,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,121,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #昨结
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,68,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,68,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #昨持仓
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,123,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,123,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #持仓
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,124,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,124,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #445日增
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,125,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,125,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #今收盘
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,126,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,126,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #今结算
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,127,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,127,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #昨虚
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,100,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,100,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #今虚
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,101,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,101,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #455最后修改毫秒
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,102,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,102,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#涨停
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,16,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,16,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #跌停
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,17,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,17,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#买一价
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,22,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,22,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #卖一价
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,23,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,23,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #标的现价
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,103,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,103,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #467标的昨收
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,104,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,104,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #标的涨跌
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,105,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,105,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #标的名称
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,2,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,2,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #change1
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,107,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,107,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #仓差
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,108,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,108,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#委买
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,108,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,108,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#479委卖
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,108,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,108,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),				
            #委差
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,54,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,54,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),	
            #交割点数
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,117,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,117,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),	
            #行权价
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,110,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,110,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #溢价率
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,111,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,111,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}), 
			#489剩余天数
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,112,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,112,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #杠杆比率
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,116,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,116,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #隐含波动率
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,113,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,113,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #495无风险利率
        	json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,114,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #496
            json.dumps({
        		'id': 'INE_ALL',
        		'param': '0,100,114,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#497代码
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,1,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #498
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,1,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#499交易状态
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,0,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #500
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #501名称
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,2,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #502
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,2,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #503昨收
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,11,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #504
           json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,11,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #505开盘
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,10,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #506
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,10,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #507最高
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,8,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #508
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,8,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #509最低
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,9,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #510
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,9,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #最新
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,7,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,7,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #513均价
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,18,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,18,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #涨跌
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #涨跌幅
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,-3,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            # 
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,-3,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #成交量
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,13,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,13,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #成交额
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #当前成交量
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,14,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,14,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#525换手率
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,15,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,15,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#量比
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,21,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #内盘
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,25,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,25,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #外盘
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,24,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,24,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#总市值
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,26,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,26,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#流通市值
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,27,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,27,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#净资产
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,28,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,28,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#539动态市盈率
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,29,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,29,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),			
            #市净率
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,30,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
           json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,30,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #总股本
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,31,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,31,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #流通股
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,32,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,32,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #振幅比率
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,37,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #动态每股收益
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,38,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #静态市盈率
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,42,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #交易日
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,119,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,119,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#委比
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,53,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,53,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#交易日
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,119,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,119,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #559结算组代码
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,120,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,120,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #结算编号
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,121,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,121,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #昨结
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,68,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,68,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #昨持仓
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,123,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,123,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #持仓
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,124,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,124,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #日增
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,125,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,125,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #今收盘
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,126,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,126,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #今结算
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,127,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,127,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #昨虚
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,100,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,100,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #今虚
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,101,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,101,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #579最后修改毫秒
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,102,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,102,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#涨停
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,16,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,16,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #跌停
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,17,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,17,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#买一价
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,22,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,22,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #卖一价
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,23,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,23,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #标的现价
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,103,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,103,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #467标的昨收
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,104,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,104,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #标的涨跌
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,105,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,105,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #标的名称
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,2,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,2,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #change1
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,107,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,107,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #仓差
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,108,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,108,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#委买
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,108,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,108,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#603委卖
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,108,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,108,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),				
            #委差
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,54,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,54,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),	
            #交割点数
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,117,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,117,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),	
            #行权价
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,110,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,110,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #溢价率
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,111,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,111,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}), 
			#613剩余天数
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,112,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,112,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #杠杆比率
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,116,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,116,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #隐含波动率
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,113,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,113,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #619无风险利率
        	json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,114,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #620
            json.dumps({
        		'id': 'CFF_ALL',
        		'param': '0,100,114,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
        ])
        case_list.append(case_conf)
        #....................................新三板........................
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'CATESORTING_2'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
			#001代码
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,1,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #002
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,1,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#003交易状态
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,0,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #004
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #005名称
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,2,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #006
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,2,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #007昨收
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,11,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #008
           json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,11,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #009开盘
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,10,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #010
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,10,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #011最高
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,8,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #012
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,8,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #013最低
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,9,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #014
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,9,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #015最新
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,7,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #016
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,7,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #017涨跌
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #018
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #019涨跌幅
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,-3,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #020
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,-3,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #021成交量
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,13,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #022
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,13,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #023成交额
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #024
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #025当前成交量
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,14,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #026
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,14,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#027换手率
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,15,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #028
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,15,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#029量比
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,21,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #030
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #031内盘
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,25,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #032
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,25,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #033外盘
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,24,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #034
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,24,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#035总市值
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,26,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #036
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,26,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#037流通市值
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,27,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #038
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,27,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#039净资产
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,28,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #040
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,28,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#041动态市盈率
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,29,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #042
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,29,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),			
            #043市净率
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,30,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #044
           json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,30,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #045总股本
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,31,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #046
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,31,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #047流通股
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,32,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #048
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,32,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #049振幅比率
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,37,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #050
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #051动态每股收益
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,38,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #052
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#053委比
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,53,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #054
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,53,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #055静态市盈率
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,42,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #056
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #055交易日
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,119,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #056
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,119,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#057昨收
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,11,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #058
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,11,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			 #059开盘
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,10,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #060
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,10,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #061最高
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,8,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #062
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,8,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #063最低
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,9,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #064
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,100,9,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #065最新
        	json.dumps({
        		'id': 'BJ1002',
        		'param': '0,100,7,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #066
            json.dumps({
        		'id': 'BJ1002',
        		'param': '0,100,7,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #067涨跌
        	json.dumps({
        		'id': 'BJ1002',
        		'param': '0,100,19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #068
            json.dumps({
        		'id': 'BJ1002',
        		'param': '0,100,19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #069涨跌幅
        	json.dumps({
        		'id': 'BJ1002',
        		'param': '0,100,-3,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #070
            json.dumps({
        		'id': 'BJ1002',
        		'param': '0,100,-3,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #071成交量
        	json.dumps({
        		'id': 'BJ1005',
        		'param': '0,100,13,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #072
            json.dumps({
        		'id': 'BJ1005',
        		'param': '0,100,13,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#073成交额
        	json.dumps({
        		'id': 'BJ1005',
        		'param': '0,100,20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #074
            json.dumps({
        		'id': 'BJ1005',
        		'param': '0,100,20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #075当前成交量
        	json.dumps({
        		'id': 'BJ1005',
        		'param': '0,100,14,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #076
            json.dumps({
        		'id': 'BJ1005',
        		'param': '0,100,14,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#077换手率
        	json.dumps({
        		'id': 'BJ1006',
        		'param': '0,100,15,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #078
            json.dumps({
        		'id': 'BJ1006',
        		'param': '0,100,15,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#079量比
        	json.dumps({
        		'id': 'BJ1006',
        		'param': '0,100,21,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #080
            json.dumps({
        		'id': 'BJ1006',
        		'param': '0,100,21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #081内盘
        	json.dumps({
        		'id': 'BJ1006',
        		'param': '0,100,25,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #082
            json.dumps({
        		'id': 'BJ1006',
        		'param': '0,100,25,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #083外盘
        	json.dumps({
        		'id': 'BJ1007',
        		'param': '0,100,24,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #084
            json.dumps({
        		'id': 'BJ1007',
        		'param': '0,100,24,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#085总市值
        	json.dumps({
        		'id': 'BJ1007',
        		'param': '0,100,26,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #086
            json.dumps({
        		'id': 'BJ1007',
        		'param': '0,100,26,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#087流通市值
        	json.dumps({
        		'id': 'BJ1007',
        		'param': '0,100,27,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #088
            json.dumps({
        		'id': 'BJ1007',
        		'param': '0,100,27,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#089净资产
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,28,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #090
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,28,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#091动态市盈率
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,29,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #092
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,29,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),			
            #093市净率
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,30,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #094
           json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,30,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #095总股本
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,31,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #096
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,31,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #097流通股
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,32,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #098
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,32,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #099振幅比率
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,37,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #100
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #101动态每股收益
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,38,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #102
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#103委比
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,53,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #104
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,53,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #105静态市盈率
        	json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,42,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #106
            json.dumps({
        		'id': '899001.bj',
        		'param': '0,100,42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
        ])
        case_list.append(case_conf)
        #..................................沪伦通、全球指数、外汇.............
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'CATESORTING_2'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
			#001当前份额
        	json.dumps({
        		'id': 'UK1540',
        		'param': '0,100,57,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #002
            json.dumps({
        		'id': 'UK1540',
        		'param': '0,100,57,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#003前收盘份额
        	json.dumps({
        		'id': 'UK1540',
        		'param': '0,100,58,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #004
            json.dumps({
        		'id': 'UK1540',
        		'param': '0,100,58,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #005最新
        	json.dumps({
        		'id': 'GB1400',
        		'param': '0,100,300,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #006
            json.dumps({
        		'id': 'GB1400',
        		'param': '0,100,300,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #007最低
        	json.dumps({
        		'id': 'GB1400',
        		'param': '0,100,301,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #008
            json.dumps({
        		'id': 'GB1400',
        		'param': '0,100,301,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            
            #009涨跌额
        	json.dumps({
        		'id': 'GB1400',
        		'param': '0,100,302,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #010
            json.dumps({
        		'id': 'GB1400',
        		'param': '0,100,302,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #011涨跌幅
        	json.dumps({
        		'id': 'GB1400',
        		'param': '0,100,303,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #012
            json.dumps({
        		'id': 'GB1400',
        		'param': '0,100,303,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #013成交额
        	json.dumps({
        		'id': 'GB1400',
        		'param': '0,100,304,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #014
            json.dumps({
        		'id': 'GB1400',
        		'param': '0,100,304,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #015名称
        	json.dumps({
        		'id': 'GB1400',
        		'param': '0,100,305,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #016
            json.dumps({
        		'id': 'GB1400',
        		'param': '0,100,305,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #017成交量
        	json.dumps({
        		'id': 'GB1400',
        		'param': '0,100,306,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #018
            json.dumps({
        		'id': 'GB1400',
        		'param': '0,100,306,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#019昨收
        	json.dumps({
        		'id': 'GB1400',
        		'param': '0,100,307,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #020
            json.dumps({
        		'id': 'GB1400',
        		'param': '0,100,307,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#021最高
        	json.dumps({
        		'id': 'GB1400',
        		'param': '0,100,308,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #022
            json.dumps({
        		'id': 'GB1400',
        		'param': '0,100,308,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #023最新
        	json.dumps({
        		'id': 'GB1001',
        		'param': '0,100,300,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #024
            json.dumps({
        		'id': 'GB1001',
        		'param': '0,100,300,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #025最低
        	json.dumps({
        		'id': 'GB1001',
        		'param': '0,100,301,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #026
            json.dumps({
        		'id': 'GB1001',
        		'param': '0,100,301,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#027涨跌额
        	json.dumps({
        		'id': 'GB1001',
        		'param': '0,100,302,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #028
            json.dumps({
        		'id': 'GB1001',
        		'param': '0,100,302,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#029涨跌幅
        	json.dumps({
        		'id': 'GB1001',
        		'param': '0,100,303,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #030
            json.dumps({
        		'id': 'GB1001',
        		'param': '0,100,303,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#031成交额
        	json.dumps({
        		'id': 'GB1001',
        		'param': '0,100,304,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #032
            json.dumps({
        		'id': 'GB1001',
        		'param': '0,100,304,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#033名称
        	json.dumps({
        		'id': 'GB1001',
        		'param': '0,100,305,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #034
            json.dumps({
        		'id': 'GB1001',
        		'param': '0,100,305,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),			
            #035成交量
        	json.dumps({
        		'id': 'GB1001',
        		'param': '0,100,306,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #036
           json.dumps({
        		'id': 'GB1001',
        		'param': '0,100,306,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #037昨收价
        	json.dumps({
        		'id': 'GB1001',
        		'param': '0,100,307,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #038
            json.dumps({
        		'id': 'GB1001',
        		'param': '0,100,307,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #039最高价
        	json.dumps({
        		'id': 'GB1001',
        		'param': '0,100,308,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #040
            json.dumps({
        		'id': 'GB1001',
        		'param': '0,100,308,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
        ])
        case_list.append(case_conf)
		
        runner_conf.casesConfig.extend(case_list)
        print('i,case_list.length is ', case_list.__len__())
        runner_conf_list.append(runner_conf)

    return runner_conf_list


default_args = {
    'owner': 'test',
    'depends_on_past': False, # 是否依赖上一个自己的执行状态
    'start_date': datetime(2019, 11, 12),
    'email': ['2079647340@qq.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG( dag_id='test_sdk', default_args=default_args,schedule_interval='@once')
       
start_task = DummyOperator(
    task_id='run_this_first',
    queue='worker',
    dag=dag
    
)

run_this_last = DummyOperator(
    task_id='run_this_last',
    queue='worker',
    dag=dag
)

runner_conf_list = initRunnerConfig()
task_id_to_cmp_list = ['adb_shell_cmp_a', 'adb_shell_cmp_b']

android_release = AndroidReleaseOperator(
    task_id='android_release',
    provide_context=False,
    repo_name='stocksdktest/AndroidTestRunner',
    tag_id='release-20191030-0.0.2',
    tag_sha='91af71d21a42200c63ae4f37bd8f2bcf868866c5',
    runner_conf=runner_conf_list[0],
    dag=dag
)

android_a = AndroidRunnerOperator(
    task_id=task_id_to_cmp_list[0],
    provide_context=False,
    apk_id='com.chi.ssetest',
    apk_version='release-20191030-0.0.2',
    runner_conf=runner_conf_list[0],
    dag=dag
)

android_b = AndroidRunnerOperator(
    task_id=task_id_to_cmp_list[1],
    provide_context=False,
    apk_id='com.chi.ssetest',
    apk_version='release-20191030-0.0.2',
    runner_conf=runner_conf_list[1],
    dag=dag
)
                                                      
android_cmp = DataCompareOperator(
    task_id='data_compare',
    task_id_list=task_id_to_cmp_list,
    retries=3,
    provide_context=False,
    runner_conf=RunnerConfig,
    dag=dag
)

start_task >> android_release >> [android_a, android_b] >> android_cmp >> run_this_last

if __name__ == "__main__":
    dag.cli()
