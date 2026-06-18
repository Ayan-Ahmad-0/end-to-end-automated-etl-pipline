from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 8, 1),
    'depends_on_past': False,
    'retries': 1,
}

with DAG(
    dag_id='Taxi_data_pipeline',
    default_args=default_args,
    schedule_interval='*/15 * * * *',  
    catchup=False,
    description='Produce and consume NYC taxi data using Kafka and store in PostgreSQL',
) as dag:

    produce_data = BashOperator(
    task_id='run_kafka_producer',
    bash_command='python /opt/airflow/scripts/kproducer.py || exit 1',
    do_xcom_push=True,
)

    consume_data = BashOperator(
        task_id='run_kafka_consumer',
        bash_command='python /opt/airflow/scripts/consumer_to_postgres.py',
        execution_timeout=timedelta(minutes=5),
    )

    ml_demand_forecast = BashOperator(
    task_id="ml_demand_forecast",
    bash_command="python /opt/airflow/scripts/ml_demand_forecast.py",
)
    
    ml_busy_location = BashOperator(
    task_id="ml_busy_location",
    bash_command="python /opt/airflow/scripts/ml_busy_location.py",
)
    
    add_weather = BashOperator(
    task_id="add_weather_data",
    bash_command="python /opt/airflow/scripts/weather_enrichment.py",
    execution_timeout=timedelta(minutes=2),
)

    backup_postgres = BashOperator(
    task_id="backup_postgres_data",
    bash_command="bash -c '/opt/airflow/scripts/postgres_backup.sh'",
)

    produce_data >> consume_data>>ml_demand_forecast>>ml_busy_location>>add_weather>>backup_postgres
