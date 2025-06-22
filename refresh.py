import os
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

TOKEN_PATH = 'YOUR_TOKEN_PATH'

# Add YouTube Live Streaming related scopes
SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/youtube',
    'https://www.googleapis.com/auth/youtube.readonly'  # Optional, broader scope
]

def refresh_token():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, scopes=SCOPES)

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
        print("Token refreshed.")
    else:
        print("Token is still valid.")

if __name__ == "__main__":
    refresh_token()
