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

def report_instagram(username, vpn, amount):
    for i in range(amount):
        print(f"[{i+1}/{amount}] Reporting @{username}...")

        url = "https://help.instagram.com/ajax/help/contact/submit/page"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest"
        }

        report_type = random.choice(["nudity", "sexual_content", "spam"])
        data = {
            "username": username,
            "report_type": report_type,
            "lsd": "mocktoken123",  # placeholder
            "__ajax__": "1"
        }

        try:
            res = requests.post(url, headers=headers, data=data, timeout=10)
            if res.status_code == 200:
                print(f"   [✓] Report sent as {report_type}")
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

    report_instagram(username, vpn, amount)
