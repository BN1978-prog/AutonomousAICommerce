# Part 4 — Product Hunter AI

This module adds the first autonomous opportunity-discovery layer.

## Capabilities

- Searches all registered supplier adapters.
- Estimates demand through deterministic, testable signals.
- Estimates competition using MVP-safe heuristics.
- Calculates recommended sale price.
- Converts supplier products into the shared `ProductCandidate` contract.
- Runs every candidate through the `AIGovernor` before returning it.
- Returns ranked opportunities only when they pass minimum scoring and risk checks.

## Endpoint

`POST /hunter/opportunities`

Example body:

```json
{
  "keywords": "pet grooming",
  "target_market": "UK",
  "currency": "GBP",
  "max_unit_cost": 20,
  "min_stock": 5,
  "max_delivery_days": 20,
  "min_opportunity_score": 0.45,
  "max_results": 5
}
```

## Production Upgrade Path

Replace the deterministic demand estimator with connectors for:

- marketplace sold listings,
- Google Trends,
- TikTok/Reddit trend signals,
- ad-platform conversion data,
- historical internal sales data.

The public contracts are stable, so later ML models can be added without changing the rest of the system.
