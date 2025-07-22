from airflow import DAG
from airflow.providers.google.cloud.operators.dataproc import DataprocStartClusterOperator
from datetime import datetime, timedelta
PROJECT_ID = "iot-stream-project"
REGION = "us-central1"
CLUSTER_NAME = "iot-processing-cluster"
# Default arguments for the DAG
default_args = {
    'start_date': datetime(2025, 7, 21),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
# Define the DAG
with DAG(
    dag_id='stop_cluster_dag',
    schedule_interval="0 1 * * *",  # stops every day at 1:00 AM
    default_args=default_args,
    catchup=False,
    tags=['dataproc', 'stop'],
) as dag:
# Task to start the Dataproc cluster
    start_cluster = DataprocStartClusterOperator( 
        task_id="stop_cluster_task",
        project_id=PROJECT_ID,
        region=REGION,
        cluster_name=CLUSTER_NAME,
    )
