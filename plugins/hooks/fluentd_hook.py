from airflow.hooks.base_hook import BaseHook
from fluent import asyncsender as sender

class FluentdHook(BaseHook):

    conn_type = 'Fluentd'

    def __init__(self, conn_id='fluentd_default', *args, **kwargs):
        super().__init__(source='fluentd')
        # self.fluentd_conn_id = conn_id
        self.connection = self.get_connection(conn_id)
        self.extras = self.connection.extra_dejson
        self.app = self.extras.get('app', 'TEST_RECORD')

    def get_conn(self):
        conn = self.connection
        return sender.FluentSender(tag=self.app, host=conn.host, port=conn.port)
