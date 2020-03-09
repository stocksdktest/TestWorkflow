from airflow.utils.decorators import apply_defaults
from operators.stock_operator import StockOperator

from airflow.contrib.hooks.mongo_hook import MongoHook
from utils import *
from pymongo.errors import DocumentTooLarge
from collections import defaultdict
import sys


class DataCompareOperator(StockOperator):
    @apply_defaults
    def __init__(self, runner_conf, task_id_list, run_times=1, quote_detail = False, *args, **kwargs):
        super(DataCompareOperator, self).__init__(queue='worker', runner_conf=runner_conf, *args, **kwargs)
        self.task_id_list = task_id_list
        self.mongo_hk = MongoHook(conn_id='stocksdktest_mongo')
        self.conn = self.mongo_hk.get_conn()
        self.run_times = run_times
        self.quote_detail = quote_detail
        self.mongo_reader = SdkMongoReader(client=self.mongo_hk.client)

    def close_connection(self):
        self.mongo_hk.close_conn()

    def get_ios_data(self):
        return 0

    def get_android_data(self):
        return 0

    def execute(self, context):
        self.runner_conf = self.runner_conf_replicate(runner_conf=self.runner_conf,
                                                      replicate_numbers=self.run_times - 1)
        id1 = self.xcom_pull(context, key=self.task_id_list[0])
        id2 = self.xcom_pull(context, key=self.task_id_list[1])
        # # TODO: AD HOC
        # id1 = 'RUN--7d7acfc9-b3f5-4aec-a3ff-cb98ad8ec197'
        # id2 = 'RUN--05da2757-a085-4b89-aa53-8e33526d9967'
        print('xcom_pull', id1)
        print('xcom_pull', id2)
        print("-----------------------------Synchronize MongoDB--------------------------------")
        expectation = self.get_runner_conf_records()
        timeout = expectation * 5  # 一个case最多给10s的时间
        if timeout < 300:
            timeout = 300
        print('timeout(records to return) is {}'.format(timeout))
        self.mongo_reader.synchronizer(
            runnerID1=id1,
            runnerID2=id2,
            dbName=self.runner_conf.storeConfig.dbName,
            collectionName=self.runner_conf.storeConfig.collectionName,
            timeout=timeout,
            expectation=expectation
        )
        print("-----------------------------Prepare for paramData to paramStr--------------------------------")
        self.mongo_reader.prepare_param(
            runnerID1=id1,
            runnerID2=id2,
            dbName=self.runner_conf.storeConfig.dbName,
            collectionName=self.runner_conf.storeConfig.collectionName
        )
        print("-----------------------------Now Get Data From Mongo Directly--------------------------------")
        result = dict()  # 存储所有返回的结果
        cmp_result = dict()  # 比较的结果
        error_result = list()  # 异常的结果
        mismatch_result = list()  # 无法比较的结果
        empty_result = list()  # 返回为空的结果

        result['jobID'] = self.runner_conf.jobID
        result['dagID'] = self.dag_id
        result['runnerID1'] = id1
        result['runnerID2'] = id2
        result['compared'] = cmp_result
        result['error'] = error_result
        result['mismatch'] = mismatch_result
        result['empty'] = empty_result

        cmp_result['true'] = list()
        cmp_result['false'] = list()

        result_exception = self.mongo_reader.get_exception(
            runnerID1=id1,
            runnerID2=id2,
            dbName=self.runner_conf.storeConfig.dbName,
            collectionName=self.runner_conf.storeConfig.collectionName
        )

        print("----------------------------- Test Failure --------------------------------")
        if result_exception.__len__() != 0:
            for x in result_exception[0]['record']:
                if x['isPass'] == False:
                    print(x['runnerID'], 'recordID', x['recordID'], x['testcaseID'], 'test failure')
                    error_result.append(x)
                else:
                    print(x['runnerID'], 'recordID', x['recordID'], x['testcaseID'], 'test empty')
                    empty_result.append(x)

        print("----------------------------- Test Success --------------------------------")
        if self.quote_detail == False:
            result_group = self.mongo_reader.get_results(
                runnerID1=id1,
                runnerID2=id2,
                dbName=self.runner_conf.storeConfig.dbName,
                collectionName=self.runner_conf.storeConfig.collectionName
            )
            if result_group.__len__() != 0:
                for res in result_group:
                    if res['record'].__len__() == 1:
                        mismatch_result.append(res['record'][0])
                        continue
                    # TODO: 如果加上竞品，就得Cn2了
                    x = res['record'][0]
                    y = res['record'][1]

                    # prepare for res_item
                    res_item = dict()
                    res_item['recordID1'] = x['recordID']
                    res_item['recordID2'] = y['recordID']
                    res_item['testcaseID1'] = x['testcaseID']
                    res_item['testcaseID2'] = y['testcaseID']
                    res_item['paramData1'] = x['paramData']
                    res_item['paramData2'] = y['paramData']
                    res_item['endtime1'] = x['endTime']
                    res_item['endtime2'] = y['endTime']

                    r1 = x['resultData']
                    r2 = y['resultData']
                    res = record_compare(r1, r2)

                    if res['result'] == True:
                        cmp_result['true'].append(res_item)
                    else:
                        res_item['result1'] = r1
                        res_item['result2'] = r2
                        res_item['details'] = res['details']
                        cmp_result['false'].append(res_item)
        else:
            group_resharp = mongo_reader.get_quote_results(
                runnerID1=id1,
                runnerID2=id2,
                dbName=dbName,
                collectionName=collectionName
            )
            if group_resharp.__len__() != 0:
                for res in group_resharp:
                    param = res['param']
                    results = res['results']
                    keys = list(results.keys())  # runnerID
                    # TODO: 如果加上竞品，就得Cn2了
                    list1 = results[keys[0]]
                    list2 = results[keys[1]]
                    x = list(list1.keys())
                    y = list(list2.keys())
                    times = list(set(x + y))
                    times.sort()

                    # prepare for res_item
                    res_item = dict()
                    miss_time = set()
                    dismatch = list()
                    res_item['testcaseID'] = param['testcaseID']
                    res_item['paramData'] = param['paramStr']
                    res_item['result'] = dismatch
                    print("In runnerIDs in {}".format(keys))
                    print("Compared for {} in {}".format(param['testcaseID'], param['paramStr']))

                    for time in times:
                        r1 = list1.get(time)
                        r2 = list2.get(time)
                        if r1 is None:
                            # print("r1 at time {} is None".format(time))
                            miss_time.add(time)
                            continue
                        if r2 is None:
                            # print("r2 at time {} is None".format(time))
                            miss_time.add(time)
                            continue

                        res = record_compare(r1, r2)
                        flag = res['result']
                        # print("At time {}".format(time,))
                        # print("r1 is {}".format(r1))
                        # print("r2 is {}".format(r2))
                        if res['result'] == True:
                            print("--------------------------------")
                        if res['result'] == False:
                            dismatch.append(res)
                            # print("result is {}".format(res['result']))
                            # print("detial is {}".format(res))

                    miss_rate = miss_time.__len__() / times.__len__()
                    error_rate = dismatch.__len__() / times.__len__()
                    res_item['miss_time'] = list(miss_time)
                    res_item['numbers'] = times.__len__()
                    res_item['miss_rate'] = format(miss_rate, '.0%')
                    res_item['error_rate'] = format(error_rate, '.0%')

                    if dismatch.__len__() == 0:
                        cmp_result['true'].append(res_item)
                    else:
                        cmp_result['false'].append(res_item)

        print("------------------The Size(sys) of result is {}".format(sys.getsizeof(result)))
        print("------------------The Size(val) of result is {}".format(result.__sizeof__()))


        col_res = self.mongo_hk.client[self.runner_conf.storeConfig.dbName][
            self.runner_conf.storeConfig.collectionName + '_test_result']
        try:
            col_res.insert_one(result)
        except TypeError as e:
            print(e)
        except DocumentTooLarge as e:
            print("DocumentTooLarge Error")
            for item in result['compared']['false']:
                item.pop('result1')
                item.pop('result2')
            col_res.insert_one(result)


if __name__ == '__main__':
    mongo_hk = MongoHook(conn_id='stocksdktest_mongo')
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
    res = a.execute("")
    # print(res)
    # mongo_reader.synchronizer(runnerID1=id1,runnerID2=id2,dbName=dbName,collectionName=collectionName,expectation=602)
    # # mongo_reader.prepare_param(runnerID1=id1, runnerID2=id2, dbName=dbName, collectionName=collectionName)
    # exception = mongo_reader.get_exception(runnerID1=id1, runnerID2=id2, dbName=dbName, collectionName=collectionName)
    # group = mongo_reader.get_results(runnerID1=id1, runnerID2=id2, dbName=dbName, collectionName=collectionName)
    # group_resharp = mongo_reader.get_quote_results(runnerID1=id1, runnerID2=id2, dbName=dbName, collectionName=collectionName)






