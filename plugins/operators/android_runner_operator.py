import re
import sys
import datetime

from airflow.contrib.hooks.mongo_hook import MongoHook

from airflow.exceptions import AirflowException
from airflow.utils.decorators import apply_defaults

from operators.stock_operator import StockOperator

# TODO only this import style can work on airflow
from protos_gen import *
from utils import *

class AndroidRunnerOperator(StockOperator):

	@apply_defaults
	def __init__(self, apk_id, apk_version, runner_conf, target_device=None, release_xcom_key = "android_release",*args, **kwargs):
		super(AndroidRunnerOperator, self).__init__(queue='android', runner_conf=runner_conf, *args, **kwargs)
		self.apk_id = apk_id
		self.apk_version = apk_version
		self.apk_path = None
		self.test_apk_path = None
		self.serial = target_device
		self.release_xcom_key = release_xcom_key
		self.mongo_hk = MongoHook(conn_id='stocksdktest_mongo')
		self.conn = self.mongo_hk.get_conn()

	def install_apk(self, apk_files):
		"""
		:param apk_files:
		:type apk_files: list(operators.release_ci_operator.ReleaseFile)
		"""
		for file in apk_files:
			path = '/tmp/%s/%s' % (file.md5sum,file.name) 
			download_file(url=file.url, file_path=path, md5=file.md5sum)
			if exec_adb_cmd(['adb', 'install', '-r', '-t', path], serial=self.serial) != 0:
				raise AirflowException('Install apk from %s failed' % file)

	def pre_execute(self, context):
		super(AndroidRunnerOperator, self).pre_execute(context)

		# TODO: TO Debug, so annotate it and return
		# it seems 2 apks have been installed and com.chi.ssetest too
		if not start_adb_server():
			raise AirflowException('ADB Server can not start')

		if not self.serial:
			self.serial = scan_local_device()
			if not self.serial:
				raise AirflowException('can not scan device')

		if not connect_to_device(self.serial):
			print("serial",self.serial)
			raise AirflowException('can not connect to device "%s"' % self.serial)

		main_apk_version = get_app_version(self.serial, self.apk_id)
		print('Verify App(%s) version: %s, cur is %s' % (self.apk_id, self.apk_version, main_apk_version))
		if self.apk_version == main_apk_version:
			return
		else:
			if main_apk_version is not None:
				# uninstall previous apk
				if exec_adb_cmd(['adb', 'uninstall', self.apk_id], serial=self.serial) != 0 or\
					exec_adb_cmd(['adb', 'uninstall', '%s.test' % self.apk_id], serial=self.serial) != 0:
					raise AirflowException('Uninstall previous apk error')

			release_files = self.xcom_pull(context, key=self.release_xcom_key)
			print('release: %s' % release_files)
			if release_files is None or not isinstance(release_files, list):
				raise AirflowException('Can not get Android release assets: %s')
			self.install_apk(release_files)

	@staticmethod
	def protobuf_record_to_dict(record):
		if record is None:
			sys.stderr('TextExecutionRecordtoDict Type Error, param is NoneType')
			return
		if type(record) != TestExecutionRecord:
			sys.stderr('TextExecutionRecordtoDict Type Error, param is not TestExecutionRecord')
			return
		res = dict()
		res['jobID'] = record.jobID
		res['runnerID'] = record.runnerID
		res['testcaseID'] = record.testcaseID
		res['recordID'] = record.recordID
		res['isPass'] = record.isPass
		res['startTime'] = record.startTime
		res['paramData'] = bytes_to_dict(record.paramData)
		res['resultData'] = bytes_to_dict(record.resultData)
		res['exceptionData'] = bytes_to_dict(record.exceptionData)
		return res

	def pre_process_dot(self,record_dict_list):
		for i in range(record_dict_list.__len__()):
			resultData = record_dict_list[i]['resultData']
			if resultData != None:
				old_keys = []
				for k in resultData.keys():
					old_keys.append(k)
				for old_key in old_keys:
					new_key = old_key.replace('.', '_')
					new_key = new_key.replace('$', '_')
					print('old_key', old_key)
					print('new_key', new_key)
					resultData[new_key] = resultData.pop(old_key)
		return record_dict_list

	def execute(self, context):
		record_dict_list = list()
		chunk_cache = LogChunkCache()
		def read_record(record_str):
			record = TestExecutionRecord()
			data = parse_logcat(chunk_cache, record_str)
			if data:
				record.ParseFromString(data)
			if len(record.ListFields()) > 0:
				print("*************************")
				print(record)
				record_dict_list.append(AndroidRunnerOperator.protobuf_record_to_dict(record))
				print("*************************")

		spawn_logcat(serial=self.serial, logger=read_record)

		test_status_code = []
		def check_test_result(line):
			if 'INSTRUMENTATION_STATUS_CODE:' in line:
				# find number in string, https://stackoverflow.com/a/29581287/9797889
				codes = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", line)
				# check whether code ONLY contains '0' or '1'
				test_status_code.extend(codes)

		command_to_script(args=[
			'am', 'instrument', '-w', '-r',
			'-e', 'debug', 'false',
			'-e', 'filter', 'com.chi.ssetest.TestcaseFilter',
			'-e', 'listener', 'com.chi.ssetest.TestcaseExecutionListener',
			'-e', 'collector_file', 'test.log',
			'-e', 'runner_config', base64_encode(self.runner_conf.SerializeToString()),
			'com.chi.ssetest.test/android.support.test.runner.AndroidJUnitRunner'
		], script_path='/tmp/test.sh')
		cmd_code_push = exec_adb_cmd(args=['adb', 'push', '/tmp/test.sh', '/data/local/tmp/'], serial=self.serial)
		cmd_logcat_clear = exec_adb_cmd(args=['adb', 'logcat', '-c'], serial=self.serial)
		cmd_code_exec = exec_adb_cmd(args=['adb', 'shell', 'sh', '/data/local/tmp/test.sh'], serial=self.serial,
									 logger=check_test_result)
		# cmd_logcat = exec_adb_cmd(args=['adb','logcat','-c'], serial=self.serial)

		if cmd_code_push != 0 or cmd_code_exec != 0 or len(test_status_code) == 0 or \
				(test_status_code.count('0') + test_status_code.count('1') < len(test_status_code)):
			raise AirflowException('Android Test Failed')

		client = self.mongo_hk.client
		db = client["stockSdkTest"]
		col = db[self.task_id + datetime.date.today().__str__()]
		print('Debug Airflow: dict_list:---------------')
		record_dict_list =  self.pre_process_dot(record_dict_list)
		print(record_dict_list)
		try:
			col.insert_many(record_dict_list)
		except TypeError as s:
			print(s)
			self.xcom_push(context, key=self.task_id, value=s)
		finally:
			self.xcom_push(context, key=self.task_id, value=self.runner_conf.runnerID)
			self.xcom_push(context, key=self.runner_conf.runnerID,  value=record_dict_list)
