import unittest
import os
from datetime import datetime

from airflow import DAG, settings
from airflow.operators.python_operator import PythonOperator
from airflow.models import Connection, TaskInstance

from utils import get_app_version
from protos_gen.config_pb2 import RunnerConfig
from operators.release_ci_operator import ReleaseFile
from operators.android_runner_operator import AndroidRunnerOperator
from operators.android_release_operator import AndroidReleaseOperator

class TestReleaseOperator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        access_token = os.environ['GITHUB_ACCESS_TOKEN']
        conn = Connection(
            conn_id='stocksdktest/AndroidTestRunner',
            extra='{"access_token": "%s"}' % access_token
        )
        session = settings.Session()
        session.add(conn)
        session.commit()

    def test_android_ci_task_push_assets_to_xcom(self):
        with DAG(dag_id='any_dag', start_date=datetime.now()) as dag:
            android_release = AndroidReleaseOperator(
                task_id='android_release',
                provide_context=False,
                repo_name='stocksdktest/AndroidTestRunner',
                tag_id='release-20191028-0.0.1',
                tag_sha='83eab8326e7901d744599bff60defaea135f7bf0',
                runner_conf=RunnerConfig()
            )

            task_instance = TaskInstance(task=android_release, execution_date=datetime.now())
            android_release.execute(task_instance.get_template_context())

            release_files = task_instance.xcom_pull(key='android_release')
            self.assertIsNotNone(release_files)
            print(release_files)

    def test_android_runner_task_install_android_apks(self):
        device_serial = '192.168.31.223:5555'
        app_id = 'com.chi.ssetest'
        release_version = 'release-20191016-0.0.3'

        with DAG(dag_id='any_dag', start_date=datetime.now()) as dag:
            def push_function(**kwargs):
                release_apk = ReleaseFile()
                release_apk.name = 'app-debug.apk'
                release_apk.type = 'application/vnd.android.package-archive'
                release_apk.url = 'https://github.com/stocksdktest/AndroidTestRunner/releases/download/release-20191016-0.0.3/app-debug.apk'
                release_testing = ReleaseFile()
                release_testing.name = 'app-debug-androidTest.apk'
                release_testing.type = 'application/vnd.android.package-archive'
                release_testing.url = 'https://github.com/stocksdktest/AndroidTestRunner/releases/download/release-20191016-0.0.3/app-debug-androidTest.apk'
                kwargs['ti'].xcom_push(key='android_release', value=[release_apk, release_testing])

            release_provider = PythonOperator(
                task_id='push_task',
                python_callable=push_function,
                provide_context=True
            )
            android_runner = AndroidRunnerOperator(
                task_id='android_runner',
                provide_context=True,
                apk_id=app_id,
                apk_version=release_version,
                target_device=device_serial,
                runner_conf=RunnerConfig()
            )
            release_provider >> android_runner

            execution_date = datetime.now()

            provider_instance = TaskInstance(task=release_provider, execution_date=execution_date)
            release_provider.execute(provider_instance.get_template_context())

            runner_instance = TaskInstance(task=android_runner, execution_date=execution_date)
            context = runner_instance.get_template_context()
            context['run_id'] = 'fake-run'
            android_runner.pre_execute(context)

            main_apk_version = get_app_version(device_serial, app_id)
            testing_apk_version = get_app_version(device_serial, '%s.test' % app_id)

            self.assertEqual(release_version, main_apk_version, 'main app version not match')
            self.assertEqual(release_version, testing_apk_version, 'testing app version not match')
