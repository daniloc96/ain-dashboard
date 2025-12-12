#!/usr/bin/env python3
"""
Google OAuth Token Generator

Run this script LOCALLY (not in Docker) to generate token.json:
    python generate_token.py

Prerequisites:
    pip install google-api-python-client google-auth-oauthlib
"""

import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# All required scopes for the dashboard
SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/gmail.readonly'
]

CREDENTIALS_PATH = 'credentials.json'
TOKEN_PATH = 'token.json'

def main():
    creds = None
    
    # Check if token already exists
    if os.path.exists(TOKEN_PATH):
        print(f"⚠️  {TOKEN_PATH} already exists!")
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        if creds and creds.valid:
            print("   Token is still valid.")
            print("   If you need to add new scopes, delete token.json and run again.")
            return
        elif creds and creds.expired and creds.refresh_token:
            print("   Token expired, refreshing...")
            try:
                creds.refresh(Request())
                with open(TOKEN_PATH, 'w') as token:
                    token.write(creds.to_json())
                print("   ✅ Token refreshed!")
                return
            except Exception as e:
                print(f"   ❌ Could not refresh: {e}")
                print("   Deleting old token and starting fresh...")
                os.remove(TOKEN_PATH)
    
    # Check if credentials.json exists
    if not os.path.exists(CREDENTIALS_PATH):
        print(f"❌ {CREDENTIALS_PATH} not found!")
        print("   Please download it from Google Cloud Console and place it in this directory.")
        return
    
    print("🔐 Starting OAuth flow...")
    print("   A browser window will open. Sign in with your Google account.")
    print()
    print("   Requesting permissions for:")
    print("   • Google Calendar (read)")
    print("   • Gmail (read)")
    print()
    
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
    creds = flow.run_local_server(port=0)
    
    # Save the credentials
    with open(TOKEN_PATH, 'w') as token:
        token.write(creds.to_json())
    
    print()
    print(f"✅ {TOKEN_PATH} created successfully!")
    print("   You can now run 'docker compose up' and the dashboard will work.")

if __name__ == '__main__':
    main()
