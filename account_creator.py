from playwright.sync_api import sync_playwright
import time
import random

def create_account(email, token, full_name, password):
    birth_day = str(random.randint(1, 28))
    birth_month = str(random.randint(1, 12))
    birth_year = str(random.randint(1995, 2002))  # 18+ guaranteed

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            print("[*] Navigating to Instagram signup...")
            page.goto("https://www.instagram.com/accounts/emailsignup/", timeout=60000)
            page.wait_for_load_state("networkidle")

            # Fill signup form
            page.fill("input[name=emailOrPhone]", email)
            page.fill("input[name=fullName]", full_name)
            page.fill("input[name=username]", full_name.lower().replace(" ", "") + str(random.randint(100,999)))
            page.fill("input[name=password]", password)

            page.click("button[type=submit]")
            time.sleep(5)

            # Wait for code entry page
            page.wait_for_selector("input[name=email_confirmation_code]", timeout=30000)
            print("[*] Waiting for email verification code...")

            from mailtm import wait_for_code
            code = wait_for_code(token)
            if not code:
                print("[x] No verification code received.")
                return None

            page.fill("input[name=email_confirmation_code]", code)
            page.click("button[type=submit]")

            # Fill birthdate
            page.wait_for_selector('select[title="Month:"]', timeout=15000)
            page.select_option('select[title="Month:"]', birth_month)
            page.select_option('select[title="Day:"]', birth_day)
            page.select_option('select[title="Year:"]', birth_year)
            page.click("button[type=submit]")

            # Wait for homepage load
            page.wait_for_url("https://www.instagram.com/*", timeout=30000)
            print("[✓] Account created successfully.")

            cookies = context.cookies()
            session = {cookie["name"]: cookie["value"] for cookie in cookies if ".instagram.com" in cookie["domain"]}

            context.close()
            browser.close()
            return {"session": session}

    except Exception as e:
        print(f"[x] Account creation failed: {e}")
        return None
