from dataclasses import dataclass
from typing import List, Dict, Any
from app.final_mvp.scoring import score_item

@dataclass
class SupplierItem:
    sku: str
    title: str
    supplier_cost: float
    shipping_cost: float
    stock: int
    supplier_trust_score: float

class ProductFinder:
    def __init__(self):
        self.mock_items = [
            SupplierItem("PET-BOWL-001", "Anti-slip Pet Bowl", 7.50, 3.20, 250, 88),
            SupplierItem("HOME-LED-002", "Motion Sensor LED Light", 4.10, 2.40, 500, 82),
            SupplierItem("CAR-ORG-003", "Car Seat Organizer", 6.90, 3.80, 180, 77),
            SupplierItem("KIT-GAD-004", "Kitchen Silicone Strainer", 3.20, 2.10, 900, 80),
            SupplierItem("PET-TOY-005", "Interactive Pet Toy Ball", 5.80, 3.00, 300, 84),
        ]

    def find(self, keyword: str = "", max_cost: float = 50) -> List[Dict[str, Any]]:
        keyword = keyword.lower().strip()
        results = []
        for item in self.mock_items:
            if item.supplier_cost > max_cost:
                continue
            if keyword and not any(word in item.title.lower() for word in keyword.split()):
                continue

            expected_price = round((item.supplier_cost + item.shipping_cost) * 2.8, 2)
            demand_score = 65 if "pet" in item.title.lower() else 55
            competition_score = 42

            scored = score_item(
                title=item.title,
                supplier_cost=item.supplier_cost,
                shipping_cost=item.shipping_cost,
                expected_sale_price=expected_price,
                demand_score=demand_score,
                competition_score=competition_score,
                supplier_trust_score=item.supplier_trust_score,
            )

            row = scored | {
                "sku": item.sku,
                "stock": item.stock,
                "supplier_trust_score": item.supplier_trust_score,
            }
            results.append(row)

        return sorted(results, key=lambda x: x["opportunity_score"], reverse=True)
