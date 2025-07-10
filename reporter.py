from ascii import show_banner
from account_creator import create_account
from mailtm import generate_address
from vpn import connect_to_random
import random
import string
import time

def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters, k=length))

def run_report_flow():
    show_banner()

    print("\n:: 1 instagram | 2 facebook | 3 gmail | 4 twitter ::\n")
    choice = input("[choice] > ")

    if choice != "1":
        print("[x] Only Instagram is supported for now.")
        return

    print("\n[+] Report Type")
    print(":: 1 nudity or sexual activity ::")
    report_choice = input("[choice] > ")

    if report_choice != "1":
        print("[x] Only 'nudity or sexual activity' is available.")
        return

    report_reason = "Nudity or sexual activity"
    target_username = input("\n[?] Target Instagram username > ")
    total_reports = int(input("[?] Number of reports to send > "))

    for i in range(1, total_reports + 1):
        print(f"\n[•] Starting Report #{i}")

        print("[*] Connecting to VPN...")
        connect_to_random()

        print("[*] Generating email...")
        email_data = generate_address()
        email = email_data["address"]
        token = email_data["token"]

        full_name = random_string(6) + " " + random_string(5)
        password = random_string(12)

        result = create_account(
            email=email,
            token=token,
            full_name=full_name,
            password=password,
            target_username=target_username,
            report_reason=report_reason
        )

        if result is None:
            print("[x] Failed to create Instagram account.")
        else:
            print(f"[✓] Report sent.")

        print(f"|{i}|")
        time.sleep(2)

    print("\n[✓] Done! Success:", total_reports)

