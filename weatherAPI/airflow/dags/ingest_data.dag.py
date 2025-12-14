from airflow.decorators import dag, task
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ingest_data.ingest_data import main
from airflow.operators.python import PythonOperator
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 12, 14),
    'description': 'Ingest weather data from api and load it to Postgres',
    'catchup': False,
}


@dag(
    dag_id='ingest_weather_data',
    default_args=default_args,
    schedule=timedelta(minutes=1),
    catchup=False
)
def ingest_dag():
    
    @task
    def run_ingestion_task():
        main()

    @task
    def success():
        print("Data Ingested successfully")

    run_ingestion_task() >> success()

ingest_dag()
