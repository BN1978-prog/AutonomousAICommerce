from fastapi.testclient import TestClient

from app.adaptation.engine import SelfLearningEngine
from app.adaptation.schemas import AdaptationRequest, OutcomeType, ProductPerformanceEvent
from app.main import app


def event(sku: str, outcome: OutcomeType, sale_price: float = 30.0, supplier_id: str = "sup-a") -> ProductPerformanceEvent:
    return ProductPerformanceEvent(
        sku=sku,
        product_title="Test Product",
        supplier_id=supplier_id,
        marketplace="shopify",
        category="home",
        outcome=outcome,
        sale_price=sale_price,
        supplier_cost=10.0,
        shipping_cost=3.0,
        fees=2.0,
        refund_cost=8.0 if outcome in {OutcomeType.REFUND, OutcomeType.RETURN} else 0.0,
        delivery_days=12 if outcome == OutcomeType.LATE_DELIVERY else 5,
    )


def test_learning_engine_recommends_scaling_profitable_sku():
    request = AdaptationRequest(events=[event("sku-1", OutcomeType.SALE), event("sku-1", OutcomeType.SALE)])
    summary = SelfLearningEngine().analyze(request)

    assert summary.events_processed == 2
    assert summary.total_profit > 0
    assert any(r.sku == "sku-1" and r.action == "scale_budget_carefully" for r in summary.recommendations)


def test_learning_engine_detects_bad_refund_rate():
    request = AdaptationRequest(
        events=[
            event("sku-2", OutcomeType.SALE),
            event("sku-2", OutcomeType.REFUND, sale_price=0.0),
            event("sku-2", OutcomeType.RETURN, sale_price=0.0),
        ],
        max_refund_rate=0.2,
    )
    summary = SelfLearningEngine().analyze(request)

    assert summary.refund_rate > 0.2
    assert any(r.action in {"reduce_exposure_to_high_refund_categories", "pause_or_reprice_sku"} for r in summary.recommendations)


def test_supplier_scores_penalize_complaints_and_late_delivery():
    request = AdaptationRequest(
        events=[
            event("sku-good", OutcomeType.SALE, supplier_id="sup-good"),
            event("sku-good", OutcomeType.SALE, supplier_id="sup-good"),
            event("sku-bad", OutcomeType.COMPLAINT, sale_price=0.0, supplier_id="sup-bad"),
            event("sku-bad", OutcomeType.LATE_DELIVERY, sale_price=0.0, supplier_id="sup-bad"),
        ]
    )
    summary = SelfLearningEngine().analyze(request)
    scores = {score.entity_id: score.score for score in summary.supplier_scores}

    assert scores["sup-good"] > scores["sup-bad"]


def test_adaptation_api_endpoint():
    client = TestClient(app)
    payload = {
        "events": [
            {
                "sku": "sku-api",
                "product_title": "API Product",
                "supplier_id": "sup-api",
                "marketplace": "shopify",
                "category": "home",
                "target_market": "UK",
                "outcome": "sale",
                "sale_price": 40,
                "supplier_cost": 14,
                "shipping_cost": 4,
                "fees": 3,
                "refund_cost": 0,
                "delivery_days": 4,
            }
        ]
    }
    response = client.post("/adaptation/analyze", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["events_processed"] == 1
    assert "recommendations" in data
