import subprocess
import os
import threading
import binascii

from utils import base64_decode

IPHONE_SDK_VERSION='11.2'
PLISTBUDDY_PATH=r'/usr/libexec/PlistBuddy'
XCTOOL_PATH=r'/usr/local/bin/xctool'
XCRUN_PATH=r'/usr/bin/xcrun'
PROJECT_PATH=r'/Users/lxs/Documents/StockTesting/IOSTestRunner'

"""
:param serialize_config: str, BASE64 string
:return bool
"""
def config_plist(serialize_config):
    cmd = '%s -c "Delete :runner_config" ' \
          './Build/Products/Debug-iphonesimulator/IOSTestRunner.app/Info.plist' % PLISTBUDDY_PATH
    # ignore return code
    subprocess.call(cmd, cwd=PROJECT_PATH, shell=True)

    cmd = """
    %s -c 'Add :runner_config string "%s"' ./Build/Products/Debug-iphonesimulator/IOSTestRunner.app/Info.plist
    """ % (PLISTBUDDY_PATH, serialize_config)
    process = subprocess.Popen(cmd, cwd=PROJECT_PATH, shell=True)
    process.wait()
    return process.returncode == 0

def xctest_cmd(reporter='pretty', logger=None):
    cmd = XCTOOL_PATH + ' -workspace IOSTestRunner.xcworkspace -scheme IOSTestRunner ' \
         '-configuration Debug -sdk iphonesimulator%s -reporter %s ' \
         '-destination "platform=iOS Simulator,name=iPhone 8 Plus" run-tests -only IOSTestRunnerTests' % (IPHONE_SDK_VERSION, reporter)

    process = subprocess.Popen(cmd, cwd=PROJECT_PATH, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        line = process.stdout.readline()
        if not line:
            break
        if logger and callable(logger):
            logger(str(line))
        os.write(1, line)
    process.wait()
    return process.returncode

def spawn_xcrun_log(logger=None):
    def read_log():
        cmd = """
        %s simctl spawn booted log stream --style compact --predicate 'subsystem == "com.chi.ssetest" and category == "record"'
        """ % XCRUN_PATH
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        while True:
            line = process.stdout.readline()
            if not line:
                continue
            if logger and callable(logger):
                logger(str(line, encoding='utf-8'))
        process.wait()
        return process.returncode

    t = threading.Thread(target=read_log, daemon=True)
    t.start()

def parse_data_from_log(chunk_cache, log):
    idx = log.find('[com.chi.ssetest:record]')
    if idx == -1:
        return None
    data_str = log[idx + len('[com.chi.ssetest:record]'):]
    data_str = data_str.strip()

    data_str = chunk_cache.parse_chunk_data(data_str)
    if not data_str:
        return None
    print("data_str: " + data_str)
    try:
        return base64_decode(data_str)
    except binascii.Error as e:
        print('Decode base64 data error: ' + str(e))
        return None
