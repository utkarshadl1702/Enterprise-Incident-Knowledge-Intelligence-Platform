from datetime import datetime
import sys
from pathlib import Path


from airflow.decorator import dag, task 

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from airflow.docker.dags.ingestion.github_issues import main


@dag(
    dag_id="github_issues_ingestion",
    start_date=datetime(2026, 1, 1),
    schedule="@hourly",
    catchup=False,
    tags=["github", "ingestion"],
)
def github_issues_ingestion():
    @task(task_id="ingest_github_issues")
    def ingest_github_issues():
        main()

    ingest_github_issues()


github_issues_ingestion()