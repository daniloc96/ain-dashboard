from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from schemas import GoogleAuthStatus
from services.google_auth import get_auth_status, get_authorization_url, handle_oauth_callback, AuthStatus
from services.mock_data import is_demo_mode, get_mock_google_auth_status
import os

router = APIRouter(prefix="/api/v1/google", tags=["google"])

# Get the base URL from environment, default to localhost for local dev
BASE_URL = os.getenv('NEXT_PUBLIC_API_URL', 'http://localhost:8001')
REDIRECT_URI = f"{BASE_URL}/api/v1/google/callback"


@router.get("/auth-status", response_model=GoogleAuthStatus)
def get_google_auth_status():
    """Get current Google OAuth authorization status."""
    if is_demo_mode():
        return get_mock_google_auth_status()
    status = get_auth_status()
    
    if status == AuthStatus.AUTHORIZED:
        return GoogleAuthStatus(
            status="authorized",
            message="Google account is authorized"
        )
    elif status == AuthStatus.EXPIRED:
        auth_url = get_authorization_url(REDIRECT_URI)
        return GoogleAuthStatus(
            status="expired",
            message="Google token has expired. Please re-authorize.",
            auth_url=auth_url
        )
    else:
        auth_url = get_authorization_url(REDIRECT_URI)
        return GoogleAuthStatus(
            status="not_configured",
            message="Google account is not configured",
            auth_url=auth_url
        )


@router.get("/callback", response_class=HTMLResponse)
def google_oauth_callback(code: str = Query(...)):
    """Handle OAuth callback from Google."""
    try:
        # Exchange the code for credentials
        success = handle_oauth_callback(code)
        
        if success:
            return """
            <html>
                <head>
                    <title>Authorization Successful</title>
                    <style>
                        body { font-family: system-ui; display: flex; align-items: center; justify-content: center; height: 100vh; background: #1a1a1a; color: white; }
                        .container { text-align: center; background: #2a2a2a; padding: 40px; border-radius: 10px; }
                        h1 { color: #4ade80; margin: 0 0 20px 0; }
                        p { margin: 0 0 20px 0; }
                        button { background: #0ea5e9; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 16px; }
                        button:hover { background: #0284c7; }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>✓ Authorization Successful!</h1>
                        <p>Your Google account has been authorized.</p>
                        <p>You can close this window and return to the dashboard.</p>
                        <button onclick="window.close()">Close Window</button>
                        <script>
                            // Auto-close after 3 seconds
                            setTimeout(() => window.close(), 3000);
                        </script>
                    </div>
                </body>
            </html>
            """
        else:
            return """
            <html>
                <head>
                    <title>Authorization Failed</title>
                    <style>
                        body { font-family: system-ui; display: flex; align-items: center; justify-content: center; height: 100vh; background: #1a1a1a; color: white; }
                        .container { text-align: center; background: #2a2a2a; padding: 40px; border-radius: 10px; }
                        h1 { color: #ef4444; margin: 0 0 20px 0; }
                        p { margin: 0 0 20px 0; }
                        button { background: #ef4444; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 16px; }
                        button:hover { background: #dc2626; }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>✗ Authorization Failed</h1>
                        <p>There was an error saving your authorization.</p>
                        <p>Please try again.</p>
                        <button onclick="window.close()">Close Window</button>
                    </div>
                </body>
            </html>
            """
    except Exception as e:
        print(f"Error in callback: {e}")
        return f"""
        <html>
            <head>
                <title>Error</title>
                <style>
                    body {{ font-family: system-ui; display: flex; align-items: center; justify-content: center; height: 100vh; background: #1a1a1a; color: white; }}
                    .container {{ text-align: center; background: #2a2a2a; padding: 40px; border-radius: 10px; }}
                    h1 {{ color: #ef4444; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Error</h1>
                    <p>{str(e)}</p>
                </div>
            </body>
        </html>
        """
