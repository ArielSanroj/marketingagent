#!/usr/bin/env python3
"""
Google Ads API Refresh Token Generator

This script generates a refresh token for the Google Ads API.
Run this script and follow the instructions to complete the OAuth flow.
"""

import os
import sys
from google_auth_oauthlib.flow import InstalledAppFlow

# The OAuth 2.0 scopes to request
SCOPES = ['https://www.googleapis.com/auth/adwords']

def generate_refresh_token():
    """Generate a refresh token for Google Ads API."""
    
    # Load environment variables
    client_id = os.getenv('GOOGLE_ADS_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_ADS_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("Error: GOOGLE_ADS_CLIENT_ID and GOOGLE_ADS_CLIENT_SECRET must be set in .env file")
        print("Please update your .env file with your Google Ads API credentials.")
        return None
    
    # Create the flow
    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost:8080", "http://localhost:8081", "http://localhost:8082", "http://localhost:8083", "http://localhost:8084", "http://localhost:8085"]
            }
        },
        scopes=SCOPES
    )
    
    print("Starting OAuth flow...")
    print("A browser window will open for you to authorize the application.")
    print("Please log in with a Google account that has access to your Google Ads account.")
    print()
    print("IMPORTANT: Make sure to complete the authorization in your browser.")
    print("The script will wait for you to complete the OAuth flow.")
    print()
    
    try:
        # Run the OAuth flow
        credentials = flow.run_local_server(port=0, open_browser=True)
    except Exception as e:
        print(f"Error during OAuth flow: {e}")
        print("Please try again and make sure to complete the authorization in your browser.")
        return None
    
    # Extract the refresh token
    refresh_token = credentials.refresh_token
    
    print(f"Debug: Credentials object: {credentials}")
    print(f"Debug: Refresh token: {refresh_token}")
    
    if refresh_token:
        print("=" * 60)
        print("SUCCESS! Your refresh token has been generated:")
        print("=" * 60)
        print(f"GOOGLE_ADS_REFRESH_TOKEN={refresh_token}")
        print("=" * 60)
        print()
        print("Please add this refresh token to your .env file:")
        print(f"GOOGLE_ADS_REFRESH_TOKEN={refresh_token}")
        print()
        print("You can now use the Google Ads API with your credentials.")
    else:
        print("Error: No refresh token was generated.")
        return None
    
    return refresh_token

if __name__ == "__main__":
    # Load environment variables from .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("Warning: python-dotenv not installed. Make sure your environment variables are set.")
    
    generate_refresh_token()