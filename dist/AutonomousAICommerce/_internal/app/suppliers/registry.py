from __future__ import annotations

from app.suppliers.base import SupplierClient
from app.suppliers.mock_supplier import MockSupplierClient
from app.suppliers.schemas import SupplierProduct, SupplierSearchQuery


class SupplierRegistry:
    """Coordinates multiple suppliers behind one stable interface."""

    def __init__(self, clients: list[SupplierClient] | None = None) -> None:
        self.clients: dict[str, SupplierClient] = {}
        for client in clients or [MockSupplierClient()]:
            self.register(client)

    def register(self, client: SupplierClient) -> None:
        if client.supplier_id in self.clients:
            raise ValueError(f"Duplicate supplier_id registered: {client.supplier_id}")
        self.clients[client.supplier_id] = client

    async def search_all(self, query: SupplierSearchQuery) -> list[SupplierProduct]:
        results: list[SupplierProduct] = []
        for client in self.clients.values():
            results.extend(await client.search_products(query))
        return sorted(results, key=lambda p: (p.unit_cost.amount + p.shipping_cost.amount, -p.supplier_rating))

    async def get_product(self, supplier_id: str, supplier_product_id: str) -> SupplierProduct | None:
        client = self.clients.get(supplier_id)
        if client is None:
            return None
        return await client.get_product(supplier_product_id)
