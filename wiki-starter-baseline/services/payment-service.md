---
id: service.payment
kind: Service
type: Service
title: Payment Service
status: approved
review_status: approved
owner: team-payments
domain: payments
valid_from: 2026-01-15
valid_to: null
last_verified_at: 2026-07-22
source_refs:
  - repository: payment-service
    commit: fedcba9876543210
    path: docs/hld/payment-service.md
    evidence_type: declared
relations:
  - type: PARTICIPATES_IN
    target: flow.place-order
---

# Payment Service

## Responsibility

Owns payment authorization, capture, refund, and payment-status reporting.

## E2E role

Receives payment requests from approved callers and returns an idempotent payment result.
