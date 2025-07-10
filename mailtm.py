import requests
import random
import string
import time

MAILTM_API = "https://api.mail.tm"
HEADERS = {"Content-Type": "application/json"}

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def create_temp_email():
    try:
        username = generate_random_string()
        password = generate_random_string(12)
        email_address = f"{username}@mail.tm"

        # Create account
        res = requests.post(f"{MAILTM_API}/accounts", json={
            "address": email_address,
            "password": password
        }, headers=HEADERS)

        if res.status_code != 201 and "already exists" not in res.text:
            print("[x] Failed to create mail.tm account.")
            return None

        # Get token
        res = requests.post(f"{MAILTM_API}/token", json={
            "address": email_address,
            "password": password
        }, headers=HEADERS)

        if res.status_code != 200:
            print("[x] Failed to authenticate with mail.tm.")
            return None

        token = res.json()["token"]
        return {
            "address": email_address,
            "password": password,
            "token": token
        }

    except Exception as e:
        print(f"[x] Error creating temp email: {e}")
        return None

def wait_for_verification_code(token, timeout=120):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    print("[*] Waiting for Instagram verification email...")
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            res = requests.get(f"{MAILTM_API}/messages", headers=headers)
            if res.status_code != 200:
                print("[x] Failed to check inbox.")
                time.sleep(5)
                continue

            messages = res.json().get("hydra:member", [])
            for msg in messages:
                if "Instagram" in msg.get("from", {}).get("address", "") or "Instagram" in msg.get("subject", ""):
                    msg_id = msg["id"]
                    msg_res = requests.get(f"{MAILTM_API}/messages/{msg_id}", headers=headers)
                    if msg_res.status_code == 200:
                        body = msg_res.json().get("text", "")
                        code = extract_code_from_text(body)
                        if code:
                            print(f"[✓] Verification code received: {code}")
                            return code
        except Exception as e:
            print(f"[x] Error checking inbox: {e}")

        time.sleep(5)

    print("[x] Timeout waiting for verification code.")
    return None

def extract_code_from_text(text):
    import re
    match = re.search(r"\b(\d{6})\b", text)
    return match.group(1) if match else None
