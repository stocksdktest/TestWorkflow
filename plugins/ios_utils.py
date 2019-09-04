import subprocess
import os
import platform

IPHONE_SDK_VERSION='11.2'
PLISTBUDDY_PATH=r'/usr/libexec/PlistBuddy'
XCTOOL_PATH=r'/usr/local/bin/xctool'
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