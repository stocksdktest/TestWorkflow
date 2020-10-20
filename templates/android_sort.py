import json

import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
from operators.data_sorting_operator import DataSortingOperator
from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig, Site
from operators.android_runner_operator import AndroidRunnerOperator
from operators.android_release_operator import AndroidReleaseOperator
from operators.data_compare_operator import DataCompareOperator
from init_config import initRunnerConfig
from init_config import initRunConf


params = {'Level_tmp':"1", 'HKPerms_tmp':["hk10"], 'collectionName_tmp':"test_result", 'roundIntervalSec_tmp':3, 'AirflowMethod':[
                {
                    'testcaseID': 'CATESORTING_2',
                    'paramStrs': [
                        {
                            'CateType': 'SH1133',
                            'param': '0,50,0,0,1',
                            'STOCKFIELDS': '-1',
                            'ADDVALUEFIELDS': '-1'
                        },
                        {
                            'CateType': 'SH1133',
                            'param': '0,50,0,1,1',
                            'STOCKFIELDS': '-1',
                            'ADDVALUEFIELDS': '-1'
                        }
                    ]
                }
            ], 'server':[
                {
                    'serverSites1': [
                        ["sh", "http://114.80.155.134:22016"],
                        ["tcpsh", "http://114.80.155.134:22017"],
                        ["shl2", "http://114.80.155.62:22016"],
                    ]
                },
                {
                    'serverSites2': [
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
#         HKPerms_tmp = ["hk10"]
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
#         print('Get Param AirflowMethod:', AirflowMethod)
#     else:
#         AirflowMethod = [
#             {
#                 'testcaseID': 'CATESORTING_2',
#                 'paramStrs': [
#                     {
#                         'CateType': 'SH1133',
#                         'param': '0,50,0,0,1',
#                         'STOCKFIELDS': '-1',
#                         'ADDVALUEFIELDS': '-1'
#                     },
#                     {
#                         'CateType': 'SH1133',
#                         'param': '0,50,0,1,1',
#                         'STOCKFIELDS': '-1',
#                         'ADDVALUEFIELDS': '-1'
#                     }
#                 ]
#             }
#         ]
#         print('Not Get Param AirflowMethod:', AirflowMethod)

#     server = conf.get('server')
#     if server is not None:
#         server=list(server)
#         print('Get Param server:', server)
#     else:
#         server = [
#             {
#                 'serverSites1': [
#                     ["sh", "http://114.80.155.134:22016"],
#                     ["tcpsh", "http://114.80.155.134:22017"],
#                     ["shl2", "http://114.80.155.62:22016"],
#                 ]
#             },
#             {
#                 'serverSites2': [
#                     ["sh", "http://114.80.155.134:22016"],
#                     ["tcpsh", "http://114.80.155.134:22017"],
#                     ["shl2", "http://114.80.155.62:22016"],
#                 ]
#             }
#         ]
#         print('Not Get Param server:', server)
#     serverSites1 = []
#     serverSites2 = []
#     if len(server) == 1:
#         serverSites1.extend(list(server[0].get('serverSites1')))
#         serverSites2.extend(serverSites1)
#     elif len(server) == 2:
#         for i in range(len(server)):
#             if i == 0:
#                 serverSites1.extend(list(server[0].get('serverSites1')))
#             if i == 1:
#                 serverSites2.extend(list(server[1].get('serverSites2')))

#     runner_conf_list = []

#     for i in range(2):
#         runner_conf = RunnerConfig()

#         runner_conf.sdkConfig.appKeyIOS = 'VVW0Fno7BEZt1a/y6KLM36uj9qcjw7CAHDwWZKDlWDs='
#         runner_conf.sdkConfig.appKeyAndroid = 'J6IPlk5AEU+2/Yi59rfYnsFQtdtOgAo9GAzysx8ciOM='
#         runner_conf.sdkConfig.marketPerm.Level = Level_tmp
#         runner_conf.sdkConfig.marketPerm.HKPerms.extend(HKPerms_tmp)
#         # mongoDB位置，存储的数据库位置
#         runner_conf.storeConfig.mongoUri = "mongodb://221.228.66.83:30617"
#         runner_conf.storeConfig.dbName = "stockSdkTest"
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

#         # case_list = []
#         # 测试样例
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
        dag_id='android_sort',
        default_args={
            'owner': 'jsj',
            'start_date': airflow.utils.dates.days_ago(0)
        },
        schedule_interval='@once',
) as dag:
    conf = dag.get_dagrun(execution_date=dag.latest_execution_date).conf

    # sdk版本配置
    tag = list(conf.get('tag'))
    if tag is not None:
        print('Get Param tag:', tag)
    else:
        tag = [['release-20200324-0.0.2', '9175a6e9a1147c9b82ccaa57b484b2ba906a8363']]
        print('Not Get Param tag:', tag)
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

    start_task = DummyOperator(
        task_id='run_this_first',
        queue='worker'
    )

    run_this_last = DummyOperator(
        task_id='run_this_lastok',
        queue='worker'
    )

    runner_conf_list = initRunnerConfig(conf, params)
    runner_conf_default = runner_conf_list[0]
    release_task_list = ['ReleaseOperator1', 'ReleaseOperator2']
    runner_task_list = ['RunnerOperator1', 'RunnerOperator2']
    sort_task_list = ['SortOperator1', 'SortOperator2']

    android_release1 = AndroidReleaseOperator(
        task_id=release_task_list[0],
        provide_context=False,
        repo_name='stocksdktest/AndroidTestRunner',
        tag_id=tag_id_1,
        tag_sha=tag_sha_1,
        runner_conf=runner_conf_list[0],
        release_xcom_key = "android_release_a"
    )

    android_release2 = AndroidReleaseOperator(
        task_id=release_task_list[1],
        provide_context=False,
        repo_name='stocksdktest/AndroidTestRunner',
        tag_id=tag_id_2,
        tag_sha=tag_sha_2,
        runner_conf=runner_conf_list[1],
        release_xcom_key = "android_release_b"
    )

    android_runner1 = AndroidRunnerOperator(
        task_id=runner_task_list[0],
        provide_context=False,
        apk_id='com.chi.ssetest',
        apk_version=tag_id_1,
        runner_conf=runner_conf_list[0],
        config_file=True,
        release_xcom_key = "android_release_a"
    )

    android_runner2 = AndroidRunnerOperator(
        task_id=runner_task_list[1],
        provide_context=False,
        apk_id='com.chi.ssetest',
        apk_version=tag_id_2,
        runner_conf=runner_conf_list[1],
        config_file=True,
        release_xcom_key = "android_release_b"
    )

    android_sort_a = DataSortingOperator(
        task_id=sort_task_list[0],
        from_task=runner_task_list[0],
        sort_and_comprae=True,
        retries=3,
        provide_context=False,
        runner_conf=runner_conf_default,
        dag=dag,
        release_xcom_key = "android_release_a"
    )

    android_sort_b = DataSortingOperator(
        task_id=sort_task_list[1],
        from_task=runner_task_list[1],
        sort_and_comprae=True,
        retries=3,
        provide_context=False,
        runner_conf=runner_conf_default,
        dag=dag,
        release_xcom_key = "android_release_b"
    )

    android_cmp = DataCompareOperator(
        task_id='data_compare',
        task_id_list=runner_task_list,
        sort_id_list=sort_task_list,
        sort_and_comprae=True,
        retries=3,
        provide_context=False,
        runner_conf=runner_conf_default,
        dag=dag
    )

    start_task >> [android_release1, android_release2]
    android_release1 >> android_runner1 >> android_sort_a
    android_release2 >> android_runner2 >> android_sort_b
    [android_sort_a, android_sort_b] >> android_cmp >> run_this_last

if __name__ == "__main__":
    dag.cli()