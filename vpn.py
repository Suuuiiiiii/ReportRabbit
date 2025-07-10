import subprocess

def connect_vpn():
    try:
        result = subprocess.run(["windscribe", "connect", "--fastest"], capture_output=True, text=True)
        return "Connected" in result.stdout or result.returncode == 0
    except Exception as e:
        print(f"[x] VPN connection error: {e}")
        return False

def disconnect_vpn():
    try:
        subprocess.run(["windscribe", "disconnect"], capture_output=True, text=True)
        print("[✓] VPN disconnected.")
    except Exception as e:
        print(f"[x] VPN disconnection error: {e}")
