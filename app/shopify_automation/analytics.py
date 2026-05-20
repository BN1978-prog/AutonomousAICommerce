def calculate_store_kpis(orders:list):

    revenue=0
    order_count=len(orders)
    product_sales={}

    for order in orders:

        revenue += float(
            order.get("total_price") or 0
        )

        for item in order.get("items",[]):

            key=item.get("title") or "Unknown"

            product_sales[key]=(
                product_sales.get(key,0)
                + int(item.get("quantity") or 0)
            )

    avg_order=0

    if order_count>0:
        avg_order=round(
            revenue/order_count,
            2
        )

    top_products=sorted(
        product_sales.items(),
        key=lambda x:x[1],
        reverse=True
    )[:5]

    return {
        "orders":order_count,
        "revenue":round(revenue,2),
        "average_order_value":avg_order,
        "top_products":[
            {
                "name":p[0],
                "units":p[1]
            }
            for p in top_products
        ]
    }

