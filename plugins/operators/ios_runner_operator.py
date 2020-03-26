import paramiko
import json

from airflow.exceptions import AirflowException
from airflow.utils.decorators import apply_defaults
from operators.stock_operator import StockOperator
from utils.mongo_hook import MongoHookWithDB

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


# def get_debug_release_files():
# 	from operators.release_ci_operator import ReleaseFile
# 	release_files = list()
# 	release1 = ReleaseFile(
# 		name='IOSTestRunner.app.zip',
# 		type='application/vnd.android.package-archive',
# 		filepath='/release/iOS/release-20191227-0.0.1/IOSTestRunner.app.zip',
# 	)
# 	release1.md5sum = '630076f0287bc5b17d36e59c5fb418d4'
# 	release_files.append(release1)
# 	return release_files

class IOSRunnerOperator(StockOperator):
	@apply_defaults
	def __init__(self, app_version, runner_conf, project_path=None, run_times=1, release_xcom_key = "ios_release",*args, **kwargs):
		super(IOSRunnerOperator, self).__init__(queue='osx', runner_conf=runner_conf, run_times=run_times, *args,
												**kwargs)
		self.ssh_key_path = '/root/.ssh/id_rsa'
		self.app_version = app_version
		self.project_path = project_path
		self.release_xcom_key = release_xcom_key
		self.ssh_cmd = 'ssh -p %s %s@%s ' % (OSX_PORT, OSX_USER_ID, OSX_HOSTNAME)
		self.ssh_client = paramiko.SSHClient()
		self.mongo_hk = MongoHookWithDB(conn_id='stocksdktest_mongo')
		self.conn = self.mongo_hk.get_conn()


	def install_app(self, app_files):
		"""
		:param app_files:
		:type: app_files: list(operators.release_ci_operator.ReleaseFile)
		"""
		if len(app_files) != 1:
			raise AirflowException("IOSTestRunner.app.zip should be only one")

		local_path = self.download_app_from_ftp(app_file= app_files[0])
		upload_ios_app_to_remote(app_version=self.app_version, local_path = local_path)


	def download_app_from_ftp(self, app_file):
		"""
		:param app_file:
		:type app_file: operators.release_ci_operator.ReleaseFile
		:return: path:
		"""
		file = app_file
		path = '/tmp/%s/%s' % (file.md5sum, file.name)
		download_file(url=file.filepath, file_path=path, md5=file.md5sum)

		return path

	def pre_execute(self, context):
		super(IOSRunnerOperator, self).pre_execute(context)
		self.runner_conf = self.runner_conf_replicate(runner_conf=self.runner_conf,
													  replicate_numbers=self.run_times - 1)

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

		# 先看看IOSTestRunner.app的版本是否与需求的一致 app_version
		app_version = get_ios_app_version()
		print('Verify IOSTestRunner.app version: %s, cur is %s' % (self.app_version, app_version))
		if self.app_version == app_version:
			return
		else:
			release_files = self.xcom_pull(context, key=self.release_xcom_key)
			# release_files = get_debug_release_files()

			print('release: %s' % release_files)
			if release_files is None or not isinstance(release_files, list):
				raise AirflowException('Can not get Android release assets: %s')
			self.install_app(release_files)

	def read_data(self):
		print("-----------iOS Result-----------")
		myclient = self.mongo_hk.client
		print('1',self.runner_conf)
		print('2',self.runner_conf.storeConfig)
		print('3',self.runner_conf.storeConfig.dbName)
		mydb = myclient[self.runner_conf.storeConfig.dbName]
		col = mydb[self.runner_conf.storeConfig.collectionName]
		id = self.runner_conf.runnerID
		rule = {
			'runnerID': id,
		}
		for x in col.find(rule):
			print(x)

	def execute(self, context):

		# test SSH connection
		# stdin, stdout, stderr = self.ssh_client.exec_command('echo "ok"')
		# if len(stderr.read()) != 0:
		# 	print(stderr.read())
		# 	raise AirflowException('Broken SSH connection')

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

		# self.read_data()
		self.xcom_push(context, key=self.task_id, value=self.runner_conf.runnerID)
		self.ssh_client.close()


# if __name__ == '__main__':
# 	from dags.test_ios_android import gen2iOSCaseList
#
# 	runner_conf_list = gen2iOSCaseList()
#
# 	ios_task = IOSRunnerOperator(
# 		task_id="1",
# 		provide_context=False,
# 		app_version="release-20191227-0.0.1",
# 		runner_conf=runner_conf_list[0]
# 	)
#
# 	context = dict()
# 	context['run_id'] = 'ios_release'
#
# 	ios_task.pre_execute(context)
# 	ios_task.execute(context)
# 	stdin, stdout, stderr = ios_task.ssh_client.exec_command('echo "ok"')
