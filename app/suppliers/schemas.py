from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field, HttpUrl, field_validator


class SupplierCapability(str, Enum):
    CATALOG_SEARCH = "catalog_search"
    STOCK_CHECK = "stock_check"
    PRICE_CHECK = "price_check"
    ORDER_CREATE = "order_create"
    TRACKING = "tracking"


class Money(BaseModel):
    amount: float = Field(ge=0)
    currency: str = Field(min_length=3, max_length=3)

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        return value.upper()


class SupplierProduct(BaseModel):
    supplier_id: str = Field(min_length=1)
    supplier_product_id: str = Field(min_length=1)
    title: str = Field(min_length=3, max_length=200)
    category: str = Field(default="other", min_length=2, max_length=80)
    country: str = Field(min_length=2, max_length=64)
    product_url: HttpUrl | None = None
    unit_cost: Money
    shipping_cost: Money
    estimated_delivery_days: int = Field(ge=1, le=120)
    stock_available: int = Field(ge=0)
    supplier_rating: float = Field(default=0.0, ge=0, le=5)
    return_rate_percent: float = Field(default=0.0, ge=0, le=100)
    restricted: bool = False
    metadata: dict[str, str | int | float | bool] = Field(default_factory=dict)


class SupplierSearchQuery(BaseModel):
    keywords: str = Field(min_length=2, max_length=160)
    target_market: str = Field(default="UK", min_length=2, max_length=64)
    currency: str = Field(default="GBP", min_length=3, max_length=3)
    max_unit_cost: float | None = Field(default=None, gt=0)
    min_stock: int = Field(default=1, ge=0)
    max_delivery_days: int = Field(default=30, ge=1, le=120)

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        return value.upper()


class SupplierOrderRequest(BaseModel):
    supplier_product_id: str = Field(min_length=1)
    quantity: int = Field(default=1, ge=1, le=100)
    buyer_name: str = Field(min_length=2, max_length=120)
    address_line1: str = Field(min_length=3, max_length=160)
    city: str = Field(min_length=2, max_length=120)
    country: str = Field(min_length=2, max_length=64)
    postal_code: str = Field(min_length=2, max_length=32)


class SupplierOrderResult(BaseModel):
    accepted: bool
    supplier_order_id: str | None = None
    tracking_number: str | None = None
    message: str
