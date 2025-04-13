#!/bin/bash

airflow db init

airflow users create \
    --username admin \
    --firstname Air \
    --lastname Flow \
    --role Admin \
    --email admin@example.com \
    --password admin || true

exec airflow "$@"