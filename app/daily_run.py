import subprocess
from app.run_lock import acquire_lock, release_lock

COMMANDS = [
    ["python", "-m", "app.health_check"],
    ["python", "-m", "app.scheduled_import"],
    ["python", "-m", "app.import_report"],
    ["python", "-m", "app.stock_report"],
    ["python", "-m", "app.blocked_report"],
    ["python", "-m", "app.dashboard_report"],
    ["python", "-m", "app.cleanup_logs"],
]

def run_command(command):
    print()
    print(">>> " + " ".join(command))
    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)

    if result.stderr:
        print("=== ERRORS ===")
        print(result.stderr)

def main():
    acquire_lock()
    print("=== DAILY AUTONOMOUS COMMERCE RUN ===")

    for command in COMMANDS:
        run_command(command)

    print()
    print("=== DAILY RUN COMPLETE ===")
    release_lock()

if __name__ == "__main__":
    main()
