def normalize_order(order: dict) -> dict:
    line_items = order.get("line_items") or []

    return {
        "id": order.get("id"),
        "name": order.get("name"),
        "created_at": order.get("created_at"),
        "financial_status": order.get("financial_status"),
        "fulfillment_status": order.get("fulfillment_status"),
        "currency": order.get("currency"),
        "total_price": order.get("total_price"),
        "subtotal_price": order.get("subtotal_price"),
        "total_tax": order.get("total_tax"),
        "customer_email": (
            order.get("email")
            or (order.get("customer") or {}).get("email")
        ),
        "items_count": len(line_items),
        "items": [
            {
                "title": item.get("title"),
                "sku": item.get("sku"),
                "quantity": item.get("quantity"),
                "price": item.get("price"),
                "variant_id": item.get("variant_id"),
                "product_id": item.get("product_id")
            }
            for item in line_items
        ]
    }
