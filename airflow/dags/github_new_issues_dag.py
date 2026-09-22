import sys
from pathlib import Path

from airflow.decorators import dag, task
from airflow.operators.python import get_current_context
from pendulum import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ingestion.github_issues import main_new_issues


@dag(
    dag_id="github_new_issues_ingestion",
    start_date=datetime(2026, 1, 1),
    schedule="*/5 * * * *",
    catchup=False,
    tags=["github", "issues", "ingestion"],
)
def github_new_issues_ingestion():
    @task(task_id="ingest_new_github_issues")
    def ingest_new_github_issues():
        context = get_current_context()
        main_new_issues(context["data_interval_start"])

    ingest_new_github_issues()


github_new_issues_ingestion()