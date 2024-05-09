import logging

from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.utils.trigger_rule import TriggerRule

default_args = {
    "owner": "Carlos",
    "depends_on_past": False,
    "retries": 1,

}

docs = """
### dbt Pipeline

Design a table to store the week-over-week report data. The table
should have columns for week_start_date, sessions, pageviews, users,
bounce_rate, conversion_rate, etc. The week_start_date column will be used to
represent each reporting week's starting date.

We use data.csv as a dbt seed for simulated API return.
"""


@dag(dag_id="dbt_run_v1",
     default_args=default_args,
     doc_md=docs,
     schedule_interval="@daily",
     start_date=days_ago(1)
     )
def taskflow():
    @task.bash
    def create_database() -> str:
        """
        This doesn't make sense here, but it's only for testing dbt. It would
        be a Postgres operator, this approach is used for simplicity.
        """

        logging.info("If fail it's OK. Only is need to run once")

        command = ('psql postgresql://airflow:airflow@postgres:5432/postgres '
                   '-c "CREATE DATABASE dwh"')
        return command

    @task.bash(trigger_rule=TriggerRule.ALL_DONE)
    def dbt_deps() -> str:
        """
        Install project dependencies.
        """
        return "cd /opt/airflow/dbt && dbt deps --target dev --profiles-dir ."
        
    @task.bash()
    def dbt_seed() -> str:
        """
        Seed dataset.csv
        """
        return "cd /opt/airflow/dbt && dbt seed --target dev --profiles-dir ."

    @task.bash()
    def dbt_run() -> str:
        """
        Run dbt.
        """
        return "cd /opt/airflow/dbt && dbt run --target dev --profiles-dir ."

    @task.bash()
    def dbt_test() -> str:
        """
        Test dbt.
        """
        return "cd /opt/airflow/dbt && dbt test --target dev --profiles-dir ."

    @task.bash()
    def show_values():
        """
        Some resuts!
        """

        query = """
                SELECT
                summary_week::date,
                campaign_name,
                total_spend,
                prev_spend,
                ctr,
                wow_ctr,
                cpi,
                wow_cpi
                FROM dwh.dashboard_week_campaigns
                WHERE campaign_name = 'Super campaign 16'
                ORDER BY 1 DESC;
                """
        command = f'psql postgresql://airflow:airflow@postgres:5432/dwh -c "{query}"' # noqa
        return command

    create_database()
    dbt_deps() >> dbt_seed() >> dbt_run() >> dbt_test() >> show_values()


taskflow()
