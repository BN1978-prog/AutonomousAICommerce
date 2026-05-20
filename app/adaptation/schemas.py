from __future__ import annotations

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, field_validator


class OutcomeType(str, Enum):
    SALE = "sale"
    REFUND = "refund"
    RETURN = "return"
    COMPLAINT = "complaint"
    LATE_DELIVERY = "late_delivery"
    SUPPLIER_FAILURE = "supplier_failure"
    PRICE_CHANGE = "price_change"


class ProductPerformanceEvent(BaseModel):
    sku: str = Field(min_length=1, max_length=80)
    product_title: str = Field(min_length=3, max_length=160)
    supplier_id: str = Field(min_length=1, max_length=80)
    marketplace: str = Field(min_length=1, max_length=80)
    category: str = Field(default="other", min_length=1, max_length=80)
    target_market: str = Field(default="UK", min_length=2, max_length=64)
    outcome: OutcomeType
    sale_price: float = Field(ge=0)
    supplier_cost: float = Field(ge=0)
    shipping_cost: float = Field(ge=0)
    fees: float = Field(default=0.0, ge=0)
    refund_cost: float = Field(default=0.0, ge=0)
    delivery_days: int = Field(default=7, ge=0, le=180)
    customer_rating: float | None = Field(default=None, ge=1, le=5)
    occurred_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("supplier_id", "marketplace", "category", "target_market")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        return value.strip()


class EntityScore(BaseModel):
    entity_id: str
    score: float = Field(ge=0, le=1)
    sample_size: int = Field(ge=0)
    notes: list[str] = Field(default_factory=list)


class AdaptationRecommendation(BaseModel):
    sku: str | None = None
    action: str = Field(min_length=3)
    confidence: float = Field(ge=0, le=1)
    reason: str = Field(min_length=3)
    max_budget_multiplier: float = Field(default=1.0, ge=0, le=2)
    suggested_price_multiplier: float = Field(default=1.0, ge=0.5, le=2.0)


class LearningSummary(BaseModel):
    events_processed: int = Field(ge=0)
    total_revenue: float
    total_profit: float
    average_margin_percent: float
    refund_rate: float = Field(ge=0, le=1)
    complaint_rate: float = Field(ge=0, le=1)
    late_delivery_rate: float = Field(ge=0, le=1)
    supplier_scores: list[EntityScore]
    marketplace_scores: list[EntityScore]
    recommendations: list[AdaptationRecommendation]


class AdaptationRequest(BaseModel):
    events: list[ProductPerformanceEvent] = Field(min_length=1, max_length=500)
    min_margin_percent: float = Field(default=20.0, ge=0, le=95)
    max_refund_rate: float = Field(default=0.12, ge=0, le=1)
    max_complaint_rate: float = Field(default=0.05, ge=0, le=1)
    max_late_delivery_rate: float = Field(default=0.15, ge=0, le=1)
