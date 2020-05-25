import datetime
import os
import sys
import csv
import pymongo
import json
from airflow.exceptions import AirflowException
from airflow.utils.decorators import apply_defaults

from operators.comparator.base import RecordComparator
from operators.stock_operator import StockOperator
from protos_gen import RunnerConfig

from utils.mongo_hook import MongoHookWithDB
from utils import *
from collections import defaultdict

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
    '权证1':'buyPrices',
    '发卖盘数':'sellPrices',
}


def get_csv_data(csvname):
    lines = list()
    with open(csvname, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        print(type(reader))
        for row in reader:
            lines.append(row)
    labels = lines[0]
    target_labels = csv_to_sdk.keys()
    records = list()
    cols = labels.__len__()
    rows = lines.__len__()

    for i in range(1, rows):
        record = dict()
        line = lines[i]
        for j in range(0, cols):
            label = labels[j]
            if label in target_labels:
                value = line[j]
                if value == '0':
                    value = '-'
                record[csv_to_sdk[label]] = value
        if 'datetime' in record.keys():
            record['datetime'] = record['datetime'].split('.')[0].replace('-', '').replace(':', '')
        records.append(record)

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

        # Get the datas from mongodb to compare
        cursor = self.mongo_hk.get_collection('test_result').distinct('runnerID', {'jobID': self.jobID})
        runnerIDs = list(cursor)
        runnerID = runnerIDs[0]
        sdk_records = self.get_mongo_data(runnerID)
        # prefix = '/media/young/学习/My Programs/Python Programs/Dev Testworkflow/TestWorkflow/testcases/'
        # sdk_records = load_records(prefix + 'records1.json')

        # preprocess data and distinguish by datetime Todo: can use mongodb's aggregate?
        results = [item['resultData'] for item in sdk_records]
        results = unique_datetime(results)
        results_csv = unique_datetime(csv_records)

        # Data Compare
        compare_record = CompareResultRecord(
            jobID=self.runner_conf.jobID,
            dagID=self.dag_id,
            id1=self.jobID,
            id2=self.file_name
        )
        self.compare_csv_sdk(results, results_csv, compare_record)
        result = compare_record.get_result()

        self.mongo_hk.get_collection('excel_result').insert_one(result)

        return result
