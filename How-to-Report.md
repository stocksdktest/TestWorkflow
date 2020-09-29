# 遇到问题如何报告才能更好地复现



## 目前存在的问题

最近安卓和iOS都有遇到一些问题。当遇到问题需要解决时，最理想的情况是能够复现问题。但是由于目前大部分情况下是由前端发起请求，驱动Airflow调度测试任务执行，而不是原先用python脚本进行测试，因此获取测试参数存在一些困难与不便。为了更好地协调和解决问题，这里提供一套方案。



## 预备知识

实际应用时前端实际上是进行如下命令的等价操作

```bash
curl -X POST \
  http://<AirflowIP:Port>/api/experimental/dags/<DAG_ID>/dag_runs \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -d '{"conf": <Your Config>  }'
```

conf的样例如下

```json
'conf': {
            'collectionName': 'Test_Android_quote_20200316',
            'Level': '2',
            'CffLevel':'1',
            'DceLevel':'2',
            'CzceLevel':'2',
            'FeLevel':'2',
            'GILevel':'2',
            'ShfeLevel':'2',
            'IneLevel':'2',
            'HKPerms': ['hk10'],
            'roundIntervalSec': '3',
            'tag': [['release-20200103-0.0.3', '53fcc717d954e01d88bc9bd70eaab9ac9a0acb67']],
            'run_times': '1',
            'quote_detail': '1',
            "AirflowMethod": [
                {
                    'testcaseID': 'L2TICKDETAILV2_1',
                    'paramStrs': [
                        {
                            'CODE': '000100.sz',
                            'SUBTYPE': '1001'
                        },
                        {
                            'CODE': '000078.sz',
                            'SUBTYPE': '1001'
                        },
                        {
                            'CODE': '002429.sz',
                            'SUBTYPE': '1001'
                        }
                    ]}
            ],
            'server': [
                {
                    'serverSites1': [
                        ["sh", "http://114.80.155.134:22016","tcp://114.80.155.134:22017"],
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
}
```

对于复现程序打问题，关键就在于这个**DAG_ID**和**conf**。如果能将其以如下格式记录在文件，或者存储在数据库中，对于问题的解决会有很大帮助。

```json
{
    jobID: "manual__2020-01-07T02:23:21.260116 00:00",
    dagID: "ios_compare",
    conf: ..
}
```



## 如何复现

有了如上的参数记录后，就可以用[南大这边实现的脚本](https://github.com/stocksdktest/TestWorkflow/tree/dev/unittest/templates)复现。脚本提供了对目前前端支持的所有类型计划的测试。

以上述conf为例，该conf是执行某个android_compare的参数，修改[android_compare_test.py](https://github.com/stocksdktest/TestWorkflow/blob/dev/unittest/templates/android_compare_test.py)中的`DAG_ID`和`conf`，并执行，即可复现前端过程。这样也更方便调试。