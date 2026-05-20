from __future__ import annotations

from app.core.config import Settings
from app.product_hunter.demand import DemandEstimator
from app.product_hunter.mapper import supplier_product_to_candidate
from app.product_hunter.schemas import HunterRequest, HunterResponse, ProductOpportunity
from app.product_hunter.scoring import OpportunityScorer
from app.services.governor import AIGovernor
from app.suppliers.registry import SupplierRegistry
from app.suppliers.schemas import SupplierProduct, SupplierSearchQuery


class ProductHunterService:
    def __init__(self, settings: Settings, supplier_registry: SupplierRegistry):
        self.settings = settings
        self.supplier_registry = supplier_registry
        self.demand = DemandEstimator()
        self.scorer = OpportunityScorer()
        self.governor = AIGovernor(settings)

    async def hunt(self, request: HunterRequest, current_daily_spend: float = 0.0) -> HunterResponse:
        supplier_query = SupplierSearchQuery(
            keywords=request.keywords,
            target_market=request.target_market,
            currency=request.currency,
            max_unit_cost=request.max_unit_cost,
            min_stock=request.min_stock,
            max_delivery_days=request.max_delivery_days,
        )
        supplier_products = await self.supplier_registry.search_all(supplier_query)
        opportunities: list[ProductOpportunity] = []
        rejected_count = 0

        for supplier_product in supplier_products:
            opportunity = self._evaluate_supplier_product(supplier_product, request, current_daily_spend)
            if opportunity.opportunity_score >= request.min_opportunity_score and opportunity.decision.status.value != "rejected":
                opportunities.append(opportunity)
            else:
                rejected_count += 1

        opportunities.sort(key=lambda item: item.opportunity_score, reverse=True)
        return HunterResponse(
            query=request,
            opportunities=opportunities[: request.max_results],
            rejected_count=rejected_count,
            total_supplier_products=len(supplier_products),
        )

    def _evaluate_supplier_product(self, supplier_product: SupplierProduct, request: HunterRequest, current_daily_spend: float) -> ProductOpportunity:
        signals = self.demand.estimate(supplier_product, request.target_market)
        demand_score = self.demand.aggregate(signals)
        competition_score = self._estimate_competition(supplier_product, demand_score)
        sale_price = self._recommended_sale_price(supplier_product, demand_score, competition_score)
        candidate = supplier_product_to_candidate(
            supplier_product,
            expected_sale_price=sale_price,
            target_market=request.target_market,
            currency=request.currency,
            demand_score=demand_score,
            competition_score=competition_score,
            platform_fee_percent=request.marketplace_fee_percent,
            payment_fee_percent=request.payment_fee_percent,
            estimated_ad_cost=request.estimated_ad_cost,
        )
        decision = self.governor.evaluate(candidate, current_daily_spend=current_daily_spend)
        score = self.scorer.score(supplier_product, signals, decision)
        explanation = self._explain(score, decision, demand_score, competition_score, sale_price)
        return ProductOpportunity(
            candidate=candidate,
            source_product=supplier_product,
            demand_signals=signals,
            opportunity_score=score,
            decision=decision,
            recommended_sale_price=sale_price,
            explanation=explanation,
        )

    @staticmethod
    def _estimate_competition(product: SupplierProduct, demand_score: float) -> float:
        # MVP proxy: high stock and broad categories imply more competition; higher supplier rating offsets risk.
        stock_pressure = min(product.stock_available / 500, 1.0) * 0.25
        category_pressure = 0.20 if product.category.lower() in {"home", "beauty", "electronics_accessories"} else 0.12
        demand_pressure = demand_score * 0.25
        quality_offset = (product.supplier_rating / 5) * 0.10
        return round(max(0.05, min(0.85, 0.22 + stock_pressure + category_pressure + demand_pressure - quality_offset)), 3)

    @staticmethod
    def _recommended_sale_price(product: SupplierProduct, demand_score: float, competition_score: float) -> float:
        landed_cost = product.unit_cost.amount + product.shipping_cost.amount
        markup = 1.75 + (demand_score * 0.55) - (competition_score * 0.35)
        minimum_markup = 1.45
        sale_price = max(landed_cost * max(markup, minimum_markup), landed_cost + 8.0)
        return round(sale_price, 2)

    @staticmethod
    def _explain(score: float, decision, demand_score: float, competition_score: float, sale_price: float) -> list[str]:
        return [
            f"Opportunity score: {score}",
            f"Demand score: {demand_score}",
            f"Competition score: {competition_score}",
            f"Recommended sale price: {sale_price}",
            f"Governor decision: {decision.status.value}",
        ]
