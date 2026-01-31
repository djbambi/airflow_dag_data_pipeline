from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from airflow_dag_data_pipeline.main import main

with DAG(
    dag_id="weather_simple_wrapper",
    start_date=datetime(2025, 1, 1),
    schedule=None,  # manual trigger for now (simplest)
    catchup=False,
) as dag:  # noqa: F841
    run = PythonOperator(
        task_id="run_main",
        python_callable=main,
    )
