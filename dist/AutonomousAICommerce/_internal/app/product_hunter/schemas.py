from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field, field_validator
from app.schemas.decision import CommerceDecision
from app.schemas.product import ProductCandidate
from app.suppliers.schemas import SupplierProduct


class OpportunityStatus(str, Enum):
    APPROVED = "approved"
    WATCHLIST = "watchlist"
    REJECTED = "rejected"


class DemandSignal(BaseModel):
    source: str = Field(min_length=2, max_length=80)
    score: float = Field(ge=0, le=1)
    confidence: float = Field(default=0.5, ge=0, le=1)
    notes: str = Field(default="", max_length=500)


class HunterRequest(BaseModel):
    keywords: str = Field(min_length=2, max_length=160)
    target_market: str = Field(default="UK", min_length=2, max_length=64)
    currency: str = Field(default="GBP", min_length=3, max_length=3)
    max_unit_cost: float | None = Field(default=None, gt=0)
    min_stock: int = Field(default=1, ge=0)
    max_delivery_days: int = Field(default=30, ge=1, le=120)
    marketplace_fee_percent: float = Field(default=12.0, ge=0, le=50)
    payment_fee_percent: float = Field(default=2.9, ge=0, le=20)
    estimated_ad_cost: float = Field(default=0.0, ge=0)
    min_opportunity_score: float = Field(default=0.45, ge=0, le=1)
    max_results: int = Field(default=10, ge=1, le=100)

    @field_validator("currency")
    @classmethod
    def uppercase_currency(cls, value: str) -> str:
        return value.upper()


class ProductOpportunity(BaseModel):
    candidate: ProductCandidate
    source_product: SupplierProduct
    demand_signals: list[DemandSignal]
    opportunity_score: float = Field(ge=0, le=1)
    decision: CommerceDecision
    recommended_sale_price: float = Field(gt=0)
    explanation: list[str] = Field(default_factory=list)


class HunterResponse(BaseModel):
    query: HunterRequest
    opportunities: list[ProductOpportunity]
    rejected_count: int = Field(ge=0)
    total_supplier_products: int = Field(ge=0)
