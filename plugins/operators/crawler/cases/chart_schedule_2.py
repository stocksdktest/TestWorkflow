from datetime import datetime, timedelta
import re
from operators.crawler.cases.base import CrawlerTestcase

class ChartSchedule_2(CrawlerTestcase):
    def __init__(self, testcase_config, collector, record_collection_name):
        super(ChartSchedule_2, self).__init__(
            testcase_config=testcase_config,
            testcase_collector = collector,
            record_collection_name=record_collection_name,
            crawler_result_collector=collector,
            # TODO 与Android和iOS类似，统一的testcase_id
            testcase_id='CRAWLER_CHARTV2TEST_2',
            # TODO 爬虫平台对应的后端接口
            crawler_ctrl_url='http://153.37.190.164:8989/services/search/chartSchedule',
            # TODO 预估一次爬虫运行所要花费的时间
            crawler_duration_seconds=20,
            # TODO 爬虫爬取结果所存的数据库
            crawler_collection_name='stock_trend',
        )

    def generate_post_param(self, testcase_param):
        self.TYPE = testcase_param['TYPE']
        try:
            # TODO 爬虫平台接口调用参数，testcase_param对应于TestcaseConfig中的paramStrs
            return {
                'CODE': testcase_param['CODE_P'],
                'TYPE': testcase_param['TYPE'],
                'SUBTYPE': testcase_param['SUBTYPE'],
            }
        except:
            raise Exception("Testcae(%s) param is invalid: '%s', miss some field" % (self.testcase_id, testcase_param))


    def parse_crawler_result(self, crawler_result) -> list:
        # TODO 将爬虫平台获得的数据格式转化为，与Android和iOS相对应的Testcase所生成的数据格式
        print('CrawlerTestcase(%s) get result: %s' % (self.testcase_id, crawler_result))
        print('-----------------------------------')
        dictionary = {}
        if self.TYPE == 'ChartTypeBeforeData':
            for cr in crawler_result:
                dictionary[re.sub('[- :]','',cr['transactionTime']) if 'transactionTime' in cr.keys() else 'isEmpty'] = {
                    'datetime' : re.sub('[- :]','',cr['transactionTime']) if 'transactionTime' in cr.keys() else '-',
                    'closePrice' : str(cr['transactionPrice']) if 'transactionPrice' in cr.keys() else '-',
                    # 'tradeVolume' : str(cr['singleVolume']) if 'singleVolume' in cr.keys() else '-',
                    # 'averagePrice' : str(cr['averagePrice']) if 'averagePrice' in cr.keys() else '-',
                }
        elif self.TYPE == 'ChartTypeAfterData':
            for cr in crawler_result:
                dictionary[re.sub('[- :]','',cr['transactionTime']) if 'transactionTime' in cr.keys() else 'isEmpty'] = {
                    'datetime' : re.sub('[- :]','',cr['transactionTime']) if 'transactionTime' in cr.keys() else '-',
                    'closePrice' : str(cr['transactionPrice']) if 'transactionPrice' in cr.keys() else '-',
                    'tradeVolume' : str(cr['singleVolume']) if 'singleVolume' in cr.keys() else '-',
                    # 'averagePrice' : str(cr['averagePrice']) if 'averagePrice' in cr.keys() else '-',
                }
        else:
            for cr in crawler_result:
                dictionary[re.sub('[- :]','',cr['transactionTime']) if 'transactionTime' in cr.keys() else 'isEmpty'] = {
                    'datetime' : re.sub('[- :]','',cr['transactionTime']) if 'transactionTime' in cr.keys() else '-',
                    'closePrice' : str(cr['transactionPrice']) if 'transactionPrice' in cr.keys() else '-',
                    'tradeVolume' : str(cr['singleVolume']) if 'singleVolume' in cr.keys() else '-',
                    'averagePrice' : str(cr['averagePrice']) if 'averagePrice' in cr.keys() else '-',
                }
        print(dictionary)
        return dictionary
