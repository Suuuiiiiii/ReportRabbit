from vpn import connect_vpn, disconnect_vpn
from mailtm import create_temp_email
from account_creator import create_account
from reporter import submit_report
from utils import generate_name, generate_password, print_banner
import time

def main():
    print_banner()
    print("=== P.D.O - Porn Down Operation ===\n")
    target_username = input("Enter the Instagram username to report: ").strip()

    while True:
        try:
            report_count = int(input("How many reports do you want to send? "))
            if report_count <= 0:
                raise ValueError
            break
        except ValueError:
            print("[x] Please enter a valid positive number.")

    for i in range(1, report_count + 1):
        print(f"\n=== REPORT {i} / {report_count} ===")

        print("[>] Connecting to VPN...")
        if not connect_vpn():
            print("[x] Failed to connect to VPN. Retrying in 10 seconds...")
            time.sleep(10)
            continue
        print("[✓] VPN connected.")

        print("[>] Generating temporary email...")
        email_data = create_temp_email()
        if not email_data:
            print("[x] Could not get a temporary email. Skipping.")
            disconnect_vpn()
            continue
        email = email_data["address"]
        email_token = email_data["token"]

        print(f"[✓] Temp email created: {email}")

        full_name = generate_name()
        password = generate_password()

        print("[>] Creating Instagram account...")
        result = create_account(email, email_token, full_name, password)
        if result is None or not result.get("session"):
            print("[x] Account creation failed. Cleaning up.")
            disconnect_vpn()
            continue

        session = result["session"]
        username_created = result["username"]
        print(f"[✓] Account created: @{username_created}")

        print("[>] Submitting report...")
        success = submit_report(session, target_username)
        if success:
            print(f"[✓] Report submitted against @{target_username}")
        else:
            print("[x] Report submission failed.")

        print("[>] Disconnecting VPN...")
        disconnect_vpn()

    print(f"\n[✔] Finished sending {report_count} report(s).")

if __name__ == "__main__":
    main()
