import paramiko
import json

from airflow.exceptions import AirflowException
from airflow.utils.decorators import apply_defaults
from operators.stock_operator import StockOperator

# TODO only this import style can work on airflow
from protos_gen import *
from protos_gen.config_pb2 import Site
from utils import *
from utils.ios import xcodebuild_test_cmd

OSX_HOSTNAME = '192.168.100.2'
OSX_PORT = 22
OSX_USER_ID = 'test-env'
OSX_UESR_PWD = 'test-env'
SSH_TIMEOUT = 20
IOS_REPO_PATH = '/Users/test-env/stocksdktest/IOSTestRunner'


class IOSRunnerOperator(StockOperator):
	@apply_defaults
	def __init__(self, app_id, project_path, runner_conf, *args, **kwargs):
		super(IOSRunnerOperator, self).__init__(queue='osx', runner_conf=runner_conf, *args, **kwargs)
		self.ssh_key_path = '/root/.ssh/id_rsa'
		self.app_id = app_id
		self.project_path = project_path
		self.ssh_cmd = 'ssh -p %s %s@%s ' % (OSX_PORT, OSX_USER_ID, OSX_HOSTNAME)
		self.ssh_client = paramiko.SSHClient()

	def pre_execute(self, context):
		super(IOSRunnerOperator, self).pre_execute(context)
		# check login without password
		# ssh_client = paramiko.SSHClient()
		# ssh_client.load_host_keys(self.ssh_key_path)
		try:
			self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			self.ssh_client.connect(hostname=OSX_HOSTNAME, port=OSX_PORT, username=OSX_USER_ID, password=OSX_UESR_PWD,
									timeout=SSH_TIMEOUT)
			stdin, stdout, stderr = self.ssh_client.exec_command('echo "ok"')
		except paramiko.SSHException as e:
			raise AirflowException(str(e))

	def execute(self, context):

		# test SSH connection
		stdin, stdout, stderr = self.ssh_client.exec_command('echo "ok"')
		if len(stderr.read()) != 0:
			print(stderr.read())
			raise AirflowException('Broken SSH connection')

		# TODO Do not edit!
		print(base64_encode(self.runner_conf.SerializeToString()))
		if not config_plist(ssh_cmd=self.ssh_cmd, serialize_config=base64_encode(self.runner_conf.SerializeToString())):
			print("Config Info.Plist error")
			exit(1)

		test_result = False

		def check_test_result(line):
			global test_result
			if 'TEST EXECUTE FAILED' in line:
				test_result = False
			elif 'TEST EXECUTE SUCCEEDED' in line:
				test_result = True

		cmd_code = xcodebuild_test_cmd(ssh_cmd=self.ssh_cmd, logger=check_test_result)
		print("status: ", (cmd_code == 0) and test_result)

		self.xcom_push(context, key=self.task_id, value=self.runner_conf.runnerID)
		self.ssh_client.close()


if __name__ == '__main__':
	runner_conf = RunnerConfig()
	runner_conf.jobID = 'TJ-1'
	runner_conf.runnerID = generate_id('RUN-A')

	runner_conf.sdkConfig.appKeyIOS = 'VVW0Fno7BEZt1a/y6KLM36uj9qcjw7CAHDwWZKDlWDs='
	runner_conf.sdkConfig.appKeyAndroid = 'J6IPlk5AEU+2/Yi59rfYnsFQtdtOgAo9GAzysx8ciOM='

	runner_conf.sdkConfig.marketPerm.Level = "1"
	runner_conf.sdkConfig.marketPerm.HKPerms.extend(["hk10", "hka1"])
	runner_conf.sdkConfig.serverSites["sh"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
	runner_conf.sdkConfig.serverSites["sz"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
	runner_conf.sdkConfig.serverSites["cf"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
	runner_conf.sdkConfig.serverSites["nf"].CopyFrom(Site(ips=["http://114.80.155.134:22013"]))
	runner_conf.sdkConfig.serverSites["pb"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))

	runner_conf.sdkConfig.serverSites["hk10"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))

	# mongoDB位置，存储的数据库位置
	# runner_conf.storeConfig.mongoUri = "mongodb://221.228.66.83:30617"
	# runner_conf.storeConfig.dbName = "stockSdkTest"
	# runner_conf.storeConfig.collectionName = 'ios_test'

	case_conf = TestcaseConfig()
	case_conf.testcaseID = 'AHQuoteListTestCase1'
	case_conf.continueWhenFailed = False
	case_conf.roundIntervalSec = 3
	case_conf.paramStrs.extend([
		json.dumps({
			'PAGE_SIZE': '12',
			'PAGE_INDEX': '0',
			'ASC?': 'no',
			'FIELD': '2'
		})
	])

	runner_conf.casesConfig.extend([case_conf])

	ios_task = IOSRunnerOperator(
		task_id="1",
		app_id="2",
		project_path="",
		runner_conf=runner_conf
	)
	ios_task.pre_execute("")
	ios_task.execute("")
	stdin, stdout, stderr = ios_task.ssh_client.exec_command('echo "ok"')
