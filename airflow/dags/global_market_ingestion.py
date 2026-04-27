from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

default_args = {
    "owner": "rimsha",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id = "global_market_ingestion",
    default_args = default_args,
    description="Orchestration for Global Market Harmonizer",
    start_date=datetime(2026, 4, 20),
    schedule="@daily",
    catchup=False,
    tags=["project", "orchestration", "s3", "phase2"],
) as dag:
    
    run_phase1_extraction = BashOperator(
        task_id = "run_phase1_extraction",
        bash_command="cd /opt/airflow && PYTHONPATH=/opt/airflow python -m extraction.main",
    )

    wait_for_exchange_rates_file = S3KeySensor(
        task_id = "wait_for_exchange_rates_file",
        bucket_name = "s3-retail-raw-zone",
        bucket_key = "{{ ds_nodash[:4] }}/{{ ds_nodash[4:6] }}/{{ ds_nodash[6:8] }}/exchange_rates.json",
        aws_conn_id="aws_default",
        poke_interval=30,
        timeout=300,
        mode="poke",
    )

    wait_for_products_file = S3KeySensor(
        task_id = "wait_for_products_file",
        bucket_name = "s3-retail-raw-zone",
        bucket_key = "{{ ds_nodash[:4] }}/{{ ds_nodash[4:6] }}/{{ ds_nodash[6:8] }}/products.json",
        aws_conn_id="aws_default",
        poke_interval=30,
        timeout=300,
        mode="poke",
    )

    cloud_load_start_signal = EmptyOperator(
        task_id="cloud_load_start_signal"
    )

    run_phase1_extraction >> [wait_for_exchange_rates_file, wait_for_products_file] >> cloud_load_start_signal