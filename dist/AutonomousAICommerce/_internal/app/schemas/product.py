from enum import Enum
from pydantic import BaseModel, Field, field_validator


class ProductCategory(str, Enum):
    HOME = "home"
    PETS = "pets"
    AUTO = "auto"
    BEAUTY = "beauty"
    ELECTRONICS_ACCESSORIES = "electronics_accessories"
    OTHER = "other"


class SupplierOffer(BaseModel):
    supplier_id: str = Field(min_length=1)
    supplier_name: str = Field(min_length=1)
    country: str = Field(min_length=2, max_length=64)
    product_url: str | None = None
    unit_cost: float = Field(gt=0)
    shipping_cost: float = Field(ge=0)
    estimated_delivery_days: int = Field(ge=1, le=120)
    stock_available: int = Field(ge=0)
    supplier_risk_score: float = Field(ge=0, le=1)


class ProductCandidate(BaseModel):
    title: str = Field(min_length=3, max_length=140)
    category: ProductCategory = ProductCategory.OTHER
    target_market: str = Field(default="UK", min_length=2, max_length=64)
    currency: str = Field(default="GBP", min_length=3, max_length=3)
    expected_sale_price: float = Field(gt=0)
    platform_fee_percent: float = Field(default=12.0, ge=0, le=50)
    payment_fee_percent: float = Field(default=2.9, ge=0, le=20)
    estimated_ad_cost: float = Field(default=0.0, ge=0)
    estimated_refund_rate: float = Field(default=0.05, ge=0, le=1)
    return_risk_score: float = Field(default=0.1, ge=0, le=1)
    demand_score: float = Field(default=0.5, ge=0, le=1)
    competition_score: float = Field(default=0.5, ge=0, le=1)
    offers: list[SupplierOffer] = Field(min_length=1)

    @field_validator("currency")
    @classmethod
    def uppercase_currency(cls, value: str) -> str:
        return value.upper()
