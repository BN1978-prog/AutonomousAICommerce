from fastapi import APIRouter
from pathlib import Path

router = APIRouter(prefix="/commerce", tags=["commerce"])

CJ_PRODUCTS = 400

def count_products():
    path = Path("data/published_products")
    if not path.exists():
        return 0
    return len(list(path.glob("*.json")))

def get_woo_products(woo):
    for item in woo.get("woocommerce", {}).get("post_type_counts", []):
        if item.get("type") == "product":
            return int(item.get("count") or 0)
    return 0

@router.get("/overview")
def commerce_overview():

    try:
        from app.shopify_automation.routes import orders_summary
        shopify_orders = orders_summary(50)
    except Exception:
        shopify_orders = {}

    try:
        from app.channels.meta_channel import meta_live_check
        meta = meta_live_check()
    except Exception:
        meta = {}

    try:
        from app.channels.woocommerce_gateway import woocommerce_live_check
        woo = woocommerce_live_check()
    except Exception:
        woo = {}

    published_products = count_products()
    woo_products = get_woo_products(woo)

    channels = [
        {
            "name": "Shopify",
            "products": published_products,
            "orders": shopify_orders.get("orders_count", 0),
            "revenue": shopify_orders.get("total_revenue", 0),
            "status": "connected",
        },
        {
            "name": "WooCommerce",
            "products": woo_products,
            "orders": 0,
            "revenue": 0,
            "status": "connected" if woo.get("ok") or woo_products > 0 else "not configured",
        },
        {
            "name": "Meta",
            "products": published_products,
            "orders": 0,
            "revenue": 0,
            "status": "connected" if meta.get("ok") else "not configured",
        },
        {
            "name": "CJ Dropshipping",
            "products": CJ_PRODUCTS,
            "orders": None,
            "revenue": None,
            "status": "connected",
        },
    ]

    return {
        "ok": True,
        "totals": {
            "products": published_products + woo_products + CJ_PRODUCTS,
            "orders": sum(c["orders"] or 0 for c in channels),
            "revenue": sum(c["revenue"] or 0 for c in channels),
            "active_channels": 4,
            "pending_syncs": 0,
            "system_health": "online",
        },
        "channels": channels,
    }
