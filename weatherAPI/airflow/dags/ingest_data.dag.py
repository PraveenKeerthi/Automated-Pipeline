from airflow.decorators import dag, task
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
import sys
import os
from ingest_data.ingest_data import main
from docker.types import Mount

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
    # We use network_mode='weatherapi_weatherapi' to connect this container to the 
    # existing Docker Compose network where the Postgres database creates.
    # 'weatherapi' is the project name (directory name) and 'weatherapi' is the 
    # network name defined in docker-compose.yml.

    # Bind -> 2 way comminication, so you dont have to re-build the image.
    dbt_run = DockerOperator(
        task_id='dbt_run',
        image='ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
        command='run',
        api_version='auto',
        auto_remove='success',
        docker_url="unix://var/run/docker.sock",
        network_mode="weatherapi_weatherapi",
        mounts=[
            Mount(source="D:/Projects/Automated Pipelines/weatherAPI/dbt/my_project", target="/usr/app", type="bind"),
        ],
        working_dir="/usr/app",
    )

    @task
    def success():
        print("Data Ingested successfully")

    run_ingestion_task() >> dbt_run >> success()

ingest_dag()
