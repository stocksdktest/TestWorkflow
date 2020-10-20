import json

import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
from operators.data_sorting_operator import DataSortingOperator
from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig, Site
from operators.ios_release_operator import IOSReleaseOperator
from operators.ios_runner_operator import IOSRunnerOperator


def initRunnerConfig(conf):
    # 市场权限
    Level_tmp = conf.get('Level')
    if Level_tmp is not None:
        print('Get Param Level:', Level_tmp)
    else:
        Level_tmp = "1"
        print('Not Get Param Level:', Level_tmp)
    HKPerms_tmp = conf.get('HKPerms')
    if HKPerms_tmp is not None:
        HKPerms_tmp = list(HKPerms_tmp)
        print('Get Param HKPerms:', HKPerms_tmp)
    else:
        HKPerms_tmp = ["hk10"]
        print('Not Get Param HKPerms:', HKPerms_tmp)
    collectionName_tmp = conf.get('collectionName')
    if collectionName_tmp is not None:
        print('Get Param collectionName:', collectionName_tmp)
    else:
        collectionName_tmp = "sort"
        print('Not Get Param collectionName:', collectionName_tmp)
    roundIntervalSec_tmp = conf.get('roundIntervalSec')
    if roundIntervalSec_tmp is not None:
        roundIntervalSec_tmp = int(roundIntervalSec_tmp)
        print('Get Param roundIntervalSec:', roundIntervalSec_tmp)
    else:
        roundIntervalSec_tmp = 3
        print('Not Get Param roundIntervalSec:', roundIntervalSec_tmp)

    AirflowMethod = conf.get('AirflowMethod')
    if AirflowMethod is not None:
        AirflowMethod = list(AirflowMethod)
        print('Get Param AirflowMethod:',AirflowMethod)
    else:
        AirflowMethod=[
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
            ]
        print('Not Get Param AirflowMethod:',AirflowMethod)

    server=conf.get('server')
    if server is not None:
        server=list(server)
        print('Get Param server:', server)
    else:
        server=[
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
                ]
        print('Not Get Param server:', server)
    if len(server) == 1:
        serverSites1 = list(server[0].get('serverSites1'))
        serverSites2=serverSites1
    elif len(server) == 2:
        for i in range(len(server)):
            if i==0:
                serverSites1=list(server[0].get('serverSites1'))
            if i==1:
                serverSites2=list(server[1].get('serverSites2'))

    runner_conf_list = []

    for i in range(2):
        runner_conf = RunnerConfig()

        runner_conf.sdkConfig.appKeyIOS = 'VVW0Fno7BEZt1a/y6KLM36uj9qcjw7CAHDwWZKDlWDs='
        runner_conf.sdkConfig.appKeyAndroid = 'J6IPlk5AEU+2/Yi59rfYnsFQtdtOgAo9GAzysx8ciOM='
        runner_conf.sdkConfig.marketPerm.Level = Level_tmp
        runner_conf.sdkConfig.marketPerm.HKPerms.extend(HKPerms_tmp)
        # mongoDB位置，存储的数据库位置
        runner_conf.storeConfig.mongoUri = "mongodb://221.228.66.83:30617"
        runner_conf.storeConfig.dbName = "stockSdkTest"
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
                case_conf.testcaseID = 'CHARTV2TEST_1'
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
        runner_conf_list.append(RunnerConfig())
    return runner_conf_list


with DAG(
        dag_id='ios_sort',
        default_args={
            'owner': 'jsj',
            'start_date': airflow.utils.dates.days_ago(0)
        },
        schedule_interval='@once',
) as dag:
    conf = dag.get_dagrun(execution_date=dag.latest_execution_date).conf

    # conf={
    #     'collectionName': 'Test_Android_quote_20200316',
    #     'Level': '2',
    #     'HKPerms': ['hk10'],
    #     'roundIntervalSec': '3',
    #     'tag': [['release-20200103-0.0.3', '53fcc717d954e01d88bc9bd70eaab9ac9a0acb67']],
    #     'run_times': '1',
    #     'quote_detail': '1',
    #     "AirflowMethod": [
    #         {
    #             'testcaseID': 'L2TICKDETAILV2_1',
    #             'paramStrs': [
    #                 {
    #                     'CODE': '000100.sz',
    #                     'SUBTYPE': '1001'
    #                 },
    #                 {
    #                     'CODE': '000078.sz',
    #                     'SUBTYPE': '1001'
    #                 },
    #                 {
    #                     'CODE': '002429.sz',
    #                     'SUBTYPE': '1001'
    #                 }
    #             ]
    #         }
    #     ],
    #     'server': [
    #         {
    #             'serverSites1': [
    #                 ["sh", "http://114.80.155.134:22016"],
    #                 ["tcpsh", "http://114.80.155.134:22017"],
    #                 ["shl2", "http://114.80.155.62:22016"],
    #             ]
    #         },
    #         {
    #             'serverSites2': [
    #                 ["sh", "http://114.80.155.134:22016"],
    #                 ["tcpsh", "http://114.80.155.134:22017"],
    #                 ["shl2", "http://114.80.155.62:22016"],
    #             ]
    #         }
    #     ]
    # }

    # sdk版本配置
    tag = conf.get('tag')
    if tag is not None:
        tag=list(tag)
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

    runner_conf_list = initRunnerConfig(conf)
    runner_conf_default = runner_conf_list[0]
    release_task_list = ['ReleaseOperator1', 'ReleaseOperator2']
    runner_task_list = ['RunnerOperator1', 'RunnerOperator2']

    start_task = DummyOperator(
        task_id='run_this_first',
        queue='worker'
    )

    run_this_last = DummyOperator(
        task_id='run_this_lastok',
        queue='worker'
    )

    ios_release1 = IOSReleaseOperator(
        task_id=release_task_list[0],
        provide_context=False,
        repo_name='stocksdktest/IOSTestRunner',
        tag_id=tag_id_1,
        tag_sha=tag_sha_1,
        runner_conf=runner_conf_list[0],
        release_xcom_key = "ios_release_a"
    )

    ios_release2 = IOSReleaseOperator(
        task_id=release_task_list[1],
        provide_context=False,
        repo_name='stocksdktest/IOSTestRunner',
        tag_id=tag_id_2,
        tag_sha=tag_sha_2,
        runner_conf=runner_conf_list[1],
        release_xcom_key = "ios_release_b"
    )

    ios_runner1 = IOSRunnerOperator(
        task_id=runner_task_list[0],
        provide_context=False,
        # apk_id='com.chi.ssetest',
        app_version=tag_id_1,
        runner_conf=runner_conf_list[0],
        config_file=True,
        run_times=100,
        release_xcom_key = "ios_release_a"
    )

    ios_runner2 = IOSRunnerOperator(
        task_id=runner_task_list[1],
        provide_context=False,
        # apk_id='com.chi.ssetest',
        app_version=tag_id_2,
        runner_conf=runner_conf_list[1],
        config_file=True,
        run_times=100,
        release_xcom_key = "ios_release_b"
    )

    ios_sort_1 = DataSortingOperator(
        task_id='SortOperator1',
        from_task=runner_task_list[0],
        retries=3,
        provide_context=False,
        runner_conf=runner_conf_default,
        dag=dag,
        release_xcom_key = "ios_release_a"
    )

    ios_sort_2 = DataSortingOperator(
        task_id='SortOperator2',
        from_task=runner_task_list[1],
        retries=3,
        provide_context=False,
        runner_conf=runner_conf_default,
        dag=dag,
        release_xcom_key = "ios_release_b"
    )

    start_task >> [ios_release1, ios_release2]
    ios_release1 >> ios_runner1 >> ios_sort_1
    ios_release2 >> ios_runner2 >> ios_sort_2
    [ios_sort_1, ios_sort_2] >> run_this_last

if __name__ == "__main__":
    dag.cli()
