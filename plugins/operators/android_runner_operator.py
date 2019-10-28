import re
import sys

import urllib3
from airflow.contrib.hooks.mongo_hook import MongoHook

from airflow.exceptions import AirflowException
from airflow.utils.decorators import apply_defaults

from operators.stock_operator import StockOperator

# TODO only this import style can work on airflow
from protos_gen import *
from utils import *

class AndroidRunnerOperator(StockOperator):

	@apply_defaults
	def __init__(self, apk_id, apk_version, runner_conf,target_device=None, *args, **kwargs):
		super(AndroidRunnerOperator, self).__init__(queue='android', runner_conf=runner_conf, *args, **kwargs)
		self.apk_id = apk_id
		self.apk_version = apk_version
		self.apk_path = None
		self.test_apk_path = None
		self.serial = target_device
		self.dict_list = []
		self.mongo_hk = MongoHook()
		self.conn = self.mongo_hk.get_conn()


	def install_apk(self, apk_files):
		"""
		:param apk_files:
		:type apk_files: list(operators.release_ci_operator.ReleaseFile)
		"""
		for file in apk_files:
			path = '/tmp/' + file.name
			download_file(file.url, path)
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
		def bytesToDict(bytes):
			if bytes.__len__() == 0:
				return
			str1 = str(bytes, encoding="utf-8")
			data = eval(str1)
			return data

		def TextExecutionRecordtoDict(record):
			if record == None:
				sys.stderr('TextExecutionRecordtoDict Type Error, param is NoneType')
				return
			if (type(record) != TestExecutionRecord):
				sys.stderr('TextExecutionRecordtoDict Type Error, param is not TestExecutionRecord')
				return
			res = {}
			res['jobID'] = record.jobID
			res['runnerID'] = record.runnerID
			res['testcaseID'] = record.testcaseID
			res['recordID'] = record.recordID
			res['isPass'] = record.isPass
			res['startTime'] = record.startTime
			res['paramData'] = bytesToDict(record.paramData)
			res['resultData'] = bytesToDict(record.resultData)
			res['exceptionData'] = bytesToDict(record.exceptionData)
			return res

		chunk_cache = LogChunkCache()

		def read_record(record_str):
			record = TestExecutionRecord()
			data = parse_logcat(chunk_cache, record_str)
			if data:
				record.ParseFromString(data)
			if len(record.ListFields()) > 0:
				print("*************************")
				print(record)
				self.dict_list.append(TextExecutionRecordtoDict(record))
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

		# 生成含有ADB测试命令的shell脚本
		# TODO(Ouyang): 将Shell脚本的存储位置作为参数
		def gen_adbShell(args):
			ADB_SHELL_PATH = '/tmp/test.sh'
			with open(ADB_SHELL_PATH, 'w') as sh:
				sh.write("#! /bin/bash\n")
				sh.write(" ".join(args))
				sh.close()

		gen_adbShell(args=[
			'am', 'instrument', '-w', '-r',
			'-e', 'debug', 'false',
			'-e', 'filter', 'com.chi.ssetest.TestcaseFilter',
			'-e', 'listener', 'com.chi.ssetest.TestcaseExecutionListener',
			'-e', 'collector_file', 'test.log',
			'-e', 'runner_config', base64_encode(self.runner_conf.SerializeToString()),
			'com.chi.ssetest.test/android.support.test.runner.AndroidJUnitRunner'
		])
		cmd_code_push = exec_adb_cmd(args=['adb', 'push', '/tmp/test.sh', '/data/local/tmp/'], serial=self.serial)
		cmd_code_exec = exec_adb_cmd(args=['adb', 'shell', 'sh', '/data/local/tmp/test.sh'], serial=self.serial,
									 logger=check_test_result)

		# if cmd_code != 0 or len(test_status_code) == 0 or \
		# 		(test_status_code.count('0') + test_status_code.count('1') < len(test_status_code)):
		# 	raise AirflowException('Android Test Failed')

		# TODO: HOOK DATABASE CONNECT ERROR
		# self.mongo_hk.insert_many(self.dict_list)

		myclient = self.mongo_hk.client
		mydb = myclient["stockSdkTest"]
		col = mydb[self.task_id]
		print('Debug Airflow: dict_list:---------------')
		print(self.dict_list)
		col.insert_many(self.dict_list)
		self.xcom_push(context,key=self.task_id, value=self.runner_conf.runnerID)
