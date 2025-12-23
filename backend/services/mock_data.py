"""
Mock data service for demo mode.

When DEMO_MODE=true, the API returns realistic but fictional data
for taking screenshots without exposing personal information.
"""

import os
from datetime import datetime, timedelta
from typing import List
import schemas

def is_demo_mode() -> bool:
    """Check if demo mode is enabled via environment variable."""
    return os.getenv("DEMO_MODE", "false").lower() == "true"


# =============================================================================
# MOCK TODOS
# =============================================================================

def get_mock_todos() -> List[dict]:
    """Return mock todos for demo mode."""
    return [
        {"id": 1, "title": "Review PR for authentication refactor", "completed": True, "order": 0},
        {"id": 2, "title": "Update API documentation", "completed": False, "order": 1},
        {"id": 3, "title": "Fix memory leak in worker service", "completed": False, "order": 2},
        {"id": 4, "title": "Prepare sprint retrospective slides", "completed": False, "order": 3},
        {"id": 5, "title": "Deploy v2.3.0 to staging", "completed": False, "order": 4},
        {"id": 6, "title": "Write unit tests for payment module", "completed": True, "order": 5},
    ]


# =============================================================================
# MOCK GITHUB PRS (Review Requested)
# =============================================================================

def get_mock_github_prs() -> List[schemas.GithubPR]:
    """Return mock GitHub PRs where review is requested."""
    now = datetime.utcnow()
    
    return [
        schemas.GithubPR(
            title="feat: Add OAuth2 support for third-party integrations",
            url="https://github.com/acme-corp/backend-api/pull/1234",
            repo="acme-corp/backend-api",
            author="sarah-dev",
            created_at=(now - timedelta(hours=2)).isoformat() + "Z",
            state="open",
            labels=[
                schemas.GithubLabel(name="feature", color="0e8a16"),
                schemas.GithubLabel(name="needs-review", color="fbca04"),
            ],
            mergeable=True,
            mergeable_state="clean"
        ),
        schemas.GithubPR(
            title="fix: Resolve race condition in cache invalidation",
            url="https://github.com/acme-corp/cache-service/pull/89",
            repo="acme-corp/cache-service",
            author="mike-engineer",
            created_at=(now - timedelta(hours=5)).isoformat() + "Z",
            state="open",
            labels=[
                schemas.GithubLabel(name="bug", color="d73a4a"),
                schemas.GithubLabel(name="priority: high", color="b60205"),
            ],
            mergeable=True,
            mergeable_state="clean"
        ),
        schemas.GithubPR(
            title="refactor: Migrate database queries to async",
            url="https://github.com/acme-corp/data-layer/pull/456",
            repo="acme-corp/data-layer",
            author="alex-backend",
            created_at=(now - timedelta(days=1)).isoformat() + "Z",
            state="open",
            labels=[
                schemas.GithubLabel(name="refactor", color="5319e7"),
                schemas.GithubLabel(name="performance", color="0052cc"),
            ],
            mergeable=True,
            mergeable_state="clean"
        ),
    ]


# =============================================================================
# MOCK MY PRS (PRs I Created)
# =============================================================================

def get_mock_my_prs() -> List[schemas.GithubPR]:
    """Return mock GitHub PRs created by the user."""
    now = datetime.utcnow()
    
    return [
        schemas.GithubPR(
            title="feat: Implement real-time notifications via WebSocket",
            url="https://github.com/acme-corp/frontend-app/pull/567",
            repo="acme-corp/frontend-app",
            author="demo-user",
            created_at=(now - timedelta(hours=3)).isoformat() + "Z",
            state="open",
            labels=[
                schemas.GithubLabel(name="feature", color="0e8a16"),
                schemas.GithubLabel(name="frontend", color="1d76db"),
            ],
            mergeable=True,
            mergeable_state="clean"
        ),
        schemas.GithubPR(
            title="docs: Update README with deployment instructions",
            url="https://github.com/acme-corp/infrastructure/pull/123",
            repo="acme-corp/infrastructure",
            author="demo-user",
            created_at=(now - timedelta(days=2)).isoformat() + "Z",
            state="open",
            labels=[
                schemas.GithubLabel(name="documentation", color="0075ca"),
            ],
            mergeable=True,
            mergeable_state="clean"
        ),
    ]


# =============================================================================
# MOCK JIRA TASKS
# =============================================================================

def get_mock_jira_tasks() -> List[schemas.JiraIssue]:
    """Return mock Jira issues assigned to the user."""
    return [
        schemas.JiraIssue(
            key="PROJ-1234",
            summary="Implement user dashboard analytics",
            status="In Progress",
            priority="High",
            assignee="Demo User",
            url="https://acme-corp.atlassian.net/browse/PROJ-1234"
        ),
        schemas.JiraIssue(
            key="PROJ-1189",
            summary="Fix login redirect loop on Safari",
            status="In Progress",
            priority="Highest",
            assignee="Demo User",
            url="https://acme-corp.atlassian.net/browse/PROJ-1189"
        ),
        schemas.JiraIssue(
            key="PROJ-1156",
            summary="Add export to CSV feature for reports",
            status="To Do",
            priority="Medium",
            assignee="Demo User",
            url="https://acme-corp.atlassian.net/browse/PROJ-1156"
        ),
        schemas.JiraIssue(
            key="PROJ-1098",
            summary="Optimize image compression pipeline",
            status="In Progress",
            priority="Medium",
            assignee="Demo User",
            url="https://acme-corp.atlassian.net/browse/PROJ-1098"
        ),
        schemas.JiraIssue(
            key="PROJ-1045",
            summary="Review and update API rate limiting",
            status="To Do",
            priority="Low",
            assignee="Demo User",
            url="https://acme-corp.atlassian.net/browse/PROJ-1045"
        ),
    ]


# =============================================================================
# MOCK CALENDAR EVENTS
# =============================================================================

def get_mock_calendar_events() -> List[schemas.CalendarEvent]:
    """Return mock calendar events for today."""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    return [
        schemas.CalendarEvent(
            summary="Daily Standup",
            start_time=(today.replace(hour=9, minute=30)).isoformat(),
            end_time=(today.replace(hour=9, minute=45)).isoformat(),
            location="Zoom",
            html_link="https://calendar.google.com/calendar/event?eid=demo1"
        ),
        schemas.CalendarEvent(
            summary="Sprint Planning",
            start_time=(today.replace(hour=10, minute=0)).isoformat(),
            end_time=(today.replace(hour=11, minute=30)).isoformat(),
            location="Conference Room A",
            html_link="https://calendar.google.com/calendar/event?eid=demo2"
        ),
        schemas.CalendarEvent(
            summary="1:1 with Engineering Manager",
            start_time=(today.replace(hour=14, minute=0)).isoformat(),
            end_time=(today.replace(hour=14, minute=30)).isoformat(),
            location="Google Meet",
            html_link="https://calendar.google.com/calendar/event?eid=demo3"
        ),
        schemas.CalendarEvent(
            summary="Code Review Session",
            start_time=(today.replace(hour=15, minute=30)).isoformat(),
            end_time=(today.replace(hour=16, minute=30)).isoformat(),
            location=None,
            html_link="https://calendar.google.com/calendar/event?eid=demo4"
        ),
        schemas.CalendarEvent(
            summary="Team Retrospective",
            start_time=(today.replace(hour=17, minute=0)).isoformat(),
            end_time=(today.replace(hour=18, minute=0)).isoformat(),
            location="Zoom",
            html_link="https://calendar.google.com/calendar/event?eid=demo5"
        ),
    ]


# =============================================================================
# MOCK GMAIL UNREAD COUNT
# =============================================================================

def get_mock_gmail_unread_count() -> int:
    """Return mock unread email count."""
    return 12


# =============================================================================
# MOCK GOOGLE AUTH STATUS
# =============================================================================

def get_mock_google_auth_status() -> schemas.GoogleAuthStatus:
    """Return mock Google auth status (always authorized in demo mode)."""
    return schemas.GoogleAuthStatus(
        status="authorized",
        message="Demo mode - Google account simulated as authorized",
        auth_url=None
    )
