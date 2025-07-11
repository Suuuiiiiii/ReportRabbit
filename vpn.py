import subprocess
import random

def connect_to_random():
    countries = ['US', 'GB', 'CA', 'DE', 'FR', 'NL', 'NO', 'CH', 'SE', 'IT']  # Add/remove as needed
    country = random.choice(countries)
    print(f"[*] Connecting to VPN ({country})...")

    try:
        subprocess.run(["windscribe", "disconnect"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        subprocess.run(["windscribe", "connect", country], check=True)
        print("[✓] VPN connected.")
    except subprocess.CalledProcessError:
        print("[x] VPN connection failed.")
