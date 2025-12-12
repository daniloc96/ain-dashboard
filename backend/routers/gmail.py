from fastapi import APIRouter
from schemas import GmailUnreadCount
from services import gmail_service

router = APIRouter(prefix="/api/v1/gmail", tags=["gmail"])


@router.get("/unread", response_model=GmailUnreadCount)
def get_unread_count():
    """Get the count of unread emails in inbox."""
    count = gmail_service.get_unread_count()
    return GmailUnreadCount(count=count)
