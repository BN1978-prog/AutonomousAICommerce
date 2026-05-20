# Part 3 — Marketplace Integration Module

This module adds a stable marketplace abstraction layer that can later be backed by official APIs.

## Included

- Common `MarketplaceClient` interface
- Pydantic schemas for listing drafts, listing results, price updates, and orders
- In-memory mock adapters for Shopify/eBay/mock development flows
- Listing builder that converts approved product candidates into marketplace listing drafts
- FastAPI endpoints for listing publication, price updates, and order retrieval
- Unit and API tests

## Endpoints

- `GET /marketplaces`
- `POST /marketplaces/{marketplace}/listings`
- `PATCH /marketplaces/{marketplace}/listings/price`
- `GET /marketplaces/{marketplace}/orders`

## Integration Notes

The adapters are intentionally implemented against a common contract. Production Shopify/eBay/Amazon adapters can replace the mock clients without changing downstream modules.
