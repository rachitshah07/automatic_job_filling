from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from gmail_api import GmailClient
import os
from dotenv import load_dotenv

load_dotenv('.env')
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "")
class ADPAutomator:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()  # Optional: maximize browser window
        self.wait = WebDriverWait(self.driver, 15)  # Adjust timeout as needed
        self.gmail = GmailClient()
    def open_registration_page(self, url):
        self.driver.get(url)
    def click_apply_button(self):
        """
        Clicks the 'APPLY' button on the job page.
        """
        apply_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "recruitment_jobDescription_apply"))
        )
        apply_button.click()
        # Wait until the registration page loads 
        self.wait.until(EC.presence_of_element_located((By.ID, "guestFirstName")))
    def fill_registration_form(self, first_name, last_name, email, mobile_number):
        """
        Fills out the personal info form fields and clicks 'Continue'.
        """
 
        first_name_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "guestFirstName"))
        )
        first_name_field.clear()
        first_name_field.send_keys(first_name)
        time.sleep(1)
  
        last_name_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "guestLastName"))
        )
        last_name_field.clear()
        last_name_field.send_keys(last_name)
        time.sleep(1)

        email_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "guestEmail"))
        )
        email_field.clear()
        email_field.send_keys(email)
        time.sleep(1)
        
        mobile_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "login_view_phone"))
        )
        mobile_field.click()
        mobile_field.send_keys(Keys.CONTROL, 'a')
        mobile_field.send_keys(Keys.BACKSPACE)
        # self.driver.execute_script("arguments[0].value = '';", mobile_field)
        mobile_field.send_keys(mobile_number)
        time.sleep(2)
        
        # Click Continue
        continue_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "recruitment_login_recaptcha"))
        )
        continue_button.click()

    def verify_email_code(self, email, timeout=120):
        """
        Waits for a verification code to arrive via Gmail, then enters it
        into the ADP verification field and proceeds.
        """
        try:
            time.sleep(10)
            start_time = time.time()
            code = None
            receiver_email = None
            
            while time.time() - start_time < timeout:
                try:
                    code, receiver_email = self.gmail.get_verification_code_and_receiver_email(sender_email=SENDER_EMAIL)
                    if code:
                        break
                except Exception as e:
                    print(f"Error fetching email verification code: {e}")
                
                time.sleep(5)  # Polling every 5 seconds
            
            if not code:
                raise Exception("Verification code not received within timeout.")

            if receiver_email != email:
                print(f"Receiver email does not match. Expected: {email}, Got: {receiver_email}")

            print(f"Verification code received: {code}")

            try:
                code_input = self.wait.until(
                    EC.presence_of_element_located((By.ID, "oneTimePassWord"))
                )
                time.sleep(2)
                code_input.clear()
                code_input.send_keys(code)
            except Exception as e:
                raise Exception(f"Error entering verification code: {e}")

            try:
                verify_button = self.wait.until(
                    EC.element_to_be_clickable((By.ID, "recruitment_login_verifyOTP"))
                )
                time.sleep(2)
                verify_button.click()
                time.sleep(5)
            except Exception as e:
                raise Exception(f"Error clicking verify button: {e}")

        except Exception as e:
            print(f"Email verification failed: {e}")
            self.driver.save_screenshot("email_verification_error.png")


    def close(self):
        if self.driver:
            self.driver.quit()

    def __del__(self):
        self.close()
