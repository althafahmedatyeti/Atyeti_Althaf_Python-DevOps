from airflow import DAG
from airflow.providers.google.cloud.operators.dataproc import DataprocStartClusterOperator
from datetime import datetime, timedelta
# GCP project-specific variables
PROJECT_ID = "iot-stream-project"
REGION = "us-central1"
CLUSTER_NAME = "iot-processing-cluster"
default_args = { # Default arguments for the DAG
    'start_date': datetime(2025, 7, 21),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
# Define the DAG
with DAG(
    dag_id='start_cluster_dag',
    schedule_interval="0 5 * * *",  # Runs every day at 5:00 AM
    default_args=default_args,
    catchup=False,
    tags=['dataproc', 'start'],
) as dag:

    stop_cluster = DataprocStartClusterOperator(  # starts an existing Dataproc cluster.
        task_id="start_cluster_task",
        project_id=PROJECT_ID,
        region=REGION,
        cluster_name=CLUSTER_NAME,
    )