def normalize_product(product: dict) -> dict:
    variant = (product.get("variants") or [{}])[0] if product.get("variants") else {}

    return {
        "id": product.get("id"),
        "title": product.get("title"),
        "status": product.get("status"),
        "published_at": product.get("published_at"),
        "price": product.get("price") or variant.get("price"),
        "sku": product.get("sku") or variant.get("sku"),
        "inventory": product.get("inventory") or variant.get("inventory_quantity"),
        "image": product.get("image") or ((product.get("image") or {}).get("src") if isinstance(product.get("image"), dict) else None),
    }


def evaluate_auto_publish(product: dict, rules: dict | None = None) -> dict:
    product = normalize_product(product)
    rules = rules or {}

    min_inventory = int(rules.get("min_inventory", 1))
    min_price = float(rules.get("min_price", 1))
    require_image = bool(rules.get("require_image", True))
    allowed_status = rules.get("allowed_status", ["draft"])

    price = float(product.get("price") or 0)
    inventory = int(product.get("inventory") or 0)
    status = product.get("status")

    reasons = []

    if status not in allowed_status:
        reasons.append(f"status_not_allowed:{status}")

    if inventory < min_inventory:
        reasons.append(f"inventory_too_low:{inventory}")

    if price < min_price:
        reasons.append(f"price_too_low:{price}")

    if require_image and not product.get("image"):
        reasons.append("missing_image")

    can_publish = len(reasons) == 0

    return {
        "ok": True,
        "product_id": product.get("id"),
        "sku": product.get("sku"),
        "title": product.get("title"),
        "decision": "publish" if can_publish else "skip",
        "can_publish": can_publish,
        "reasons": reasons,
        "checks": {
            "status": status,
            "price": price,
            "inventory": inventory,
            "has_image": bool(product.get("image")),
        }
    }

def detect_duplicate_skus(products:list):
    seen={}
    duplicates=set()

    for p in products:

        sku = (
            p.get("sku")
            or (
                (p.get("variants") or [{}])[0].get("sku")
                if p.get("variants")
                else None
            )
        )

        if not sku:
            continue

        if sku in seen:
            duplicates.add(sku)

        seen[sku]=seen.get(sku,0)+1

    return duplicates



