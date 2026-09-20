import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

owner = os.getenv("OWNER")
repo = os.getenv("REPO")

# Github API url to fetch issues
url = f"https://api.github.com/repos/{owner}/{repo}/issues"
# url = "https://api.github.com/repos/apache/spark/issues"


#get response and check for errors

response = requests.get(url)

response.raise_for_status()

issues = response.json()


#redirect responses to github_issues.json file in data/github directory

output_dir = Path("data/github")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "issues.json"

with open(output_file, "w") as f:
    json.dump(issues, f, indent=2)

print(f"Downloaded {len(issues)} issues and saved to {output_file}")