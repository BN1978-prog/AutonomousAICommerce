import subprocess
import sys

def main():
    p = subprocess.run(
        [sys.executable, "-m", "app.autonomous_fulfillment_runner"],
        capture_output=False,
        text=True
    )
    raise SystemExit(p.returncode)

if __name__ == "__main__":
    main()
