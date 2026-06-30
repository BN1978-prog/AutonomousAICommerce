
import json
import os
import requests
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv
from app.order_processing_ledger import is_stage_done, mark_stage

load_dotenv(override=True)

PAYLOADS = Path("app/logs/cj_order_payloads.json")
VALIDATION = Path("app/logs/cj_customer_address_validator.json")
LIVE_GATE = Path("app/logs/autonomous_commerce_live_gate_report.json")
OUT = Path("app/logs/cj_purchase_attempts.json")

DRY_RUN = os.getenv("CJ_PURCHASE_DRY_RUN", "true").lower() == "true"
CJ_ACCESS_TOKEN = os.getenv("CJ_ACCESS_TOKEN", "").strip()
CJ_CREATE_ORDER_URL = os.getenv(
    "CJ_CREATE_ORDER_URL",
    "https://developers.cjdropshipping.com/api2.0/v1/shopping/order/createOrderV3"
).strip()

payloads = json.loads(PAYLOADS.read_text(encoding="utf-8-sig")) if PAYLOADS.exists() else []
validation = json.loads(VALIDATION.read_text(encoding="utf-8-sig")) if VALIDATION.exists() else {}
gate = json.loads(LIVE_GATE.read_text(encoding="utf-8-sig")) if LIVE_GATE.exists() else {}

ready_ids = {
    x.get("order_id")
    for x in validation.get("ready", [])
    if x.get("status") == "ready_for_cj_create_order"
}

gate_approved_ids = {
    x.get("order_id")
    for x in gate.get("approved", [])
    if x.get("status") == "approved_for_live_cj_purchase"
}

attempts = []

def create_cj_order(cj_payload):
    headers = {
        "CJ-Access-Token": CJ_ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

    r = requests.post(
        CJ_CREATE_ORDER_URL,
        headers=headers,
        json=cj_payload,
        timeout=60
    )

    try:
        data = r.json()
    except Exception:
        data = {"text": r.text[:3000]}

    return {
        "status_code": r.status_code,
        "response": data
    }

def extract_cj_order_id(response):
    data = response.get("response") or {}

    candidates = [
        data.get("orderId"),
        data.get("order_id"),
        data.get("cjOrderId"),
        data.get("cj_order_id"),
    ]

    result = data.get("result")
    if isinstance(result, dict):
        candidates.extend([
            result.get("orderId"),
            result.get("order_id"),
            result.get("cjOrderId"),
            result.get("cj_order_id"),
        ])

    data_field = data.get("data")
    if isinstance(data_field, dict):
        candidates.extend([
            data_field.get("orderId"),
            data_field.get("order_id"),
            data_field.get("cjOrderId"),
            data_field.get("cj_order_id"),
        ])

    for x in candidates:
        if x:
            return str(x)

    return None

def cj_success(response):
    data = response.get("response") or {}
    if response.get("status_code") not in [200, 201]:
        return False
    if data.get("code") in [200, "200"]:
        return True
    if data.get("success") is True:
        return True
    if data.get("result") is True:
        return True
    if isinstance(data.get("result"), dict):
        return True
    return False

for payload in payloads:
    order_id = payload.get("order_id")
    sku = payload.get("sku")
    channel = payload.get("channel")

    if is_stage_done(order_id, sku, channel, "cj_order_created_live"):
        attempts.append({
            "ok": False,
            "dry_run": DRY_RUN,
            "status": "skipped_already_live_cj_order_created_in_ledger",
            "order_id": order_id,
            "sku": sku
        })
        continue

    if is_stage_done(order_id, sku, channel, "cj_purchase_attempted") and DRY_RUN:
        attempts.append({
            "ok": False,
            "dry_run": DRY_RUN,
            "status": "skipped_already_purchase_attempted_in_ledger",
            "order_id": order_id,
            "sku": sku
        })
        continue

    if order_id not in ready_ids:
        attempts.append({
            "ok": False,
            "dry_run": DRY_RUN,
            "status": "blocked_not_address_validated",
            "order_id": order_id,
            "sku": sku
        })
        continue

    cj_payload = {
        "payType": payload.get("payType", 3),
        "products": payload.get("products", []),
        "shippingAddress": payload.get("shipping_address", {}),
        "orderNumber": str(order_id),
        "remark": f"AICommerce {channel} {payload.get('channel_order_name') or ''}".strip()
    }

    if DRY_RUN:
        row = {
            "ok": True,
            "dry_run": True,
            "status": "prepared_not_purchased",
            "supplier": "cj",
            "order_id": order_id,
            "sku": sku,
            "payload": cj_payload,
            "financials": payload.get("financials", {}),
            "prepared_at": datetime.now(timezone.utc).isoformat()
        }
        attempts.append(row)
        mark_stage(order_id, sku, channel, "cj_purchase_attempted", row)
        continue

    if order_id not in gate_approved_ids:
        attempts.append({
            "ok": False,
            "dry_run": False,
            "status": "blocked_by_live_gate",
            "supplier": "cj",
            "order_id": order_id,
            "sku": sku,
            "payload": cj_payload,
            "financials": payload.get("financials", {}),
            "gate_status": gate.get("status"),
            "blocked_at": datetime.now(timezone.utc).isoformat()
        })
        continue

    if not CJ_ACCESS_TOKEN:
        attempts.append({
            "ok": False,
            "dry_run": False,
            "status": "blocked_missing_cj_access_token",
            "supplier": "cj",
            "order_id": order_id,
            "sku": sku,
            "payload": cj_payload,
            "financials": payload.get("financials", {}),
            "blocked_at": datetime.now(timezone.utc).isoformat()
        })
        continue

    api_result = create_cj_order(cj_payload)
    cj_order_id = extract_cj_order_id(api_result)
    ok = cj_success(api_result)

    row = {
        "ok": ok,
        "dry_run": False,
        "status": "live_cj_order_created" if ok else "live_cj_order_failed",
        "supplier": "cj",
        "order_id": order_id,
        "sku": sku,
        "cj_order_id": cj_order_id,
        "payload": cj_payload,
        "financials": payload.get("financials", {}),
        "api_result": api_result,
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    attempts.append(row)

    if ok:
        mark_stage(order_id, sku, channel, "cj_order_created_live", row)

OUT.write_text(json.dumps(attempts, indent=2, ensure_ascii=False), encoding="utf-8")

print("CJ PURCHASE ATTEMPTS:", len(attempts))
print("DRY_RUN:", DRY_RUN)
print("REPORT:", OUT)
