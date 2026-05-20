from __future__ import annotations

from fastapi import HTTPException
from .base import ShippingCarrier
from .mock_carriers import DHLMockCarrier, EvriMockCarrier, RoyalMailMockCarrier
from .schemas import CarrierName, Shipment, ShipmentRequest, ShippingRate, ShippingRateRequest, TrackingEvent


class ShippingRegistry:
    def __init__(self) -> None:
        self._carriers: dict[CarrierName, ShippingCarrier] = {
            CarrierName.ROYAL_MAIL: RoyalMailMockCarrier(),
            CarrierName.EVRI: EvriMockCarrier(),
            CarrierName.DHL: DHLMockCarrier(),
        }

    def list_names(self) -> list[str]:
        return [name.value for name in self._carriers]

    def get(self, carrier: CarrierName) -> ShippingCarrier:
        try:
            return self._carriers[carrier]
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=f"Carrier not configured: {carrier}") from exc

    async def quote_all(self, request: ShippingRateRequest) -> list[ShippingRate]:
        rates: list[ShippingRate] = []
        for carrier in self._carriers.values():
            rates.extend(await carrier.get_rates(request))
        return sorted(rates, key=lambda r: (r.price, -r.reliability_score, r.estimated_days))

    async def create_shipment(self, request: ShipmentRequest) -> Shipment:
        return await self.get(request.carrier).create_shipment(request)

    async def track(self, carrier: CarrierName, tracking_number: str) -> list[TrackingEvent]:
        return await self.get(carrier).track(tracking_number)
