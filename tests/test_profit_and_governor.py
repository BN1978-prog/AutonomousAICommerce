from app.core.config import Settings
from app.schemas.decision import DecisionStatus
from app.schemas.product import ProductCandidate, SupplierOffer
from app.services.governor import AIGovernor
from app.services.profit_engine import ProfitEngine


def make_product(price: float = 29.99, supplier_cost: float = 8.0, risk: float = 0.1) -> ProductCandidate:
    return ProductCandidate(
        title="Foldable pet travel bowl",
        category="pets",
        target_market="UK",
        expected_sale_price=price,
        estimated_ad_cost=2.0,
        estimated_refund_rate=0.04,
        return_risk_score=0.08,
        demand_score=0.75,
        competition_score=0.35,
        offers=[
            SupplierOffer(
                supplier_id="sup-1",
                supplier_name="Test Supplier",
                country="China",
                unit_cost=supplier_cost,
                shipping_cost=2.5,
                estimated_delivery_days=9,
                stock_available=500,
                supplier_risk_score=risk,
            )
        ],
    )


def test_profit_engine_calculates_positive_margin() -> None:
    product = make_product()
    profit = ProfitEngine.calculate(product, product.offers[0])
    assert profit.net_profit > 0
    assert profit.margin_percent > 25
    assert profit.roi_percent > 0


def test_governor_approves_good_product() -> None:
    settings = Settings(min_margin_percent=20, max_daily_spend=100, max_order_value=25)
    decision = AIGovernor(settings).evaluate(make_product())
    assert decision.status == DecisionStatus.APPROVED
    assert decision.selected_offer is not None


def test_governor_rejects_low_margin_product() -> None:
    settings = Settings(min_margin_percent=30, max_daily_spend=100, max_order_value=100)
    decision = AIGovernor(settings).evaluate(make_product(price=15.0, supplier_cost=10.0))
    assert decision.status == DecisionStatus.REJECTED
    assert any("Margin" in reason for reason in decision.reasons)


def test_governor_rejects_high_supplier_risk() -> None:
    settings = Settings(max_supplier_risk_score=0.2)
    decision = AIGovernor(settings).evaluate(make_product(risk=0.9))
    assert decision.status == DecisionStatus.REJECTED
    assert any("Supplier risk" in reason for reason in decision.reasons)
