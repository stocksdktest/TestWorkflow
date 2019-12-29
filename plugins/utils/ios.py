import subprocess
import os
import threading
import binascii

from airflow.contrib.hooks.sftp_hook import SFTPHook

from utils import base
import paramiko

OSX_HOSTNAME = '192.168.100.2'
OSX_PORT = 22
OSX_USER_ID = 'test-env'
OSX_UESR_PWD = 'test-env'
SSH_TIMEOUT = 20

IPHONE_SDK_VERSION = '11.2'
PLISTBUDDY_PATH = r'/usr/libexec/PlistBuddy'
XCTOOL_PATH = r'/usr/local/bin/xctool'
XCODEBUILD_PATH = r'/usr/bin/xcodebuild'
XCRUN_PATH = r'/usr/bin/xcrun'
APP_ID = 'com.chi.ssetest'
PROJECT_PATH = r'/Users/test-env/stocksdktest/IOSTestRunner'

ZIP_APP_PATH = '/Users/test-env/stocksdktest/IOSTestRunner/Build/Products/Debug-iphonesimulator'
APP_APP_PATH = '/Users/test-env/stocksdktest/IOSTestRunner/Build/Products/Debug-iphonesimulator/IOSTestRunner.app'
TAG_APP_PATH = '/Users/test-env/stocksdktest/IOSTestRunner/Build/Products/Debug-iphonesimulator/app_version'
TAG_FILE = 'app_version'


# TODO: use hook
def new_ssh_client():
	ssh_client = paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_client.connect(hostname=OSX_HOSTNAME, port=OSX_PORT, username=OSX_USER_ID, password=OSX_UESR_PWD,
					   timeout=SSH_TIMEOUT)
	return ssh_client

def exec_cmd(exec_command, cmd):
	print("---------execute cmd: \'%s\'-----------" % cmd)
	stdin, stdout, stderr = exec_command(cmd)
	print('stdout', stdout.read().decode())
	print('stderr', stderr.read().decode())
	print('return', stdout.channel.exit_status)

"""
:param serialize_config: str, BASE64 string
:return bool
"""


def config_plist(serialize_config, ssh_cmd=None):
	if ssh_cmd is not None:
		ssh_client = new_ssh_client()

		cmd = '%s -c "Delete :runner_config" ' \
			  '%s/Build/Products/Debug-iphonesimulator/IOSTestRunner.app/Info.plist' % (PLISTBUDDY_PATH, PROJECT_PATH)
		print("con_plist  now_cmd1:", cmd)

		stdin, stdout, stderr = ssh_client.exec_command(cmd)
		print('stdout', stdout.read().decode())
		print('stderr', stderr.read().decode())
		print('return', stdout.channel.exit_status)

		cmd = """
        %s -c 'Add :runner_config string "%s"' %s/Build/Products/Debug-iphonesimulator/IOSTestRunner.app/Info.plist
        """ % (PLISTBUDDY_PATH, serialize_config, PROJECT_PATH)
		print("con_plist  now_cmd2:", cmd)

		stdin, stdout, stderr = ssh_client.exec_command(cmd)
		print('stdout', stdout.read().decode())
		print('stderr', stdout.read().decode())
		print('return', stdout.channel.exit_status)

		rcode = stdout.channel.exit_status

		ssh_client.close()
		return rcode == 0

	else:
		cmd = '%s -c "Delete :runner_config" ' \
			  './Build/Products/Debug-iphonesimulator/IOSTestRunner.app/Info.plist' % PLISTBUDDY_PATH
		if ssh_cmd is not None:
			cmd = ssh_cmd + cmd
		# ignore return code
		subprocess.call(cmd, cwd=PROJECT_PATH, shell=True)

		cmd = """
        %s -c 'Add :runner_config string "%s"' ./Build/Products/Debug-iphonesimulator/IOSTestRunner.app/Info.plist
        """ % (PLISTBUDDY_PATH, serialize_config)
		if ssh_cmd is not None:
			cmd = ssh_cmd + cmd
		process = subprocess.Popen(cmd, cwd=PROJECT_PATH, shell=True)
		process.wait()
		return process.returncode == 0


def xcodebuild_test_cmd(ssh_cmd=None, logger=None):

	cmd = XCODEBUILD_PATH + ' -workspace IOSTestRunner.xcworkspace -scheme IOSTestRunner ' \
							'-configuration Debug -sdk iphonesimulator%s ' \
							'-destination "platform=iOS Simulator,name=iPhone 8 Plus" test-without-building -only-testing:IOSTestRunnerTests' % IPHONE_SDK_VERSION
	Start_Path = PROJECT_PATH

	if ssh_cmd is not None:
		ssh_client = new_ssh_client()

		cmd = "cd %s" % PROJECT_PATH + ";" + "pwd;" + cmd
		print("xcodebuild_test_cmd:", cmd)

		stdin, stdout, stderr = ssh_client.exec_command(command=cmd, get_pty=True)
		print('stdout', stdout.read().decode())
		print('stderr', stderr.read().decode())
		print('return', stdout.channel.exit_status)
		for line in stdout.read().decode().split('\n'):
			if logger and callable(logger):
				logger(str(line))

		recode = stdout.channel.exit_status
		ssh_client.close()
		return recode


	else:
		print("xcodebuild_test_cmd:", cmd)
		with subprocess.Popen(cmd, cwd=Start_Path, shell=True, stdout=subprocess.PIPE,
							  stderr=subprocess.PIPE) as process:
			def timeout_callback():
				print('process has timeout')
				process.kill()

			# kill process in timeout seconds unless the timer is restarted
			watchdog = base.WatchdogTimer(timeout=30, callback=timeout_callback, daemon=True)
			watchdog.start()
			for line in process.stdout:
				# don't invoke the watcthdog callback if do_something() takes too long
				with watchdog.blocked:
					if not line:
						process.kill()
						break
					if logger and callable(logger):
						logger(str(line, encoding='utf-8'))
					os.write(1, line)
					watchdog.restart()
			watchdog.cancel()
		return process.returncode


@DeprecationWarning
def xctest_cmd(reporter='pretty', ssh_cmd=None, logger=None):
	cmd = XCTOOL_PATH + ' -workspace IOSTestRunner.xcworkspace -scheme IOSTestRunner ' \
						'-configuration Debug -sdk iphonesimulator%s -reporter %s ' \
						'-destination "platform=iOS Simulator,name=iPhone 8 Plus" run-tests -only IOSTestRunnerTests' % (
			  IPHONE_SDK_VERSION, reporter)

	if ssh_cmd is not None:
		cmd = ssh_cmd + "'cd {};".format(PROJECT_PATH) + cmd + "'"
		print("use_ssh_in xctest_cmd")

	print("ccccmd2:", cmd)

	with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
						  stderr=subprocess.PIPE) as process:  # cwd=PROJECT_PATH,
		def timeout_callback():
			print('process has timeout')
			process.kill()

		# kill process in timeout seconds unless the timer is restarted
		watchdog = base.WatchdogTimer(timeout=30, callback=timeout_callback, daemon=True)
		watchdog.start()
		for line in process.stdout:
			# don't invoke the watcthdog callback if do_something() takes too long
			with watchdog.blocked:
				if not line:
					process.kill()
					break
				if logger and callable(logger):
					logger(str(line, encoding='utf-8'))
				os.write(1, line)
				watchdog.restart()
		watchdog.cancel()
	return process.returncode


def spawn_xcrun_log(ssh_cmd=None, logger=None):
	def read_log():
		# print("spawn_xcrun_log:ssh_md:",ssh_cmd)
		if ssh_cmd is None:
			cmd = """
                            %s simctl spawn booted log stream --style compact --predicate 'subsystem == "%s" and category == "record"'
                            """ % (XCRUN_PATH, APP_ID)

		else:
			# print("use_ssh_in spawn_xcrun_log")
			# cmd = "{} simctl spawn booted log stream --style compact --predicate \"subsystem == \\\"{}\\\" and category == \\\"record\\\"\"".format(
			#     XCRUN_PATH, APP_ID)
			# cmd = ssh_cmd + "'" + cmd + "'"
			cmd = '{} simctl spawn booted log stream --style compact --predicate \'subsystem == \\\"{}\\\" and category == \\\"record\\\"\''.format(
				XCRUN_PATH, APP_ID)
			cmd = ssh_cmd + ' "' + cmd + '"'
			print("1111spawn_xcrun_log cmd:", cmd)

		print("hhhh")
		process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		while True:
			line = process.stdout.readline()

			if not line:
				continue
			if logger and callable(logger):
				print("line:", line)
				logger(str(line, encoding='utf-8'))

	t = threading.Thread(target=read_log, daemon=True)
	t.start()


def parse_sim_log(chunk_cache, log):
	# print("llllog:",log)
	tag = '[%s:record]' % APP_ID
	idx = log.find(tag)
	if idx == -1:
		# print("from herre")
		return None
	data_str = log[idx + len(tag):]
	data_str = data_str.strip()

	data_str = chunk_cache.parse_chunk_data(data_str)
	if not data_str:
		return None
	print("data_str: " + data_str)
	try:
		return base.base64_decode(data_str)
	except binascii.Error as e:
		print('Decode base64 data error: ' + str(e))
		return None

def get_ios_app_version():
	# connect to remote
	ssh_client = new_ssh_client()
	sftp_client = SFTPHook('sftp_default')
	# check tag
	files = sftp_client.list_directory(path=ZIP_APP_PATH)
	tag = None

	if TAG_FILE in files:
		stdin, stdout, stderr = ssh_client.exec_command('cat %s' % TAG_APP_PATH)
		tag = stdout.read().decode().strip('\n')

	sftp_client.close_conn()
	ssh_client.close()
	return tag

def upload_ios_app_to_remote(app_version, local_path):
	# connect to remote
	ssh_client = new_ssh_client()
	sftp_client = SFTPHook('sftp_default')
	conn = sftp_client.get_conn()

	# remote directory of IOSTestRunner.app.zip
	remote_directory = local_path.replace('IOSTestRunner.app.zip', '')
	if not conn.exists(remote_directory):
		conn.mkdir(remotepath=remote_directory)

	#  zip has been upload
	if conn.exists(local_path):
		print("zip (%s) already exists" % (local_path))
	else:
		sftp_client.store_file(local_full_path=local_path, remote_full_path=local_path)

	#  zip has been unziped
	remote_app_path = local_path.replace('.zip', '')
	if conn.exists(remote_app_path):
		print("app (%s)) already exists" % remote_app_path)
	else:
		# unzip IOSTestRunner.app.zip
		cd_cmd = 'cd ' + remote_directory
		unzip_cmd = 'unzip IOSTestRunner.app.zip'
		exec_cmd(
			exec_command=ssh_client.exec_command,
			cmd=cd_cmd + ';' + unzip_cmd
		)
		exec_cmd(
			exec_command=ssh_client.exec_command,
			cmd=cd_cmd + ';' + unzip_cmd
		)
	rm_cmd = 'rm -r %s' % (APP_APP_PATH)
	exec_cmd(
		exec_command=ssh_client.exec_command,
		cmd=rm_cmd
	)
	mv_cmd = 'cp -R %s %s' % (remote_app_path, ZIP_APP_PATH)
	exec_cmd(
		exec_command=ssh_client.exec_command,
		cmd=mv_cmd
	)
	exec_cmd(
		exec_command=ssh_client.exec_command,
		cmd='echo %s > %s' % (app_version, TAG_APP_PATH)
	)

	print('list_directory: %s' % remote_directory)
	print(sftp_client.list_directory(remote_directory))

	sftp_client.close_conn()
	ssh_client.close()

if __name__ == '__main__':
	ssh_client = new_ssh_client()
	exec_cmd(
		exec_command=ssh_client.exec_command,
		cmd='echo %s > %s' % ('666', TAG_APP_PATH)
	)