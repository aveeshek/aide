---
id: flow.place-order
kind: UserFlow
type: UserFlow
title: Place Order
status: approved
review_status: approved
owner: product-commerce
last_verified_at: 2026-07-22
source_refs:
  - repository: commerce-product-docs
    commit: 1122334455667788
    path: user-flows/place-order.md
    evidence_type: declared
relations:
  - type: CONTAINS
    target: step.place-order.validate
  - type: CONTAINS
    target: step.place-order.authorize-payment
  - type: CONTAINS
    target: step.place-order.confirm
  - type: VALIDATED_BY
    target: test.place-order.e2e
---

# Place Order

## Goal

Allow an authenticated customer to submit a valid basket, authorize payment, and receive an order confirmation.

## Flow

1. Validate the request and idempotency key.
2. Create the pending order.
3. Authorize payment.
4. Confirm or reject the order.
5. Emit the lifecycle event and return the current state.
