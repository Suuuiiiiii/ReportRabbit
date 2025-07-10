from playwright.sync_api import sync_playwright
import time

def submit_report(session_cookies, target_username):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        # Apply session cookies
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
            page.click('svg[aria-label="More options"]')  # ⋯ button

            page.wait_for_selector('text=Report', timeout=10000)
            page.click('text=Report')

            time.sleep(2)  # Wait for modal to load
            page.click('text=It’s inappropriate')  # Option

            time.sleep(2)
            page.click('text=Report account')  # Step 2

            time.sleep(2)
            page.click('text=Posting inappropriate content')  # Step 3

            time.sleep(2)
            page.click('text=Submit report')  # Final step (button may vary)

            print("[✓] Report sent.")
            return True

        except Exception as e:
            print(f"[x] Report failed: {e}")
            return False

        finally:
            context.close()
            browser.close()
