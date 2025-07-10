from playwright.sync_api import sync_playwright
import time

REPORT_OPTIONS = {
    1: "Nudity or sexual activity",
    2: "Bullying or harassment",
    3: "Spam",
    4: "Hate speech or symbols",
    5: "False information"
}

def submit_report(session_cookies, target_username, report_type):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        context.add_cookies([
            {
                "name": name,
                "value": value,
                "domain": ".instagram.com",
                "path": "/",
                "httpOnly": True,
                "secure": True,
                "sameSite": "Lax"
            }
            for name, value in session_cookies.items()
        ])

        page = context.new_page()

        try:
            print(f"[*] Navigating to @{target_username}'s profile...")
            page.goto(f"https://www.instagram.com/{target_username}/", timeout=30000)
            page.wait_for_load_state('networkidle')

            print("[*] Opening report menu...")
            page.click('svg[aria-label="More options"]')

            page.wait_for_selector('text=Report', timeout=10000)
            page.click('text=Report')

            time.sleep(2)
            page.click('text=It’s inappropriate')
            time.sleep(2)
            page.click('text=Report account')
            time.sleep(2)

            reason_text = REPORT_OPTIONS.get(report_type)
            if reason_text:
                page.click(f'text={reason_text}')
                time.sleep(2)
                page.click('text=Submit report')
                print(f"[✓] Report sent for reason: {reason_text}")
                return True
            else:
                print("[x] Invalid report type passed.")
                return False

        except Exception as e:
            print(f"[x] Report failed: {e}")
            return False

        finally:
            context.close()
            browser.close()
