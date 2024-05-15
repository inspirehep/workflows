import datetime
import json

from airflow.decorators import dag, task
from airflow.sensors.sql import SqlSensor
from hooks.inspirehep.inspire_http_hook import InspireHttpHook


@dag(start_date=datetime.datetime(2021, 1, 1), schedule_interval=None)
def happy_flow_dag():
    inspire_http_hook = InspireHttpHook()

    @task
    def fetch_document(filename: str) -> dict:
        from include.utils.utils import get_s3_client

        s3_client = get_s3_client()
        s3_client.download_file("inspire-incoming", filename, f"./{filename}")
        with open(f"./{filename}") as f:
            data = json.load(f)
        return data

    @task()
    def normalize_affiliations(data):
        from include.inspire.affiliations_normalization import \
            assign_normalized_affiliations

        endpoint = "/curation/literature/affiliations-normalization"
        request_data = {"authors": data["authors"], "workflow_id": 1}
        result = inspire_http_hook.call_api(
            endpoint=endpoint, data=request_data, method="GET"
        )
        data = assign_normalized_affiliations(result.json(), data=data)
        return data

    @task.branch()
    def auto_approval(data):
        from include.inspire.approval import auto_approve

        if auto_approve(data):
            return ["validate"]
        return ["wait_for_approval"]

    sensor = SqlSensor(
        task_id="wait_for_approval",
        conn_id="inspire_db_connection",
        poke_interval=2,
        sql="select * from workflow_approval where id = '2307.13748'",
    )

    @task()
    def validate():
        return

    fetch_document_task = fetch_document("test.json")
    normalize_affiliations_task = normalize_affiliations(fetch_document_task)
    auto_approval = auto_approval(normalize_affiliations_task)
    validate_task = validate()

    (
        fetch_document_task
        >> normalize_affiliations_task
        >> auto_approval
        >> [validate_task, sensor]
    )
    sensor >> validate_task


happy_flow_dag()
