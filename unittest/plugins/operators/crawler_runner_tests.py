import unittest
import uuid
import json
from datetime import datetime
from airflow import DAG, settings
from airflow.models import Connection, TaskInstance

from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig
from operators.crawler.runner_operator import CrawlerRunnerOperator

class TestCrawlerRunnerOperator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        conn = Connection(
            conn_id='stocksdktest_mongo',
            host='221.228.66.83',
            port=30617,
        )
        conn.set_extra(json.dumps({
            'database': 'stockSdkTest'
        }))
        session = settings.Session()
        session.add(conn)
        session.commit()

    def test_construct_invalid_crawler_testcase(self):
        runner_conf = RunnerConfig()

        runner_conf.storeConfig.mongoUri = 'mongodb://221.228.66.83:30617'
        runner_conf.storeConfig.dbName = 'stockSdkTest'
        runner_conf.storeConfig.collectionName = 'test_result'
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'TESTCASE_INVALID'
        runner_conf.casesConfig.extend([case_conf])

        with DAG(dag_id='any_dag', start_date=datetime.now()) as dag:
            crawler_runner = CrawlerRunnerOperator(
                task_id='crawler',
                provide_context=False,
                runner_conf=runner_conf
            )

            task_instance = TaskInstance(task=crawler_runner, execution_date=datetime.now())
            context = task_instance.get_template_context()
            context['run_id'] = str(uuid.uuid4())
            crawler_runner.pre_execute(context)
            crawler_runner.execute(context)

            self.assertEqual(len(crawler_runner.cases_instance), 0)

    def test_construct_valid_crawler_testcase(self):
        runner_conf = RunnerConfig()

        runner_conf.storeConfig.mongoUri = 'mongodb://221.228.66.83:30617'
        runner_conf.storeConfig.dbName = 'stockSdkTest'
        runner_conf.storeConfig.collectionName = 'test_result'
        case_conf = TestcaseConfig()
        case_conf.testcaseID = 'QUOTEDETAIL_1'
        case_conf.continueWhenFailed = True
        case_conf.roundIntervalSec = 3
        case_conf.paramStrs.extend([
            json.dumps({
                'CODE': '600000.sh',
                'SUBTYPE': 'SH1001',
                'DURATION_SECONDS': 60,
                # 'STARTDATE': '2020-03-30-15-30-00',
                # 'ENDDATE': '2020-03-30-15-41-00',
            }),
        ])
        runner_conf.casesConfig.extend([case_conf])

        with DAG(dag_id='any_dag', start_date=datetime.now()) as dag:
            crawler_runner = CrawlerRunnerOperator(
                task_id='crawler',
                provide_context=False,
                runner_conf=runner_conf
            )

            task_instance = TaskInstance(task=crawler_runner, execution_date=datetime.now())
            context = task_instance.get_template_context()
            context['run_id'] = str(uuid.uuid4())
            crawler_runner.pre_execute(context)
            crawler_runner.execute(context)

            self.assertEqual(len(crawler_runner.cases_instance), 1)
