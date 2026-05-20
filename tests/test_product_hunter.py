import pytest
from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import app
from app.product_hunter.demand import DemandEstimator
from app.product_hunter.schemas import HunterRequest
from app.product_hunter.service import ProductHunterService
from app.suppliers.registry import SupplierRegistry
from app.suppliers.schemas import Money, SupplierProduct


@pytest.mark.asyncio
async def test_product_hunter_returns_ranked_opportunities():
    service = ProductHunterService(get_settings(), SupplierRegistry())
    response = await service.hunt(HunterRequest(keywords="pet", max_unit_cost=20, max_results=5))
    assert response.total_supplier_products >= 1
    assert len(response.opportunities) >= 1
    scores = [item.opportunity_score for item in response.opportunities]
    assert scores == sorted(scores, reverse=True)
    assert response.opportunities[0].decision.status.value in {"approved", "watchlist"}


def test_demand_estimator_is_deterministic():
    estimator = DemandEstimator()
    product = SupplierProduct(
        supplier_id="mock",
        supplier_product_id="P1",
        title="Portable Pet Grooming Kit",
        category="pets",
        country="UK",
        unit_cost=Money(amount=7, currency="GBP"),
        shipping_cost=Money(amount=2, currency="GBP"),
        estimated_delivery_days=4,
        stock_available=50,
        supplier_rating=4.8,
    )
    first = estimator.estimate(product, "UK")
    second = estimator.estimate(product, "UK")
    assert [x.model_dump() for x in first] == [x.model_dump() for x in second]
    assert estimator.aggregate(first) > 0.5


def test_hunter_api_endpoint():
    client = TestClient(app)
    response = client.post("/hunter/opportunities", json={"keywords": "car", "max_unit_cost": 30, "max_results": 3})
    assert response.status_code == 200
    payload = response.json()
    assert "opportunities" in payload
    assert payload["total_supplier_products"] >= len(payload["opportunities"])
