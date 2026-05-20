from app.fulfillment_guard import check_fulfillment_allowed

test_order = {
    "sku": "PET-BOWL-001",
    "paid": True,
    "sale_price": 12.70,
    "shipping_address": {
        "name": "Test Customer",
        "country": "US"
    }
}

test_product = {
    "sku": "PET-BOWL-001",
    "cost": 5.00,
    "shipping_cost": 2.00
}

print(check_fulfillment_allowed(test_order, test_product))
