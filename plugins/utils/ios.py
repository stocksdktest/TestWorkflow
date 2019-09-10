import subprocess
import os
import threading
import binascii

from . import base

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

    with subprocess.Popen(cmd, cwd=PROJECT_PATH, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
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

    t = threading.Thread(target=read_log, daemon=True)
    t.start()

def parse_sim_log(chunk_cache, log):
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
        return base.base64_decode(data_str)
    except binascii.Error as e:
        print('Decode base64 data error: ' + str(e))
        return None
