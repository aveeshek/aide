---
id: test.place-order.e2e
kind: Test
type: Test
title: Place Order E2E test
status: approved
review_status: approved
owner: team-commerce
last_verified_at: 2026-07-22
source_refs:
  - repository: order-e2e-tests
    commit: aabbccddeeff0011
    path: tests/place_order_test.py
    symbol: test_place_order_happy_path
    evidence_type: implemented
relations:
  - type: VALIDATED_BY
    target: flow.place-order
---

# Place Order E2E test

Validates the happy path across Order Service and Payment Service using stable test data and an idempotency key.
