import requests
import time
import random
import string

class TempMail:
    def __init__(self):
        self.base = "https://api.mail.tm"
        self.session = requests.Session()
        self.domain = self.get_domain()

    def get_domain(self):
        try:
            res = self.session.get(f"{self.base}/domains").json()
            return res['hydra:member'][0]['domain']
        except:
            print("[✗] Failed to fetch mail.tm domain.")
            return "mail.tm"

    def generate_email(self):
        local = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        email = f"{local}@{self.domain}"
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

        res = self.session.post(f"{self.base}/accounts", json={
            "address": email,
            "password": password
        })

        if res.status_code == 201:
            print(f"[+] Email account created: {email}")
        else:
            print("[✗] Failed to create temp email.")
            return None, None

        token = self.session.post(f"{self.base}/token", json={
            "address": email,
            "password": password
        }).json().get("token")

        self.session.headers.update({"Authorization": f"Bearer {token}"})
        return email, self.get_mailbox_id()

    def get_mailbox_id(self):
        res = self.session.get(f"{self.base}/me").json()
        return res.get("id")

    def wait_for_code(self, mailbox_id, timeout=120):
        print("[*] Waiting for Instagram email verification...")
        start = time.time()
        while time.time() - start < timeout:
            res = self.session.get(f"{self.base}/messages").json()
            for msg in res.get("hydra:member", []):
                if "Instagram" in msg["from"]["address"]:
                    print("[✓] Verification email received.")
                    return self.extract_code(msg["intro"])
            time.sleep(5)
        print("[✗] Timeout waiting for code.")
        return None

    def extract_code(self, text):
        return ''.join(filter(str.isdigit, text))[:6]
