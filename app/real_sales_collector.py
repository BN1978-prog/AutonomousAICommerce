import os
import json
import requests
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime, timezone, timedelta

ENV=Path(".env")
REGISTRY=Path("app/logs/imported_skus.json")
OUT=Path("app/logs/real_sales_report.json")

def load_env(path):
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line=line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k,v=line.split("=",1)
        os.environ[k.strip()]=v.strip().strip('"').strip("'")

def norm_shop(value):
    if value.startswith("http://") or value.startswith("https://"):
        return urlparse(value).netloc.rstrip("/")
    return value.strip().strip("/")

load_env(ENV)

registry=json.loads(REGISTRY.read_text(encoding="utf-8"))

sales_by_sku={}

def add_sale(sku,channel,qty,revenue,currency=None):
    if not sku or qty<=0:
        return
    if not sku:
        return

    sales_by_sku.setdefault(sku,{
        "sku":sku,
        "total_quantity":0,
        "total_revenue":0.0,
        "channels":{}
    })

    sales_by_sku[sku]["total_quantity"]+=qty
    sales_by_sku[sku]["total_revenue"]+=revenue

    sales_by_sku[sku]["channels"].setdefault(channel,{
        "quantity":0,
        "revenue":0.0,
        "currency":currency
    })

    sales_by_sku[sku]["channels"][channel]["quantity"]+=qty
    sales_by_sku[sku]["channels"][channel]["revenue"]+=revenue

# Shopify orders
try:
    shop=norm_shop(os.getenv("SHOPIFY_STORE_URL"))
    token=os.getenv("SHOPIFY_ACCESS_TOKEN") or os.getenv("SHOPIFY_ADMIN_TOKEN")
    api_version=os.getenv("SHOPIFY_API_VERSION","2025-01")

    url=f"https://{shop}/admin/api/{api_version}/orders.json"

    params={
        "status":"any",
        "limit":250,
        "created_at_min":(
            datetime.now(timezone.utc)-timedelta(days=30)
        ).isoformat(),
        "fields":"id,name,currency,line_items"
    }

    r=requests.get(
        url,
        headers={"X-Shopify-Access-Token":token},
        params=params,
        timeout=30
    )

    if r.status_code==200:
        for order in r.json().get("orders",[]):
            currency=order.get("currency")
            for line in order.get("line_items",[]):
                sku=line.get("sku")
                qty=int(line.get("quantity") or 0)
                price=float(line.get("price") or 0)
                add_sale(sku,"shopify",qty,qty*price,currency)
except Exception as e:
    pass

# eBay offers / soldQuantity
try:
    ebay_token=(
        os.getenv("EBAY_ACCESS_TOKEN")
        or os.getenv("EBAY_OAUTH_TOKEN")
        or os.getenv("EBAY_USER_TOKEN")
    )

    ebay_base=os.getenv("EBAY_API_BASE","https://api.ebay.com")

    headers={
        "Authorization":f"Bearer {ebay_token}",
        "Accept":"application/json",
        "Content-Language":"en-US",
        "X-EBAY-C-MARKETPLACE-ID":"EBAY_US"
    }

    for sku,item in registry.items():
        offer_id=item.get("ebay_offer_id")
        if not offer_id:
            continue

        r=requests.get(
            f"{ebay_base}/sell/inventory/v1/offer/{offer_id}",
            headers=headers,
            timeout=30
        )

        if r.status_code!=200:
            continue

        offer=r.json()
        listing=offer.get("listing") or {}
        sold=int(listing.get("soldQuantity") or 0)

        price_data=(
            offer.get("pricingSummary",{})
            .get("price",{})
        )

        price=float(price_data.get("value") or 0)
        currency=price_data.get("currency")

        add_sale(sku,"ebay",sold,sold*price,currency)
except Exception as e:
    pass

# WooCommerce products total_sales
try:
    woo_url=(
        os.getenv("WOOCOMMERCE_STORE_URL")
        or os.getenv("WOO_STORE_URL")
        or os.getenv("WC_STORE_URL")
    ).rstrip("/")

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

    page=1

    while True:
        r=requests.get(
            f"{woo_url}/wp-json/wc/v3/products",
            auth=(ck,cs),
            params={"per_page":100,"page":page},
            timeout=30
        )

        if r.status_code!=200:
            break

        products=r.json()

        if not products:
            break

        for p in products:
            sku=p.get("sku")
            sold=int(p.get("total_sales") or 0)
            price=float(p.get("price") or 0)
            add_sale(sku,"woocommerce",sold,sold*price,None)

        page+=1

except Exception as e:
    pass

report={
    "created_at":datetime.now(timezone.utc).isoformat(),
    "sku_count":len(sales_by_sku),
    "total_quantity":sum(x["total_quantity"] for x in sales_by_sku.values()),
    "total_revenue":round(sum(x["total_revenue"] for x in sales_by_sku.values()),2),
    "items":list(sales_by_sku.values())
}

OUT.write_text(json.dumps(report,indent=2),encoding="utf-8")

print("REAL SALES SKU:",report["sku_count"])
print("TOTAL QTY:",report["total_quantity"])
print("TOTAL REVENUE:",report["total_revenue"])
