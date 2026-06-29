
import json
import os
import re
import time
import requests
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

REGISTRY = Path("app/logs/imported_skus.json")
OUT = Path("app/logs/cj_product_discovery_importer.json")

CJ_API_BASE = os.getenv("CJ_API_URL", "https://developers.cjdropshipping.com/api2.0/v1").rstrip("/")
CJ_ACCESS_TOKEN = os.getenv("CJ_ACCESS_TOKEN", "").strip()

KEYWORD = os.getenv("CJ_DISCOVERY_KEYWORD", "").strip()
KEYWORDS_FILE = Path("app/logs/cj_discovery_keywords.txt")
BLACKLIST_FILE = Path("app/logs/cj_discovery_blacklist.txt")
MAX_IMPORT = int(os.getenv("CJ_DISCOVERY_MAX_IMPORT", "5"))
MIN_PROFIT_GBP = float(os.getenv("CJ_MIN_PROFIT_GBP", "5"))
MARKUP_MULTIPLIER = float(os.getenv("CJ_MARKUP_MULTIPLIER", "2.4"))
DEFAULT_SHIPPING_COST = float(os.getenv("CJ_DEFAULT_SHIPPING_COST", "2.99"))
COUNTRY_CODE = os.getenv("CJ_MAPPER_COUNTRY", "GB").strip().upper()

headers = {
    "CJ-Access-Token": CJ_ACCESS_TOKEN,
    "Content-Type": "application/json"
}

def to_float(v, default=0.0):
    try:
        if isinstance(v, str) and "--" in v:
            v = v.split("--", 1)[0].strip()
        return float(v or default)
    except Exception:
        return default

def money(v):
    return round(float(v or 0), 2)

def search_cj(keyword):
    url = CJ_API_BASE + "/product/list"
    params = {
        "pageNum": 1,
        "pageSize": 20,
        "productName": keyword
    }
    r = requests.get(url, headers=headers, params=params, timeout=30)
    return r.status_code, r.json()

def get_detail(pid):
    url = CJ_API_BASE + f"/product/query?pid={pid}"
    r = requests.get(url, headers=headers, timeout=30)
    return r.status_code, r.json()

def pick_variant(detail_data):
    variants = detail_data.get("variants") or []
    if not variants:
        return None
    return sorted(variants, key=lambda v: to_float(v.get("variantSellPrice")))[0]

def load_lines(path):
    if not path.exists():
        return []
    return [x.strip().lower().replace("\ufeff", "") for x in path.read_text(encoding="utf-8-sig", errors="ignore").splitlines() if x.strip()]

def blocked_text(text, blacklist):
    t = str(text or "").lower()
    return any(b in t for b in blacklist)

def relevance_score(title, keyword):
    title_words = set(re.findall(r"[a-z0-9]+", str(title or "").lower()))
    key_words = [w for w in re.findall(r"[a-z0-9]+", str(keyword or "").lower()) if len(w) > 2]
    return sum(1 for w in key_words if w in title_words)

def clean_title(v):
    v = str(v or "").strip()
    v = re.sub(r"\s+", " ", v)
    return v[:140]

def make_sku(product_sku, variant_sku):
    base = variant_sku or product_sku
    return str(base).strip()

def main():
    if not CJ_ACCESS_TOKEN:
        report = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "status": "CJ_DISCOVERY_MISSING_TOKEN",
            "imported": 0
        }
        OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps(report, indent=2))
        return

    registry = json.loads(REGISTRY.read_text(encoding="utf-8-sig")) if REGISTRY.exists() else {}

    blacklist = load_lines(BLACKLIST_FILE)

    if KEYWORD:
        keywords = [KEYWORD.lower()]
    else:
        keywords = load_lines(KEYWORDS_FILE)

    if not keywords:
        keywords = ["home organizer", "kitchen gadget", "travel accessory"]

    all_cj_items = []
    searches = []

    for keyword in keywords:
        status_code, search = search_cj(keyword)
        cj_items = (((search or {}).get("data") or {}).get("list") or [])
        searches.append({
            "keyword": keyword,
            "status_code": status_code,
            "total": (((search or {}).get("data") or {}).get("total")),
            "returned": len(cj_items)
        })

        for x in cj_items:
            x["_discovery_keyword"] = keyword
            all_cj_items.append(x)

        time.sleep(0.8)

    cj_items = all_cj_items
    status_code = 200

    imported = 0
    skipped = []
    imported_rows = []

    for item in cj_items:
        if imported >= MAX_IMPORT:
            break

        keyword = item.get("_discovery_keyword") or KEYWORD or ""
        pid = item.get("pid")
        if not pid:
            continue

        countries = item.get("shippingCountryCodes") or []
        if countries and COUNTRY_CODE not in countries and "CN" not in countries and "CN_US" not in countries:
            skipped.append({"pid": pid, "reason": "country_not_supported", "countries": countries})
            continue

        title_for_filter = item.get("productNameEn") or item.get("productName") or ""
        if blocked_text(title_for_filter, blacklist):
            skipped.append({"pid": pid, "reason": "blacklisted_title", "title": title_for_filter[:160]})
            continue

        if relevance_score(title_for_filter, keyword) < 1:
            skipped.append({"pid": pid, "reason": "low_relevance", "keyword": keyword, "title": title_for_filter[:160]})
            continue

        detail_status, detail = get_detail(pid)
        detail_data = (detail.get("data") or {}) if isinstance(detail, dict) else {}

        variant = pick_variant(detail_data)
        if not variant:
            skipped.append({"pid": pid, "reason": "no_variant"})
            continue

        product_sku = detail_data.get("productSku") or item.get("productSku")
        variant_sku = variant.get("variantSku")
        sku = make_sku(product_sku, variant_sku)

        if not sku:
            skipped.append({"pid": pid, "reason": "missing_sku"})
            continue

        if sku in registry:
            skipped.append({"sku": sku, "pid": pid, "reason": "already_exists"})
            continue

        supplier_cost = money(variant.get("variantSellPrice") or detail_data.get("sellPrice") or item.get("sellPrice"))
        shipping_cost = 0.0 if item.get("isFreeShipping") else DEFAULT_SHIPPING_COST
        sale_price = money((supplier_cost + shipping_cost) * MARKUP_MULTIPLIER)
        estimated_profit = money(sale_price - supplier_cost - shipping_cost)
        margin_percent = round((estimated_profit / sale_price) * 100, 2) if sale_price else 0

        if estimated_profit < MIN_PROFIT_GBP:
            skipped.append({
                "sku": sku,
                "pid": pid,
                "reason": "profit_too_low",
                "estimated_profit": estimated_profit
            })
            continue

        title = clean_title(detail_data.get("productNameEn") or item.get("productNameEn") or item.get("productName"))

        if blocked_text(title + " " + str(detail_data.get("description") or ""), blacklist):
            skipped.append({"sku": sku, "pid": pid, "reason": "blacklisted_detail", "title": title[:160]})
            continue
        image = detail_data.get("bigImage") or item.get("productImage")

        registry[sku] = {
            "status": "cj_discovered_ready_for_listing",
            "source": "cj_product_discovery",
            "created_at": datetime.now(timezone.utc).isoformat(),

            "title": title,
            "description": detail_data.get("description") or title,
            "price": str(sale_price),
            "currency": "GBP",
            "image": image,

            "supplier": "cj",
            "supplier_name": detail_data.get("supplierName") or item.get("supplierName"),
            "supplier_id": detail_data.get("supplierId") or item.get("supplierId"),
            "supplier_product_id": pid,
            "supplier_variant_id": variant.get("vid"),
            "cj_product_id": pid,
            "cj_variant_id": variant.get("vid"),
            "cj_product_sku": product_sku,
            "cj_variant_sku": variant_sku,

            "supplier_cost": supplier_cost,
            "shipping_cost": shipping_cost,
            "estimated_profit": estimated_profit,
            "margin_percent": margin_percent,
            "profitable": True,
            "inventory_supplier": variant.get("inventoryNum"),

            "product_weight": detail_data.get("productWeight") or item.get("productWeight"),
            "category_name": detail_data.get("categoryName") or item.get("categoryName"),
            "shipping_country": COUNTRY_CODE,
            "discovery_keyword": keyword,

            "publish_targets": {
                "shopify": True,
                "etsy": True,
                "ebay": True,
                "woocommerce": True,
                "amazon": False
            },
            "channels": {
                "shopify": {},
                "etsy": {},
                "ebay": {},
                "woocommerce": {},
                "amazon": {}
            }
        }

        imported += 1
        imported_rows.append({
            "sku": sku,
            "pid": pid,
            "vid": variant.get("vid"),
            "title": title,
            "supplier_cost": supplier_cost,
            "sale_price": sale_price,
            "estimated_profit": estimated_profit,
            "margin_percent": margin_percent
        })

        time.sleep(0.5)

    REGISTRY.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")

    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "CJ_DISCOVERY_IMPORT_COMPLETED",
        "keyword": KEYWORD or "multi_keyword",
        "searches": searches,
        "search_status_code": status_code,
        "cj_total_found": (((search or {}).get("data") or {}).get("total")),
        "imported": imported,
        "skipped_count": len(skipped),
        "imported_rows": imported_rows,
        "skipped": skipped[:30]
    }

    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
