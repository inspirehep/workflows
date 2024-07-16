FROM apache/airflow:2.8.3-python3.11

COPY --chown=airflow:root dags /opt/airflow/dags/
COPY --chown=airflow:root plugins /opt/airflow/plugins/
COPY --chown=airflow:root requirements.txt ./requirements.txt

RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r requirements.txt
