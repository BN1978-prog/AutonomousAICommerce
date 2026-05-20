from pydantic import BaseModel, Field
from typing import Literal

Decision = Literal["approve", "watch", "reject"]

class ProductOpportunityInput(BaseModel):
    title: str
    supplier_cost: float = Field(gt=0)
    expected_sale_price: float = Field(gt=0)
    shipping_cost: float = Field(ge=0, default=0)
    platform_fee_percent: float = Field(ge=0, le=100, default=12)
    estimated_return_rate_percent: float = Field(ge=0, le=100, default=5)
    demand_score: float = Field(ge=0, le=100, default=50)
    competition_score: float = Field(ge=0, le=100, default=50)
    supplier_trust_score: float = Field(ge=0, le=100, default=80)

class ProductOpportunityScore(BaseModel):
    title: str
    net_profit: float
    margin_percent: float
    risk_score: float
    opportunity_score: float
    decision: Decision
    explanation: str

def score_product_opportunity(item: ProductOpportunityInput) -> ProductOpportunityScore:
    platform_fee = item.expected_sale_price * (item.platform_fee_percent / 100)
    expected_refund_cost = item.expected_sale_price * (item.estimated_return_rate_percent / 100) * 0.35
    net_profit = item.expected_sale_price - item.supplier_cost - item.shipping_cost - platform_fee - expected_refund_cost
    margin_percent = (net_profit / item.expected_sale_price) * 100 if item.expected_sale_price else 0

    demand_component = item.demand_score * 0.35
    competition_component = (100 - item.competition_score) * 0.20
    supplier_component = item.supplier_trust_score * 0.20
    margin_component = max(0, min(100, margin_percent * 2)) * 0.25

    opportunity_score = demand_component + competition_component + supplier_component + margin_component

    risk_score = (
        item.competition_score * 0.25
        + (100 - item.supplier_trust_score) * 0.35
        + item.estimated_return_rate_percent * 0.25
        + max(0, 25 - margin_percent) * 0.15
    )

    if net_profit <= 0 or margin_percent < 15 or risk_score > 55:
        decision: Decision = "reject"
    elif opportunity_score >= 65 and margin_percent >= 25 and risk_score <= 40:
        decision = "approve"
    else:
        decision = "watch"

    return ProductOpportunityScore(
        title=item.title,
        net_profit=round(net_profit, 2),
        margin_percent=round(margin_percent, 2),
        risk_score=round(risk_score, 2),
        opportunity_score=round(opportunity_score, 2),
        decision=decision,
        explanation=(
            f"Decision={decision}; net profit={net_profit:.2f}; "
            f"margin={margin_percent:.2f}%; risk={risk_score:.2f}; "
            f"opportunity={opportunity_score:.2f}."
        ),
    )
