import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def assert_ok(response):
    assert response.status_code < 400, response.text


# Health
r = client.get('/health')
assert_ok(r)
assert r.json()['status'] == 'ok'

# Supplier search
r = client.post('/suppliers/search', json={
    'keywords': 'pet bowl',
    'target_market': 'UK',
    'max_results': 3,
    'max_delivery_days': 20
})
assert_ok(r)
assert isinstance(r.json(), list)

# Hunter opportunities
r = client.post('/hunter/opportunities', json={
    'keywords': 'pet bowl',
    'target_market': 'UK',
    'max_results': 3,
    'max_delivery_days': 20
})
assert_ok(r)

# Listing generation
r = client.post('/listings/generate', json={
    'product_title': 'Adjustable Pet Toy',
    'category': 'pet accessories',
    'marketplace': 'mock_shopify',
    'key_features': ['durable', 'lightweight', 'easy to clean'],
    'target_market': 'UK'
})
assert_ok(r)

# Dashboard status
r = client.get('/dashboard/status')
assert_ok(r)

print('Smoke test passed: core, suppliers, hunter, listings, dashboard')
