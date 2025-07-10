import csv
from datetime import datetime
import os

HISTORY_FILE = "report_history.csv"

def log_history(email, target_username, reason, status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    is_new = not os.path.exists(HISTORY_FILE)

    with open(HISTORY_FILE, "a", newline='') as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["Timestamp", "Email", "Target", "Reason", "Status"])
        writer.writerow([timestamp, email, target_username, reason, status])
