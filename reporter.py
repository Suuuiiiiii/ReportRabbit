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


def perform_report():
    while True:
        os.system("clear")
        show_banner()

        # Select report reason
        print("\n[1] Nudity or sexual activity\n")
        reason_input = input("[?] Choose report type [1]: ").strip()
        report_reason = "Nudity or sexual activity"  # Only one for now

        # Target username
        target_username = input("[?] Target Instagram username: ").strip()

        # Number of reports
        try:
            total_reports = int(input("[?] Number of reports: "))
        except:
            print("[x] Invalid number.")
            continue

        success_count = 0
        for i in range(total_reports):
            print(f"\n[•] Starting Report #{i + 1}")
            print("[*] Connecting to VPN...")
            connect_to_random()

            # Generate temp mail
            email, token = generate_address()
            print(f"[✓] Temp email created: {email}")

            # Generate account
            full_name = generate_random_name()
            password = generate_password()

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

                    # Set session cookies
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

                    # Click search
                    page.click("svg[aria-label='Search']")
                    time.sleep(1)
                    page.fill("input[placeholder='Search']", target_username)
                    time.sleep(2)

                    # Check if username appears in dropdown
                    try:
                        page.click(f"text={target_username}")
                        time.sleep(3)
                    except:
                        print("[x] Account not found A.N.F")
                        break  # Exit loop, go back to ask username again

                    # Click 3-dot menu
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
                    page.click(f"text={report_reason}")  # confirm
                    print(f"[✓] Report submitted.")
                    success_count += 1
                    print(f"|{success_count}|")

                    context.close()
                    browser.close()

            except Exception as e:
                print(f"[x] Failed to submit report: {e}")

        # After the loop, return to username step
        input("\n[↩] Press Enter to return to target entry...")
