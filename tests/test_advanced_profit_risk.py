from fastapi.testclient import TestClient

from app.finance.advanced_profit_engine import AdvancedProfitEngine
from app.finance.schemas import CostAssumptions, FeeModel, AdvancedEvaluationRequest
from app.main import app
from app.risk.advanced_risk_engine import AdvancedRiskEngine
from app.services.advanced_governor import AdvancedAIGovernor
from app.core.config import Settings


def test_advanced_profit_engine_calculates_positive_margin():
    engine = AdvancedProfitEngine()
    profit = engine.calculate(
        sale_price=39.99,
        supplier_cost=10.00,
        supplier_shipping=3.00,
        fee_model=FeeModel(marketplace_fee_percent=10, payment_fee_percent=2.9),
        cost_assumptions=CostAssumptions(estimated_ad_cost=2.0, estimated_refund_rate=0.04),
    )
    assert profit.net_profit > 15
    assert profit.margin_percent > 35
    assert profit.break_even_price < profit.sale_price


def test_advanced_risk_engine_blocks_out_of_stock():
    engine = AdvancedRiskEngine()
    report = engine.evaluate(
        supplier_risk_score=0.1,
        return_risk_score=0.1,
        demand_score=0.8,
        competition_score=0.3,
        estimated_delivery_days=7,
        stock_available=0,
        margin_percent=40,
        roi_percent=100,
    )
    assert report.level in {"medium", "high"}
    assert "No supplier stock available" in report.blocking_reasons


def test_advanced_governor_approves_strong_candidate():
    governor = AdvancedAIGovernor(Settings(enable_autonomous_purchase=True, min_margin_percent=20))
    request = AdvancedEvaluationRequest(
        title="Pet grooming glove",
        expected_sale_price=34.99,
        supplier_cost=6.0,
        supplier_shipping=2.0,
        estimated_delivery_days=8,
        stock_available=200,
        supplier_risk_score=0.08,
        return_risk_score=0.06,
        demand_score=0.85,
        competition_score=0.25,
        fee_model=FeeModel(marketplace_fee_percent=10, payment_fee_percent=2.9),
        cost_assumptions=CostAssumptions(estimated_ad_cost=1.0, estimated_refund_rate=0.03),
    )
    decision = governor.evaluate(request)
    assert decision.status.value == "approved"
    assert decision.allowed_to_autonomously_buy is True


def test_advanced_governor_rejects_bad_margin():
    governor = AdvancedAIGovernor(Settings(min_margin_percent=25))
    request = AdvancedEvaluationRequest(
        title="Weak margin product",
        expected_sale_price=15.0,
        supplier_cost=10.0,
        supplier_shipping=3.0,
        estimated_delivery_days=10,
        stock_available=100,
        supplier_risk_score=0.1,
        return_risk_score=0.1,
        demand_score=0.7,
        competition_score=0.3,
    )
    decision = governor.evaluate(request)
    assert decision.status.value == "rejected"
    assert any("Margin" in reason or "negative" in reason for reason in decision.reasons)


def test_advanced_evaluate_endpoint():
    client = TestClient(app)
    payload = {
        "title": "Kitchen organiser",
        "expected_sale_price": 29.99,
        "supplier_cost": 7.0,
        "supplier_shipping": 2.0,
        "estimated_delivery_days": 9,
        "stock_available": 150,
        "supplier_risk_score": 0.1,
        "return_risk_score": 0.07,
        "demand_score": 0.8,
        "competition_score": 0.25,
    }
    response = client.post("/risk/advanced-evaluate", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["profit"]["net_profit"] > 0
    assert body["risk"]["total_score"] < 0.65


def test_profit_scenarios_endpoint_returns_three_scenarios():
    client = TestClient(app)
    payload = {
        "title": "Scenario item",
        "expected_sale_price": 39.99,
        "supplier_cost": 9.0,
        "supplier_shipping": 3.0,
        "estimated_delivery_days": 7,
        "stock_available": 300,
        "supplier_risk_score": 0.05,
    }
    response = client.post("/profit/scenarios", json=payload)
    assert response.status_code == 200
    assert [item["scenario"] for item in response.json()] == ["base", "downside", "upside"]
