from enum import Enum
from utils import *
from deepdiff import DeepDiff

CompareResult = Enum('CompareResult', ('Pass', 'Data Inconsistency', 'Data Amount Inconsistency'))


class CompareDetailItem(object):

    def __init__(self, type: CompareResult) -> None:
        super().__init__()
        self.type = type.name
        self.location = None
        self.src_a = 'not exist'
        self.src_b = 'not exist'

    def set_location(self, location):
        self.location = location

    def set_src_a(self, src_a):
        if isinstance(src_a, dict):
            src_a = 'exist'
        self.src_a = src_a

    def set_src_b(self, src_b):
        if isinstance(src_b, dict):
            src_b = 'exist'
        self.src_b = src_b

    def get_detail_item(self):
        return {
            'type': self.type,
            'location': self.location,
            'src_a': self.src_a,
            'src_b': self.src_b
        }


class CompareResultItem(object):

    def __init__(self) -> None:
        super().__init__()
        self.result = True
        self.false_count = 0
        self.details = list()
        self.compareDetail = {
            "result": self.result,
            "details": self.details
        }

    def parse_location(self, location):
        pass

    def insert_details(self, item: CompareDetailItem):
        self.details.append(item.get_detail_item())

    def insert_debug_info(self, info):
        self.details.append(info)

    def insert_dictionary_item_added(self, raw_datas):
        self.false_count = self.false_count + raw_datas.__len__()
        for data in raw_datas:
            item = CompareDetailItem(type=CompareResult['Data Amount Inconsistency'])
            location = data
            item.set_location(location)
            item.set_src_b(src_b=raw_datas[location])
            self.insert_details(item)

    def insert_values_changed(self, raw_datas):
        self.false_count = self.false_count + raw_datas.__len__()
        for data in raw_datas:
            item = CompareDetailItem(type=CompareResult['Data Inconsistency'])
            location = data
            item.set_location(location)
            item.set_src_a(src_a=raw_datas[location]['old_value'])
            item.set_src_b(src_b=raw_datas[location]['new_value'])
            self.insert_details(item)

    def insert_dictionary_item_removed(self, raw_datas):
        self.false_count = self.false_count + raw_datas.__len__()
        for data in raw_datas:
            item = CompareDetailItem(type=CompareResult['Data Amount Inconsistency'])
            location = data
            item.set_location(location)
            item.set_src_a(src_a=raw_datas[location])
            self.insert_details(item)

    def get_result_item(self):
        if self.false_count != 0:
            self.compareDetail['result'] = False
        return self.compareDetail


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

    def compare_deep_diff(self, record_a: dict, record_b: dict):
        raw_datas = DeepDiff(t1=record_a, t2=record_b, verbose_level=2)

        detailItem = CompareResultItem()
        for type in raw_datas.keys():
            if type == 'dictionary_item_added' or type == 'iterable_item_added':
                detailItem.insert_dictionary_item_added(raw_datas.get(type))
            elif type == 'dictionary_item_removed' or type == 'iterable_item_removed':
                detailItem.insert_dictionary_item_removed(raw_datas.get(type))
            elif type == 'values_changed' or 'type_changes':
                detailItem.insert_values_changed(raw_datas.get(type))
            else:
                print("Key {} Error in Deep Diff".format(type))
                detailItem.insert_debug_info(raw_datas.get(type))

        return detailItem.get_result_item()

    def compare_same_key(self, record_a: dict, record_b: dict):
        self.save_same_key(record_a, record_b)
        return self.compare_deep_diff(record_a, record_b)


if __name__ == '__main__':
    import pymongo

    myclient = pymongo.MongoClient("mongodb://221.228.66.83:30617")  # 远程MongoDB服务器
    mydb = myclient["stockSdkTest"]
    col = mydb["test_result"]
    results = list()
    # id1 = 'RUN--b8a445a0-2b89-4517-b559-d5706a5f3b4d'
    # id2 = 'RUN--e71868b6-cfed-4901-98f1-273095557ed8'
    id1 = 'RUN--52fb7f41-aa24-496c-9e19-faa49d2780f7'
    id2 = 'RUN--df2dbe1c-bcee-4724-a207-3def57f2fcb4'

    mongo_reader = SdkMongoReader(myclient)

    result_group = mongo_reader.get_results(
        runnerID1=id1,
        runnerID2=id2,
        dbName="stockSdkTest",
        collectionName="test_result"
    )

    result_gerneral = list()
    result_deep_diff = list()

    comparator = RecordComparator()

    if result_group.__len__() != 0:
        for res in result_group:
            if res['record'].__len__() == 1:
                continue
            # TODO: 如果加上竞品，就得Cn2了
            r1 = res['record'][0]['resultData']
            r2 = res['record'][1]['resultData']

            res = comparator.compare_general(r1, r2)
            # if res['details'].__len__() > 0:
            result_gerneral.append(res)

            res = comparator.compare_deep_diff(r1, r2)
            # if res['details'].__len__() > 0:
            result_deep_diff.append(res)
