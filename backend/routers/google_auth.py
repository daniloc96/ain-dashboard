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
def google_oauth_callback(
    code: str = Query(None),
    error: str = Query(None),
    error_description: str = Query(None)
):
    """Handle OAuth callback from Google."""
    # Handle error responses from Google (e.g., user denied access)
    if error:
        error_msg = error_description or error
        return f"""
        <html>
            <head>
                <title>Authorization Denied</title>
                <style>
                    body {{ font-family: system-ui; display: flex; align-items: center; justify-content: center; height: 100vh; background: #1a1a1a; color: white; }}
                    .container {{ text-align: center; background: #2a2a2a; padding: 40px; border-radius: 10px; max-width: 400px; }}
                    h1 {{ color: #f59e0b; margin: 0 0 20px 0; }}
                    p {{ margin: 0 0 20px 0; }}
                    .error {{ color: #9ca3af; font-size: 14px; }}
                    button {{ background: #6b7280; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 16px; }}
                    button:hover {{ background: #4b5563; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>⚠ Authorization Denied</h1>
                    <p>Access was not granted to your Google account.</p>
                    <p class="error">{error_msg}</p>
                    <p>Please close this window and try again if you want to enable Calendar and Gmail widgets.</p>
                    <button onclick="window.close()">Close Window</button>
                </div>
            </body>
        </html>
        """
    
    # Handle missing code (shouldn't happen if no error, but just in case)
    if not code:
        return """
        <html>
            <head>
                <title>Invalid Request</title>
                <style>
                    body { font-family: system-ui; display: flex; align-items: center; justify-content: center; height: 100vh; background: #1a1a1a; color: white; }
                    .container { text-align: center; background: #2a2a2a; padding: 40px; border-radius: 10px; }
                    h1 { color: #ef4444; margin: 0 0 20px 0; }
                    button { background: #6b7280; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 16px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>✗ Invalid Request</h1>
                    <p>No authorization code received.</p>
                    <button onclick="window.close()">Close Window</button>
                </div>
            </body>
        </html>
        """
    
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
