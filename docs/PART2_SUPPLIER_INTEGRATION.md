# Part 2 — Supplier Integration Module

This module adds a stable supplier interface that future real suppliers can implement without changing the rest of the commerce system.

## Included

- `SupplierClient` abstract contract
- normalized supplier product schemas
- mock global supplier for local development and tests
- supplier registry for multi-supplier search
- deterministic currency converter for MVP/testing
- supplier-to-core `SupplierOffer` normalizer
- `/suppliers/search` API endpoint

## Production replacement points

Replace `MockSupplierClient` with real API clients for approved suppliers. Avoid browser automation where an official API exists. Every supplier client should normalize price, stock, delivery, restrictions, and risk signals before the product reaches the decision engine.

## Compatibility

This module is compatible with Part 1 because it converts external supplier products into the existing `SupplierOffer` schema consumed by `AIGovernor`.
