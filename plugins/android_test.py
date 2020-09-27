import json
import re

from protos_gen.config_pb2 import RunnerConfig, TestcaseConfig, Site
from protos_gen.record_pb2 import TestExecutionRecord
# from utils.base import LogChunkCache, base64_encode, generate_id, runner_config_to_file, command_to_script

# from utils.adb import exec_adb_cmd, parse_logcat, spawn_logcat
from utils.base import  *
from utils.adb import *

serial = 'emulator-5554'
# serial = '818fd179'

if __name__ == '__main__':
    runner_conf = RunnerConfig()
    runner_conf.jobID = 'TJ-1'
    runner_conf.runnerID = generate_id('RUN-A')

    runner_conf.sdkConfig.appKeyIOS = 'VVW0Fno7BEZt1a/y6KLM36uj9qcjw7CAHDwWZKDlWDs='
    runner_conf.sdkConfig.appKeyAndroid = 'J6IPlk5AEU+2/Yi59rfYnsFQtdtOgAo9GAzysx8ciOM='
    runner_conf.sdkConfig.marketPerm.Level = "2"
    runner_conf.sdkConfig.marketPerm.HKPerms.extend(["hk10"])
    runner_conf.jobID = 'dagID'
    runner_conf.storeConfig.mongoUri = "mongodb://221.228.66.83:30617"
    runner_conf.storeConfig.dbName = "stockSdkTest"
    runner_conf.storeConfig.collectionName = "quote_detail"

    runner_conf.sdkConfig.serverSites["sh"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
    runner_conf.sdkConfig.serverSites["tcpsh"].CopyFrom(Site(ips=["http://114.80.155.134:22017"]))
    runner_conf.sdkConfig.serverSites["shl2"].CopyFrom(Site(ips=["http://114.80.155.62:22016"]))
    runner_conf.sdkConfig.serverSites["tcpshl2"].CopyFrom(Site(ips=["http://114.80.155.62:22017"]))
    runner_conf.sdkConfig.serverSites["sz"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
    runner_conf.sdkConfig.serverSites["szl2"].CopyFrom(Site(ips=["http://114.80.155.47:22016"]))
    runner_conf.sdkConfig.serverSites["tcpsz"].CopyFrom(Site(ips=["http://114.80.155.134:22017"]))
    runner_conf.sdkConfig.serverSites["tcpszl2"].CopyFrom(Site(ips=["http://114.80.155.47:22017"]))
    runner_conf.sdkConfig.serverSites["bj"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
    runner_conf.sdkConfig.serverSites["cf"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
    runner_conf.sdkConfig.serverSites["nf"].CopyFrom(Site(ips=["http://114.80.155.134:22013"]))
    runner_conf.sdkConfig.serverSites["gf"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
    runner_conf.sdkConfig.serverSites["pb"].CopyFrom(Site(ips=["http://114.80.155.134:22016"]))
    runner_conf.sdkConfig.serverSites["hk1"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
    runner_conf.sdkConfig.serverSites["hk5"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
    runner_conf.sdkConfig.serverSites["hk10"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
    runner_conf.sdkConfig.serverSites["tcphk10"].CopyFrom(Site(ips=["http://114.80.155.133:22017"]))
    runner_conf.sdkConfig.serverSites["hka1"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
    runner_conf.sdkConfig.serverSites["hkd1"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
    runner_conf.sdkConfig.serverSites["hkaz"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))
    runner_conf.sdkConfig.serverSites["hkdz"].CopyFrom(Site(ips=["http://114.80.155.133:22016"]))

    # case_conf = TestcaseConfig()
    # case_conf.testcaseID = 'BANKUAISORTING_1'
    # case_conf.continueWhenFailed = True
    # case_conf.roundIntervalSec = 3
    # case_conf.paramStrs.extend([
    #     json.dumps({
    #         'SYMBOL': 'Trade',
    #         'param': '0,10,hsl,1'  # 按照换手率排序
    #     }),
    #     json.dumps({
    #         'SYMBOL': 'Trade',
    #         'param': '0,10,zgj,1'  # 按照最高价排序
    #     }),
    #     json.dumps({
    #         'SYMBOL': 'Notion',
    #         'param': '0,10,zxj,1'  # 按照最新价排序
    #     }),
    #     json.dumps({
    #         'SYMBOL': 'Notion',
    #         'param': '0,10,zdj,1'  # 按照最低价排序
    #     }),
    #     json.dumps({
    #         'SYMBOL': 'Area',
    #         'param': '0,10,hsl,1'  # 按照换手率排序
    #     }),
    #     json.dumps({
    #         'SYMBOL': 'Area',
    #         'param': '0,10,zf,1'  # 按照振幅排序
    #     }),
    #     #---
    #     json.dumps({
    #         'SYMBOL': 'Trade',
    #         'param': '0,10,hsl,0'  # 按照换手率排序
    #     }),
    #     json.dumps({
    #         'SYMBOL': 'Trade',
    #         'param': '0,10,zgj,0'  # 按照最高价排序
    #     }),
    #     json.dumps({
    #         'SYMBOL': 'Notion',
    #         'param': '0,10,zxj,0'  # 按照最新价排序
    #     }),
    #     json.dumps({
    #         'SYMBOL': 'Notion',
    #         'param': '0,10,zdj,0'  # 按照最低价排序
    #     }),
    #     json.dumps({
    #         'SYMBOL': 'Area',
    #         'param': '0,10,hsl,0'  # 按照换手率排序
    #     }),
    #     json.dumps({
    #         'SYMBOL': 'Area',
    #         'param': '0,10,zf,0'  # 按照振幅排序
    #     }),
    # ])
    #
    # case_conf_2 = TestcaseConfig()
    # case_conf_2.testcaseID = 'CATESORTING_2'
    # case_conf_2.continueWhenFailed = True
    # case_conf_2.roundIntervalSec = 3
    # case_conf_2.paramStrs.extend([
    #     json.dumps({
    #         'CateType': 'SH1001',
    #         'param': '0,100,7,0,1',  # 最新价正序排
    #         'STOCKFIELDS': '-1',
    #         'ADDVALUEFIELDS': '-1'
    #     }),
    #     json.dumps({
    #         'CateType': 'SH1001',
    #         'param': '0,100,7,1,1',  # 最新价倒序排
    #         'STOCKFIELDS': '-1',
    #         'ADDVALUEFIELDS': '-1'
    #     }),
    #     json.dumps({
    #         'CateType': 'SH1001',
    #         'param': '0,100,8,0,1',  # 最高价正序排
    #         'STOCKFIELDS': '-1',
    #         'ADDVALUEFIELDS': '-1'
    #     }),
    #     json.dumps({
    #         'CateType': 'SH1001',
    #         'param': '0,100,8,1,1',
    #         'STOCKFIELDS': '-1',
    #         'ADDVALUEFIELDS': '-1'
    #     }),
    #     json.dumps({
    #         'CateType': 'SH1001',
    #         'param': '0,100,9,0,1',  # 最低价正序排
    #         'STOCKFIELDS': '-1',
    #         'ADDVALUEFIELDS': '-1'
    #     }),
    #     json.dumps({
    #         'CateType': 'SH1001',
    #         'param': '0,100,9,1,1',
    #         'STOCKFIELDS': '-1',
    #         'ADDVALUEFIELDS': '-1'
    #     }),
    #     json.dumps({
    #         'CateType': 'SH1001',
    #         'param': '0,100,10,0,1',  # 今开价正序排
    #         'STOCKFIELDS': '-1',
    #         'ADDVALUEFIELDS': '-1'
    #     }),
    #     json.dumps({
    #         'CateType': 'SH1001',
    #         'param': '0,100,10,1,1',
    #         'STOCKFIELDS': '-1',
    #         'ADDVALUEFIELDS': '-1'
    #     }),
    #     json.dumps({
    #         'CateType': 'SH1001',
    #         'param': '0,100,11,0,1',  # 昨收价正序排
    #         'STOCKFIELDS': '-1',
    #         'ADDVALUEFIELDS': '-1'
    #     }),
    #     json.dumps({
    #         'CateType': 'SH1001',
    #         'param': '0,100,11,1,1',
    #         'STOCKFIELDS': '-1',
    #         'ADDVALUEFIELDS': '-1'
    #     }),
    #     json.dumps({
    #         'CateType': 'SH1001',
    #         'param': '0,100,12,0,1',  # 涨跌比率正序排
    #         'STOCKFIELDS': '-1',
    #         'ADDVALUEFIELDS': '-1'
    #     }),
    #     json.dumps({
    #         'CateType': 'SH1001',
    #         'param': '0,100,12,1,1',
    #         'STOCKFIELDS': '-1',
    #         'ADDVALUEFIELDS': '-1'
    #     }),
    #     json.dumps({
    #         'CateType': 'SH1001',
    #         'param': '0,100,13,0,1',  # 总手正序排
    #         'STOCKFIELDS': '-1',
    #         'ADDVALUEFIELDS': '-1'
    #     }),
    #     json.dumps({
    #         'CateType': 'SH1001',
    #         'param': '0,100,13,1,1',
    #         'STOCKFIELDS': '-1',
    #         'ADDVALUEFIELDS': '-1'
    #     }),
    #     json.dumps({
    #         'CateType': 'SH1001',
    #         'param': '0,100,14,0,1',  # 当前成交量正序排
    #         'STOCKFIELDS': '-1',
    #         'ADDVALUEFIELDS': '-1'
    #     }),
    #     json.dumps({
    #         'CateType': 'SH1001',
    #         'param': '0,100,14,1,1',
    #         'STOCKFIELDS': '-1',
    #         'ADDVALUEFIELDS': '-1'
    #     }),
    # ])

    # 行情快照  需要添加执行间隔时间和执行次数（1m,100次）
    case_conf = TestcaseConfig()
    case_conf.testcaseID = 'QUOTEDETAIL_1'
    case_conf.continueWhenFailed = True
    case_conf.roundIntervalSec = 3
    # case_conf.paramStrs.extend([
    #     json.dumps({
    #         'CODE': '600000.sh',
    #     }),
    #     json.dumps({
    #         'CODE': '000001.sz',
    #     }),
    #     json.dumps({
    #         'CODE': '600425.sh',
    #     }),
    # ])
    for i in range(50):
        case_conf.paramStrs.extend([
            json.dumps({
                'CODE': '600000.sh',
            })
        ])
    for i in range(50):
        case_conf.paramStrs.extend([
            json.dumps({
                'CODE': '000001.sz',
            }),
        ])
    for i in range(50):
        case_conf.paramStrs.extend([
            json.dumps({
                'CODE': '600425.sh',
            }),
        ])

    runner_conf.casesConfig.extend([case_conf])

    print(base64_encode(runner_conf.SerializeToString()))
    chunk_cache = LogChunkCache()
    def read_record(record_str):
        # print(record_str)
        record = TestExecutionRecord()
        data = parse_logcat(chunk_cache, record_str)
        if data:
            record.ParseFromString(data)
        if len(record.ListFields()) > 0:
            print("*************************")
            print(record)
            print("*************************")


    spawn_logcat(serial=serial, logger=read_record)

    test_status_code = []
    def check_test_result(line):
        if 'INSTRUMENTATION_STATUS_CODE' in line:
            # find number in string, https://stackoverflow.com/a/29581287/9797889
            codes = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", line)
            # check whether code ONLY contains '0' or '1'
            test_status_code.extend(codes)

    runner_conf_local = '/tmp/runner_config'
    runner_conf_android = '/data/local/tmp/runner_config'

    command_to_script(args=[
        'am', 'instrument', '-w', '-r',
        '-e', 'debug', 'false',
        '-e', 'filter', 'com.chi.ssetest.TestcaseFilter',
        '-e', 'listener', 'com.chi.ssetest.TestcaseExecutionListener',
        '-e', 'collector_file', 'test.log',
        '-e', 'runner_config', runner_conf_android,
        'com.chi.ssetest.test/android.support.test.runner.AndroidJUnitRunner'
    ], script_path='/tmp/test.sh')
    runner_config_to_file(
        encoded_runner_config=base64_encode(runner_conf.SerializeToString()),
        file_path=runner_conf_local
    )
    cmd_code_push = exec_adb_cmd(args=['adb', 'push', '/tmp/test.sh', '/data/local/tmp/'], serial=serial)
    cmd_conf_push = exec_adb_cmd(args=['adb', 'push', '/tmp/runner_config', '/data/local/tmp/'], serial=serial)
    cmd_code_exec = exec_adb_cmd(args=['adb', 'shell', 'sh', '/data/local/tmp/test.sh'], serial=serial,
                                 logger=check_test_result)

    # print("status: ", (cmd_code == 0) and \
	# 		   len(test_status_code) > 0 and \
	# 		   (test_status_code.count('0') + test_status_code.count('1') == len(test_status_code)))

    print("RunnerID is ", runner_conf.runnerID)