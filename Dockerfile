FROM apache/airflow:2.6.3

USER root

RUN mkdir -p ${AIRFLOW_HOME} && chown -R airflow: ${AIRFLOW_HOME}

USER airflow

RUN airflow db init
