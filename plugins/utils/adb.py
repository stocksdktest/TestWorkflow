import subprocess
import os
import platform
import threading
import binascii

from . import base

ADB_EXEC_PATH = '/usr/local/bin/adb' if platform.system() == 'Darwin' else '/usr/bin/adb'

"""
:param args: [str]
:param serial: str
:param logger: lambda: (str) -> {}
"""
def exec_adb_cmd(args, serial=None, logger=None):
	adb_env = os.environ.copy()
	if serial:
		adb_env['ANDROID_SERIAL'] = serial
	# TODO replace ADB_EXEC_PATH
	with subprocess.Popen(args, executable=ADB_EXEC_PATH, stdout=subprocess.PIPE, env=adb_env) as process:
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
					logger(str(line))
				os.write(1, line)
				watchdog.restart()
		watchdog.cancel()
	return process.returncode

def spawn_logcat(serial=None, logger=None):
	def read_log():
		adb_env = os.environ.copy()
		if serial:
			adb_env['ANDROID_SERIAL'] = serial

		# ignore return code
		subprocess.call(args=["adb", "logcat", "-c"], executable=ADB_EXEC_PATH, env=adb_env)

		process = subprocess.Popen([
			"adb", "logcat",
			"-v", "tag",
			"-s", "TestResult.TestExecutionRecord"
		], executable=ADB_EXEC_PATH, stdout=subprocess.PIPE, env=adb_env)
		while True:
			line = process.stdout.readline()
			if not line:
				continue
			if logger and callable(logger):
				logger(str(line, encoding='utf-8'))

	t = threading.Thread(target=read_log, daemon=True)
	t.start()


def parse_logcat(chunk_cache, log):
	idx = log.find('TestResult.TestExecutionRecord')
	if idx == -1:
		return None

	data_str = log[idx + len('TestResult.TestExecutionRecord') + 1:]
	data_str = data_str.strip()

	data_str = chunk_cache.parse_chunk_data(data_str)
	if not data_str:
		return None

	print('data_str: ' + data_str)
	try:
		return base.base64_decode(data_str)
	except binascii.Error as e:
		print('Decode base64 data error: ' + str(e))
		return None


if __name__ == '__main__':
	exec_adb_cmd([
		'adb', 'devices'
	])