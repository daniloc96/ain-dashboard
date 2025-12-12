import os
from typing import Optional

# Google API imports
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Shared Google API configuration
SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/gmail.readonly'
]

CREDENTIALS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH', '/app/credentials.json')
TOKEN_PATH = os.getenv('GOOGLE_TOKEN_PATH', '/app/token.json')


def get_credentials() -> Optional[Credentials]:
    """Get or refresh Google API credentials. Shared by all Google services."""
    creds = None
    
    # Check if token.json exists (saved authorization)
    if os.path.exists(TOKEN_PATH):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        except Exception as e:
            print(f"Error loading token.json: {e}")
            creds = None
    
    # If no valid credentials, try to get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing credentials: {e}")
                creds = None
        
        # If still no creds, need to run OAuth flow
        if not creds:
            if os.path.exists(CREDENTIALS_PATH):
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
                    creds = flow.run_local_server(port=0)
                except Exception as e:
                    print(f"Error running OAuth flow: {e}")
                    return None
            else:
                print(f"credentials.json not found at {CREDENTIALS_PATH}")
                return None
        
        # Save the credentials for future use
        if creds:
            try:
                with open(TOKEN_PATH, 'w') as token:
                    token.write(creds.to_json())
            except Exception as e:
                print(f"Warning: Could not save token.json: {e}")
    
    return creds
