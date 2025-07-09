import requests
import random
import time
import os
import sys

def rotate_ip():
    print("[*] Rotating IP with Windscribe...")
    os.system("windscribe connect")

def choose_platform():
    platforms = {
        "1": "Instagram",
        "2": "TikTok",
        "3": "Facebook",
        "4": "YouTube"
    }

    while True:
        print("\n:: 1 Instagram   |   2 TikTok   |  3 Facebook  |   4 YouTube ::")
        choice = input("[choice] : ").strip()

        if choice in platforms:
            print(f"\n[✓] You chose: {platforms[choice]}\n")
            return platforms[choice]
        else:
            print("[!] Invalid input. Please enter a number between 1 and 4.")

def get_username():
    username = input("Enter the target username (no @): ").strip()
    if username == "":
        print("[!] Username cannot be empty.")
        sys.exit(1)
    return username

def ask_vpn():
    while True:
        vpn = input("Use VPN? (1 = Yes, 0 = No): ").strip()
        if vpn in ["0", "1"]:
            return vpn == "1"
        else:
            print("[!] Invalid input. Enter 0 or 1.")

def ask_amount():
    while True:
        amount = input("How many reports? ").strip()
        if amount.isdigit() and int(amount) > 0:
            return int(amount)
        else:
            print("[!] Enter a valid positive number.")

def choose_report_type():
    report_types = {
        "1": "nudity",
        "2": "sexual_activity",
        "3": "harassment_or_bullying",
        "4": "hate_speech_or_symbols",
        "5": "spam",
        "6": "suicide_or_self_injury",
        "7": "false_information",
        "8": "illegal_or_regulated_goods",
        "9": "scam_or_fraud",
        "10": "intellectual_property_violation"
    }

    print("\n:: Choose Report Type ::")
    for key, value in report_types.items():
        print(f"{key}. {value.replace('_', ' ').title()}")

    while True:
        choice = input("[type number] : ").strip()
        if choice in report_types:
            print(f"\n[✓] Selected: {report_types[choice].replace('_', ' ').title()}\n")
            return report_types[choice]
        else:
            print("[!] Invalid input. Please choose a number between 1 and 10.")

def report_instagram(username, vpn, amount, report_type):
    for i in range(amount):
        print(f"[{i+1}/{amount}] Reporting @{username} for {report_type.replace('_', ' ').title()}...")

        url = "https://help.instagram.com/ajax/help/contact/submit/page"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest"
        }

        data = {
            "username": username,
            "report_type": report_type,
            "lsd": "mocktoken123",  # Placeholder for now
            "__ajax__": "1"
        }

        try:
            res = requests.post(url, headers=headers, data=data, timeout=10)
            if res.status_code == 200:
                print(f"   [✓] Report sent")
            else:
                print(f"   [X] Failed ({res.status_code})")
        except Exception as e:
            print(f"   [!] Error: {e}")

        if vpn and (i % 5 == 0):
            rotate_ip()

        time.sleep(random.randint(2, 5))

if __name__ == "__main__":
    platform = choose_platform()
    if platform != "Instagram":
        print(f"[x] Reporting for {platform} is not implemented yet.")
        sys.exit(0)

    username = get_username()
    vpn = ask_vpn()
    amount = ask_amount()
    report_type = choose_report_type()

    report_instagram(username, vpn, amount, report_type)
