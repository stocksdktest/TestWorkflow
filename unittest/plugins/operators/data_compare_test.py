
from operators.data_compare_operator import DataCompareOperator
from utils import *
from utils.mongo_hook import MongoHookWithDB

if __name__ == '__main__':
    mongo_hk = MongoHookWithDB(conn_id='stocksdktest_mongo')
    conn = mongo_hk.get_conn()
    myclient = mongo_hk.client
    mongo_reader = SdkMongoReader(client=myclient)
    dbName = 'stockSdkTest'
    collectionName = 'quotedetail'

    id1 = 'RUN--7d7acfc9-b3f5-4aec-a3ff-cb98ad8ec197'
    id2 = 'RUN--05da2757-a085-4b89-aa53-8e33526d9967'

    # r1, r2 = get_two_testresult()
    #
    from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig

    runner_conf = RunnerConfig()
    runner_conf.jobID = 'TJ-1'
    runner_conf.runnerID = generate_id('RUN-A')
    runner_conf.storeConfig.mongoUri = 'mongodb://221.228.66.83:30617'
    runner_conf.storeConfig.dbName = dbName
    runner_conf.storeConfig.collectionName = collectionName
    runner_conf.storeConfig.restEndpoint = 'http://mongo-python-eve.sdk-test.svc.cluster.local:80'

    # 测试样例
    import json
    case_conf = TestcaseConfig()
    case_conf.testcaseID = 'SEARTEST_1'
    case_conf.roundIntervalSec = 2
    case_conf.continueWhenFailed = False
    case_conf.paramStrs.extend([
        json.dumps({
            'MARKET': 'shszsdsd'
        }),
        json.dumps({
            'MARKET': 'sh'
        }),
    ])
    case_conf = TestcaseConfig()
    case_conf.testcaseID = 'QUOTEDETAIL_1'
    case_conf.continueWhenFailed = True
    case_conf.roundIntervalSec = 3
    # case_conf.paramStrs.extend([
    #     json.dumps({
    #         'CODE': '600000.sh',
    #     }),
    #     json.dumps({
    #         'CODE': '000001.sz',
    #     }),
    #     json.dumps({
    #         'CODE': '600425.sh',
    #     }),
    # ])
    for i in range(50):
        case_conf.paramStrs.extend([
            json.dumps({
                'CODE': '600000.sh',
            })
        ])
    for i in range(50):
        case_conf.paramStrs.extend([
            json.dumps({
                'CODE': '000001.sz',
            }),
        ])
    for i in range(50):
        case_conf.paramStrs.extend([
            json.dumps({
                'CODE': '600425.sh',
            }),
        ])

    runner_conf.casesConfig.extend([case_conf])

    a = DataCompareOperator(
        runner_conf=runner_conf,
        task_id='11',
        task_id_list=['a', 'b'],
        quote_detail=True
    )
    context = {}
    context['run_id'] = 'fake-run'
    context['expectation'] = 8
    context['unit_test'] = True
    res = a.execute(context)
    # print(res)
    # mongo_reader.synchronizer(runnerID1=id1,runnerID2=id2,dbName=dbName,collectionName=collectionName,expectation=602)
    # # mongo_reader.prepare_param(runnerID1=id1, runnerID2=id2, dbName=dbName, collectionName=collectionName)
    # exception = mongo_reader.get_exception(runnerID1=id1, runnerID2=id2, dbName=dbName, collectionName=collectionName)
    # group = mongo_reader.get_results(runnerID1=id1, runnerID2=id2, dbName=dbName, collectionName=collectionName)
    # group_resharp = mongo_reader.get_quote_results(runnerID1=id1, runnerID2=id2, dbName=dbName, collectionName=collectionName)
