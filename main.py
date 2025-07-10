import time
from vpn import connect_to_vpn
from mailtm import get_temp_email
from account_creator import create_account
from reporter import display_banner

# Configuration
TARGET_USERNAME = "target_account_here"  # replace this
REPORT_REASON = "Nudity or sexual activity"
REPORT_COUNT = 1  # how many reports to attempt

def main():
    success = 0
    fail = 0

    display_banner()

    for i in range(1, REPORT_COUNT + 1):
        print(f"\n[•] Starting Report #{i}")

        try:
            print("[*] Connecting to VPN...")
            connect_to_vpn()
            time.sleep(5)

            email_info = get_temp_email()
            if not email_info:
                print("[x] Failed to get temp email.")
                fail += 1
                continue

            print(f"[✓] Temp email created: {email_info['address']}")

            full_name = "John Doe"
            password = "StrongP@ssword123"

            result = create_account(
                email_info["address"],
                email_info["token"],
                full_name,
                password,
                TARGET_USERNAME,
                REPORT_REASON
            )

            if result:
                print("[✓] Report successfully submitted.")
                success += 1
            else:
                print("[x] Failed to create Instagram account.")
                fail += 1

        except KeyboardInterrupt:
            print("\n[x] Interrupted.")
            break

    print(f"\n[✓] Done! Success: {success}, Failed: {fail}")

if __name__ == "__main__":
    main()
