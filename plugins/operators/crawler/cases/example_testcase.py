from datetime import datetime, timedelta

from operators.crawler.cases.base import CrawlerTestcase

class ExampleTestcase(CrawlerTestcase):
    def __init__(self, testcase_config, collector):
        super(ExampleTestcase, self).__init__(
            testcase_id='TESTCASE_0',
            testcase_config=testcase_config,
            testcase_collector = collector,
            crawler_ctrl_url='http://153.37.190.164:8989/services/search/quoteSchedule',
            crawler_duration_seconds=90,
            mongo_collector=collector,
            crawler_collection_name='stock_his',
            record_collection_name='test_result'
        )

    def generate_post_param(self, testcase_param):
        cur = datetime.now()
        try:
            return {
                'CODE': testcase_param['CODE'],
                'SUBTYPE': testcase_param['SUBTYPE'],
                'STARTDATE': cur.strftime('%Y-%m-%d-%H-%M-%S'),
                'ENDDATE': (cur + timedelta(seconds=self.crawler_duration_seconds)).strftime('%Y-%m-%d-%H-%M-%S')
            }
        except:
            raise Exception("Testcae(%s) param is invalid: '%s', miss some field" % (self.testcase_id, testcase_param))


    def parse_crawler_result(self, crawler_result) -> list:
        print('CrawlerTestcase(%s) get result: %s' % (self.testcase_id, crawler_result))
        return crawler_result
