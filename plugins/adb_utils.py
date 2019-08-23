import subprocess
import os
import platform

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


if __name__ == '__main__':
	exec_adb_cmd([
		'adb', 'devices'
	])