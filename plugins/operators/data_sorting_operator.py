import datetime
from airflow.exceptions import AirflowException
from airflow.utils.decorators import apply_defaults
from operators.stock_operator import StockOperator

from airflow.contrib.hooks.mongo_hook import MongoHook
from utils import *
from collections import defaultdict

def sort_type_key_mapper(testcaseID, sort_type):
    try:
        key = sort_map.get(testcaseID).get(sort_type)
        if key is not None:
            return key
        else:
            # raise AirflowException("Invalid sort type {} for {}".format(sort_type, testcaseID))
            print("-----------------------Invalid sort type {} for {}".format(sort_type, testcaseID))
    except AttributeError as e:
        # raise AirflowException("Invalid testcaseID {}".format(testcaseID))
        print("-----------------------Invalid testcaseID {}".format(testcaseID))
        print(e)


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


def is_list_sort(sort_list: list, testcaseID, sort_type, ascending=True):
    # TODO: 传入了错误的key的异常处理
    key = sort_type_key_mapper(testcaseID=testcaseID, sort_type=sort_type)  # 把"hsl"这样的拼音转化为待排序项的key
    print("-----Info Checking %s, sort_type is %s, key is %s" % (testcaseID, sort_type, key))
    print("Is it Ascending?") if ascending else print("Is it Descending?")

    # TODO: safe eval from str to numbers
    try:
        key_list = [eval(item[key]) for item in sort_list]  # extract key from list
    except SyntaxError as e:
        try:
            key_list = [int(item[key]) for item in sort_list]  # extract key from list
        except Exception as e:
            key_list = [item[key] for item in sort_list]  # extract key from list

    print("Key list is ", key_list)
    check_result = check_list(sort_list=key_list, key=key, ascending=ascending)
    print("Checking Sort Result is ", check_result)

    return check_result

class DataSortingOperator(StockOperator):
    @apply_defaults
    def __init__(self, runner_conf, from_task,sdk_type='android', *args, **kwargs):
        super(DataSortingOperator, self).__init__(queue='worker', runner_conf=runner_conf, *args, **kwargs)
        self.from_task = from_task
        self.sdk_type = sdk_type
        self.mongo_hk = MongoHook(conn_id='stocksdktest_mongo')
        self.conn = self.mongo_hk.get_conn()

    def close_connection(self):
        self.mongo_hk.close_conn()

    def execute(self, context):
        myclient = self.mongo_hk.client
        mydb = myclient[self.runner_conf.storeConfig.dbName]
        col = mydb[self.runner_conf.storeConfig.collectionName]

        # TODO: FOR TEST AD HOC
        id = self.xcom_pull(context, key=self.from_task)
        # id = 'RUN-A-11921697-65a6-4c3e-ac78-20d15212e305'
        print('xcom_pull', id)
        print("-----------------------------Now Get Data From Mongo Directly--------------------------------")
        result = dict()
        sort_result = defaultdict(list)
        exception_result = list()
        result['sort_result'] = sort_result
        result['exception'] = exception_result
        # TODO: 对异常的处理
        # 筛选规则
        rule = {
            'runnerID': id,
            # TODO: 加上对于排序 testcaseID的限制
            '$or': [{'resultData': {'$ne': None}}, {'exceptionData': {'$ne': None}}]
        }
        records = list()  # 存储待排序的记录
        for record in col.find(rule):
            # 异常处理
            if record['exceptionData'] is not None:
                exception_result.append(record)
                continue

            # 得到正常的数据
            testcaseID = record['testcaseID']
            param = record['paramData']['param']
            recordID = record['recordID']
            sort_asc = True  # 默认升序
            if testcaseID == 'BANKUAISORTING_1':  # 先处理 BANKUAISORTING_1相关的
                records.append(record)
                sort_type = param.split(',')[2]
                sort_asc = int(param.split(',')[3])
            elif testcaseID == 'CATESORTING_2':
                # TODO:
                records.append(record)
                sort_type = param.split(',')[2]
                sort_asc = int(param.split(',')[3]) ^ 1
            else:
                continue

            result_list = list(record['resultData'].values())  # 待验证排序的list
            check_res = is_list_sort(
                sort_list=result_list.copy(),
                testcaseID=testcaseID,
                sort_type=sort_type,
                ascending=bool(sort_asc)
            )
            sort_result[testcaseID].append({
                # 'origin_result': result_list,
                'recordID': recordID,
                'check_result': check_res,
                'param': param
            })

        col = mydb[self.runner_conf.storeConfig.collectionName+"_result"]
        col.insert(result)

def test_main():
    import pymongo

    myclient = pymongo.MongoClient("mongodb://221.228.66.83:30617")  # 远程MongoDB服务器
    mydb = myclient["stockSdkTest"]
    col = mydb["sort"]
    id = 'RUN-A-11921697-65a6-4c3e-ac78-20d15212e305'
    print('xcom_pull', id)
    print("-----------------------------Now Get Data From Mongo Directly--------------------------------")
    result = dict()
    sort_result = defaultdict(list)
    exception_result = list()
    result['sort_result'] = sort_result
    # TODO: 对异常的处理
    # 筛选规则
    rule = {
        'runnerID': id,
        # TODO: 加上对于排序 testcaseID的限制
        '$or': [{'resultData': {'$ne': None}}, {'exceptionData': {'$ne': None}}]
    }
    records = list()  # 存储待排序的记录
    for record in col.find(rule):
        # 异常处理
        if record['exceptionData'] is not None:
            exception_result.append(record)
            continue

        # 得到正常的数据
        testcaseID = record['testcaseID']
        param = record['paramData']['param']
        recordID = record['recordID']
        sort_asc = True  # 默认升序
        if testcaseID == 'BANKUAISORTING_1':  # 先处理 BANKUAISORTING_1相关的
            records.append(record)
            sort_type = param.split(',')[2]
            sort_asc = int(param.split(',')[3])
        elif testcaseID == 'CATESORTING_2':
            # TODO:
            records.append(record)
            sort_type = param.split(',')[2]
            sort_asc = int(param.split(',')[3])^1
        else:
            continue

        result_list = list(record['resultData'].values())  # 待验证排序的list
        check_res = is_list_sort(
            sort_list=result_list.copy(),
            testcaseID=testcaseID,
            sort_type=sort_type,
            ascending=bool(sort_asc)
        )
        sort_result[testcaseID].append({
            # 'origin_result': result_list,
            'recordID': recordID,
            'check_result': check_res,
            'param': param
        })

    col = mydb['sort_result']
    col.insert(result)

    myclient.close()


if __name__ == '__main__':
    from protos_gen.config_pb2 import RunnerConfig

    runner_conf = RunnerConfig()
    runner_conf.jobID = 'TJ-1'
    runner_conf.runnerID = generate_id('RUN-A')
    runner_conf.storeConfig.mongoUri = "mongodb://221.228.66.83:30617"
    runner_conf.storeConfig.dbName = "stockSdkTest"
    runner_conf.storeConfig.collectionName = "sort"
    runner_conf.storeConfig.restEndpoint = 'http://mongo-python-eve.sdk-test.svc.cluster.local:80'

    data_sorter = DataSortingOperator(
        runner_conf=runner_conf,
        task_id="sorting",
        from_task="android_before"
    )

    data_sorter.execute(" ")