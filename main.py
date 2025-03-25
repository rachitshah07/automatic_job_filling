from adp_automator import ADPAutomator
import config
import os
from dotenv import load_dotenv

load_dotenv('.env')
def main():
    automator = ADPAutomator()
    try:
        registration_url = os.environ.get("REGISTRATION_URL", "")
        automator.open_registration_page(registration_url)
        automator.click_apply_button()
        automator.fill_registration_form(first_name=config.ADP_CREDENTIALS['first_name'],last_name=config.ADP_CREDENTIALS['last_name'],email=config.ADP_CREDENTIALS['email'],mobile_number=config.ADP_CREDENTIALS['mobile_number'])
        automator.verify_email_code(email = config.ADP_CREDENTIALS["email"])
    except Exception as e:
        print(f"Automation failed: {str(e)}")

if __name__ == "__main__":
    main()