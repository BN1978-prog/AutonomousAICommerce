# Added features

This build adds the requested 4 features:

1. Improved GUI dashboard
   - live controls
   - metrics
   - supplier search
   - semi-auto workflow launcher
   - emergency stop button

2. Shopify connector
   - sandbox mode without credentials
   - optional live draft product creation through Shopify Admin API credentials
   - never publishes live products automatically in this build; it creates drafts first

3. Supplier sandbox
   - mock global supplier catalog
   - search endpoint
   - safe deterministic responses

4. Semi-auto workflow
   - searches suppliers
   - evaluates profit/risk
   - generates listing content
   - creates marketplace draft/sandbox listing when controls allow it

## New endpoint

POST /automation/semi-auto/run

## Safety

Dry-run is enabled by default. Emergency stop disables autonomous execution.
