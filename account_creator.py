from playwright.sync_api import sync_playwright
import time
import random
from mailtm import wait_for_code

def create_account(email, token, full_name, password):
    birth_day = str(random.randint(1, 28))
    birth_month = str(random.randint(1, 12))
    birth_year = str(random.randint(1995, 2003))  # Must be 18+

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            print("[*] Navigating to signup page...")
            page.goto("https://www.instagram.com/accounts/emailsignup/", timeout=60000)
            page.wait_for_load_state("networkidle")

            # Fill the form
            page.fill('input[name="emailOrPhone"]', email)
            page.fill('input[name="fullName"]', full_name)
            page.fill('input[name="username"]', full_name.lower().replace(" ", "") + str(random.randint(100,999)))
            page.fill('input[name="password"]', password)
            page.click('button[type="submit"]')
            time.sleep(3)

            # Wait for email code input
            page.wait_for_selector('input[name="email_confirmation_code"]', timeout=30000)
            print("[*] Waiting for email verification code...")
            code = wait_for_code(token)

            if not code:
                print("[x] No code received. Aborting.")
                return None

            page.fill('input[name="email_confirmation_code"]', code)
            page.click('button[type="submit"]')
            print("[✓] Code submitted.")

            # Wait for birthday page
            page.wait_for_selector('select[title="Month:"]', timeout=30000)
            page.select_option('select[title="Month:"]', birth_month)
            page.select_option('select[title="Day:"]', birth_day)
            page.select_option('select[title="Year:"]', birth_year)
            page.click('button[type="submit"]')
            print("[✓] Birthday submitted.")

            # Wait for home page
            page.wait_for_url("https://www.instagram.com/*", timeout=30000)
            print("[✓] Account created successfully.")

            # Get session cookies
            cookies = context.cookies()
            session = {
                cookie["name"]: cookie["value"]
                for cookie in cookies
                if ".instagram.com" in cookie["domain"]
            }

            context.close()
            browser.close()
            return {"session": session}

    except Exception as e:
        print(f"[x] Account creation failed: {e}")
        return None
