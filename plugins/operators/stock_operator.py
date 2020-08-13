from airflow.exceptions import AirflowException
from airflow.utils.decorators import apply_defaults
from airflow.models import BaseOperator

from utils import *


class StockOperator(BaseOperator):
    TAG_RECORD = 'TEST_RECORD'
    TAG_EVENT = 'JOB_EVENT'

    @apply_defaults
    def __init__(self, queue, runner_conf, run_times=1, *args, **kwargs):
        """
        SDK测试相关Operator的基类
        @param queue: 测试的job应该进入哪个队列，值有'android', 'osx', 'worker'。将会通过 CeleryExecutor 交给不同的虚拟机执行。
        @param runner_conf: 测试计划的运行参数
        @param run_times: 测试计划中单个用例执行的次数，默认值为1，
        @param args:
        @param kwargs:
        """
        super(StockOperator, self).__init__(queue=queue, *args, **kwargs)
        self.runner_conf = runner_conf
        self.run_times = run_times

    def runner_conf_replicate(self, runner_conf, replicate_numbers):
        """
        复制runner_conf中的用例
        @param runner_conf: 运行参数
        @param replicate_numbers: 复制次数 TODO: 确认replicate_numbers为1的时候到底复制不复制？
        @return: 用例复制后的运行参数
        """
        replicated = runner_conf.__deepcopy__()
        for case_conf in replicated.casesConfig:
            param_collector = case_conf.paramStrs.__deepcopy__()
            for i in range(replicate_numbers):
                case_conf.paramStrs.extend(param_collector)
            case_conf.paramStrs.sort()
        return replicated

    def get_runner_conf_cases(self):
        """
        @return: 该runner_conf需要执行的用例数
        """
        cnt = 0
        for caseConfig in self.runner_conf.casesConfig:
            cnt = cnt + caseConfig.paramStrs.__len__()
        return cnt

    def get_runner_conf_records(self):
        """
        由于对每个用例，多了一条测试结果总结。因此每个用例返回的记录会比执行的用例数多1。
        @return: 该runner_conf需要返回的记录数。
        """
        cnt = 0
        for caseConfig in self.runner_conf.casesConfig:
            cnt = cnt + caseConfig.paramStrs.__len__() + 1
        return cnt

    def pre_execute(self, context):
        """
        用airflow任务上下文的run_id作为该次测试的jobID，并生成runnerID。
        @param context:
        @return:
        """
        self.runner_conf.jobID = context.get('run_id').replace('+',' ')  # dag_run_id，加号在前端MongoDB的查询中检索不到，因此替换为空格
        self.runner_conf.runnerID = generate_id('RUN-')
        if not self.runner_conf.IsInitialized():
            raise AirflowException('RunnerConfig not init: %s' % str(self.runner_conf))
