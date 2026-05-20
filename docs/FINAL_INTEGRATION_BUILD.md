# Part 12 — Final Integration Build

This package combines all finished modules into one FastAPI application.

## Included modules

1. Core System
2. Supplier Integration Module
3. Marketplace Integration Module
4. Product Hunter AI
5. Advanced Profit & Risk Engine
6. Auto Listing Generator
7. Order Fulfillment Agent
8. Shipping & Tracking Module
9. Customer Support AI
10. Self-Learning / Adaptation Engine
11. Admin Dashboard
12. Final Integration Build

## Safety defaults

- Dry-run mode is enabled by default.
- Real autonomous purchasing must not be enabled until live supplier, payment, marketplace, tax, and compliance integrations are reviewed.
- Emergency stop is available through dashboard controls.
- Risk limits are enforced by the governor modules.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

- API health: http://127.0.0.1:8000/health
- API docs: http://127.0.0.1:8000/docs
- Dashboard: http://127.0.0.1:8000/dashboard

## Test

```bash
python -m compileall app tests
pytest -q
python scripts/smoke_test.py
```

## Production next steps

Replace mock adapters with approved production API integrations:

- Supplier APIs
- Shopify Admin API
- Marketplace APIs
- Payment provider
- Shipping providers
- Tax/VAT engine
- Fraud/risk provider
- Monitoring and alerting

