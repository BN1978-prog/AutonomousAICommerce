from __future__ import annotations

from app.automation.schemas import SemiAutoProductResult, SemiAutoRunRequest, SemiAutoRunResult
from app.core.config import Settings
from app.dashboard.service import DashboardService
from app.finance.schemas import AdvancedEvaluationRequest, CostAssumptions, FeeModel
from app.listings.generator import AutoListingGenerator
from app.listings.schemas import ListingGenerationRequest
from app.marketplaces.registry import MarketplaceRegistry
from app.marketplaces.schemas import ListingDraft, MarketplaceName
from app.services.advanced_governor import AdvancedAIGovernor
from app.suppliers.registry import SupplierRegistry
from app.suppliers.schemas import SupplierSearchQuery


class SemiAutoCommerceService:
    """Safe semi-auto workflow.

    It can search supplier sandbox/live connectors, evaluate risk/profit, generate listings,
    and create marketplace drafts only when dashboard controls allow it. Real purchases are
    never made by this service.
    """

    def __init__(
        self,
        settings: Settings,
        dashboard_service: DashboardService,
        supplier_registry: SupplierRegistry,
        marketplace_registry: MarketplaceRegistry,
    ) -> None:
        self.settings = settings
        self.dashboard_service = dashboard_service
        self.supplier_registry = supplier_registry
        self.marketplace_registry = marketplace_registry
        self.governor = AdvancedAIGovernor(settings)
        self.generator = AutoListingGenerator()

    async def run(self, request: SemiAutoRunRequest) -> SemiAutoRunResult:
        controls = self.dashboard_service.get_status().autonomy
        query = SupplierSearchQuery(
            keywords=request.keywords,
            target_market=request.target_market,
            currency=self.settings.default_currency,
            max_delivery_days=30,
            min_stock=1,
        )
        products = (await self.supplier_registry.search_all(query))[: request.max_products]
        results: list[SemiAutoProductResult] = []
        listed = 0
        rejected = 0
        reviewed = 0

        for product in products:
            suggested_sale_price = round((product.unit_cost.amount + product.shipping_cost.amount) * 2.4, 2)
            eval_request = AdvancedEvaluationRequest(
                title=product.title,
                category=product.category,
                target_market=request.target_market,
                currency=product.unit_cost.currency,
                expected_sale_price=suggested_sale_price,
                supplier_cost=product.unit_cost.amount,
                supplier_shipping=product.shipping_cost.amount,
                estimated_delivery_days=product.estimated_delivery_days,
                stock_available=product.stock_available,
                supplier_risk_score=max(0.0, min(1.0, (5.0 - product.supplier_rating) / 5.0)),
                return_risk_score=max(0.0, min(1.0, product.return_rate_percent / 100.0)),
                demand_score=0.62,
                competition_score=0.45,
                fee_model=FeeModel(),
                cost_assumptions=CostAssumptions(),
            )
            decision = self.governor.evaluate(eval_request, current_daily_spend=request.current_daily_spend)
            action = "review"
            warnings: list[str] = []
            generated_listing = None
            listing_result = None

            if decision.status.value.lower() in {"rejected"}:
                rejected += 1
                action = "rejected_by_risk_engine"
            else:
                generated_listing = self.generator.generate(
                    ListingGenerationRequest(
                        product_title=product.title,
                        category=product.category,
                        target_market=request.target_market,
                        key_features=[
                            f"Ships from {product.country}",
                            f"Estimated delivery {product.estimated_delivery_days} days",
                            f"Supplier rating {product.supplier_rating}/5",
                        ],
                        tone="professional",
                    )
                )
                if not controls.enabled or controls.emergency_stop:
                    reviewed += 1
                    action = "generated_only_autonomy_disabled"
                    warnings.append("Autonomy is disabled or emergency stop is active; listing not published.")
                elif not request.publish_drafts:
                    reviewed += 1
                    action = "generated_only_publish_disabled"
                else:
                    draft = ListingDraft(
                        sku=product.supplier_product_id,
                        title=generated_listing.title,
                        description=generated_listing.description,
                        price=suggested_sale_price,
                        currency=product.unit_cost.currency,
                        quantity=min(product.stock_available, 25),
                        category=product.category,
                        tags=generated_listing.tags,
                        image_urls=[],
                        supplier_product_id=product.supplier_product_id,
                    )
                    marketplace = MarketplaceName(request.marketplace)
                    listing_result = await self.marketplace_registry.get(marketplace).publish_listing(draft)
                    listed += 1
                    action = "draft_listing_created" if controls.dry_run else "listing_created"
                    if controls.dry_run:
                        warnings.append("Dry-run is enabled; connector uses sandbox/mock behavior unless live API credentials are configured.")

            results.append(
                SemiAutoProductResult(
                    supplier_product=product,
                    decision=decision,
                    generated_listing=generated_listing,
                    listing_result=listing_result,
                    action=action,
                    warnings=warnings,
                )
            )

        return SemiAutoRunResult(
            mode="semi_auto",
            dry_run=controls.dry_run,
            autonomy_enabled=controls.enabled,
            results=results,
            summary={
                "products_checked": len(products),
                "listed": listed,
                "rejected": rejected,
                "needs_review": reviewed,
            },
        )
