import os, json, requests
from pathlib import Path
from datetime import datetime, timezone

ENV = Path(".env")

def load_env():
    data = {}
    for line in ENV.read_text(encoding="utf-8-sig").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1)
            data[k.strip()] = v.strip()
    return data

def update_env(updates):
    lines = ENV.read_text(encoding="utf-8-sig").splitlines()
    seen = set()
    out = []

    for line in lines:
        if "=" in line and not line.strip().startswith("#"):
            k = line.split("=", 1)[0].strip()
            if k in updates:
                out.append(f"{k}={updates[k]}")
                seen.add(k)
            else:
                out.append(line)
        else:
            out.append(line)

    for k, v in updates.items():
        if k not in seen:
            out.append(f"{k}={v}")

    ENV.write_text("\n".join(out) + "\n", encoding="utf-8")

env = load_env()

shop = (
    env.get("SHOPIFY_SHOP_DOMAIN")
    or env.get("SHOPIFY_STORE_URL")
    or "aicommerce-test-store-2.myshopify.com"
).replace("https://", "").replace("http://", "").strip("/")

if not shop.endswith(".myshopify.com"):
    shop = shop + ".myshopify.com"

client_id = env.get("SHOPIFY_CLIENT_ID")
client_secret = env.get("SHOPIFY_CLIENT_SECRET")
version = env.get("SHOPIFY_API_VERSION", "2025-01")

if not client_id or not client_secret:
    print(json.dumps({
        "status": "SHOPIFY_TOKEN_REFRESH_FAILED",
        "reason": "Missing SHOPIFY_CLIENT_ID or SHOPIFY_CLIENT_SECRET"
    }, indent=2))
    raise SystemExit(1)

body = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret
}

url = f"https://{shop}/admin/oauth/access_token"

r = requests.post(
    url,
    json=body,
    headers={"Content-Type": "application/json"},
    timeout=30
)

result = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "shop": shop,
    "token_endpoint_status": r.status_code,
    "status": "UNKNOWN"
}

try:
    payload = r.json()
except Exception:
    payload = {"raw": r.text}

token = (
    payload.get("access_token")
    or payload.get("accessToken")
    or payload.get("token")
)

if r.status_code not in [200, 201] or not token:
    result["status"] = "SHOPIFY_TOKEN_REFRESH_FAILED"
    result["response"] = payload
    Path("app/logs/shopify_token_refresh.json").write_text(
        json.dumps(result, indent=2),
        encoding="utf-8"
    )
    print(json.dumps(result, indent=2))
    raise SystemExit(1)

update_env({
    "SHOPIFY_ADMIN_TOKEN": token,
    "SHOPIFY_ACCESS_TOKEN": token
})

test = requests.get(
    f"https://{shop}/admin/api/{version}/products.json?limit=1",
    headers={"X-Shopify-Access-Token": token},
    timeout=30
)

result["products_test_status"] = test.status_code
result["status"] = "SHOPIFY_TOKEN_REFRESH_OK" if test.status_code == 200 else "SHOPIFY_TOKEN_REFRESHED_BUT_TEST_FAILED"

Path("app/logs/shopify_token_refresh.json").write_text(
    json.dumps(result, indent=2),
    encoding="utf-8"
)

print(json.dumps(result, indent=2))
