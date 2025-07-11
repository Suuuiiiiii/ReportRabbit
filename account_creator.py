from playwright.sync_api import sync_playwright
import time
import random
from mailtm import wait_for_code

def create_account(email, token, full_name, password):
    birth_day = str(random.randint(1, 28))
    birth_month = str(random.randint(1, 12))

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            print("[*] Navigating to signup page...")
            page.goto("https://www.instagram.com/accounts/emailsignup/", timeout=60000)
            page.wait_for_load_state("networkidle")

            try:
                page.click('button:has-text("Decline optional cookies")', timeout=5000)
                print("[✓] Cookie banner dismissed")
            except:
                print("[!] No cookie banner to dismiss")

            page.fill('input[name="emailOrPhone"]', email)
            page.fill('input[name="fullName"]', full_name)
            page.fill('input[name="username"]', full_name.lower().replace(" ", "") + str(random.randint(100, 999)))
            page.fill('input[name="password"]', password)
            page.click('button[type="submit"]')
            time.sleep(3)

            print("[*] Filling in birthday...")
            page.wait_for_selector('select[title="Month:"]', timeout=30000)
            page.select_option('select[title="Month:"]', birth_month)
            page.select_option('select[title="Day:"]', birth_day)

            year_dropdown = page.locator('select[title="Year:"]')
            year_dropdown.click()
            time.sleep(0.5)
            for _ in range(30):
                year_dropdown.press("ArrowDown")
                time.sleep(0.05)
            page.select_option('select[title="Year:"]', "2000")
            time.sleep(0.5)

            page.click('button[type="submit"]')
            print("[✓] Birthday submitted.")

            print("[*] Waiting for email verification code...")
            try:
                page.wait_for_selector('input[name="email_confirmation_code"]', timeout=60000)
            except:
                print("[x] Email confirmation field didn't appear.")
                return None

            code = wait_for_code(token, timeout=120)

            if not code:
                print("[*] No code received, trying to resend...")
                try:
                    page.click("text=Resend code")
                    time.sleep(5)
                    code = wait_for_code(token, timeout=60)
                except:
                    print("[x] Couldn't click Resend code.")

            if not code:
                print("[x] Still no code received. Aborting.")
                return None

            page.fill('input[name="email_confirmation_code"]', code)
            page.click('button[type="submit"]')
            print("[✓] Code submitted.")

            page.wait_for_url("https://www.instagram.com/*", timeout=30000)
            print("[✓] Account created successfully.")

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
