import subprocess
import os
import platform

PROJECT_PATH=r'/Users/lxs/Documents/StockTesting/IOSTestRunner'

"""
:param serialize_config: str, BASE64 string
:return bool
"""
def config_plist(serialize_config):
    cmd = '/usr/libexec/PlistBuddy -c "Delete :runner_config" ' \
          './Build/Products/Release-iphonesimulator/IOSTestRunner.app/Info.plist'
    # ignore return code
    subprocess.call(cmd, cwd=PROJECT_PATH, shell=True)

    cmd = """
    /usr/libexec/PlistBuddy -c 'Add :runner_config string "%s"' ./Build/Products/Release-iphonesimulator/IOSTestRunner.app/Info.plist
    """ % serialize_config
    process = subprocess.Popen(cmd, cwd=PROJECT_PATH, shell=True)
    process.wait()
    return process.returncode == 0

def xctest_cmd(reporter='pretty', logger=None):
    cmd ='/usr/local/bin/xctool -workspace IOSTestRunner.xcworkspace -scheme IOSTestRunner ' \
         '-configuration Release -sdk iphonesimulator11.2 -reporter %s ' \
         '-destination "platform=iOS Simulator,name=iPhone 8 Plus" run-tests -only IOSTestRunnerTests' % reporter

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