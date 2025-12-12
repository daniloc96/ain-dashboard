import os
from typing import Optional
from googleapiclient.discovery import build
from services.google_auth import get_credentials, CREDENTIALS_PATH, TOKEN_PATH


def get_unread_count() -> int:
    """Fetch the count of unread emails in the inbox using labels.get API."""
    
    # Check if credentials file exists
    if not os.path.exists(CREDENTIALS_PATH) and not os.path.exists(TOKEN_PATH):
        print("Google not configured. Returning 0 unread.")
        return 0
    
    try:
        creds = get_credentials()
        if not creds:
            print("Could not get Google credentials. Returning 0 unread.")
            return 0
        
        # Build the Gmail API service
        service = build('gmail', 'v1', credentials=creds)
        
        # Use labels.get to get the exact unread count for INBOX label
        # This matches what Gmail shows in the sidebar
        label_info = service.users().labels().get(
            userId='me',
            id='INBOX'
        ).execute()
        
        # Get the unread message count directly from the label
        unread_count = label_info.get('messagesUnread', 0)
        
        return unread_count
        
    except Exception as e:
        print(f"Error fetching Gmail unread count: {e}")
        return 0
