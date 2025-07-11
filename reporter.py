from ASCII import show_banner
from vpn import connect_to_random
from mailtm import generate_address, wait_for_code
from account_creator import create_account
from playwright.sync_api import sync_playwright
import random
import string
import time
import os


def generate_random_name():
    first_names = ["Alex", "Sam", "Jamie", "Casey", "Jordan", "Taylor"]
    last_names = ["Smith", "Brown", "Lee", "Wilson", "Adams", "Scott"]
    return random.choice(first_names) + " " + random.choice(last_names)


def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


def perform_report(target_username, report_reason):
    success_count = 0

    while True:
        os.system("clear")
        show_banner()
        print(f"\n[•] Starting Report #{success_count + 1}")
        print("[*] Connecting to VPN...")
        connect_to_random()

        email, token = generate_address()
        full_name = generate_random_name()
        password = generate_password()

        print(f"[✓] Temp email created: {email}")

        session_info = create_account(email, token, full_name, password)
        if not session_info:
            print("[x] Failed to create Instagram account.")
            continue

        print("[*] Logging in to perform report...")

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()

                for name, value in session_info["session"].items():
                    context.add_cookies([{
                        "name": name,
                        "value": value,
                        "domain": ".instagram.com",
                        "path": "/",
                        "httpOnly": True,
                        "secure": True
                    }])

                page.goto("https://www.instagram.com/", timeout=60000)
                page.wait_for_load_state("networkidle")
                time.sleep(3)

                page.click("svg[aria-label='Search']")
                time.sleep(1)
                page.fill("input[placeholder='Search']", target_username)
                time.sleep(2)

                try:
                    page.click(f"text={target_username}")
                    time.sleep(3)
                except:
                    print("[x] Account not found A.N.F")
                    input("[↩] Press Enter to enter a new username...")
                    return False

                page.click("svg[aria-label='Options']")
                time.sleep(1)
                page.click("text=Report")
                time.sleep(1)
                page.click("text=Report Account")
                time.sleep(1)
                page.click("text=It's posting content that shouldn't be on Instagram")
                time.sleep(1)
                page.click(f"text={report_reason}")
                time.sleep(1)
                page.click(f"text={report_reason}")
                print("[✓] Report submitted.")

                success_count += 1
                print(f"| {success_count} |")

                context.close()
                browser.close()
                return True

        except Exception as e:
            print(f"[x] Failed to report: {e}")
            return False
