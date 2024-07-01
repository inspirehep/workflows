airflow connections import ${AIRFLOW_HOME}/scripts/connections/connections.json
airflow connections add 'minio' --conn-type 'aws' --conn-login ${MINIO_USER} --conn-password ${MINIO_PASSWORD} --conn-host 's3' --conn-port 9000 --conn-schema 'http'
