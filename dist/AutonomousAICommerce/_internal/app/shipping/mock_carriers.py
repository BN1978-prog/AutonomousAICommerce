from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha1

from .base import ShippingCarrier
from .schemas import CarrierName, Shipment, ShipmentRequest, ShippingRate, ShippingRateRequest, TrackingEvent


class DeterministicMockCarrier(ShippingCarrier):
    def __init__(self, carrier: CarrierName, base_price: float, base_days: int, reliability: float) -> None:
        self.carrier = carrier
        self.base_price = base_price
        self.base_days = base_days
        self.reliability = reliability

    async def get_rates(self, request: ShippingRateRequest) -> list[ShippingRate]:
        international = request.origin.country_code.upper() != request.destination.country_code.upper()
        weight_surcharge = max(request.parcel.weight_kg - 1, 0) * 1.75
        intl_surcharge = 7.50 if international else 0.0
        days = self.base_days + (3 if international else 0)
        standard = ShippingRate(
            carrier=self.carrier,
            service="tracked_standard",
            price=round(self.base_price + weight_surcharge + intl_surcharge, 2),
            estimated_days=days,
            reliability_score=self.reliability,
        )
        express = ShippingRate(
            carrier=self.carrier,
            service="tracked_express",
            price=round(standard.price + 5.95, 2),
            estimated_days=max(1, days - 2),
            reliability_score=min(1.0, self.reliability + 0.03),
        )
        rates = [standard, express]
        if request.max_delivery_days:
            rates = [r for r in rates if r.estimated_days <= request.max_delivery_days]
        return rates

    async def create_shipment(self, request: ShipmentRequest) -> Shipment:
        seed = f"{request.order_id}:{self.carrier}:{request.service}:{request.destination.postal_code}"
        digest = sha1(seed.encode("utf-8")).hexdigest()[:12].upper()
        tracking_number = f"{self.carrier.value[:3].upper()}{digest}"
        return Shipment(
            shipment_id=f"shp_{digest.lower()}",
            order_id=request.order_id,
            carrier=self.carrier,
            service=request.service,
            tracking_number=tracking_number,
            tracking_url=f"https://tracking.example/{self.carrier.value}/{tracking_number}",
            status="label_created",
            created_at=datetime.now(timezone.utc),
        )

    async def track(self, tracking_number: str) -> list[TrackingEvent]:
        now = datetime.now(timezone.utc)
        return [
            TrackingEvent(
                tracking_number=tracking_number,
                carrier=self.carrier,
                status="label_created",
                location="origin_hub",
                occurred_at=now,
                message="Shipping label created and awaiting carrier pickup.",
            )
        ]


class RoyalMailMockCarrier(DeterministicMockCarrier):
    def __init__(self) -> None:
        super().__init__(CarrierName.ROYAL_MAIL, base_price=3.49, base_days=3, reliability=0.94)


class EvriMockCarrier(DeterministicMockCarrier):
    def __init__(self) -> None:
        super().__init__(CarrierName.EVRI, base_price=2.99, base_days=4, reliability=0.89)


class DHLMockCarrier(DeterministicMockCarrier):
    def __init__(self) -> None:
        super().__init__(CarrierName.DHL, base_price=6.99, base_days=2, reliability=0.97)
