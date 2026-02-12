import logging

import requests
from requests import Response, Session
from tenacity import (
    after_log,
    before_sleep_log,
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential_jitter,
)

from airflow_dag_data_pipeline.config import Settings

settings = Settings()
session = requests.Session()
logger = logging.getLogger(__name__)
params: dict[str, str | int | float] = {
    "lat": 54.9069,
    "lon": -1.3838,
    "dt": 1767830400,
    "appid": settings.openweather_api_key,
    "units": "metric",
}


def _should_retry(exception: BaseException) -> bool:
    """Determine if an exception should trigger a retry.

    Args:
        exception: The exception that was raised

    Returns:
        True if the request should be retried, False otherwise
    """
    if isinstance(exception, (requests.Timeout, requests.ConnectionError)):
        return True

    # HTTP errors - only retry specific codes
    if isinstance(exception, requests.HTTPError):
        if exception.response is not None:
            return exception.response.status_code in {408, 429, 500, 502, 503, 504}

    return False


DEFAULT_HEADERS: dict[str, str] = {
    "User-Agent": "WeatherApp/1.0",
    "Accept": "application/json",
}


@retry(
    stop=stop_after_attempt(settings.max_retry_attempts),
    wait=wait_exponential_jitter(
        initial=settings.retry_initial_wait_seconds,
        max=settings.retry_max_wait_seconds,
        exp_base=settings.retry_backoff_multiplier,
    ),
    retry=retry_if_exception(_should_retry),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    after=after_log(logger, logging.INFO),
    reraise=True,
)
def api_call(
    session: Session,
    url: str,
    params: dict[str, str | int | float] | None = None,
    timeout_s: float = 3.0,
) -> Response:
    """Make an HTTP GET request with retry logic.

    Args:
        session: requests Session object
        url: URL to request
        params: Query parameters (optional)
        timeout_s: Request timeout in seconds

    Returns:
        Response object from the HTTP request
    """
    response = session.get(url, params=params, timeout=timeout_s)
    response.raise_for_status()
    return response
