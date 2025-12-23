from fastapi import APIRouter
from typing import List
import schemas
from services import jira_service
from services.mock_data import is_demo_mode, get_mock_jira_tasks

router = APIRouter(
    prefix="/api/v1/jira",
    tags=["jira"],
)

@router.get("/tasks", response_model=List[schemas.JiraIssue])
async def read_jira_tasks():
    if is_demo_mode():
        return get_mock_jira_tasks()
    return jira_service.get_my_tasks()
