import tenacity


def tenacity_retry_kwargs() -> dict:
    return dict(
        wait=tenacity.wait_exponential(),
        stop=tenacity.stop_after_attempt(5),
        retry=tenacity.retry_if_exception_type(Exception),
    )
