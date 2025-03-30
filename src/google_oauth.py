# src/google_oauth.py
import os
import pickle
from pathlib import Path
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import streamlit as st

class GoogleOAuth:
    def __init__(self):
        self.scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive.metadata.readonly'
        ]
        self.token_file = Path('token.json')
        self.client_secret = Path('client_secret.json')  # You'll provide this file
        self.creds = None

    def authenticate(self):
        """Handles the entire OAuth flow"""
        # Check for existing token
        if self.token_file.exists():
            self.creds = Credentials.from_authorized_user_file(
                self.token_file, self.scopes
            )

        # If no valid credentials, run OAuth flow
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = Flow.from_client_secrets_file(
                    self.client_secret,
                    scopes=self.scopes,
                    redirect_uri='urn:ietf:wg:oauth:2.0:oob'
                )
                auth_url, _ = flow.authorization_url(prompt='consent')
                
                # Display auth URL to user
                st.markdown(f"""
                ### Google Authentication Required
                1. [Click here to authorize]({auth_url})
                2. Copy the authorization code
                3. Paste it below
                """)
                
                code = st.text_input("Authorization code")
                if st.button("Connect") and code:
                    with st.spinner("Authenticating..."):
                        flow.fetch_token(code=code)
                        self.creds = flow.credentials
                        # Save credentials
                        with open(self.token_file, 'w') as token:
                            token.write(self.creds.to_json())
                    st.success("Successfully authenticated!")
                    st.rerun()
                st.stop()  # Stop execution until authenticated
        
        return self.creds