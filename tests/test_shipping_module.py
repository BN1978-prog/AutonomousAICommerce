import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.shipping.registry import ShippingRegistry
from app.shipping.schemas import Address, Parcel, ShippingRateRequest, ShipmentRequest, CarrierName
from app.shipping.selector import ShippingSelector


def sample_rate_request() -> ShippingRateRequest:
    return ShippingRateRequest(
        origin=Address(name="Warehouse", line1="1 Depot Road", city="London", postal_code="E1 1AA", country_code="GB"),
        destination=Address(name="Customer", line1="9 High Street", city="Manchester", postal_code="M1 1AA", country_code="GB"),
        parcel=Parcel(weight_kg=0.8, length_cm=20, width_cm=15, height_cm=10, declared_value=29.99),
    )


@pytest.mark.asyncio
async def test_shipping_registry_quotes_all_carriers_sorted_by_price():
    registry = ShippingRegistry()
    rates = await registry.quote_all(sample_rate_request())
    assert len(rates) == 6
    assert rates[0].price <= rates[-1].price
    assert {rate.carrier for rate in rates} == {CarrierName.ROYAL_MAIL, CarrierName.EVRI, CarrierName.DHL}


@pytest.mark.asyncio
async def test_shipping_selector_prefers_reliable_low_cost_rate():
    selector = ShippingSelector()
    rates = await ShippingRegistry().quote_all(sample_rate_request())
    best = selector.choose_best(rates, min_reliability=0.9)
    assert best.reliability_score >= 0.9
    assert best.carrier in {CarrierName.ROYAL_MAIL, CarrierName.DHL}


@pytest.mark.asyncio
async def test_create_shipment_returns_tracking_number():
    registry = ShippingRegistry()
    req = sample_rate_request()
    shipment = await registry.create_shipment(
        ShipmentRequest(
            order_id="ord_123",
            carrier=CarrierName.ROYAL_MAIL,
            service="tracked_standard",
            origin=req.origin,
            destination=req.destination,
            parcel=req.parcel,
        )
    )
    assert shipment.tracking_number.startswith("ROY")
    events = await registry.track(CarrierName.ROYAL_MAIL, shipment.tracking_number)
    assert events[0].status == "label_created"


def test_shipping_api_endpoints_work():
    client = TestClient(app)
    payload = sample_rate_request().model_dump()
    rates_resp = client.post("/shipping/rates", json=payload)
    assert rates_resp.status_code == 200
    assert len(rates_resp.json()) == 6

    shipment_payload = {
        "order_id": "ord_api_1",
        "carrier": "dhl",
        "service": "tracked_express",
        "origin": payload["origin"],
        "destination": payload["destination"],
        "parcel": payload["parcel"],
    }
    shipment_resp = client.post("/shipping/shipments", json=shipment_payload)
    assert shipment_resp.status_code == 200
    tracking = shipment_resp.json()["tracking_number"]
    track_resp = client.get(f"/shipping/dhl/track/{tracking}")
    assert track_resp.status_code == 200
    assert track_resp.json()[0]["tracking_number"] == tracking
