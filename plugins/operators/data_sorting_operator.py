import datetime
import sys

from airflow.exceptions import AirflowException
from airflow.utils.decorators import apply_defaults
from operators.stock_operator import StockOperator

from utils.mongo_hook import MongoHookWithDB
from utils import *
from collections import defaultdict


def sort_type_key_mapper(testcaseID, sort_type):
    """
    把"hsl"这样的拼音转化为待排序项的key
    @param testcaseID:
    @param sort_type: 类似hsl这样的排序参数
    @return: 类似turnoverRate这样的key
    """
    try:
        key = sort_map.get(testcaseID).get(sort_type)
        if key is not None:
            return key
        else:
            raise KeyError("Invalid sort type {} for {}".format(sort_type, testcaseID))
    except AttributeError as e:
        raise KeyError("Invalid testcaseID {}".format(testcaseID))


def check_list(sort_list: list, key, ascending=True):
    flags = list()
    for i in range(sort_list.__len__() - 1):
        if ascending:
            flags.append(int(sort_list[i] <= sort_list[i + 1]))
        else:
            flags.append(int(sort_list[i] >= sort_list[i + 1]))

    print('key = %s, ascending = %s, flags = %s' % (key, ascending, flags))
    if flags.count(0) > 0:
        return False
    else:
        return True


def phrase_keylist(sort_list: list, key):
    items = list()  # 根据key从结果中取得待排序项
    for item in sort_list:
        if key in item.keys():
            items.append(item[key])
        else:
            raise KeyError("Key {} not exists in records {}".format(key, item.keys()))

    print("origin key list is {}".format(items))

    def invalid(item):
        if item == '' or item == '一':
            return False
        else:
            return True

    items = list(filter(invalid, items))
    try:
        key_list = [float(item) for item in items]
    except ValueError as e:
        key_list = items

    return key_list


def is_list_sort(sort_list: list, testcaseID, sort_type, ascending=True):
    """
    判断对于testcaseID的sort_list，是否根据sort_type按照升降序排列
    @param sort_list:
    @param testcaseID:
    @param sort_type:
    @param ascending:
    @return:
    """
    res = {
        'check_res': None,
        'error_msg': None
    }
    try:
        key = sort_type_key_mapper(testcaseID=testcaseID, sort_type=sort_type)  # 把"hsl"这样的拼音转化为待排序项的key
    except KeyError as e:
        print("Status Unknown", e)
        res['error_msg'] = repr(e)
        return res

    print("-------------------Info------------------\n"
          "Checking %s, sort_type is %s, key is %s" % (testcaseID, sort_type, key))
    print("Is it Ascending?") if ascending else print("Is it Descending?")

    try:
        key_list = phrase_keylist(sort_list=sort_list, key=key)
    except KeyError as e:
        print("Status Unknown", e)
        res['error_msg'] = repr(e)
        return res

    print("Key list is ", key_list)
    check_result = check_list(sort_list=key_list, key=key, ascending=ascending)
    res['check_res'] = check_result
    print("Checking Sort Result is {}".format(check_result))

    return res


class DataSortingOperator(StockOperator):
    @apply_defaults
    def __init__(self, runner_conf, from_task, sdk_type='android', sort_and_comprae=False, *args, **kwargs):
        super(DataSortingOperator, self).__init__(queue='worker', runner_conf=runner_conf, *args, **kwargs)
        self.from_task = from_task
        self.sdk_type = sdk_type
        self.sort_and_comprae = sort_and_comprae
        self.mongo_hk = MongoHookWithDB(conn_id='stocksdktest_mongo')
        self.conn = self.mongo_hk.get_conn()
        self.mongo_reader = SdkMongoReader(client=self.mongo_hk.client)

    def close_connection(self):
        self.mongo_hk.close_conn()

    def execute(self, context):
        myclient = self.mongo_hk.client
        mydb = myclient[self.runner_conf.storeConfig.dbName]
        col = mydb[self.runner_conf.storeConfig.collectionName]

        id = self.xcom_pull(context, key=self.from_task)
        print('xcom_pull', id)

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
        self.mongo_reader.synchronizer_single(
            runnerID=id,
            dbName=self.runner_conf.storeConfig.dbName,
            collectionName=self.runner_conf.storeConfig.collectionName,
            timeout=timeout,
            expectation=expectation,
            sleep_time=sleep_time
        )
        print("-----------------------------Now Get Data From Mongo Directly--------------------------------")
        sort_record = SortResultRecord(
            jobID=self.runner_conf.jobID,
            dagID=self.dag_id,
            id=id
        )

        result_exception = self.mongo_reader.get_exception(
            runnerID1=id,
            runnerID2=id,
            dbName=self.runner_conf.storeConfig.dbName,
            collectionName=self.runner_conf.storeConfig.collectionName
        )

        print("----------------------------- Test Failure --------------------------------")
        if result_exception.__len__() != 0:
            for x in result_exception[0]['record']:
                if x['isPass'] == False:
                    sort_record.append_error(x)
                else:
                    sort_record.append_empty(x)

        print("----------------------------- Test Success --------------------------------")

        rule = {
            'runnerID': id,
            'testcaseID': {'$in': sort_map['SORT_TESTCASEIDS']},
            'resultData': {'$gt': {}}
        }
        records = list()  # 存储待排序的记录
        for record in col.find(rule):

            testcaseID = record['testcaseID']
            param = record['paramData']['param']
            recordID = record['recordID']
            sort_asc = True  # 默认升序
            if testcaseID in sort_map['BANKUAI']:
                records.append(record)
                sort_type = param.split(',')[2]
                sort_asc = int(param.split(',')[3])
            elif testcaseID in sort_map['CATE']:
                records.append(record)
                sort_type = param.split(',')[2]
                sort_asc = int(param.split(',')[3]) ^ 1
            else:
                continue

            result_list = list()
            for x in record['resultData'].values():
                if isinstance(x, dict):
                    result_list.append(x)
            check_res = is_list_sort(
                sort_list=result_list.copy(),
                testcaseID=testcaseID,
                sort_type=sort_type,
                ascending=bool(sort_asc)
            )
            item = {
                # 'origin_result': result_list,
                'recordID': recordID,
                'paramData': record['paramData'],
                'check_result': check_res['check_res'],
                'error_msg': check_res['error_msg'],
                'param': param
            }
            sort_record.append_sort_result(
                testcaseID=testcaseID,
                item=item,
                sort_ok=check_res['check_res']
            )

        result = sort_record.get_result()

        print("------------------The Size(sys) of result is {}".format(sys.getsizeof(result)))
        print("------------------The Size(val) of result is {}".format(result.__sizeof__()))

        dbName = self.runner_conf.storeConfig.dbName
        # collectionName = self.runner_conf.storeConfig.collectionName + '_test_result'
        collectionName = 'compare_result'

        print("dbName is {}".format(dbName))
        print("collectionName is {}".format(collectionName))

        if self.sort_and_comprae:
            self.xcom_push(context, key=self.task_id, value=result)
        else:
            if context.get('unit_test') is not None:
                self.close_connection()
                return result, records

            col = mydb[collectionName]
            col.insert(result)
