import subprocess
import os
import platform
import threading
import binascii

from utils import base64_decode

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
	process = subprocess.Popen(args, executable=ADB_EXEC_PATH, stdout=subprocess.PIPE, env=adb_env)
	while True:
		line = process.stdout.readline()
		if not line:
			break
		if logger and callable(logger):
			logger(str(line))
		os.write(1, line)
	process.wait()
	return process.returncode

def spawn_logcat(serial=None, logger=None):
	def read_log():
		adb_env = os.environ.copy()
		if serial:
			adb_env['ANDROID_SERIAL'] = serial

		# ignore return code
		subprocess.call(args=["adb", "logcat", "-c"], executable=ADB_EXEC_PATH, env=adb_env)

		args = [
			"adb", "logcat",
			"-v", "tag",
			"-s", "TestResult.TestExecutionRecord"
		]
		process = subprocess.Popen(args, executable=ADB_EXEC_PATH, stdout=subprocess.PIPE, env=adb_env)
		while True:
			line = process.stdout.readline()
			if not line:
				continue
			if logger and callable(logger):
				logger(str(line, encoding='utf-8'))
		process.wait()

	t = threading.Thread(target=read_log, daemon=True)
	t.start()


def parse_data_from_logcat(chunk_cache, log):
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
		return base64_decode(data_str)
	except binascii.Error as e:
		print('Decode base64 data error: ' + str(e))
		return None


if __name__ == '__main__':
	exec_adb_cmd([
		'adb', 'devices'
	])