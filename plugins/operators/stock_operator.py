from airflow.exceptions import AirflowException
from airflow.utils.decorators import apply_defaults
from airflow.models import BaseOperator

from utils import *


class StockOperator(BaseOperator):
    TAG_RECORD = 'TEST_RECORD'
    TAG_EVENT = 'JOB_EVENT'

    @apply_defaults
    def __init__(self, queue, runner_conf, run_times=1, *args, **kwargs):
        super(StockOperator, self).__init__(queue=queue, *args, **kwargs)
        self.runner_conf = runner_conf
        self.run_times = run_times

    def runner_conf_replicate(self, runner_conf, replicate_numbers):
        replicated = runner_conf.__deepcopy__()
        for case_conf in replicated.casesConfig:
            param_collector = case_conf.paramStrs.__deepcopy__()
            for i in range(replicate_numbers):
                case_conf.paramStrs.extend(param_collector)
            case_conf.paramStrs.sort()
        return replicated

    #  这个runner_conf有样例
    def get_runner_conf_cases(self):
        cnt = 0
        for caseConfig in self.runner_conf.casesConfig:
            cnt = cnt + caseConfig.paramStrs.__len__()
        return cnt

    # 这个runner_conf需要返回几条记录
    def get_runner_conf_records(self):
        cnt = 0
        for caseConfig in self.runner_conf.casesConfig:
            cnt = cnt + caseConfig.paramStrs.__len__() + 1
        return cnt

    def pre_execute(self, context):
        self.runner_conf.jobID = context.get('run_id').replace('+',' ')  # dag_run_id
        self.runner_conf.runnerID = generate_id('RUN-')
        # if not self.runner_conf.storeConfig.HasField('collectionName'):
        # 	self.runner_conf.storeConfig.collectionName = self.dag_id
        if not self.runner_conf.IsInitialized():
            raise AirflowException('RunnerConfig not init: %s' % str(self.runner_conf))
