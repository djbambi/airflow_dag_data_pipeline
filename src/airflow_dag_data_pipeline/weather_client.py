import logging
from typing import Any, Mapping

import requests
from tenacity import (
    Retrying,
    after_log,
    before_sleep_log,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential_jitter,
)

from airflow_dag_data_pipeline.config import Settings

DEFAULT_HEADERS: dict[str, str] = {
    "User-Agent": "WeatherApp/1.0",
    "Accept": "application/json",
}

logger = logging.getLogger(__name__)


def _is_retryable_exception(exc: BaseException) -> bool:
    """Determine if an exception should trigger a retry."""
    # Network-level problems: usually retryable
    if isinstance(exc, (requests.Timeout, requests.ConnectionError)):
        return True

    # HTTP errors: retry only for transient status codes
    if isinstance(exc, requests.HTTPError):
        resp = exc.response
        if resp is None:
            return False
        return resp.status_code in {408, 429, 500, 502, 503, 504}

    return False


def _make_http_request(
    session: requests.Session,
    url: str,
    params: Mapping[str, str | int | float],
    timeout_s: float,
) -> requests.Response:
    """
    Make HTTP GET request and validate status code.

    Args:
        session: Configured requests session with headers
        url: Target API endpoint
        params: Query parameters
        timeout_s: Request timeout in seconds

    Returns:
        HTTP response object

    Raises:
        HTTPError: If response status indicates an error
        Timeout: If request exceeds timeout
        ConnectionError: If connection fails
    """
    response = session.get(url, params=params, timeout=timeout_s)
    response.raise_for_status()
    return response


def _parse_json_response(response: requests.Response, url: str) -> dict[str, Any]:
    """
    Parse and validate JSON response.

    Args:
        response: HTTP response object
        url: Original request URL (for error context)

    Returns:
        Parsed JSON as dictionary

    Raises:
        ValueError: If response body is not valid JSON
    """
    try:
        return response.json()
    except ValueError as e:
        raise ValueError(f"Invalid JSON from {url}") from e


def fetch_openweather_data(
    *,
    session: requests.Session,
    url: str,
    params: Mapping[str, str | int | float],
    timeout_s: float,
    settings: Settings,
) -> dict[str, Any]:
    """
    Fetch weather data from OpenWeather API with automatic retries.

    Orchestrates HTTP request with exponential backoff retry logic for
    transient failures (network errors, rate limits, server errors).

    Args:
        session: Configured requests session with headers
        url: OpenWeather API endpoint
        params: Query parameters (lat, lon, dt, appid, units)
        timeout_s: Request timeout in seconds
        settings: Application settings with retry configuration

    Returns:
        Parsed JSON response as dictionary

    Raises:
        HTTPError: For non-retryable HTTP errors (4xx except 408, 429)
        Timeout: After max retries exhausted
        ConnectionError: After max retries exhausted
        ValueError: For malformed JSON responses
    """
    retryer = Retrying(
        stop=stop_after_attempt(settings.max_retries),
        wait=wait_exponential_jitter(
            initial=1,
            max=settings.retry_max_wait_seconds,
            exp_base=settings.retry_backoff_multiplier,
        ),
        retry=retry_if_exception(_is_retryable_exception),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        after=after_log(logger, logging.INFO),
        reraise=True,
    )

    for attempt in retryer:
        with attempt:
            response = _make_http_request(session, url, params, timeout_s)
            return _parse_json_response(response, url)

    raise RuntimeError("Unreachable")
