from fastapi.testclient import TestClient

from app.main import app


def test_semi_auto_workflow_generates_results_safely():
    api = TestClient(app)
    response = api.post('/automation/semi-auto/run', json={
        'keywords': 'pet bowl',
        'target_market': 'UK',
        'marketplace': 'shopify',
        'max_products': 2,
        'publish_drafts': True,
    })
    assert response.status_code == 200
    data = response.json()
    assert data['mode'] == 'semi_auto'
    assert data['summary']['products_checked'] >= 1
    assert data['results'][0]['action'] in {'generated_only_autonomy_disabled', 'rejected_by_risk_engine', 'draft_listing_created', 'listing_created'}


def test_dashboard_can_enable_semi_auto_controls():
    api = TestClient(app)
    response = api.put('/dashboard/controls', json={
        'enabled': True,
        'dry_run': True,
        'daily_budget_limit': 250,
        'max_orders_per_day': 10,
        'minimum_margin_percent': 25,
        'emergency_stop': False,
    })
    assert response.status_code == 200
    assert response.json()['enabled'] is True
