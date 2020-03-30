from datetime import datetime, timedelta

from operators.crawler.cases.base import CrawlerTestcase

class OhlcSchedule_2(CrawlerTestcase):
    def __init__(self, testcase_config, collector, record_collection_name):
        super(OhlcSchedule_2, self).__init__(
            testcase_config=testcase_config,
            testcase_collector = collector,
            record_collection_name=record_collection_name,
            crawler_result_collector=collector,
            # TODO 与Android和iOS类似，统一的testcase_id
            testcase_id='OHLCV3_2',
            # TODO 爬虫平台对应的后端接口
            crawler_ctrl_url='http://153.37.190.164:8989/services/search/ohlcSchedule',
            # TODO 预估一次爬虫运行所要花费的时间
            crawler_duration_seconds=90,
            # TODO 爬虫爬取结果所存的数据库
            crawler_collection_name='stock_kline',
        )

    def generate_post_param(self, testcase_param):
        cur = datetime.now()
        try:
            # TODO 爬虫平台接口调用参数，testcase_param对应于TestcaseConfig中的paramStrs
            return {
                'CODE': testcase_param['CODE'],
                'PERIOD': testcase_param['PERIOD'],
                'SUBTYPE': testcase_param['SUBTYPE'],
                'PRICEADJUSTEDMODE': testcase_param['PRICEADJUSTEDMODE'],
                'COUNT': testcase_param['COUNT'],
                # 'STARTDATE': testcase_param['STARTDATE'],
                'ENDDATE': testcase_param['ENDDATE']
            }
        except:
            raise Exception("Testcae(%s) param is invalid: '%s', miss some field" % (self.testcase_id, testcase_param))


    def parse_crawler_result(self, crawler_result) -> list:
        # TODO 将爬虫平台获得的数据格式转化为，与Android和iOS相对应的Testcase所生成的数据格式
        print('CrawlerTestcase(%s) get result: %s' % (self.testcase_id, crawler_result))
        return crawler_result
