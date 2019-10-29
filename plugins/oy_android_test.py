import json
import re
import pickle
from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig, Site
from protos_gen.record_pb2 import TestExecutionRecord
from utils.base import LogChunkCache, base64_encode, generate_id, command_to_script
from utils.adb import exec_adb_cmd, parse_logcat, spawn_logcat
from gen_testcase import get_case_list

serial_str = '818fd179'

test_out = []   # raw data
test_db = []    # ParseFromString
buffer_out = [] # 4 testfiles


def testAndroidCases(case_conf, market_level, hk_perms, server_sites):
    """
    测试安卓样例
    :param case_conf:       case_conf
    :param market_level:    runner_conf.sdkConfig.marketPerm.Level
    :param hk_perms:        runner_conf.sdkConfig.marketPerm.HKPerms.extend([ @param ])
    :param server_sites:    runner_conf.sdkConfig.serverSites[ @key ].CopyFrom(Site(ips=[ @value ]))
    """
    runner_conf = RunnerConfig()
    runner_conf.jobID = 'TJ-1'
    runner_conf.runnerID = generate_id('RUN-A')
    runner_conf.sdkConfig.appKeyIOS = 'VVW0Fno7BEZt1a/y6KLM36uj9qcjw7CAHDwWZKDlWDs='
    runner_conf.sdkConfig.appKeyAndroid = 'J6IPlk5AEU+2/Yi59rfYnsFQtdtOgAo9GAzysx8ciOM='
    runner_conf.sdkConfig.marketPerm.Level = market_level
    runner_conf.casesConfig.extend(case_conf)

    if hk_perms.__len__() != 0:
        runner_conf.sdkConfig.marketPerm.HKPerms.extend(hk_perms)

    if server_sites.__len__() != 0:
        for k, v in server_sites.items():
            runner_conf.sdkConfig.serverSites[k].CopyFrom(Site(ips=[v]))

    print(base64_encode(runner_conf.SerializeToString()))

    chunk_cache = LogChunkCache()

    def read_record(record_str):
        record = TestExecutionRecord()
        data = parse_logcat(chunk_cache, record_str)
        if data:
            record.ParseFromString(data)
        if len(record.ListFields()) > 0:
            print("*********Record Start****************")
            # print(record)
            test_db.append(record)
            test_out.append(data)
            print("*********Record End****************\n")

    spawn_logcat(serial=serial_str, logger=read_record)

    test_status_code = []

    def check_test_result(line):
        global test_result
        if 'INSTRUMENTATION_STATUS_CODE' in line:
            # find number in string, https://stackoverflow.com/a/29581287/9797889
            codes = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", line)
            # check whether code ONLY contains '0' or '1'
            test_status_code.extend(codes)

    # 生成含有ADB测试命令的shell脚本
    # TODO(Ouyang): 将Shell脚本的存储位置作为参数
    command_to_script(args=[
        'am', 'instrument', '-w', '-r',
        '-e', 'debug', 'false',
        '-e', 'filter', 'com.chi.ssetest.TestcaseFilter',
        '-e', 'listener', 'com.chi.ssetest.TestcaseExecutionListener',
        '-e', 'collector_file', 'test.log',
        '-e', 'runner_config', base64_encode(runner_conf.SerializeToString()),
        'com.chi.ssetest.test/android.support.test.runner.AndroidJUnitRunner'
    ], script_path='/tmp/test.sh')
    # 将测试脚本push进设备并执行（因为binder传输1MB的限制）
    cmd_code_push = exec_adb_cmd(args=['adb', 'push', '/tmp/test.sh', '/data/local/tmp/'], serial=serial_str)
    cmd_code_exec = exec_adb_cmd(args=['adb', 'shell', 'sh', '/data/local/tmp/test.sh'], serial=serial_str,
                                 logger=check_test_result)

    #
    print("status: ", (cmd_code_exec == 0) and \
          len(test_status_code) > 0 and \
          (test_status_code.count('0') + test_status_code.count('1') == len(test_status_code)))


def save_testcase(dataList, save_path):
    # 使用dump()将数据序列化到文件中
    fw = open(save_path, 'wb')
    # Pickle dictionary using protocol 0.
    pickle.dump(dataList, fw)
    fw.close()


def load_testcase(save_path):
    # 使用load()将数据从文件中序列化读出
    fr = open(save_path, 'rb')
    data1 = pickle.load(fr)
    print(data1)
    fr.close()
    return data1


def testAll():
    case_list, m_list, hk_list, ssites_list = get_case_list()
    for i in range(case_list.__len__()):
        print("Test List No.", i)
        testAndroidCases(
            case_conf=case_list[i],
            market_level=m_list[i],
            hk_perms=hk_list[i],
            server_sites=ssites_list[i]
        )

        save_testcase(test_out, "../testcases/testout3/AndroidTestCase" + str(i))

        rec = test_db.copy()
        buffer_out.append(rec)
        test_out.clear()
        test_db.clear()

    # parse_list = []
    # for case in load_data:
    #     rec = TestExecutionRecord()
    #     rec.ParseFromString(case)
    #     parse_list.append(rec)

def testOne():
    case_conf = TestcaseConfig()
    case_conf.testcaseID = 'OHLCTEST_1'
    case_conf.roundIntervalSec = 3
    case_conf.continueWhenFailed = False
    case_conf.paramStrs.extend([
        json.dumps({
            'stk': '00700.hk',
            'type': 'dayk'
        })
    ])
    server_sites = {}
    server_sites['sh'] = ''
    testAndroidCases(
        case_conf= [case_conf],
        market_level="2",
        hk_perms= ["hk10"],
        server_sites = {}
    )

if __name__ == '__main__':
    testOne()
