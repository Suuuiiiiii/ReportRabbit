import os
import time
from ASCII import show_banner
from reporter import perform_report

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def ask(prompt, choices):
    while True:
        print(f"\n{prompt}")
        for i, choice in enumerate(choices, 1):
            print(f"{i}. {choice}")
        try:
            answer = int(input("\n> "))
            if 1 <= answer <= len(choices):
                return choices[answer - 1]
        except:
            continue
        print("[x] Invalid choice. Try again.")

def main():
    clear()
    show_banner()

    platform = ask("Choose platform to report on:", ["Instagram"])

    reason = ask("Choose report reason:", ["Nudity or sexual activity"])

    while True:
        target_username = input("\nEnter target username: @").strip().lstrip("@")
        if not target_username:
            print("[x] Username cannot be empty.")
            continue

        try:
            count = int(input("\nHow many reports to send? > "))
        except ValueError:
            print("[x] Invalid number.")
            continue

        success = 0
        for i in range(count):
            print(f"\n[•] Starting Report #{i+1}")
            result = perform_report(target_username, reason)
            if result:
                success += 1
                print(f"[✓] Report #{i+1} complete.")
            else:
                print(f"[x] Report #{i+1} failed.")
            print(f"\n| {success} |")
            time.sleep(2)

        print(f"\n[✓] Done! Success: {success}, Failed: {count - success}\n")
        again = input("Do you want to report another target? (y/n) > ").strip().lower()
        if again != "y":
            break
        clear()
        show_banner()

if __name__ == "__main__":
    main()
