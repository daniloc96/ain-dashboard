import os
import requests
from dotenv import load_dotenv

# Load env vars
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API_URL = "https://api.github.com"

def check_prs_with_labels():
    if not GITHUB_TOKEN:
        print("GITHUB_TOKEN not set")
        return

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Search for PRs
    query = "type:pr state:open review-requested:@me"
    print(f"Searching with query: {query}")
    
    resp = requests.get(
        f"{GITHUB_API_URL}/search/issues",
        headers=headers,
        params={"q": query}
    )
    
    if resp.status_code != 200:
        print(f"Error: {resp.status_code} - {resp.text}")
        return

    items = resp.json().get("items", [])
    print(f"Found {len(items)} PRs directly requested.")

    for item in items:
        title = item['title']
        labels = item.get('labels', [])
        print(f"PR: {title}")
        print(f"  Labels ({len(labels)}): {[l['name'] for l in labels]}")
        if labels:
            print(f"  First label color: {labels[0]['color']}")

if __name__ == "__main__":
    check_prs_with_labels()
