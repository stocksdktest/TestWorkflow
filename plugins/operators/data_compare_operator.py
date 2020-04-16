from airflow.utils.decorators import apply_defaults
from operators.stock_operator import StockOperator

from utils.mongo_hook import MongoHookWithDB
from utils import *
from pymongo.errors import DocumentTooLarge
from collections import defaultdict
import sys


class DataCompareOperator(StockOperator):
    @apply_defaults
    def __init__(self, runner_conf, task_id_list, run_times=1, quote_detail=False, sort_id_list=None,
                 sort_and_comprae=False, *args, **kwargs):
        super(DataCompareOperator, self).__init__(queue='worker', runner_conf=runner_conf, *args, **kwargs)
        self.task_id_list = task_id_list
        self.sort_id_list = sort_id_list
        self.sort_and_comprae = sort_and_comprae
        self.mongo_hk = MongoHookWithDB(conn_id='stocksdktest_mongo')
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
        print('xcom_pull', id1)
        print('xcom_pull', id2)
        print("-----------------------------Synchronize MongoDB--------------------------------")
        expectation = self.get_runner_conf_records()
        sleep_time = 30
        if context.get('expectation') is not None:
            expectation = context.get('expectation')
            sleep_time = 5
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
            expectation=expectation,
            sleep_time=sleep_time
        )
        print("-----------------------------Prepare for paramData to paramStr--------------------------------")
        self.mongo_reader.prepare_param(
            runnerID1=id1,
            runnerID2=id2,
            dbName=self.runner_conf.storeConfig.dbName,
            collectionName=self.runner_conf.storeConfig.collectionName
        )
        print("-----------------------------Now Get Data From Mongo Directly--------------------------------")
        compare_record = CompareResultRecord(
            jobID=self.runner_conf.jobID,
            dagID=self.dag_id,
            id1=id1,
            id2=id2
        )

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
                    compare_record.append_error(x)
                else:
                    compare_record.append_empty(x)

        print("----------------------------- Test Success --------------------------------")
        if not self.quote_detail:
            result_group = self.mongo_reader.get_results(
                runnerID1=id1,
                runnerID2=id2,
                dbName=self.runner_conf.storeConfig.dbName,
                collectionName=self.runner_conf.storeConfig.collectionName
            )
            if result_group.__len__() != 0:
                for res in result_group:
                    if res['record'].__len__() == 1:
                        compare_record.append_mismatch(res['record'][0])
                        continue
                    # TODO: 如果加上竞品，就得Cn2了
                    x = res['record'][0]
                    y = res['record'][1]

                    compare_item = CompareItemRecord(records=[x, y])

                    r1 = x['resultData']
                    r2 = y['resultData']

                    # for sorting add ids
                    if self.sort_and_comprae:
                        # reformat r1 and r2:
                        try:
                            key_list_1 = r1.keys()
                            key_list_2 = r2.keys()
                            for key in key_list_1:
                                item = r1[key]
                                id = item['id'].replace('.',"")
                                r1[id] = r1.pop(key)
                            for key in key_list_2:
                                item = r2[key]
                                id = item['id'].replace('.',"")
                                r2[id] = r2.pop(key)
                        except KeyError as e:
                            print("Error when reformat sort records", e)



                        # record code_list
                        code_list1 = list()
                        code_list2 = list()
                        try:
                            for r in r1.values():
                                if isinstance(x, dict):
                                    code_list1.append(r['id'])
                            for r in r2.values():
                                if isinstance(x, dict):
                                    code_list2.append(r['id'])

                        except KeyError as e:
                            print("Error when id", e)
                        finally:
                            compare_item.add_sort_code_list([code_list1, code_list2])

                    res = record_compare(r1, r2)

                    if res['result'] == True:
                        item = compare_item.get_item()
                        compare_record.append_compare_true(item)
                    else:
                        compare_item.append_results(results=[r1, r2], details=res['details'])
                        item = compare_item.get_item()
                        compare_record.append_compare_false(item)
        else:
            group_resharp = self.mongo_reader.get_quote_results(
                runnerID1=id1,
                runnerID2=id2,
                dbName=self.runner_conf.storeConfig.dbName,
                collectionName=self.runner_conf.storeConfig.collectionName
            )
            if group_resharp.__len__() != 0:
                for res in group_resharp:
                    param = res['param']
                    results = res['records']
                    keys = list(results.keys())  # runnerID
                    if keys.__len__() < 2:
                        print("for param {} , no enough data to compare".format(param))
                        continue
                    # TODO: 如果加上竞品，就得Cn2了
                    list1 = results[keys[0]]
                    list2 = results[keys[1]]
                    x = list(list1.keys())
                    y = list(list2.keys())
                    times = list(set(x + y))
                    times.sort()

                    if 'paramData' in res.keys():
                        paramData = res['paramData']
                    else:
                        paramData = param['paramStr']

                    # prepare for res_item
                    quote_item = QuoteDetaiItemRecord(
                        testcaseID=param['testcaseID'],
                        paramData=paramData,
                        times_cnts=times.__len__(),
                        recordID=param['paramStr']
                    )
                    match_cnt = 0
                    print("In runnerIDs in {}".format(keys))

                    # import pprint
                    # print("list1 is ")
                    # pprint.pprint(list1)

                    for time in times:
                        record1 = list1.get(time)
                        record2 = list2.get(time)
                        if record1 is None:
                            # print("r1 at time {} is None".format(time))
                            quote_item.missing(time)
                            continue
                        if record2 is None:
                            # print("r2 at time {} is None".format(time))
                            quote_item.missing(time)
                            continue

                        r1 = record1['resultData']
                        r2 = record2['resultData']

                        res = record_compare(r1, r2)
                        res['datetime'] = time
                        res['recordID1'] = record1['recordID']
                        res['recordID2'] = record2['recordID']
                        res['resultData1'] = r1
                        res['resultData2'] = r2
                        # print("At time {}".format(time,))
                        # print("r1 is {}".format(r1))
                        # print("r2 is {}".format(r2))
                        if res['result'] == True:
                            print("--------------------------------")
                            match_cnt = match_cnt + 1
                            quote_item.matching(time)
                        if res['result'] == False:
                            quote_item.append_dismatch(res)
                            # print("result is {}".format(res['result']))
                            # print("detial is {}".format(res))

                    quote_item.caucalute(match_cnt=match_cnt)
                    item = quote_item.get_item()
                    if quote_item.is_mismatch():
                        compare_record.append_mismatch(item, is_quote=True)
                    elif quote_item.is_dismatch():
                        compare_record.append_compare_true(item)
                    else:
                        compare_record.append_compare_false(item)

        result = compare_record.get_result()

        print("------------------The Size(sys) of result is {}".format(sys.getsizeof(result)))
        print("------------------The Size(val) of result is {}".format(result.__sizeof__()))

        dbName = self.runner_conf.storeConfig.dbName
        collectionName = 'compare_result'
        print("dbName is {}".format(dbName))
        print("collectionName is {}".format(collectionName))

        if self.sort_and_comprae:
            sort_result1 = self.xcom_pull(context, key=self.sort_id_list[0])
            sort_result2 = self.xcom_pull(context, key=self.sort_id_list[1])
            result['result']['sort1'] = sort_result1['result']
            result['result']['sort2'] = sort_result2['result']

        if context.get('unit_test') is not None:
            self.close_connection()
            return result

        col_res = self.mongo_hk.client[dbName][collectionName]
        try:
            col_res.insert_one(result)
        except TypeError as e:
            print(e)
        except DocumentTooLarge as e:
            print("DocumentTooLarge Error")
            # TODO: 如果Details也过大，应该怎么办
            if not self.quote_detail:
                for item in result['result']['false']:
                    item.pop('result1')
                    item.pop('result2')
            else:
                pass
            col_res.insert_one(result)
