import datetime
import os
import sys
import csv
import pymongo
import json
import re
from airflow.exceptions import AirflowException
from airflow.utils.decorators import apply_defaults

from operators.comparator.base import RecordComparator
from operators.stock_operator import StockOperator
from protos_gen import RunnerConfig

from utils.mongo_hook import MongoHookWithDB
from utils import *
from collections import defaultdict, Sequence

# TODO:
#  1. 代码.sh
#  2. 权证1 和 发卖盘数，字符串转列表的处理

csv_to_sdk = {
    'VDE时间': 'datetime',
    # '代码':'id',
    '开盘': 'openPrice',
    '最高': 'highPrice',
    '最低': 'lowPrice',
    '最新': 'lastPrice',
    '股数': 'volume',
    '金额': 'amount',
    '当前成交量': 'nowVolume',
    '振幅比率': 'amplitudeRate',
    '涨跌': 'change',
    '换手率': 'turnoverRate',
    '总买股数':'sumBuy',
    '总卖股数':'sumSell',
    '总买价':'averageBuy',
    '总卖价':'averageSell',
    '卖盘数据': 'sellVolume',
    '买盘数据': 'buyVolume',
    # '权证1':'buyPrices-buyVolumes',
    # '发卖盘数':'sellPrices-sellVolumes',
    '发卖盘数': 'buyPrices-buyVolumes',
    '权证1': 'sellPrices-sellVolumes',
    # '买价1':'buyPrice1',
    # '买价2':'buyPrice2',
    # '买价3':'buyPrice3',
    # '买价4':'buyPrice4',
    # '买价5':'buyPrice5',
    # '买量1':'buyVolume1',
    # '买量2':'buyVolume2',
    # '买量3':'buyVolume3',
    # '买量4':'buyVolume4',
    # '买量5':'buyVolume5',
    # '卖价1': 'sellPrice1',
    # '卖价2': 'sellPrice2',
    # '卖价3': 'sellPrice3',
    # '卖价4': 'sellPrice4',
    # '卖价5': 'sellPrice5',
    # '卖量1': 'sellVolume1',
    # '卖量2': 'sellVolume2',
    # '卖量3': 'sellVolume3',
    # '卖量4': 'sellVolume4',
    # '卖量5': 'sellVolume5',
}


def get_csv_data(csvname):
    lines = list()
    with open(csvname, 'r', encoding='UTF-8-sig') as f:
        reader = csv.reader(f)
        print(type(reader))
        for row in reader:
            lines.append(row)
    labels = lines[0]
    target_labels = csv_to_sdk.keys()
    records = list()
    cols = labels.__len__()
    rows = lines.__len__()

    number_set = dict()

    for i in range(1, rows):
        record = dict()
        line = lines[i]
        for j in range(0, cols):
            label = labels[j].replace(' ','') # remove space
            if label in target_labels:
                value = line[j]
                if value == '0':
                    value = '-'
                record[csv_to_sdk[label]] = value
        if 'datetime' in record.keys():
            record['datetime'] = record['datetime'].split('.')[0].replace('-', '').replace(':', '')

        base_lists = ['buyPrices', 'buyVolumes', 'sellPrices', 'sellVolumes']
        for key in base_lists:
            record[key] = list()

        # V2: 自己解析权证
        # '权证1': 'buyPrices-buyVolumes',
        # '发卖盘数': 'sellPrices-sellVolumes',
        # TODO: 自己解析权证1和发卖盘数
        # TODO: STEP1: 用 re 匹配连续空格并分割
        buyPrices_buyVolumes = re.split(pattern=" +", string=record['buyPrices-buyVolumes'])
        sellPrices_sellVolumes = re.split(pattern=" +", string=record['sellPrices-sellVolumes'])
        # print(buyPrices_buyVolumes)
        # print(sellPrices_sellVolumes)
        # TODO: STEP2: 分别解析权证1和发卖盘数
        base_number = 10 # 如果没有数据的记录
        n = buyPrices_buyVolumes.__len__()
        if n not in number_set.keys():
            number_set[n] = buyPrices_buyVolumes

        cnt = n - base_number
        base_x = 0
        base_y = 0
        for i in range(0, base_number//2):
            x = 2*i + base_x
            y = 2*i+1 + base_y
            record['buyPrices'].append(buyPrices_buyVolumes[x])
            record['buyVolumes'].append(buyPrices_buyVolumes[y])
            record['sellPrices'].append(sellPrices_sellVolumes[x])
            record['sellVolumes'].append(sellPrices_sellVolumes[y])
            if cnt > 0:
                cnt = cnt - 1
                base_x = base_x + 1
                base_y = base_y + 1

        record['buyPrices'].reverse()
        record['buyVolumes'].reverse()

        records.append(record)

    for n in number_set.keys():
        print("n is ", n, ":", number_set[n])

    return records


def load_records(file):
    with open(file, encoding='utf-8') as f:
        return json.loads(f.read())


def unique_datetime(results: list):
    times = set()
    res = dict()
    for result in results:
        if result is not None and isinstance(result, dict) and 'datetime' in result.keys():
            time = result['datetime']
            if time not in times:
                times.add(time)
                res[time] = result
    return res

def to_float(data, type=None):
    res = data
    try:
        res = float(data)
        if type is not None:
            if type == '/100':
                res = res/100
    except ValueError as e:
        pass
    except TypeError as e:
        pass
    finally:
        return res

def data_to_float(item:dict, key, is_sdk = True, type = None):
    if key in item.keys():
        if is_sdk:
            item[key] = to_float(item[key], type=type)
        else:
            item[key] = to_float(item[key])



def data_proprocess(item: dict, is_sdk = True):
    print("Process process, is_sdk is {}".format(is_sdk))
    print("item is {}".format(item))

    data_to_float(item, 'volume', is_sdk = is_sdk, type = '/100')
    data_to_float(item, 'nowVolume', is_sdk = is_sdk, type = '/100')
    data_to_float(item, 'sellVolume', is_sdk = is_sdk, type = '/100')
    data_to_float(item, 'buyVolume', is_sdk = is_sdk, type = '/100')
    data_to_float(item, 'turnoverRate')
    data_to_float(item, 'amplitudeRate')

    if item.get('sellVolumes') is not None and isinstance(item.get('sellVolumes'), list):
        sellVolumes = item.get('sellVolumes')
        n = sellVolumes.__len__()
        for i in range(n):
            if is_sdk:
                sellVolumes[i] = to_float(sellVolumes[i], type='/100')
            else:
                sellVolumes[i] = to_float(sellVolumes[i])

    if item.get('buyVolumes') is not None and isinstance(item.get('buyVolumes'), list):
        buyVolumes = item.get('buyVolumes')
        n = buyVolumes.__len__()
        for i in range(n):
            if is_sdk:
                buyVolumes[i] = to_float(buyVolumes[i], type='/100')
            else:
                buyVolumes[i] = to_float(buyVolumes[i])

class FileCompareOperator(StockOperator):
    @apply_defaults
    def __init__(self, runner_conf, jobID, file_name, *args, **kwargs):
        super(FileCompareOperator, self).__init__(queue='worker', runner_conf=runner_conf, *args, **kwargs)
        self.jobID = jobID
        self.file_name = file_name
        self.mongo_hk = MongoHookWithDB(conn_id='stocksdktest_mongo')
        self.conn = self.mongo_hk.get_conn()

    def get_mongo_data(self, runnerID):
        print("get data from mongodb with runnerID = {}".format(runnerID))
        col = self.mongo_hk.get_collection('test_result')
        records = list()
        cnts = 0
        all = col.find({'runnerID': runnerID}).count()
        print("There are {} records".format(all))
        cursor = col.find({'runnerID': runnerID})
        for record in cursor:
            cnts = cnts + 1
            print("get_mongo_data of runnerID {} is to {}%".format(runnerID, cnts / all))
            record['_id'] = record['_id'].__str__()
            records.append(record)
        return records

    def compare_csv_sdk(self, data_csv: dict, data_sdk: dict, compare_record: CompareResultRecord):
        time_csv = set(data_csv.keys())
        time_sdk = set(data_sdk.keys())
        same_time = time_csv.intersection(time_sdk)
        comparator = RecordComparator()
        for time in same_time:
            item_csv = data_csv[time]
            item_sdk = data_sdk[time]
            comparator.save_same_key(item_csv, item_sdk)
            data_proprocess(item_csv, is_sdk= False)
            data_proprocess(item_sdk, is_sdk= True)
            res = comparator.compare_deep_diff(item_csv, item_sdk)
            if res['result']:
                compare_record.append_compare_true(res)
            else:
                for i in range(res['details'].__len__()):
                    res['details'][i]['location'] = time + ":" + res['details'][i]['location']
                compare_record.append_compare_false(res)

    def execute(self, context):

        url = 'csv/{}'.format(self.file_name)
        path = '/tmp/csv/{}'.format(self.file_name)

        if not os.path.exists(path):
            # if not cache, download csv file from ftp
            os.makedirs(os.path.dirname(path), exist_ok=True)
            downloader = FTP_Downloader()
            downloader.download(remote_path=url, local_path=path)

        # read data from csv
        csv_records = get_csv_data(path)
        print("csv_records.length is {}".format(csv_records.__len__()))

        # Get the datas from mongodb to compare
        cursor = self.mongo_hk.get_collection('test_result').distinct('runnerID', {'jobID': self.jobID})
        runnerIDs = list(cursor)
        runnerID = runnerIDs[0]
        # sdk_records = self.get_mongo_data(runnerID)
        prefix = '/media/young/学习/My Programs/Python Programs/Dev Testworkflow/TestWorkflow/testcases/'
        sdk_records = load_records(prefix + 'records1.json')

        # preprocess data and distinguish by datetime Todo: can use mongodb's aggregate?
        results_sdk = [item['resultData'] for item in sdk_records]
        results_sdk = unique_datetime(results_sdk)
        results_csv = unique_datetime(csv_records)
        print("results_csv.length is {}".format(results_csv.__len__()))

        # Data Compare
        compare_record = CompareResultRecord(
            jobID=self.runner_conf.jobID,
            dagID=self.dag_id,
            id1=self.jobID,
            id2=self.file_name
        )
        self.compare_csv_sdk(results_sdk, results_csv, compare_record)
        result = compare_record.get_result()

        self.mongo_hk.get_collection('excel_result').insert_one(result)

        return {
            'result':result,
            'results_sdk':results_sdk,
            'results_csv':results_csv
        }