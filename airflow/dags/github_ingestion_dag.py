from datetime import datetime
import sys

from airflow.decorators import dag, task

sys.path.insert(0, "/Users/utkarshadlakha/Documents/Enterprise-Incident-Knowledge-Intelligence-Platform")

from ingestion.github_issues import main


@dag(
    dag_id="github_issues_ingestion",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["github", "ingestion"],
)
def github_issues_ingestion():
    @task(task_id="ingest_github_issues")
    def ingest_github_issues():
        main()

    ingest_github_issues()


github_issues_ingestion()