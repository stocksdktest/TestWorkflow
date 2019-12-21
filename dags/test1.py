import json

import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
from operators.data_compare_operator import DataCompareOperator
from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig, Site
from operators.android_runner_operator import AndroidRunnerOperator
from operators.android_release_operator import AndroidReleaseOperator

#全真（新版SDK）和生产（现生产版本SDK）对比
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
        #走势数据
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'CHARTV2TEST_2'
        case_conf.continueWhenFailed = False
        case_conf.roundIntervalSec = 3
        case_conf.paramStrs.extend([
            json.dumps({
        		'CODES': '831814.bj',
        		'Chart_Types': 'ChartTypeOneDay',       
        	}),
			#005
        	json.dumps({
        		'CODES': '841004.bj',
        		'Chart_Types': 'ChartTypeOneDay',       
        	}),
        ])
        case_list.append(case_conf)

        # 排行
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'CATESORTING_2'
        case_conf.continueWhenFailed = False
        case_conf.roundIntervalSec = 3
        case_conf.paramStrs.extend([
            #010  
			json.dumps({
				'id': 'SH1001',
				'param': '0,100,7,0,1',
				'quoteCustom': '-1',
				'addvalueCustom': 'null'
			}),
        ])
        case_list.append(case_conf)

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

        runner_conf.casesConfig.extend(case_list)
        print('i,case_list.length is ', case_list.__len__())
        runner_conf_list.append(runner_conf)

    return runner_conf_list


with DAG(
       dag_id='android_test1',
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