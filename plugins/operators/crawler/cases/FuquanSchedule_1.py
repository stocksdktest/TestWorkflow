import re
from datetime import datetime, timedelta
from decimal import Decimal
from operators.crawler.cases.base import CrawlerTestcase

class FuquanSchedule_1(CrawlerTestcase):
    def __init__(self, testcase_config, collector, record_collection_name):
        super(FuquanSchedule_1, self).__init__(
            testcase_config=testcase_config,
            testcase_collector = collector,
            record_collection_name=record_collection_name,
            crawler_result_collector=collector,
            # TODO 与Android和iOS类似，统一的testcase_id
            testcase_id='CRAWLER_OHLCSUBTEST_1',
            # TODO 爬虫平台对应的后端接口
            crawler_ctrl_url='http://153.37.190.164:8989/services/search/fuquanSchedule',
            # TODO 预估一次爬虫运行所要花费的时间
            crawler_duration_seconds=20,
            # TODO 爬虫爬取结果所存的数据库
            crawler_collection_name='stock_fuquan',
        )

    def generate_post_param(self, testcase_param):
        cur = datetime.now()
        try:
            # TODO 爬虫平台接口调用参数，testcase_param对应于TestcaseConfig中的paramStrs
            return {
                'CODE': testcase_param['CODE_P'],
            }
        except:
            raise Exception("Testcae(%s) param is invalid: '%s', miss some field" % (self.testcase_id, testcase_param))


    def parse_crawler_result(self, crawler_result) -> list:
        # TODO 将爬虫平台获得的数据格式转化为，与Android和iOS相对应的Testcase所生成的数据格式
        print('CrawlerTestcase(%s) get result: %s' % (self.testcase_id, crawler_result))
        print('-----------------------------------')
        dictionary = {}
        j = 0
        for cr in crawler_result:
            dictionary1 = {
                'datetime': re.sub('[-]','',cr['dateTime']) if 'dateTime' in cr.keys() else '-',
                'bonusProportion': cr['bonusProportion'] if 'bonusProportion' in cr.keys() else '-',
                'allotmentProportion': cr['allotmentProportion'] if 'allotmentProportion' in cr.keys() else '-',
                'allotmentPrice': cr['allotmentPrice'] if 'allotmentPrice' in cr.keys() else '-',
                'increaseProportion': cr['increaseProportion'] if 'increaseProportion' in cr.keys() else '-',
                'increasePrice': cr['increasePrice'] if 'increasePrice' in cr.keys() else '-',
                'increaseVolume': cr['increaseVolume'] if 'increaseVolume' in cr.keys() else '-',
                'bonusAmount': cr['bonusAmount'] if 'bonusAmount' in cr.keys() else '-',
            }
            for i in dictionary1.keys():
                dictionary1[i] = Decimal(self.custom_round(dictionary1[i],3)).quantize(Decimal('0.000')) if self.judge(dictionary1[i]) else dictionary1[i]
                dictionary1[i] = str(dictionary1[i])
            dictionary1['datetime'] = str(int(float(dictionary1['datetime']))) if self.judge(dictionary1['datetime']) else dictionary1['datetime']
            dictionary[re.sub('[-]', '', cr['dateTime']) if 'dateTime' in cr.keys() else 'isEmpty_' + str(j)] = dictionary1
            j += 1
        print(dictionary)
        return dictionary
