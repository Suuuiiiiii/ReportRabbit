import random
import time
from playwright.async_api import async_playwright

HELP_CENTER_URL = "https://help.instagram.com/contact/497253480400030"

last_reason_used = None  # Track last selected reason for logging

def load_reasons_from_file():
    try:
        with open("report_reasons.txt", "r") as f:
            reasons = [line.strip() for line in f if line.strip()]
        return reasons
    except FileNotFoundError:
        print("[!] report_reasons.txt not found.")
        return []

def choose_reason():
    global last_reason_used
    reasons = load_reasons_from_file()
    if not reasons:
        print("[!] No reasons available.")
        return None

    print("\n[?] Choose a report reason:")
    for i, reason in enumerate(reasons, 1):
        print(f"{i}. {reason}")
    while True:
        choice = input("Enter reason number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(reasons):
            last_reason_used = reasons[int(choice) - 1]
            return last_reason_used
        print("[!] Invalid choice. Try again.")

async def submit_report(session_storage, target_username):
    reason_label = choose_reason()
    if not reason_label:
        print("[!] No valid reason selected. Aborting.")
        return False

    print(f"[•] Reporting @{target_username} for: {reason_label}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=session_storage)
        page = await context.new_page()

        try:
            await page.goto(HELP_CENTER_URL, timeout=30000)
            await page.wait_for_selector("input[name='Field1785749746197248']", timeout=10000)

            print("[*] Filling report form...")

            # Fill target account URL
            target_url = f"https://www.instagram.com/{target_username}/"
            await page.fill("input[name='Field1785749746197248']", target_url)

            # Select reason
            await page.select_option("select[name='Field1785749746197252']", label=reason_label)

            # Optional description
            await page.fill("textarea[name='Field1785749746197256']", f"This account is violating the rules due to: {reason_label.lower()}.")

            await page.click("button[type='submit']")
            await page.wait_for_timeout(3000)

            print("[✓] Report submitted.")
            await browser.close()
            return True

        except Exception as e:
            print(f"[✗] Error submitting report: {e}")
            await browser.close()
            return False
