import json
import re
import threading

from utils import generate_id, base64_encode
from adb_utils import exec_adb_cmd
from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig, SDKPermissions

if __name__ == '__main__':
    runner_conf = RunnerConfig()
    runner_conf.jobID = 'TJ-1'
    runner_conf.runnerID = generate_id('RUN-A')

    runner_conf.sdkConfig.appKey = 'J6IPlk5AEU+2/Yi59rfYnsFQtdtOgAo9GAzysx8ciOM='
    runner_conf.sdkConfig.sdkLevel = SDKPermissions.LEVEL_2
    runner_conf.sdkConfig.sdkSseLevel = SDKPermissions.LEVEL_2
    runner_conf.sdkConfig.hkPerms.extend([SDKPermissions.HK10])

    case_conf = TestcaseConfig()
    case_conf.testcaseID = 'TESTCASE_0'
    case_conf.executionTimes = 1
    case_conf.continueWhenFailed = False
    case_conf.paramStr = json.dumps({
        'QUOTE_NUMBERS': '600000.sh'
        # 'QUOTE_NUMBERS': '600028.sh'
    })

    runner_conf.casesConfig.extend([case_conf])

    test_status_code = []
    def check_test_result(line):
        global test_result
        if 'INSTRUMENTATION_STATUS_CODE' in line:
            # find number in string, https://stackoverflow.com/a/29581287/9797889
            codes = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", line)
            # check whether code ONLY contains '0' or '1'
            test_status_code.extend(codes)

    cmd_code = exec_adb_cmd([
        'adb', 'shell', 'am', 'instrument', '-w', '-r',
        '-e', 'debug', 'false',
        '-e', 'filter', 'com.chi.ssetest.TestcaseFilter',
        '-e', 'listener', 'com.chi.ssetest.TestcaseExecutionListener',
        '-e', 'collector_file', 'test.log',
        '-e', 'runner_config', base64_encode(runner_conf.SerializeToString()),
        'com.chi.ssetest.test/android.support.test.runner.AndroidJUnitRunner'
    ], serial='ZX1G22DBHC', logger=check_test_result)

    print("status: ", (cmd_code == 0) and \
			   len(test_status_code) > 0 and \
			   (test_status_code.count('0') + test_status_code.count('1') == len(test_status_code)))