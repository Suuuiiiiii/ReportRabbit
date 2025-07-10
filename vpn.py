import subprocess
import random
import time

# Recommended Windscribe server locations
WIND_LOCATIONS = [
    "US", "CA", "FR", "DE", "GB", "NL", "NO", "RO", "SG", "TR"
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
        print("[x] Windscribe not logged in. Please run 'windscribe login' first.")
        return False

    location = random.choice(WIND_LOCATIONS)
    try:
        print(f"[*] Connecting to VPN ({location})...")
        subprocess.run(["windscribe", "connect", location], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)
        return True
    except Exception as e:
        print(f"[x] VPN connection failed: {e}")
        return False

def disconnect_vpn():
    try:
        subprocess.run(["windscribe", "disconnect"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1)
        return True
    except:
        return False
