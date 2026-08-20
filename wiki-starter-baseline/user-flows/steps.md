---
id: step.place-order.validate
kind: FlowStep
type: FlowStep
title: Validate order request
status: approved
review_status: approved
owner: team-commerce
last_verified_at: 2026-07-22
source_refs:
  - repository: commerce-product-docs
    commit: 1122334455667788
    path: user-flows/place-order.md
    evidence_type: declared
relations:
  - type: PRECEDES
    target: step.place-order.authorize-payment
---

# Validate order request

Validate the customer, basket, request schema, and idempotency key.

---

> This starter file demonstrates one concept per file as the preferred production convention. Split the remaining step IDs into separate pages before using this sample as production data.
