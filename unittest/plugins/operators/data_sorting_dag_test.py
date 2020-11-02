import unittest
import json
from airflow import DAG, settings
from datetime import datetime

from airflow.models import TaskInstance
from airflow.operators.python_operator import PythonOperator

from operators.data_compare_operator import DataCompareOperator
from operators.data_sorting_operator import DataSortingOperator
from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig
from utils import *


def get_test_runer_config(dbName, collectionName):
    # just care for database
    runner_conf = RunnerConfig()
    runner_conf.jobID = 'TJ-1'
    runner_conf.runnerID = generate_id('RUN-A')
    runner_conf.storeConfig.mongoUri = 'mongodb://221.228.66.83:30617'
    runner_conf.storeConfig.dbName = dbName
    runner_conf.storeConfig.collectionName = collectionName
    runner_conf.storeConfig.restEndpoint = 'http://mongo-python-eve.sdk-test.svc.cluster.local:80'

    return runner_conf

def test_data_sorting():
    dbName = 'stockSdkTest'
    collectionName = 'test_result'
    runner_conf = get_test_runer_config(dbName=dbName, collectionName=collectionName)
    task_from = 'a'
    id = 'RUN--0370e5a1-6863-4278-b9b3-0ff6e5d24d23'

    with DAG(dag_id='any_dag', start_date=datetime.now()) as dag:
        def push_function(**kwargs):
            kwargs['ti'].xcom_push(key=task_from, value=id)

        runnerid_provider = PythonOperator(
            task_id='push_task',
            python_callable=push_function,
            provide_context=True
        )
        sorter = DataSortingOperator(
            task_id='android_sort_a',
            from_task=task_from,
            retries=3,
            provide_context=False,
            runner_conf=runner_conf,
            dag=dag
        )
        runnerid_provider >> sorter

        execution_date = datetime.now()

        provider_instance = TaskInstance(task=runnerid_provider, execution_date=execution_date)
        runnerid_provider.execute(provider_instance.get_template_context())

        sort_instance = TaskInstance(task=sorter, execution_date=execution_date)
        context = sort_instance.get_template_context()
        context['run_id'] = 'fake-run'
        context['expectation'] = 15
        context['unit_test'] = True
        if context.get('expectation') is not None:
            expectation = context.get('expectation')
        result, records = sorter.execute(context)

    return result

# class TestDataCompareOperator(unittest.TestCase):
#
#     def test_data_compare_task_by_xcom(self):
#         result = test_data_sorting()

if __name__ == '__main__':
    result = test_data_sorting()
    # import pymongo
    # client = pymongo.MongoClient("mongodb://221.228.66.83:30617")  # 远程MongoDB服务器
    # sdk_writer = SdkMongoWriter(client)
    # result2 = sdk_writer.write_result_record(result)