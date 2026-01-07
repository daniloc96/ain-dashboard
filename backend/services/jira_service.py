import requests
import os
from typing import List
from schemas import JiraIssue
from requests.auth import HTTPBasicAuth

# Support comma-separated domains: "domain1.atlassian.net,domain2.atlassian.net"
# Parse comma-separated domains and strip quotes
JIRA_DOMAINS = os.getenv("JIRA_DOMAINS", os.getenv("JIRA_DOMAIN", "")).strip('"\'')
JIRA_EMAIL = os.getenv("JIRA_EMAIL", "").strip('"\'')
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN", "").strip('"\'')

def get_my_tasks() -> List[JiraIssue]:
    if not (JIRA_DOMAINS and JIRA_EMAIL and JIRA_API_TOKEN):
        return []

    # Parse comma-separated domains
    domains = [d.strip() for d in JIRA_DOMAINS.split(",") if d.strip()]
    
    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
    headers = {"Accept": "application/json"}

    # Read status filter and strip potential quotes
    status_env = os.getenv("JIRA_TASK_STATUS_ENABLED", "In Progress").strip('"\'')
    statuses = [f'"{s.strip()}"' for s in status_env.split(",") if s.strip()]
    status_str = ",".join(statuses) if statuses else '"In Progress"'

    jql = f"assignee = currentUser() AND status in ({status_str}) ORDER BY priority DESC, updated DESC"
    
    params = {
        "jql": jql,
        "fields": "summary,status,priority,assignee"
    }

    all_issues = []
    
    for domain in domains:
        try:
            url = f"https://{domain}/rest/api/3/search/jql"
            response = requests.get(url, headers=headers, params=params, auth=auth)
            response.raise_for_status()
            data = response.json()
            
            for item in data.get("issues", []):
                fields = item.get("fields") or {}
                
                prio_obj = fields.get("priority")
                priority = prio_obj.get("name", "Unknown") if prio_obj else "Unknown"
                
                status_obj = fields.get("status")
                status = status_obj.get("name", "Unknown") if status_obj else "Unknown"
                
                assignee_obj = fields.get("assignee")
                assignee_name = assignee_obj.get("displayName", "Unassigned") if assignee_obj else "Unassigned"
                
                all_issues.append(JiraIssue(
                    key=item["key"],
                    summary=fields.get("summary", ""),
                    status=status,
                    priority=priority,
                    assignee=assignee_name,
                    url=f"https://{domain}/browse/{item['key']}"
                ))
                
        except Exception as e:
            print(f"Error fetching Jira issues from {domain}: {e}")
            # Continue to next domain even if one fails
            continue
    
    return all_issues
