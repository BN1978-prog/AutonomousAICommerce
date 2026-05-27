import os, json, requests
from pathlib import Path
from datetime import datetime, timezone

ENV = Path(".env")
for line in ENV.read_text(encoding="utf-8-sig").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k,v = line.split("=",1)
        os.environ[k.strip()] = v.strip()

shop = os.getenv("SHOPIFY_SHOP_DOMAIN") or os.getenv("SHOPIFY_STORE_URL")
token = os.getenv("SHOPIFY_ADMIN_TOKEN") or os.getenv("SHOPIFY_ACCESS_TOKEN")
version = os.getenv("SHOPIFY_API_VERSION","2025-01")

OUT = Path("app/logs/shopify_crm_events.json")

events = []

headers = {
    "X-Shopify-Access-Token": token,
    "Content-Type": "application/json"
}

orders_url = f"https://{shop}/admin/api/{version}/orders.json?status=any&limit=25"
customers_url = f"https://{shop}/admin/api/{version}/customers.json?limit=25"

orders_resp = requests.get(orders_url, headers=headers, timeout=30)
customers_resp = requests.get(customers_url, headers=headers, timeout=30)

orders = orders_resp.json().get("orders", []) if orders_resp.status_code == 200 else []
customers = customers_resp.json().get("customers", []) if customers_resp.status_code == 200 else []

for o in orders:
    email = o.get("email") or (o.get("customer") or {}).get("email")
    if not email:
        continue

    events.append({
        "event_type": "order_confirmation",
        "email": email,
        "customer_id": (o.get("customer") or {}).get("id"),
        "order_id": o.get("id"),
        "order_name": o.get("name"),
        "total_price": o.get("total_price"),
        "created_at": o.get("created_at")
    })

    if o.get("financial_status") in ["paid", "partially_paid"]:
        events.append({
            "event_type": "review_request",
            "email": email,
            "customer_id": (o.get("customer") or {}).get("id"),
            "order_id": o.get("id"),
            "order_name": o.get("name"),
            "created_at": o.get("created_at")
        })

for c in customers:
    email = c.get("email")
    if not email:
        continue

    events.append({
        "event_type": "win_back",
        "email": email,
        "customer_id": c.get("id"),
        "first_name": c.get("first_name"),
        "last_name": c.get("last_name"),
        "created_at": c.get("created_at")
    })

OUT.write_text(json.dumps({
    "created_at": datetime.now(timezone.utc).isoformat(),
    "orders_status": orders_resp.status_code,
    "customers_status": customers_resp.status_code,
    "events_count": len(events),
    "events": events
}, indent=2), encoding="utf-8")

print("Shopify CRM events created:", len(events))
print("Orders status:", orders_resp.status_code)
print("Customers status:", customers_resp.status_code)
print("Output:", OUT)
