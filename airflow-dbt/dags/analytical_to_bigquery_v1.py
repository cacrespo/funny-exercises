import logging
import os

from airflow.decorators import dag, task
from airflow.utils.dates import days_ago


# GCP
GCP_BUCKET = 'uri_gcs_bucket' # os.getenv("GCP_BUCKET")
GCP_BIGQUERY_DATASET = 'crespo-datum.raw_data'# os.getenv("GCP_BIGQUERY_DATASET_RAW_DATA")

# EXTERNAL
ANALYTICS_API_KEY = 'magic_api' #os.getenv("ANALYTICS_API_KEY")


TIME_WINDOW = 2  # days
REQUEST_DATE = '{{ ds }}'

default_args = {
    "owner": "Carlos",
    "depends_on_past": False,
    "retries": 1,
}

docs = f"""
### Analytics to BigQuery DAG

This DAG processes events AAA, BBB, and CCC and moves the data to Google Cloud
Storage ({GCP_BUCKET}) and then to BigQuery ({GCP_BIGQUERY_DATASET}) for
further processing.

#### Tasks:
1. **Request Data from API**: This task retrieves data from the source API.
2. **Move Data to GCS**: Copies data into the GCS bucket.
3. **Write Data to BigQuery**: Loads data into BigQuery tables.
4. **Sanity Check**: Performs data integrity checks.
5. **Send Notifications**: Notifies via Slack or email.
"""


@dag(dag_id="analytics_to_bigquery_v1",
     default_args=default_args,
     doc_md=docs,
     schedule_interval="@daily",
     start_date=days_ago(1)
     )
def taskflow():
    @task(task_id="request_API")
    def request_data(REQUEST_DATE, TIME_WINDOW):
        """
        Retrieve relevant data from the source API.
        """
        logging.info("Send HTTP GET request to the API endpoint")
        logging.info("Accept the response (probably a JSON)")
        logging.info("Parse the response and 'flatten' it into .parquet files")

        comment = f"""
        The key here is to always retrieve the information
        associated with the scheduled execution day of the DAG. Every day, we
        will exclusively request information related to {REQUEST_DATE}
        (REQUEST_DATE).
        Additionally, we can use it in combination with {TIME_WINDOW}
        (TIME_WINDOW) to establish a Point In Time and regularly request data
        within a rolling window. This approach ensures that we incrementally
        update our data warehouse and guarantee that if some values were
        recently fixed, we have the correct data.
        """

        logging.info(comment)

    @task(task_id="move_files_GCS")
    def move_data():
        """
        Move data to the specified GCS bucket.
        """
        logging.info("Moving files to Google Cloud Storage")
        logging.info("Using a dedicated bucket is a good practice."
                     "It can be useful in the future if we want to trigger"
                     "processes when a new file is loaded.")

    @task(task_id="write_BQ_table")
    def write_data():
        """
        Use BigQuery to materialize all the information into table(s).
        """
        logging.info("Remember: Airflow is an orchestrator! Don't transform "
                     "the data here.")
        logging.info("The week-over-week calculations can be done later.")
        logging.info("This is a job for BigQuery. We will clean and prepare "
                     "the data using dbt, making efficient and clever use of "
                     "our resources.")

        comment = """
        Here it is important to partition the tables by dates. It
        is crucial for analytical purposes and will also allow us to reduce the
        cost of removing duplicates (for example, if the request brings events
        from 'yesterday and the day before yesterday' and we are required to
        clean that).
        """

        logging.info(comment)

    @task(task_id="sanity_check")
    def sanity_data():
        """
        Simple check: Is the amount of information the same at the end of the
        process as it was at the beginning?
        """
        logging.info("We can use XCOM messages between tasks.")

    @task(task_id="notification")
    def notification():
        """
        Send messages to Slack or email. Was everything OK?
        """
        logging.info("In fact, we can send some preliminary values if someone "
                     "wants them.")

    request_data(REQUEST_DATE, TIME_WINDOW) >> move_data() >> write_data() >> sanity_data() >> notification() # noqa


taskflow()
