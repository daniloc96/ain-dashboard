from fastapi import APIRouter
from schemas import GmailUnreadCount
from services import gmail_service
from services.mock_data import is_demo_mode, get_mock_gmail_unread_count

router = APIRouter(prefix="/api/v1/gmail", tags=["gmail"])


@router.get("/unread", response_model=GmailUnreadCount)
def get_unread_count():
    """Get the count of unread emails in inbox."""
    if is_demo_mode():
        return GmailUnreadCount(count=get_mock_gmail_unread_count())
    count = gmail_service.get_unread_count()
    return GmailUnreadCount(count=count)
