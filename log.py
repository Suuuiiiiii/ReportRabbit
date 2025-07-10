import os
from datetime import datetime

LOG_FILE = "pdo.log"

def write_log(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}\n"

    with open(LOG_FILE, "a") as f:
        f.write(log_line)

def clear_log():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
