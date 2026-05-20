from pathlib import Path
import json

ORDERS = Path("app/logs/incoming_orders.json")
BACKUP = Path("app/logs/incoming_orders_TEST_BACKUP.json")

if ORDERS.exists():
    data = json.loads(ORDERS.read_text(encoding="utf-8"))

    BACKUP.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8"
    )

    ORDERS.write_text(
        json.dumps([], indent=2),
        encoding="utf-8"
    )

    print("fake orders moved to backup")
    print("BACKUP:", BACKUP)
else:
    print("incoming_orders.json not found")
