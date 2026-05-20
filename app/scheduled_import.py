import subprocess
from datetime import datetime

def main():
    print("=== SCHEDULED IMPORT START ===")
    print(datetime.now())

    result = subprocess.run(
        ["python", "-m", "app.import_supplier_products"],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.stderr:
        print("=== ERRORS ===")
        print(result.stderr)

    print("=== SCHEDULED IMPORT END ===")

if __name__ == "__main__":
    main()
