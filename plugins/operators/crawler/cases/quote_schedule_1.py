import re
from datetime import datetime, timedelta
from decimal import Decimal

from operators.crawler.cases.base import CrawlerTestcase

class QuoteSchedule_1(CrawlerTestcase):
    def __init__(self, testcase_config, collector, record_collection_name):
        # now = datetime.now()
        # endtime = datetime.strptime(self.ENDDATE,'%Y-%m-%d-%H-%M-%S')
        super(QuoteSchedule_1, self).__init__(
            testcase_config=testcase_config,
            testcase_collector = collector,
            record_collection_name=record_collection_name,
            crawler_result_collector=collector,
            # TODO 与Android和iOS类似，统一的testcase_id
            testcase_id='CRAWLER_QUOTEDETAIL_1',
            # TODO 爬虫平台对应的后端接口
            crawler_ctrl_url='http://192.168.128.58:8989/services/search/quoteSchedule',
            # TODO 预估一次爬虫运行所要花费的时间
            crawler_duration_seconds=20,
            # TODO 爬虫爬取结果所存的数据库
            crawler_collection_name='stock_his',
        )

    def generate_post_param(self, testcase_param):
        self.SHSC = testcase_param['SHSC']
        self.ENDDATE = testcase_param['ENDDATE']
        try:
            # TODO 爬虫平台接口调用参数，testcase_param对应于TestcaseConfig中的paramStrs
            return {
                'CODE': testcase_param['CODE_P'],
                'SUBTYPE': testcase_param['SUBTYPE'],
                'STARTDATE': testcase_param['STARTDATE'],
                'ENDDATE': testcase_param['ENDDATE'],
                'SHSC': testcase_param['SHSC'],
                # 'STARTDATE': cur.strftime('%Y-%m-%d-%H-%M-%S'),
                # 'ENDDATE': (cur + timedelta(seconds=self.crawler_duration_seconds)).strftime('%Y-%m-%d-%H-%M-%S')
            }
        except:
            raise Exception("Testcae(%s) param is invalid: '%s', miss some field" % (self.testcase_id, testcase_param))

    def custom_round(self,_float, _len=None):
        if _len != None:
            if str(_float)[::-1].find('.') <= _len:
                return (round(float(_float), _len))
            elif str(_float)[-1] == '5':
                return (round(float(str(_float)[:-1] + '6'), _len))
            else:
                return (round(float(_float), _len))
        else:
            if str(_float)[-1] == '5':
                return (round(float(str(_float)[:-1] + '6')))
            else:
                return (round(float(_float)))
    def judge(self,_any) -> bool:
        temporary = str(_any)
        try:
            float(temporary)
        except:
            return False
        else:
            return True
    def jjsjsj(self,cr) -> dict:
        print(self.judge(cr['shadiao']) if 'shadiao' in cr.keys() else 'laji')
        print('shadiao' in cr.keys())
        dictionary = {
            'shadiao':((cr['shadiao'] if float(cr['shadiao']) <= 0 else '+' + str(cr['shadiao'])) if self.judge(cr['shadiao']) else cr['shadiao']) if 'shadiao' in cr.keys() else '-',
        }
        return dictionary
    def parse_crawler_result(self, crawler_result) -> list:
        # TODO 将爬虫平台获得的数据格式转化为，与Android和iOS相对应的Testcase所生成的数据格式
        print('CrawlerTestcase(%s) get result: %s' % (self.testcase_id, crawler_result))
        print('-----------------------------------')
        print(self.jjsjsj({'shadiao':'-/-/-'}))
        print(self.custom_round(0.2135*10,2))
        print(Decimal(self.custom_round(0.0250 * 10, 1)).quantize(Decimal('0.000')))
        A = datetime.now()
        B = datetime.strptime(self.ENDDATE,'%Y-%m-%d-%H-%M-%S')
        print(A)
        print(B)
        print((B - A).seconds if B > A else 20)
        dictionary = {}
        if self.SHSC == 'HSQQ':
            for cr in crawler_result:
                dictionary1= {
                    'lastPrice': cr['lastPrice'] if 'lastPrice' in cr.keys() else '-',
                    'averageValue': cr['averageValue'] if 'averageValue' in cr.keys() else '-',
                    'changeRate': cr['changeRate'] if 'changeRate' in cr.keys() else '-',
                    'change': ((cr['change'] if float(cr['change']) <= 0 else '+' + str(cr['change'])) if self.judge(cr['change']) else cr['change']) if 'change' in cr.keys() else '-',
                    'volume': cr['volume'] if 'volume' in cr.keys() else '-',
                    'amount': (self.custom_round(cr['amount']) if self.judge(cr['amount']) else cr['amount']) if 'amount' in cr.keys() else '-',
                    'openInterest': cr['openInterest'] if 'openInterest' in cr.keys() else '-',
                    # 'position_chg': cr['position_chg'] if 'position_chg' in cr.keys() else '-',
                    'highPrice': cr['highPrice'] if 'highPrice' in cr.keys() else '-',
                    'lowPrice': cr['lowPrice'] if 'lowPrice' in cr.keys() else '-',
                    'setPrice': cr['setPrice'] if 'setPrice' in cr.keys() else '-',
                    'openPrice': cr['openPrice'] if 'openPrice' in cr.keys() else '-',
                    'presetPrice': cr['presetPrice'] if 'presetPrice' in cr.keys() else '-',
                    'stockUnit': cr['stockUnit'] if 'stockUnit' in cr.keys() else '-',
                    'limitUp': cr['limitUp'] if 'limitUp' in cr.keys() else '-',
                    'limitDown': cr['limitDown'] if 'limitDown' in cr.keys() else '-',
                    'excercisePx': (str(Decimal(self.custom_round(float(cr['excercisePx']) * 10, 3)).quantize(Decimal('0.000'))) if self.judge(cr['excercisePx']) else cr['excercisePx']) if 'excercisePx' in cr.keys() else '-',
                    'remainDate': cr['remainDate'] if 'remainDate' in cr.keys() else '-',
                    'inValue': cr['inValue'] if 'inValue' in cr.keys() else '-',
                    'premiumRate': cr['premiumRate'] if 'premiumRate' in cr.keys() else '-',
                    'impliedVolatility': cr['impliedVolatility'] if 'impliedVolatility' in cr.keys() else '-',
                    'delta': cr['delta'] if 'delta' in cr.keys() else '-',
                    'gramma': cr['gramma'] if 'gramma' in cr.keys() else '-',
                    'theta': cr['theta'] if 'theta' in cr.keys() else '-',
                    'vega': cr['vega'] if 'vega' in cr.keys() else '-',
                    'rho': cr['rho'] if 'rho' in cr.keys() else '-',
                    'sellPrices1': cr['sellPrices1'] if 'sellPrices1' in cr.keys() else '-',
                    'sellPrices2': cr['sellPrices2'] if 'sellPrices2' in cr.keys() else '-',
                    'sellPrices3': cr['sellPrices3'] if 'sellPrices3' in cr.keys() else '-',
                    'sellPrices4': cr['sellPrices4'] if 'sellPrices4' in cr.keys() else '-',
                    'sellPrices5': cr['sellPrices5'] if 'sellPrices5' in cr.keys() else '-',
                    'sellVolumes1': cr['sellVolumes1'] if 'sellVolumes1' in cr.keys() else '-',
                    'sellVolumes2': cr['sellVolumes2'] if 'sellVolumes2' in cr.keys() else '-',
                    'sellVolumes3': cr['sellVolumes3'] if 'sellVolumes3' in cr.keys() else '-',
                    'sellVolumes4': cr['sellVolumes4'] if 'sellVolumes4' in cr.keys() else '-',
                    'sellVolumes5': cr['sellVolumes5'] if 'sellVolumes5' in cr.keys() else '-',
                    'buyPrices1': cr['buyPrices1'] if 'buyPrices1' in cr.keys() else '-',
                    'buyPrices2': cr['buyPrices2'] if 'buyPrices2' in cr.keys() else '-',
                    'buyPrices3': cr['buyPrices3'] if 'buyPrices3' in cr.keys() else '-',
                    'buyPrices4': cr['buyPrices4'] if 'buyPrices4' in cr.keys() else '-',
                    'buyPrices5': cr['buyPrices5'] if 'buyPrices5' in cr.keys() else '-',
                    'buyVolumes1': cr['buyVolumes1'] if 'buyVolumes1' in cr.keys() else '-',
                    'buyVolumes2': cr['buyVolumes2'] if 'buyVolumes2' in cr.keys() else '-',
                    'buyVolumes3': cr['buyVolumes3'] if 'buyVolumes3' in cr.keys() else '-',
                    'buyVolumes4': cr['buyVolumes4'] if 'buyVolumes4' in cr.keys() else '-',
                    'buyVolumes5': cr['buyVolumes5'] if 'buyVolumes5' in cr.keys() else '-',
                }
                for i in dictionary1.keys():
                    dictionary1[i] = str(dictionary1[i])
                dictionary[re.sub('[- :]', '', cr['dataTime']) if 'dataTime' in cr.keys() else 'isEmpty'] = dictionary1
        elif self.SHSC == 'HSSC':
            for cr in crawler_result:
                dictionary1 = {
                    'lastPrice': cr['lastPrice'] if 'lastPrice' in cr.keys() else '-',
                    'averageValue': cr['averageValue'] if 'averageValue' in cr.keys() else '-',
                    'changeRate': cr['changeRate'] if 'changeRate' in cr.keys() else '-',
                    'change': ((cr['change'] if float(cr['change']) <= 0 else '+' + str(cr['change'])) if self.judge(cr['change']) else cr['change']) if 'change' in cr.keys() else '-',
                    'volume': cr['volume'] if 'volume' in cr.keys() else '-',
                    'amount': (self.custom_round(cr['amount']) if self.judge(cr['amount']) else cr['amount']) if 'amount' in cr.keys() else '-',
                    'turnoverRate': cr['turnoverRate'] if 'turnoverRate' in cr.keys() else '-',
                    'volumeRatio': cr['volumeRatio'] if 'volumeRatio' in cr.keys() else '-',
                    'highPrice': cr['highPrice'] if 'highPrice' in cr.keys() else '-',
                    'lowPrice': cr['lowPrice'] if 'lowPrice' in cr.keys() else '-',
                    'openPrice': cr['openPrice'] if 'openPrice' in cr.keys() else '-',
                    'preClosePrice': cr['preClosePrice'] if 'preClosePrice' in cr.keys() else '-',
                    'limitUp': cr['limitUp'] if 'limitUp' in cr.keys() else '-',
                    'limitDown': cr['limitDown'] if 'limitDown' in cr.keys() else '-',
                    'buyVolume': cr['buyVolume'] if 'buyVolume' in cr.keys() else '-',
                    'sellVolume': cr['sellVolume'] if 'sellVolume' in cr.keys() else '-',
                    'orderRatio': cr['orderRatio'] if 'orderRatio' in cr.keys() else '-',
                    'amplitudeRate': cr['amplitudeRate'] if 'amplitudeRate' in cr.keys() else '-',
                    'pe': cr['pe'] if 'pe' in cr.keys() else '-',
                    'pe2': cr['pe2'] if 'pe2' in cr.keys() else '-',
                    'netAsset': cr['netAsset'] if 'netAsset' in cr.keys() else '-',
                    'pb': cr['pb'] if 'pb' in cr.keys() else '-',
                    'capitalization': (self.custom_round(cr['capitalization']) if self.judge(cr['capitalization']) else cr['capitalization']) if 'capitalization' in cr.keys() else '-',
                    'totalValue': (self.custom_round(cr['totalValue']) if self.judge(cr['totalValue']) else cr['totalValue']) if 'totalValue' in cr.keys() else '-',
                    'circulatingShares': (self.custom_round(cr['circulatingShares']) if self.judge(cr['circulatingShares']) else cr['circulatingShares']) if 'circulatingShares' in cr.keys() else '-',
                    'flowValue': (self.custom_round(cr['flowValue']) if self.judge(cr['flowValue']) else cr['flowValue']) if 'flowValue' in cr.keys() else '-',
                    'sellPrices1': cr['sellPrices1'] if 'sellPrices1' in cr.keys() else '-',
                    'sellPrices2': cr['sellPrices2'] if 'sellPrices2' in cr.keys() else '-',
                    'sellPrices3': cr['sellPrices3'] if 'sellPrices3' in cr.keys() else '-',
                    'sellPrices4': cr['sellPrices4'] if 'sellPrices4' in cr.keys() else '-',
                    'sellPrices5': cr['sellPrices5'] if 'sellPrices5' in cr.keys() else '-',
                    'sellVolumes1': cr['sellVolumes1'] if 'sellVolumes1' in cr.keys() else '-',
                    'sellVolumes2': cr['sellVolumes2'] if 'sellVolumes2' in cr.keys() else '-',
                    'sellVolumes3': cr['sellVolumes3'] if 'sellVolumes3' in cr.keys() else '-',
                    'sellVolumes4': cr['sellVolumes4'] if 'sellVolumes4' in cr.keys() else '-',
                    'sellVolumes5': cr['sellVolumes5'] if 'sellVolumes5' in cr.keys() else '-',
                    'buyPrices1': cr['buyPrices1'] if 'buyPrices1' in cr.keys() else '-',
                    'buyPrices2': cr['buyPrices2'] if 'buyPrices2' in cr.keys() else '-',
                    'buyPrices3': cr['buyPrices3'] if 'buyPrices3' in cr.keys() else '-',
                    'buyPrices4': cr['buyPrices4'] if 'buyPrices4' in cr.keys() else '-',
                    'buyPrices5': cr['buyPrices5'] if 'buyPrices5' in cr.keys() else '-',
                    'buyVolumes1': cr['buyVolumes1'] if 'buyVolumes1' in cr.keys() else '-',
                    'buyVolumes2': cr['buyVolumes2'] if 'buyVolumes2' in cr.keys() else '-',
                    'buyVolumes3': cr['buyVolumes3'] if 'buyVolumes3' in cr.keys() else '-',
                    'buyVolumes4': cr['buyVolumes4'] if 'buyVolumes4' in cr.keys() else '-',
                    'buyVolumes5': cr['buyVolumes5'] if 'buyVolumes5' in cr.keys() else '-',
                }
                for i in dictionary1:
                    dictionary1[i] = str(dictionary1[i])
                dictionary[re.sub('[- :]','',cr['dataTime']) if 'dataTime' in cr.keys() else 'isEmpty'] = dictionary1
        elif self.SHSC == 'QHSC':
            for cr in crawler_result:
                dictionary1 = {
                    'lastPrice': cr['lastPrice'] if 'lastPrice' in cr.keys() else '-',
                    'averageValue': cr['averageValue'] if 'averageValue' in cr.keys() else '-',
                    'change': ((cr['change'] if float(cr['change']) <= 0 else '+' + str(cr['change'])) if self.judge(cr['change']) else cr['change']) if 'change' in cr.keys() else '-',
                    'changeRate': cr['changeRate'] if 'changeRate' in cr.keys() else '-',
                    'openPrice': cr['openPrice'] if 'openPrice' in cr.keys() else '-',
                    'highPrice': cr['highPrice'] if 'highPrice' in cr.keys() else '-',
                    'lowPrice': cr['lowPrice'] if 'lowPrice' in cr.keys() else '-',
                    'volume': cr['volume'] if 'volume' in cr.keys() else '-',
                    'amount': cr['amount'] if 'amount' in cr.keys() else '-',
                    'buyVolume': cr['buyVolume'] if 'buyVolume' in cr.keys() else '-',
                    'sellVolume': cr['sellVolume'] if 'sellVolume' in cr.keys() else '-',
                    'openInterest': cr['openInterest'] if 'openInterest' in cr.keys() else '-',
                    'preSettlement': cr['preSettlement'] if 'preSettlement' in cr.keys() else '-',
                    'position_chg': cr['position_chg'] if 'position_chg' in cr.keys() else '-',
                    'askpx1': cr['sellPrices1'] if 'sellPrices1' in cr.keys() else '-',
                    'askvol1': cr['sellVolumes1'] if 'sellVolumes1' in cr.keys() else '-',
                    'bidpx1': cr['buyPrices1'] if 'buyPrices1' in cr.keys() else '-',
                    'bidvol1': cr['buyVolumes1'] if 'buyVolumes1' in cr.keys() else '-',
                    # 'turnoverRate': cr['turnoverRate'] if 'turnoverRate' in cr.keys() else '-',
                    'limitUp': cr['limitUp'] if 'limitUp' in cr.keys() else '-',
                    'limitDown': cr['limitDown'] if 'limitDown' in cr.keys() else '-',
                    # 'volumeRatio': cr['volumeRatio'] if 'volumeRatio' in cr.keys() else '-',
                }
                for i in dictionary1:
                    dictionary1[i] = str(dictionary1[i])
                dictionary[re.sub('[- :]', '', cr['dataTime']) if 'dataTime' in cr.keys() else 'isEmpty'] = dictionary1
        elif self.SHSC == 'ZS':
            for cr in crawler_result:
                dictionary1 = {
                    'lastPrice': cr['lastPrice'] if 'lastPrice' in cr.keys() else '-',
                    'changeRate': cr['changeRate'] if 'changeRate' in cr.keys() else '-',
                    'change': ((cr['change'] if float(cr['change']) <= 0 else '+' + str(cr['change'])) if self.judge(cr['change']) else cr['change']) if 'change' in cr.keys() else '-',
                    'openPrice': cr['openPrice'] if 'openPrice' in cr.keys() else '-',
                    'highPrice': cr['highPrice'] if 'highPrice' in cr.keys() else '-',
                    'lowPrice': cr['lowPrice'] if 'lowPrice' in cr.keys() else '-',
                    'preClosePrice': cr['preClosePrice'] if 'preClosePrice' in cr.keys() else '-',
                    'amplitudeRate': cr['amplitudeRate'] if 'amplitudeRate' in cr.keys() else '-',
                    'volume': cr['volume'] if 'volume' in cr.keys() else '-',
                    'turnoverRate': cr['turnoverRate'] if 'turnoverRate' in cr.keys() else '-',
                    'volumeRatio': cr['volumeRatio'] if 'volumeRatio' in cr.keys() else '-',
                    'upCount': cr['upCount'] if 'upCount' in cr.keys() else '-',
                    'sameCount': cr['sameCount'] if 'sameCount' in cr.keys() else '-',
                    'downCount': cr['downCount'] if 'downCount' in cr.keys() else '-',
                    'averageValue': cr['averageValue'] if 'averageValue' in cr.keys() else '-',
                    'orderRatio': cr['orderRatio'] if 'orderRatio' in cr.keys() else '-',
                    'buyVolume': cr['buyVolume'] if 'buyVolume' in cr.keys() else '-',
                    'sellVolume': cr['sellVolume'] if 'sellVolume' in cr.keys() else '-',
                }
                for i in dictionary1:
                    dictionary1[i] = str(dictionary1[i])
                dictionary[re.sub('[- :]', '', cr['dataTime']) if 'dataTime' in cr.keys() else 'isEmpty'] = dictionary1
        elif self.SHSC == 'GG':
            for cr in crawler_result:
                dictionary1 = {
                    'lastPrice': cr['lastPrice'] if 'lastPrice' in cr.keys() else '-',
                    'averageValue': cr['averageValue'] if 'averageValue' in cr.keys() else '-',
                    'changeRate': cr['changeRate'] if 'changeRate' in cr.keys() else '-',
                    'change': ((cr['change'] if float(cr['change']) <= 0 else '+' + str(cr['change'])) if self.judge(cr['change']) else cr['change']) if 'change' in cr.keys() else '-',
                    'volume': cr['volume'] if 'volume' in cr.keys() else '-',
                    'amount': (self.custom_round(cr['amount']) if self.judge(cr['amount']) else cr['amount']) if 'amount' in cr.keys() else '-',
                    'turnoverRate': cr['turnoverRate'] if 'turnoverRate' in cr.keys() else '-',
                    'openPrice': cr['openPrice'] if 'openPrice' in cr.keys() else '-',
                    'preClosePrice': cr['preClosePrice'] if 'preClosePrice' in cr.keys() else '-',
                    'highPrice': cr['highPrice'] if 'highPrice' in cr.keys() else '-',
                    'lowPrice': cr['lowPrice'] if 'lowPrice' in cr.keys() else '-',
                    'buyVolume': cr['buyVolume'] if 'buyVolume' in cr.keys() else '-',
                    'sellVolume': cr['sellVolume'] if 'sellVolume' in cr.keys() else '-',
                    'pe': cr['pe'] if 'pe' in cr.keys() else '-',
                    'netAsset': (self.custom_round(cr['netAsset'],2) if self.judge(cr['netAsset']) else cr['netAsset']) if 'netAsset' in cr.keys() else '-',
                    'pb': cr['pb'] if 'pb' in cr.keys() else '-',
                    'capitalization': (self.custom_round(cr['capitalization']) if self.judge(cr['capitalization']) else cr['capitalization']) if 'capitalization' in cr.keys() else '-',
                    'totalValue': (self.custom_round(cr['totalValue']) if self.judge(cr['totalValue']) else cr['totalValue']) if 'totalValue' in cr.keys() else '-',
                    'hs': (self.custom_round(cr['hs']) if self.judge(cr['hs']) else cr['hs']) if 'hs' in cr.keys() else '-',
                    'HKTotalValue': (self.custom_round(cr['HKTotalValue']) if self.judge(cr['HKTotalValue']) else cr['HKTotalValue']) if 'HKTotalValue' in cr.keys() else '-',
                }
                for i in dictionary1:
                    dictionary1[i] = str(dictionary1[i])
                dictionary[re.sub('[- :]', '', cr['dataTime']) if 'dataTime' in cr.keys() else 'isEmpty'] = dictionary1
        elif self.SHSC == 'JJ':
            for cr in crawler_result:
                dictionary1 = {
                    'lastPrice': cr['lastPrice'] if 'lastPrice' in cr.keys() else '-',
                    'change': ((cr['change'] if float(cr['change']) <= 0 else '+' + str(cr['change'])) if self.judge(cr['change']) else cr['change']) if 'change' in cr.keys() else '-',
                    'changeRate': cr['changeRate'] if 'changeRate' in cr.keys() else '-',
                    'turnoverRate': cr['turnoverRate'] if 'turnoverRate' in cr.keys() else '-',
                    'limitUp': cr['limitUp'] if 'limitUp' in cr.keys() else '-',
                    'limitDown': cr['limitDown'] if 'limitDown' in cr.keys() else '-',
                    'openPrice': cr['openPrice'] if 'openPrice' in cr.keys() else '-',
                    'preClosePrice': cr['preClosePrice'] if 'preClosePrice' in cr.keys() else '-',
                    'highPrice': cr['highPrice'] if 'highPrice' in cr.keys() else '-',
                    'lowPrice': cr['lowPrice'] if 'lowPrice' in cr.keys() else '-',
                    'volumeRatio': cr['volumeRatio'] if 'volumeRatio' in cr.keys() else '-',
                    'volume': cr['volume'] if 'volume' in cr.keys() else '-',
                    'amount': (self.custom_round(cr['amount']) if self.judge(cr['amount']) else cr['amount']) if 'amount' in cr.keys() else '-',
                    'IOPV': cr['IOPV'] if 'IOPV' in cr.keys() else '-',
                    'sellPrices1': cr['sellPrices1'] if 'sellPrices1' in cr.keys() else '-',
                    'sellPrices2': cr['sellPrices2'] if 'sellPrices2' in cr.keys() else '-',
                    'sellPrices3': cr['sellPrices3'] if 'sellPrices3' in cr.keys() else '-',
                    'sellPrices4': cr['sellPrices4'] if 'sellPrices4' in cr.keys() else '-',
                    'sellPrices5': cr['sellPrices5'] if 'sellPrices5' in cr.keys() else '-',
                    'sellVolumes1': cr['sellVolumes1'] if 'sellVolumes1' in cr.keys() else '-',
                    'sellVolumes2': cr['sellVolumes2'] if 'sellVolumes2' in cr.keys() else '-',
                    'sellVolumes3': cr['sellVolumes3'] if 'sellVolumes3' in cr.keys() else '-',
                    'sellVolumes4': cr['sellVolumes4'] if 'sellVolumes4' in cr.keys() else '-',
                    'sellVolumes5': cr['sellVolumes5'] if 'sellVolumes5' in cr.keys() else '-',
                    'buyPrices1': cr['buyPrices1'] if 'buyPrices1' in cr.keys() else '-',
                    'buyPrices2': cr['buyPrices2'] if 'buyPrices2' in cr.keys() else '-',
                    'buyPrices3': cr['buyPrices3'] if 'buyPrices3' in cr.keys() else '-',
                    'buyPrices4': cr['buyPrices4'] if 'buyPrices4' in cr.keys() else '-',
                    'buyPrices5': cr['buyPrices5'] if 'buyPrices5' in cr.keys() else '-',
                    'buyVolumes1': cr['buyVolumes1'] if 'buyVolumes1' in cr.keys() else '-',
                    'buyVolumes2': cr['buyVolumes2'] if 'buyVolumes2' in cr.keys() else '-',
                    'buyVolumes3': cr['buyVolumes3'] if 'buyVolumes3' in cr.keys() else '-',
                    'buyVolumes4': cr['buyVolumes4'] if 'buyVolumes4' in cr.keys() else '-',
                    'buyVolumes5': cr['buyVolumes5'] if 'buyVolumes5' in cr.keys() else '-',
                }
                for i in dictionary1:
                    dictionary1[i] = str(dictionary1[i])
                dictionary[re.sub('[- :]', '', cr['dataTime']) if 'dataTime' in cr.keys() else 'isEmpty'] = dictionary1
        elif self.SHSC == 'ZQ':
            for cr in crawler_result:
                dictionary1 = {
                    'lastPrice': cr['lastPrice'] if 'lastPrice' in cr.keys() else '-',
                    'change': ((cr['change'] if float(cr['change']) <= 0 else '+' + str(cr['change'])) if self.judge(cr['change']) else cr['change']) if 'change' in cr.keys() else '-',
                    'changeRate': cr['changeRate'] if 'changeRate' in cr.keys() else '-',
                    'volume': cr['volume'] if 'volume' in cr.keys() else '-',
                    'volumeRatio': cr['volumeRatio'] if 'volumeRatio' in cr.keys() else '-',
                    'amount': (self.custom_round(cr['amount']) if self.judge(cr['amount']) else cr['amount']) if 'amount' in cr.keys() else '-',
                    'openPrice': cr['openPrice'] if 'openPrice' in cr.keys() else '-',
                    'preClosePrice': cr['preClosePrice'] if 'preClosePrice' in cr.keys() else '-',
                    'buyVolume': cr['buyVolume'] if 'buyVolume' in cr.keys() else '-',
                    'sellVolume': cr['sellVolume'] if 'sellVolume' in cr.keys() else '-',
                    'sellPrices1': cr['sellPrices1'] if 'sellPrices1' in cr.keys() else '-',
                    'sellPrices2': cr['sellPrices2'] if 'sellPrices2' in cr.keys() else '-',
                    'sellPrices3': cr['sellPrices3'] if 'sellPrices3' in cr.keys() else '-',
                    'sellPrices4': cr['sellPrices4'] if 'sellPrices4' in cr.keys() else '-',
                    'sellPrices5': cr['sellPrices5'] if 'sellPrices5' in cr.keys() else '-',
                    'sellVolumes1': cr['sellVolumes1'] if 'sellVolumes1' in cr.keys() else '-',
                    'sellVolumes2': cr['sellVolumes2'] if 'sellVolumes2' in cr.keys() else '-',
                    'sellVolumes3': cr['sellVolumes3'] if 'sellVolumes3' in cr.keys() else '-',
                    'sellVolumes4': cr['sellVolumes4'] if 'sellVolumes4' in cr.keys() else '-',
                    'sellVolumes5': cr['sellVolumes5'] if 'sellVolumes5' in cr.keys() else '-',
                    'buyPrices1': cr['buyPrices1'] if 'buyPrices1' in cr.keys() else '-',
                    'buyPrices2': cr['buyPrices2'] if 'buyPrices2' in cr.keys() else '-',
                    'buyPrices3': cr['buyPrices3'] if 'buyPrices3' in cr.keys() else '-',
                    'buyPrices4': cr['buyPrices4'] if 'buyPrices4' in cr.keys() else '-',
                    'buyPrices5': cr['buyPrices5'] if 'buyPrices5' in cr.keys() else '-',
                    'buyVolumes1': cr['buyVolumes1'] if 'buyVolumes1' in cr.keys() else '-',
                    'buyVolumes2': cr['buyVolumes2'] if 'buyVolumes2' in cr.keys() else '-',
                    'buyVolumes3': cr['buyVolumes3'] if 'buyVolumes3' in cr.keys() else '-',
                    'buyVolumes4': cr['buyVolumes4'] if 'buyVolumes4' in cr.keys() else '-',
                    'buyVolumes5': cr['buyVolumes5'] if 'buyVolumes5' in cr.keys() else '-',
                }
                for i in dictionary1:
                    dictionary1[i] = str(dictionary1[i])
                dictionary[re.sub('[- :]', '', cr['dataTime']) if 'dataTime' in cr.keys() else 'isEmpty'] = dictionary1
        elif self.SHSC == 'KCB':
            for cr in crawler_result:
                dictionary1 = {
                    'lastPrice': cr['lastPrice'] if 'lastPrice' in cr.keys() else '-',
                    'averageValue': cr['averageValue'] if 'averageValue' in cr.keys() else '-',
                    'changeRate': cr['changeRate'] if 'changeRate' in cr.keys() else '-',
                    'change': ((cr['change'] if float(cr['change']) <= 0 else '+' + str(cr['change'])) if self.judge(cr['change']) else cr['change']) if 'change' in cr.keys() else '-',
                    'volume': cr['volume'] if 'volume' in cr.keys() else '-',
                    'amount': (self.custom_round(cr['amount']) if self.judge(cr['amount']) else cr['amount']) if 'amount' in cr.keys() else '-',
                    'turnoverRate': cr['turnoverRate'] if 'turnoverRate' in cr.keys() else '-',
                    'volumeRatio': cr['volumeRatio'] if 'volumeRatio' in cr.keys() else '-',
                    'highPrice': cr['highPrice'] if 'highPrice' in cr.keys() else '-',
                    'lowPrice': cr['lowPrice'] if 'lowPrice' in cr.keys() else '-',
                    'openPrice': cr['openPrice'] if 'openPrice' in cr.keys() else '-',
                    'preClosePrice': cr['preClosePrice'] if 'preClosePrice' in cr.keys() else '-',
                    'limitUp': cr['limitUp'] if 'limitUp' in cr.keys() else '-',
                    'limitDown': cr['limitDown'] if 'limitDown' in cr.keys() else '-',
                    'buyVolume': cr['buyVolume'] if 'buyVolume' in cr.keys() else '-',
                    'sellVolume': cr['sellVolume'] if 'sellVolume' in cr.keys() else '-',
                    'orderRatio': cr['orderRatio'] if 'orderRatio' in cr.keys() else '-',
                    'amplitudeRate': cr['amplitudeRate'] if 'amplitudeRate' in cr.keys() else '-',
                    'afterHoursVolume': cr['afterHoursVolume'] if 'afterHoursVolume' in cr.keys() else '-',
                    'afterHoursAmount': cr['afterHoursAmount'] if 'afterHoursAmount' in cr.keys() else '-',
                    'pe': cr['pe'] if 'pe' in cr.keys() else '-',
                    'pe2': cr['pe2'] if 'pe2' in cr.keys() else '-',
                    'netAsset': (self.custom_round(cr['netAsset'],2) if self.judge(cr['netAsset']) else cr['netAsset']) if 'netAsset' in cr.keys() else '-',
                    'pb': cr['pb'] if 'pb' in cr.keys() else '-',
                    'vote': cr['vote'] if 'vote' in cr.keys() else '-',
                    'capitalization': (self.custom_round(cr['capitalization']) if self.judge(cr['capitalization']) else cr['capitalization']) if 'capitalization' in cr.keys() else '-',
                    'totalValue': (self.custom_round(cr['totalValue']) if self.judge(cr['totalValue']) else cr['totalValue']) if 'totalValue' in cr.keys() else '-',
                    'circulatingShares': (self.custom_round(cr['circulatingShares']) if self.judge(cr['circulatingShares']) else cr['circulatingShares']) if 'circulatingShares' in cr.keys() else '-',
                    'flowValue': (self.custom_round(cr['flowValue']) if self.judge(cr['flowValue']) else cr['flowValue']) if 'flowValue' in cr.keys() else '-',
                    'issuedCapital': cr['issuedCapital'] if 'issuedCapital' in cr.keys() else '-',
                    'upf': cr['upf'] if 'upf' in cr.keys() else '-',
                    'sellPrices1': cr['sellPrices1'] if 'sellPrices1' in cr.keys() else '-',
                    'sellPrices2': cr['sellPrices2'] if 'sellPrices2' in cr.keys() else '-',
                    'sellPrices3': cr['sellPrices3'] if 'sellPrices3' in cr.keys() else '-',
                    'sellPrices4': cr['sellPrices4'] if 'sellPrices4' in cr.keys() else '-',
                    'sellPrices5': cr['sellPrices5'] if 'sellPrices5' in cr.keys() else '-',
                    'sellVolumes1': cr['sellVolumes1'] if 'sellVolumes1' in cr.keys() else '-',
                    'sellVolumes2': cr['sellVolumes2'] if 'sellVolumes2' in cr.keys() else '-',
                    'sellVolumes3': cr['sellVolumes3'] if 'sellVolumes3' in cr.keys() else '-',
                    'sellVolumes4': cr['sellVolumes4'] if 'sellVolumes4' in cr.keys() else '-',
                    'sellVolumes5': cr['sellVolumes5'] if 'sellVolumes5' in cr.keys() else '-',
                    'buyPrices1': cr['buyPrices1'] if 'buyPrices1' in cr.keys() else '-',
                    'buyPrices2': cr['buyPrices2'] if 'buyPrices2' in cr.keys() else '-',
                    'buyPrices3': cr['buyPrices3'] if 'buyPrices3' in cr.keys() else '-',
                    'buyPrices4': cr['buyPrices4'] if 'buyPrices4' in cr.keys() else '-',
                    'buyPrices5': cr['buyPrices5'] if 'buyPrices5' in cr.keys() else '-',
                    'buyVolumes1': cr['buyVolumes1'] if 'buyVolumes1' in cr.keys() else '-',
                    'buyVolumes2': cr['buyVolumes2'] if 'buyVolumes2' in cr.keys() else '-',
                    'buyVolumes3': cr['buyVolumes3'] if 'buyVolumes3' in cr.keys() else '-',
                    'buyVolumes4': cr['buyVolumes4'] if 'buyVolumes4' in cr.keys() else '-',
                    'buyVolumes5': cr['buyVolumes5'] if 'buyVolumes5' in cr.keys() else '-',
                }
                for i in dictionary1:
                    dictionary1[i] = str(dictionary1[i])
                dictionary[re.sub('[- :]', '', cr['dataTime']) if 'dataTime' in cr.keys() else 'isEmpty'] = dictionary1
        else:
            print('-------输入的(SHSC)不在范围内--------')
        print(dictionary)
        return dictionary
