import json

import requests
import tenacity
from airflow.models import Variable
from airflow.providers.http.hooks.http import HttpHook


class InspireHttpHook(HttpHook):
    """
    Hook to manage connection to Inspire API
    It overrides the original `run` method in HttpHook so that
    we can pass data argument as data, not params
    """

    def __init__(self, method="GET", http_conn_id="inspire_connection"):
        super().__init__(method=method, http_conn_id=http_conn_id)

    def run(self, endpoint, data=None, headers=None, extra_options=None):
        extra_options = extra_options or {}

        session = self.get_conn(headers)

        if not self.base_url.endswith("/") and not endpoint.startswith("/"):
            url = self.base_url + "/" + endpoint
        else:
            url = self.base_url + endpoint

        req = requests.Request(self.method, url, data=data, headers=headers)

        prepped_request = session.prepare_request(req)
        self.log.info("Sending '%s' to url: %s", self.method, url)
        return self.run_and_check(session, prepped_request, extra_options)


def call_inspire_api_with_hook(endpoint, data):
    http_hook = InspireHttpHook(http_conn_id="inspire_connection", method="GET")
    headers = {
        "Authorization": f'Bearer {Variable.get("inspire_token")}',
        "Accept": "application/json",
    }
    retry_args = dict(
        wait=tenacity.wait_exponential(),
        stop=tenacity.stop_after_attempt(10),
        retry=tenacity.retry_if_exception_type(Exception),
    )
    response = http_hook.run_with_advanced_retry(
        _retry_args=retry_args,
        endpoint=endpoint,
        headers=headers,
        data=json.dumps(data),
    )
    return response
