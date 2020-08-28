import unittest
import json
from airflow import DAG, settings
from datetime import datetime

from airflow.models import TaskInstance
from airflow.operators.python_operator import PythonOperator

from operators.data_compare_operator import DataCompareOperator
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

def test_data_compare():
    dbName = 'stockSdkTest'
    collectionName = 'test_result'
    runner_conf = get_test_runer_config(dbName=dbName, collectionName=collectionName)
    task_id_list = ['a', 'b']
    id1 = 'RUN--52fb7f41-aa24-496c-9e19-faa49d2780f7'
    id2 = 'RUN--df2dbe1c-bcee-4724-a207-3def57f2fcb4'

    with DAG(dag_id='any_dag', start_date=datetime.now()) as dag:
        def push_function(**kwargs):
            kwargs['ti'].xcom_push(key=task_id_list[0], value=id1)
            kwargs['ti'].xcom_push(key=task_id_list[1], value=id2)


        runnerid_provider = PythonOperator(
            task_id='push_task',
            python_callable=push_function,
            provide_context=True
        )
        data_compare = DataCompareOperator(
            runner_conf=runner_conf,
            task_id='data_compare',
            provide_context=True,
            task_id_list=task_id_list,
            quote_detail=False
        )
        runnerid_provider >> data_compare

        execution_date = datetime.now()

        provider_instance = TaskInstance(task=runnerid_provider, execution_date=execution_date)
        runnerid_provider.execute(provider_instance.get_template_context())

        compare_instance = TaskInstance(task=data_compare, execution_date=execution_date)
        context = compare_instance.get_template_context()
        context['run_id'] = 'fake-run'
        context['expectation'] = 8
        context['unit_test'] = True
        if context.get('expectation') is not None:
            expectation = context.get('expectation')
        data_compare.pre_execute(context)
        result = data_compare.execute(context)

    return result

# class TestDataCompareOperator(unittest.TestCase):
#
#     def test_data_compare_task_by_xcom(self):
#         result = test_data_compare()

if __name__ == '__main__':
    result = test_data_compare()
