from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def say_hello() -> None:
    print("Hello, world!")


with DAG(
    dag_id="hello_world",
    start_date=datetime(2025, 1, 1),
    schedule=None,  # manual trigger only
    catchup=False,
    tags=["example"],
) as dag:
    PythonOperator(
        task_id="say_hello",
        python_callable=say_hello,
    )
