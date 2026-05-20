from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class Decision(str, Enum):
    LIST = "LIST"
    REJECT = "REJECT"
    PAUSE = "PAUSE"
    REVIEW = "REVIEW"

class ProductCandidate(BaseModel):
    supplier_id: str
    supplier_name: str
    title: str
    source_country: str
    target_market: str
    category: str
    supplier_price: float
    shipping_cost: float
    estimated_sale_price: float
    platform_fee_percent: float = 12
    payment_fee_percent: float = 2.9
    estimated_refund_rate_percent: float = 5
    delivery_days: int
    supplier_rating: float = Field(ge=0, le=5)
    monthly_search_score: int = Field(ge=0, le=100)
    competition_score: int = Field(ge=0, le=100)
    prohibited: bool = False

class ProfitResult(BaseModel):
    gross_revenue: float
    total_cost: float
    net_profit: float
    net_margin_percent: float

class RiskResult(BaseModel):
    supplier_risk: int
    logistics_risk: int
    country_risk: int
    compliance_risk: int
    total_risk: int
    reasons: List[str]

class CommerceDecision(BaseModel):
    product: ProductCandidate
    profit: ProfitResult
    risk: RiskResult
    decision: Decision
    confidence: float
    actions: List[str]
