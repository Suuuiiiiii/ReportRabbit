import asyncio
from playwright.async_api import async_playwright
import random
import time

REPORT_REASONS = [
    "It's inappropriate",  # default path
    # Additional report paths can be added here later
]

async def report_account(username: str, session_id: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent=random_user_agent(),
            storage_state={
                "cookies": [
                    {
                        "name": "sessionid",
                        "value": session_id,
                        "domain": ".instagram.com",
                        "path": "/",
                        "httpOnly": True,
                        "secure": True
                    }
                ]
            }
        )

        page = await context.new_page()

        try:
            print(f"[+] Navigating to profile: {username}")
            await page.goto(f"https://www.instagram.com/{username}/", timeout=30000)
            await page.wait_for_selector('svg[aria-label="Options"]', timeout=15000)

            print("[+] Clicking the ⋯ menu")
            await page.click('svg[aria-label="Options"]')
            await asyncio.sleep(random.uniform(1.0, 2.0))

            print("[+] Clicking 'Report'")
            await page.click('text=Report')
            await asyncio.sleep(random.uniform(1.0, 2.0))

            print("[+] Selecting 'It\'s inappropriate'")
            await page.click('text=It\'s inappropriate')
            await asyncio.sleep(random.uniform(1.0, 2.0))

            print("[+] Selecting 'Report account'")
            await page.click('text=Report Account')
            await asyncio.sleep(random.uniform(1.0, 2.0))

            print("[+] Choosing reason: 'Posting inappropriate content'")
            await page.click('text=Posting inappropriate content')
            await asyncio.sleep(random.uniform(1.0, 2.0))

            print("[+] Submitting report")
            await page.click('text=Submit')
            await asyncio.sleep(1.5)

            print("[✓] Report submitted successfully.")
        except Exception as e:
            print(f"[✗] Failed to report: {e}")
        finally:
            await browser.close()

def random_user_agent():
    # Keep it simple — or fetch from list/fake_useragent if needed
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
    ]
    return random.choice(agents)

# Entry point for testing
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python reporter.py <username> <sessionid>")
    else:
        asyncio.run(report_account(sys.argv[1], sys.argv[2]))
