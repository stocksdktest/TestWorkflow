import pymongo
import pprint
from collections import defaultdict, Sequence
from enum import Enum

StockResultTypes = Enum('StockResultTypes', ('Default', 'Quote', 'Sort', 'File', 'DefaultSort', 'QuoteSort'))


class TestResultMongoRecord(object):

    def __init__(self, record) -> None:
        super().__init__()
        self.record = record
        self._id = record['_id']
        self.jobID = record['jobID']
        self.runnerID = record['runnerID']
        self.testcaseID = record['testcaseID']
        self.recordID = record['recordID']
        self.isPass = record['isPass']
        self.startTime = record['startTime']
        self.endTime = record['endTime']
        self.paramData = record['paramData']
        self.resultData = record['resultData']
        self.exceptionData = record['exceptionData']


class StockResultRecord(object):

    def __init__(self, jobID, dagID, rtype:StockResultTypes) -> None:
        super().__init__()

        self.result = dict()  # 存储所有返回的结果
        self.error = list()  # 异常的结果
        self.empty = list()  # 返回为空的结果
        self.mismatch = list()  # 无法比较的结果

        self.result['jobID'] = jobID
        self.result['dagID'] = dagID
        self.result['type'] = rtype

    def __str__(self) -> str:
        return self.result.__str__()

    def __repr__(self) -> str:
        return self.result.__repr__()

    def pop(self, record: dict):
        keys = ['resultData']
        for key in keys:
            if key in record.keys():
                record.pop(key)

    def add_status(self, item: dict):
        item['status'] = 0
        item['bugDescribe'] = None

    def append_empty(self, record):
        self.pop(record)
        self.add_status(record)
        self.empty.append(record)
        print("{} {} recordID {} test empty".format(record['runnerID'], record['testcaseID'], record['recordID']))

    def append_error(self, record):
        self.pop(record)
        self.add_status(record)
        self.error.append(record)
        print("{} {} recordID {} test failure".format(record['runnerID'], record['testcaseID'], record['recordID']))

    def append_mismatch(self, record, is_quote=False):
        self.pop(record)
        self.add_status(record)
        self.mismatch.append(record)
        if not is_quote:
            print("{} {} recordID {} mismatch".format(record['runnerID'], record['testcaseID'], record['recordID']))


    def get_result(self):
        return self.result


class CompareResultRecord(StockResultRecord):

    def __init__(self, jobID, dagID, rtype, id1, id2) -> None:
        super().__init__(jobID, dagID, rtype)

        self.compare = dict()  # 比较的结果
        self.compare['true'] = list()
        self.compare['false'] = list()
        self.result['runnerID1'] = id1
        self.result['runnerID2'] = id2
        self.result['result'] = self.compare
        self.result['error'] = self.error
        self.result['mismatch'] = self.mismatch
        self.result['empty'] = self.empty
        self.result['error_msg'] = None

    def append_compare_true(self, item):
        self.compare['true'].append(item)

    def append_compare_false(self, item):
        self.add_status(item)
        self.compare['false'].append(item)


class SortResultRecord(StockResultRecord):

    def __init__(self, jobID, dagID, rtype, id) -> None:
        super().__init__(jobID, dagID, rtype)
        self.sort_result = dict()
        self.sort_result['true'] = list()
        self.sort_result['false'] = list()
        self.sort_result['unknown'] = list()
        self.result['runnerID1'] = id
        self.result['runnerID2'] = id
        self.result['result'] = self.sort_result
        self.result['error'] = self.error
        self.result['mismatch'] = self.mismatch
        self.result['empty'] = self.empty

    def append_sort_result(self, testcaseID, item, sort_ok):
        item['testcaseID'] = testcaseID
        if not sort_ok:
            self.add_status(item)

        if sort_ok == True:
            self.sort_result['true'].append(item)
        elif sort_ok == False:
            self.sort_result['false'].append(item)
        else:
            self.sort_result["unknown"].append(item)

class CompareItemRecord(object):

    def __init__(self, records: list) -> None:
        super().__init__()
        self.item = dict()
        self.append_base_info(records)

    def add_sort_code_list(self, codelists: list):
        self.item['codelist1'] = codelists[0]
        self.item['codelist2'] = codelists[1]

    def append_base_info(self, records: list):
        for i in range(records.__len__()):
            self.item['runnerID{}'.format(i + 1)] = records[i]['runnerID']
        for i in range(records.__len__()):
            self.item['recordID{}'.format(i + 1)] = records[i]['recordID']
        for i in range(records.__len__()):
            self.item['testcaseID{}'.format(i + 1)] = records[i]['testcaseID']
        for i in range(records.__len__()):
            self.item['paramData{}'.format(i + 1)] = records[i]['paramData']
        for i in range(records.__len__()):
            self.item['startTime{}'.format(i + 1)] = records[i]['startTime']
        for i in range(records.__len__()):
            self.item['endTime{}'.format(i + 1)] = records[i]['endTime']

    def append_results(self, results, details):
        # for i in range(results.__len__()):
        #     self.item['result{}'.format(i+1)] = results[i]
        self.item['details'] = details

    def get_item(self):
        return self.item


class QuoteDetaiItemRecord(object):

    def __init__(self, testcaseID, paramData, times_cnts, recordID) -> None:
        super().__init__()
        self.item = dict()
        self.miss = set()
        self.match = set()
        self.dismatch = list()

        # 一共多少的时间
        self.times_cnts = times_cnts

        self.item['testcaseID'] = testcaseID
        self.item['paramData'] = paramData
        self.item['result'] = self.dismatch
        self.item['recordID'] = recordID

        print("Compared for {} in {}".format(testcaseID, paramData))

    def missing(self, time):
        self.miss.add(time)

    def matching(self, time):
        self.match.add(time)

    def append_dismatch(self, res):
        self.dismatch.append(res)

    def caucalute(self, match_cnt):
        cnts = self.times_cnts
        miss_rate = self.miss.__len__() / cnts
        error_rate = self.dismatch.__len__() / cnts
        match_rate = match_cnt / cnts
        self.item['miss_time'] = list(self.miss)
        self.item['match_time'] = list(self.match)
        self.item['numbers'] = cnts
        self.item['miss_rate'] = format(miss_rate, '.0%')
        self.item['match_rate'] = format(match_rate, '.0%')
        self.item['error_rate'] = format(error_rate, '.0%')

    def is_mismatch(self):
        cnts = self.times_cnts
        miss_rate = self.miss.__len__() / cnts
        return (miss_rate == 1)

    def is_dismatch(self):
        return (self.dismatch.__len__() == 0)

    def get_item(self):
        return self.item


if __name__ == '__main__':
    jobID = 'TJ-1'
    dagID = 'dagID'
    id1 = 'RUN--7d7acfc9-b3f5-4aec-a3ff-cb98ad8ec197'
    id2 = 'RUN--05da2757-a085-4b89-aa53-8e33526d9967'

    compare = CompareResultRecord(jobID=jobID, dagID=dagID, id1=id1, id2=id2)
    sorting = SortResultRecord(jobID=jobID, dagID=dagID, id=id1)

    for i in range(10):
        compare.append_error("error_record{}".format(i))
        compare.append_empty("empty_record{}".format(i))
        compare.append_compare_true("true item{}".format(i))
        compare.append_compare_false("false item{}".format(i))

        sorting.append_empty("empty_record{}".format(i))
        sorting.append_error("error_record{}".format(i))
        sorting.append_sort_result("testcaseID{}".format(i), "sort result{}".format(i))

    pprint.pprint(compare.result)
    pprint.pprint(sorting.result)
