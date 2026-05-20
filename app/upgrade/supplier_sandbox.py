from typing import List, Dict, Any

class SupplierSandboxClient:
    def __init__(self):
        self.products = [
            {"sku": "PET-BOWL-001", "title": "Anti-slip Pet Bowl", "unit_cost": 7.5, "shipping_cost": 3.2, "stock": 250, "trust_score": 88},
            {"sku": "HOME-LED-002", "title": "Motion Sensor LED Light", "unit_cost": 4.1, "shipping_cost": 2.4, "stock": 500, "trust_score": 82},
            {"sku": "CAR-ORG-003", "title": "Car Seat Organizer", "unit_cost": 6.9, "shipping_cost": 3.8, "stock": 180, "trust_score": 77},
            {"sku": "KIT-GAD-004", "title": "Kitchen Silicone Strainer", "unit_cost": 3.2, "shipping_cost": 2.1, "stock": 900, "trust_score": 80},
        ]

    def search_products(self, query: str, max_cost: float = 50) -> List[Dict[str, Any]]:
        q = query.lower().strip()
        return [
            p for p in self.products
            if p["unit_cost"] <= max_cost and (not q or any(word in p["title"].lower() for word in q.split()))
        ]

    def create_purchase_order(self, sku: str, quantity: int, shipping_address: Dict[str, Any]) -> Dict[str, Any]:
        product = next((p for p in self.products if p["sku"] == sku), None)
        if not product:
            raise ValueError("SKU not found")

        return {
            "dry_run": True,
            "purchase_order_id": f"SANDBOX-PO-{sku}-{quantity}",
            "sku": sku,
            "quantity": quantity,
            "status": "simulated",
            "tracking_number": "SANDBOXTRACK123",
            "shipping_address": shipping_address,
        }
