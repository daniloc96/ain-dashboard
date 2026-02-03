"""
One-off script to test Jira API: prints JQL, calls each domain, shows response or error.
Run from repo root: python backend/debug_jira.py
"""
import os
import sys
import requests
from requests.auth import HTTPBasicAuth

# Load .env from project root (parent of backend)
try:
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent
    env_path = root / ".env"
except Exception:
    env_path = ".env"

def load_env():
    try:
        from dotenv import load_dotenv
        load_dotenv(env_path)
    except ImportError:
        pass

load_env()

JIRA_DOMAINS = os.getenv("JIRA_DOMAINS", os.getenv("JIRA_DOMAIN", "")).strip('"\'')
JIRA_EMAIL = os.getenv("JIRA_EMAIL", "").strip('"\'')
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN", "").strip('"\'')

def main():
    print("=== Jira API debug ===\n")
    if not JIRA_DOMAINS:
        print("JIRA_DOMAINS (or JIRA_DOMAIN) not set")
        sys.exit(1)
    if not JIRA_EMAIL:
        print("JIRA_EMAIL not set")
        sys.exit(1)
    if not JIRA_API_TOKEN:
        print("JIRA_API_TOKEN not set")
        sys.exit(1)

    domains = [d.strip() for d in JIRA_DOMAINS.split(",") if d.strip()]
    print(f"Domains: {domains}\n")

    status_env = os.getenv("JIRA_TASK_STATUS_ENABLED", "In Progress").strip('"\'')
    statuses = [f'"{s.strip()}"' for s in status_env.split(",") if s.strip()]
    status_str = ",".join(statuses) if statuses else '"In Progress"'

    project_keys_env = os.getenv("JIRA_PROJECT_KEYS", "").strip('"\'')
    project_filter = ""
    if project_keys_env:
        keys = [k.strip() for k in project_keys_env.split(",") if k.strip()]
        if keys:
            keys_quoted = [f'"{k}"' for k in keys]
            project_filter = f" AND project in ({','.join(keys_quoted)})"

    jql = f"assignee = currentUser() AND status in ({status_str}){project_filter} ORDER BY priority DESC, updated DESC"
    print(f"JQL:\n{jql}\n")

    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
    headers = {"Accept": "application/json"}
    params = {"jql": jql, "fields": "summary,status,priority,assignee", "maxResults": 100}

    total = 0
    for domain in domains:
        url = f"https://{domain}/rest/api/3/search/jql"
        print(f"Domain: {domain}")
        try:
            r = requests.get(url, headers=headers, params=params, auth=auth)
            print(f"  Status: {r.status_code}")
            if not r.ok:
                print(f"  Body: {r.text[:500]}")
                continue
            data = r.json()
            issues = data.get("issues", [])
            total_issues = data.get("total", len(issues))
            total += len(issues)
            print(f"  Total (Jira): {total_issues}, returned: {len(issues)}")
            for i, issue in enumerate(issues[:5]):
                key = issue.get("key", "?")
                summary = (issue.get("fields") or {}).get("summary", "")[:50]
                print(f"    - {key}: {summary}...")
            if len(issues) > 5:
                print(f"    ... and {len(issues) - 5} more")
        except Exception as e:
            print(f"  Error: {e}")
        print()

    print(f"=== Total issues across domains: {total} ===")

if __name__ == "__main__":
    main()
