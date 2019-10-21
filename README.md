### How to testing without Airflow clusters

* put your testing code under `unittest/`
* add pypi dependence in `build.py`
* `docker run -it -v $(pwd):/opt -v $(pwd)/unittest/adbkeys:/root/.android -e AIRFLOW__CORE__PLUGINS_FOLDER=/opt/plugins -e AIRFLOW__CORE__DAGS_FOLDER=/opt/dags -e GITHUB_ACCESS_TOKEN=${token} --entrypoint /mnt/entrypoint.sh registry.cn-shanghai.aliyuncs.com/sdk-test/airflow-test-infra:pybuilder-base pyb install_dependencies run_unit_tests`
