import requests
import random
import time
from fake_useragent import UserAgent

# Instagram endpoints and constants
BASE_URL = "https://www.instagram.com"
REPORT_URL = f"{BASE_URL}/users/{'{user_id}'}/report/"
USER_AGENT_FALLBACK = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
]

def get_random_user_agent():
    try:
        return UserAgent().random
    except:
        return random.choice(USER_AGENT_FALLBACK)

def build_headers(session_token):
    return {
        "User-Agent": get_random_user_agent(),
        "X-IG-App-ID": "936619743392459",  # standard Instagram web app ID
        "X-CSRFToken": session_token.get('csrf_token', ''),
        "Referer": BASE_URL,
        "Origin": BASE_URL,
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Cookie": f"sessionid={session_token['sessionid']}; csrftoken={session_token['csrf_token']};"
    }

def fetch_user_id(username, headers):
    url = f"{BASE_URL}/{username}/?__a=1&__d=dis"
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        try:
            data = res.json()
            return data['graphql']['user']['id']
        except:
            print("[!] Failed to parse user ID.")
    else:
        print(f"[!] Failed to fetch user ID. Status: {res.status_code}")
    return None

def report_user(username, session_token):
    headers = build_headers(session_token)
    print(f"[+] Getting user ID for @{username}...")
    user_id = fetch_user_id(username, headers)
    if not user_id:
        print("[✗] Could not find user ID. Aborting.")
        return False

    report_url = f"{BASE_URL}/users/{user_id}/report/"
    payload = {
        "source_name": "",
        "reason_id": "1",  # "It's inappropriate"
        "frx_context": ""
    }

    print(f"[+] Submitting report for @{username} (user ID: {user_id})...")
    time.sleep(random.uniform(1.5, 3.0))  # Simulate human delay
    res = requests.post(report_url, headers=headers, data=payload)

    if res.status_code == 200:
        print("[✓] Report submitted successfully.")
        return True
    else:
        print(f"[✗] Report failed. Status: {res.status_code}")
        print("Response:", res.text)
        return False
