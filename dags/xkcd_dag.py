from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.append('/opt/airflow/scripts')

from extract import fetch_comic
from transform import enrich_comic
from load import insert_to_db

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

def run_etl():
    comic = fetch_comic()
    if comic:
        views, review, cost = enrich_comic(comic)
        insert_to_db(comic, views, review, cost)

def run_specific_comic_etl(comic_num):
    comic = fetch_comic(comic_num=comic_num)
    if comic:
        views, review, cost = enrich_comic(comic)
        insert_to_db(comic, views, review, cost)

with DAG(
    dag_id='xkcd_etl',
    default_args=default_args,
    description='ETL XKCD comics to PostgreSQL',
    schedule_interval='0 12 * * 1,3,5',
    start_date=datetime(2024, 4, 10),
    catchup=False
) as dag:
    
    task_fetch_transform_load = PythonOperator(
        task_id='fetch_transform_load',
        python_callable=run_etl
    )

    task_specific_comic = PythonOperator(
        task_id='fetch_specific_comic',
        python_callable=run_specific_comic_etl,
        op_args=[614]
    )

    # dbt transformations and tests are executed manually via CLI:
    # docker compose run --rm dbt debug
    # docker compose run --rm dbt run
    # docker compose run --rm dbt test

    task_fetch_transform_load >> task_specific_comic 

