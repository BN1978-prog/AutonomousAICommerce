from __future__ import annotations

from app.core.config import Settings
from app.finance.advanced_profit_engine import AdvancedProfitEngine
from app.finance.schemas import AdvancedEvaluationRequest
from app.risk.advanced_risk_engine import AdvancedRiskEngine
from app.schemas.decision import AdvancedCommerceDecision, DecisionStatus


class AdvancedAIGovernor:
    """Higher fidelity approval gate for autonomous buying/listing decisions."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.profit_engine = AdvancedProfitEngine()
        self.risk_engine = AdvancedRiskEngine()

    def evaluate(self, request: AdvancedEvaluationRequest, current_daily_spend: float = 0.0) -> AdvancedCommerceDecision:
        profit = self.profit_engine.calculate(
            sale_price=request.expected_sale_price,
            supplier_cost=request.supplier_cost,
            supplier_shipping=request.supplier_shipping,
            fee_model=request.fee_model,
            cost_assumptions=request.cost_assumptions,
        )
        risk = self.risk_engine.evaluate(
            supplier_risk_score=request.supplier_risk_score,
            return_risk_score=request.return_risk_score,
            demand_score=request.demand_score,
            competition_score=request.competition_score,
            estimated_delivery_days=request.estimated_delivery_days,
            stock_available=request.stock_available,
            margin_percent=profit.margin_percent,
            roi_percent=profit.roi_percent,
        )
        reasons: list[str] = []
        reasons.extend(risk.blocking_reasons)
        if profit.margin_percent < self.settings.min_margin_percent:
            reasons.append(f"Margin {profit.margin_percent}% is below minimum {self.settings.min_margin_percent}%")
        if request.supplier_cost + request.supplier_shipping > self.settings.max_order_value:
            reasons.append("Supplier cost exceeds max order value")
        if current_daily_spend + request.supplier_cost + request.supplier_shipping > self.settings.max_daily_spend:
            reasons.append("Daily spend limit would be exceeded")
        if request.supplier_risk_score > self.settings.max_supplier_risk_score:
            reasons.append("Supplier risk score exceeds configured limit")
        if request.return_risk_score > self.settings.max_return_risk_score:
            reasons.append("Return risk score exceeds configured limit")
        if risk.total_score >= 0.65:
            reasons.append("Combined risk score is high")

        if reasons:
            status = DecisionStatus.REJECTED
            allowed = False
        elif risk.watch_reasons or risk.total_score >= 0.35:
            status = DecisionStatus.WATCHLIST
            reasons = risk.watch_reasons or ["Profitable but risk requires monitoring"]
            allowed = False
        else:
            status = DecisionStatus.APPROVED
            reasons = ["Passed advanced profit, risk, and budget checks"]
            allowed = bool(self.settings.enable_autonomous_purchase)

        return AdvancedCommerceDecision(
            status=status,
            profit=profit,
            risk=risk,
            reasons=reasons,
            allowed_to_autonomously_buy=allowed,
        )
