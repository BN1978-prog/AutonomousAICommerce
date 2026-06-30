
import json
from pathlib import Path
from datetime import datetime, timezone

LEDGER = Path("app/logs/order_processing_ledger.json")

def load_ledger():
    if not LEDGER.exists():
        return {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "orders": {}
        }
    try:
        return json.loads(LEDGER.read_text(encoding="utf-8-sig"))
    except Exception:
        return {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "orders": {}
        }

def save_ledger(ledger):
    ledger["updated_at"] = datetime.now(timezone.utc).isoformat()
    LEDGER.write_text(json.dumps(ledger, indent=2, ensure_ascii=False), encoding="utf-8")

def key(order_id, sku, channel):
    return f"{channel}:{order_id}:{sku}"

def is_stage_done(order_id, sku, channel, stage):
    ledger = load_ledger()
    k = key(order_id, sku, channel)
    return bool(ledger.get("orders", {}).get(k, {}).get("stages", {}).get(stage))

def mark_stage(order_id, sku, channel, stage, data=None):
    ledger = load_ledger()
    k = key(order_id, sku, channel)
    ledger.setdefault("orders", {}).setdefault(k, {
        "order_id": order_id,
        "sku": sku,
        "channel": channel,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "stages": {}
    })
    ledger["orders"][k]["stages"][stage] = {
        "done": True,
        "at": datetime.now(timezone.utc).isoformat(),
        "data": data or {}
    }
    save_ledger(ledger)

def main():
    ledger = load_ledger()
    save_ledger(ledger)
    print(json.dumps({
        "status": "ORDER_PROCESSING_LEDGER_READY",
        "orders": len(ledger.get("orders", {})),
        "file": str(LEDGER)
    }, indent=2))

if __name__ == "__main__":
    main()
