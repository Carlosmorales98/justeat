FROM apache/airflow:2.6.1

USER airflow

RUN pip install --no-cache-dir requests psycopg2-binary
