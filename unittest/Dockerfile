FROM registry.cn-shanghai.aliyuncs.com/sdk-test/airflow-test-infra:pybuilder-base

RUN pip install 'pymongo==3.9.0' \
    && pip install 'paramiko==2.6.0' \
    && apt install -y android-tools-adb
