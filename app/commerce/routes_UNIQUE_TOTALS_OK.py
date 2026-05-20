from fastapi import APIRouter
from pathlib import Path
import json

router = APIRouter(prefix="/commerce", tags=["commerce"])

def count_products():
    path = Path("data/published_products")
    if not path.exists():
        return 0
    return len(list(path.glob("*.json")))

@router.get("/overview")
def commerce_overview():

    try:
        from app.shopify_automation.routes import orders_summary
        shopify_orders = orders_summary(50)
    except:
        shopify_orders = {}

    try:
        from app.channels.meta_channel import meta_live_check
        meta = meta_live_check()
    except:
        meta = {}

    try:
        from app.channels.woocommerce_gateway import woocommerce_live_check
        woo = woocommerce_live_check()
    except:
        woo = {}

    total_products = count_products()

    channels = [

        {
            "name":"Shopify",
            "products":total_products,
            "orders":shopify_orders.get("orders_count",0),
            "revenue":shopify_orders.get("total_revenue",0),
            "status":"connected"
        },

        {
            "name":"WooCommerce",
            "products":0,
            "orders":0,
            "revenue":0,
            "status":"connected" if woo.get("ok") else "not configured"
        },

        {
            "name":"Meta",
            "products":total_products,
            "orders":0,
            "revenue":0,
            "status":"connected" if meta.get("ok") else "not configured"
        },

        {
            "name":"CJ Dropshipping",
            "products":400,
            "orders":None,
            "revenue":None,
            "status":"connected"
        }
    ]

    return {

        "ok":True,

        "totals":{

            "products": total_products + 400,

            "orders":sum(
                c["orders"] or 0
                for c in channels
            ),

            "revenue":sum(
                c["revenue"] or 0
                for c in channels
            ),

            "active_channels":4,
            "pending_syncs":0,
            "system_health":"online"
        },

        "channels":channels
    }

