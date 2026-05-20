from fastapi import APIRouter

router = APIRouter(prefix="/commerce", tags=["commerce"])

@router.get("/overview")
def commerce_overview():

    channels = [
        {
            "name":"Shopify",
            "products":50,
            "orders":0,
            "revenue":0,
            "status":"connected"
        },
        {
            "name":"WooCommerce",
            "products":0,
            "orders":0,
            "revenue":0,
            "status":"connected"
        },
        {
            "name":"Meta",
            "products":50,
            "orders":0,
            "revenue":0,
            "status":"connected"
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
            "products":sum(
                c["products"] or 0
                for c in channels
            ),

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

