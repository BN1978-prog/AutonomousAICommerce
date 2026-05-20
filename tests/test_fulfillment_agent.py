import pytest
from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import app
from app.fulfillment.schemas import FulfillmentRequest, ShippingAddress, FulfillmentStatus
from app.fulfillment.service import FulfillmentService
from app.suppliers.registry import SupplierRegistry


def _address():
    return ShippingAddress(
        buyer_name="Test Buyer",
        address_line1="1 Test Street",
        city="London",
        country="UK",
        postal_code="SW1A 1AA",
    )


def _request(**overrides):
    payload = dict(
        order_id="ORDER-001",
        listing_id="LISTING-001",
        sku="PET-BOWL-001",
        supplier_id="mock_global_supplier",
        supplier_product_id="PET-BOWL-001",
        quantity=1,
        sale_price=19.99,
        currency="GBP",
        buyer_country="UK",
        shipping_address=_address(),
        dry_run=True,
    )
    payload.update(overrides)
    return FulfillmentRequest(**payload)


@pytest.mark.asyncio
async def test_fulfillment_dry_run_approves_profitable_order():
    service = FulfillmentService(get_settings(), SupplierRegistry())
    result = await service.fulfill(_request())
    assert result.status == FulfillmentStatus.APPROVED_DRY_RUN
    assert result.net_profit is not None and result.net_profit > 0
    assert "dry_run_no_purchase" in result.audit_events


@pytest.mark.asyncio
async def test_fulfillment_blocks_unprofitable_order():
    service = FulfillmentService(get_settings(), SupplierRegistry())
    result = await service.fulfill(_request(sale_price=5.50))
    assert result.status == FulfillmentStatus.BLOCKED
    assert any("Margin" in reason or "risk" in reason.lower() for reason in result.reasons)


@pytest.mark.asyncio
async def test_fulfillment_blocks_real_purchase_when_setting_disabled():
    service = FulfillmentService(get_settings(), SupplierRegistry())
    result = await service.fulfill(_request(dry_run=False))
    assert result.status == FulfillmentStatus.BLOCKED
    assert any("disabled" in reason.lower() for reason in result.reasons)


def test_fulfillment_api_endpoint():
    client = TestClient(app)
    response = client.post(
        "/fulfillment/process",
        json={
            "order_id": "ORDER-API-001",
            "listing_id": "LISTING-API-001",
            "sku": "PET-BOWL-001",
            "supplier_id": "mock_global_supplier",
            "supplier_product_id": "PET-BOWL-001",
            "quantity": 1,
            "sale_price": 19.99,
            "currency": "GBP",
            "buyer_country": "UK",
            "shipping_address": {
                "buyer_name": "Test Buyer",
                "address_line1": "1 Test Street",
                "city": "London",
                "country": "UK",
                "postal_code": "SW1A 1AA",
            },
            "dry_run": True,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "approved_dry_run"
    assert body["supplier_product_id"] == "PET-BOWL-001"
