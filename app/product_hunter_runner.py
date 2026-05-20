import asyncio

from app.core.config import Settings
from app.product_hunter.schemas import HunterRequest
from app.product_hunter.service import ProductHunterService
from app.suppliers.registry import SupplierRegistry


async def main():
    settings = Settings()
    registry = SupplierRegistry()
    service = ProductHunterService(settings, registry)

    request = HunterRequest(
        keywords="pet",
        target_market="GB",
        currency="GBP",
        max_unit_cost=999,
        min_stock=0,
        max_delivery_days=120,
        min_opportunity_score=0.0,
        max_results=20
    )

    await service.hunt_and_promote(request)


if __name__ == "__main__":
    asyncio.run(main())
