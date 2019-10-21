import re
import urllib3

from airflow.exceptions import AirflowException
from airflow.utils.decorators import apply_defaults

from operators.stock_operator import StockOperator

# TODO only this import style can work on airflow
from protos_gen import *
from utils import *

class AndroidRunnerOperator(StockOperator):

	@apply_defaults
	def __init__(self, apk_id, apk_version, runner_conf, target_device=None, *args, **kwargs):
		super(AndroidRunnerOperator, self).__init__(queue='android', runner_conf=runner_conf, *args, **kwargs)
		self.apk_id = apk_id
		self.apk_version = apk_version
		self.apk_path = None
		self.test_apk_path = None
		self.serial = target_device

	def install_apk(self, apk_files):
		"""
		:param apk_files:
		:type apk_files: list(operators.release_ci_operator.ReleaseFile)
		"""
		http = urllib3.PoolManager()
		for file in apk_files:
			r = http.request('GET', file.url, preload_content=False)
			path = '/tmp/' + file.name
			with open(path, 'wb') as out:
				while True:
					data = r.read(65536)
					if not data:
						break
					out.write(data)
			r.release_conn()
			if exec_adb_cmd(['adb', 'install', '-r', '-t', path], serial=self.serial) != 0:
				raise AirflowException('Install apk from %s failed' % file)

	def pre_execute(self, context):
		super(AndroidRunnerOperator, self).pre_execute(context)

		if not self.serial:
			self.serial = scan_local_device()
			if not self.serial:
				raise AirflowException('can not scan device')

		if not connect_to_device(self.serial):
			raise AirflowException('can not connect to device "%s"' % self.serial)

		main_apk_version = get_app_version(self.serial, self.apk_id)
		testing_apk_version = get_app_version(self.serial, '%s.test' % self.apk_id)
		print('Verify App(%s) version: %s, main is %s, testing is %s' % (self.apk_id, self.apk_version,
																		 main_apk_version, testing_apk_version))
		if self.apk_version == main_apk_version and self.apk_version == testing_apk_version:
			return

		release_files = self.xcom_pull(context, key='android_release')
		print('release: %s' % release_files)
		if release_files is None or not isinstance(release_files, list):
			raise AirflowException('Can not get Android release assets: %s')
		self.install_apk(release_files)

	def execute(self, context):
		chunk_cache = LogChunkCache()

		def read_record(record_str):
			record = TestExecutionRecord()
			data = parse_logcat(chunk_cache, record_str)
			if data:
				record.ParseFromString(data)
			if len(record.ListFields()) > 0:
				print("*************************")
				print(record)
				print("*************************")

		spawn_logcat(serial=self.serial, logger=read_record)

		test_status_code = []
		def check_test_result(line):
			if 'INSTRUMENTATION_STATUS_CODE:' in line:
				# find number in string, https://stackoverflow.com/a/29581287/9797889
				codes = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", line)
				# check whether code ONLY contains '0' or '1'
				test_status_code.extend(codes)

		cmd_code = exec_adb_cmd([
			'adb', 'shell', 'am', 'instrument', '-w', '-r',
			'-e', 'debug', 'false',
			'-e', 'filter', 'com.chi.ssetest.TestcaseFilter',
			'-e', 'listener', 'com.chi.ssetest.TestcaseExecutionListener',
			'-e', 'collector_file', 'test.log',
			# android store env in string, can not contain some special char, encode to base64
			'-e', 'runner_config', base64_encode(self.runner_conf.SerializeToString()),
			'com.chi.ssetest.test/android.support.test.runner.AndroidJUnitRunner'
		], serial=self.serial, logger=check_test_result)

		if cmd_code != 0 or len(test_status_code) == 0 or \
				(test_status_code.count('0') + test_status_code.count('1') < len(test_status_code)):
			raise AirflowException('Android Test Failed')
