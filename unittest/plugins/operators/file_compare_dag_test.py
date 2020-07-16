import unittest
import json
from airflow import DAG, settings
from datetime import datetime

from airflow.models import TaskInstance
from airflow.operators.python_operator import PythonOperator

from operators.data_compare_operator import DataCompareOperator
from operators.file_compare_operator import FileCompareOperator
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

def test_file_compare():
    dbName = 'stockSdkTest'
    collectionName = 'test_result'
    runner_conf = get_test_runer_config(dbName=dbName, collectionName=collectionName)
    task_id_list = ['a', 'b']
    id1 = 'a' # useless
    id2 = 'b' # useless
    date_time = '20200702'
    # 5.12 original version
    # jobID = 'manual__2020-05-12T00:55:55.479340 00:00',
    # file_name = '5.12-600000.sh.csv'
    # 上海市场
    # 688001.sh
    # jobID = 'manual__2020-06-24T01:03:08.609581 00:00'
    # file_name = 'DispMD_5688001_20200629.csv'
    # market_type = 'sh'
    # pre_close_price = 45380
    # circulating_share_capital = 38451196
    # 600000.sh
    # jobID = 'manual__2020-06-24T01:03:16.349728 00:00'
    # file_name = 'DispMD_5600000_20200629.csv'
    # market_type = 'sh'
    # pre_close_price = 10480
    # circulating_share_capital = 28103794812
    # 900905.sh
    # jobID = 'manual__2020-06-24T01:03:44.519576 00:00'
    # file_name = 'DispMD_5900905_20200629.csv'
    # market_type = 'sh'
    # pre_close_price = 3045
    # circulating_share_capital = 206008134
    # 深圳市场
    # 002032.sz
    jobID = 'manual__2020-07-02T00:59:51.811376 00:00'
    file_name = 'DispMD_7002032_20200703.csv'
    market_type = 'sz'
    pre_close_price = 72130
    circulating_share_capital = 610742243
    # 399001.sz
    # jobID = 'manual__2020-07-02T01:01:13.571553 00:00'
    # file_name = 'DispMD_7399001_20200703.csv'
    # 200596.sz
    # jobID = 'manual__2020-07-02T01:02:54.086476 00:00'
    # file_name = 'DispMD_7200596_20200703.csv'
    # market_type = 'sz'
    # pre_close_price = 84700
    # circulating_share_capital = 120000000


    with DAG(dag_id='any_dag', start_date=datetime.now()) as dag:
        def push_function(**kwargs):
            kwargs['ti'].xcom_push(key=task_id_list[0], value=id1)
            kwargs['ti'].xcom_push(key=task_id_list[1], value=id2)


        runnerid_provider = PythonOperator(
            task_id='push_task',
            python_callable=push_function,
            provide_context=True
        )
        file_compare = FileCompareOperator(
            runner_conf = runner_conf,
            task_id='file_compare',
            provide_context=True,
            jobID=jobID,
            file_name=file_name,
            date_time=date_time,
            market_type=market_type,
            pre_close_price=pre_close_price,
            circulating_share_capital=circulating_share_capital
        )

        runnerid_provider >> file_compare

        execution_date = datetime.now()

        provider_instance = TaskInstance(task=runnerid_provider, execution_date=execution_date)
        runnerid_provider.execute(provider_instance.get_template_context())

        compare_instance = TaskInstance(task=file_compare, execution_date=execution_date)
        context = compare_instance.get_template_context()
        context['run_id'] = 'fake-run'
        context['expectation'] = 8
        context['unit_test'] = True
        if context.get('expectation') is not None:
            expectation = context.get('expectation')
        result = file_compare.execute(context)

    return result


if __name__ == '__main__':
    result = test_file_compare()
