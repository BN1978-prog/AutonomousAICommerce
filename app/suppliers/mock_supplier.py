from __future__ import annotations

from app.suppliers.base import SupplierClient
from app.suppliers.schemas import (
    Money,
    SupplierCapability,
    SupplierOrderRequest,
    SupplierOrderResult,
    SupplierProduct,
    SupplierSearchQuery,
)


class MockSupplierClient(SupplierClient):
    supplier_id = "mock_global_supplier"
    supplier_name = "Mock Global Supplier"
    capabilities = {
        SupplierCapability.CATALOG_SEARCH,
        SupplierCapability.STOCK_CHECK,
        SupplierCapability.PRICE_CHECK,
        SupplierCapability.ORDER_CREATE,
        SupplierCapability.TRACKING,
    }

    def __init__(self, catalog: list[SupplierProduct] | None = None) -> None:
        self.catalog = catalog or self._default_catalog()
        self.orders: dict[str, SupplierOrderResult] = {}

    async def search_products(self, query: SupplierSearchQuery) -> list[SupplierProduct]:
        keywords = query.keywords.lower().split()
        matches: list[SupplierProduct] = []
        for product in self.catalog:
            searchable = f"{product.title} {product.category}".lower()
            if not all(word in searchable for word in keywords):
                continue
            if product.stock_available < query.min_stock:
                continue
            if product.estimated_delivery_days > query.max_delivery_days:
                continue
            if query.max_unit_cost is not None and product.unit_cost.amount > query.max_unit_cost:
                continue
            if product.restricted:
                continue
            matches.append(product)
        return sorted(matches, key=lambda p: (p.unit_cost.amount + p.shipping_cost.amount, -p.stock_available))

    async def get_product(self, supplier_product_id: str) -> SupplierProduct | None:
        return next((p for p in self.catalog if p.supplier_product_id == supplier_product_id), None)

    async def create_order(self, request: SupplierOrderRequest) -> SupplierOrderResult:
        product = await self.get_product(request.supplier_product_id)
        if product is None:
            return SupplierOrderResult(accepted=False, message="Product not found")
        if product.stock_available < request.quantity:
            return SupplierOrderResult(accepted=False, message="Insufficient stock")
        order_id = f"MOCK-{len(self.orders) + 1:06d}"
        result = SupplierOrderResult(
            accepted=True,
            supplier_order_id=order_id,
            tracking_number=f"TRK{order_id[-6:]}",
            message="Order accepted by mock supplier",
        )
        self.orders[order_id] = result
        return result

    def _default_catalog(self) -> list[SupplierProduct]:
        return [
            SupplierProduct(
                supplier_id=self.supplier_id,
                supplier_product_id="PET-BOWL-001",
                title="Non-slip silicone pet feeding bowl",
                category="pets",
                country="CN",
                unit_cost=Money(amount=3.20, currency="GBP"),
                shipping_cost=Money(amount=1.50, currency="GBP"),
                estimated_delivery_days=9,
                stock_available=500,
                supplier_rating=4.6,
                return_rate_percent=3.0,
            ),
            SupplierProduct(
                supplier_id=self.supplier_id,
                supplier_product_id="HOME-LED-002",
                title="Rechargeable motion sensor LED light",
                category="home",
                country="PL",
                unit_cost=Money(amount=5.40, currency="GBP"),
                shipping_cost=Money(amount=2.10, currency="GBP"),
                estimated_delivery_days=5,
                stock_available=220,
                supplier_rating=4.7,
                return_rate_percent=4.5,
            ),
            SupplierProduct(
                supplier_id=self.supplier_id,
                supplier_product_id="BAD-RESTRICTED-999",
                title="Restricted unsafe product",
                category="other",
                country="CN",
                unit_cost=Money(amount=1.00, currency="GBP"),
                shipping_cost=Money(amount=1.00, currency="GBP"),
                estimated_delivery_days=3,
                stock_available=999,
                supplier_rating=4.9,
                restricted=True,
            ),
        ]
