from __future__ import annotations

from abc import ABC, abstractmethod

from app.suppliers.schemas import (
    SupplierCapability,
    SupplierOrderRequest,
    SupplierOrderResult,
    SupplierProduct,
    SupplierSearchQuery,
)


class SupplierClient(ABC):
    """Stable supplier integration contract used by the rest of the system."""

    supplier_id: str
    supplier_name: str
    capabilities: set[SupplierCapability]

    @abstractmethod
    async def search_products(self, query: SupplierSearchQuery) -> list[SupplierProduct]:
        """Return normalized products matching the query."""

    @abstractmethod
    async def get_product(self, supplier_product_id: str) -> SupplierProduct | None:
        """Return a single normalized supplier product, or None if unavailable."""

    @abstractmethod
    async def create_order(self, request: SupplierOrderRequest) -> SupplierOrderResult:
        """Create a supplier order. Implementations must be idempotent upstream where possible."""
