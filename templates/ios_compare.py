import json
from datetime import timedelta

import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator

from operators.data_compare_operator import DataCompareOperator, generate_id
from operators.ios_release_operator import IOSReleaseOperator
from operators.ios_runner_operator import IOSRunnerOperator
from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig, Site
from init_config import initRunnerConfig
from init_config import initRunConf


params = {'Level_tmp':"1", 'HKPerms_tmp':["hk10"], 'collectionName_tmp':"test_result", 'roundIntervalSec_tmp':3, 'AirflowMethod':[
                {
                    'testcaseID': 'CATESORTING_2',
                    'paramStrs': [
                        {
                            'testcaseID': 'CHARTV2TEST_1',
                            'paramStrs': [
                                {
                                    'CODE': '600000.sh',
                                    'TYPE': 'ChartTypeOneDay',
                                    'SUBTYPE': '1001'
                                }
                            ]
                        }
                    ]
                }
            ], 'server':[
                {
                    'serverSites1':[
                        ["sh", "http://114.80.155.134:22016"],
                        ["tcpsh", "http://114.80.155.134:22017"],
                        ["shl2", "http://114.80.155.62:22016"],
                    ]
                },
                {
                    'serverSites2':[
                        ["sh", "http://114.80.155.134:22016"],
                        ["tcpsh", "http://114.80.155.134:22017"],
                        ["shl2", "http://114.80.155.62:22016"],
                    ]
                }
            ], 'testcaseID':"CHARTV2TEST_1"}

# def initRunnerConfig(conf):
#     # 市场权限
#     Level_tmp = conf.get('Level')
#     if Level_tmp is not None:
#         print('Get Param Level:', Level_tmp)
#     else:
#         Level_tmp = "1"
#         print('Not Get Param Level:', Level_tmp)
#     HKPerms_tmp = list(conf.get('HKPerms'))
#     if HKPerms_tmp is not None:
#         print('Get Param HKPerms:', HKPerms_tmp)
#     else:
#         HKPerms_tmp=["hk10"]
#         print('Not Get Param HKPerms:', HKPerms_tmp)
#     collectionName_tmp = conf.get('collectionName')
#     if collectionName_tmp is not None:
#         print('Get Param collectionName:', collectionName_tmp)
#     else:
#         collectionName_tmp = "test_result"
#         print('Not Get Param collectionName:', collectionName_tmp)
#     roundIntervalSec_tmp = int(conf.get('roundIntervalSec'))
#     if roundIntervalSec_tmp is not None:
#         print('Get Param roundIntervalSec:', roundIntervalSec_tmp)
#     else:
#         roundIntervalSec_tmp = 3
#         print('Not Get Param roundIntervalSec:', roundIntervalSec_tmp)
#     AirflowMethod = list(conf.get('AirflowMethod'))
#     if AirflowMethod is not None:
#         print('Get Param AirflowMethod:',AirflowMethod)
#     else:
#         AirflowMethod=[
#                 {
#                     'testcaseID': 'CHARTV2TEST_1',
#                     'paramStrs': [
#                         {
#                             'CODE': '600000.sh',
#                             'TYPE': 'ChartTypeOneDay',
#                             'SUBTYPE': '1001'
#                         }
#                     ]
#                 }
#             ]
#         print('Not Get Param AirflowMethod:',AirflowMethod)
#     server=list(conf.get('server'))
#     if server is not None:
#         print('Get Param server:', server)
#     else:
#         server=[
#                     {
#                         serverSites1:[
#                             ["sh", "http://114.80.155.134:22016"],
#                             ["tcpsh", "http://114.80.155.134:22017"],
#                             ["shl2", "http://114.80.155.62:22016"],
#                         ]
#                     },
#                     {
#                         serverSites2:[
#                             ["sh", "http://114.80.155.134:22016"],
#                             ["tcpsh", "http://114.80.155.134:22017"],
#                             ["shl2", "http://114.80.155.62:22016"],
#                         ]
#                     }
#                 ]
#         print('Not Get Param server:', server)
#     if len(server) == 1:
#         serverSites1 = list(server[0].get('serverSites1'))
#         serverSites2=serverSites1
#     elif len(server) == 2:
#         for i in range(len(server)):
#             if i==0:
#                 serverSites1=list(server[0].get('serverSites1'))
#             if i==1:
#                 serverSites2=list(server[1].get('serverSites2'))

#     runner_conf_list = []
#     for i in range(2):
#         runner_conf = RunnerConfig()

#         runner_conf.sdkConfig.appKeyIOS = 'VVW0Fno7BEZt1a/y6KLM36uj9qcjw7CAHDwWZKDlWDs='
#         runner_conf.sdkConfig.appKeyAndroid = 'J6IPlk5AEU+2/Yi59rfYnsFQtdtOgAo9GAzysx8ciOM='
#         runner_conf.sdkConfig.marketPerm.Level = Level_tmp
#         runner_conf.sdkConfig.marketPerm.HKPerms.extend(HKPerms_tmp)
#         # mongoDB位置，存储的数据库位置
#         runner_conf.storeConfig.mongoUri = 'mongodb://221.228.66.83:30617'
#         runner_conf.storeConfig.dbName = 'stockSdkTest'
#         runner_conf.storeConfig.restEndpoint = 'http://mongo-python-eve.sdk-test.svc.cluster.local:80'
#         runner_conf.storeConfig.collectionName = collectionName_tmp
#         if i == 0:
#             # 各个环境的站点配置
#             for i in serverSites1:
#                 i = list(i)
#                 runner_conf.sdkConfig.serverSites[i[0]].CopyFrom(Site(ips=[i[1]]))
#             print('Get Param serverSites1:', serverSites1)
#         else:
#             # 生产站点
#             for i in serverSites2:
#                 i = list(i)
#                 runner_conf.sdkConfig.serverSites[i[0]].CopyFrom(Site(ips=[i[1]]))
#             print('Get Param serverSites2:', serverSites2)
#         # 测试样例
#         # case_list = []
#         for case in AirflowMethod:
#             case_conf = TestcaseConfig()
#             case_conf.continueWhenFailed = True
#             case_conf.roundIntervalSec = roundIntervalSec_tmp
#             testcaseID = case.get('testcaseID')
#             paramStrs = case.get('paramStrs')
#             if testcaseID is not None:
#                 case_conf.testcaseID = testcaseID
#                 print('Get Param testcaseID:', testcaseID)
#             else:
#                 case_conf.testcaseID = 'CHARTV2TEST_1'
#                 print('Not Get Param testcaseID:', testcaseID)
#             if paramStrs is not None:
#                 paramStrs_update = []
#                 for i in paramStrs:
#                     paramStrs_update.append(json.dumps(i))
#                 case_conf.paramStrs.extend(paramStrs_update)
#                 print('Get Param paramStrs:', paramStrs_update)
#             else:
#                 case_conf.paramStrs.extend([])
#                 print('Not Get Param paramStrs:', paramStrs)
#             runner_conf.casesConfig.extend([case_conf])
#         # print('i,case_list.length is ', case_list.__len__())
#         runner_conf_list.append(runner_conf)
#     return runner_conf_list

with DAG(
        dag_id='ios_compare',  # 测试计划名称
        default_args={
            'owner': 'jsj',
            'start_date': airflow.utils.dates.days_ago(0)
        },
        schedule_interval='@once',
) as dag:
    conf = dag.get_dagrun(execution_date=dag.latest_execution_date).conf

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

    runner_conf_list = initRunnerConfig(conf, params)

    task_id_to_cmp_list = ['ios_cmp_a', 'ios_cmp_b']
    # sdk版本配置
    tag = list(conf.get('tag'))
    if tag is not None:
        print('Get Param tag:',tag)
    else:
        tag=[['release-20200324-0.0.2', '9175a6e9a1147c9b82ccaa57b484b2ba906a8363']]
        print('Not Get Param tag:',tag)
    if len(tag) == 1:
        tag_id_1 = tag[0][0]
        tag_id_2 = tag[0][0]
        tag_sha_1 = tag[0][1]
        tag_sha_2 = tag[0][1]
    else:
        tag_id_1 = tag[0][0]
        tag_id_2 = tag[1][0]
        tag_sha_1 = tag[0][1]
        tag_sha_2 = tag[1][1]

    run_times_tmp=int(conf.get('run_times'))
    if run_times_tmp is not None:
        print('Get Param run_times:',run_times_tmp)
    else:
        run_times_tmp=1
        print('Not Get Param run_times',run_times_tmp)

    quote_detail_tmp=bool(int(conf.get('quote_detail')))
    if quote_detail_tmp is not None:
        print('Get Param quote_detail:',quote_detail_tmp)
    else:
        quote_detail_tmp=True
        print('Not Get Param quote_detail:',quote_detail_tmp)

    ios_release_a = IOSReleaseOperator(
        task_id='ios_release_a',
        provide_context=False,
        repo_name='stocksdktest/IOSTestRunner',
        tag_id=tag_id_1,
        tag_sha=tag_sha_1,
        runner_conf=runner_conf_list[0],
        release_xcom_key = "ios_release_a"
    )
    
    ios_release_b = IOSReleaseOperator(
        task_id='ios_release_b',
        provide_context=False,
        repo_name='stocksdktest/IOSTestRunner',
        tag_id=tag_id_2,
        tag_sha=tag_sha_2,
        runner_conf=runner_conf_list[1],
        release_xcom_key = "ios_release_b"
    )

    ios_a = IOSRunnerOperator(
        task_id=task_id_to_cmp_list[0],
        provide_context=False,
		app_version=tag_id_1,
        config_file=True,
        runner_conf=runner_conf_list[0],
        run_times=run_times_tmp,
        release_xcom_key = "ios_release_a"
    )

    ios_b = IOSRunnerOperator(
        task_id=task_id_to_cmp_list[1],
        provide_context=False,
		app_version=tag_id_2,
        config_file=True,
        runner_conf=runner_conf_list[1],
        run_times=run_times_tmp,
        release_xcom_key = "ios_release_b"
    )

    runner_conf_cmp = runner_conf_list[0]

    ios_cmp = DataCompareOperator(
        task_id='data_compare',
        task_id_list=task_id_to_cmp_list,
        retries=3,
        provide_context=False,
        runner_conf=runner_conf_cmp,
        run_times=run_times_tmp,
        quote_detail=quote_detail_tmp,
        dag=dag
    )
    start_task >> [ios_release_a, ios_release_b] >> release_ok >> [ios_a,ios_b] >> ios_cmp >> run_this_last

if __name__ == "__main__":
    dag.cli()