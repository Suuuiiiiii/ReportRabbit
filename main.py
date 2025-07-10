import asyncio
from termcolor import cprint
from vpn import connect_vpn, disconnect_vpn
from mailtm import TempMail
from account_creator import create_instagram_account
from reporter import submit_report

TARGET_USERNAME = "target_username_here"  # Instagram account to report
REPORT_CYCLES = 5  # Number of fake accounts to create & report with

def banner():
    cprint("""
██████╗ ██████╗  ██████╗ 
██╔══██╗██╔══██╗██╔═══██╗
██████╔╝██████╔╝██║   ██║
██╔═══╝ ██╔═══╝ ██║   ██║
██║     ██║     ╚██████╔╝
╚═╝     ╚═╝      ╚═════╝ 

P.D.O - Porn Down Operation
Automated Instagram Reporting
    """, "red")

async def run_report_cycle(cycle_number):
    print(f"\n[•] Starting report cycle #{cycle_number}")

    if not connect_vpn():
        print("[✗] VPN failed. Skipping this cycle.")
        return

    # Step 1: Generate temp email
    mail = TempMail()
    email, mailbox_id = mail.generate_email()
    print(f"[+] Temp email: {email}")

    # Step 2: Create IG account with Playwright
    session = await create_instagram_account(email, mailbox_id, mail)
    if not session:
        print("[✗] Failed to create Instagram account.")
        disconnect_vpn()
        return

    # Step 3: Report the target account
    success = await submit_report(session, TARGET_USERNAME)
    if success:
        print("[✓] Report submitted.")
    else:
        print("[✗] Report failed.")

    # Step 4: Disconnect VPN to rotate IP next round
    disconnect_vpn()

async def main():
    banner()
    for i in range(1, REPORT_CYCLES + 1):
        await run_report_cycle(i)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        disconnect_vpn()
        print("\n[!] Interrupted. VPN disconnected.")
