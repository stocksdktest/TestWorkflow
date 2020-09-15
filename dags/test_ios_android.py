import json
from datetime import timedelta

import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator

from operators.android_runner_operator import AndroidRunnerOperator
from operators.data_compare_operator import DataCompareOperator, generate_id
from operators.ios_release_operator import IOSReleaseOperator
from operators.ios_runner_operator import IOSRunnerOperator
from operators.android_release_operator import AndroidReleaseOperator
from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig, Site


def gen2iOSCaseList():
    res = []
    for i in range(2):
        runner_conf = RunnerConfig()
        runner_conf.jobID = 'TJ-1'
        runner_conf.runnerID = generate_id('RUN-A')
        runner_conf.sdkConfig.appKeyIOS = 'VVW0Fno7BEZt1a/y6KLM36uj9qcjw7CAHDwWZKDlWDs='
        runner_conf.sdkConfig.appKeyAndroid = 'J6IPlk5AEU+2/Yi59rfYnsFQtdtOgAo9GAzysx8ciOM='
        runner_conf.sdkConfig.marketPerm.Level = "1"
        runner_conf.sdkConfig.marketPerm.HKPerms.extend(["hk10"])

        runner_conf.sdkConfig.serverSites["sh"].CopyFrom(Site(ips=["http://114.80.155.134:22016", "tcp://114.80.155.134:22017"]))
        runner_conf.sdkConfig.serverSites["tcpsh"].CopyFrom(Site(ips=["tcp://114.80.155.134:22017"]))
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
        runner_conf.sdkConfig.serverSites["hkdz"].CopyFrom(Site(ips=["http://114.80.155.61:7710"]))

        runner_conf.storeConfig.mongoUri = 'mongodb://221.228.66.83:30617'
        runner_conf.storeConfig.dbName = 'stockSdkTest'
        runner_conf.storeConfig.collectionName = 'test_result'
        runner_conf.storeConfig.restEndpoint = 'http://mongo-python-eve.sdk-test.svc.cluster.local:80'
        if i == 0 or i == 1:

            case_conf = TestcaseConfig()
            case_conf.testcaseID = 'QUOTEDETAIL_1'
            case_conf.continueWhenFailed = True
            case_conf.roundIntervalSec = 3
            case_conf.paramStrs.extend([
                json.dumps({
                    'CODE': '000001.sz'
                }),
                json.dumps({
                    'CODE': '000002.sz'
                }),
                json.dumps({
                    'CODE': '000004.sz'
                }),
                json.dumps({
                    'CODE': '000005.sz'
                }),
                json.dumps({
                    'CODE': '000006.sz'
                }),
                json.dumps({
                    'CODE': '000007.sz'
                }),
                json.dumps({
                    'CODE': '000008.sz'
                }),
                json.dumps({
                    'CODE': '600000.sh'
                }),
                json.dumps({
                    'CODE': '600004.sh'
                }),
                json.dumps({
                    'CODE': '600006.sh'
                }),
                json.dumps({
                    'CODE': '600007.sh'
                }),
                json.dumps({
                    'CODE': '600008.sh'
                }),
                json.dumps({
                    'CODE': '600009.sh'
                }),
                json.dumps({
                    'CODE': '600010.sh'
                }),
                json.dumps({
                    'CODE': '600011.sh'
                }),
                json.dumps({
                    'CODE': '600012.sh'
                }),
                json.dumps({
                    'CODE': '600015.sh'
                }),
                json.dumps({
                    'CODE': '200017.sz'
                }),
                json.dumps({
                    'CODE': '300014.sz'
                }),
                json.dumps({
                    'CODE': '300015.sz'
                }),
                json.dumps({
                    'CODE': '300026.sz'
                }),
                json.dumps({
                    'CODE': '688001.sh'
                }),
                json.dumps({
                    'CODE': '688002.sh'
                }),
                json.dumps({
                    'CODE': '688003.sh'
                }),
                json.dumps({
                    'CODE': '688005.sh'
                }),
                json.dumps({
                    'CODE': '688006.sh'
                }),
                json.dumps({
                    'CODE': '688007.sh'
                }),
                json.dumps({
                    'CODE': '688008.sh'
                }),
                json.dumps({
                    'CODE': '688009.sh'
                }),
                json.dumps({
                    'CODE': '000991.sz'
                }),
                json.dumps({
                    'CODE': '02800.hk'
                }),
                json.dumps({
                    'CODE': '02827.hk'
                }),
                json.dumps({
                    'CODE': '150008.sz'
                }),
                json.dumps({
                    'CODE': '150013.sz'
                }),
                json.dumps({
                    'CODE': '150019.sz'
                }),
                json.dumps({
                    'CODE': '150023.sz'
                }),
                json.dumps({
                    'CODE': '150029.sz'
                }),
                json.dumps({
                    'CODE': '150052.sz'
                }),
                json.dumps({
                    'CODE': '150095.sz'
                }),
                json.dumps({
                    'CODE': '150124.sz'
                }),
                json.dumps({
                    'CODE': '150149.sz'
                }),
                json.dumps({
                    'CODE': '150190.sz'
                }),
                json.dumps({
                    'CODE': '501000.sh'
                }),
                json.dumps({
                    'CODE': '501001.sh'
                }),
                json.dumps({
                    'CODE': '501005.sh'
                }),
                json.dumps({
                    'CODE': '501007.sh'
                }),
                json.dumps({
                    'CODE': '501008.sh'
                }),
                json.dumps({
                    'CODE': '501009.sh'
                }),
                json.dumps({
                    'CODE': '501010.sh'
                }),
                json.dumps({
                    'CODE': '501012.sh'
                }),
                json.dumps({
                    'CODE': '501012.sh'
                }),
                json.dumps({
                    'CODE': '501015.sh'
                }),
                json.dumps({
                    'CODE': '010107.sh'
                }),
                json.dumps({
                    'CODE': '010303.sh'
                }),
                json.dumps({
                    'CODE': '01687.hk'
                }),
                json.dumps({
                    'CODE': '018007.sh'
                }),
                json.dumps({
                    'CODE': '86620.hk'
                }),
                json.dumps({
                    'CODE': '86621.hk'
                }),
                json.dumps({
                    'CODE': '86624.hk'
                }),
                json.dumps({
                    'CODE': '52221.hk'
                }),
                json.dumps({
                    'CODE': '52238.hk'
                }),
                json.dumps({
                    'CODE': '56966.hk'
                }),
                json.dumps({
                    'CODE': '56983.hk'
                }),

            ])
            runner_conf.casesConfig.extend([case_conf])

            res.append(runner_conf)
        else:
            pass
        res.append(runner_conf)
        return res


with DAG(
        dag_id='ios_android_test',
        default_args={
            'owner': 'jc',
            'start_date': airflow.utils.dates.days_ago(0),
            # 'on_failure_callback': on_failure_callback,
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
        queue='android'
    )

    task_id_to_cmp_list1 = ['ios_test', 'android_test']

    runner_conf_list = gen2iOSCaseList()

    android_release = AndroidReleaseOperator(
        task_id='android_release',
        provide_context=False,
        repo_name='stocksdktest/AndroidTestRunner',
        tag_id='release-20200908-0.0.1',
        tag_sha='78dcf944420370d7c0726bae9bdd9e730ac6d192',
        runner_conf=runner_conf_list[0]
    )

    ios_release = IOSReleaseOperator(
        task_id='ios_release',
        provide_context=False,
        repo_name='stocksdktest/IOSTestRunner',
        tag_id='release-20200911-0.0.0',
        tag_sha='28feeb26f0aeccac7b01e5c992a7471a1e4352e4',
        runner_conf=runner_conf_list[0]
    )

    ios = IOSRunnerOperator(
        task_id=task_id_to_cmp_list1[0],
        provide_context=False,
        app_version='release-20200911-0.0.0',
        runner_conf=runner_conf_list[0],
        config_file=True,
        # run_times=30
    )

    android = AndroidRunnerOperator(
        task_id=task_id_to_cmp_list1[1],
        provide_context=False,
        apk_id='com.chi.ssetest',
        apk_version='release-20200908-0.0.1',
        runner_conf=runner_conf_list[1],
        config_file=True,
        # run_times=30
    )

    cmp_runner = runner_conf_list[1]

    ios_android_cmp = DataCompareOperator(
        task_id='data_compare',
        task_id_list=task_id_to_cmp_list1,
        retries=3,
        provide_context=False,
        runner_conf=cmp_runner,
        # run_times=30,
        dag=dag
    )

    start_task >> [ios_release, android_release] >> release_ok >> [ios, android] >> ios_android_cmp >> run_this_last

if __name__ == "__main__":
    dag.cli()

