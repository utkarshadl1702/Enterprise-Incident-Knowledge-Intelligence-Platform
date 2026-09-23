import requests
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import boto3
from dotenv import load_dotenv

load_dotenv()


def _config():
    owner = os.getenv("OWNER")
    repo = os.getenv("REPO")
    s3_bucket = os.getenv("S3_BUCKET")

    if not owner or not repo:
        raise RuntimeError("OWNER and REPO must be set in .env")
    if not s3_bucket:
        raise RuntimeError("S3_BUCKET must be set in .env")

    return owner, repo, s3_bucket


def _upload_to_s3(issues, bucket, prefix):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    s3_key = f"{prefix}/{timestamp}.json"
    boto3.client("s3").put_object(
        Bucket=bucket,
        Key=s3_key,
        Body=json.dumps(issues, indent=2).encode("utf-8"),
        ContentType="application/json",
    )
    return s3_key


def main():
    owner, repo, s3_bucket = _config()

    # Github API url to fetch issues

    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    # url = "https://api.github.com/repos/apache/spark/issues"


    #get response and check for errors

    response = requests.get(url)

    response.raise_for_status()

    issues = response.json()


    #redirect responses to github_issues.json file in data/github directory (locally for now/test)

    output_dir = Path("data/github")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "issues.json"

    with open(output_file, "w") as f:
        json.dump(issues, f, indent=2)




    #Saving the json file in S3 bucket with timestamped key

    s3_key = _upload_to_s3(issues, s3_bucket, "raw/github-issues")

    print(f"Downloaded {len(issues)} issues, saved locally to {output_file}")
    print(f"Uploaded to s3://{s3_bucket}/{s3_key}")


def main_new_issues(since):
    owner, repo, s3_bucket = _config()
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    response = requests.get(
        url,
        params={"since": since.astimezone(timezone.utc).isoformat(), "per_page": 100},
        timeout=30,
    )
    response.raise_for_status()

    issues = [
        issue
        for issue in response.json()
        if "pull_request" not in issue
        and datetime.fromisoformat(issue["created_at"].replace("Z", "+00:00")) >= since
    ]

    if not issues:
        print("No new GitHub issues found")
        return

    s3_key = _upload_to_s3(issues, s3_bucket, "raw/github-issues")
    print(f"Found {len(issues)} new issues")
    print(f"Uploaded to s3://{s3_bucket}/{s3_key}")


if __name__ == "__main__":
    main()