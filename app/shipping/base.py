from __future__ import annotations

from abc import ABC, abstractmethod
from .schemas import Shipment, ShipmentRequest, ShippingRate, ShippingRateRequest, TrackingEvent


class ShippingCarrier(ABC):
    @abstractmethod
    async def get_rates(self, request: ShippingRateRequest) -> list[ShippingRate]:
        raise NotImplementedError

    @abstractmethod
    async def create_shipment(self, request: ShipmentRequest) -> Shipment:
        raise NotImplementedError

    @abstractmethod
    async def track(self, tracking_number: str) -> list[TrackingEvent]:
        raise NotImplementedError
