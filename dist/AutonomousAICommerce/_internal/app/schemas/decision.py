from enum import Enum
from pydantic import BaseModel, Field
from app.schemas.product import SupplierOffer


class DecisionStatus(str, Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    WATCHLIST = "watchlist"


class ProfitBreakdown(BaseModel):
    sale_price: float
    supplier_cost: float
    supplier_shipping: float
    platform_fee: float
    payment_fee: float
    ad_cost: float
    expected_refund_cost: float
    net_profit: float
    margin_percent: float
    roi_percent: float


class CommerceDecision(BaseModel):
    status: DecisionStatus
    selected_offer: SupplierOffer | None = None
    profit: ProfitBreakdown | None = None
    risk_score: float = Field(ge=0, le=1)
    reasons: list[str]

from app.finance.schemas import AdvancedProfitBreakdown
from app.risk.schemas import AdvancedRiskReport


class AdvancedCommerceDecision(BaseModel):
    status: DecisionStatus
    profit: AdvancedProfitBreakdown
    risk: AdvancedRiskReport
    reasons: list[str]
    allowed_to_autonomously_buy: bool = False
