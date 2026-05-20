import os
import json
import base64
import requests
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlparse

ENV=Path(".env")
OUT=Path("app/logs/token_manager_status.json")

def now():
    return datetime.now(timezone.utc).isoformat()

def load_env():
    if not ENV.exists():
        return

    for line in ENV.read_text(encoding="utf-8").splitlines():
        line=line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        k,v=line.split("=",1)
        os.environ[k.strip()]=v.strip().strip('"').strip("'")

def save_env_var(key,value):
    lines=[]

    if ENV.exists():
        lines=ENV.read_text(encoding="utf-8").splitlines()

    lines=[
        line for line in lines
        if not line.startswith(key+"=")
    ]

    lines.append(f"{key}={value}")

    ENV.write_text(
        "\n".join(lines)+"\n",
        encoding="utf-8"
    )

def shop_domain(value):
    if not value:
        return None

    if value.startswith("http://") or value.startswith("https://"):
        return urlparse(value).netloc.rstrip("/")

    return value.strip().strip("/")

def row(provider,ok,status,extra=None):
    r={
        "provider":provider,
        "ok":ok,
        "status":status,
        "checked_at":now()
    }

    if extra:
        r.update(extra)

    return r

load_env()

results=[]

# Shopify
try:
    shop=shop_domain(
        os.getenv("SHOPIFY_STORE_URL")
        or os.getenv("SHOPIFY_SHOP")
    )

    token=(
        os.getenv("SHOPIFY_ACCESS_TOKEN")
        or os.getenv("SHOPIFY_ADMIN_TOKEN")
        or os.getenv("SHOPIFY_ADMIN_ACCESS_TOKEN")
    )

    api_version=os.getenv("SHOPIFY_API_VERSION","2025-01")

    if not shop or not token:
        results.append(row(
            "shopify",
            False,
            "missing_shop_or_token",
            {
                "can_auto_refresh":False,
                "action":"add_valid_shopify_admin_token"
            }
        ))
    else:
        r=requests.get(
            f"https://{shop}/admin/api/{api_version}/shop.json",
            headers={
                "X-Shopify-Access-Token":token,
                "Content-Type":"application/json"
            },
            timeout=30
        )

        results.append(row(
            "shopify",
            200 <= r.status_code < 300,
            "token_valid" if 200 <= r.status_code < 300 else "token_invalid_needs_new_admin_token",
            {
                "status_code":r.status_code,
                "can_auto_refresh":False,
                "response":r.text[:500] if r.status_code>=300 else ""
            }
        ))

except Exception as e:
    results.append(row("shopify",False,"error",{"error":str(e)}))

# WooCommerce
try:
    woo_url=(
        os.getenv("WOOCOMMERCE_STORE_URL")
        or os.getenv("WOO_STORE_URL")
        or os.getenv("WC_STORE_URL")
    )

    ck=(
        os.getenv("WOOCOMMERCE_CONSUMER_KEY")
        or os.getenv("WOO_CONSUMER_KEY")
        or os.getenv("WC_CONSUMER_KEY")
    )

    cs=(
        os.getenv("WOOCOMMERCE_CONSUMER_SECRET")
        or os.getenv("WOO_CONSUMER_SECRET")
        or os.getenv("WC_CONSUMER_SECRET")
    )

    if not woo_url or not ck or not cs:
        results.append(row(
            "woocommerce",
            False,
            "missing_consumer_key_or_secret",
            {
                "can_auto_refresh":False,
                "action":"create_new_woocommerce_rest_api_key"
            }
        ))
    else:
        r=requests.get(
            f"{woo_url.rstrip('/')}/wp-json/wc/v3/products",
            auth=(ck,cs),
            params={"per_page":1},
            timeout=30
        )

        results.append(row(
            "woocommerce",
            200 <= r.status_code < 300,
            "keys_valid" if 200 <= r.status_code < 300 else "keys_invalid_needs_new_key",
            {
                "status_code":r.status_code,
                "can_auto_refresh":False,
                "response":r.text[:500] if r.status_code>=300 else ""
            }
        ))

except Exception as e:
    results.append(row("woocommerce",False,"error",{"error":str(e)}))

# eBay
try:
    refresh=os.getenv("EBAY_REFRESH_TOKEN")
    client_id=os.getenv("EBAY_CLIENT_ID")
    client_secret=os.getenv("EBAY_CLIENT_SECRET")

    scope=os.getenv(
        "EBAY_SCOPE",
        "https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/sell.inventory https://api.ebay.com/oauth/api_scope/sell.fulfillment"
    )

    if not refresh or not client_id or not client_secret:
        results.append(row(
            "ebay",
            False,
            "missing_refresh_token_or_client_credentials",
            {
                "can_auto_refresh":False,
                "missing":[
                    k for k,v in {
                        "EBAY_REFRESH_TOKEN":refresh,
                        "EBAY_CLIENT_ID":client_id,
                        "EBAY_CLIENT_SECRET":client_secret
                    }.items()
                    if not v
                ],
                "action":"complete_ebay_oauth_once"
            }
        ))
    else:
        basic=base64.b64encode(
            f"{client_id}:{client_secret}".encode()
        ).decode()

        r=requests.post(
            "https://api.ebay.com/identity/v1/oauth2/token",
            headers={
                "Authorization":f"Basic {basic}",
                "Content-Type":"application/x-www-form-urlencoded"
            },
            data={
                "grant_type":"refresh_token",
                "refresh_token":refresh,
                "scope":scope
            },
            timeout=30
        )

        if r.status_code==200:
            data=r.json()
            access=data.get("access_token")

            if access:
                save_env_var("EBAY_ACCESS_TOKEN",access)

            results.append(row(
                "ebay",
                True,
                "access_token_refreshed",
                {
                    "can_auto_refresh":True,
                    "expires_in":data.get("expires_in"),
                    "env_updated":"EBAY_ACCESS_TOKEN"
                }
            ))
        else:
            results.append(row(
                "ebay",
                False,
                "refresh_failed_needs_reauth",
                {
                    "can_auto_refresh":False,
                    "status_code":r.status_code,
                    "response":r.text[:800]
                }
            ))

except Exception as e:
    results.append(row("ebay",False,"error",{"error":str(e)}))

# Google Ads
try:
    refresh=os.getenv("GOOGLE_ADS_REFRESH_TOKEN")
    client_id=os.getenv("GOOGLE_ADS_CLIENT_ID")
    client_secret=os.getenv("GOOGLE_ADS_CLIENT_SECRET")

    if not refresh or not client_id or not client_secret:
        results.append(row(
            "google_ads",
            False,
            "missing_refresh_token_or_client_credentials",
            {
                "can_auto_refresh":False,
                "missing":[
                    k for k,v in {
                        "GOOGLE_ADS_REFRESH_TOKEN":refresh,
                        "GOOGLE_ADS_CLIENT_ID":client_id,
                        "GOOGLE_ADS_CLIENT_SECRET":client_secret
                    }.items()
                    if not v
                ],
                "action":"complete_google_oauth_once"
            }
        ))
    else:
        r=requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id":client_id,
                "client_secret":client_secret,
                "refresh_token":refresh,
                "grant_type":"refresh_token"
            },
            timeout=30
        )

        if r.status_code==200:
            data=r.json()
            access=data.get("access_token")

            if access:
                save_env_var("GOOGLE_ADS_ACCESS_TOKEN",access)

            results.append(row(
                "google_ads",
                True,
                "access_token_refreshed",
                {
                    "can_auto_refresh":True,
                    "expires_in":data.get("expires_in"),
                    "env_updated":"GOOGLE_ADS_ACCESS_TOKEN"
                }
            ))
        else:
            results.append(row(
                "google_ads",
                False,
                "refresh_failed_needs_reauth",
                {
                    "can_auto_refresh":False,
                    "status_code":r.status_code,
                    "response":r.text[:800]
                }
            ))

except Exception as e:
    results.append(row("google_ads",False,"error",{"error":str(e)}))

# Meta
try:
    token=os.getenv("META_ACCESS_TOKEN")
    app_id=os.getenv("META_APP_ID")
    app_secret=os.getenv("META_APP_SECRET")

    if not token:
        results.append(row(
            "meta",
            False,
            "missing_token_needs_reauth",
            {
                "can_auto_refresh":False,
                "action":"generate_new_meta_token"
            }
        ))

    elif app_id and app_secret:
        r=requests.get(
            "https://graph.facebook.com/v19.0/oauth/access_token",
            params={
                "grant_type":"fb_exchange_token",
                "client_id":app_id,
                "client_secret":app_secret,
                "fb_exchange_token":token
            },
            timeout=30
        )

        if r.status_code==200:
            data=r.json()
            new_token=data.get("access_token")

            if new_token:
                save_env_var("META_ACCESS_TOKEN",new_token)

            results.append(row(
                "meta",
                True,
                "token_exchanged_or_extended",
                {
                    "can_auto_refresh":True,
                    "expires_in":data.get("expires_in"),
                    "env_updated":"META_ACCESS_TOKEN"
                }
            ))
        else:
            results.append(row(
                "meta",
                False,
                "refresh_failed_needs_reauth",
                {
                    "can_auto_refresh":False,
                    "status_code":r.status_code,
                    "response":r.text[:800]
                }
            ))
    else:
        r=requests.get(
            "https://graph.facebook.com/v19.0/me",
            params={
                "access_token":token,
                "fields":"id,name"
            },
            timeout=30
        )

        results.append(row(
            "meta",
            200 <= r.status_code < 300,
            "token_valid_but_no_app_secret_for_auto_refresh"
            if 200 <= r.status_code < 300
            else "invalid_token_needs_reauth",
            {
                "can_auto_refresh":False,
                "status_code":r.status_code,
                "response":r.text[:800]
            }
        ))

except Exception as e:
    results.append(row("meta",False,"error",{"error":str(e)}))

summary={
    "created_at":now(),
    "commerce_channels_ok":all(
        x["ok"] for x in results
        if x["provider"] in ["shopify","woocommerce","ebay"]
    ),
    "paid_ads_ok":all(
        x["ok"] for x in results
        if x["provider"] in ["google_ads","meta"]
    ),
    "results":results
}

OUT.write_text(json.dumps(summary,indent=2),encoding="utf-8")

print(json.dumps(summary,indent=2))
