import requests
import time
import re

BASE_URL = "https://api.mail.tm"

def create_temp_email():
    try:
        print("[*] Generating temporary email...")
        domain_resp = requests.get(f"{BASE_URL}/domains")
        domain_resp.raise_for_status()
        domain = domain_resp.json()["hydra:member"][0]["domain"]

        username = f"pdo{int(time.time())}"
        address = f"{username}@{domain}"
        password = "PDOtool123"

        # Register
        register = requests.post(f"{BASE_URL}/accounts", json={
            "address": address,
            "password": password
        })

        if register.status_code != 201:
            print("[x] Failed to register temp email.")
            return None

        # Authenticate
        auth = requests.post(f"{BASE_URL}/token", json={
            "address": address,
            "password": password
        })

        if auth.status_code != 200:
            print("[x] Failed to authenticate temp email.")
            return None

        token = auth.json()["token"]
        print(f"[✓] Temp email created: {address}")
        return {"address": address, "token": token}

    except Exception as e:
        print(f"[x] Mail.tm error: {e}")
        return None


def wait_for_code(token, timeout=120):
    print("[*] Waiting for verification code...")
    headers = {"Authorization": f"Bearer {token}"}
    start = time.time()

    while time.time() - start < timeout:
        try:
            msgs = requests.get(f"{BASE_URL}/messages", headers=headers)
            msgs.raise_for_status()
            messages = msgs.json()["hydra:member"]

            for msg in messages:
                if "Instagram" in msg["from"]["address"] or "security code" in msg["subject"]:
                    msg_detail = requests.get(f"{BASE_URL}/messages/{msg['id']}", headers=headers)
                    content = msg_detail.json()["text"]
                    match = re.search(r"\b(\d{6})\b", content)
                    if match:
                        code = match.group(1)
                        print(f"[✓] Code received: {code}")
                        return code
        except:
            pass

        time.sleep(5)

    print("[x] Timed out waiting for code.")
    return None
