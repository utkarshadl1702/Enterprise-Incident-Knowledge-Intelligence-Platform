import requests
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import boto3
from dotenv import load_dotenv

load_dotenv()

owner = os.getenv("OWNER")
repo = os.getenv("REPO")
s3_bucket = os.getenv("S3_BUCKET")

if not owner or not repo:
    raise RuntimeError("OWNER and REPO must be set in .env")
if not s3_bucket:
    raise RuntimeError("S3_BUCKET must be set in .env")

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

timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
s3_key = f"raw/github-issues/{timestamp}.json"
boto3.client("s3").put_object(
    Bucket=s3_bucket,
    Key=s3_key,
    Body=json.dumps(issues, indent=2).encode("utf-8"),
    ContentType="application/json",
)

print(f"Downloaded {len(issues)} issues, saved locally to {output_file}")
print(f"Uploaded to s3://{s3_bucket}/{s3_key}")