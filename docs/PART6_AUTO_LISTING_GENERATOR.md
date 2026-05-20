# Part 6 — Auto Listing Generator

Adds a marketplace-aware listing generation module.

## Capabilities

- Generates marketplace-safe titles, descriptions, bullet points, SEO keywords and tags.
- Applies per-marketplace limits for mock Shopify, mock eBay and generic channels.
- Removes HTML and normalizes whitespace.
- Detects blocked terms and risky marketing/compliance claims.
- Exposes `POST /listings/generate`.

## Design notes

This module is deterministic by default so tests are stable. A future production AI provider can be added behind the same `AutoListingGenerator.generate()` contract without changing API clients.
