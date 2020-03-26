import json
from time import sleep
from urllib import parse
import uuid
import requests

class CrawlerTestcase(object):
    def __init__(self, testcase_id, testcase_config, testcase_collector,
                 crawler_ctrl_url, crawler_duration_seconds, crawler_result_collector,
                 crawler_collection_name, record_collection_name):
        self.testcase_id = testcase_id
        self.testcase_config = testcase_config
        self.testcase_collector = testcase_collector
        self.crawler_ctrl_url = crawler_ctrl_url
        self.crawler_duration_seconds = crawler_duration_seconds

        self.crawler_result_collector = crawler_result_collector
        self.crawler_collection_name = crawler_collection_name
        self.record_collection_name = record_collection_name

    @staticmethod
    def generate_crawler_job_id() -> str:
        return str(uuid.uuid1())

    def generate_post_param(self, testcase_param) -> dict:
        raise NotImplementedError()

    def parse_crawler_result(self, crawler_result) -> list:
        raise NotImplementedError()

    def start_crawl(self):
        if self.testcase_config is None or self.testcase_config.paramStrs is None:
            return
        params = list()
        for param_str in self.testcase_config.paramStrs:
            try:
                obj = json.loads(param_str)
                params.append(obj)
            except json.JSONDecodeError:
                print('JSON decode error: %s' % param_str)

        for param in params:
            post_param = self.generate_post_param(testcase_param=param)
            crawler_job_id = CrawlerTestcase.generate_crawler_job_id()
            post_param['JOBID'] = crawler_job_id
            form_data = {
                'params': post_param
            }
            payload = parse.urlencode(form_data)
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            response = requests.post(self.crawler_ctrl_url, headers=headers, data=payload)
            resp_obj = response.json()
            if response.status_code == 200 and resp_obj is not None and resp_obj['status'] == 'SUCCESS' \
                    and 'data' in resp_obj and 'data' in resp_obj['data']:
                nested_data_str = resp_obj['data']['data']
                nested_data_obj = json.loads(nested_data_str)
                if nested_data_obj['status'] == 'ok':
                    print('Crawler(%s) start with param: \'%s\', response is: \'%s\'' % (
                    self.crawler_ctrl_url, post_param, response.text))
                    # wait until crawler done
                    sleep(self.crawler_duration_seconds)
                    crawler_result = self.crawler_result_collector.get_crawler_result(
                        collection_name=self.crawler_collection_name, crawler_job_id=crawler_job_id)
                    if len(crawler_result) == 0:
                        self.testcase_collector.on_test_fail(
                            collection_name=self.record_collection_name,
                            testcase_id=self.testcase_id,
                            param_data=param
                        )
                    else:
                        result_data = self.parse_crawler_result(crawler_result)
                        self.testcase_collector.on_test_success(
                            collection_name=self.record_collection_name,
                            testcase_id=self.testcase_id,
                            param_data=param,
                            result_data=result_data
                        )
                else:
                    print('Control crawler(%s) by param \'%s\' has error: %s' % (
                    self.crawler_ctrl_url, post_param, response.text))
            else:
                print('Control crawler(%s) by param \'%s\' has error: %s' % (
                self.crawler_ctrl_url, post_param, response.text))

