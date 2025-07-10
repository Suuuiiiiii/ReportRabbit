from vpn import connect_vpn, disconnect_vpn
from mailtm import create_temp_email
from account_creator import create_account
from reporter import submit_report

import random
import string
import time
import sys

def generate_full_name():
    first = random.choice(["Adam", "John", "David", "Ryan", "Mike", "Leo", "Sam", "Chris", "Josh"])
    last = random.choice(["Smith", "Brown", "Taylor", "White", "Lee", "King", "Turner", "Baker"])
    return f"{first} {last}"

def generate_password(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def prompt_number(msg, min_val, max_val):
    while True:
        try:
            value = int(input(msg))
            if value < min_val or value > max_val:
                print(f"[x] Please enter a number between {min_val} and {max_val}.")
            else:
                return value
        except:
            print("[x] Invalid input. Try again.")

def main():
    print(":: Instagram Report Tool — P.D.O ::")
    print(":: 1 Instagram   |   2 TikTok   | 3 Facebook  | 4 YouTube ::")
    platform_choice = prompt_number("[Platform Number]: ", 1, 1)  # Only Instagram for now

    username = input("[Target Username]: ").strip()
    vpn_choice = prompt_number("[VPN? 1=Yes / 0=No]: ", 0, 1)
    amount = prompt_number("[Number of Reports]: ", 1, 100)

    print("\n:: Report Types ::")
    print("1. Nudity")
    print("2. Sexual Activity")
    print("3. Harassment")
    print("4. Spam")
    print("5. Hate Speech")
    print("6. False Info")
    report_type = prompt_number("[Report Type Number]: ", 1, 6)

    success = 0
    fail = 0

    for i in range(amount):
        print(f"\n[•] Starting Report #{i+1}")

        if vpn_choice:
            print("[*] Connecting to VPN...")
            if not connect_vpn():
                print("[x] VPN failed.")
                break

        email_data = create_temp_email()
        if not email_data:
            print("[x] Failed to get temp email.")
            fail += 1
            continue

        full_name = generate_full_name()
        password = generate_password()

        account_data = create_account(
            email_data["address"],
            email_data["token"],
            full_name,
            password
        )

        if not account_data:
            print("[x] Failed to create Instagram account.")
            fail += 1
            if vpn_choice:
                disconnect_vpn()
            continue

        session = account_data["session"]
        result = submit_report(session, username, report_type)

        if result:
            success += 1
        else:
            fail += 1

        if vpn_choice:
            print("[*] Disconnecting VPN...")
            disconnect_vpn()

    print(f"\n[✓] Done! Success: {success}, Failed: {fail}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[x] Interrupted.")
        sys.exit(0)
