from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class FeeModel(BaseModel):
    """Marketplace/payment/tax assumptions for profit calculation."""

    marketplace_fee_percent: float = Field(default=12.0, ge=0, le=50)
    marketplace_fixed_fee: float = Field(default=0.0, ge=0)
    payment_fee_percent: float = Field(default=2.9, ge=0, le=20)
    payment_fixed_fee: float = Field(default=0.30, ge=0)
    vat_or_sales_tax_percent: float = Field(default=0.0, ge=0, le=30)
    currency_conversion_percent: float = Field(default=0.0, ge=0, le=10)


class CostAssumptions(BaseModel):
    """Commercial assumptions used by the governor before autonomous execution."""

    estimated_ad_cost: float = Field(default=0.0, ge=0)
    estimated_refund_rate: float = Field(default=0.05, ge=0, le=1)
    refund_processing_cost: float = Field(default=1.50, ge=0)
    packaging_cost: float = Field(default=0.50, ge=0)
    buffer_percent: float = Field(default=3.0, ge=0, le=30)


class AdvancedProfitBreakdown(BaseModel):
    sale_price: float
    supplier_cost: float
    supplier_shipping: float
    marketplace_fee: float
    payment_fee: float
    tax_estimate: float
    currency_conversion_cost: float
    ad_cost: float
    packaging_cost: float
    expected_refund_cost: float
    risk_buffer: float
    total_cost: float
    net_profit: float
    margin_percent: float
    roi_percent: float
    break_even_price: float


class ProfitScenario(BaseModel):
    name: str = Field(min_length=1)
    sale_price_multiplier: float = Field(default=1.0, gt=0)
    refund_rate_multiplier: float = Field(default=1.0, ge=0)
    ad_cost_multiplier: float = Field(default=1.0, ge=0)


class ScenarioResult(BaseModel):
    scenario: str
    profit: AdvancedProfitBreakdown


class AdvancedEvaluationRequest(BaseModel):
    title: str = Field(min_length=3, max_length=140)
    category: str = Field(default="other")
    target_market: str = Field(default="UK", min_length=2, max_length=64)
    currency: str = Field(default="GBP", min_length=3, max_length=3)
    expected_sale_price: float = Field(gt=0)
    supplier_cost: float = Field(gt=0)
    supplier_shipping: float = Field(ge=0)
    estimated_delivery_days: int = Field(ge=1, le=120)
    stock_available: int = Field(ge=0)
    supplier_risk_score: float = Field(ge=0, le=1)
    return_risk_score: float = Field(default=0.1, ge=0, le=1)
    demand_score: float = Field(default=0.5, ge=0, le=1)
    competition_score: float = Field(default=0.5, ge=0, le=1)
    fee_model: FeeModel = Field(default_factory=FeeModel)
    cost_assumptions: CostAssumptions = Field(default_factory=CostAssumptions)

    @field_validator("currency")
    @classmethod
    def uppercase_currency(cls, value: str) -> str:
        return value.upper()
