from urllib3 import PoolManager
import json
from airflow.utils.timezone import datetime, parse as parse_datetime, utcnow
from datetime import timedelta

# endpoint_url = 'http://localhost:8080/api/experimental/'
endpoint_url = 'http://221.228.66.83:30690/api/experimental/'


class AirflowRestClient():
    def __init__(self, endpoint_url=endpoint_url) -> None:
        super().__init__()
        self.endpoint_url = endpoint_url
        self.http = PoolManager()

    def http_request_get(self, url):
        r = self.http.request('GET', url)
        print('http request url:', url)
        print('http request GET, status:', r.status)
        if r.status == 500:
            return 'HTTP error'
        try:
            res = json.loads(r.data.decode('utf-8'))
        except json.decoder.JSONDecodeError as e:
            res = r
        return res

    def trigger_dag(self, DAG_ID, data: json):
        """
        POST /api/experimental/dags/<DAG_ID>/dag_runs
        :param DAG_ID:
        :return:Creates a dag_run for a given dag id.Trigger DAG with config
        """
        # Creates a dag_run for a given dag id.Trigger DAG with config
        url = self.endpoint_url + 'dags/' + DAG_ID + '/dag_runs'
        headers = {
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json'
        }
        r = self.http.request(
            method='POST',
            url=url,
            headers=headers,
            body=data
        )

        res = json.loads(r.data.decode('utf-8'))
        print('end trigger')
        return res

    def get_dag_runs(self, DAG_ID):
        """
        GET /api/experimental/dags/<DAG_ID>/dag_runs
        :param DAG_ID:
        :return: Returns a list of Dag Runs for a specific DAG ID.
        """
        url = self.endpoint_url + 'dags/' + DAG_ID + '/dag_runs'
        return self.http_request_get(url)

    def get_dag_runs_instance(self, DAG_ID: str, exeution_on_date: str):
        """
        GET /api/experimental/dags/<string:dag_id>/dag_runs/<string:execution_date>
        :param DAG_ID:
        :param exeution_on_date: “YYYY-mm-DDTHH:MM:SS”,for example: “2016-11-16T11:34:15”.
                if not found, the date could get in get_dag_runs
        :return: Returns a JSON with a dag_run’s public instance variables.
        """
        url = self.endpoint_url + 'dags/' + DAG_ID + '/dag_runs/' + exeution_on_date
        return self.http_request_get(url)

    def get_server_status(self):
        """
        GET /api/experimental/test
        :return: To check REST API server correct work. Return status ‘OK’.
        """
        url = self.endpoint_url + 'test'
        return self.http_request_get(url)

    def get_dag_task_instance(self, DAG_ID: str, exeution_on_date: str, TASK_ID: str):
        """
        GET /api/experimental/dags/<DAG_ID>/dag_runs/<string:execution_date>/tasks/<TASK_ID>
        :param DAG_ID:
        :param exeution_on_date: “YYYY-mm-DDTHH:MM:SS”,for example: “2016-11-16T11:34:15”.
                if not found, the date could get in get_dag_runs
        :param TASK_ID:
        :return: Returns a JSON with a task instance’s public instance variables.
        """
        url = self.endpoint_url + 'dags/' + DAG_ID + '/dag_runs/' + exeution_on_date + '/tasks/' + TASK_ID
        return self.http_request_get(url)

    def pause_dag(self, DAG_ID: str, paused: bool):
        """
        GET /api/experimental/dags/<DAG_ID>/paused/<string:paused>
        :param DAG_ID:
        :param paused:
        :return:
        """
        url = self.endpoint_url + 'dags/' + DAG_ID + '/paused/' + paused.__str__().lower()
        return self.http_request_get(url)

    def get_lastest_runs(self):
        """
        GET /api/experimental/latest_runs
        Returns the latest DagRun for each DAG formatted for the UI.
        :return:
        """
        url = self.endpoint_url + 'latest_runs'
        return self.http_request_get(url)

    def get_pools(self):
        """
        GET /api/experimental/pools
        :return: Get all pools.
        """
        url = self.endpoint_url + 'pools'
        return self.http_request_get(url)

    def get_pool_by_name(self, name: str):
        """
        GET /api/experimental/pools/<string:name>
        :param name:
        :return: Get pool by a given name.
        """
        url = self.endpoint_url + 'pools/' + name
        return self.http_request_get(url)


if __name__ == '__main__':
    DAG_ID = 'ios_sort'
    #execution_on_date = '2020-02-11T04:13:50'
    rest = AirflowRestClient()
    #execution_date = utcnow() + timedelta(minutes=1)
    execution_date = utcnow()
    datetime_string = execution_date.isoformat()
    data = json.dumps({
        'conf': {
            'collectionName': 'test_result',
            'Level': '1',
            'HKPerms': ['hk10'],
            'roundIntervalSec': '3',
            'tag': [['release-20200310-0.0.5', '9e2d1a04b6dba6e800cafadd5046b777326c8bfd']],
            "AirflowMethod": [
                {
                    'testcaseID': 'CATESORTING_2',
                    'paramStrs': [
                        {
                            'CateType': 'SH1133',
                            'param': '0,50,0,0,1',
                            'STOCKFIELDS': '-1',
                            'ADDVALUEFIELDS': '-1'
                        },
                        {
                            'CateType': 'SH1133',
                            'param': '0,50,0,1,1',
                            'STOCKFIELDS': '-1',
                            'ADDVALUEFIELDS': '-1'
                        },
                        {
                            'CateType': 'SH1133',
                            'param': '0,50,1,0,1',
                            'STOCKFIELDS': '-1',
                            'ADDVALUEFIELDS': '-1'
                        }
                    ]
                }
            ],
            'server': [
                {
                    'serverSites1': [
                        ["sh", "http://114.80.155.134:22016"],
                        ["tcpsh", "http://114.80.155.134:22017"],
                    ]
                },
                {
                    'serverSites2': [
                        ["sh", "http://114.80.155.134:22016"],
                        ["shl2", "http://114.80.155.62:22016"],
                    ]
                }
            ]
        },
        'execution_date': datetime_string
    })
    res = rest.trigger_dag(DAG_ID=DAG_ID, data=data)
    print(execution_date)
    print(res)
