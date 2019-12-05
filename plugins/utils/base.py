import uuid
import base64
import re
import os
import hashlib
import json
from threading import Event, Lock, Thread
from time import monotonic
import requests

def generate_id(prefix):
	return prefix + '-' + str(uuid.uuid4())

def base64_encode(data):
	return bytes.decode(base64.b64encode(data))

def base64_decode(data_str):
	return base64.b64decode(data_str)

def test_base64_str(test_str):
	return re.match(r'^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$', test_str)

def file_md5(file_path):
	hash_md5 = hashlib.md5()
	with open(file_path, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)
	return hash_md5.hexdigest()

def download_file(url, file_path, md5=None, retry=3):
	os.makedirs(os.path.dirname(file_path), exist_ok=True)
	if md5 is not None and os.path.exists(file_path) and file_md5(file_path) == md5:
		print("file(%s) exist, md5(%s) match" % (file_path, md5))
		return

	with open(file_path, "wb") as f:
		while retry > 0:
			try:
				response = requests.get(url, stream=True, timeout=120)
				total_length = response.headers.get('content-length')

				if total_length is None or int(total_length) < 65536:  # no content length header
					f.write(response.content)
				else:
					download_length = 0
					total_length = int(total_length)
					for data in response.iter_content(chunk_size=65536):
						download_length += len(data)
						f.write(data)
						print('Downloading %s ... %.3f' % (url, float(download_length) / total_length))
				return
			except requests.exceptions.Timeout as e:
				retry -= 1
				print("Download retry %d: %s" % (retry, e))
				if retry <= 0:
					raise Exception("Download %s timeout" % url)

def bytes_to_dict(bytes_data):
	bytes = bytes_data
	if bytes.__len__() == 0:
		return
	str1 = str(bytes, encoding="utf-8")
	data = "raw data"
	try:
		data = eval(str1)
		print("---------------data = eval(str1)----------------")
	except NameError as ne:
		try:
			print("---------------data = json.loads(str1)----------------")
			data = json.loads(str1)
		except ValueError as ve:
			print(ve)
	finally:
		print(data)
	return data

def command_to_script(args, script_path):
	os.makedirs(os.path.dirname(script_path), exist_ok=True)
	with open(script_path, 'w') as sh:
		sh.write("#! /bin/bash\n")
		sh.write(" ".join(args))
		sh.close()

class LogChunkCache(object):
	def __init__(self):
		# chunk_id: data_string
		self._cache = dict()

	"""
	:return str
	if chunk has finished, return concat string, else return None
	"""
	def parse_chunk_data(self, raw_str):
		chunk_match = re.search(r'Chunk\.(.+)\.(\d+):', raw_str)
		# log has only one chunk
		if not chunk_match:
			return raw_str
		chunk_data = raw_str[chunk_match.span()[1]:]
		chunk_data = chunk_data.strip()
		chunk_id, idx = chunk_match.groups()
		print('chunk_data: ' + chunk_data)
		if chunk_id in self._cache:
			self._cache[chunk_id] += chunk_data
		else:
			self._cache[chunk_id] = chunk_data

		# chunks not finished
		if int(idx) > 0:
			return None
		return self._cache.pop(chunk_id, None)

class WatchdogTimer(Thread):
	"""Run *callback* in *timeout* seconds unless the timer is restarted."""

	def __init__(self, timeout, callback, *args, timer=monotonic, **kwargs):
		super().__init__(**kwargs)
		self.timeout = timeout
		self.callback = callback
		self.args = args
		self.timer = timer
		self.cancelled = Event()
		self.blocked = Lock()

	def run(self):
		self.restart() # don't start timer until `.start()` is called
		# wait until timeout happens or the timer is canceled
		while not self.cancelled.wait(self.deadline - self.timer()):
			# don't test the timeout while something else holds the lock
			# allow the timer to be restarted while blocked
			with self.blocked:
				if self.deadline <= self.timer() and not self.cancelled.is_set():
					return self.callback(*self.args)  # on timeout

	def restart(self):
		"""Restart the watchdog timer."""
		self.deadline = self.timer() + self.timeout

	def cancel(self):
		self.cancelled.set()