import unittest
import json
from airflow import DAG, settings
from datetime import datetime

from airflow.models import TaskInstance
from airflow.operators.python_operator import PythonOperator

from operators.data_compare_operator import DataCompareOperator
from operators.ios_release_operator import IOSReleaseOperator
from operators.ios_runner_operator import IOSRunnerOperator
from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig, Site
from utils import *


def get_test_runner_config_0(dbName, collectionName):
    runner_conf = RunnerConfig()
    runner_conf.jobID = 'TJ-1'
    runner_conf.runnerID = generate_id('RUN-A')
    runner_conf.storeConfig.mongoUri = 'mongodb://221.228.66.83:30617'
    runner_conf.storeConfig.dbName = dbName
    runner_conf.storeConfig.collectionName = collectionName
    runner_conf.storeConfig.restEndpoint = 'http://mongo-python-eve.sdk-test.svc.cluster.local:80'
    runner_conf.sdkConfig.appKeyIOS = 'VVW0Fno7BEZt1a/y6KLM36uj9qcjw7CAHDwWZKDlWDs='
    runner_conf.sdkConfig.appKeyAndroid = 'J6IPlk5AEU+2/Yi59rfYnsFQtdtOgAo9GAzysx8ciOM='

    runner_conf.sdkConfig.marketPerm.CffLevel = "1"
    runner_conf.sdkConfig.marketPerm.DceLevel = "2"
    runner_conf.sdkConfig.marketPerm.CzceLevel = "2"
    runner_conf.sdkConfig.marketPerm.FeLevel = "2"
    runner_conf.sdkConfig.marketPerm.GILevel = "2"
    runner_conf.sdkConfig.marketPerm.ShfeLevel = "2"
    runner_conf.sdkConfig.marketPerm.IneLevel = "2"
    runner_conf.sdkConfig.marketPerm.Level = "1"
    runner_conf.sdkConfig.marketPerm.HKPerms.extend(["hk10"])

    runner_conf.sdkConfig.serverSites["sh"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
    runner_conf.sdkConfig.serverSites["tcpsh"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
    runner_conf.sdkConfig.serverSites["shl2"].CopyFrom(Site(ips=["http://114.80.155.62:22016"]))

    case_conf = TestcaseConfig()
    case_conf.testcaseID = 'L2TICKDETAILV2_1'
    case_conf.continueWhenFailed = False
    case_conf.roundIntervalSec = 3
    case_conf.paramStrs.extend([
        json.dumps({
            "CODE": "000100.sz", "SUBTYPE": "1001"
        }),
        json.dumps({
            "CODE": "000078.sz", "SUBTYPE": "1001"
        }),
        json.dumps({
            "CODE": "002429.sz", "SUBTYPE": "1001"
        }),
    ])

    return runner_conf

# http://221.228.66.83:30690/admin/airflow/log?task_id=ios_cmp_b&dag_id=ios_compare2&execution_date=2020-09-11T09%3A32%3A33%2B00%3A00&format=json
def get_test_runer_config(dbName, collectionName):
    runner_conf = RunnerConfig()
    runner_conf.jobID = 'TJ-1'
    runner_conf.runnerID = generate_id('RUN-A')
    runner_conf.storeConfig.mongoUri = 'mongodb://221.228.66.83:30617'
    runner_conf.storeConfig.dbName = dbName
    runner_conf.storeConfig.collectionName = collectionName
    runner_conf.storeConfig.restEndpoint = 'http://mongo-python-eve.sdk-test.svc.cluster.local:80'
    runner_conf.sdkConfig.appKeyIOS = 'VVW0Fno7BEZt1a/y6KLM36uj9qcjw7CAHDwWZKDlWDs='
    runner_conf.sdkConfig.appKeyAndroid = 'J6IPlk5AEU+2/Yi59rfYnsFQtdtOgAo9GAzysx8ciOM='

    runner_conf.sdkConfig.marketPerm.CffLevel = "1"
    runner_conf.sdkConfig.marketPerm.DceLevel = "2"
    runner_conf.sdkConfig.marketPerm.CzceLevel = "2"
    runner_conf.sdkConfig.marketPerm.FeLevel = "2"
    runner_conf.sdkConfig.marketPerm.GILevel = "2"
    runner_conf.sdkConfig.marketPerm.ShfeLevel = "2"
    runner_conf.sdkConfig.marketPerm.IneLevel = "2"
    runner_conf.sdkConfig.marketPerm.Level = "2"
    runner_conf.sdkConfig.marketPerm.HKPerms.extend(["hk10"])

    AirflowMethod = [{'testcaseID': 'BANKUAISORTING_1', 'paramStrs': [{'SYMBOL': 'Trade', 'PARAMS': '0,10,s,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,jzf,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,zcje,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,zdjs,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,hsl,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,qzf,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,zlzjjlr,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,zlzjlr,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,zlzjlc,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,zlzjjlr5,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,zlzjjlr10,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,xcjl,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,zcjl,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,ggzf,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,ggzfb,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,ztjs,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,dtjs,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,zgb,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,kpj,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,zgj,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,zxj,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,zdj,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,wb,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,wc,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,wm3,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,wm4,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,zsj,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,zde,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,zf,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,zdf,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,szzh,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,lzzh,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,zdf5,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,zdf10,1'},
                                                                      {'SYMBOL': 'Trade', 'PARAMS': '0,10,lzg,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,s,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,jzf,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,zcje,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,zdjs,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,hsl,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,qzf,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,zlzjjlr,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,zlzjlr,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,zlzjlc,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,zlzjjlr5,1'},
                                                                      {'SYMBOL': 'Notion',
                                                                       'PARAMS': '0,10,zlzjjlr10,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,xcjl,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,zcjl,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,ggzf,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,ggzfb,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,ztjs,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,dtjs,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,zgb,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,kpj,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,zgj,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,zxj,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,zdj,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,wb,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,wc,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,wm3,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,wm4,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,zsj,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,zde,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,zf,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,zdf,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,szzh,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,lzzh,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,zdf5,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,zdf10,1'},
                                                                      {'SYMBOL': 'Notion', 'PARAMS': '0,10,lzg,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,s,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,jzf,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,zcje,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,zdjs,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,hsl,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,qzf,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,zlzjjlr,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,zlzjlr,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,zlzjlc,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,zlzjjlr5,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,zlzjjlr10,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,xcjl,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,zcjl,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,ggzf,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,ggzfb,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,ztjs,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,dtjs,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,zgb,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,kpj,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,zgj,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,zxj,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,zdj,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,wb,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,wc,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,wm3,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,wm4,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,zsj,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,zde,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,zf,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,zdf,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,szzh,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,lzzh,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,zdf5,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,zdf10,1'},
                                                                      {'SYMBOL': 'Area', 'PARAMS': '0,10,lzg,1'},
                                                                      {'SYMBOL': 'HKTrade', 'PARAMS': '0,10,s,1'},
                                                                      {'SYMBOL': 'Trade_sw', 'PARAMS': '0,10,wm4,1'},
                                                                      {'SYMBOL': 'Trade_sw', 'PARAMS': '0,10,zsj,1'},
                                                                      {'SYMBOL': 'Trade_sw', 'PARAMS': '0,10,zde,1'},
                                                                      {'SYMBOL': 'Trade_sw', 'PARAMS': '0,10,zf,1'},
                                                                      {'SYMBOL': 'Trade_sw', 'PARAMS': '0,10,zdf,1'},
                                                                      {'SYMBOL': 'Trade_sw', 'PARAMS': '0,10,szzh,1'},
                                                                      {'SYMBOL': 'Trade_sw', 'PARAMS': '0,10,lzzh,1'},
                                                                      {'SYMBOL': 'Trade_sw', 'PARAMS': '0,10,zdf5,1'},
                                                                      {'SYMBOL': 'Trade_sw', 'PARAMS': '0,10,zdf10,1'},
                                                                      {'SYMBOL': 'Trade_sw', 'PARAMS': '0,10,lzg,1'},
                                                                      {'SYMBOL': 'Trade_sw1', 'PARAMS': '0,10,s,1'},
                                                                      {'SYMBOL': 'Trade_sw1', 'PARAMS': '0,10,jzf,1'},
                                                                      {'SYMBOL': 'Trade_sw1', 'PARAMS': '0,10,zcje,1'},
                                                                      {'SYMBOL': 'Trade_sw1', 'PARAMS': '0,10,zdjs,1'},
                                                                      {'SYMBOL': 'Trade_sw1', 'PARAMS': '0,10,hsl,1'},
                                                                      {'SYMBOL': 'Trade_sw1', 'PARAMS': '0,10,qzf,1'},
                                                                      {'SYMBOL': 'Trade_sw1',
                                                                       'PARAMS': '0,10,zlzjjlr,1'},
                                                                      {'SYMBOL': 'Trade_sw1',
                                                                       'PARAMS': '0,10,zlzjlr,1'},
                                                                      {'SYMBOL': 'Trade_sw1',
                                                                       'PARAMS': '0,10,zlzjlc,1'},
                                                                      {'SYMBOL': 'Trade_sw1',
                                                                       'PARAMS': '0,10,zlzjjlr5,1'},
                                                                      {'SYMBOL': 'Trade_sw1',
                                                                       'PARAMS': '0,10,zlzjjlr10,1'},
                                                                      {'SYMBOL': 'Trade_sw1', 'PARAMS': '0,10,xcjl,1'},
                                                                      {'SYMBOL': 'Trade_sw1', 'PARAMS': '0,10,zcjl,1'},
                                                                      {'SYMBOL': 'Trade_sw1', 'PARAMS': '0,10,ggzf,1'},
                                                                      {'SYMBOL': 'Trade_sw1', 'PARAMS': '0,10,ggzfb,1'},
                                                                      {'SYMBOL': 'Trade_szyp',
                                                                       'PARAMS': '0,10,ggzfb,0'},
                                                                      {'SYMBOL': 'Trade_szyp', 'PARAMS': '0,10,ztjs,0'},
                                                                      {'SYMBOL': 'Trade_szyp', 'PARAMS': '0,10,dtjs,0'},
                                                                      {'SYMBOL': 'Trade_szyp', 'PARAMS': '0,10,zgb,0'},
                                                                      {'SYMBOL': 'Trade_szyp', 'PARAMS': '0,10,kpj,0'},
                                                                      {'SYMBOL': 'Trade_szyp', 'PARAMS': '0,10,zgj,0'},
                                                                      {'SYMBOL': 'Trade_szyp', 'PARAMS': '0,10,zxj,0'},
                                                                      {'SYMBOL': 'Trade_szyp', 'PARAMS': '0,10,zdj,0'},
                                                                      {'SYMBOL': 'Trade_szyp', 'PARAMS': '0,10,wb,0'},
                                                                      {'SYMBOL': 'Trade_szyp', 'PARAMS': '0,10,wc,0'},
                                                                      {'SYMBOL': 'Trade_szyp', 'PARAMS': '0,10,wm3,0'},
                                                                      {'SYMBOL': 'Trade_szyp', 'PARAMS': '0,10,wm4,0'},
                                                                      {'SYMBOL': 'Trade_szyp', 'PARAMS': '0,10,zsj,0'},
                                                                      {'SYMBOL': 'Trade_szyp', 'PARAMS': '0,10,zde,0'},
                                                                      {'SYMBOL': 'Trade_szyp', 'PARAMS': '0,10,zf,0'},
                                                                      {'SYMBOL': 'Trade_szyp', 'PARAMS': '0,10,zdf,0'},
                                                                      {'SYMBOL': 'Trade_szyp', 'PARAMS': '0,10,szzh,0'},
                                                                      {'SYMBOL': 'Trade_szyp', 'PARAMS': '0,10,lzzh,0'},
                                                                      {'SYMBOL': 'Trade_szyp', 'PARAMS': '0,10,zdf5,0'},
                                                                      {'SYMBOL': 'Trade_szyp',
                                                                       'PARAMS': '0,10,zdf10,0'},
                                                                      {'SYMBOL': 'Trade_szyp', 'PARAMS': '0,10,lzg,0'},
                                                                      {'SYMBOL': 'Area_szyp', 'PARAMS': '0,10,s,0'},
                                                                      {'SYMBOL': 'Area_szyp', 'PARAMS': '0,10,jzf,0'},
                                                                      {'SYMBOL': 'Area_szyp', 'PARAMS': '0,10,zcje,0'},
                                                                      {'SYMBOL': 'Area_szyp', 'PARAMS': '0,10,zdjs,0'},
                                                                      {'SYMBOL': 'Area_szyp', 'PARAMS': '0,10,hsl,0'},
                                                                      {'SYMBOL': 'Area_szyp', 'PARAMS': '0,10,qzf,0'},
                                                                      {'SYMBOL': 'Area_szyp', 'PARAMS': '0,10,dtjs,0'},
                                                                      {'SYMBOL': 'Area_szyp', 'PARAMS': '0,10,zgb,0'},
                                                                      {'SYMBOL': 'Area_szyp', 'PARAMS': '0,10,kpj,0'},
                                                                      {'SYMBOL': 'Area_szyp', 'PARAMS': '0,10,zgj,0'},
                                                                      {'SYMBOL': 'Area_szyp', 'PARAMS': '0,10,zxj,0'},
                                                                      {'SYMBOL': 'Area_szyp', 'PARAMS': '0,10,zdj,0'},
                                                                      {'SYMBOL': 'Area_szyp', 'PARAMS': '0,10,wb,0'},
                                                                      {'SYMBOL': 'Area_szyp', 'PARAMS': '0,10,wc,0'},
                                                                      {'SYMBOL': 'Area_szyp', 'PARAMS': '0,10,wm3,0'},
                                                                      {'SYMBOL': 'Area_szyp', 'PARAMS': '0,10,wm4,0'},
                                                                      {'SYMBOL': 'Area_szyp', 'PARAMS': '0,10,zsj,0'},
                                                                      {'SYMBOL': 'Area_szyp', 'PARAMS': '0,10,zde,0'},
                                                                      {'SYMBOL': 'Area_szyp', 'PARAMS': '0,10,zf,0'},
                                                                      {'SYMBOL': 'Area_szyp', 'PARAMS': '0,10,zdf,0'},
                                                                      {'SYMBOL': 'Area_szyp', 'PARAMS': '0,10,szzh,0'},
                                                                      {'SYMBOL': 'Area_szyp', 'PARAMS': '0,10,lzzh,0'},
                                                                      {'SYMBOL': 'Area_szyp', 'PARAMS': '0,10,zdf5,0'},
                                                                      {'SYMBOL': 'Area_szyp', 'PARAMS': '0,10,zdf10,0'},
                                                                      {'SYMBOL': 'Area_szyp', 'PARAMS': '0,10,lzg,0'},
                                                                      {'SYMBOL': 'Notion_szyp', 'PARAMS': '0,10,s,0'},
                                                                      {'SYMBOL': 'Notion_szyp', 'PARAMS': '0,10,jzf,0'},
                                                                      {'SYMBOL': 'Notion_szyp', 'PARAMS': '0,10,zcje,0'},
                                                                      {'SYMBOL': 'Notion_szyp',
                                                                       'PARAMS': '0,10,zdjs,0'},
                                                                      {'SYMBOL': 'Notion_szyp', 'PARAMS': '0,10,hsl,0'},
                                                                      {'SYMBOL': 'Notion_szyp', 'PARAMS': '0,10,qzf,0'},
                                                                      {'SYMBOL': 'Notion_szyp',
                                                                       'PARAMS': '0,10,zlzjjlr,0'},
                                                                      {'SYMBOL': 'Notion_szyp',
                                                                       'PARAMS': '0,10,zlzjlr,0'},
                                                                      {'SYMBOL': 'Notion_szyp',
                                                                       'PARAMS': '0,10,zlzjlc,0'},
                                                                      {'SYMBOL': 'Notion_szyp',
                                                                       'PARAMS': '0,10,zlzjjlr5,0'},
                                                                      {'SYMBOL': 'Notion_szyp',
                                                                       'PARAMS': '0,10,zlzjjlr10,0'},
                                                                      {'SYMBOL': 'Notion_szyp',
                                                                       'PARAMS': '0,10,xcjl,0'},
                                                                      {'SYMBOL': 'Notion_szyp',
                                                                       'PARAMS': '0,10,zcjl,0'},
                                                                      {'SYMBOL': 'Notion_szyp',
                                                                       'PARAMS': '0,10,ggzf,0'},
                                                                      {'SYMBOL': 'Notion_szyp',
                                                                       'PARAMS': '0,10,ggzfb,0'},
                                                                      {'SYMBOL': 'Notion_szyp',
                                                                       'PARAMS': '0,10,ztjs,0'},
                                                                      {'SYMBOL': 'Notion_szyp',
                                                                       'PARAMS': '0,10,dtjs,0'},
                                                                      {'SYMBOL': 'Notion_szyp', 'PARAMS': '0,10,zgb,0'},
                                                                      {'SYMBOL': 'Notion_szyp', 'PARAMS': '0,10,kpj,0'},
                                                                      {'SYMBOL': 'Notion_szyp', 'PARAMS': '0,10,zgj,0'},
                                                                      {'SYMBOL': 'Notion_szyp', 'PARAMS': '0,10,zxj,0'},
                                                                      {'SYMBOL': 'Notion_szyp', 'PARAMS': '0,10,zdj,0'},
                                                                      {'SYMBOL': 'Notion_szyp', 'PARAMS': '0,10,wb,0'},
                                                                      {'SYMBOL': 'Notion_szyp', 'PARAMS': '0,10,wc,0'},
                                                                      {'SYMBOL': 'Notion_szyp', 'PARAMS': '0,10,wm3,0'},
                                                                      {'SYMBOL': 'Notion_szyp', 'PARAMS': '0,10,wm4,0'},
                                                                      {'SYMBOL': 'Notion_szyp', 'PARAMS': '0,10,zsj,0'},
                                                                      {'SYMBOL': 'Notion_szyp', 'PARAMS': '0,10,zde,0'},
                                                                      {'SYMBOL': 'Notion_szyp', 'PARAMS': '0,10,zf,0'},
                                                                      {'SYMBOL': 'Notion_szyp', 'PARAMS': '0,10,zdf,0'},
                                                                      {'SYMBOL': 'Notion_szyp',
                                                                       'PARAMS': '0,10,szzh,0'},
                                                                      {'SYMBOL': 'Notion_szyp',
                                                                       'PARAMS': '0,10,lzzh,0'},
                                                                      {'SYMBOL': 'Notion_szyp',
                                                                       'PARAMS': '0,10,zdf5,0'},
                                                                      {'SYMBOL': 'Notion_szyp',
                                                                       'PARAMS': '0,10,zdf10,0'},
                                                                      {'SYMBOL': 'Notion_szyp',
                                                                       'PARAMS': '0,10,lzg,0'}]}]

    server = {'serverSites1': [
        ['sh', 'http://222.73.139.202:22016', 'tcp://222.73.139.202:22017'],
        ['sz', 'http://222.73.139.202:22016', 'tcp://222.73.139.202:22017'],
        ['shl2', 'http://222.73.139.209:22016', 'tcp://222.73.139.209:22017'],
        ['szl2', 'http://222.73.139.210:22016', 'tcp://222.73.139.210:22017'],
        ['hk10', 'http://222.73.139.208:22016', 'tcp://222.73.139.208:22017'],
        ['pb', 'http://222.73.139.202:22016'], ['bj', 'http://222.73.139.202:22016'],
        ['cf', 'http://222.73.139.202:22016']]}

    sites1 = server['serverSites1']
    for site in sites1:
        runner_conf.sdkConfig.serverSites[site[0]].CopyFrom(Site(ips=[site[1]]))

    paramStrs = AirflowMethod[0]['paramStrs']
    paramStrs_update = []
    for i in paramStrs:
        paramStrs_update.append(json.dumps(i))


    case_conf = TestcaseConfig()
    case_conf.testcaseID = 'BANKUAISORTING_1'
    case_conf.continueWhenFailed = False
    case_conf.roundIntervalSec = 3
    case_conf.paramStrs.extend(paramStrs_update)

    return runner_conf


def test_ios_runner():
    dbName = 'stockSdkTest'
    collectionName = 'test_result'
    runner_conf = get_test_runer_config(dbName=dbName, collectionName=collectionName)

    with DAG(dag_id='test_ios_runner', start_date=datetime.now()) as dag:
        ios_release = IOSReleaseOperator(
            task_id='release',
            provide_context=False,
            repo_name='stocksdktest/IOSTestRunner',
            tag_id='release-20200324-0.0.2',
            tag_sha='ef7cc138ad1d620302b5e5675c0710d0',
            runner_conf=runner_conf
        )

        ios_runner = IOSRunnerOperator(
            task_id='runner',
            provide_context=False,
            app_version='release-20200324-0.0.2',
            runner_conf=runner_conf,
            config_file=True

        )

        ios_release >> ios_runner

        execution_date = datetime.now()

        release_instance = TaskInstance(task=ios_release, execution_date=execution_date)
        ios_release.execute(release_instance.get_template_context())

        runner_instance = TaskInstance(task=ios_runner, execution_date=execution_date)
        context = runner_instance.get_template_context()
        context['run_id'] = 'test_ios_runner-test-run'
        ios_runner.pre_execute(context)
        result = ios_runner.execute(context)

    return result


# class TestIOSRunnerOperator(unittest.TestCase):
#
#     def test_data_compare_task_by_xcom(self):
#         result = test_data_compare_quote()

if __name__ == '__main__':
    result = test_ios_runner()

    # import paramiko
    #
    # OSX_HOSTNAME = '221.228.66.83'
    # OSX_PORT = 30753
    # OSX_USER_ID = 'test-env'
    # OSX_UESR_PWD = 'test-env'
    # SSH_TIMEOUT = 20
    #
    # ssh_client = paramiko.SSHClient()
    # ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh_client.connect(hostname=OSX_HOSTNAME, port=OSX_PORT, username=OSX_USER_ID, password=OSX_UESR_PWD,
    #                         timeout=SSH_TIMEOUT)
    # stdin, stdout, stderr = ssh_client.exec_command('echo "ok"')
