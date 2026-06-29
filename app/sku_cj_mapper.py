
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
OUT = Path("app/logs/sku_cj_mapper.json")

CJ_API_BASE = os.getenv("CJ_API_URL", "https://developers.cjdropshipping.com/api2.0/v1").rstrip("/")
CJ_ACCESS_TOKEN = os.getenv("CJ_ACCESS_TOKEN", "").strip()

MAX_SKUS = int(os.getenv("CJ_MAPPER_MAX_SKUS", "10"))
MIN_CONFIDENCE = int(os.getenv("CJ_MAPPER_MIN_CONFIDENCE", "25"))
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

def clean_keyword(title):
    title = str(title or "")
    title = re.sub(r"[^a-zA-Z0-9 ]+", " ", title)
    words = [w for w in title.split() if len(w) > 2]
    return " ".join(words[:6]) or title[:50] or "pet product"

def search_cj(keyword):
    url = CJ_API_BASE + "/product/list"
    params = {
        "pageNum": 1,
        "pageSize": 5,
        "productName": keyword
    }
    r = requests.get(url, headers=headers, params=params, timeout=30)
    data = r.json()
    return r.status_code, data

def get_detail(pid):
    url = CJ_API_BASE + f"/product/query?pid={pid}"
    r = requests.get(url, headers=headers, timeout=30)
    data = r.json()
    return r.status_code, data

def score_candidate(item, sku_item):
    title = str(sku_item.get("title") or "").lower()
    name = str(item.get("productNameEn") or item.get("productName") or "").lower()
    score = 0

    for w in re.findall(r"[a-z0-9]+", title):
        if len(w) > 3 and w in name:
            score += 3

    countries = item.get("shippingCountryCodes") or []
    if COUNTRY_CODE in countries:
        score += 10

    if item.get("saleStatus") in [3, "3"]:
        score += 5

    if item.get("isFreeShipping"):
        score += 2

    return score

def pick_variant(detail):
    data = (((detail or {}).get("response") or detail).get("data") or {})
    variants = data.get("variants") or []

    if not variants:
        return None

    variants = sorted(variants, key=lambda v: to_float(v.get("variantSellPrice")))
    return variants[0]

def main():
    if not CJ_ACCESS_TOKEN:
        report = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "status": "CJ_MAPPER_MISSING_TOKEN",
            "mapped": 0,
            "errors": ["CJ_ACCESS_TOKEN missing"]
        }
        OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps(report, indent=2))
        return

    registry = json.loads(REGISTRY.read_text(encoding="utf-8-sig")) if REGISTRY.exists() else {}

    results = []
    mapped = 0
    skipped_existing = 0
    errors = 0

    candidates = [
        (sku, item)
        for sku, item in registry.items()
        if isinstance(item, dict)
        and not item.get("cj_product_id")
        and item.get("title")
    ][:MAX_SKUS]

    for sku, item in candidates:
        keyword = clean_keyword(item.get("title"))
        row = {
            "sku": sku,
            "title": item.get("title"),
            "keyword": keyword,
            "ok": False
        }

        try:
            status_code, search = search_cj(keyword)
            row["search_status_code"] = status_code
            row["search_code"] = search.get("code")
            cj_items = (((search or {}).get("data") or {}).get("list") or [])

            if not cj_items:
                row["status"] = "no_candidates"
                results.append(row)
                continue

            best = sorted(cj_items, key=lambda x: score_candidate(x, item), reverse=True)[0]
            row["candidate_pid"] = best.get("pid")
            row["candidate_sku"] = best.get("productSku")
            row["candidate_name"] = best.get("productNameEn") or best.get("productName")
            row["candidate_score"] = score_candidate(best, item)

            sku_match = str(best.get("productSku") or "").strip().upper() == str(sku).strip().upper()
            if not sku_match and row["candidate_score"] < MIN_CONFIDENCE:
                row["status"] = "low_confidence_skipped"
                row["reason"] = "candidate score below threshold and SKU does not match"
                results.append(row)
                continue

            detail_status, detail = get_detail(best.get("pid"))
            row["detail_status_code"] = detail_status

            detail_data = (detail.get("data") or {}) if isinstance(detail, dict) else {}
            variant = pick_variant(detail)

            if not variant:
                row["status"] = "no_variant"
                results.append(row)
                continue

            supplier_cost = to_float(
                variant.get("variantSellPrice") or detail_data.get("sellPrice") or best.get("sellPrice")
            )
            sale_price = to_float(item.get("price") or item.get("last_price"))
            shipping_cost = 0.0 if best.get("isFreeShipping") else to_float(item.get("shipping_cost"), 2.99)

            estimated_profit = round(sale_price - supplier_cost - shipping_cost, 2)
            margin_percent = round((estimated_profit / sale_price) * 100, 2) if sale_price > 0 else 0

            item["supplier"] = "cj"
            item["supplier_name"] = detail_data.get("supplierName") or best.get("supplierName")
            item["supplier_id"] = detail_data.get("supplierId") or best.get("supplierId")
            item["supplier_product_id"] = detail_data.get("pid") or best.get("pid")
            item["supplier_variant_id"] = variant.get("vid")
            item["cj_product_id"] = item["supplier_product_id"]
            item["cj_variant_id"] = item["supplier_variant_id"]
            item["cj_product_sku"] = detail_data.get("productSku") or best.get("productSku")
            item["cj_variant_sku"] = variant.get("variantSku")
            item["supplier_cost"] = supplier_cost
            item["shipping_cost"] = shipping_cost
            item["estimated_profit"] = estimated_profit
            item["margin_percent"] = margin_percent
            item["profitable"] = estimated_profit >= 5 and margin_percent > 0
            item["inventory_supplier"] = variant.get("inventoryNum")
            item["cj_mapped_at"] = datetime.now(timezone.utc).isoformat()
            item["cj_mapping_confidence"] = row["candidate_score"]
            item["cj_shipping_country"] = COUNTRY_CODE
            item["cj_product_url"] = None

            row["ok"] = True
            row["status"] = "mapped"
            row["supplier_cost"] = supplier_cost
            row["shipping_cost"] = shipping_cost
            row["estimated_profit"] = estimated_profit
            row["margin_percent"] = margin_percent
            mapped += 1

        except Exception as e:
            row["status"] = "exception"
            row["error"] = str(e)
            errors += 1

        results.append(row)
        time.sleep(0.3)

    REGISTRY.write_text(json.dumps(registry, indent=2), encoding="utf-8")

    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "CJ_MAPPING_COMPLETED",
        "max_skus": MAX_SKUS,
        "processed": len(candidates),
        "mapped": mapped,
        "skipped_existing": skipped_existing,
        "errors": errors,
        "country": COUNTRY_CODE,
        "results": results
    }

    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
