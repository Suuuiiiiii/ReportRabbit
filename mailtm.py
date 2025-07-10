import requests
import time
import random
import string

class TempMail:
    def __init__(self):
        self.base_url = "https://api.mail.tm"
        self.session = requests.Session()
        self.token = None
        self.mailbox_id = None
        self.email = None
        self.password = None
        self.domain = self._get_domain()

    def _get_domain(self):
        try:
            res = self.session.get(f"{self.base_url}/domains")
            res.raise_for_status()
            return res.json()['hydra:member'][0]['domain']
        except:
            print("[✗] Failed to fetch mail.tm domain. Using fallback.")
            return "mail.tm"

    def generate_email(self):
        self.email = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + f"@{self.domain}"
        self.password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

        # Register mailbox
        acc_res = self.session.post(f"{self.base_url}/accounts", json={
            "address": self.email,
            "password": self.password
        })

        if acc_res.status_code != 201:
            print("[✗] Failed to create email account.")
            return None, None

        # Get token
        token_res = self.session.post(f"{self.base_url}/token", json={
            "address": self.email,
            "password": self.password
        })

        if token_res.status_code != 200:
            print("[✗] Failed to retrieve mail.tm token.")
            return None, None

        self.token = token_res.json()["token"]
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})

        # Get mailbox ID
        profile = self.session.get(f"{self.base_url}/me").json()
        self.mailbox_id = profile.get("id")

        print(f"[+] Mailbox ready: {self.email}")
        return self.email, self.mailbox_id

    def wait_for_code(self, timeout=120):
        print("[*] Waiting for Instagram verification email...")
        start = time.time()

        while time.time() - start < timeout:
            try:
                res = self.session.get(f"{self.base_url}/messages")
                res.raise_for_status()
                messages = res.json().get("hydra:member", [])
                for msg in messages:
                    if "Instagram" in msg["from"]["address"]:
                        print("[✓] Verification email received.")
                        return self._extract_code(msg["intro"])
            except Exception as e:
                print(f"[!] Mailbox check failed: {e}")
            time.sleep(5)

        print("[✗] Timeout waiting for verification code.")
        return None

    def _extract_code(self, text):
        return ''.join(filter(str.isdigit, text))[:6]
