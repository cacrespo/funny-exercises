#!/bin/bash
airflow users create -u airflow -p airflow -r Admin -e test@test.com -f airflow -l airflow;
exec airflow webserver
