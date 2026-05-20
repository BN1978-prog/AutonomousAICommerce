from __future__ import annotations

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class CarrierName(str, Enum):
    ROYAL_MAIL = "royal_mail"
    EVRI = "evri"
    DHL = "dhl"


class Address(BaseModel):
    name: str = Field(min_length=1)
    line1: str = Field(min_length=1)
    city: str = Field(min_length=1)
    postal_code: str = Field(min_length=1)
    country_code: str = Field(min_length=2, max_length=2)


class Parcel(BaseModel):
    weight_kg: float = Field(gt=0)
    length_cm: float = Field(gt=0)
    width_cm: float = Field(gt=0)
    height_cm: float = Field(gt=0)
    declared_value: float = Field(ge=0)
    currency: str = Field(default="GBP", min_length=3, max_length=3)


class ShippingRateRequest(BaseModel):
    origin: Address
    destination: Address
    parcel: Parcel
    max_delivery_days: int | None = Field(default=None, gt=0)


class ShippingRate(BaseModel):
    carrier: CarrierName
    service: str
    price: float = Field(ge=0)
    currency: str = "GBP"
    estimated_days: int = Field(gt=0)
    tracked: bool = True
    reliability_score: float = Field(ge=0, le=1)


class ShipmentRequest(BaseModel):
    order_id: str = Field(min_length=1)
    carrier: CarrierName
    service: str
    origin: Address
    destination: Address
    parcel: Parcel


class Shipment(BaseModel):
    shipment_id: str
    order_id: str
    carrier: CarrierName
    service: str
    tracking_number: str
    tracking_url: str
    status: str
    created_at: datetime


class TrackingEvent(BaseModel):
    tracking_number: str
    carrier: CarrierName
    status: str
    location: str
    occurred_at: datetime
    message: str
