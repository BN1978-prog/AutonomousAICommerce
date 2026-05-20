from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field, field_validator

from app.marketplaces.schemas import MarketplaceName
from app.finance.schemas import FeeModel, CostAssumptions


class FulfillmentStatus(str, Enum):
    APPROVED_DRY_RUN = "approved_dry_run"
    PURCHASED = "purchased"
    BLOCKED = "blocked"
    FAILED = "failed"


class ShippingAddress(BaseModel):
    """Address object used only at the supplier execution boundary."""

    buyer_name: str = Field(min_length=2, max_length=120)
    address_line1: str = Field(min_length=3, max_length=160)
    city: str = Field(min_length=2, max_length=120)
    country: str = Field(min_length=2, max_length=64)
    postal_code: str = Field(min_length=2, max_length=32)


class FulfillmentRequest(BaseModel):
    marketplace: MarketplaceName = MarketplaceName.MOCK
    order_id: str = Field(min_length=3)
    listing_id: str = Field(min_length=3)
    sku: str = Field(min_length=3)
    supplier_id: str = Field(min_length=1)
    supplier_product_id: str = Field(min_length=1)
    quantity: int = Field(default=1, ge=1, le=100)
    sale_price: float = Field(gt=0)
    currency: str = Field(default="GBP", min_length=3, max_length=3)
    buyer_country: str = Field(default="UK", min_length=2, max_length=64)
    shipping_address: ShippingAddress
    demand_score: float = Field(default=0.60, ge=0, le=1)
    competition_score: float = Field(default=0.45, ge=0, le=1)
    fee_model: FeeModel = Field(default_factory=FeeModel)
    cost_assumptions: CostAssumptions = Field(default_factory=CostAssumptions)
    dry_run: bool = True

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        return value.upper()


class FulfillmentResult(BaseModel):
    status: FulfillmentStatus
    order_id: str
    supplier_id: str
    supplier_product_id: str
    supplier_order_id: str | None = None
    tracking_number: str | None = None
    net_profit: float | None = None
    margin_percent: float | None = None
    reasons: list[str] = Field(default_factory=list)
    audit_events: list[str] = Field(default_factory=list)
