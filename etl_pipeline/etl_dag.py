import os
from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator

DEFAULT_ARGS = {
    "owner": "you",
    "retries": 2,  # retry a failed task up to 2 times
    "retry_delay": timedelta(minutes=5),  # wait 5 minutes between retries
    "email_on_failure": False,  # set to True and add 'email' to alert
    "email_on_retry": False,
}


TMP_DIR = Path(__file__).parents[1] / "tmp"
RAW_PARQUET = str(TMP_DIR / "raw_{{ ds }}.parquet")  # {{ ds }} = run date
CLEAN_PARQUET = str(TMP_DIR / "clean_{{ ds }}.parquet")


def task_extract(**context) -> None:

    import sys

    sys.path.insert(0, str(Path(__file__).parents[1]))

    from config import Settings
    from extract import extract

    settings = Settings()
    TMP_DIR.mkdir(exist_ok=True)

    ds = context["ds"]
    raw_path = str(TMP_DIR / f"raw_{ds}.parquet")

    raw_df = extract(settings.csv_path)
    raw_df.to_parquet(raw_path, index=False)

    context["ti"].xcom_push(key="raw_path", value=raw_path)


def task_transform(**context) -> None:

    import sys

    sys.path.insert(0, str(Path(__file__).parents[1]))

    import pandas as pd

    from transform import transform

    ds = context["ds"]
    clean_path = str(TMP_DIR / f"clean_{ds}.parquet")

    raw_path = context["ti"].xcom_pull(task_ids="extract_task", key="raw_path")

    raw_df = pd.read_parquet(raw_path)
    clean_df = transform(raw_df)
    clean_df.to_parquet(clean_path, index=False)

    context["ti"].xcom_push(key="clean_path", value=clean_path)


def task_load(**context) -> None:

    import sys

    sys.path.insert(0, str(Path(__file__).parents[1]))

    import pandas as pd

    from config import Settings
    from load import get_engine, load, verify_connection

    settings = Settings()

    clean_path = context["ti"].xcom_pull(task_ids="transform_task", key="clean_path")

    clean_df = pd.read_parquet(clean_path)
    engine = get_engine(settings.database_url)
    verify_connection(engine)
    load(clean_df, engine, settings.table_name)


def task_cleanup(**context) -> None:

    import os

    ds = context["ds"]
    for path in [
        TMP_DIR / f"raw_{ds}.parquet",
        TMP_DIR / f"clean_{ds}.parquet",
    ]:
        if path.exists():
            os.remove(path)


with DAG(
    dag_id="etl_csv_to_postgres",
    description="Daily ETL: reads sales CSV, cleans data, loads to Postgres",
    default_args=DEFAULT_ARGS,
    schedule="0 6 * * *",  # every day at 06:00 UTC
    start_date=datetime(2024, 1, 1),
    catchup=False,  # don't backfill historical runs
    tags=["etl", "sales", "postgres"],
) as dag:
    extract_task = PythonOperator(
        task_id="extract_task",
        python_callable=task_extract,
    )

    transform_task = PythonOperator(
        task_id="transform_task",
        python_callable=task_transform,
    )

    load_task = PythonOperator(
        task_id="load_task",
        python_callable=task_load,
    )

    cleanup_task = PythonOperator(
        task_id="cleanup_task",
        python_callable=task_cleanup,
        trigger_rule="all_done",
    )

    extract_task >> transform_task >> load_task >> cleanup_task
