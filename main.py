import asyncio
from termcolor import cprint
from dotenv import load_dotenv
import os

from vpn import connect_vpn, disconnect_vpn
from mailtm import TempMail
from account_creator import create_instagram_account
from reporter import submit_report

# Load environment variables from .env
load_dotenv()

TARGET_USERNAME = os.getenv("TARGET_USERNAME", "default_user")
REPORT_CYCLES = int(os.getenv("REPORT_CYCLES", "1"))

def banner():
    cprint(r"""
██████╗ ██████╗  ██████╗ 
██╔══██╗██╔══██╗██╔═══██╗
██████╔╝██████╔╝██║   ██║
██╔═══╝ ██╔═══╝ ██║   ██║
██║     ██║     ╚██████╔╝
╚═╝     ╚═╝      ╚═════╝ 
P.D.O - Porn Down Operation
""", "magenta")

async def run_report_cycle(cycle_num):
    print(f"\n[ Cycle {cycle_num + 1} / {REPORT_CYCLES} ]")

    if not connect_vpn():
        print("[!] VPN connection failed. Skipping this cycle.")
        return

    mail = TempMail()
    email, mailbox_id = mail.generate_email()
    if not email:
        print("[!] Email generation failed. Skipping.")
        disconnect_vpn()
        return

    session = await create_instagram_account(email, mailbox_id, mail)
    if not session:
        print("[!] IG account creation failed. Skipping.")
        disconnect_vpn()
        return

    await submit_report(session, TARGET_USERNAME)
    disconnect_vpn()

async def main():
    banner()
    for i in range(REPORT_CYCLES):
        await run_report_cycle(i)
    print("\n[✓] All cycles completed.")

if __name__ == "__main__":
    asyncio.run(main())
