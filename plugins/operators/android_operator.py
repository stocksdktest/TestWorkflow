import re

from airflow.exceptions import AirflowException
from airflow.utils.decorators import apply_defaults

from operators.stock_operator import StockOperator
from utils import base64_encode
from adb_utils import exec_adb_cmd

class AndroidStockOperator(StockOperator):

	@apply_defaults
	def __init__(self, runner_conf, *args, **kwargs):
		super(AndroidStockOperator, self).__init__(queue='android', runner_conf=runner_conf, *args, **kwargs)

	def execute(self, context):
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
		], serial='192.168.2.177:20001', logger=check_test_result)
		# ], serial='192.168.1.112:20001', logger=check_test_result)

		if cmd_code != 0 or len(test_status_code) == 0 or \
				(test_status_code.count('0') + test_status_code.count('1') < len(test_status_code)):
			raise AirflowException("Android Test Failed")
