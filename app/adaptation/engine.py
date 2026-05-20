from __future__ import annotations

from collections import defaultdict
from statistics import mean

from app.adaptation.schemas import (
    AdaptationRecommendation,
    AdaptationRequest,
    EntityScore,
    LearningSummary,
    OutcomeType,
    ProductPerformanceEvent,
)


class SelfLearningEngine:
    """Deterministic learning engine for safe autonomous adaptation.

    This module intentionally uses transparent rules rather than opaque model
    updates. It produces recommendations and risk scores that can be audited,
    tested, and used by the AI Governor before autonomous execution.
    """

    def analyze(self, request: AdaptationRequest) -> LearningSummary:
        events = request.events
        total_revenue = sum(e.sale_price for e in events if e.outcome == OutcomeType.SALE)
        total_profit = sum(self._event_profit(e) for e in events)
        margins = [self._margin_percent(e) for e in events if e.sale_price > 0]
        avg_margin = mean(margins) if margins else 0.0

        refund_rate = self._rate(events, {OutcomeType.REFUND, OutcomeType.RETURN})
        complaint_rate = self._rate(events, {OutcomeType.COMPLAINT})
        late_rate = self._rate(events, {OutcomeType.LATE_DELIVERY})

        supplier_scores = self._entity_scores(events, "supplier")
        marketplace_scores = self._entity_scores(events, "marketplace")
        recommendations = self._recommend(events, request, avg_margin, refund_rate, complaint_rate, late_rate)

        return LearningSummary(
            events_processed=len(events),
            total_revenue=round(total_revenue, 2),
            total_profit=round(total_profit, 2),
            average_margin_percent=round(avg_margin, 2),
            refund_rate=round(refund_rate, 4),
            complaint_rate=round(complaint_rate, 4),
            late_delivery_rate=round(late_rate, 4),
            supplier_scores=supplier_scores,
            marketplace_scores=marketplace_scores,
            recommendations=recommendations,
        )

    def _event_profit(self, event: ProductPerformanceEvent) -> float:
        revenue = event.sale_price if event.outcome == OutcomeType.SALE else 0.0
        # For bad outcomes, refund_cost and operational costs still matter.
        return revenue - event.supplier_cost - event.shipping_cost - event.fees - event.refund_cost

    def _margin_percent(self, event: ProductPerformanceEvent) -> float:
        if event.sale_price <= 0:
            return 0.0
        return (self._event_profit(event) / event.sale_price) * 100

    def _rate(self, events: list[ProductPerformanceEvent], outcomes: set[OutcomeType]) -> float:
        if not events:
            return 0.0
        return sum(1 for event in events if event.outcome in outcomes) / len(events)

    def _entity_scores(self, events: list[ProductPerformanceEvent], kind: str) -> list[EntityScore]:
        grouped: dict[str, list[ProductPerformanceEvent]] = defaultdict(list)
        for event in events:
            key = event.supplier_id if kind == "supplier" else event.marketplace
            grouped[key].append(event)

        results: list[EntityScore] = []
        for entity_id, group in sorted(grouped.items()):
            refund_rate = self._rate(group, {OutcomeType.REFUND, OutcomeType.RETURN})
            complaint_rate = self._rate(group, {OutcomeType.COMPLAINT})
            late_rate = self._rate(group, {OutcomeType.LATE_DELIVERY, OutcomeType.SUPPLIER_FAILURE})
            margin_values = [max(min(self._margin_percent(e), 80), -80) for e in group if e.sale_price > 0]
            margin_component = ((mean(margin_values) if margin_values else 0) + 80) / 160
            reliability_component = 1 - min((refund_rate * 1.5) + (complaint_rate * 2.0) + late_rate, 1)
            score = (margin_component * 0.45) + (reliability_component * 0.55)
            notes = []
            if refund_rate > 0.12:
                notes.append("high refund/return rate")
            if complaint_rate > 0.05:
                notes.append("customer complaints detected")
            if late_rate > 0.15:
                notes.append("delivery or supplier reliability issue")
            if not notes:
                notes.append("within current operating limits")
            results.append(EntityScore(entity_id=entity_id, score=round(max(0, min(score, 1)), 4), sample_size=len(group), notes=notes))
        return sorted(results, key=lambda item: item.score, reverse=True)

    def _recommend(
        self,
        events: list[ProductPerformanceEvent],
        request: AdaptationRequest,
        avg_margin: float,
        refund_rate: float,
        complaint_rate: float,
        late_rate: float,
    ) -> list[AdaptationRecommendation]:
        recs: list[AdaptationRecommendation] = []

        if avg_margin < request.min_margin_percent:
            recs.append(
                AdaptationRecommendation(
                    action="raise_prices_or_pause_low_margin_items",
                    confidence=0.86,
                    reason=f"Average margin {avg_margin:.2f}% is below required {request.min_margin_percent:.2f}%.",
                    max_budget_multiplier=0.55,
                    suggested_price_multiplier=1.08,
                )
            )
        if refund_rate > request.max_refund_rate:
            recs.append(
                AdaptationRecommendation(
                    action="reduce_exposure_to_high_refund_categories",
                    confidence=0.82,
                    reason=f"Refund/return rate {refund_rate:.2%} exceeds limit {request.max_refund_rate:.2%}.",
                    max_budget_multiplier=0.45,
                    suggested_price_multiplier=1.0,
                )
            )
        if complaint_rate > request.max_complaint_rate:
            recs.append(
                AdaptationRecommendation(
                    action="pause_items_with_customer_complaints",
                    confidence=0.9,
                    reason=f"Complaint rate {complaint_rate:.2%} exceeds limit {request.max_complaint_rate:.2%}.",
                    max_budget_multiplier=0.3,
                    suggested_price_multiplier=1.0,
                )
            )
        if late_rate > request.max_late_delivery_rate:
            recs.append(
                AdaptationRecommendation(
                    action="prefer_faster_suppliers_or_extend_delivery_promises",
                    confidence=0.78,
                    reason=f"Late delivery rate {late_rate:.2%} exceeds limit {request.max_late_delivery_rate:.2%}.",
                    max_budget_multiplier=0.65,
                    suggested_price_multiplier=1.02,
                )
            )

        # SKU-level recommendations.
        grouped: dict[str, list[ProductPerformanceEvent]] = defaultdict(list)
        for event in events:
            grouped[event.sku].append(event)
        for sku, group in sorted(grouped.items()):
            sku_margin_values = [self._margin_percent(e) for e in group if e.sale_price > 0]
            sku_margin = mean(sku_margin_values) if sku_margin_values else 0.0
            sku_bad_rate = self._rate(group, {OutcomeType.REFUND, OutcomeType.RETURN, OutcomeType.COMPLAINT, OutcomeType.LATE_DELIVERY, OutcomeType.SUPPLIER_FAILURE})
            if len(group) >= 2 and sku_margin >= request.min_margin_percent + 8 and sku_bad_rate <= 0.05:
                recs.append(
                    AdaptationRecommendation(
                        sku=sku,
                        action="scale_budget_carefully",
                        confidence=0.74,
                        reason=f"SKU has strong margin {sku_margin:.2f}% and low bad-outcome rate {sku_bad_rate:.2%}.",
                        max_budget_multiplier=1.25,
                        suggested_price_multiplier=1.0,
                    )
                )
            elif len(group) >= 2 and (sku_margin < request.min_margin_percent or sku_bad_rate > 0.2):
                recs.append(
                    AdaptationRecommendation(
                        sku=sku,
                        action="pause_or_reprice_sku",
                        confidence=0.8,
                        reason=f"SKU margin {sku_margin:.2f}% or bad-outcome rate {sku_bad_rate:.2%} is outside limits.",
                        max_budget_multiplier=0.0,
                        suggested_price_multiplier=1.1 if sku_margin < request.min_margin_percent else 1.0,
                    )
                )

        if not recs:
            recs.append(
                AdaptationRecommendation(
                    action="continue_current_strategy_with_existing_limits",
                    confidence=0.7,
                    reason="Performance is within configured risk and margin limits.",
                )
            )
        return recs
