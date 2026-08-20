---
id: step.place-order.confirm
kind: FlowStep
type: FlowStep
title: Confirm order
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
  - type: IMPLEMENTS
    target: service.order
---

# Confirm order

Persist the final state and return an order confirmation or rejection.
