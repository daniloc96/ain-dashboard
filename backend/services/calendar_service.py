from datetime import datetime, timedelta
from typing import List
from schemas import CalendarEvent
from services.google_auth import get_credentials, CREDENTIALS_PATH, TOKEN_PATH
from googleapiclient.discovery import build
import os


def get_todays_events() -> List[CalendarEvent]:
    """Fetch today's events from Google Calendar."""
    
    # Check if credentials file exists
    if not os.path.exists(CREDENTIALS_PATH) and not os.path.exists(TOKEN_PATH):
        print("Google Calendar not configured. Using mock data.")
        return _get_mock_events()
    
    try:
        creds = get_credentials()
        if not creds:
            print("Could not get Google credentials. Using mock data.")
            return _get_mock_events()
        
        # Build the Calendar API service
        service = build('calendar', 'v3', credentials=creds)
        
        # Get today's time range (UTC)
        now = datetime.utcnow()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        
        time_min = start_of_day.isoformat() + 'Z'
        time_max = end_of_day.isoformat() + 'Z'
        
        # Fetch events
        events_result = service.events().list(
            calendarId='primary',
            timeMin=time_min,
            timeMax=time_max,
            maxResults=20,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        calendar_events = []
        for event in events:
            # Handle all-day events vs timed events
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            
            calendar_events.append(CalendarEvent(
                summary=event.get('summary', 'No title'),
                start_time=start,
                end_time=end,
                location=event.get('location', ''),
                html_link=event.get('htmlLink', '')
            ))
        
        return calendar_events
        
    except Exception as e:
        print(f"Error fetching calendar events: {e}")
        return _get_mock_events()


def _get_mock_events() -> List[CalendarEvent]:
    """Return mock events when Google Calendar is not configured."""
    now = datetime.now()
    
    return [
        CalendarEvent(
            summary="Daily Standup",
            start_time=(now.replace(hour=10, minute=0)).isoformat(),
            end_time=(now.replace(hour=10, minute=30)).isoformat(),
            location="Google Meet",
            html_link="https://calendar.google.com"
        ),
        CalendarEvent(
            summary="Team Lunch",
            start_time=(now.replace(hour=13, minute=0)).isoformat(),
            end_time=(now.replace(hour=14, minute=0)).isoformat(),
            location="Office Kitchen",
            html_link="https://calendar.google.com"
        ),
        CalendarEvent(
            summary="Project Review",
            start_time=(now.replace(hour=15, minute=30)).isoformat(),
            end_time=(now.replace(hour=16, minute=30)).isoformat(),
            location="Meeting Room A",
            html_link="https://calendar.google.com"
        )
    ]
