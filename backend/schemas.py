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

class GithubPR(BaseModel):
    title: str
    url: str
    repo: str
    author: str
    created_at: str
    state: str

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
