from playwright.sync_api import sync_playwright
import time
import random
import requests
from mailtm import wait_for_code

CAPTCHA_API_KEY = "k=6LdktRgnAAAAAFQ6icovYI2-masYLFjEFyzQzpix&co=aHR0cHM6Ly93d3cuZmJzYnguY29tOjQ0Mw..&hl=en&v=_cn5mBoBXIA0_T7xBjxkUqUA&theme=dark&size=normal&cb=44bqayhdjeie"
CAPTCHA_SITEKEY = "6LdktRgnAAAAAFQ6icovYI2-masYLFjEFyzQzpix"
CAPTCHA_URL = "https://www.instagram.com/accounts/emailsignup/"

def solve_captcha():
    print("[*] Solving CAPTCHA...")
    resp = requests.post("http://2captcha.com/in.php", data={
        'key': CAPTCHA_API_KEY,
        'method': 'userrecaptcha',
        'googlekey': CAPTCHA_SITEKEY,
        'pageurl': CAPTCHA_URL,
        'json': 1
    }).json()

    if resp['status'] != 1:
        print("[x] Failed to send CAPTCHA request.")
        return None

    captcha_id = resp['request']
    # Polling for result
    for _ in range(40):
        time.sleep(5)
        result = requests.get(f"http://2captcha.com/res.php?key={CAPTCHA_API_KEY}&action=get&id={captcha_id}&json=1").json()
        if result['status'] == 1:
            print("[✓] CAPTCHA Solved.")
            return result['request']
    print("[x] CAPTCHA solving timed out.")
    return None

def create_account(email, token, full_name, password):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            print("[*] Navigating to signup page...")
            page.goto(CAPTCHA_URL, timeout=60000)
            page.wait_for_load_state("networkidle")

            try:
                page.click('button:has-text("Decline optional cookies")', timeout=5000)
            except:
                pass

            # Step 1: Fill signup form
            username = full_name.lower().replace(" ", "") + str(random.randint(100,999))
            page.fill('input[name="emailOrPhone"]', email)
            page.fill('input[name="fullName"]', full_name)
            page.fill('input[name="username"]', username)
            page.fill('input[name="password"]', password)
            page.click('button[type="submit"]')
            time.sleep(3)

            # Step 2: Fill birthday
            print("[*] Filling in birthday...")
            page.wait_for_selector('select[title="Month:"]', timeout=30000)
            page.select_option('select[title="Month:"]', str(random.randint(1, 12)))
            page.select_option('select[title="Day:"]', str(random.randint(1, 28)))
            page.select_option('select[title="Year:"]', "2000")
            page.click('button[type="submit"]')
            time.sleep(3)

            # Step 3: Solve CAPTCHA
            token = solve_captcha()
            if not token:
                print("[x] CAPTCHA bypass failed.")
                return None

            print("[*] Injecting CAPTCHA token...")
            page.evaluate("""
                (token) => {
                    document.querySelector('textarea[name="g-recaptcha-response"]').style.display = 'block';
                    document.querySelector('textarea[name="g-recaptcha-response"]').value = token;
                }
            """, token)

            time.sleep(2)
            page.click('button[type="submit"]')  # Confirm after CAPTCHA

            # Step 4: Wait for email confirmation input
            print("[*] Waiting for email code input...")
            page.wait_for_selector('input[name="email_confirmation_code"]', timeout=60000)
            code = wait_for_code(token)

            if not code:
                print("[*] Resending email code...")
                try:
                    page.click("text=Resend code")
                    time.sleep(10)
                    code = wait_for_code(token)
                except:
                    print("[x] Couldn't click resend.")

            if not code:
                print("[x] No verification code. Aborting.")
                return None

            page.fill('input[name="email_confirmation_code"]', code)
            page.click('button[type="submit"]')
            print("[✓] Code submitted.")

            # Step 5: Final step, logged in
            page.wait_for_url("https://www.instagram.com/*", timeout=30000)
            print("[✓] Account created and logged in.")

            # Extract session
            cookies = context.cookies()
            session = {cookie["name"]: cookie["value"]
                       for cookie in cookies if ".instagram.com" in cookie["domain"]}
            context.close()
            browser.close()
            return {"session": session}

    except Exception as e:
        print(f"[x] Account creation failed: {e}")
        return None
