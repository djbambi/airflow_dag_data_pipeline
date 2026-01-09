from __future__ import annotations

from pathlib import Path

from airflow.models import DagBag


def test_dag_imports_without_errors() -> None:
    dags_folder = Path(__file__).resolve().parents[1] / "dags"
    dagbag = DagBag(dag_folder=str(dags_folder), include_examples=False)

    assert dagbag.import_errors == {}, f"Import errors: {dagbag.import_errors}"


def test_hello_world_dag_has_expected_task() -> None:
    dags_folder = Path(__file__).resolve().parents[1] / "dags"
    dagbag = DagBag(dag_folder=str(dags_folder), include_examples=False)

    dag = dagbag.dags.get("hello_world")
    assert dag is not None

    assert {t.task_id for t in dag.tasks} == {"say_hello"}
