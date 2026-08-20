---
id: step.place-order.authorize-payment
kind: FlowStep
type: FlowStep
title: Authorize payment
status: approved
review_status: approved
owner: team-payments
last_verified_at: 2026-07-22
source_refs:
  - repository: commerce-product-docs
    commit: 1122334455667788
    path: user-flows/place-order.md
    evidence_type: declared
relations:
  - type: PRECEDES
    target: step.place-order.confirm
  - type: IMPLEMENTS
    target: service.payment
---

# Authorize payment

Request an idempotent authorization from the Payment Service.
