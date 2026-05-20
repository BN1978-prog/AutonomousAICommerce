# Part 5 — Advanced Profit & Risk Engine

This module upgrades the decision layer from a simple margin/risk check to a repeatable commercial approval gate.

## Added modules

- `app/finance/advanced_profit_engine.py`
- `app/finance/schemas.py`
- `app/risk/advanced_risk_engine.py`
- `app/risk/schemas.py`
- `app/services/advanced_governor.py`

## Added API endpoints

- `POST /risk/advanced-evaluate`
- `POST /profit/scenarios`

## Safety design

The advanced governor is deterministic and does not call an LLM. It blocks autonomous buying if margin, supplier risk, return risk, stock, delivery, or daily spend limits fail.

Autonomous buying still requires `ENABLE_AUTONOMOUS_PURCHASE=true`; otherwise the system can approve a product but will not allow automatic purchase execution.
