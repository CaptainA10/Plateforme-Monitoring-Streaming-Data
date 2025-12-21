from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

# Default Arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define DAG
with DAG(
    'daily_aggregation_dag',
    default_args=default_args,
    description='A daily DAG to aggregate user activity',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
    tags=['monitoring', 'spark'],
    catchup=False
) as dag:

    # Task 1: Print Start
    start_task = BashOperator(
        task_id='print_start',
        bash_command='echo "Starting Daily Aggregation..."',
    )

    # Task 2: Submit Spark Job
    # Note: In a real production environment, we would use SparkSubmitOperator.
    # However, since our Airflow container might not have spark-submit binary or 
    # connection to the Spark Master configured via network in this specific docker-compose setup,
    # we will simulate the submission or use a DockerOperator if available.
    # For this demo, we assume we can trigger it via a simple script or just log the intent.
    # Ideally:
    # spark_submit_task = SparkSubmitOperator(
    #    task_id='spark_submit_job',
    #    application='/opt/airflow/dags/src/batch/daily_stats.py',
    #    conn_id='spark_default',
    #    ...
    # )
    
    # Workaround for Demo: We will just print that we are submitting.
    # To make this functional, we would need to install spark-client in the airflow image.
    spark_submit_task = BashOperator(
        task_id='submit_spark_job',
        bash_command='echo "Simulating Spark Submission of src/batch/daily_stats.py"'
    )

    # Task 3: Run dbt Transformations
    dbt_run_task = BashOperator(
        task_id='dbt_run_transformations',
        bash_command='cd /opt/airflow/dags/dbt_transformations && dbt run --profiles-dir .'
    )

    # Task 3: Notify Completion
    end_task = BashOperator(
        task_id='notify_completion',
        bash_command='echo "Daily Aggregation Completed!"',
    )

    start_task >> spark_submit_task >> dbt_run_task >> end_task
