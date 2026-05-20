from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def shopify_auto_health():
    return {
        "ok": True,
        "module": "shopify_automation",
        "features": [
            "auto_publish_rules",
            "auto_price_optimization",
            "order_sync",
            "dashboard_ui"
        ]
    }

from app.shopify_automation.rules import evaluate_auto_publish

@router.post("/auto-publish/evaluate-product")
def auto_publish_evaluate_product(product: dict):
    return evaluate_auto_publish(product)

@router.get("/auto-publish/evaluate-catalog")
def auto_publish_evaluate_catalog():
    from app.main import dashboard_shopify_products

    catalog = dashboard_shopify_products()

    if not catalog.get("ok"):
        return catalog

    results = [
        evaluate_auto_publish(product)
        for product in catalog.get("products", [])
    ]

    publishable = [r for r in results if r.get("can_publish")]

    return {
        "ok": True,
        "total": len(results),
        "publishable_count": len(publishable),
        "publishable": publishable,
        "results": results
    }

from app.shopify_automation.rules import evaluate_auto_publish

@router.post("/auto-publish/evaluate-product")
def auto_publish_evaluate_product(product: dict):
    return evaluate_auto_publish(product)

@router.get("/auto-publish/evaluate-catalog")
def auto_publish_evaluate_catalog():
    from app.main import dashboard_shopify_products

    catalog = dashboard_shopify_products()

    if not catalog.get("ok"):
        return catalog

    results = [
        evaluate_auto_publish(product)
        for product in catalog.get("products", [])
    ]

    publishable = [r for r in results if r.get("can_publish")]

    return {
        "ok": True,
        "total": len(results),
        "publishable_count": len(publishable),
        "publishable": publishable,
        "results": results
    }

@router.get("/auto-publish/evaluate-catalog-safe")
def auto_publish_evaluate_catalog_safe():
    from app.main import dashboard_shopify_products
    from app.shopify_automation.rules import detect_duplicate_skus, evaluate_auto_publish

    catalog = dashboard_shopify_products()

    if not catalog.get("ok"):
        return catalog

    products = catalog.get("products", [])
    duplicate_skus = detect_duplicate_skus(products)

    results = []

    for product in products:
        result = evaluate_auto_publish(product)

        sku = result.get("sku")

        if sku in duplicate_skus:
            result["decision"] = "skip"
            result["can_publish"] = False
            result["reasons"].append("duplicate_sku")

        results.append(result)

    publishable = [r for r in results if r.get("can_publish")]

    return {
        "ok": True,
        "total": len(results),
        "publishable_count": len(publishable),
        "duplicate_skus": list(duplicate_skus),
        "publishable": publishable,
        "results": results
    }

@router.post("/auto-publish/run")
def auto_publish_run(payload: dict = None):
    import os
    import requests

    payload = payload or {}
    force = bool(payload.get("force", False))

    from app.main import dashboard_shopify_products
    from app.shopify_automation.rules import detect_duplicate_skus, evaluate_auto_publish

    catalog = dashboard_shopify_products()

    if not catalog.get("ok"):
        return catalog

    products = catalog.get("products", [])
    duplicate_skus = detect_duplicate_skus(products)

    evaluated = []

    for product in products:
        result = evaluate_auto_publish(product)

        if result.get("sku") in duplicate_skus:
            result["decision"] = "skip"
            result["can_publish"] = False
            result["reasons"].append("duplicate_sku")

        evaluated.append(result)

    publishable = [r for r in evaluated if r.get("can_publish")]

    if not force:
        return {
            "ok": True,
            "dry_run": True,
            "message": "Dry run only. Send force:true to publish.",
            "publishable_count": len(publishable),
            "publishable": publishable,
            "duplicate_skus": list(duplicate_skus)
        }

    store = (os.getenv("SHOPIFY_STORE_URL") or "").strip().replace("https://", "").replace("http://", "").rstrip("/")
    token = (os.getenv("SHOPIFY_ADMIN_TOKEN") or os.getenv("SHOPIFY_ACCESS_TOKEN") or "").strip()

    headers = {
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json"
    }

    published = []
    failed = []

    for item in publishable:
        product_id = item.get("product_id")

        r = requests.put(
            f"https://{store}/admin/api/2024-01/products/{product_id}.json",
            headers=headers,
            json={
                "product": {
                    "id": product_id,
                    "status": "active"
                }
            },
            timeout=30
        )

        if r.status_code in [200, 201]:
            published.append({
                "product_id": product_id,
                "sku": item.get("sku"),
                "title": item.get("title")
            })
        else:
            failed.append({
                "product_id": product_id,
                "sku": item.get("sku"),
                "status_code": r.status_code,
                "error": r.text[:500]
            })

    return {
        "ok": len(failed) == 0,
        "dry_run": False,
        "published_count": len(published),
        "failed_count": len(failed),
        "skipped_count": len(evaluated) - len(publishable),
        "published": published,
        "failed": failed
    }

from app.shopify_automation.pricing import calculate_optimized_price

@router.post("/pricing/optimize")
def pricing_optimize(payload: dict):
    cost = payload.get("cost")
    rules = payload.get("rules") or {}
    return calculate_optimized_price(cost, rules)


@router.post("/pricing/preview-catalog")
def pricing_preview_catalog(payload: dict = None):
    payload = payload or {}
    default_cost_ratio = float(payload.get("default_cost_ratio", 0.45))

    from app.main import dashboard_shopify_products

    catalog = dashboard_shopify_products()

    if not catalog.get("ok"):
        return catalog

    results = []

    for product in catalog.get("products", []):
        variant = (
            (product.get("variants") or [{}])[0]
            if product.get("variants")
            else {}
        )

        sku = product.get("sku") or variant.get("sku")

        price = float(
            product.get("price")
            or variant.get("price")
            or 0
        )

        estimated_cost = float(
            product.get("cost")
            or variant.get("cost")
            or 0
        )

        if estimated_cost <= 0 and price > 0:
            estimated_cost = price * default_cost_ratio

        optimized = calculate_optimized_price(estimated_cost)

        results.append({
            "product_id": product.get("id"),
            "sku": sku,
            "title": product.get("title"),
            "current_price": price,
            "estimated_cost": round(estimated_cost, 2),
            "optimization": optimized
        })

    return {
        "ok": True,
        "count": len(results),
        "default_cost_ratio": default_cost_ratio,
        "results": results
    }

from app.shopify_automation.pricing import calculate_optimized_price

@router.post("/pricing/optimize")
def pricing_optimize(payload: dict):
    cost = payload.get("cost")
    rules = payload.get("rules") or {}
    return calculate_optimized_price(cost, rules)


@router.post("/pricing/preview-catalog")
def pricing_preview_catalog(payload: dict = None):
    payload = payload or {}
    default_cost_ratio = float(payload.get("default_cost_ratio", 0.45))

    from app.main import dashboard_shopify_products

    catalog = dashboard_shopify_products()

    if not catalog.get("ok"):
        return catalog

    results = []

    for product in catalog.get("products", []):
        variant = (
            (product.get("variants") or [{}])[0]
            if product.get("variants")
            else {}
        )

        sku = product.get("sku") or variant.get("sku")

        price = float(
            product.get("price")
            or variant.get("price")
            or 0
        )

        estimated_cost = float(
            product.get("cost")
            or variant.get("cost")
            or 0
        )

        if estimated_cost <= 0 and price > 0:
            estimated_cost = price * default_cost_ratio

        optimized = calculate_optimized_price(estimated_cost)

        results.append({
            "product_id": product.get("id"),
            "sku": sku,
            "title": product.get("title"),
            "current_price": price,
            "estimated_cost": round(estimated_cost, 2),
            "optimization": optimized
        })

    return {
        "ok": True,
        "count": len(results),
        "default_cost_ratio": default_cost_ratio,
        "results": results
    }


@router.post("/pricing/apply-catalog")
def pricing_apply_catalog(payload: dict = None):
    import os
    import requests

    payload = payload or {}
    force = bool(payload.get("force", False))
    default_cost_ratio = float(payload.get("default_cost_ratio",0.45))

    from app.main import dashboard_shopify_products
    from app.shopify_automation.pricing import calculate_optimized_price

    catalog = dashboard_shopify_products()

    if not catalog.get("ok"):
        return catalog

    from app.shopify_automation.rules import detect_duplicate_skus

    duplicate_skus = detect_duplicate_skus(
        catalog.get("products",[])
    )

    updated=[]
    skipped=[]

    store=(os.getenv("SHOPIFY_STORE_URL") or "").replace("https://","").strip("/")
    token=(os.getenv("SHOPIFY_ADMIN_TOKEN") or os.getenv("SHOPIFY_ACCESS_TOKEN") or "")

    headers={
        "X-Shopify-Access-Token":token,
        "Content-Type":"application/json"
    }

    for product in catalog.get("products",[]):

        variant=((product.get("variants") or [{}])[0])

        price=float(
            product.get("price")
            or variant.get("price")
            or 0
        )

        sku=product.get("sku") or variant.get("sku")

        if sku in duplicate_skus:
            skipped.append(sku)
            continue

        cost=price*default_cost_ratio

        optimized=calculate_optimized_price(cost)

        new_price=optimized["optimized_price"]

        if abs(new_price-price) < 0.01:
            skipped.append(sku)
            continue

        if not force:
            updated.append({
                "sku":sku,
                "current":price,
                "new":new_price,
                "dry_run":True
            })
            continue

        r=requests.put(
            f"https://{store}/admin/api/2024-01/variants/{variant.get('id')}.json",
            headers=headers,
            json={
                "variant":{
                    "id":variant.get("id"),
                    "price":str(new_price)
                }
            }
        )

        updated.append({
            "sku":sku,
            "current":price,
            "new":new_price,
            "status_code":r.status_code
        })

    return {
        "ok":True,
        "dry_run":not force,
        "updated_count":len(updated),
        "skipped_count":len(skipped),
        "updated":updated
    }




from app.shopify_automation.orders import normalize_order

@router.get("/orders/sync")
def orders_sync(limit: int = 50, status: str = "any"):
    import os
    import requests

    store = (os.getenv("SHOPIFY_STORE_URL") or "").strip().replace("https://","").replace("http://","").rstrip("/")
    token = (os.getenv("SHOPIFY_ADMIN_TOKEN") or os.getenv("SHOPIFY_ACCESS_TOKEN") or "").strip()

    headers = {
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json"
    }

    r = requests.get(
        f"https://{store}/admin/api/2024-01/orders.json",
        headers=headers,
        params={
            "status": status,
            "limit": max(1, min(int(limit), 250))
        },
        timeout=30
    )

    if r.status_code != 200:
        return {
            "ok": False,
            "status_code": r.status_code,
            "error": r.text[:1000]
        }

    orders = [
        normalize_order(order)
        for order in r.json().get("orders", [])
    ]

    return {
        "ok": True,
        "count": len(orders),
        "orders": orders
    }


@router.get("/orders/summary")
def orders_summary(limit: int = 50):
    synced = orders_sync(limit=limit, status="any")

    if not synced.get("ok"):
        return synced

    orders = synced.get("orders", [])

    total_revenue = 0.0
    paid = 0
    pending = 0
    fulfilled = 0
    unfulfilled = 0

    for order in orders:
        total_revenue += float(order.get("total_price") or 0)

        if order.get("financial_status") == "paid":
            paid += 1
        else:
            pending += 1

        if order.get("fulfillment_status") == "fulfilled":
            fulfilled += 1
        else:
            unfulfilled += 1

    return {
        "ok": True,
        "orders_count": len(orders),
        "total_revenue": round(total_revenue, 2),
        "paid_orders": paid,
        "pending_or_other_orders": pending,
        "fulfilled_orders": fulfilled,
        "unfulfilled_orders": unfulfilled
    }

@router.get("/dashboard-status")
def shopify_automation_dashboard():

    from app.main import dashboard_shopify_catalog_health
    from app.main import dashboard_shopify_products

    catalog = dashboard_shopify_catalog_health()

    pricing = pricing_apply_catalog({})
    orders = orders_summary(50)

    publish = auto_publish_evaluate_catalog_safe()

    return {
        "ok":True,

        "catalog":{
            "health":catalog.get("health"),
            "products":catalog.get("total_products"),
            "duplicates":catalog.get("duplicate_sku_count")
        },

        "pricing":{
            "pending_updates":pricing.get("updated_count"),
            "synced":pricing.get("updated_count")==0
        },

        "publish":{
            "publishable":publish.get("publishable_count"),
            "duplicates":len(
                publish.get("duplicate_skus",[])
            )
        },

        "orders":{
            "orders_count":orders.get("orders_count"),
            "revenue":orders.get("total_revenue")
        }
    }


from app.shopify_automation.analytics import calculate_store_kpis

@router.get("/analytics/kpis")
def analytics_kpis():

    synced=orders_sync(
        limit=250,
        status="any"
    )

    if not synced.get("ok"):
        return synced

    return {
        "ok":True,
        "kpis":calculate_store_kpis(
            synced.get("orders",[])
        )
    }

