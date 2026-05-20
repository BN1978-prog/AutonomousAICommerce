from __future__ import annotations

from app.risk.schemas import AdvancedRiskReport, RiskSignal


class AdvancedRiskEngine:
    """Weighted risk model for autonomous commerce decisions."""

    def evaluate(
        self,
        *,
        supplier_risk_score: float,
        return_risk_score: float,
        demand_score: float,
        competition_score: float,
        estimated_delivery_days: int,
        stock_available: int,
        margin_percent: float,
        roi_percent: float,
    ) -> AdvancedRiskReport:
        delivery_risk = min(estimated_delivery_days / 45, 1.0)
        stock_risk = 1.0 if stock_available <= 0 else min(20 / stock_available, 1.0)
        demand_risk = 1 - demand_score
        margin_risk = 1.0 if margin_percent < 0 else max(0.0, min(1.0, (30 - margin_percent) / 30))
        roi_risk = 1.0 if roi_percent < 0 else max(0.0, min(1.0, (50 - roi_percent) / 50))
        signals = [
            RiskSignal(name="supplier", score=supplier_risk_score, weight=0.22, explanation="Supplier reliability/compliance risk"),
            RiskSignal(name="returns", score=return_risk_score, weight=0.16, explanation="Expected return/refund exposure"),
            RiskSignal(name="delivery", score=delivery_risk, weight=0.13, explanation="Long delivery increases disputes and refunds"),
            RiskSignal(name="stock", score=stock_risk, weight=0.09, explanation="Low stock can break fulfillment"),
            RiskSignal(name="demand", score=demand_risk, weight=0.14, explanation="Weak demand reduces sell-through"),
            RiskSignal(name="competition", score=competition_score, weight=0.10, explanation="High competition pressures margin"),
            RiskSignal(name="margin", score=margin_risk, weight=0.10, explanation="Thin margin creates loss risk"),
            RiskSignal(name="roi", score=roi_risk, weight=0.06, explanation="Low ROI ties up cash inefficiently"),
        ]
        weighted = sum(signal.score * signal.weight for signal in signals)
        weight_total = sum(signal.weight for signal in signals)
        total_score = round(max(0.0, min(weighted / weight_total, 1.0)), 4)
        blocking: list[str] = []
        watch: list[str] = []
        if stock_available <= 0:
            blocking.append("No supplier stock available")
        if supplier_risk_score >= 0.70:
            blocking.append("Supplier risk is critically high")
        if margin_percent < 0:
            blocking.append("Expected net profit is negative")
        if estimated_delivery_days > 60:
            blocking.append("Delivery estimate exceeds 60 days")
        if 0.45 <= total_score < 0.65:
            watch.append("Combined risk requires monitoring")
        if return_risk_score >= 0.35:
            watch.append("Return risk is elevated")
        level = "low" if total_score < 0.35 else "medium" if total_score < 0.65 else "high"
        if blocking:
            level = "high"
        return AdvancedRiskReport(total_score=total_score, level=level, signals=signals, blocking_reasons=blocking, watch_reasons=watch)
