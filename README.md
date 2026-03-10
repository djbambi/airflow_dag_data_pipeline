# Airflow DAG Data Pipeline

A Python-based data pipeline that fetches weather data from an external API and
orchestrates processing with Apache Airflow.

---

## Open Issues Summary

The following is a summary of the 16 open issues currently tracked in this
repository, grouped by theme.

---

### 🔌 API & Data Source

| # | Title | Description |
|---|-------|-------------|
| [#51](https://github.com/djbambi/airflow_dag_data_pipeline/issues/51) | Change weather data API endpoint | Switch from the OpenWeather API to the OpenMeteo API. |
| [#52](https://github.com/djbambi/airflow_dag_data_pipeline/issues/52) | Expose result data via FastAPI | Add a FastAPI layer so that pipeline result data can be served over HTTP. |

---

### 🏗️ Infrastructure & DevOps

| # | Title | Description |
|---|-------|-------------|
| [#12](https://github.com/djbambi/airflow_dag_data_pipeline/issues/12) | Pyspark Setup with Docker | Implement a simple PySpark function, configure Spark via Docker Compose, and add an Airflow DAG that runs a Spark calculation. |
| [#18](https://github.com/djbambi/airflow_dag_data_pipeline/issues/18) | Use a frozen/locked install mode | Use `uv sync --dev --frozen` in CI so the build fails when `uv.lock` is out of date, ensuring reproducible installs. |
| [#54](https://github.com/djbambi/airflow_dag_data_pipeline/issues/54) | Add an infra folder for Infrastructure-as-Code | Create an `infra/` directory to manage cloud infrastructure using Pulumi in Python. |

---

### 🏛️ Architecture & Refactoring

| # | Title | Description |
|---|-------|-------------|
| [#10](https://github.com/djbambi/airflow_dag_data_pipeline/issues/10) | Extract OpenWeather request parameter construction into client helper | Move OpenWeather-specific request-parameter building (e.g. `appid`, `dt`) out of `main.py` and into a dedicated helper alongside the client code. |
| [#14](https://github.com/djbambi/airflow_dag_data_pipeline/issues/14) | Save JSON data with a date-based filename | Replace the hardcoded output filename `weather_data.json` with one derived from the date, configurable via environment variables or function parameters. |
| [#36](https://github.com/djbambi/airflow_dag_data_pipeline/issues/36) | Remove import-time Settings initialisation | `Settings()` is instantiated at module import time; this causes Pydantic validation errors during Airflow DAG parsing and in unit tests unless `OPENWEATHER_API_KEY` is set. Inject `Settings` into functions instead. |
| [#55](https://github.com/djbambi/airflow_dag_data_pipeline/issues/55) | Refactor to separate business logic from data engineering logic | Reorganise the codebase so that core business logic is decoupled from data engineering concerns and other software domains. |

---

### 🛡️ Error Handling & Logging

| # | Title | Description |
|---|-------|-------------|
| [#19](https://github.com/djbambi/airflow_dag_data_pipeline/issues/19) | Restore `HttpUrl` type in `config.py` | The `openweather_base_url` field was weakened from `HttpUrl` to `str`, losing Pydantic's URL validation. It should be restored to a proper URL type. |
| [#29](https://github.com/djbambi/airflow_dag_data_pipeline/issues/29) | Add user-friendly error handling for missing environment variables | Catch Pydantic `ValidationError` in `main.py`, display a clean error message to stderr listing each missing variable, and exit with code 1 instead of showing a raw traceback. |
| [#39](https://github.com/djbambi/airflow_dag_data_pipeline/issues/39) | Add logging for exception status codes | Log the HTTP status code when `_should_retry` inspects an `HTTPError`, so retry decisions are observable in logs. |

---

### 🧪 Testing

| # | Title | Description |
|---|-------|-------------|
| [#34](https://github.com/djbambi/airflow_dag_data_pipeline/issues/34) | Add retry loop tests for the weather client | The tenacity-based retry decorator on `api_call` is not covered by tests. Add a test that simulates e.g. a 503 followed by a 200 and asserts the request was retried. |
| [#40](https://github.com/djbambi/airflow_dag_data_pipeline/issues/40) | Review scope of test fixtures | Consider changing pytest fixture scope to `module` (or higher) where appropriate to avoid redundant initialisation, while being careful about shared state side-effects. |
| [#41](https://github.com/djbambi/airflow_dag_data_pipeline/issues/41) | Consolidate duplicated tests using parametrize | Several similar tests could be merged into a single parametrized test, and logging assertions could be added at the same time. |

---

### 🔧 Tooling

| # | Title | Description |
|---|-------|-------------|
| [#53](https://github.com/djbambi/airflow_dag_data_pipeline/issues/53) | Switch type checker from mypy to ty | Replace mypy with `ty` for type checking. |
