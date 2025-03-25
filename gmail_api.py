import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailClient:
    def __init__(self, credentials_file='credentials.json'):
        self.creds = None
        
        if os.path.exists('token.json'):
            try:
                self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            except Exception as e:
                print(f"Error loading token.json: {e}")
                self.creds = None

        # If no valid creds, do the manual console OAuth flow
        if not self.creds or not self.creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            flow.run_local_server(
                host='localhost',
                port=8080,
                authorization_prompt_message='Please visit this URL: {url}',
                success_message='The auth flow is complete; you may close this window.',
                open_browser=False  
            )

            self.creds = flow.credentials

            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

        try:
            self.service = build('gmail', 'v1', credentials=self.creds)
        except Exception as e:
            print(f"Error creating Gmail service: {e}")
            raise
    def get_receiver_email(self,payload:dict)->str:
        headers = payload.get("headers", [])
        for dict in headers:
            if dict.get("name") == "To":
                value = dict.get("value")
                return value
    def get_verification_code_and_receiver_email(self, sender_email):
        """
        Fetches the latest email from the given sender with the specified subject,
        extracts the first 6-digit numeric code from the email body, and returns it.
        """
        try:
            query = f'from:{sender_email}"'
            results = self.service.users().messages().list(
                userId='me',
                q=query
            ).execute()
        except Exception as e:
            print(f"Error fetching message list: {e}")
            return None,None
    
        if 'messages' not in results:
            print("No messages found matching the query.")
            return None,None
        
        try:
            latest_msg = results['messages'][0]
            msg = self.service.users().messages().get(
                userId='me',
                id=latest_msg['id']
            ).execute()
        except Exception as e:
            print(f"Error fetching message content: {e}")
            return None,None

        try:
            receiver_email = self.get_receiver_email(msg.get("payload",{}))
            print("Recciever Email to be added in Database",receiver_email)
            snippet = msg.get('snippet', {})
            code = ''.join(filter(str.isdigit, snippet))[:6]
            if code:
                print(f"Verification code found: {code}")
                return code,receiver_email
            else:
                print("No 6-digit code found in the email body.")
                return None,None
        except Exception as e:
            print(f"Error decoding or extracting verification code: {e}")
            return None,None
