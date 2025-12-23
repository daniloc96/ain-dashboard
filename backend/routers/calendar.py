from fastapi import APIRouter
from typing import List
import schemas
from services import calendar_service
from services.mock_data import is_demo_mode, get_mock_calendar_events

router = APIRouter(
    prefix="/api/v1/calendar",
    tags=["calendar"],
)

@router.get("/events", response_model=List[schemas.CalendarEvent])
def get_events():
    if is_demo_mode():
        return get_mock_calendar_events()
    return calendar_service.get_todays_events()
