import json
from pathlib import Path

STOCK_STATE_FILE = Path(r"C:\Users\omen\AutonomousAICommerce\app\logs\stock_state.json")

def load_stock_state():
    if not STOCK_STATE_FILE.exists():
        return {}

    try:
        return json.loads(STOCK_STATE_FILE.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}

def save_stock_state(sku, inventory):
    STOCK_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = load_stock_state()
    previous = data.get(sku)

    data[sku] = {
        "inventory": int(inventory)
    }

    STOCK_STATE_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

    return previous

def detect_stock_change(sku, inventory):
    data = load_stock_state()
    previous = data.get(sku)

    if previous is None:
        return {
            "changed": True,
            "previous": None,
            "current": int(inventory)
        }

    previous_inventory = int(previous.get("inventory", 0))
    current_inventory = int(inventory)

    return {
        "changed": previous_inventory != current_inventory,
        "previous": previous_inventory,
        "current": current_inventory
    }
