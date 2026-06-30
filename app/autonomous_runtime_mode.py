
import json
import os
from pathlib import Path
from datetime import datetime, timezone

CONFIG = Path("app/logs/autonomous_commerce_live_gate.json")
OUT = Path("app/logs/autonomous_runtime_mode.json")

default_config = {
    "live_mode": False,
    "cj_live_purchase_enabled": False,
    "shopify_fulfillment_live_enabled": False
}

config = json.loads(CONFIG.read_text(encoding="utf-8-sig")) if CONFIG.exists() else default_config

live_mode = bool(config.get("live_mode"))
cj_live = bool(config.get("cj_live_purchase_enabled"))
shopify_fulfillment_live = bool(config.get("shopify_fulfillment_live_enabled"))

runtime = {
    "CJ_PURCHASE_DRY_RUN": "false" if live_mode and cj_live else "true",
    "SHOPIFY_FULFILLMENT_DRY_RUN": "false" if live_mode and shopify_fulfillment_live else "true"
}

for k, v in runtime.items():
    os.environ[k] = v

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "status": "AUTONOMOUS_RUNTIME_MODE_SET",
    "live_mode": live_mode,
    "cj_live_purchase_enabled": cj_live,
    "shopify_fulfillment_live_enabled": shopify_fulfillment_live,
    "runtime": runtime,
    "note": "This module sets runtime mode for the current process. Subprocess runners should also read live gate directly."
}

OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(report, indent=2, ensure_ascii=False))
