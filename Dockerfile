FROM apache/airflow:2.8.3-python3.11

USER root

RUN mkdir -p ${AIRFLOW_HOME} && chown -R airflow: ${AIRFLOW_HOME}

USER airflow

RUN airflow db init
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade --user -r requirements.txt
