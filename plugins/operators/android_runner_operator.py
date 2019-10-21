import re

from airflow.exceptions import AirflowException
from airflow.utils.decorators import apply_defaults

from operators.stock_operator import StockOperator

# TODO only this import style can work on airflow
from protos_gen import *
from utils import *

class AndroidStockOperator(StockOperator):

	@apply_defaults
	def __init__(self, apk_id, apk_version, apk_path, test_apk_path, runner_conf, *args, **kwargs):
		super(AndroidStockOperator, self).__init__(queue='android', runner_conf=runner_conf, *args, **kwargs)
		self.apk_id = apk_id
		self.apk_version = apk_version
		self.apk_path = apk_path
		self.test_apk_path = test_apk_path
		self.serial = None

	def pre_execute(self, context):
		super(AndroidStockOperator, self).pre_execute(context)

		def scan_device(line):
			reg_obj = re.search(r'(emulator-\d+)', line)
			if reg_obj:
				self.serial = reg_obj.groups()[0]
		if exec_adb_cmd(['adb', 'devices'], logger=scan_device) != 0:
			raise AirflowException('ADB init failed')
		if not self.serial:
			raise AirflowException('Can not find android devices')

		cur_apk_version = None
		def check_apk_version(line):
			global cur_apk_version
			reg_obj = re.search(r'versionName=(\d{8}_\d{4}_[0-9a-z]{7})', line)
			if reg_obj:
				cur_apk_version = reg_obj.groups()[0]
		exec_adb_cmd([
			'adb', 'shell', 'dumpsys', 'package', self.apk_id
		], serial=self.serial, logger=check_apk_version)
		print('Verify App(%s) version: %s, cur is %s' % (self.apk_id, self.apk_version, cur_apk_version))

		if self.apk_version == cur_apk_version:
			return
		if exec_adb_cmd(['adb', 'install', '-r', '-t', self.apk_path], serial=self.serial) != 0 \
				or exec_adb_cmd(['adb', 'install', '-r', '-t', self.test_apk_path], serial=self.serial) != 0:
			raise AirflowException('Can not install App: %s, test App: %s' % (self.apk_path, self.test_apk_path))

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
