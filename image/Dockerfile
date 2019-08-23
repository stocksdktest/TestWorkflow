FROM registry.njuics.cn/fluentd/python:3.5

ENV C_FORCE_ROOT true

RUN apt-get update && apt-get install -y vim android-tools-adb

RUN pip install -U -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com apache-airflow apache-airflow[postgres] apache-airflow[celery] apache-airflow[rabbitmq] psycopg2 celery redis flower fluent-logger protobuf
