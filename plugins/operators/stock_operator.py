from airflow.exceptions import AirflowException
from airflow.utils.decorators import apply_defaults
from airflow.models import BaseOperator

from utils import *

class StockOperator(BaseOperator):
	TAG_RECORD = 'TEST_RECORD'
	TAG_EVENT = 'JOB_EVENT'

	@apply_defaults
	def __init__(self, queue, runner_conf, *args, **kwargs):
		super(StockOperator, self).__init__(queue=queue, *args, **kwargs)
		self.runner_conf = runner_conf

	def pre_execute(self, context):
		self.runner_conf.jobID = context.get('run_id') # dag_run_id
		self.runner_conf.runnerID = generate_id('RUN-')
		# if not self.runner_conf.storeConfig.HasField('collectionName'):
		# 	self.runner_conf.storeConfig.collectionName = self.dag_id
		if not self.runner_conf.IsInitialized():
			raise AirflowException('RunnerConfig not init: %s' % str(self.runner_conf))
