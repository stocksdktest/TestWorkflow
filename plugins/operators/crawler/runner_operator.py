import uuid
from datetime import datetime
from airflow.contrib.hooks.mongo_hook import MongoHook
from airflow.exceptions import AirflowException
from airflow.utils.decorators import apply_defaults

from operators.stock_operator import StockOperator
from operators.crawler.types import StockTestcaseClasses
from utils.mongo_hook import MongoHookWithDB

class CrawlerRunnerOperator(StockOperator):
    @apply_defaults
    def __init__(self, runner_conf, *args, **kwargs):
        super(CrawlerRunnerOperator, self).__init__(queue='worker', runner_conf=runner_conf, *args, **kwargs)
        self.cases_instance = list()

    def pre_execute(self, context):
        collector = CrawlerTestResultCollector(
            job_id=self.runner_conf.jobID,
            runner_id=self.runner_conf.runnerID
        )
        for case_config in self.runner_conf.casesConfig:
            testcase_id = case_config.testcaseID
            if testcase_id in StockTestcaseClasses:
                testcase_instance = StockTestcaseClasses[testcase_id](case_config, collector)
                print('Construct Crawler Testcase: %s' % testcase_id)
                self.cases_instance.append((testcase_id, testcase_instance))
            else:
                print('Testcase(%s) not implement' % testcase_id)

    def execute(self, context):
        for testcase_id, instance in self.cases_instance:
            try:
                crawl_func = getattr(instance, 'start_crawl')
                print('Execute Crawler start: %s' % testcase_id)
                crawl_func()
                print('Execute Crawler done: %s' % testcase_id)
            except Exception as e:
                print('CrawlerTestcase(%s) start_crawl() has error: %s' % (testcase_id, str(e)))


class CrawlerTestResultCollector(object):
    def __init__(self, job_id, runner_id):
        self.mongo_hk = MongoHookWithDB(conn_id='stocksdktest_mongo')

        self.job_id = job_id
        self.runner_id = runner_id

    def get_crawler_result(self, collection_name, crawler_job_id):
        col = self.mongo_hk.get_collection(collection_name)
        crawler_result = list()
        for document in col.find({'jobId': crawler_job_id}):
            crawler_result.append(document)
        return crawler_result

    def on_test_success(self, collection_name, testcase_id, param_data, result_data):
        col = self.mongo_hk.get_collection(collection_name)
        test_result_record = {
            'jobID': self.job_id,
            'runnerID': self.runner_id,
            'testcaseID': testcase_id,
            'recordID': str(uuid.uuid1()),
            'isPass': True,
            'startTime': datetime.now().timestamp(),
            'endTime': datetime.now().timestamp(),
            'paramData': param_data,
            'resultData': result_data
        }
        col.insert_one(test_result_record)

    def on_test_fail(self, collection_name, testcase_id, param_data):
        col = self.mongo_hk.get_collection(collection_name)
        test_result_record = {
            'jobID': self.job_id,
            'runnerID': self.runner_id,
            'testcaseID': testcase_id,
            'recordID': str(uuid.uuid1()),
            'isPass': False,
            'startTime': datetime.now().timestamp(),
            'endTime': datetime.now().timestamp(),
            'paramData': param_data,
            'exceptionData': { 'message': 'crawler can not get data' }
        }
        col.insert_one(test_result_record)