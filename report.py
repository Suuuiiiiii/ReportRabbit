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

def report_instagram(username):
    print(f"[>] Reporting @{username} to Instagram...")

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
        "lsd": "mocktoken123",  # This may need to be extracted in future
        "__ajax__": "1"
    }

    try:
        res = requests.post(url, headers=headers, data=data, timeout=10)
        if res.status_code == 200:
            print(f"[✓] Report sent for @{username} as {report_type}")
        else:
            print(f"[X] Failed ({res.status_code}) for @{username}")
    except Exception as e:
        print(f"[!] Error for @{username}: {e}")

def handle_platform(platform):
    usernames = [
        "pornpage1", "nsfw_account2", "softcore_spammer"
    ]

    for i, user in enumerate(usernames):
        if platform == "Instagram":
            report_instagram(user)
        elif platform == "TikTok":
            print(f"[x] TikTok report logic not implemented yet for {user}")
        elif platform == "Facebook":
            print(f"[x] Facebook report logic not implemented yet for {user}")
        elif platform == "YouTube":
            print(f"[x] YouTube report logic not implemented yet for {user}")
        else:
            print("[!] Unknown platform.")
            sys.exit(1)

        time.sleep(random.randint(2, 5))
        if i % 5 == 0:
            rotate_ip()

if __name__ == "__main__":
    selected = choose_platform()
    handle_platform(selected)
