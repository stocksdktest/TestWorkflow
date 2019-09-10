import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(0),
}

with DAG(
    dag_id='StockSDKTest',
    default_args=args,
    schedule_interval='@once',
) as dag:
    compare_1 = DummyOperator(
        task_id='结果比对-Testcase-1',
    )

    android_1 = DummyOperator(
        task_id='股票信息-Android-Testcase-1'
    )

    ios_1 = DummyOperator(
        task_id='股票信息-iOS-Testcase-1'
    )

    crawler_1 = DummyOperator(
        task_id='股票信息-Crawler-Testcase-1'
    )

    compare_2 = DummyOperator(
        task_id='结果比对-Testcase-2',
    )

    android_2 = DummyOperator(
        task_id='股票信息-Android-Testcase-2'
    )

    ios_2 = DummyOperator(
        task_id='股票信息-iOS-Testcase-2'
    )

    crawler_2 = DummyOperator(
        task_id='股票信息-Crawler-Testcase-2'
    )

    [android_1, ios_1, crawler_1] >> compare_1 >> [android_2, ios_2, crawler_2] >> compare_2

if __name__ == "__main__":
    dag.cli()
