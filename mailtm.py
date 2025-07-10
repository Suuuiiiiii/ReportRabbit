# mailtm.py
import requests
import time
import random
import string

BASE_URL = "https://api.mail.tm"

def generate_random_name():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))

def generate_address():
    username = generate_random_name()
    domain = "mechanicspedia.com"  # or use domains from mail.tm's list
    email = f"{username}@{domain}"
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

    # Create account
    response = requests.post(f"{BASE_URL}/accounts", json={
        "address": email,
        "password": password
    })

    if response.status_code not in [200, 201]:
        raise Exception(f"Failed to create temp email: {response.text}")

    # Get token
    token_resp = requests.post(f"{BASE_URL}/token", json={
        "address": email,
        "password": password
    })
    token = token_resp.json()["token"]

    print(f"[✓] Temp email created: {email}")
    return email, token

def wait_for_code(token, timeout=120):
    headers = {"Authorization": f"Bearer {token}"}
    print("[*] Waiting for verification email...")

    for _ in range(timeout):
        resp = requests.get(f"{BASE_URL}/messages", headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            if data["hydra:member"]:
                msg_id = data["hydra:member"][0]["id"]
                msg_resp = requests.get(f"{BASE_URL}/messages/{msg_id}", headers=headers)
                msg_text = msg_resp.json()["text"]

                # Extract 6-digit code
                import re
                match = re.search(r"\b\d{6}\b", msg_text)
                if match:
                    return match.group(0)

        time.sleep(1)

    return None
