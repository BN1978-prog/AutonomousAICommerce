# Autonomous AI Commerce System — Part 8: Shipping & Tracking Module

This build contains Parts 1–8 and keeps the project modular so later components can be connected without rewrites.

## Included modules

- Core product evaluation and AI Governor
- Supplier integration module
- Marketplace integration module
- Product Hunter AI
- Advanced Profit & Risk Engine
- Auto Listing Generator
- Order Fulfillment Agent
- Shipping & Tracking Module

## New in Part 8

- Unified shipping carrier interface
- Mock Royal Mail, Evri and DHL-style carriers
- Shipping rate quotes
- Shipment creation
- Deterministic tracking numbers
- Tracking event endpoint
- Shipping selector for reliable low-cost rates

## API endpoints added

- `GET /shipping/carriers`
- `POST /shipping/rates`
- `POST /shipping/shipments`
- `GET /shipping/{carrier}/track/{tracking_number}`

## Validation performed

- `python -m compileall app tests`
- `pytest -q`

Result: 33 tests passed.

## Safety note

All carrier integrations in this part are deterministic mocks. Real Royal Mail, Evri, DHL, ShipStation or EasyPost integrations should be added using official APIs and sandbox credentials before production use.

## Final integration build

This archive is the combined application containing Parts 1–12.

Validation performed before packaging:

- `python -m compileall app tests`
- `pytest -q`
- `python scripts/smoke_test.py`

The system uses mock/sandbox adapters by default. Production use requires replacing mock suppliers, mock marketplaces, shipping and payment integrations with approved live APIs and compliance checks.
