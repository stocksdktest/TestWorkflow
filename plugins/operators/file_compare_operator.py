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


csv_to_sdk = {
    'VDE时间': 'datetime',
    'CE时间': 'CETime',
    # '代码':'id',
    '开盘': 'openPrice',
    '最高': 'highPrice',
    '最低': 'lowPrice',
    '最新': 'lastPrice',
    '股数': 'volume',
    '金额': 'amount',
    # '当前成交量': 'nowVolume', # 根据数据计算
    # '振幅比率': 'amplitudeRate', # 根据数据计算
    # '涨跌': 'change', # 根据数据计算
    # '换手率': 'turnoverRate', # 根据数据计算
    '总买股数': 'sumBuy',
    '总卖股数': 'sumSell',
    '总买价': 'averageBuy',
    '总卖价': 'averageSell',
    '卖盘数据': 'sellVolume',
    '买盘数据': 'buyVolume',
}

csv_to_sdk_type = {
    # 上海
    'sh': {
        '发卖盘数': 'buyPrices-buyVolumes',
        '权证1': 'sellPrices-sellVolumes',
    },
    # 深圳
    'sz': {
        '权证2': 'buyPrices-buyVolumes',
        '权证': 'sellPrices-sellVolumes',
    }
}


def get_csv_data(csvname, market_type, date_time, pre_close_price, circulating_share_capital):
    '''
    读入csv文件，转化为可以和sdk_record比较的格式
    @param csvname: csv文件名
    @param market_type: 市场类型，sh，sz等
    @param date_time: 待跟帐当天时间
    @param pre_close_price: 昨收价
    @param circulating_share_capital: 流通股本
    @return:
    '''
    lines = list()
    with open(csvname, 'r', encoding='UTF-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            lines.append(row)
    labels = lines[0]  # csv表的标签
    # 根据类型处理标签
    print('market_type is {}'.format(market_type))
    if market_type in csv_to_sdk_type.keys():
        csv_to_sdk.update(csv_to_sdk_type[market_type])
    else:
        raise AirflowException("Invalid Market Type")

    target_labels = list(csv_to_sdk.keys())  # 需要处理的标签
    records = list()  # 返回的数据
    cols = labels.__len__()  # 列数
    rows = lines.__len__()  # 行数

    number_set = dict()  # Debug用的

    for i in range(1, rows):
        record = dict()  # csv表的每一行
        line = lines[i]
        # 预处理空格和其他数据
        for j in range(0, cols):
            label = labels[j].replace(' ', '')
            if label in target_labels:
                value = line[j]
                # TODO: 没有的数据比不比？
                if value == '':
                    value = '-'
                record[csv_to_sdk[label]] = value.strip(' ')
        # 预处理时间
        if market_type == 'sh':
            if 'datetime' in record.keys():
                record['datetime'] = record['datetime'].split('.')[0].replace('-', '').replace(':', '')
        elif market_type == 'sz':
            CETime = record['CETime']
            if CETime.__len__() == 5:
                record['datetime'] = date_time + '0' + CETime
            elif CETime.__len__() == 6:
                record['datetime'] = date_time + CETime
            else:
                raise AirflowException("Invalid CE Time")
        else:
            raise AirflowException("Invalid Market Type")

        base_lists = ['buyPrices', 'buyVolumes', 'sellPrices', 'sellVolumes']
        for key in base_lists:
            record[key] = list()

        # TODO: 计算数据并自己解析
        # TODO: STEP0: 计算当前成交量(nowVolume)，振幅比率(amplitudeRate)，涨跌(change)，换手率(turnoverRate)
        try:
            if i != 1:
                record['nowVolume'] = record['volume'] - records[i-2]['volume']
        except TypeError as e:
            pass
        try:
            record['amplitudeRate'] = (to_float(record['highPrice']) - to_float(record['lowPrice'])) / pre_close_price
        except TypeError as e:
            pass
        try:
            record['change'] = to_float(record['lastPrice']) - pre_close_price
        except TypeError as e:
            pass
        try:
            record['turnoverRate'] = record['volume'] / circulating_share_capital
        except TypeError as e:
            pass
        # TODO: STEP1: 用 re 匹配连续空格并分割
        buyPrices_buyVolumes = re.split(pattern=" +", string=record['buyPrices-buyVolumes'])
        sellPrices_sellVolumes = re.split(pattern=" +", string=record['sellPrices-sellVolumes'])
        if market_type == 'sh':
            # TODO: STEP2: 分别解析权证1和发卖盘数（上海）
            base_number = 10  # 如果没有数据的记录, 上海的会默认补零
            n = buyPrices_buyVolumes.__len__()
            if n not in number_set.keys():
                number_set[n] = buyPrices_buyVolumes

            cnt = n - base_number
            base_x = 0
            base_y = 0
            for i in range(0, base_number // 2):
                x = 2 * i + base_x
                y = 2 * i + 1 + base_y
                if buyPrices_buyVolumes[x] != '0' and buyPrices_buyVolumes[y] != '0':
                    record['buyPrices'].append(buyPrices_buyVolumes[x])
                    record['buyVolumes'].append(buyPrices_buyVolumes[y])
                if sellPrices_sellVolumes[x] != '0' and sellPrices_sellVolumes[y] != '0':
                    record['sellPrices'].append(sellPrices_sellVolumes[x])
                    record['sellVolumes'].append(sellPrices_sellVolumes[y])
                if cnt > 0:
                    cnt = cnt - 1
                    base_x = base_x + 1
                    base_y = base_y + 1

            record['buyPrices'].reverse()
            record['buyVolumes'].reverse()
        elif market_type == 'sz':
            # TODO: STEP2: 分别解析权证和权证2（深圳）
            # 深圳的要分开处理，根据3的倍数
            # '权证2': 'buyPrices-buyVolumes',
            # '权证': 'sellPrices-sellVolumes',
            prices_volumes = [buyPrices_buyVolumes, sellPrices_sellVolumes]
            pv_keys = [{
                'price': 'buyPrices',
                'volume': 'buyVolumes'
            }, {
                'price': 'sellPrices',
                'volume': 'sellVolumes'
            }]
            for k in range(2):
                pv = prices_volumes[k]
                pv_key = pv_keys[k]
                n = pv.__len__()
                if n == 0 or n % 3 != 0:
                    break
                else:
                    valid_number = n / 3  # 有效位数
                    base_number = int(valid_number * 2)  # 如果没有数据的记录
                    cnt = n - base_number
                    base_x = 0
                    base_y = 0
                    for i in range(0, base_number // 2):
                        x = 2 * i + base_x
                        y = 2 * i + 1 + base_y
                        if pv[x] != '0' and pv[y] != '0':
                            record[pv_key['price']].append(pv[x])
                            record[pv_key['volume']].append(pv[y])
                        if cnt > 0:
                            cnt = cnt - 1
                            base_x = base_x + 1
                            base_y = base_y + 1
                if k == 0:
                    # sell 不用反转
                    record[pv_key['price']].reverse()
                    record[pv_key['volume']].reverse()
                print("--------------------")
                print("buyPrices.length = {}".format(record['buyPrices'].__len__()))
                print("buyVolumes.length = {}".format(record['buyVolumes'].__len__()))
                print("sellPrices.length = {}".format(record['sellPrices'].__len__()))
                print("sellVolumes.length = {}".format(record['sellVolumes'].__len__()))
        else:
            raise AirflowException("Invalid Market Type")

        # TODO: 整理异常数据
        abnormal_table = ['一', '-']
        refs = [record['buyPrices'], record['buyVolumes'], record['sellPrices'], record['sellVolumes']]
        for ref in refs:
            for i in range(ref.__len__()):
                if ref[i] in abnormal_table:
                    ref[i] = 0.0

        # if record['datetime'] == '20200624092429':
        #     print('record[buyPrices]', record['buyPrices'])
        #     print('record[buyVolumes]', record['buyVolumes'])
        #     print('record[sellPrices]', record['sellPrices'])
        #     print('record[sellVolumes]', record['sellVolumes'])

        records.append(record)

    for n in number_set.keys():
        print("n is ", n, ":", number_set[n])

    return records


def load_records(file):
    with open(file, encoding='utf-8') as f:
        return json.loads(f.read())


def unique_datetime(results: list):
    '''
    @param results: list of resultData in records
    @return: a dict, key is datetime, value is resultData
    To filter the redundant resultData by unique datetime.
    '''
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
                res = res / 100
            elif type == '/10000':
                res = res / 10000
            elif type == '*100':
                res = round(res * 100, 2)
    except ValueError as e:
        pass
    except TypeError as e:
        pass
    finally:
        return res


def data_to_float(item: dict, key, is_sdk=True, type=None):
    if key in item.keys():
        if is_sdk:
            item[key] = to_float(item[key], type=type)
        else:
            item[key] = to_float(item[key])


def data_proprocess(market_type, item: dict, is_sdk=True):
    data_to_float(item, 'nowVolume', is_sdk=is_sdk, type='/100')
    data_to_float(item, 'sellVolume', is_sdk=is_sdk, type='/100')
    data_to_float(item, 'buyVolume', is_sdk=is_sdk, type='/100')
    data_to_float(item, 'turnoverRate')
    data_to_float(item, 'amplitudeRate', is_sdk=is_sdk, type='*100')

    if item.get('sellVolumes') is not None and isinstance(item.get('sellVolumes'), list):
        sellVolumes = item.get('sellVolumes')
        n = sellVolumes.__len__()
        for i in range(n):
            if is_sdk:
                if market_type == 'sh':
                    sellVolumes[i] = to_float(sellVolumes[i], type='/100')
                elif market_type == 'sz':
                    sellVolumes[i] = to_float(sellVolumes[i], type='/10000')
            else:
                sellVolumes[i] = to_float(sellVolumes[i])

    if item.get('buyVolumes') is not None and isinstance(item.get('buyVolumes'), list):
        buyVolumes = item.get('buyVolumes')
        n = buyVolumes.__len__()
        for i in range(n):
            if is_sdk:
                if market_type == 'sh':
                    buyVolumes[i] = to_float(buyVolumes[i], type='/100')
                elif market_type == 'sz':
                    buyVolumes[i] = to_float(buyVolumes[i], type='/10000')
            else:
                buyVolumes[i] = to_float(buyVolumes[i])


class FileCompareOperator(StockOperator):
    @apply_defaults
    def __init__(self, runner_conf, jobID, file_name, market_type, pre_close_price, circulating_share_capital,
                 date_time, *args, **kwargs):
        '''
        @param jobID: 运行SDK测试收集数据的JobID
        @param file_name: 需要对比的文件名
        @param type: 'sh','sz', etc.
        @param pre_close_price: 昨收价
        @param circulating_share_capital: 流通股本
        @param date_time: 待跟账时间
        '''
        super(FileCompareOperator, self).__init__(queue='worker', runner_conf=runner_conf, *args, **kwargs)
        self.jobID = jobID
        self.file_name = file_name
        self.mongo_hk = MongoHookWithDB(conn_id='stocksdktest_mongo')
        self.conn = self.mongo_hk.get_conn()
        self.market_type = market_type
        self.pre_close_price = pre_close_price
        self.circulating_share_capital = circulating_share_capital
        self.date_time = date_time

    def parse_csv_result(self, csv_result):
        '''
        根据 market_type 对csv的结果进行预处理
        @param csv_result:
        @return:
        '''
        return csv_result

    def get_mongo_data(self, runnerID):
        '''
        @param runnerID: runnerID of sdk records
        @return: a list of resultData with runnerID
        use json.dump and load for cache
        '''
        print("get data from mongodb with runnerID = {}".format(runnerID))
        path = '/tmp/sdks/{}.json'.format(runnerID)
        if os.path.exists(path):
            print("Get from local cache")
            return load_records(path)
        else:
            print("Get from remote mongodb")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            col = self.mongo_hk.get_collection('test_result')
            records = list()
            cnts = 0
            all = col.find({'runnerID': runnerID}).count()
            print("There are {} records".format(all))
            cursor = col.find({'runnerID': runnerID})
            for record in cursor:
                cnts = cnts + 1
                if cnts % 100 == 0 or cnts == all:
                    print("get_mongo_data of runnerID {} is to {}%".format(runnerID, cnts / all))
                record['_id'] = record['_id'].__str__()
                # 预处理
                if 'resultData' in record.keys() and record['resultData'] is not None:
                    resultData = record['resultData']
                    resultKeys = list(resultData.keys())
                    for key in resultKeys:
                        if resultData[key] in ['-','一']:
                            resultData.pop(key)
                    records.append(record)
            with open(path, "w", encoding="UTF-8") as f:
                json.dump(records, f, ensure_ascii=False)
            # 预处理
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
            data_proprocess(item = item_csv, is_sdk=False, market_type=self.market_type)
            data_proprocess(item = item_sdk, is_sdk=True, market_type=self.market_type)
            res = comparator.compare_deep_diff(item_csv, item_sdk)
            if res['result']:
                compare_record.append_compare_true(res)
            else:
                for i in range(res['details'].__len__()):
                    res['details'][i]['location'] = time + ":" + res['details'][i]['location']
                compare_record.append_compare_false(res)

    def execute(self, context):

        url = 'csv/{}'.format(self.file_name)  # ftp远程csv目录
        path = '/tmp/csv/{}'.format(self.file_name)  # 本地csv缓存目录

        if not os.path.exists(path):
            # 如果没有缓存，就从ftp下载csv文件
            os.makedirs(os.path.dirname(path), exist_ok=True)
            downloader = FTP_Downloader()
            downloader.download(remote_path=url, local_path=path)

        # 从csv读取文件
        csv_records = get_csv_data(csvname=path, market_type=self.market_type, date_time=self.date_time,
                                   pre_close_price=self.pre_close_price,
                                   circulating_share_capital=self.circulating_share_capital)
        print("csv_records.length is {}".format(csv_records.__len__()))

        # 从mongodb获取sdk数据
        cursor = self.mongo_hk.get_collection('test_result').distinct('runnerID', {'jobID': self.jobID})
        runnerIDs = list(cursor) # 获取 runnerIDs（一般会有全真和测试2个环境）
        print('jobID is {}, runnerIDs is {}'.format(self.jobID, runnerIDs))
        # TODO: 确定要与全真环境对比还是测试环境
        runnerID = runnerIDs[0]
        sdk_records = self.get_mongo_data(runnerID)

        # 根据时间戳 datetime 对
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
            id2=self.file_name,
            rtype=StockResultTypes.File
        )
        self.compare_csv_sdk(results_sdk, results_csv, compare_record)
        result = compare_record.get_result()

        self.mongo_hk.get_collection('excel_result').insert_one(result)

        return {
            'result': result,
            'results_sdk': results_sdk,
            'results_csv': results_csv
        }
