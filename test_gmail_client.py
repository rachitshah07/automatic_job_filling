import unittest
from gmail_api import GmailClient
from dotenv import load_dotenv
import os
load_dotenv('.env')
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "")
class TestGmailClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Called once before running any tests in this class.
        Initializes the GmailClient with the specified credentials file.
        """
        cls.client = GmailClient(credentials_file='credentials.json')

    def test_get_verification_code(self):
        """
        Test if we can successfully fetch a verification code from the latest email
        sent by 'SecurityServices_NoReply@adp.com'.
        """
        code = self.client.get_verification_code_and_receiver_email(sender_email=SENDER_EMAIL)
        self.assertIsNotNone(code, "Verification code should not be None if the email exists.")
        print(f"\nFetched verification code: {code}")

if __name__ == '__main__':
    unittest.main()
