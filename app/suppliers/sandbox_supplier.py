DISABLED_IN_PRODUCTION=True

def fetch_supplier_products():
    return [
        {
            "sku": "DISABLED-TEST-SUPPLIER-002",
            "title": "Sandbox Test Product",
            "description": "Imported from supplier sandbox",
            "price": 19.99,
            "currency": "GBP",
            "inventory": 10,
            "vendor": "Sandbox Supplier",
            "image": None
        }
    ]

