from pydantic import BaseModel

class TodoBase(BaseModel):
    title: str
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int

    class Config:
        orm_mode = True

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
