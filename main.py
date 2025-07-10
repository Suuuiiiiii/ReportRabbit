import asyncio
import os
import traceback
import argparse
from termcolor import cprint
from dotenv import load_dotenv

from vpn import connect_vpn, disconnect_vpn
from mailtm import TempMail
from account_creator import create_instagram_account
from reporter import submit_report, last_reason_used
from log import write_log
from history import log_history

# CLI argument parsing
parser = argparse.ArgumentParser(description="P.D.O - Porn Down Operation")
parser.add_argument("--target", help="Instagram username to report")
parser.add_argument("--cycles", type=int, help="Number of report cycles")
args = parser.parse_args()

# Load .env and config
load_dotenv()
TARGET_USERNAME = args.target or os.getenv("TARGET_USERNAME", "default_user")
REPORT_CYCLES = args.cycles or int(os.getenv("REPORT_CYCLES", "1"))

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
    status = "Success" if result else "Failed"
    write_log(f"Report {'submitted' if result else 'failed'} for @{TARGET_USERNAME}")
    if last_reason_used:
        write_log(f"Reason used: {last_reason_used}")

    log_history(email, TARGET_USERNAME, last_reason_used or "Unknown", status)

    disconnect_vpn()
    write_log("VPN disconnected.\n")

async def main():
    banner()
    for i in range(REPORT_CYCLES):
        try:
            await run_report_cycle(i)
        except Exception as e:
            error_message = f"[Cycle {i+1}] Exception: {e}"
            print(f"[!] {error_message}")
            write_log(error_message)
            with open("pdo_error.log", "a") as errlog:
                errlog.write(f"\n{error_message}\n")
                errlog.write(traceback.format_exc())
    print("\n[✓] All cycles completed.")
    write_log("All report cycles completed.\n")

if __name__ == "__main__":
    asyncio.run(main())
