import re
import json
import sys
import datetime

from utils.mongo_hook import MongoHookWithDB

from airflow.exceptions import AirflowException
from airflow.utils.decorators import apply_defaults

from operators.stock_operator import StockOperator

# TODO only this import style can work on airflow
from protos_gen import *
from utils import *


# def get_debug_release_files():
# 	from operators.release_ci_operator import ReleaseFile
# 	release_files = list()
# 	release1 = ReleaseFile(
# 		name='app-debug-androidTest.apk',
# 		type='application/vnd.android.package-archive',
# 		filepath='/release/Android/release-20191229-0.0.1/app-debug-androidTest.apk',
# 	)
# 	release1.md5sum = 'f95a2395013d2c51bbc4a88dae896012'
#
# 	release2 = ReleaseFile(
# 		name='app-debug.apk',
# 		type='application/vnd.android.package-archive',
# 		filepath='/release/Android/release-20191229-0.0.1/app-debug.apk',
# 	)
# 	release2.md5sum = 'f2b55540e3ecba9abe5ef20a39d7e313'
#
# 	release_files.append(release1)
# 	release_files.append(release2)
# 	return release_files

class AndroidRunnerOperator(StockOperator):

    @apply_defaults
    def __init__(self, apk_id, apk_version, runner_conf, run_times=1, target_device=None,
                 release_xcom_key="android_release", config_file=False, tcp_times=-1, *args, **kwargs):
        """
		@param apk_id: apk_id，基本是`com.chi.ssetest`
		@param apk_version: 对应ReleaseOperator中的tag_id，例如`release-20200103-0.0.3`
		@param runner_conf: 测试计划的运行参数
		@param run_times: 测试计划中单个用例执行的次数，默认值为1
		@param target_device: [DEBUG] 指定运行该测试计划的设备，默认为None，系统会自动分配。调试时可以指定。
		@param release_xcom_key: TestRunner在Xcom中绑定的键，RunnerOperator与之对应，从该键获得TestRunner的信息
		@param config_file: 是否将运行参数通过脚本形式push入adb并执行。为保证兼容，默认为False。但是后续使用应该用True
		@param tcp_times: TCP相关的测试计划等待的时间 TODO: 待讨论
		@param args:
		@param kwargs:
		"""
        super(AndroidRunnerOperator, self).__init__(queue='android', runner_conf=runner_conf, run_times=run_times,
                                                    *args, **kwargs)
        self.apk_id = apk_id
        self.apk_version = apk_version
        self.apk_path = None
        self.test_apk_path = None
        self.serial = target_device
        self.release_xcom_key = release_xcom_key
        self.config_file = config_file
        self.tcp_times = tcp_times
        self.mongo_hk = MongoHookWithDB(conn_id='stocksdktest_mongo')
        self.conn = self.mongo_hk.get_conn()

    def install_apk(self, apk_files):
        """
		:param apk_files:
		:type apk_files: list(operators.release_ci_operator.ReleaseFile)
		"""
        for file in apk_files:
            path = '/tmp/%s/%s' % (file.md5sum, file.name)
            download_file(url=file.filepath, file_path=path, md5=file.md5sum)
            if exec_adb_cmd(['adb', 'install', '-r', '-t', path], serial=self.serial) != 0:
                raise AirflowException('Install apk from %s failed' % file)

    def pre_execute(self, context):
        super(AndroidRunnerOperator, self).pre_execute(context)
        self.runner_conf = self.runner_conf_replicate(runner_conf=self.runner_conf,
                                                      replicate_numbers=self.run_times - 1)

        # TODO: if one apk is installed successfully another failed, many throw exception about version unmatched
        # it seems 2 apks have been installed and com.chi.ssetest too
        if not start_adb_server():
            raise AirflowException('ADB Server can not start')

        if not self.serial:
            self.serial = scan_local_device()
            if not self.serial:
                raise AirflowException('can not scan device')

        # TODO: 测试的时候注释，到时候记得注释回来
        if not connect_to_device(self.serial):
            print("serial", self.serial)
            raise AirflowException('can not connect to device "%s"' % self.serial)

        main_apk_version = get_app_version(self.serial, self.apk_id)
        print('Verify App(%s) version: %s, cur is %s' % (self.apk_id, self.apk_version, main_apk_version))
        if self.apk_version == main_apk_version:
            return
        else:
            if main_apk_version is not None:
                # uninstall previous apk
                if exec_adb_cmd(['adb', 'uninstall', self.apk_id], serial=self.serial) != 0 or \
                        exec_adb_cmd(['adb', 'uninstall', '%s.test' % self.apk_id], serial=self.serial) != 0:
                    raise AirflowException('Uninstall previous apk error')

            release_files = self.xcom_pull(context, key=self.release_xcom_key)
            # release_files = get_debug_release_files()

            print('release: %s' % release_files)
            if release_files is None or not isinstance(release_files, list):
                raise AirflowException('Can not get Android release assets: %s')
            self.install_apk(release_files)

    def read_data(self):
        print("-----------Android Result-----------")
        myclient = self.mongo_hk.client
        mydb = myclient[self.runner_conf.storeConfig.dbName]
        col = mydb[self.runner_conf.storeConfig.collectionName]
        id = self.runner_conf.runnerID
        rule = {
            'runnerID': id,
        }
        for x in col.find(rule):
            print(x)

    def get_tcp_total_times(self):
        tcp_total_times = 0
        try:
            for casesConfig in self.runner_conf.casesConfig:
                for paramStrs in casesConfig.paramStrs:
                    params = json.loads(paramStrs)
                    tcp_total_times = tcp_total_times + int(params['SECONDS']) + 10
        except:
            raise AirflowException('Can not get TCP time from the runner_conf,'
                                   'Please check the parameters.')
        finally:
            return tcp_total_times

    def execute(self, context):

        test_status_code = []
        # TODO: adb进程等待多少时间就返回（tcp的需要特殊处理）
        timeout = self.get_runner_conf_cases() * 3
        if timeout < 300:
            timeout = 300
        if self.tcp_times != -1:
            timeout = max(timeout, self.get_tcp_total_times())

        print("Process Timeout is set in {} seconds".format(timeout))
        print("RunnerID is {}".format(self.runner_conf.runnerID))

        def check_test_result(line):
            if 'INSTRUMENTATION_STATUS_CODE:' in line:
                # find number in string, https://stackoverflow.com/a/29581287/9797889
                codes = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", line)
                # check whether code ONLY contains '0' or '1'
                test_status_code.extend(codes)

        if self.config_file == False:
            command_to_script(args=[
                'am', 'instrument', '-w', '-r',
                '-e', 'debug', 'false',
                '-e', 'filter', 'com.chi.ssetest.TestcaseFilter',
                '-e', 'listener', 'com.chi.ssetest.TestcaseExecutionListener',
                '-e', 'collector_file', 'test.log',
                '-e', 'runner_config', base64_encode(self.runner_conf.SerializeToString()),
                'com.chi.ssetest.test/android.support.test.runner.AndroidJUnitRunner'
            ], script_path='/tmp/test.sh')
            cmd_code_push = exec_adb_cmd(args=['adb', 'push', '/tmp/test.sh', '/data/local/tmp/'], serial=self.serial)
            cmd_code_exec = exec_adb_cmd(args=['adb', 'shell', 'sh', '/data/local/tmp/test.sh'], serial=self.serial,
                                         logger=check_test_result,
                                         timeout=timeout)

            if cmd_code_push != 0 and cmd_code_exec != 0:
                raise AirflowException('Android ADB Failed')
        else:
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
                encoded_runner_config=base64_encode(self.runner_conf.SerializeToString()),
                file_path=runner_conf_local
            )
            cmd_code_push = exec_adb_cmd(args=['adb', 'push', '/tmp/test.sh', '/data/local/tmp/'], serial=self.serial)
            cmd_conf_push = exec_adb_cmd(args=['adb', 'push', '/tmp/runner_config', '/data/local/tmp/'],
                                         serial=self.serial)
            cmd_code_exec = exec_adb_cmd(args=['adb', 'shell', 'sh', '/data/local/tmp/test.sh'], serial=self.serial,
                                         logger=check_test_result,
                                         timeout=timeout)

            if cmd_code_push != 0 and cmd_code_exec != 0 and cmd_conf_push != 0:
                raise AirflowException('Android ADB Failed')

        # TODO: 一次测试就报错的话，其他测试成功的结果就没用了
        # if cmd_code_push != 0 or cmd_code_exec != 0 or len(test_status_code) == 0 or \
        # 		(test_status_code.count('0') + test_status_code.count('1') < len(test_status_code)):
        # 	raise AirflowException('Android Test Failed')

        # self.read_data()
        self.xcom_push(context, key=self.task_id, value=self.runner_conf.runnerID)

# if __name__ == '__main__':
#
# 	from dags.test_adb import initRunnerConfig
#
# 	runner_conf_list = initRunnerConfig()
# 	task_id_to_cmp_list = ['adb_shell_cmp_a', 'adb_shell_cmp_b']
# 	device = '818fd179'
#
# 	android_a = AndroidRunnerOperator(
# 		task_id=task_id_to_cmp_list[0],
# 		provide_context=False,
# 		apk_id='com.chi.ssetest',
# 		apk_version='release-20191229-0.0.1',
# 		runner_conf=runner_conf_list[0],
# 		target_device=device
# 		# run_times = 10
# 	)
# 	context = dict()
# 	context['run_id'] = '1'
#
# 	android_a.pre_execute(context)
# 	android_a.execute(context)
