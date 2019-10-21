import re
import os
import paramiko

from airflow.exceptions import AirflowException
from airflow.utils.decorators import apply_defaults

from operators.stock_operator import StockOperator

# TODO only this import style can work on airflow
from protos_gen import *
from utils import *

OSX_HOSTNAME='192.168.100.2'
OSX_USER_ID='test-env'
SSH_TIMEOUT=20
IOS_REPO_PATH='/Users/test-env/stocksdktest/IOSTestRunner'

class IOSStockOperator(StockOperator):
    @apply_defaults
    def __init__(self, app_id, project_path, runner_conf, *args, **kwargs):
        super(IOSStockOperator, self).__init__(queue='osx', runner_conf=runner_conf, *args, **kwargs)
        self.ssh_key_path = '/root/.ssh/id_rsa'
        self.app_id = app_id
        self.project_path = project_path
        self.ssh_cmd = 'ssh %s@%s ' % (OSX_USER_ID, OSX_HOSTNAME)

    def pre_execute(self, context):
        # check login without password
        ssh_client = paramiko.SSHClient()
        ssh_client.load_host_keys(self.ssh_key_path)
        try:
            ssh_client.connect(hostname=OSX_HOSTNAME, port=22, username=OSX_USER_ID, timeout=SSH_TIMEOUT)
            ssh_client.exec_command('echo "ok"')
        except paramiko.SSHException as e:
            raise AirflowException(str(e))

        ssh_client.exec_command('mkdir -p %s' % IOS_REPO_PATH)
        ssh_client.exec_command('git clone --depth=1 %s %s')

    def execute(self, context):
        _, _, stderr = self.ssh.exec_command('echo "ok"')
        if stderr is not None:
            raise AirflowException('Broken SSH connection')

