from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field, HttpUrl, field_validator


class MarketplaceName(str, Enum):
    SHOPIFY = "shopify"
    EBAY = "ebay"
    MOCK = "mock"


class ListingStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    FAILED = "failed"


class MarketplaceFees(BaseModel):
    platform_fee_percent: float = Field(default=12.0, ge=0, le=50)
    payment_fee_percent: float = Field(default=2.9, ge=0, le=20)
    fixed_fee: float = Field(default=0.0, ge=0)


class ListingDraft(BaseModel):
    sku: str = Field(min_length=3, max_length=80)
    title: str = Field(min_length=3, max_length=140)
    description: str = Field(min_length=10, max_length=5000)
    price: float = Field(gt=0)
    currency: str = Field(default="GBP", min_length=3, max_length=3)
    quantity: int = Field(default=1, ge=0, le=100000)
    category: str = Field(default="other", min_length=2, max_length=80)
    tags: list[str] = Field(default_factory=list, max_length=25)
    image_urls: list[str] = Field(default_factory=list, max_length=12)
    supplier_product_id: str | None = None

    @field_validator("currency")
    @classmethod
    def uppercase_currency(cls, value: str) -> str:
        return value.upper()


class ListingResult(BaseModel):
    marketplace: MarketplaceName
    listing_id: str = Field(min_length=3)
    status: ListingStatus
    public_url: str | None = None
    sku: str
    price: float = Field(gt=0)
    currency: str = Field(min_length=3, max_length=3)
    warnings: list[str] = Field(default_factory=list)


class MarketplaceOrder(BaseModel):
    marketplace: MarketplaceName
    order_id: str = Field(min_length=3)
    listing_id: str = Field(min_length=3)
    sku: str = Field(min_length=3)
    quantity: int = Field(gt=0)
    sale_price: float = Field(gt=0)
    currency: str = Field(min_length=3, max_length=3)
    buyer_country: str = Field(min_length=2, max_length=64)
    shipping_address_hash: str = Field(min_length=8, description="Hashed address reference; do not store raw PII in core flow.")


class PriceUpdateRequest(BaseModel):
    listing_id: str = Field(min_length=3)
    new_price: float = Field(gt=0)
    currency: str = Field(default="GBP", min_length=3, max_length=3)

    @field_validator("currency")
    @classmethod
    def uppercase_currency(cls, value: str) -> str:
        return value.upper()
