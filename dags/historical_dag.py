import os
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import datetime
from get_rates import get_historical_rates

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
PG_USER = "airflow"
PG_PASSWORD = "airflow"
PG_HOST = "postgres"
PG_PORT = "5432"
PG_DATABASE = "postgres"
PG_TABLE = 'btc_usd_rates'


START_DATE = datetime.datetime(2020, 1, 1)

default_args = {
    "owner": "airflow",
    "start_date": START_DATE,
    "depends_on_past": True,
    "retries": 1,
}

with DAG(
    dag_id="historical_dag",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=True,
    max_active_runs=2,
    tags=['exchange_etl'],
) as dag:
    historical_rates = PythonOperator(
        task_id="historical_rates_task",
        python_callable=get_historical_rates,
        op_kwargs={
            "user": f"{PG_USER}",
            "password": f"{PG_PASSWORD}",
            "host": f"{PG_HOST}",
            "port": f"{PG_PORT}",
            "db": f"{PG_DATABASE}",
            "table_name": f"{PG_TABLE}",
            "execution_date": "{{ execution_date.strftime(\'%Y-%m-%d\') }}",
        }
    )
    sleep = BashOperator(
        task_id='need_some_sleep',
        bash_command=f'sleep 3'
    )

historical_rates >> sleep

