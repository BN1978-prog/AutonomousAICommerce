from app.schemas.product import ProductCandidate, SupplierOffer


class RiskEngine:
    """Combines known risk signals into a bounded 0..1 score."""

    @staticmethod
    def score(product: ProductCandidate, offer: SupplierOffer) -> float:
        delivery_risk = min(offer.estimated_delivery_days / 60, 1.0)
        stock_risk = 1.0 if offer.stock_available == 0 else min(10 / offer.stock_available, 1.0) * 0.4
        market_risk = (product.competition_score * 0.45) + ((1 - product.demand_score) * 0.55)
        combined = (
            offer.supplier_risk_score * 0.35
            + product.return_risk_score * 0.20
            + delivery_risk * 0.15
            + stock_risk * 0.10
            + market_risk * 0.20
        )
        return round(max(0.0, min(combined, 1.0)), 4)
