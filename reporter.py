import random
import time
from playwright.async_api import async_playwright

HELP_CENTER_URL = "https://help.instagram.com/contact/497253480400030"  # Report a user

async def submit_report(session_storage, target_username):
    print(f"[•] Reporting user: {target_username}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=session_storage)
        page = await context.new_page()

        try:
            await page.goto(HELP_CENTER_URL, timeout=30000)

            # Wait for form to load
            await page.wait_for_selector("input[name='Field1785749746197248']", timeout=10000)

            print("[*] Filling report form...")

            # Fill target account URL
            target_url = f"https://www.instagram.com/{target_username}/"
            await page.fill("input[name='Field1785749746197248']", target_url)

            # Select reason from dropdown (Posting inappropriate content)
            await page.select_option("select[name='Field1785749746197252']", label="Nudity or pornography")

            # (Optional) Fill description box
            await page.fill("textarea[name='Field1785749746197256']", "This account is sharing explicit adult content.")

            # Submit the form
            await page.click("button[type='submit']")

            await page.wait_for_timeout(3000)
            print("[✓] Report submitted successfully.")

            await browser.close()
            return True

        except Exception as e:
            print(f"[✗] Failed to submit report: {e}")
            await browser.close()
            return False
