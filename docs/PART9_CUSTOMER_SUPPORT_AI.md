# Part 9 — Customer Support AI

Adds a deterministic customer-support module that is safe for autonomous commerce workflows.

## Capabilities

- Classifies customer messages into ecommerce intents.
- Detects escalation risks such as legal threats, fraud/chargeback language, high-value orders, negative sentiment, and unknown intent.
- Drafts bounded template-based replies.
- Allows auto-send only when confidence is high and escalation is false.
- Integrates with fulfillment and tracking schemas.

## API

- `POST /support/classify`
- `POST /support/reply`

## Safety Design

The module does not use uncontrolled free-form LLM output in V1. Replies are generated from validated templates. This prevents accidental promises, refunds, legal statements, or policy exceptions without review.
