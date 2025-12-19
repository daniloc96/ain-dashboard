from pydantic import BaseModel
from typing import List

class TodoBase(BaseModel):
    title: str
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int
    order: int = 0

    class Config:
        orm_mode = True

class TodoReorder(BaseModel):
    """Schema for reordering todos - list of todo IDs in new order."""
    order: List[int]

class GithubLabel(BaseModel):
    name: str
    color: str

class GithubPR(BaseModel):
    title: str
    url: str
    repo: str
    author: str
    created_at: str
    state: str
    labels: List[GithubLabel] = []
    mergeable: bool | None = None
    mergeable_state: str | None = None

class JiraIssue(BaseModel):
    key: str
    summary: str
    status: str
    priority: str
    assignee: str
    url: str

class CalendarEvent(BaseModel):
    summary: str
    start_time: str
    end_time: str
    location: str | None = None
    html_link: str

class GmailUnreadCount(BaseModel):
    count: int

class GoogleAuthStatus(BaseModel):
    status: str
    message: str
    auth_url: str | None = None
