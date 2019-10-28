import pymongo
import pickle
import sys
from protos_gen.record_pb2 import TestExecutionRecord

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# myclient = pymongo.MongoClient("mongodb://localhost:8082/")
# myclient = pymongo.MongoClient("mongodb://114.212.189.141:31498")  # 远程MongoDB服务器
mydb = myclient["stockSdkTest2"]
col1 = mydb["androidCase1"]
col2 = mydb["androidCase2"]
col3 = mydb["androidCase3"]
col4 = mydb["androidCase4"]
mycol = [col1, col2, col3, col4]


def load_testcase(save_path):
    # 使用load()将数据从文件中序列化读出
    fr = open(save_path, 'rb')
    data1 = pickle.load(fr)
    print(data1)
    fr.close()
    return data1


def decode_x(str):
    ss = str.encode('raw_unicode_escape')
    return ss.decode()


def bytesToDict(bytes):
    if bytes.__len__() == 0:
        return
    str1 = str(bytes, encoding="utf-8")
    data = eval(str1)
    return data


def TextExecutionRecordtoDict(record):
    if record == None:
        sys.stderr('TextExecutionRecordtoDict Type Error, param is NoneType')
        return
    if (type(record) != TestExecutionRecord):
        sys.stderr('TextExecutionRecordtoDict Type Error, param is not TestExecutionRecord')
        return
    res = {}
    res['jobID'] = record.jobID
    res['runnerID'] = record.runnerID
    res['testcaseID'] = record.testcaseID
    res['recordID'] = record.recordID
    res['isPass'] = record.isPass
    res['startTime'] = record.startTime
    res['paramData'] = bytesToDict(record.paramData)
    res['resultData'] = bytesToDict(record.resultData)
    res['exceptionData'] = bytesToDict(record.exceptionData)
    return res


if __name__ == '__main__':

    myclient
    # parse_list = []
    # dict_list = []
    # for i in range(4):
    #     load_data = load_testcase("../testcases/testout3/AndroidTestCase" + str(i))
    #     for case in load_data:
    #         rec = TestExecutionRecord()
    #         if case != None:
    #             rec.ParseFromString(case)
    #         parse_list.append(rec)
    #         dict_list.append(TextExecutionRecordtoDict(rec))
    #     mycol[i].insert_many(dict_list)
    #     parse_list.clear()
    #     dict_list.clear()
