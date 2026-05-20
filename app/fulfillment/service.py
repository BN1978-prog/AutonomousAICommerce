from __future__ import annotations

from app.core.config import Settings
from app.finance.schemas import AdvancedEvaluationRequest
from app.fulfillment.schemas import FulfillmentRequest, FulfillmentResult, FulfillmentStatus
from app.services.advanced_governor import AdvancedAIGovernor
from app.suppliers.schemas import SupplierOrderRequest
from app.suppliers.registry import SupplierRegistry


class FulfillmentService:
    """Executes the final supplier purchase only after deterministic risk approval.

    Real production adapters must use official supplier APIs and idempotency keys.
    This service is intentionally strict: by default it performs a dry-run unless
    ENABLE_AUTONOMOUS_PURCHASE=true and the request dry_run flag is false.
    """

    def __init__(self, settings: Settings, supplier_registry: SupplierRegistry) -> None:
        self.settings = settings
        self.supplier_registry = supplier_registry
        self.governor = AdvancedAIGovernor(settings)

    async def fulfill(self, request: FulfillmentRequest, current_daily_spend: float = 0.0) -> FulfillmentResult:
        audit: list[str] = ["fulfillment_request_received"]
        supplier = self.supplier_registry.clients.get(request.supplier_id)
        if supplier is None:
            return FulfillmentResult(
                status=FulfillmentStatus.FAILED,
                order_id=request.order_id,
                supplier_id=request.supplier_id,
                supplier_product_id=request.supplier_product_id,
                reasons=["Supplier is not registered"],
                audit_events=audit + ["supplier_not_found"],
            )

        product = await supplier.get_product(request.supplier_product_id)
        if product is None:
            return FulfillmentResult(
                status=FulfillmentStatus.FAILED,
                order_id=request.order_id,
                supplier_id=request.supplier_id,
                supplier_product_id=request.supplier_product_id,
                reasons=["Supplier product was not found"],
                audit_events=audit + ["supplier_product_not_found"],
            )

        supplier_cost = product.unit_cost.amount * request.quantity
        supplier_shipping = product.shipping_cost.amount
        eval_request = AdvancedEvaluationRequest(
            title=product.title,
            category=product.category,
            target_market=request.buyer_country,
            currency=request.currency,
            expected_sale_price=request.sale_price,
            supplier_cost=supplier_cost,
            supplier_shipping=supplier_shipping,
            estimated_delivery_days=product.estimated_delivery_days,
            stock_available=product.stock_available,
            supplier_risk_score=max(0.0, min(1.0, 1 - (product.supplier_rating / 5))),
            return_risk_score=product.return_rate_percent / 100,
            demand_score=request.demand_score,
            competition_score=request.competition_score,
            fee_model=request.fee_model,
            cost_assumptions=request.cost_assumptions,
        )
        decision = self.governor.evaluate(eval_request, current_daily_spend=current_daily_spend)
        audit.append(f"governor_status:{decision.status.value}")

        base_result = {
            "order_id": request.order_id,
            "supplier_id": request.supplier_id,
            "supplier_product_id": request.supplier_product_id,
            "net_profit": decision.profit.net_profit,
            "margin_percent": decision.profit.margin_percent,
            "reasons": decision.reasons,
        }

        if decision.status.value != "approved":
            return FulfillmentResult(status=FulfillmentStatus.BLOCKED, audit_events=audit + ["blocked_by_governor"], **base_result)

        if request.dry_run:
            return FulfillmentResult(status=FulfillmentStatus.APPROVED_DRY_RUN, audit_events=audit + ["dry_run_no_purchase"], **base_result)

        if not decision.allowed_to_autonomously_buy:
            return FulfillmentResult(
                status=FulfillmentStatus.BLOCKED,
                audit_events=audit + ["autonomous_purchase_disabled"],
                reasons=decision.reasons + ["Autonomous purchase is disabled in settings"],
                **{k: v for k, v in base_result.items() if k != "reasons"},
            )

        supplier_order = await supplier.create_order(
            SupplierOrderRequest(
                supplier_product_id=request.supplier_product_id,
                quantity=request.quantity,
                buyer_name=request.shipping_address.buyer_name,
                address_line1=request.shipping_address.address_line1,
                city=request.shipping_address.city,
                country=request.shipping_address.country,
                postal_code=request.shipping_address.postal_code,
            )
        )
        if not supplier_order.accepted:
            return FulfillmentResult(
                status=FulfillmentStatus.FAILED,
                supplier_order_id=supplier_order.supplier_order_id,
                tracking_number=supplier_order.tracking_number,
                audit_events=audit + ["supplier_order_rejected"],
                reasons=decision.reasons + [supplier_order.message],
                **{k: v for k, v in base_result.items() if k != "reasons"},
            )

        return FulfillmentResult(
            status=FulfillmentStatus.PURCHASED,
            supplier_order_id=supplier_order.supplier_order_id,
            tracking_number=supplier_order.tracking_number,
            audit_events=audit + ["supplier_order_created"],
            **base_result,
        )
