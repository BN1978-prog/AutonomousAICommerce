from app.core.config import Settings
from app.schemas.decision import CommerceDecision, DecisionStatus
from app.schemas.product import ProductCandidate, SupplierOffer
from app.services.profit_engine import ProfitEngine
from app.services.risk_engine import RiskEngine


class AIGovernor:
    """Safety gate. Every autonomous action must pass this class first."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.profit_engine = ProfitEngine()
        self.risk_engine = RiskEngine()

    def evaluate(self, product: ProductCandidate, current_daily_spend: float = 0.0) -> CommerceDecision:
        best_offer: SupplierOffer | None = None
        best_profit = None
        best_risk = 1.0

        for offer in product.offers:
            profit = self.profit_engine.calculate(product, offer)
            risk = self.risk_engine.score(product, offer)
            if best_profit is None or profit.net_profit > best_profit.net_profit:
                best_offer = offer
                best_profit = profit
                best_risk = risk

        reasons: list[str] = []
        if best_offer is None or best_profit is None:
            return CommerceDecision(status=DecisionStatus.REJECTED, risk_score=1, reasons=["No valid supplier offers"])

        if best_offer.stock_available <= 0:
            reasons.append("Supplier has no available stock")
        if best_profit.margin_percent < self.settings.min_margin_percent:
            reasons.append(f"Margin {best_profit.margin_percent}% is below minimum {self.settings.min_margin_percent}%")
        if best_offer.unit_cost + best_offer.shipping_cost > self.settings.max_order_value:
            reasons.append("Supplier cost exceeds max order value")
        if current_daily_spend + best_offer.unit_cost + best_offer.shipping_cost > self.settings.max_daily_spend:
            reasons.append("Daily spend limit would be exceeded")
        if best_offer.supplier_risk_score > self.settings.max_supplier_risk_score:
            reasons.append("Supplier risk score is too high")
        if product.return_risk_score > self.settings.max_return_risk_score:
            reasons.append("Return risk score is too high")
        if best_risk > 0.55:
            reasons.append("Combined risk score is too high")

        if reasons:
            status = DecisionStatus.REJECTED
        elif best_risk > 0.40:
            status = DecisionStatus.WATCHLIST
            reasons.append("Profitable but requires monitoring due to medium risk")
        else:
            status = DecisionStatus.APPROVED
            reasons.append("Passed all profit and risk checks")

        return CommerceDecision(
            status=status,
            selected_offer=best_offer,
            profit=best_profit,
            risk_score=best_risk,
            reasons=reasons,
        )
