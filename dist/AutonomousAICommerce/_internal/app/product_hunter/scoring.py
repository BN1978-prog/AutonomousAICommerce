from __future__ import annotations

from app.schemas.decision import CommerceDecision, DecisionStatus
from app.product_hunter.schemas import DemandSignal
from app.suppliers.schemas import SupplierProduct


class OpportunityScorer:
    def score(self, product: SupplierProduct, signals: list[DemandSignal], decision: CommerceDecision) -> float:
        demand = self._aggregate(signals)
        decision_factor = self._decision_factor(decision.status)
        margin = max(min((decision.profit.margin_percent if decision.profit else 0) / 60, 1), 0)
        roi = max(min((decision.profit.roi_percent if decision.profit else 0) / 150, 1), 0)
        supplier_quality = product.supplier_rating / 5
        delivery_quality = max(0, 1 - (product.estimated_delivery_days / 60))
        return round(max(0, min(
            demand * 0.30
            + margin * 0.22
            + roi * 0.15
            + supplier_quality * 0.13
            + delivery_quality * 0.10
            + decision_factor * 0.10,
            1,
        )), 3)

    @staticmethod
    def _aggregate(signals: list[DemandSignal]) -> float:
        weighted = sum(signal.score * signal.confidence for signal in signals)
        weights = sum(signal.confidence for signal in signals) or 1
        return weighted / weights

    @staticmethod
    def _decision_factor(status: DecisionStatus) -> float:
        if status == DecisionStatus.APPROVED:
            return 1.0
        if status == DecisionStatus.WATCHLIST:
            return 0.55
        return 0.0
