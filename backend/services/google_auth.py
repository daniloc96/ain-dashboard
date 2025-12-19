import os
from typing import Optional
from enum import Enum
import json

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


class AuthStatus(str, Enum):
    """Google OAuth authorization status"""
    AUTHORIZED = "authorized"
    EXPIRED = "expired"
    NOT_CONFIGURED = "not_configured"


def get_auth_status() -> AuthStatus:
    """Check current Google authorization, attempting a silent refresh if possible."""
    if not os.path.exists(TOKEN_PATH):
        return AuthStatus.NOT_CONFIGURED

    try:
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        if creds and creds.valid:
            return AuthStatus.AUTHORIZED
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                # Persist refreshed token
                save_credentials(creds)
                return AuthStatus.AUTHORIZED
            except Exception as refresh_err:
                print(f"Auth status refresh failed: {refresh_err}")
                return AuthStatus.EXPIRED
        # Either expired without refresh or invalid
        return AuthStatus.EXPIRED
    except Exception as e:
        print(f"Error checking auth status: {e}")
        return AuthStatus.NOT_CONFIGURED


# Global variable to store the flow for callback
_oauth_flow = None


def get_authorization_url(redirect_uri: str) -> Optional[str]:
    """Get the OAuth authorization URL with proper redirect_uri."""
    global _oauth_flow
    
    if not os.path.exists(CREDENTIALS_PATH):
        return None
    
    try:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
        
        # Set the redirect URI for web-based flow
        flow.redirect_uri = redirect_uri
        
        # Get the authorization URL
        auth_uri, state = flow.authorization_url(access_type='offline', prompt='consent')
        
        # Store the flow for later use in the callback
        _oauth_flow = flow
        
        return auth_uri
    except Exception as e:
        print(f"Authorization URL generation failed: {e}")
        return None


def handle_oauth_callback(code: str) -> bool:
    """Handle OAuth callback by exchanging code for credentials."""
    global _oauth_flow
    
    if _oauth_flow is None:
        return False
    
    try:
        # Exchange the authorization code for credentials
        _oauth_flow.fetch_token(code=code)
        creds_obj = _oauth_flow.credentials

        # Save the credentials
        success = save_credentials(creds_obj)
        return success
    except Exception as e:
        print(f"OAuth callback error: {e}")
        return False


def save_credentials(credentials) -> bool:
    """Save credentials to token.json in authorized_user format expected by Google libs.

    The file must include client_id and client_secret in addition to refresh_token.
    """
    try:
        # Load client_id and client_secret from the installed app credentials file
        with open(CREDENTIALS_PATH, 'r') as f:
            client_cfg = json.load(f)
        installed = client_cfg.get('installed') or client_cfg.get('web') or {}
        client_id = installed.get('client_id')
        client_secret = installed.get('client_secret')

        if not client_id or not client_secret:
            raise RuntimeError('Missing client_id/client_secret in credentials.json')

        # Normalize to dict fields
        if isinstance(credentials, Credentials):
            data = {
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": credentials.refresh_token,
                "token": credentials.token,
                "scopes": credentials.scopes,
                "type": "authorized_user",
            }
        elif isinstance(credentials, dict):
            # Ensure required fields present
            data = {
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": credentials.get("refresh_token"),
                "token": credentials.get("access_token") or credentials.get("token"),
                "scopes": SCOPES,
                "type": "authorized_user",
            }
        else:
            # Fallback attempt to serialize
            data = {
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": getattr(credentials, 'refresh_token', None),
                "token": getattr(credentials, 'token', None),
                "scopes": SCOPES,
                "type": "authorized_user",
            }

        # Basic validation
        # (No verbose warnings in normal runtime)

        with open(TOKEN_PATH, 'w') as token_file:
            json.dump(data, token_file)

        return True
    except Exception as e:
        print(f"Error saving credentials: {e}")
        return False


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
            save_credentials(creds)
    
    return creds
