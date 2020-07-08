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

def test_data_compare():
    dbName = 'stockSdkTest'
    collectionName = 'test_result'
    runner_conf = get_test_runer_config(dbName=dbName, collectionName=collectionName)
    task_id_list = ['a', 'b']
    sort_id_list = ['sort1', 'sort2']
    id1 = 'RUN--3a52c1ce-162a-4dbb-9c2d-a86d05717fec'
    id2 = 'RUN--9c36d016-ff25-4bfb-a4d2-3cde074b2ab9'

    with DAG(dag_id='any_dag', start_date=datetime.now()) as dag:
        def push_function(**kwargs):
            kwargs['ti'].xcom_push(key=task_id_list[0], value=id1)
            kwargs['ti'].xcom_push(key=task_id_list[1], value=id2)


        runnerid_provider = PythonOperator(
            task_id='push_task',
            python_callable=push_function,
            provide_context=True
        )
        sorter1 = DataSortingOperator(
            task_id=sort_id_list[0],
            from_task=task_id_list[0],
            retries=3,
            provide_context=False,
            runner_conf=runner_conf,
            sort_and_comprae=True,
            dag=dag
        )
        sorter2 = DataSortingOperator(
            task_id=sort_id_list[1],
            from_task=task_id_list[1],
            retries=3,
            provide_context=False,
            runner_conf=runner_conf,
            sort_and_comprae=True,
            dag=dag
        )
        data_compare = DataCompareOperator(
            runner_conf=runner_conf,
            task_id='data_compare',
            provide_context=True,
            task_id_list=task_id_list,
            sort_id_list=sort_id_list,
            sort_and_comprae=True,
            quote_detail=False
        )
        runnerid_provider >> [sorter1, sorter2] >> data_compare
        execution_date = datetime.now()

        provider_instance = TaskInstance(task=runnerid_provider, execution_date=execution_date)
        runnerid_provider.execute(provider_instance.get_template_context())

        sorter1_instance = TaskInstance(task=sorter1, execution_date=execution_date)
        context_sorter1 = sorter1_instance.get_template_context()
        context_sorter1['run_id'] = 'fake-run'
        context_sorter1['expectation'] = 46
        context_sorter1['unit_test'] = True
        sorter1.execute(context_sorter1)

        sorter2_instance = TaskInstance(task=sorter2, execution_date=execution_date)
        context_sorter2 = sorter2_instance.get_template_context()
        context_sorter2['run_id'] = 'fake-run'
        context_sorter2['expectation'] = 46
        context_sorter2['unit_test'] = True
        sorter2.execute(context_sorter2)

        compare_instance = TaskInstance(task=data_compare, execution_date=execution_date)
        context = compare_instance.get_template_context()
        context['run_id'] = 'fake-run'
        context['expectation'] = 46
        context['unit_test'] = True
        if context.get('expectation') is not None:
            expectation = context.get('expectation')
        result = data_compare.execute(context)

    return result

# class TestDataCompareAndSortOperator(unittest.TestCase):
#
#     def test_data_compare_task_by_xcom(self):
#         result = test_data_compare()


if __name__ == '__main__':
    result = test_data_compare()
