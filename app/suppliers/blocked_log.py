import json
from datetime import datetime
from pathlib import Path

BLOCKED_FILE = Path(r"C:\Users\omen\AutonomousAICommerce\app\logs\blocked_products.json")

def log_blocked_product(raw, normalized, safety):
    BLOCKED_FILE.parent.mkdir(parents=True, exist_ok=True)

    if BLOCKED_FILE.exists():
        try:
            data = json.loads(BLOCKED_FILE.read_text(encoding="utf-8-sig"))
        except Exception:
            data = []
    else:
        data = []

    data.append({
        "timestamp": datetime.now().isoformat(),
        "sku": normalized.get("sku"),
        "issues": safety.get("issues", []),
        "profit": safety.get("profit"),
        "margin_percent": safety.get("margin_percent"),
        "raw": raw,
        "normalized": normalized
    })

    BLOCKED_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
