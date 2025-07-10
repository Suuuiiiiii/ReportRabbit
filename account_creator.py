from playwright.sync_api import sync_playwright
from mailtm import wait_for_verification_code
import random
import time

def generate_birthday():
    year = random.randint(1985, 2004)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return day, month, year

def create_account(email, token, full_name, password):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        try:
            page.goto("https://www.instagram.com/accounts/emailsignup/")
            page.wait_for_selector('input[name="emailOrPhone"]', timeout=15000)

            # Fill out the form
            page.fill('input[name="emailOrPhone"]', email)
            page.fill('input[name="fullName"]', full_name)
            page.fill('input[name="username"]', full_name.replace(" ", "") + str(random.randint(1000, 9999)))
            page.fill('input[name="password"]', password)

            page.click('button[type="submit"]')

            # Wait for DOB fields
            page.wait_for_selector('select[title="Month"]', timeout=10000)
            day, month, year = generate_birthday()
            page.select_option('select[title="Month"]', str(month))
            page.select_option('select[title="Day"]', str(day))
            page.select_option('select[title="Year"]', str(year))
            page.click('button[type="button"]:has-text("Next")')

            # Wait for verification code field
            page.wait_for_selector('input[name="email_confirmation_code"]', timeout=60000)

            # Poll for code
            code = wait_for_verification_code(token)
            if not code:
                print("[x] No code received.")
                return None

            page.fill('input[name="email_confirmation_code"]', code)
            page.click('button[type="submit"]')

            # Wait for main feed or profile redirect
            page.wait_for_load_state('networkidle', timeout=15000)

            # Extract session cookies
            cookies = context.cookies()
            session = {c['name']: c['value'] for c in cookies}

            username = page.url.split("/")[-2] if "instagram.com" in page.url else full_name.lower()

            return {
                "session": session,
                "username": username
            }

        except Exception as e:
            print(f"[x] Account creation error: {e}")
            return None

        finally:
            context.close()
            browser.close()
