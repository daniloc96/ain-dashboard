from fastapi import APIRouter
from typing import List
import schemas
from services import github_service
from services.mock_data import is_demo_mode, get_mock_github_prs, get_mock_my_prs

router = APIRouter(
    prefix="/api/v1/github",
    tags=["github"],
)

@router.get("/prs", response_model=List[schemas.GithubPR])
def get_prs():
    if is_demo_mode():
        return get_mock_github_prs()
    return github_service.get_review_requested_prs()

@router.get("/my-prs", response_model=List[schemas.GithubPR])
def get_my_prs():
    if is_demo_mode():
        return get_mock_my_prs()
    return github_service.get_my_prs()
