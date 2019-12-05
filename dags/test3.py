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
        #..................全真和测试（新版SDK）对比.........................
        #...................................437................................
		#新债列表
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
		#新债详情
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'F10_BNDSHAREIPODETAI_1'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
			#007
			json.dumps({
				'code': '110061.sh',
				'src': 'd'
			}),
			# #008 
			# json.dumps({
			# 	'code': '',
			# 	'src': 'd'
			# }),
			# #009 
			# json.dumps({
			# 	'code': '',
			# 	'src': 'd'
			# }),
        ])
        case_list.append(case_conf)
        #.................................445....................................
		#分量区间统计请求
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'MOREVOLUMETEST_1'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
			#001 
			json.dumps({
				'code': '600000.sh',
				'subtype': '1001'
			}),
			#002 
			json.dumps({
				'code': '688001.sh',
				'subtype': '1006'
			}),
			#003
			json.dumps({
				'code': '900903.sh',
				'subtype': '1002'
			}),
			#004 
			json.dumps({
				'code': '000001.sh',
				'subtype': '1400'
			}),
			#005 
			json.dumps({
				'code': '502058.sh',
				'subtype': '1100'
			}),
			#006 
			json.dumps({
				'code': '513680.sh',
				'subtype': '1120'
			}),
			#007 
			json.dumps({
				'code': '501311.sh',
				'subtype': '1110'
			}),
			#008
			json.dumps({
				'code': '124418.sh',
				'subtype': '1300'
			}),
			#009 
			json.dumps({
				'code': '204001.sh',
				'subtype': '1311'
			}),
			#010
			json.dumps({
				'code': '113544.sh',
				'subtype': '1312'
			}),
			#011
			json.dumps({
				'code': '10001910.sh',
				'subtype': '3002'
			}),
			#012 
			json.dumps({
				'code': '600003.sh',
				'subtype': '9800'
			}),
			#013 
			json.dumps({
				'code': '600610.sh',
				'subtype': '1011'
			}),
			#014
			json.dumps({
				'code': '900951.sh',
				'subtype': 'SHS'
			}),
			#015
			json.dumps({
				'code': '020322.sh',
				'subtype': '1313'
			}),
			#016
			json.dumps({
				'code': '120702.sh',
				'subtype': '1314'
			}),
			#017
			json.dumps({
				'code': '001979.sz',
				'subtype': '1005'
			}),
			#018
			json.dumps({
				'code': '000001.sz',
				'subtype': '1001'
			}),
			#019
			json.dumps({
				'code': '002524.sz',
				'subtype': '1003'
			}),
			#020
			json.dumps({
				'code': '300484.sz',
				'subtype': '1004'
			}),
			#021 
			json.dumps({
				'code': '200986.sz',
				'subtype': '1002'
			}),
			#022 
			json.dumps({
				'code': '399001.sz',
				'subtype': '1400'
			}),
			#023
			json.dumps({
				'code': '150258.sz',
				'subtype': '1100'
			}),
			#024
			json.dumps({
				'code': '159955.sz',
				'subtype': '1120'
			}),
			#025
			json.dumps({
				'code': '169301.sz',
				'subtype': '1110'
			}),
			#026
			json.dumps({
				'code': '123007.sz',
				'subtype': '1300'
			}),
			#027
			json.dumps({
				'code': '128074.sz',
				'subtype': '1312'
			}),
			#028
			json.dumps({
				'code': '131810.sz',
				'subtype': '1311'
			}),
			#029
			json.dumps({
				'code': '101988.sz',
				'subtype': '1313'
			}),
			#030
			json.dumps({
				'code': '111924.sz',
				'subtype': '1314'
			}),
			#031
			json.dumps({
				'code': '200168.sz',
				'subtype': 'SZS'
			}),
			#032
			json.dumps({
				'code': '002070.sz',
				'subtype': '9800'
			}),
			#033
			json.dumps({
				'code': '000995.sz',
				'subtype': '1011'
			}),
        ])
        case_list.append(case_conf)
        #......................................446...........................
		#个股所属板块行情
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'BANKUAIQUOTE_1'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
			#001 
			json.dumps({
				'code': '600132.sh',				
			}),
			#002
			json.dumps({
				'code': 'sw_600132.sh',				
			}),
			#003 
			json.dumps({
				'code': 'szyp_600132.sh',
			}),
			#004
			json.dumps({
				'code': '601872.sh',
				'params': 'trade,area,notion,hktrade,trade_sw,trade_sw1,notion_szyp,area_szyp,trade_szyp'
			}),
			#005 
			json.dumps({
				'code': '601872.sh',
				'params': 'trade'
			}),
			# #006
			# json.dumps({
			# 	'code': '"601872.sh',
			# 	'params': 'trade,notion'
			# }),
			# #007 
			# json.dumps({
			# 	'code': '"601872.sh',
			# 	'params': 'trade_sw,notion_szyp,trade_sw1'
			# }),
			#008
			json.dumps({
				'code': '601872.sh',
				'params': 'notion,,notion_szyp,trade_sw1,area'
			}),
        ])
        case_list.append(case_conf)	
        #......................................452...........................
		#分类排行
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'CATESORTING_2'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([			
			#003
			json.dumps({
				'id': 'SZ1400',
				'param': '0,100,1,0,1',
				'quoteCustom': '-1',
				'addvalueCustom': 'null',			
			}),
        ])
        case_list.append(case_conf)	
		#股票查询 方法4
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'SEARTEST_4'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
			#004
			json.dumps({
				'keyword': '395',
				'searchCode': 'SZ_1400',
				'searchSize': '0',
				'querySts': '9900'
			}),
			#005
			json.dumps({
				'keyword': '395',
				'searchCode': 'SZ_1400',
				'searchSize': '0',
				'querySts': '9800'
			})
        ])
        case_list.append(case_conf)	
        #新版股名在线搜索
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'SEARV2TEST_2'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
			#006
			json.dumps({
				'keyword': '0010',
				'markets': 'sz',
				'count': '100'
			}),	   
		])
        case_list.append(case_conf)
		#交易行情
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'TRADEQUOTE_1'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
			# #010
			# json.dumps({
			# 	'code': '3950001.sz'
			# }),	   
		])
        case_list.append(case_conf)
		#行情快照
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'QUOTEDETAIL_2'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
			#007
			json.dumps({
				'CODES': '395001.sz',
				'COUNTS': '10',
				'INTS1': 'null',
				'INTS2': 'null'
			}),	   
		])
        case_list.append(case_conf)
		#证券行情列表
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'QUOTE_2'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
			# #008
			# json.dumps({
			# 	'CODES': '395001.sz',
			# 	'INTS1': 'null',
			# 	'INTS2': 'null'
			# }),	 
			# json.dumps({
			# 	'CODES': '395002.sz',
			# 	'INTS1': 'null',
			# 	'INTS2': 'null'
			# }),	  
		])
        case_list.append(case_conf)
		#版块类股票行情
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'CATEQUOTE_1'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
			#009
			json.dumps({
				'CateType': 'SZ1400',
				'page': '0',
			}),	   
		])
        case_list.append(case_conf)
        #..........................................418..........................
		#行情快照
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'QUOTEDETAIL_2'
        case_conf.continueWhenFailed = False
        case_conf.roundIntervalSec = 3
        case_conf.paramStrs.extend([
            #001
        	json.dumps({
        		'CODES': '399998.sz',
        		'COUNTS': '10',
                'INTS1': 'null',
        		'INTS2': 'null',
        	}),
            #002
            json.dumps({
        		'CODES': '399001.sz',
        		'COUNTS': '10',
                'INTS1': 'null',
        		'INTS2': 'null',
        	}),
            #003
            json.dumps({
        		'CODES': '399996.sz',
        		'COUNTS': '10',
                'INTS1': 'null',
        		'INTS2': 'null',
        	}),
            #004
            json.dumps({
        		'CODES': '399997.sz',
        		'COUNTS': '10',
                'INTS1': 'null',
        		'INTS2': 'null',
        	}),
			# #005
            # json.dumps({
        	# 	'CODES': '398999.sz',
        	# 	'COUNTS': '10',
            #     'INTS1': 'null',
        	# 	'INTS2': 'null',
        	# }),
        ])
        case_list.append(case_conf)
        #走势数据 
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'CHARTV2TEST_2'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
            #006
        	json.dumps({
        		'CODES': '399998.sz',
        		'Chart_Types': 'ChartTypeOneDay',       
        	}),
			#007
        	json.dumps({
        		'CODES': '399001.sz',
        		'Chart_Types': 'ChartTypeOneDay',       
        	}),
			#008
        	json.dumps({
        		'CODES': '399996.sz',
        		'Chart_Types': 'ChartTypeOneDay',       
        	}),
			#009
        	json.dumps({
        		'CODES': '399997.sz',
        		'Chart_Types': 'ChartTypeOneDay',       
        	}),
			#010
        	json.dumps({
        		'CODES': '399998.sz',
        		'Chart_Types': 'ChartTypeOneDay',       
        	}),		
            #011  one/flive分开传
            json.dumps({
				'CODES': '399998.sz',
				'Chart_Types': 'ChartTypeFiveDay', 
            }),			
            #012
            json.dumps({
				'CODES': '399001.sz',
				'Chart_Types': 'ChartTypeFiveDay', 
            }),
			#013
            json.dumps({
				'CODES': '399996.sz',
				'Chart_Types': 'ChartTypeFiveDay', 
            }),
            #014
            json.dumps({
				'CODES': '399997.sz',
				'Chart_Types': 'ChartTypeFiveDay', 
            }),
            # #015
            # json.dumps({
			# 	'CODES': '399999.sz',
			# 	'Chart_Types': 'ChartTypeFiveDay', 
            # }),
        ])
        case_list.append(case_conf)
        #历史k线 方法5
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'OHLCV3_5'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
            #016
            json.dumps({
                'CODES': '399998.sz',
                'TYPES': 'dayk',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #017
            json.dumps({
                'CODES': '399998.sz',
                'TYPES': 'weekk',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#018
            json.dumps({
                'CODES': '399998.sz',
                'TYPES': 'monthk',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #019
            json.dumps({
                'CODES': '399998.sz',
                'TYPES': 'yeark',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#020
            json.dumps({
                'CODES': '399998.sz',
                'TYPES': 'm1',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #021
            json.dumps({
                'CODES': '399998.sz',
                'TYPES': 'm5',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#022
            json.dumps({
                'CODES': '399998.sz',
                'TYPES': 'm15',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #023
            json.dumps({
                'CODES': '399998.sz',
                'TYPES': 'm30',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#024
            json.dumps({
                'CODES': '399998.sz',
                'TYPES': 'm60',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #025
            json.dumps({
                'CODES': '399998.sz',
                'TYPES': 'm120',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#026
            json.dumps({
                'CODES': '399001.sz',
                'TYPES': 'dayk',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #027
            json.dumps({
                'CODES': '399001.sz',
                'TYPES': 'weekk',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#028
            json.dumps({
                'CODES': '399001.sz',
                'TYPES': 'monthk',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #029
            json.dumps({
                'CODES': '399001.sz',
                'TYPES': 'yeark',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#030
            json.dumps({
                'CODES': '399001.sz',
                'TYPES': 'm1',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #031
            json.dumps({
                'CODES': '399001.sz',
                'TYPES': 'm5',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#032
            json.dumps({
                'CODES': '399001.sz',
                'TYPES': 'm15',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #033
            json.dumps({
                'CODES': '399001.sz',
                'TYPES': 'm30',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#034
            json.dumps({
                'CODES': '399001.sz',
                'TYPES': 'm60',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #035
            json.dumps({
                'CODES': '399001.sz',
                'TYPES': 'm120',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#036
            json.dumps({
                'CODES': '399996.sz',
                'TYPES': 'dayk',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #037
            json.dumps({
                'CODES': '399996.sz',
                'TYPES': 'weekk',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#038
            json.dumps({
                'CODES': '399996.sz',
                'TYPES': 'monthk',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #039
            json.dumps({
                'CODES': '399996.sz',
                'TYPES': 'yeark',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#040
            json.dumps({
                'CODES': '399996.sz',
                'TYPES': 'm1',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
             #041
            json.dumps({
                'CODES': '399996.sz',
                'TYPES': 'm5',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#042
            json.dumps({
                'CODES': '399996.sz',
                'TYPES': 'm15',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #043
            json.dumps({
                'CODES': '399996.sz',
                'TYPES': 'm30',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#044
            json.dumps({
                'CODES': '399996.sz',
                'TYPES': 'm60',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #045
            json.dumps({
                'CODES': '399996.sz',
                'TYPES': 'm120',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#046
            json.dumps({
                'CODES': '399997.sz',
                'TYPES': 'dayk',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #047
            json.dumps({
                'CODES': '399997.sz',
                'TYPES': 'weekk',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#048
            json.dumps({
                'CODES': '399997.sz',
                'TYPES': 'monthk',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #049
            json.dumps({
                'CODES': '399997.sz',
                'TYPES': 'yeark',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#050
            json.dumps({
                'CODES': '399997.sz',
                'TYPES': 'm1',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #051
            json.dumps({
                'CODES': '399997.sz',
                'TYPES': 'm5',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#052
            json.dumps({
                'CODES': '399997.sz',
                'TYPES': 'm15',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #053
            json.dumps({
                'CODES': '399997.sz',
                'TYPES': 'm30',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#054
            json.dumps({
                'CODES': '399997.sz',
                'TYPES': 'm60',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #055
            json.dumps({
                'CODES': '399997.sz',
                'TYPES': 'm120',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#056
            json.dumps({
                'CODES': '399999.sz',
                'TYPES': 'dayk',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #057
            json.dumps({
                'CODES': '399999.sz',
                'TYPES': 'weekk',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#058
            json.dumps({
                'CODES': '399999.sz',
                'TYPES': 'monthk',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #059
            json.dumps({
                'CODES': '399999.sz',
                'TYPES': 'yeark',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#060
            json.dumps({
                'CODES': '399999.sz',
                'TYPES': 'm1',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #061
            json.dumps({
                'CODES': '399999.sz',
                'TYPES': 'm5',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#062
            json.dumps({
                'CODES': '399999.sz',
                'TYPES': 'm15',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #063
            json.dumps({
                'CODES': '399999.sz',
                'TYPES': 'm30',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#064
            json.dumps({
                'CODES': '399999.sz',
                'TYPES': 'm60',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #065
            json.dumps({
                'CODES': '399999.sz',
                'TYPES': 'm120',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),          
        ])
		#分类排行
        case_list.append(case_conf)
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'CATESORTING_2'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
			#066代码
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,2000,1,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #067
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,1,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #068交易状态
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,0,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #069
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#070名称
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,2,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #071
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,2,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),			
            #072昨收
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,11,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #073
           json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,11,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #074开盘
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,10,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #075
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,10,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #076最高
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,8,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #077
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,8,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #078最低
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,9,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #079
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,9,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #080最新
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,7,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #081
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,7,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#082涨跌
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #083
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #084涨跌幅
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-3,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #085
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-3,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #086成交量
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,13,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #087
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,13,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #088成交额
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #089
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #90当前成交量
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,14,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #091
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,14,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#092换手率
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,15,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #093
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,15,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#094量比
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,21,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #095
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#096内盘
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,25,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #097
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,25,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #098外盘
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,24,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #099
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,24,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#100总市值
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,26,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #101
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,26,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#102流通市值
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,27,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #103
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,27,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#104净资产
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,28,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #105
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,28,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#106动态市盈率
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,29,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #107
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,29,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),			
            #108市净率
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,30,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #109
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,30,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #110总股本
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,31,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #111
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,31,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #112流通股
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,32,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #113
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,32,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #114振幅比率
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,37,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #115
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #116动态每股收益
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,38,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #117
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#118委比
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,53,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #119
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,53,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #120静态市盈率
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,42,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #121
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #122大单净流入
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #123
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#124大单净流入
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #125
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#126中单净流入
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-21,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #127
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#128小单净流入
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-22,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #129
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-22,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #130大单净差
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-34,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #131
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-34,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#132五日大单净差
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-35,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #133
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-35,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#134十日大单净差
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-36,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #135
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-36,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),	
			#136主力动向
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-37,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #137
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#138五日主力动向
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-38,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #139
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#140十日主力动向
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-39,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #141
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-39,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #142涨跌动因
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-40,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #143
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-40,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#144五日涨跌动因
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-41,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #145
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-41,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#146十日涨跌动因
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-42,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #147
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#148主力净流入
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-47,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #149
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-47,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#1505分钟涨跌幅
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-48,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #151
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-48,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#1525日主力净流入
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-58,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #153
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-58,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#15410日主力净流入
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-59,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #155
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-59,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#15620日主力净流入
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-60,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #157
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-60,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#1585日主力净流入占比
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-61,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #159
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-61,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#16010日主力净流入占比
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-62,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #161
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-62,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#16220日主力净流入占比
        	json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-63,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
            #163
            json.dumps({
        		'id': 'SZ1400',
        		'param': '0,100,-63,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': 'null',
        	}),
			#164代码
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,1,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #165
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,1,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #166交易状态
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,0,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #167
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#168名称
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,2,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #169
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,2,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),			
            #170昨收
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,11,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #171
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,11,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #172开盘
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,10,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #173
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,10,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #174最高
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,8,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #175
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,8,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #176最低
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,9,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #177
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,9,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #178最新
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,7,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #179
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,7,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#180涨跌
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #181
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #182涨跌幅
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-3,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #183
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-3,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #184成交量
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,13,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #185
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,13,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #186成交额
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #187
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #188当前成交量
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,14,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #189
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,14,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#190换手率
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,15,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #191
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,15,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#192量比
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,21,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #193
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#194内盘
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,25,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #195
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,25,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #196外盘
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,24,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #197
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,24,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#198总市值
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,26,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #199
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,26,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#200流通市值
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,27,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #201
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,27,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#202净资产
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,28,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #203
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,28,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#204动态市盈率
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,29,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #205
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,29,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),			
            #206市净率
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,30,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #207
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,30,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #208总股本
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,31,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #209
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,31,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #210流通股
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,32,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #211
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,32,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #212振幅比率
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,37,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #213
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #214动态每股收益
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,38,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #215
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#216委比
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,53,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #217
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,53,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #218静态市盈率
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,42,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #219
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #220大单净流入
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #221
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#222大单净流入
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #223
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#224中单净流入
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-21,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #225
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#226小单净流入
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-22,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #227
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-22,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #228大单净差
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-34,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #229
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-34,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#230五日大单净差
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-35,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #231
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-35,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#232十日大单净差
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-36,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #233
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-36,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),	
			#234主力动向
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-37,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #235
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#236五日主力动向
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-38,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #237
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#238十日主力动向
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-39,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #239
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-39,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #240涨跌动因
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-40,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #241
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-40,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#242五日涨跌动因
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-41,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #243
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-41,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#244十日涨跌动因
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-42,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #245
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#246主力净流入
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-47,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #247
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-47,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#2485分钟涨跌幅
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-48,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #249
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-48,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#2505日主力净流入
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-58,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #251
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-58,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#25210日主力净流入
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-59,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #253
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-59,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#25420日主力净流入
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-60,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #255
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-60,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#2565日主力净流入占比
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-61,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #257
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-61,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#25810日主力净流入占比
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-62,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #259
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-62,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#26020日主力净流入占比
        	json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-63,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #261
            json.dumps({
        		'id': 'SZ1401',
        		'param': '0,100,-63,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#262代码
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,2000,1,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #263
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,1,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #264交易状态
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,0,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #265
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#266名称
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,2,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #267
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,2,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),			
            #268昨收
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,11,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #269
           json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,11,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #270开盘
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,10,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #271
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,10,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #272最高
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,8,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #273
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,8,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #274最低
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,9,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #275
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,9,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #276最新
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,7,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #277
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,7,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#278涨跌
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #279
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #280涨跌幅
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-3,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #281
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-3,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #282成交量
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,13,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #283
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,13,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #284成交额
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #285
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #286当前成交量
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,14,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #287
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,14,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#288换手率
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,15,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #289
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,15,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#290量比
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,21,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #291
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#292内盘
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,25,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #293
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,25,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #294外盘
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,24,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #295
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,24,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#296总市值
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,26,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #297
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,26,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#298流通市值
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,27,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #299
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,27,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#300净资产
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,28,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #301
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,28,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#302动态市盈率
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,29,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #303
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,29,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),			
            #304市净率
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,30,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #305
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,30,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #306总股本
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,31,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #307
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,31,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #308流通股
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,32,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #309
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,32,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #310振幅比率
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,37,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #311
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #312动态每股收益
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,38,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #313
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#314委比
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,53,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #315
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,53,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #316静态市盈率
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,42,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #317
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #318大单净流入
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #319
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#320大单净流入
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #321
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#322中单净流入
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-21,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #323
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#324小单净流入
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-22,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #325
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-22,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #326大单净差
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-34,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #327
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-34,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#328五日大单净差
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-35,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #329
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-35,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#330十日大单净差
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-36,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #331
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-36,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),	
			#332主力动向
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-37,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #333
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#334五日主力动向
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-38,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #335
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#336十日主力动向
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-39,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #337
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-39,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #338涨跌动因
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-40,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #339
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-40,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#340五日涨跌动因
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-41,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #341
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-41,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#342十日涨跌动因
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-42,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #343
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#344主力净流入
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-47,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #345
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-47,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#3465分钟涨跌幅
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-48,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #347
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-48,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#3485日主力净流入
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-58,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #349
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-58,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#35010日主力净流入
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-59,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #351
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-59,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#35220日主力净流入
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-60,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #353
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-60,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#3545日主力净流入占比
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-61,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #355
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-61,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#35610日主力净流入占比
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-62,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #357
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-62,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#35820日主力净流入占比
        	json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-63,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #359
            json.dumps({
        		'id': 'SZ1402',
        		'param': '0,100,-63,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#360代码
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,2000,1,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #361
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,1,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #362交易状态
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,0,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #363
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#364名称
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,2,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #365
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,2,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),			
            #366昨收
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,11,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #367
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,11,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #368开盘
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,10,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #369
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,10,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #370最高
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,8,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #371
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,8,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #372最低
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,9,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #373
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,9,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #374最新
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,7,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #375
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,7,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#376涨跌
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #377
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #378涨跌幅
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-3,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #379
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-3,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #380成交量
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,13,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #381
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,13,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #382成交额
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #383
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #384当前成交量
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,14,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #385
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,14,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#386换手率
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,15,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #387
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,15,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#388量比
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,21,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #389
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#390内盘
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,25,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #391
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,25,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #392外盘
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,24,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #393
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,24,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#394总市值
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,26,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #395
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,26,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#396流通市值
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,27,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #397
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,27,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#398净资产
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,28,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #399
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,28,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#400动态市盈率
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,29,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #401
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,29,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),			
            #402市净率
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,30,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #403
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,30,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #404总股本
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,31,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #405
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,31,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #406流通股
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,32,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #407
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,32,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #408振幅比率
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,37,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #409
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #410动态每股收益
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,38,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #411
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#412委比
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,53,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #413
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,53,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #414静态市盈率
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,42,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #415
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #416大单净流入
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #417
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#418大单净流入
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #419
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#420中单净流入
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-21,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #421
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#422小单净流入
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-22,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #423
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-22,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #424大单净差
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-34,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #425
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-34,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#426五日大单净差
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-35,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #427
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-35,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#428十日大单净差
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-36,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #429
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-36,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),	
			#430主力动向
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-37,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #431
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#432五日主力动向
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-38,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #433
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#434十日主力动向
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-39,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #435
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-39,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #436涨跌动因
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-40,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #437
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-40,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#438五日涨跌动因
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-41,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #439
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-41,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#440十日涨跌动因
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-42,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #441
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#442主力净流入
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-47,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #443
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-47,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#4445分钟涨跌幅
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-48,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #445
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-48,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#4465日主力净流入
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-58,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #447
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-58,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#44810日主力净流入
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-59,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #449
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-59,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#45020日主力净流入
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-60,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #451
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-60,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#4525日主力净流入占比
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-61,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #453
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-61,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#45410日主力净流入占比
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-62,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #455
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-62,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#45610日主力净流入占比
        	json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-63,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #457
            json.dumps({
        		'id': 'SZ1403',
        		'param': '0,100,-63,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#458代码
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,2000,1,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #459
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,1,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #460交易状态
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,0,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #461
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#462名称
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,2,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #463
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,2,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),			
            #464昨收
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,11,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #465
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,11,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #466开盘
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,10,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #467
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,10,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #468最高
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,8,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #469
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,8,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #470最低
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,9,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #471
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,9,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #472最新
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,7,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #473
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,7,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#474涨跌
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #475
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #476涨跌幅
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-3,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #477
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-3,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #478成交量
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,13,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #479
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,13,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #480成交额
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #481
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #482当前成交量
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,14,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #483
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,14,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#484换手率
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,15,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #485
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,15,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#486量比
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,21,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #487
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#488内盘
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,25,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #489
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,25,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #490外盘
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,24,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #491
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,24,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#492总市值
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,26,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #493
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,26,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#494流通市值
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,27,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #495
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,27,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#496净资产
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,28,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #497
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,28,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#498动态市盈率
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,29,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #499
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,29,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),			
            #500市净率
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,30,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #501
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,30,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #502总股本
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,31,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #503
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,31,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #504流通股
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,32,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #505
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,32,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #506振幅比率
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,37,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #507
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #508动态每股收益
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,38,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #509
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#510委比
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,53,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #511
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,53,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #512静态市盈率
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,42,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #513
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #514大单净流入
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #515
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#516大单净流入
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #517
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#518中单净流入
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-21,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #519
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#520小单净流入
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-22,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #521
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-22,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #522大单净差
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-34,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #523
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-34,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#524五日大单净差
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-35,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #525
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-35,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#526十日大单净差
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-36,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #527
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-36,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),	
			#528主力动向
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-37,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #529
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#530五日主力动向
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-38,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #531
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#532十日主力动向
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-39,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #533
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-39,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #534涨跌动因
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-40,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #535
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-40,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#536五日涨跌动因
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-41,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #537
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-41,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#538十日涨跌动因
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-42,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #539
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#540主力净流入
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-47,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #541
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-47,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#5425分钟涨跌幅
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-48,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #543
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-48,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#5445日主力净流入
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-58,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #545
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-58,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#54610日主力净流入
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-59,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #547
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-59,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#54820日主力净流入
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-60,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #549
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-60,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#5505日主力净流入占比
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-61,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #551
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-61,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#55210日主力净流入占比
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-62,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #553
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-62,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#55410日主力净流入占比
        	json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-63,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #555
            json.dumps({
        		'id': 'SZ1404',
        		'param': '0,100,-63,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),			
        ])
        case_list.append(case_conf)
        #...........................使用3.0的SDK测试...........................
        #..........................................455..........................
		#期权-标的行情
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'OPTIONLIST_1'
        case_conf.continueWhenFailed = False
        case_conf.roundIntervalSec = 3
        case_conf.paramStrs.extend([
            #001
        	json.dumps({
        		
        	}),
        ])
        case_list.append(case_conf)
        #行情快照
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'QUOTEDETAIL_1'
        case_conf.continueWhenFailed = False
        case_conf.roundIntervalSec = 3
        case_conf.paramStrs.extend([
            #002
        	json.dumps({
        		'CODES': '90000019.sz',
        	}),     
        ])
        case_list.append(case_conf)
        #期权-商品行情
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'OPTIONQUOTE_1'
        case_conf.continueWhenFailed = False
        case_conf.roundIntervalSec = 3
        case_conf.paramStrs.extend([
            #001
        	json.dumps({
        		'stockID': '159902.sz',
				'page': '0',
        	}), 
			#002
        	json.dumps({
        		'stockID': '159902.sz_CALL',
				'page': '0',
        	}),
			#003
        	json.dumps({
        		'stockID': '159902.sz_PUT',
				'page': '0',
        	}),  
			#001
        	json.dumps({
        		'stockID': '510050.sh',
				'page': '0',
        	}), 
			#002
        	json.dumps({
        		'stockID': '510050.sh_CALL',
				'page': '0',
        	}),
			#003
        	json.dumps({
        		'stockID': '510050.sh_PUT',
				'page': '0',
        	}),    
        ])
        case_list.append(case_conf)
		#期权-T型报价
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'OPTIONTQUOTE_1'
        case_conf.continueWhenFailed = False
        case_conf.roundIntervalSec = 3
        case_conf.paramStrs.extend([
            #001
        	json.dumps({
        		'stockID': '159915.sz',
				'yearmonth': '1911',
        	}),   
			#001
        	json.dumps({
        		'stockID': '510050.sh',
				'yearmonth': '1911',
        	}),   
        ])
        case_list.append(case_conf)
		#期权-交割月
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'OPTIONEXPIRE_1'
        case_conf.continueWhenFailed = False
        case_conf.roundIntervalSec = 3
        case_conf.paramStrs.extend([
            #001
        	json.dumps({
        		'stockID': '159915.sz',
        	}), 
			#001
        	json.dumps({
        		'stockID': '510050.sh',
        	}),    
        ])
        case_list.append(case_conf)
		#走势数据
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'CHARTV2TEST_2'
        case_conf.continueWhenFailed = False
        case_conf.roundIntervalSec = 3
        case_conf.paramStrs.extend([
            #001
        	json.dumps({
        		'CODES': '90000022.sz',
        		'Chart_Types': 'ChartTypeOneDay',       
        	}),
			#002
        	json.dumps({
        		'CODES': '90000022.sz',
        		'Chart_Types': 'ChartTypeFiveDay',       
        	}), 
			#001
        	json.dumps({
        		'CODES': '10002005.sh',
        		'Chart_Types': 'ChartTypeOneDay',       
        	}),
			#002
        	json.dumps({
        		'CODES': '10002005.sh',
        		'Chart_Types': 'ChartTypeFiveDay',       
        	}),  
        ])
        case_list.append(case_conf)
        #历史k线 方法5
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'OHLCV3_5'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
            #001
            json.dumps({
                'CODES': '90000022.sz',
                'TYPES': 'dayk',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #002
            json.dumps({
               'CODES': '90000022.sz',
                'TYPES': 'weekk',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#003
            json.dumps({
                'CODES': '90000022.sz',
                'TYPES': 'monthk',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #004
            json.dumps({
               'CODES': '90000022.sz',
                'TYPES': 'm5',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#005
            json.dumps({
                'CODES': '90000022.sz',
                'TYPES': 'm15',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #006
            json.dumps({
               'CODES': '90000022.sz',
                'TYPES': 'm30',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#007
            json.dumps({
                'CODES': '90000022.sz',
                'TYPES': 'm60',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #008
            json.dumps({
               'CODES': '90000022.sz',
                'TYPES': 'm120',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#009
            json.dumps({
                'CODES': '90000022.sz',
                'TYPES': 'm1',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #010
            json.dumps({
               'CODES': '90000022.sz',
                'TYPES': 'yeark',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#001
            json.dumps({
                'CODES': '10002005.sh',
                'TYPES': 'dayk',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #002
            json.dumps({
               'CODES': '10002005.sh',
                'TYPES': 'weekk',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#003
            json.dumps({
                'CODES': '10002005.sh',
                'TYPES': 'monthk',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #004
            json.dumps({
               'CODES': '10002005.sh',
                'TYPES': 'm5',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#005
            json.dumps({
                'CODES': '10002005.sh',
                'TYPES': 'm15',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #006
            json.dumps({
               'CODES': '10002005.sh',
                'TYPES': 'm30',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#007
            json.dumps({
                'CODES': '10002005.sh',
                'TYPES': 'm60',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #008
            json.dumps({
               'CODES': '10002005.sh',
                'TYPES': 'm120',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
			#009
            json.dumps({
                'CODES': '10002005.sh',
                'TYPES': 'm1',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
            #010
            json.dumps({
               'CODES': '10002005.sh',
                'TYPES': 'yeark',
                'FqTypes': '2',
                'Dates': 'null',
                'Numbers': '300',
            }),
        ])
        case_list.append(case_conf)
        #分时明细
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'TICK_1'
        case_conf.continueWhenFailed = False
        case_conf.roundIntervalSec = 3
        case_conf.paramStrs.extend([
            #001
        	json.dumps({
        		'CODES': '90000022.sz',
        		'PAGES': '0,100,-1',  
				'SUBTYPES': '3002',      
        	}),
			# #002
        	# json.dumps({
        	# 	'CODES': '.sz',
        	# 	'Chart_Types': '0,100,-1',  
			# 	'SUBTYPES': '',       
        	# }), 
			#001
        	json.dumps({
        		'CODES': '10002005.sh',
        		'PAGES': '0,100,-1',  
				'SUBTYPES': '3002',      
        	}),
			# #002
        	# json.dumps({
        	# 	'CODES': '',
        	# 	'Chart_Types': '0,100,-1',  
			# 	'SUBTYPES': '',       
        	# }),  
        ])
        case_list.append(case_conf)
		#分价
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'MOREPRICE_1'
        case_conf.continueWhenFailed = False
        case_conf.roundIntervalSec = 3
        case_conf.paramStrs.extend([
            #001
        	json.dumps({
        		'code': '90000022.sz',
        		'subtype': '3002',        
        	}),
			# #002
        	# json.dumps({
        	# 	'code': '.sz',
        	# 	'subtype': '',         
        	# }),   
			#001
        	json.dumps({
        		'code': '10002004.sh',
        		'subtype': '3002',        
        	}),
			# #002
        	# json.dumps({
        	# 	'code': '',
        	# 	'subtype': '',         
        	# }), 
        ])
        case_list.append(case_conf)
        #股票查询 方法2
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'SEARTEST_2'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([
			#001
			json.dumps({
				'keyword': '009',
				'searchSize': '100',			
			}),
        ])
        case_list.append(case_conf)	
        #分类排行
        case_list.append(case_conf)
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'CATESORTING_2'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([		
            #001交易状态
            json.dumps({
        		'id': 'SZ3002',
        		'param': '0,50,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#002代码
        	json.dumps({
        		'id': 'SZ3002',
        		'param': '0,50,1,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #003最新
        	json.dumps({
        		'id': 'SZ3002',
        		'param': '0,50,7,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #004最高
        	json.dumps({
        		'id': 'SZ3002',
        		'param': '0,50,8,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #005最低
        	json.dumps({
        		'id': 'SZ3002',
        		'param': '0,50,9,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #006开盘
        	json.dumps({
        		'id': 'SZ3002',
        		'param': '0,50,10,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#007昨收
        	json.dumps({
        		'id': 'SZ3002',
        		'param': '0,50,11,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#008涨跌
        	json.dumps({
        		'id': 'SZ3002',
        		'param': '0,50,19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),          
            #009涨跌幅
        	json.dumps({
        		'id': 'SZ3002',
        		'param': '0,50,-3,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #010成交量
        	json.dumps({
        		'id': 'SZ3002',
        		'param': '0,50,13,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}), 
            #011当前成交量
        	json.dumps({
        		'id': 'SZ3002',
        		'param': '0,50,14,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),	
            #012换手率
        	json.dumps({
        		'id': 'SZ3002',
        		'param': '0,50,15,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),			
            #013成交额
        	json.dumps({
        		'id': 'SZ3002',
        		'param': '0,50,20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),                     
			#014量比
        	json.dumps({
        		'id': 'SZ3002',
        		'param': '0,50,21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}), 
            #015外盘
        	json.dumps({
        		'id': 'SZ3002',
        		'param': '0,50,24,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),			
			#016内盘
        	json.dumps({
        		'id': 'SZ3002',
        		'param': '0,50,25,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#017总市值
        	json.dumps({
        		'id': 'SZ3002',
        		'param': '0,50,26,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),            
			#018流通市值
        	json.dumps({
        		'id': 'SZ3002',
        		'param': '0,50,27,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),            
			#019净资产
        	json.dumps({
        		'id': 'SZ3002',
        		'param': '0,50,28,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),            
			#020动态市盈率
        	json.dumps({
        		'id': 'SZ3002',
        		'param': '0,50,29,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #021静态市盈率
            json.dumps({
        		'id': 'SZ3002',
        		'param': '0,50,42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),			
            #022市净率
        	json.dumps({
        		'id': 'SZ3002',
        		'param': '0,50,30,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #023总股本
        	json.dumps({
        		'id': 'SZ3002',
        		'param': '0,50,31,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),           
            #024流通股
        	json.dumps({
        		'id': 'SZ3002',
        		'param': '0,50,32,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),          
            #025振幅比率
        	json.dumps({
        		'id': 'SZ3002',
        		'param': '0,50,37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),          
            #026动态每股收益
        	json.dumps({
        		'id': 'SZ3002',
        		'param': '0,50,38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#027委比
        	json.dumps({
        		'id': 'SZ3002',
        		'param': '0,50,53,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#028委差
        	json.dumps({
        		'id': 'SZ3002',
        		'param': '0,50,54,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#029委比
        	json.dumps({
        		'id': 'SZ3002',
        		'param': '0,50,53,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#030委差
        	json.dumps({
        		'id': 'SZ3002',
        		'param': '10,50,54,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}), 
			#001交易状态
            json.dumps({
        		'id': 'SH3002',
        		'param': '0,50,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#002代码
        	json.dumps({
        		'id': 'SH3002',
        		'param': '0,50,1,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #003最新
        	json.dumps({
        		'id': 'SH3002',
        		'param': '0,50,7,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #004最高
        	json.dumps({
        		'id': 'SH3002',
        		'param': '0,50,8,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #005最低
        	json.dumps({
        		'id': 'SH3002',
        		'param': '0,50,9,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #006开盘
        	json.dumps({
        		'id': 'SH3002',
        		'param': '0,50,10,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#007昨收
        	json.dumps({
        		'id': 'SH3002',
        		'param': '0,50,11,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#008涨跌
        	json.dumps({
        		'id': 'SH3002',
        		'param': '0,50,19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),          
            #009涨跌幅
        	json.dumps({
        		'id': 'SH3002',
        		'param': '0,50,-3,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #010成交量
        	json.dumps({
        		'id': 'SH3002',
        		'param': '0,50,13,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}), 
            #011当前成交量
        	json.dumps({
        		'id': 'SH3002',
        		'param': '0,50,14,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),	
            #012换手率
        	json.dumps({
        		'id': 'SH3002',
        		'param': '0,50,15,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),			
            #013成交额
        	json.dumps({
        		'id': 'SH3002',
        		'param': '0,50,20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),                     
			#014量比
        	json.dumps({
        		'id': 'SH3002',
        		'param': '0,50,21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}), 
            #015外盘
        	json.dumps({
        		'id': 'SH3002',
        		'param': '0,50,24,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),			
			#016内盘
        	json.dumps({
        		'id': 'SH3002',
        		'param': '0,50,25,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#017总市值
        	json.dumps({
        		'id': 'SH3002',
        		'param': '0,50,26,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),            
			#018流通市值
        	json.dumps({
        		'id': 'SH3002',
        		'param': '0,50,27,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),            
			#019净资产
        	json.dumps({
        		'id': 'SH3002',
        		'param': '0,50,28,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),            
			#020动态市盈率
        	json.dumps({
        		'id': 'SH3002',
        		'param': '0,50,29,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #021静态市盈率
            json.dumps({
        		'id': 'SH3002',
        		'param': '0,50,42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),			
            #022市净率
        	json.dumps({
        		'id': 'SH3002',
        		'param': '0,50,30,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #023总股本
        	json.dumps({
        		'id': 'SH3002',
        		'param': '0,50,31,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),           
            #024流通股
        	json.dumps({
        		'id': 'SH3002',
        		'param': '0,50,32,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),          
            #025振幅比率
        	json.dumps({
        		'id': 'SH3002',
        		'param': '0,50,37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),          
            #026动态每股收益
        	json.dumps({
        		'id': 'SH3002',
        		'param': '0,50,38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#027委比
        	json.dumps({
        		'id': 'SH3002',
        		'param': '0,50,53,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#028委差
        	json.dumps({
        		'id': 'SH3002',
        		'param': '0,50,54,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#029委比
        	json.dumps({
        		'id': 'SH3002',
        		'param': '0,50,53,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#030委差
        	json.dumps({
        		'id': 'SH3002',
        		'param': '10,50,54,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),          			
        ])
        case_list.append(case_conf)
		#..........................................456..........................
		#行情快照
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'QUOTEDETAIL_1'
        case_conf.continueWhenFailed = False
        case_conf.roundIntervalSec = 3
        case_conf.paramStrs.extend([
            #001
        	json.dumps({
        		'CODES': '841004.bj',
        	}), 
			#002
        	json.dumps({
        		'CODES': '832397.bj',
        	}),    
        ])
        case_list.append(case_conf)
		#证券行情列表
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'QUOTE_1'
        case_conf.continueWhenFailed = False
        case_conf.roundIntervalSec = 3
        case_conf.paramStrs.extend([
            #001
        	json.dumps({
        		'CODES': '841003.bj,841004.bj,841005.bj,841006.bj,832397.bj',
        	}),    
        ])
        case_list.append(case_conf)
		#分类排行
        case_list.append(case_conf)
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'CATESORTING_2'
        case_conf.roundIntervalSec = 3
        case_conf.continueWhenFailed = False
        case_conf.paramStrs.extend([		
            #001交易状态
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,50,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#002代码
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,50,1,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #003最新
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,50,7,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #004最高
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,50,8,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #005最低
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,50,9,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #006开盘
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,50,10,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#007昨收
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,50,11,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#008涨跌
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,50,19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),          
            #009涨跌幅
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,50,-3,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #010成交量
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,50,13,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}), 
            #011当前成交量
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,50,14,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),	
            #012换手率
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,50,15,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),			
            #013成交额
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,50,20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),                     
			#014量比
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,50,21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}), 
            #015外盘
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,50,24,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),			
			#016内盘
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,50,25,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#017总市值
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,50,26,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),            
			#018流通市值
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,50,27,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),            
			#019净资产
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,50,28,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),            
			#020动态市盈率
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,50,29,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #021静态市盈率
            json.dumps({
        		'id': 'BJ1000',
        		'param': '0,50,42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),			
            #022市净率
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,50,30,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #023总股本
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,50,31,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),           
            #024流通股
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,50,32,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),          
            #025振幅比率
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,50,37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),          
            #026动态每股收益
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,50,38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#027委比
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,50,53,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#028委差
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,50,54,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#029委比
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '0,50,53,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#030委差
        	json.dumps({
        		'id': 'BJ1000',
        		'param': '10,50,54,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#031交易状态
            json.dumps({
        		'id': 'BJ1001',
        		'param': '0,50,0,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#032代码
        	json.dumps({
        		'id': 'BJ1002',
        		'param': '0,50,1,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #033最新
        	json.dumps({
        		'id': 'BJ1003',
        		'param': '0,50,7,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #034最高
        	json.dumps({
        		'id': 'BJ1004',
        		'param': '0,50,8,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #035最低
        	json.dumps({
        		'id': 'BJ1005',
        		'param': '0,50,9,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #036开盘
        	json.dumps({
        		'id': 'BJ1006',
        		'param': '0,50,10,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#037昨收
        	json.dumps({
        		'id': 'BJ1007',
        		'param': '0,50,11,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#038涨跌
        	json.dumps({
        		'id': 'BJ1008',
        		'param': '0,50,19,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),          
            #039涨跌幅
        	json.dumps({
        		'id': 'BJ1009',
        		'param': '0,50,-3,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #040成交量
        	json.dumps({
        		'id': 'BJ1010',
        		'param': '0,50,13,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}), 
            #041当前成交量
        	json.dumps({
        		'id': 'BJ1011',
        		'param': '0,50,14,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),	
            #042换手率
        	json.dumps({
        		'id': 'BJ1012',
        		'param': '0,50,15,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),			
            #043成交额
        	json.dumps({
        		'id': 'BJ1400',
        		'param': '0,50,20,0,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#044交易状态
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,50,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#045代码
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,50,1,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #046最新
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,50,7,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #047最高
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,50,8,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #048最低
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,50,9,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #049开盘
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,50,10,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#050昨收
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,50,11,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#051涨跌
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,50,19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),          
            #052涨跌幅
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,50,-3,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #053成交量
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,50,13,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}), 
            #054当前成交量
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,50,14,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),	
            #055换手率
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,50,15,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),			
            #056成交额
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,50,20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),                     
			#057量比
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,50,21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}), 
            #058外盘
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,50,24,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),			
			#059内盘
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,50,25,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#060总市值
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,50,26,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),            
			#061流通市值
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,50,27,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),            
			#062净资产
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,50,28,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),            
			#063动态市盈率
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,50,29,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #064静态市盈率
            json.dumps({
        		'id': 'BJ1013',
        		'param': '0,50,42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),			
            #065市净率
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,50,30,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #066总股本
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,50,31,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),           
            #067流通股
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,50,32,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),          
            #068振幅比率
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,50,37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),          
            #069动态每股收益
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,50,38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#070委比
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,50,53,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#071委差
        	json.dumps({
        		'id': 'BJ1013',
        		'param': '0,50,54,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#072交易状态
            json.dumps({
        		'id': 'BJ101301',
        		'param': '0,50,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}), 
			#073交易状态
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,50,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#074代码
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,50,1,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #075最新
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,50,7,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #076最高
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,50,8,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #077最低
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,50,9,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #078开盘
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,50,10,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#079昨收
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,50,11,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#080涨跌
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,50,19,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),          
            #081涨跌幅
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,50,-3,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #082成交量
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,50,13,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}), 
            #083当前成交量
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,50,14,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),	
            #084换手率
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,50,15,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),			
            #085成交额
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,50,20,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),                     
			#086量比
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,50,21,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}), 
            #087外盘
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,50,24,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),			
			#088内盘
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,50,25,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#089总市值
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,50,26,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),            
			#090流通市值
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,50,27,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),            
			#091净资产
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,50,28,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),            
			#092动态市盈率
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,50,29,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #093静态市盈率
            json.dumps({
        		'id': 'BJ101302',
        		'param': '0,50,42,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),			
            #094市净率
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,50,30,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
            #095总股本
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,50,31,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),           
            #096流通股
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,50,32,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),          
            #097振幅比率
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,50,37,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),          
            #098动态每股收益
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,50,38,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#099委比
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,50,53,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#100委差
        	json.dumps({
        		'id': 'BJ101302',
        		'param': '0,50,54,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#101股票状态
            json.dumps({
        		'id': 'BJ1014',
        		'param': '0,50,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#102股票状态
            json.dumps({
        		'id': 'BJ101401',
        		'param': '0,50,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#103股票状态
            json.dumps({
        		'id': 'BJ101402',
        		'param': '0,50,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#104股票状态
            json.dumps({
        		'id': 'BJ1015',
        		'param': '0,50,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#105股票状态
            json.dumps({
        		'id': 'BJ101501',
        		'param': '0,50,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#106股票状态
            json.dumps({
        		'id': 'BJ101502',
        		'param': '0,50,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),
			#107股票状态
            json.dumps({
        		'id': 'BJ101503',
        		'param': '0,50,0,1,1',
                'quoteCustom': '-1',
        		'addvalueCustom': '-1',
        	}),			         			
        ])
        case_list.append(case_conf)
        #走势数据
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'CHARTV2TEST_2'
        case_conf.continueWhenFailed = False
        case_conf.roundIntervalSec = 3
        case_conf.paramStrs.extend([
            #001
        	json.dumps({
        		'CODES': '839068.bj',
        		'Chart_Types': 'ChartTypeOneDay',       
        	}),
			#002
        	json.dumps({
        		'CODES': '839068.bj',
        		'Chart_Types': 'ChartTypeFiveDay',       
        	}),  
        ])
        case_list.append(case_conf)
        #分时明细
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'TICK_1'
        case_conf.continueWhenFailed = False
        case_conf.roundIntervalSec = 3
        case_conf.paramStrs.extend([
            #001
        	json.dumps({
        		'CODES': '832397.bj',
        		'PAGES': '0,100,-1',  
				'SUBTYPES': '1000',      
        	}),
        ])
        case_list.append(case_conf)

        runner_conf.casesConfig.extend(case_list)
        print('i,case_list.length is ', case_list.__len__())
        runner_conf_list.append(runner_conf)

    return runner_conf_list


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 11, 28),
    'email': ['ss333@qq.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG( dag_id='test3', default_args=default_args,schedule_interval=timedelta(days=1))
       
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
    tag_id='release-20191202-0.0.2',
    tag_sha='0b0e32fe16c690957a7582d9f61bbc6d9eb3444e',
    runner_conf=runner_conf_list[0],
    dag=dag
)

android_a = AndroidRunnerOperator(
    task_id=task_id_to_cmp_list[0],
    provide_context=False,
    apk_id='com.chi.ssetest',
    apk_version='release-20191202-0.0.2',
    runner_conf=runner_conf_list[0],
    dag=dag
)

android_b = AndroidRunnerOperator(
    task_id=task_id_to_cmp_list[1],
    provide_context=False,
    apk_id='com.chi.ssetest',
    apk_version='release-20191202-0.0.2',
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
# ....................................a/i比较.......test2下面.............................