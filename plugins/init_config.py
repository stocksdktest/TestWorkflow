import json

import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

from operators.crawler.runner_operator import CrawlerRunnerOperator
from operators.data_sorting_operator import DataSortingOperator
from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig, Site
from operators.android_runner_operator import AndroidRunnerOperator
from operators.android_release_operator import AndroidReleaseOperator
from operators.data_compare_operator import DataCompareOperator


def initRunConf(Level_tmp, HKPerms_tmp, collectionName_tmp, roundIntervalSec_tmp, serverSites1, serverSites2, AirflowMethod, caseID, i):
    runner_conf = RunnerConfig()
    runner_conf.sdkConfig.appKeyIOS = 'VVW0Fno7BEZt1a/y6KLM36uj9qcjw7CAHDwWZKDlWDs='
    runner_conf.sdkConfig.appKeyAndroid = 'J6IPlk5AEU+2/Yi59rfYnsFQtdtOgAo9GAzysx8ciOM='
    runner_conf.sdkConfig.marketPerm.Level = Level_tmp
    runner_conf.sdkConfig.marketPerm.HKPerms.extend(HKPerms_tmp)
    # mongoDB位置，存储的数据库位置
    runner_conf.storeConfig.mongoUri = 'mongodb://221.228.66.83:30617'
    runner_conf.storeConfig.dbName = 'stockSdkTest'
    runner_conf.storeConfig.restEndpoint = 'http://mongo-python-eve.sdk-test.svc.cluster.local:80'
    runner_conf.storeConfig.collectionName = collectionName_tmp
    if i == 0:
        # 各个环境的站点配置
        for i in serverSites1:
            i = list(i)
            runner_conf.sdkConfig.serverSites[i[0]].CopyFrom(Site(ips=[i[1]]))
        print('Get Param serverSites1:', serverSites1)
    else:
        # 生产站点
        for i in serverSites2:
            i = list(i)
            runner_conf.sdkConfig.serverSites[i[0]].CopyFrom(Site(ips=[i[1]]))
        print('Get Param serverSites2:', serverSites2)
    # 测试样例
    # case_list = []
    for case in AirflowMethod:
        case_conf = TestcaseConfig()
        case_conf.continueWhenFailed = True
        case_conf.roundIntervalSec = roundIntervalSec_tmp
        testcaseID = case.get('testcaseID')
        paramStrs = case.get('paramStrs')
        if testcaseID is not None:
            case_conf.testcaseID = testcaseID
            print('Get Param testcaseID:', testcaseID)
        else:
            # case_conf.testcaseID = 'CHARTV2TEST_1'
            # case_conf.testcaseID = params['testcaseID']
            case_conf.testcaseID = caseID
            print('Not Get Param testcaseID:', testcaseID)
        if paramStrs is not None:
            paramStrs_update = []
            for i in paramStrs:
                paramStrs_update.append(json.dumps(i))
            case_conf.paramStrs.extend(paramStrs_update)
            print('Get Param paramStrs:', paramStrs_update)
        else:
            case_conf.paramStrs.extend([])
            print('Not Get Param paramStrs:', paramStrs)
        runner_conf.casesConfig.extend([case_conf])
    return runner_conf
    # print('i,case_list.length is ', case_list.__len__())
    # runner_conf_list.append(runner_conf)



# params：dict
def initRunnerConfig(conf, params):
    Level_tmp = conf.get('Level')
    if Level_tmp is not None:
        print('Get Param Level:', Level_tmp)
    else:
        Level_tmp = params['Level_tmp']
        print('Not Get Param Level:', Level_tmp)
    HKPerms_tmp = list(conf.get('HKPerms'))
    if HKPerms_tmp is not None:
        print('Get Param HKPerms:', HKPerms_tmp)
    else:
        HKPerms_tmp = params['HKPerms_tmp']
        print('Not Get Param HKPerms:', HKPerms_tmp)
    collectionName_tmp = conf.get('collectionName')
    if collectionName_tmp is not None:
        print('Get Param collectionName:', collectionName_tmp)
    else:
        collectionName_tmp = params['collectionName_tmp']
        print('Not Get Param collectionName:', collectionName_tmp)
    roundIntervalSec_tmp = conf.get('roundIntervalSec')
    if roundIntervalSec_tmp is not None:
        roundIntervalSec_tmp = int(roundIntervalSec_tmp)
        print('Get Param roundIntervalSec:', roundIntervalSec_tmp)
    else:
        roundIntervalSec_tmp = params['roundIntervalSec_tmp']
        print('Not Get Param roundIntervalSec:', roundIntervalSec_tmp)
    AirflowMethod = conf.get('AirflowMethod')
    if AirflowMethod is not None:
        AirflowMethod = list(AirflowMethod)
        print('Get Param AirflowMethod:',AirflowMethod)
    else:
        # AirflowMethod=[
        #         {
        #             'testcaseID': 'CRAWLER_CHARTV2TEST_2',
        #             'paramStrs': [
        #                 {
        #                     'CODE_A': '600000.sh',
        #                     'CODE_P': '600000.sh',
        #                     'SUBTYPE': 'SH1001',
        #                     'TYPE': 'ChartTypeBeforeData',
        #                     'DURATION_SECONDS': 60,
        #                 }
        #             ]
        #         }
        #     ]
        AirflowMethod = params['AirflowMethod']
        print('Not Get Param AirflowMethod:',AirflowMethod)
    server=conf.get('server')
    if server is not None:
        server = list(server)
        print('Get Param server:', server)
    else:
        # server=[
        #             {
        #                 serverSites1:[
        #                     ["sh", "http://114.80.155.134:22016"],
        #                     ["tcpsh", "http://114.80.155.134:22017"],
        #                     ["shl2", "http://114.80.155.62:22016"],
        #                 ]
        #             },
        #             {
        #                 serverSites2:[]
        #             }
        #         ]
        server = params['server']
        print('Not Get Param server:', server)

    caseID = params['testcaseID']
    runner_conf_list = []
    if len(server) == 1:
        serverSites1 = list(server[0].get('serverSites1'))
        serverSites2=serverSites1
        runner_conf = initRunConf(Level_tmp, HKPerms_tmp, collectionName_tmp, roundIntervalSec_tmp, serverSites1, serverSites2, AirflowMethod, caseID, 0)
        return runner_conf
    elif len(server) == 2:
        for i in range(len(server)):
            if i==0:
                serverSites1=list(server[0].get('serverSites1'))
            if i==1:
                serverSites2=list(server[1].get('serverSites2'))
        for j in range(2):
            runner_conf = initRunConf(Level_tmp, HKPerms_tmp, collectionName_tmp, roundIntervalSec_tmp, serverSites1, serverSites2, AirflowMethod, caseID, j)
            runner_conf_list.append(runner_conf)
        return runner_conf_list
    return runner_conf_list