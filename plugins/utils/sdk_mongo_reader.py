import time
from collections import defaultdict

class SdkMongoReader(object):
    def __init__(self, client) -> None:
        """
        @param client: 传入一个Mongodb的client
        """
        super().__init__()
        self.client = client

    def get_exception(self, runnerID1, runnerID2, dbName='stockSdkTest', collectionName='test_result'):
        """
        @todo: 可能需要进行修改，因为异常也有返回param了，不过待确认
        得到某次测试的异常结果
        @return:
        """
        mydb = self.client[dbName]
        col = mydb[collectionName]

        match = dict()
        group = dict()
        empty_param = dict()  # paramData exists but resultData empty
        except_exist = dict()  # exceptionData exists or no resultData
        runnerID_exist = dict()  # from selected runnerID

        empty_param['$and'] = [
            {'resultData': {'$eq': {}}},
            {'paramData': {'$gt': {}}}
        ]

        except_exist['$or'] = [
            {'exceptionData': {'$gt': {}}},
            empty_param
        ]

        runnerID_exist['$or'] = [
            {'runnerID': {'$eq': runnerID1}},
            {'runnerID': {'$eq': runnerID2}}
        ]

        match['$and'] = [
            except_exist,
            runnerID_exist
        ]

        group['_id'] = {
            'testcaseID': '$testcaseID',
        }
        group['record'] = {
            '$push': '$$ROOT'
        }

        pipeline = [
            {'$match': match},
            {'$group': group},
        ]

        cursor = col.aggregate(pipeline)
        res = list()
        for document in cursor:
            res.append(document)
        return res

    def get_result(self, runnerID, dbName='stockSdkTest', collectionName='test_result'):
        """
        Group by testcaseID and paramDatas,得到某次测试的非空非异常结果
        """
        mydb = self.client[dbName]
        col = mydb[collectionName]

        match = dict()
        group = dict()
        result_exist = dict()

        result_exist['$and'] = [
            {'resultData': {'$gt': {}}},
            # {'resultData': {'$ne': None}},
        ]

        match['runnerID'] = {'$eq': runnerID}
        match['$or'] = [
            result_exist,
        ]

        group['_id'] = {
            'testcaseID': '$testcaseID',
            'paramStr': '$paramStr'
        }
        group['record'] = {
            '$push': '$$ROOT'
        }

        pipeline = [
            {'$match': match},
            {'$group': group},
        ]

        cursor = col.aggregate(pipeline)
        res = list()
        for document in cursor:
            res.append(document)
        return res

    def get_results(self, runnerID1, runnerID2, dbName='stockSdkTest', collectionName='test_result'):
        """
        Group by testcaseID and paramDatas,得到某次测试的非空非异常结果
        """
        mydb = self.client[dbName]
        col = mydb[collectionName]

        match = dict()
        group = dict()
        result_exist = dict()
        runnerID_exist = dict()

        result_exist['$and'] = [
            {'resultData': {'$gt': {}}},
        ]

        runnerID_exist['$or'] = [
            {'runnerID': {'$eq': runnerID1}},
            {'runnerID': {'$eq': runnerID2}}
        ]
        match['$and'] = [
            result_exist,
            runnerID_exist
        ]

        group['_id'] = {
            'testcaseID': '$testcaseID',
            'paramStr': '$paramStr'
        }
        group['record'] = {
            '$push': '$$ROOT'
        }

        pipeline = [
            {'$match': match},
            {'$group': group},
        ]

        cursor = col.aggregate(pipeline)
        res = list()
        for document in cursor:
            res.append(document)
        return res

    def get_quote_results(self, runnerID1, runnerID2, dbName='stockSdkTest', collectionName='test_result'):
        """
        Group by testcaseID and paramDatas,得到某次测试的非空非异常结果,专门整形为适合行情快照的结果
        """
        group = self.get_results(runnerID1,runnerID2,dbName,collectionName)
        group_resharp = list()
        for res in group:
            results = res['record']
            param = res['_id']
            id_result_time_dict = defaultdict(dict)  # 存储每个runnerID对应的记录(默认是的行情快照),以runnerID为key，对应一个dict，dict以datetime为key
            id_time_dict = defaultdict(set)
            item = dict()
            item['param'] = param
            item['results'] = id_result_time_dict

            for record in results:
                runnerID = record['runnerID']
                resultData = record['resultData']
                # if 'addValue' in resultData.keys():
                #     resultData.pop('addValue')
                try: 
                    datetime = resultData['datetime']
                except KeyError as e:
                    print("record has no field datetime {}".format(record))
                    continue
                if datetime not in id_time_dict[runnerID]:  # 对于同一个datetime，有一条记录就够了
                    id_time_dict[runnerID].add(datetime)
                    id_result_time_dict[runnerID][datetime] = resultData

            group_resharp.append(item)

        return group_resharp

    def prepare_param(self, runnerID1, runnerID2, dbName='stockSdkTest', collectionName='test_result'):
        """
        @todo 对于Android和iOS两多种情况端，对于空的情况，有null和-等多种情况，考虑在此处或者比较的时候进行预处理
        根据实际应用的需要，对于来自MongoDB的数据进行预处理
        目前主要是为了根据paramData对records进行group by操作(主要是对于Android和iOS)，
        将paramData的tuple排序然后转化成字符串为一个新字段
        @param runnerID1:
        @param runnerID2:
        @param dbName:
        @param collectionName:
        """
        mydb = self.client[dbName]
        col = mydb[collectionName]
        rule = dict()
        rule['$or'] = [
            {'runnerID': {'$eq': runnerID1}},
            {'runnerID': {'$eq': runnerID2}}
        ]
        rule['$and'] = [
            {'paramData': {'$gt': {}}}
        ]

        hash_list = list()
        for x in col.find(rule):
            hash_list.append({
                '_id': x['_id'],
                'paramData': x['paramData']
            })

        print(hash_list)

        for x in hash_list:
            dx = x['paramData']
            col.update(
                {'_id': x['_id']},
                {'$set': {'paramStr': sorted(dx.items()).__str__()}})

    def synchronizer(self, runnerID1, runnerID2, expectation, dbName='stockSdkTest', collectionName='test_result', timeout=10,
                     sleep_time=30):
        """
        同步数据库中两端的数据，等待到两端数据都与预计的参数相当，或者超时，或者连续3个sleep时间段里数据库的数据量不变
        @param runnerID1:
        @param runnerID2:
        @param expectation: 预计数据库中会有多少条记录
        @param dbName:
        @param collectionName:
        @param timeout:
        @param sleep_time: 每次等待的时间
        @return:
        """
        mydb = self.client[dbName]
        col = mydb[collectionName]
        cnt1 = 0
        cnt2 = 0
        cnt1_pre = 0
        cnt2_pre = 0
        counter = 0  # 数据库2端数据不变的次数
        timer = 0
        max = timeout

        print("Synchronizer : runnerID1 is {}".format(runnerID1))
        print("Synchronizer : runnerID2 is {}".format(runnerID2))
        print("Synchronizer : dbName is {}".format(dbName))
        print("Synchronizer : collectionName is {}".format(collectionName))
        print("Synchronizer : expectation is {}".format(expectation))
        print("Synchronizer : timeout is {}".format(timeout))

        while col.find({'runnerID': runnerID1}).count() != cnt1 or col.find(
                {'runnerID': runnerID2}).count() != cnt2 or cnt1 != cnt2:

            print('cnt1', cnt1, 'cnt2', cnt2)

            cnt1_pre = cnt1
            cnt2_pre = cnt2
            cnt1 = col.find({'runnerID': runnerID1}).count()
            cnt2 = col.find({'runnerID': runnerID2}).count()
            if cnt1 == expectation and cnt2 == expectation:
                print("cnt1 and cnt2 are both ", expectation)
                break

            if cnt1_pre == cnt1 and cnt2_pre == cnt2:
                counter = counter + 1
            else:
                counter = 0

            time.sleep(sleep_time)
            timer = timer + sleep_time
            if timer > max:
                print('---------------------Time out for %d Seconds---------------------' % max)
                break
            if counter > 5:
                print('---------------------Records numbers not change for 3 sleep period---------------------')
                break
            print('---------------------Synchronize MongoDB for %d Seconds---------------------' % timer)

        print("Synchronizer End, cnt1 is {}, cnt2 is {}".format(cnt1,cnt2))