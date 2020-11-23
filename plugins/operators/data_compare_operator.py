from airflow.utils.decorators import apply_defaults

from operators.comparator.base import RecordComparator
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
        """
        @param runner_conf: 测试计划的运行参数
        @param task_id_list: 以哪些task的运行结果作为比较的输入
        @param run_times: 测试计划中单个用例执行的次数，默认值为1
        @param quote_detail: 是否是行情快照
        @param sort_id_list: 是否整合排序接口的结果，若非None，则获取排序任务的结果
        @param sort_and_comprae: 是否整合排序接口的结果
        @param args:
        @param kwargs:
        """
        super(DataCompareOperator, self).__init__(queue='worker', runner_conf=runner_conf, *args, **kwargs)
        self.task_id_list = task_id_list
        self.sort_id_list = sort_id_list
        self.sort_and_compare = sort_and_comprae
        self.mongo_hk = MongoHookWithDB(conn_id='stocksdktest_mongo')
        self.conn = self.mongo_hk.get_conn()
        self.run_times = run_times
        self.quote_detail = quote_detail
        self.mongo_reader = SdkMongoReader(client=self.mongo_hk.client)
        self.comparator = RecordComparator()
        self.TICK_LIST = ['CRAWLER_TICK_2']

        self.id1 = None
        self.id2 = None
        self.compare_record = None

    def data_synchronizer(self, context):
        print("-----------------------------Synchronize MongoDB--------------------------------")
        expectation = self.get_runner_conf_records()
        sleep_time = 30
        if context.get('expectation') is not None:  # For Debug
            expectation = context.get('expectation')
            sleep_time = 5
        timeout = expectation * 5  # 一个case最多给10s的时间
        if timeout < 300:
            timeout = 300
        print('Timeout(records to return) is {}'.format(timeout))
        self.mongo_reader.synchronizer(
            runnerID1=self.id1,
            runnerID2=self.id2,
            dbName=self.runner_conf.storeConfig.dbName,
            collectionName=self.runner_conf.storeConfig.collectionName,
            timeout=timeout,
            expectation=expectation,
            sleep_time=sleep_time
        )

    def data_prepare(self):
        print("-----------------------------Prepare for paramData to paramStr--------------------------------")
        self.mongo_reader.prepare_param(
            runnerID1=self.id1,
            runnerID2=self.id2,
            dbName=self.runner_conf.storeConfig.dbName,
            collectionName=self.runner_conf.storeConfig.collectionName
        )

    def pre_execute(self, context):
        super(DataCompareOperator, self).pre_execute(context)
        self.runner_conf = self.runner_conf_replicate(runner_conf=self.runner_conf,
                                                      replicate_numbers=self.run_times - 1)

        self.id1 = self.xcom_pull(context, key=self.task_id_list[0])
        self.id2 = self.xcom_pull(context, key=self.task_id_list[1])
        print('xcom_pull', self.id1)
        print('xcom_pull', self.id2)

        self.data_synchronizer(context=context)
        self.data_prepare()

        rtype = StockResultTypes.Default
        if self.quote_detail:
            if self.sort_and_compare:
                rtype = StockResultTypes.QuoteSort
            else:
                rtype = StockResultTypes.Quote
        else:
            if self.sort_and_compare:
                rtype = StockResultTypes.DefaultSort

        self.compare_record = CompareResultRecord(
            jobID=self.runner_conf.jobID,
            dagID=self.dag_id,
            id1=self.id1,
            id2=self.id2,
            rtype=rtype
        )

    def collect_exception(self):
        print("----------------------------- Test Failure --------------------------------")
        result_exception = self.mongo_reader.get_exception(
            runnerID1=self.id1,
            runnerID2=self.id2,
            dbName=self.runner_conf.storeConfig.dbName,
            collectionName=self.runner_conf.storeConfig.collectionName
        )
        if result_exception.__len__() != 0:
            for error_and_empty in result_exception:
                for x in error_and_empty['record']:
                    if not x['isPass']:
                        self.compare_record.append_error(x)
                    else:
                        self.compare_record.append_empty(x)


    def collect_success(self):
        print("----------------------------- Test Success --------------------------------")
        if not self.quote_detail:
            self.collect_normal_success()
        else:
            self.collect_quote_detail_success()


    def collect_quote_detail_success(self):
        print("----------------------------- Compare Quote --------------------------------")
        group_resharp = self.mongo_reader.get_quote_results(
            runnerID1=self.id1,
            runnerID2=self.id2,
            dbName=self.runner_conf.storeConfig.dbName,
            collectionName=self.runner_conf.storeConfig.collectionName
        )
        print("----------------------------- Get Group Resharp OK--------------------------------")
        if group_resharp.__len__() != 0:
            for res in group_resharp:
                param = res['param']
                results = res['records']
                keys = list(results.keys())  # runnerID
                print("keys is {}".format(keys))
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

                    res = self.comparator.compare_deep_diff(r1, r2)
                    res['datetime'] = time
                    res['recordID1'] = record1['recordID']
                    res['recordID2'] = record2['recordID']
                    # res['resultData1'] = r1
                    # res['resultData2'] = r2
                    # print("At time {}".format(time,))
                    # print("r1 is {}".format(r1))
                    # print("r2 is {}".format(r2))
                    if res['result'] == True:
                        # print("--------------------------------")
                        match_cnt = match_cnt + 1
                        quote_item.matching(time)
                    if res['result'] == False:
                        quote_item.append_dismatch(res)
                        # print("result is {}".format(res['result']))
                        # print("detial is {}".format(res))

                quote_item.caucalute(match_cnt=match_cnt)
                item = quote_item.get_item()
                if quote_item.is_mismatch():
                    self.compare_record.append_mismatch(item, is_quote=True)
                elif quote_item.is_dismatch():
                    self.compare_record.append_compare_true(item)
                else:
                    self.compare_record.append_compare_false(item)

    def collect_normal_success(self):
        print("----------------------------- Compare Normal --------------------------------")
        # TODO: 这里有数据量过大的隐患，可以通过先获取id再整理解决，不过暂时只在Quote出现
        result_group = self.mongo_reader.get_results(
            runnerID1=self.id1,
            runnerID2=self.id2,
            dbName=self.runner_conf.storeConfig.dbName,
            collectionName=self.runner_conf.storeConfig.collectionName
        )
        if result_group.__len__() != 0:
            for res in result_group:
                if res['record'].__len__() == 1:
                    self.compare_record.append_mismatch(res['record'][0])
                    continue
                # TODO: 如果加上竞品，就得Cn2了
                x = res['record'][0]
                y = res['record'][1]

                compare_item = CompareItemRecord(records=[x, y])

                r1 = x['resultData']
                r2 = y['resultData']
                rs = [r1, r2]

                # for sorting add ids
                if self.sort_and_compare:
                    # reformat r1 and r2:
                    try:
                        key_lists = [list(r1.keys()).copy(), list(r2.keys()).copy()]
                        for i in range(2):
                            key_list = key_lists[i]
                            r = rs[i]
                            for key in key_list:
                                item = r[key]
                                if 'id' in item.keys():
                                    id_key = 'id'
                                elif 'ID' in item.keys():
                                    id_key = 'ID'
                                else:
                                    continue
                                id = item[id_key].replace('.', "")
                                r[id] = r.pop(key)

                    except KeyError as e:
                        print("Error when reformat sort records", e)

                    # record code_list
                    code_list1 = list()
                    code_list2 = list()

                    try:
                        code_lists = [code_list1, code_list2]
                        for i in range(2):
                            code_list = code_lists[i]
                            for r in rs[i].values():
                                if isinstance(r, dict):
                                    if 'id' in r.keys():
                                        code_list.append(r['id'])
                                    elif 'ID' in r.keys():
                                        code_list.append(r['ID'])

                    except KeyError as e:
                        print("Error when id", e)
                    finally:
                        compare_item.add_sort_code_list([code_list1, code_list2])

                try:
                    testcaseID = x['testcaseID']
                except KeyError as e:
                    testcaseID = None

                if testcaseID in self.TICK_LIST:
                    res = self.comparator.compare_same_key(r1, r2)
                else:
                    res = self.comparator.compare_deep_diff(r1, r2)

                if res['result'] == True:
                    item = compare_item.get_item()
                    self.compare_record.append_compare_true(item)
                else:
                    compare_item.append_results(results=[r1, r2], details=res['details'])
                    item = compare_item.get_item()
                    self.compare_record.append_compare_false(item)


    def close_connection(self):
        self.mongo_hk.close_conn()

    def get_ios_data(self):
        return 0

    def get_android_data(self):
        return 0

    def execute(self, context):
        print("-----------------------------Now Get Data From Mongo Directly--------------------------------")
        self.collect_exception()
        self.collect_success()
        result = self.compare_record.get_result()

        result_size = get_obj_real_size(result)

        print("------------------The Size(sys) of result is {}".format(result_size))

        dbName = self.runner_conf.storeConfig.dbName
        collectionName = 'compare_result'
        print("dbName is {}".format(dbName))
        print("collectionName is {}".format(collectionName))

        if self.sort_and_compare:
            sort_result1 = self.xcom_pull(context, key=self.sort_id_list[0])
            sort_result2 = self.xcom_pull(context, key=self.sort_id_list[1])
            result['result']['sort1'] = sort_result1['result']
            result['result']['sort2'] = sort_result2['result']

        if context.get('unit_test') is not None:
            self.close_connection()
            return result

        try:
            db_writer = SdkMongoWriter(client=self.mongo_hk.client)
            db_writer.write_record(record=result, collection_name=collectionName)
        except Exception as e:
            print(e)
