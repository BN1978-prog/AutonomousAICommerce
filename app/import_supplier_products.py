import os
import asyncio
from dotenv import load_dotenv

from app.suppliers.sandbox_supplier import fetch_supplier_products
from app.suppliers.real_supplier import fetch_real_supplier_products
from app.suppliers.mock_real_supplier import fetch_mock_real_supplier_products
from app.suppliers.normalize_product import normalize_supplier_product
from app.suppliers.shopify_mapper import to_shopify_product_payload
from app.suppliers.import_state import get_imported_sku, save_imported_sku
from app.suppliers.audit_log import save_supplier_raw_log
from app.suppliers.stock_state import detect_stock_change, save_stock_state
from app.suppliers.product_safety import validate_product_for_import
from app.suppliers.ai_product_score import score_product
from app.pricing_ai import dynamic_price
from app.suppliers.blocked_log import log_blocked_product
from app.final_mvp.shopify import ShopifyDraftService
from app.runtime_safety import validate_runtime_safety

load_dotenv()

DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"
LIMIT = int(os.getenv("SUPPLIER_LIMIT", 1))
SUPPLIER_MODE = os.getenv("SUPPLIER_MODE", "sandbox").lower()
IMPORT_EXISTING_ACTION = os.getenv("IMPORT_EXISTING_ACTION", "skip").lower()

def get_supplier_products():
    if SUPPLIER_MODE == "mock_real":
        print("Supplier mode: MOCK_REAL")
        return fetch_mock_real_supplier_products()

    if SUPPLIER_MODE == "real":
        print("Supplier mode: REAL")
        return fetch_real_supplier_products()

    print("Supplier mode: SANDBOX")
    return fetch_supplier_products()

def main():
    issues = validate_runtime_safety()
    if issues:
        print("=== RUNTIME SAFETY BLOCKED ===")
        for issue in issues:
            print(f"- {issue}")
        return

    raw_products = get_supplier_products()
    selected = raw_products[:LIMIT]
    shopify = ShopifyDraftService()

    for raw in selected:
        raw_log_path = save_supplier_raw_log(raw)
        print(f"Supplier raw log saved: {raw_log_path}")

        normalized = normalize_supplier_product(raw)
        safety = validate_product_for_import(normalized)

        print()
        print("=== PRODUCT SAFETY ===")
        print(safety)

        if not safety["allowed"]:
            print()
            print(f"Product blocked by safety gate: {normalized['sku']}"); log_blocked_product(raw, normalized, safety)
            continue

        payload = to_shopify_product_payload(normalized)

        score = score_product(normalized)

        print()
        print("=== AI PRODUCT SCORE ===")
        print(score)

        pricing = dynamic_price(normalized.get("cost", 0), score.get("score", 50))
        normalized["price"] = pricing["price"]

        print("=== DYNAMIC PRICE ===")
        print(pricing)

        if not score["approved"]:
            print()
            print(f"Product blocked by AI score: {normalized['sku']}")
            continue

        stock_change = detect_stock_change(
            normalized["sku"],
            normalized["inventory"]
        )

        print()
        print("=== STOCK SYNC ===")
        print(stock_change)

        existing = get_imported_sku(normalized["sku"])

        if existing:
            product_id = existing.get("product_id")

            if IMPORT_EXISTING_ACTION == "update" and product_id:
                print()
                print(f"SKU already imported - updating Shopify draft: {normalized['sku']}")

                result = asyncio.run(
                    shopify.update_product_from_payload(product_id, payload)
                )

                print()
                print("=== SHOPIFY UPDATE RESULT ===")
                print(result)

                save_stock_state(
                    normalized["sku"],
                    normalized["inventory"]
                )

                continue

            print()
            print(f"SKU already imported - skipped: {normalized['sku']}")
            continue

        print()
        print("=== SUPPLIER RAW ===")
        print(raw)

        print()
        print("=== NORMALIZED ===")
        print(normalized)

        print()
        print("=== SHOPIFY PAYLOAD ===")
        print(payload)

        if DRY_RUN:
            print()
            print("DRY_RUN enabled - Shopify product not created.")
            continue

        result = asyncio.run(shopify.create_draft_from_payload(payload))

        print()
        print("=== SHOPIFY RESULT ===")
        print(result)

        product_id = result.get("response", {}).get("product", {}).get("id")
        image_status = "failed" if result.get("image_failed") else "ok"

        save_imported_sku(
            normalized["sku"],
            product_id,
            image_status
        )

        save_stock_state(
            normalized["sku"],
            normalized["inventory"]
        )

if __name__ == "__main__":
    main()
