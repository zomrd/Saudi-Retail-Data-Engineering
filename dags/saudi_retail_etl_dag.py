
from datetime import datetime
import subprocess

from airflow.sdk import dag, task


@dag(
    dag_id="saudi_retail_etl",
    schedule="0 9 * * *",
    start_date=datetime(2026, 10, 1),
    catchup=False,
    tags=["saudi_retail", "data_engineering"],
)
def saudi_retail_pipeline():

    @task
    def run_etl():

        etl_file = (
            "/mnt/c/Users/zmrds/"
            "Saudi_Retail_Data_Engineering/"
            "etl_pipeline.py"
        )

        subprocess.run(
            [
                "/home/zomrod_salman/airflow_project/"
                "airflow_venv/bin/python",
                etl_file,
            ],
            check=True,
        )

    run_etl()


saudi_retail_pipeline()
from datetime import datetime

from airflow.sdk import dag, task


