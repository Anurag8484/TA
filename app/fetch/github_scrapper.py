import os
import requests
from urllib.parse import urljoin

GITHUB_OWNER = "sanand0"
GITHUB_REPO = "tools-in-data-science-public"
BRANCH = "tds-2025-01"
API_BASE = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents"
RAW_BASE = f"https://raw.githubusercontent.com/{GITHUB_OWNER}/{GITHUB_REPO}/{BRANCH}"
OUTPUT_DIR = "app/data/raw/github"

def fetch_md_files(api_url=API_BASE, base_path=""):
    response = requests.get(api_url, params={"ref": BRANCH})
    response.raise_for_status()
    files = response.json()
    md_urls = []
    for file in files:
        if file["type"] == "file" and file["name"].endswith(".md"):
            raw_url = urljoin(RAW_BASE + "/", file["path"])
            md_urls.append((file["path"], raw_url))
        elif file["type"] == "dir":
            md_urls += fetch_md_files(file["url"], file["path"])
    return md_urls

def download_all_markdowns():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    md_files = fetch_md_files()
    for path, url in md_files:
        local_path = os.path.join(OUTPUT_DIR, path)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        print(f"📥 Downloading {path}")
        r = requests.get(url)
        if r.status_code == 200:
            with open(local_path, "w", encoding="utf-8") as f:
                f.write(r.text)
        else:
            print(f"❌ Failed to download {url}")
    print(f"✅ Downloaded {len(md_files)} markdown files to {OUTPUT_DIR}")

if __name__ == "__main__":
    download_all_markdowns()
