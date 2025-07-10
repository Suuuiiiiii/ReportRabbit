import asyncio
from termcolor import cprint
from dotenv import load_dotenv
import os

from vpn import connect_vpn, disconnect_vpn
from mailtm import TempMail
from account_creator import create_instagram_account
from reporter import submit_report, last_reason_used
from log import write_log

# Load .env configuration
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
    write_log(f"Cycle {cycle_num + 1}: Starting")

    write_log("Connecting to VPN...")
    if not connect_vpn():
        print("[!] VPN connection failed. Skipping this cycle.")
        write_log("VPN connection failed. Skipping cycle.\n")
        return

    mail = TempMail()
    email, mailbox_id = mail.generate_email()
    if not email:
        print("[!] Email generation failed. Skipping.")
        write_log("Email generation failed.\n")
        disconnect_vpn()
        return
    write_log(f"Generated email: {email}")

    session = await create_instagram_account(email, mailbox_id, mail)
    if not session:
        print("[!] IG account creation failed. Skipping.")
        write_log(f"Account creation failed for {email}\n")
        disconnect_vpn()
        return
    write_log(f"Instagram account created using {email}")

    result = await submit_report(session, TARGET_USERNAME)
    if result:
        print("[✓] Report sent.")
        write_log(f"Report sent successfully to @{TARGET_USERNAME}")
        if last_reason_used:
            write_log(f"Reason used: {last_reason_used}")
    else:
        print("[✗] Report failed.")
        write_log(f"Report failed for @{TARGET_USERNAME}")

    disconnect_vpn()
    write_log("VPN disconnected.\n")

async def main():
    banner()
    for i in range(REPORT_CYCLES):
        await run_report_cycle(i)
    print("\n[✓] All cycles completed.")
    write_log("All report cycles completed.\n")

if __name__ == "__main__":
    asyncio.run(main())
