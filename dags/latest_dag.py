import os
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from get_rates import get_historical_rates
import datetime


AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
PG_USER = "airflow"
PG_PASSWORD = "airflow"
PG_HOST = "postgres"
PG_PORT = "5432"
PG_DATABASE = "postgres"
PG_TABLE = 'btc_usd_rates'


default_args = {
    "owner": "airflow",
    "start_date": datetime.datetime.now(),
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="latest_dag",
    schedule_interval="0 */3 * * *",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['exchange_etl'],
) as dag:
    latest_rates = PythonOperator(
        task_id="latest_rates_task",
        python_callable=get_historical_rates,
        op_kwargs={
            "user": f"{PG_USER}",
            "password": f"{PG_PASSWORD}",
            "host": f"{PG_HOST}",
            "port": f"{PG_PORT}",
            "db": f"{PG_DATABASE}",
            "table_name": f"{PG_TABLE}",
        }
    )
    sleep = BashOperator(
        task_id='need_some_sleep',
        bash_command=f'sleep 3'
    )

latest_rates >> sleep


