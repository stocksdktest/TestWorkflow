from collections import defaultdict

from operators.data_sorting_operator import is_list_sort


def test_main():
    import pymongo

    myclient = pymongo.MongoClient("mongodb://221.228.66.83:30617")  # 远程MongoDB服务器
    mydb = myclient["stockSdkTest"]
    col = mydb["sort"]
    id = 'RUN--dc0ddbe1-8a1d-45ec-ae14-8ba250afbbb8'
    print('xcom_pull', id)
    print("-----------------------------Now Get Data From Mongo Directly--------------------------------")
    result = dict()
    sort_result = defaultdict(list)
    exception_result = list()
    result['sort_result'] = sort_result
    result['exception_result'] = exception_result
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
    # from protos_gen.config_pb2 import RunnerConfig
    #
    # runner_conf = RunnerConfig()
    # runner_conf.jobID = 'TJ-1'
    # runner_conf.runnerID = generate_id('RUN-A')
    # runner_conf.storeConfig.mongoUri = "mongodb://221.228.66.83:30617"
    # runner_conf.storeConfig.dbName = "stockSdkTest"
    # runner_conf.storeConfig.collectionName = "sort"
    # runner_conf.storeConfig.restEndpoint = 'http://mongo-python-eve.sdk-test.svc.cluster.local:80'
    #
    # data_sorter = DataSortingOperator(
    #     runner_conf=runner_conf,
    #     task_id="sorting",
    #     from_task="android_before"
    # )
    #
    # data_sorter.execute(" ")
    import pymongo

    myclient = pymongo.MongoClient("mongodb://221.228.66.83:30617")  # 远程MongoDB服务器
    mydb = myclient["stockSdkTest"]
    col = mydb["sort"]
    id = 'RUN--dc0ddbe1-8a1d-45ec-ae14-8ba250afbbb8'
    print('xcom_pull', id)
    print("-----------------------------Now Get Data From Mongo Directly--------------------------------")
    result = dict()
    sort_result = defaultdict(list)
    exception_result = list()
    result['sort_result'] = sort_result
    result['exception_result'] = exception_result
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
        print("record:", record)
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

        # result_list = list(record['resultData'].values())  # 待验证排序的list
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
        sort_result[testcaseID].append({
            # 'origin_result': result_list,
            'recordID': recordID,
            'check_result': check_res,
            'param': param
        })

    # col = mydb['sort_result']
    # col.insert(result)

    myclient.close()