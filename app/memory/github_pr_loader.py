import os
import requests
from pathlib import Path

GITHUB_API = "https://api.github.com"

def download_pr_files(owner: str, repo: str, pr_number: int, save_dir: str = "repos/") -> str:
    headers = {"Accept": "application/vnd.github.v3+json"}
    url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{pr_number}/files"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    files = response.json()

    pr_dir = Path(save_dir) / f"{owner}_{repo}_pr{pr_number}"
    pr_dir.mkdir(parents=True, exist_ok=True)

    for file_info in files:
        if file_info["filename"].endswith(".py") and file_info["status"] in ("added", "modified"):
            raw_url = file_info["raw_url"]
            file_path = pr_dir / file_info["filename"]
            file_path.parent.mkdir(parents=True, exist_ok=True)

            file_content = requests.get(raw_url).text
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(file_content)

    return str(pr_dir)
