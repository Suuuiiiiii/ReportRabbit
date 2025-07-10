import random
import string
import time
from playwright.async_api import async_playwright
from mailtm import TempMail

def generate_random_name():
    return random.choice(["Adam", "Eva", "Zane", "Lina", "Rami", "Maya", "Leo", "Nora"]) + \
           " " + random.choice(["Smith", "Zidan", "Ali", "Khan", "Lee", "Frost"])

def generate_username():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits + "!@#", k=12))

async def create_instagram_account(email, mailbox_id, mail: TempMail):
    full_name = generate_random_name()
    username = generate_username()
    password = generate_password()

    print(f"[•] Creating IG account: {username}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) " +
                       "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
            viewport={"width": 390, "height": 844}
        )
        page = await context.new_page()

        try:
            await page.goto("https://www.instagram.com/accounts/emailsignup/", timeout=60000)

            await page.fill("input[name=emailOrPhone]", email)
            await page.fill("input[name=fullName]", full_name)
            await page.fill("input[name=username]", username)
            await page.fill("input[name=password]", password)

            await page.click("button[type=submit]")
            await page.wait_for_timeout(3000)

            print("[*] Waiting for verification code...")
            code = mail.wait_for_code()

            if not code:
                print("[✗] No code received. Aborting.")
                await browser.close()
                return None

            print(f"[✓] Got code: {code}")

            await page.fill("input[name='email_confirmation_code']", code)
            await page.click("button[type=submit]")
            await page.wait_for_timeout(5000)

            print("[✓] Account created successfully!")

            storage = await context.storage_state()
            await browser.close()
            return storage

        except Exception as e:
            print(f"[✗] Error during signup: {e}")
            await browser.close()
            return None
