import subprocess
import random
import time

# List of recommended Windscribe locations
WIND_LOCATIONS = [
    "US", "CA", "FR", "DE", "NL", "GB", "NO", "RO", "UA", "SG"
]

def is_windscribe_installed():
    try:
        subprocess.run(["windscribe", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

def is_logged_in():
    try:
        result = subprocess.run(["windscribe", "account"], capture_output=True, text=True)
        return "Account" in result.stdout
    except:
        return False

def connect_vpn():
    if not is_windscribe_installed():
        print("[x] Windscribe CLI not found.")
        return False

    if not is_logged_in():
        print("[x] You must log in to Windscribe before using this tool.")
        return False

    location = random.choice(WIND_LOCATIONS)
    try:
        print(f"[*] Connecting to Windscribe VPN ({location})...")
        subprocess.run(["windscribe", "connect", location], stdout=subprocess.DEVNULL)
        time.sleep(2)
        return True
    except Exception as e:
        print(f"[x] VPN connection failed: {e}")
        return False

def disconnect_vpn():
    try:
        subprocess.run(["windscribe", "disconnect"], stdout=subprocess.DEVNULL)
        time.sleep(1)
        return True
    except:
        return False
