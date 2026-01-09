import requests
import os
from typing import List, Set
from schemas import GithubPR

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API_URL = "https://api.github.com"

# Cache for user's teams (fetched once at startup)
_user_teams_cache: Set[str] = set()
_teams_fetched: bool = False


def _get_user_teams() -> Set[str]:
    """Fetch all teams the authenticated user belongs to."""
    global _user_teams_cache, _teams_fetched
    
    if _teams_fetched:
        return _user_teams_cache
    
    if not GITHUB_TOKEN:
        _teams_fetched = True
        return _user_teams_cache
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        # Get all teams the user belongs to across all organizations
        # This endpoint lists all teams for the authenticated user
        teams_response = requests.get(
            f"{GITHUB_API_URL}/user/teams",
            headers=headers,
            params={"per_page": 100}
        )
        teams_response.raise_for_status()
        
        teams = set()
        for team in teams_response.json():
            # Format: org/team-slug
            team_slug = f"{team['organization']['login']}/{team['slug']}"
            teams.add(team_slug)
        
        _user_teams_cache = teams
        _teams_fetched = True
        print(f"GitHub: Found {len(teams)} teams: {teams}")
        return teams
        
    except Exception as e:
        print(f"Error fetching user teams: {e}")
        # Don't cache failure, so we retry next time
        return _user_teams_cache


def get_review_requested_prs() -> List[GithubPR]:
    """Get PRs where review is requested from user or their teams."""
    if not GITHUB_TOKEN:
        print("Warning: GITHUB_TOKEN not set")
        return []

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    all_prs = {}  # Use dict to deduplicate by URL
    
    # 1. Get PRs with review requested from user directly
    try:
        query = "type:pr state:open review-requested:@me"
        response = requests.get(
            f"{GITHUB_API_URL}/search/issues",
            headers=headers,
            params={"q": query}
        )
        if response.status_code == 403 or response.status_code == 429:
             print(f"Rate limit exceeded fetching personal reviews: {response.text}")
        else:
            response.raise_for_status()
            
            for item in response.json().get("items", []):
                pr_url = item["html_url"]
                if pr_url not in all_prs:
                    all_prs[pr_url] = _parse_pr_item(item)
                
    except Exception as e:
        print(f"Error fetching personal review requests: {e}")
    
    # 2. Get PRs with review requested from user's teams
    # Batch queries to avoid rate limits
    teams = list(_get_user_teams())
    
    # Process in chunks of 5 teams to keep query length reasonable
    CHUNK_SIZE = 5
    for i in range(0, len(teams), CHUNK_SIZE):
        chunk = teams[i:i + CHUNK_SIZE]
        
        # specific team queries OR'd together
        # e.g. team-review-requested:org/team1 OR team-review-requested:org/team2
        team_queries = [f"team-review-requested:{team}" for team in chunk]
        combined_query = f"type:pr state:open {' '.join(team_queries)}"
        
        # If we have multiple teams, wrap the OR part in parentheses if needed? 
        # Actually GitHub search implicit AND between terms, but we can do:
        # type:pr state:open (team-review-requested:A OR team-review-requested:B)
        # But requests handles simple space as implicit AND.
        # Let's try explicit ORs for the team part.
        
        if len(chunk) > 1:
            teams_part = " OR ".join([f"team-review-requested:{t}" for t in chunk])
            query = f"type:pr state:open ( {teams_part} )"
        else:
            query = f"type:pr state:open team-review-requested:{chunk[0]}"
            
        try:
            print(f"GitHub: Searching team reviews with query: {query}")
            response = requests.get(
                f"{GITHUB_API_URL}/search/issues",
                headers=headers,
                params={"q": query}
            )
            
            if response.status_code == 403 or response.status_code == 429:
                 print(f"Rate limit exceeded fetching team reviews (chunk {i}): {response.text}")
                 continue
                 
            response.raise_for_status()
            
            items = response.json().get("items", [])
            print(f"GitHub: Found {len(items)} PRs for team chunk {i}")
            
            for item in items:
                pr_url = item["html_url"]
                if pr_url not in all_prs:
                    all_prs[pr_url] = _parse_pr_item(item)
                    
        except Exception as e:
            print(f"Error fetching team review requests for chunk {chunk}: {e}")
    
    # Sort by created_at descending
    prs = list(all_prs.values())
    prs.sort(key=lambda x: x.created_at, reverse=True)
    
    return prs


def _parse_pr_item(item: dict) -> GithubPR:
    """Parse a GitHub search result item into a GithubPR."""
    pr_url = item["html_url"]
    repo_url = item["repository_url"]
    repo_name = repo_url.split("repos/")[-1]
    
    labels = [{"name": l["name"], "color": l["color"]} for l in item.get("labels", [])]
    
    return GithubPR(
        title=item["title"],
        url=pr_url,
        repo=repo_name,
        author=item["user"]["login"],
        created_at=item["created_at"],
        state=item["state"],
        labels=labels
    )


def get_my_prs() -> List[GithubPR]:
    """Get open PRs created by the authenticated user."""
    if not GITHUB_TOKEN:
        print("Warning: GITHUB_TOKEN not set")
        return []

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        # Search for open PRs authored by the current user
        query = "type:pr state:open author:@me"
        response = requests.get(
            f"{GITHUB_API_URL}/search/issues",
            headers=headers,
            params={"q": query, "sort": "created", "order": "desc"}
        )
        response.raise_for_status()
        items = response.json().get("items", [])
        
        prs = []
        for item in items:
            # Get detailed PR info including mergeable status
            pr_api_url = item["pull_request"]["url"]
            pr_detail_response = requests.get(pr_api_url, headers=headers)
            pr_detail_response.raise_for_status()
            pr_detail = pr_detail_response.json()
            
            pr = _parse_pr_item(item)
            pr.mergeable = pr_detail.get("mergeable")
            pr.mergeable_state = pr_detail.get("mergeable_state")
            prs.append(pr)
        
        return prs
        
    except Exception as e:
        print(f"Error fetching my PRs: {e}")
        return []
