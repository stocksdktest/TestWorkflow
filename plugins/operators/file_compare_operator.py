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

csv_to_sdk = {
    'VDE时间': 'datetime',
    # '代码':'id',
    '开盘': 'openPrice',
    '最高': 'highPrice',
    '最低': 'lowPrice',
    '最新': 'lastPrice',
    '金额': 'amount',
    '卖盘': 'sellVolume',
    '买股': 'buyVolume',
    '当前成交量': 'nowVolume',
    '振幅比率': 'amplitudeRate',
    '涨跌': 'change',
    '换手率': 'turnoverRate',
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
                    value = '一'
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

    def compare_csv_sdk(self, data_csv: dict, data_sdk: dict):
        time_csv = set(data_csv.keys())
        time_sdk = set(data_sdk.keys())
        same_time = time_csv.intersection(time_sdk)
        result = dict()
        result['true'] = list()
        result['false'] = list()
        comparator = RecordComparator()
        for time in same_time:
            item_csv = data_csv[time]
            item_sdk = data_sdk[time]
            comparator.save_same_key(item_csv, item_sdk)
            res = comparator.compare_deep_diff(item_csv, item_sdk)
            flag = res['result']
            if flag:
                result['true'].append(res)
            else:
                result['false'].append(res)
        return result

    def execute(self, context):
        # TODO: Download excel from ftp
        url = 'csv/{}'.format(self.file_name)
        path = '/tmp/csv/{}'.format(self.file_name)

        os.makedirs(os.path.dirname(path), exist_ok=True)
        downloader = FTP_Downloader()
        downloader.download(remote_path=url, local_path=path)

        # TODO: read data from csv
        csv_records = get_csv_data(path)

        # TODO: Get the datas from mongodb to compare
        cursor = self.mongo_hk.get_collection('test_result').distinct('runnerID', {'jobID': self.jobID})
        runnerIDs = list(cursor)
        runnerID1 = 'RUN--b29f0069-e9e8-4735-b56e-2b4f181e3f8b'
        runnerID2 = 'RUN--75e24ba8-86a4-463f-8163-e15dc0f4fe36'
        # sdk_records1 = self.get_mongo_data(runnerID1)
        # sdk_records2 = self.gget_mongo_data(runnerID2)
        prefix = '/media/young/学习/My Programs/Python Programs/Dev Testworkflow/TestWorkflow/testcases/'
        sdk_records1 = load_records(prefix + 'records1.json')
        sdk_records2 = load_records(prefix + 'records2.json')

        # TODO: pre process the data
        results1 = [item['resultData'] for item in sdk_records1]
        results2 = [item['resultData'] for item in sdk_records2]

        results1 = unique_datetime(results1)
        results2 = unique_datetime(results2)
        results_csv = unique_datetime(csv_records)

        # TODO: data compare
        comp1 = self.compare_csv_sdk(results1, results_csv)
        comp2 = self.compare_csv_sdk(results2, results_csv)

        res1 = dict()
        res2 = dict()
        res1['jobID'] = sdk_records1[0]['jobID']
        res2['jobID'] = sdk_records2[0]['jobID']
        res1['runnerID'] = sdk_records1[0]['runnerID']
        res2['runnerID'] = sdk_records2[0]['runnerID']
        res1['result'] = comp1
        res2['result'] = comp2

        # client = pymongo.MongoClient("mongodb://221.228.66.83:30617")
        # col = client.get_database("stockSdkTest").get_collection("excel_result")
        # col.insert_one(res1)
        # col.insert_one(res2)
        return [res1, res2]
