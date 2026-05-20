import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.suppliers.currency import CurrencyConverter
from app.suppliers.mock_supplier import MockSupplierClient
from app.suppliers.normalizer import SupplierNormalizer
from app.suppliers.registry import SupplierRegistry
from app.suppliers.schemas import SupplierSearchQuery


@pytest.mark.asyncio
async def test_mock_supplier_search_filters_restricted_and_stock():
    client = MockSupplierClient()
    results = await client.search_products(SupplierSearchQuery(keywords="pet bowl", max_delivery_days=20))
    assert len(results) == 1
    assert results[0].supplier_product_id == "PET-BOWL-001"
    assert not results[0].restricted


@pytest.mark.asyncio
async def test_registry_search_all_returns_sorted_products():
    registry = SupplierRegistry(clients=[MockSupplierClient()])
    results = await registry.search_all(SupplierSearchQuery(keywords="led light", max_delivery_days=10))
    assert [p.supplier_product_id for p in results] == ["HOME-LED-002"]


def test_currency_converter_round_trip_supported_currency():
    converter = CurrencyConverter()
    assert converter.convert(10, "USD", "GBP") == 8.00
    assert converter.convert(8, "GBP", "USD") == 10.00


def test_normalizer_creates_core_supplier_offer():
    supplier = MockSupplierClient()
    product = supplier.catalog[0]
    offer = SupplierNormalizer().to_offer(product, target_currency="GBP")
    assert offer.supplier_id == "mock_global_supplier"
    assert offer.unit_cost == 3.20
    assert 0 <= offer.supplier_risk_score <= 1


def test_supplier_search_api_endpoint():
    response = TestClient(app).post("/suppliers/search", json={"keywords": "pet bowl", "max_delivery_days": 20})
    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]["supplier_product_id"] == "PET-BOWL-001"
