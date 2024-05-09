# Instructions
1. Set user permissions for Airflow to match your current user
```
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
```
1. Launch Airflow using Docker Compose:
```bash
docker compose up -d
```
1. Check the status of running containers:
```bash
docker ps
```
1. Open a web browser and navigate to type http://localhost:8080 to access the Airflow web interface.

# dbt
We already have a .csv file located inside `datawarehouse/seeds`
