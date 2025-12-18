from fastapi import APIRouter
from typing import List
import schemas
from services import github_service

router = APIRouter(
    prefix="/api/v1/github",
    tags=["github"],
)

@router.get("/prs", response_model=List[schemas.GithubPR])
def get_prs():
    return github_service.get_review_requested_prs()

@router.get("/my-prs", response_model=List[schemas.GithubPR])
def get_my_prs():
    return github_service.get_my_prs()
