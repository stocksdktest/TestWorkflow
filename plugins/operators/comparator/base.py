from enum import Enum
from utils import *
from json_diff import Comparator

CompareResult = Enum('CompareResult', ('Pass', 'Data Inconsistency', 'Data Amount Inconsistency'))


class RecordComparator(object):

    def save_same_key(self, record_a: dict, record_b: dict):
        keys_a = set(record_a.keys())
        keys_b = set(record_b.keys())
        keys = keys_a.intersection(keys_b)

        for key in keys_a:
            if key not in keys:
                print("record_a pop {}".format(key))
                record_a.pop(key)

        for key in keys_b:
            if key not in keys:
                print("record_b pop {}".format(key))
                record_b.pop(key)

    def compare(self, record_a, record_b):
        """
        :param record_a:
        :param record_b:
        :return: CompareResult
        """
        if record_a == record_b:
            return CompareResult['Pass']
        else:
            return CompareResult['Data Inconsistency']

    def compare_general(self, record_a: dict, record_b: dict):
        return record_compare(record_a, record_b)

    def compare_json_diff(self, record_a: dict, record_b: dict):
        comparator = Comparator()
        self.save_same_key(record_a, record_b)
        return comparator.compare_dicts(record_a, record_b)

    def compare_same_key(self, record_a: dict, record_b: dict):

        self.save_same_key(record_a, record_b)
        return record_compare(record_a, record_b)


if __name__ == '__main__':
    import pymongo

    myclient = pymongo.MongoClient("mongodb://221.228.66.83:30617")  # 远程MongoDB服务器
    mydb = myclient["stockSdkTest"]
    col = mydb["test_result"]
    results = list()
    rule = {'jobID': 'manual__2020-04-17T08:56:51.337611 00:00'}
    for x in col.find(rule):
        if x['resultData'] is not None:
            results.append(x['resultData'])
    record1 = results[0]
    record2 = results[1]
    a1 = {
        'a':'a',
        'x':'c'
    }
    a2 = {
        'a':'a',
        'x':'y'
    }
    b = {
        'b':a1,
        'c':111
    }
    c = {
        'b':a2,
        'c':121
    }
    record1['x'] = b
    record2['x'] = c

    comparator = RecordComparator()
    res = comparator.compare_general(record1, record2)
    res_same_key = comparator.compare_same_key(record1, record2)
    res_diff = comparator.compare_json_diff(record1, record2)
    print(res)
