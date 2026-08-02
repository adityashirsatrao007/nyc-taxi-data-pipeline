"""Daily NYC Taxi ETL DAG.

Downloads the daily NYC Yellow Taxi trip CSV, loads it into the warehouse
(duckdb locally, BigQuery in cloud), then invokes dbt build.
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

DEFAULT_DATE = "{{ ds }}"
DATA_DIR = "/tmp/nyc_taxi"


def download_trips(ds: str = None, **kwargs):
    import os
    import urllib.request

    os.makedirs(DATA_DIR, exist_ok=True)
    # Use an available public sample (2024 Yellow Taxi, per-month file).
    # Swap to your preferred source; GCS public bucket below is a common one.
    date_part = (datetime.strptime(ds or "2024-01-01", "%Y-%m-%d")).strftime("%Y-%m")
    url = (
        "https://d37ci6vzurychx.cloudfront.net/trip-data/"
        f"yellow_tripdata_{date_part}.parquet"
    )
    dest = os.path.join(DATA_DIR, f"yellow_{date_part}.parquet")
    urllib.request.urlretrieve(url, dest)
    print(f"Downloaded {dest}")
    return dest


default_args = {
    "owner": "aditya",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2024, 1, 1),
    "catchup": False,
}

with DAG(
    "nyc_taxi_etl",
    default_args=default_args,
    description="NYC taxi batch ETL: download -> ingest -> dbt build",
    schedule_interval="@daily",
    catchup=False,
    tags=["data-engineering", "nyc-taxi"],
) as dag:

    download = PythonOperator(
        task_id="download_trips",
        python_callable=download_trips,
        provide_context=True,
    )

    ingest = BashOperator(
        task_id="ingest_to_warehouse",
        bash_command=f"python {DATA_DIR}/load.py {{ ti.xcom_pull(task_ids='download_trips') }}",
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command="cd /opt/dbt/nyc_taxi && dbt build --profiles-dir /opt/dbt",
        env={
            "DBT_TARGET": "{{ var.value.dbt_target | default('duckdb') }}",
        },
    )

    download >> ingest >> dbt_build
