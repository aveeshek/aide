---
id: service.order
kind: Service
type: Service
title: Order Service
status: approved
review_status: approved
owner: team-commerce
domain: order-management
valid_from: 2026-01-15
valid_to: null
last_verified_at: 2026-07-22
source_refs:
  - repository: order-service
    commit: 0123456789abcdef
    path: docs/hld/order-service.md
    lines: "41-96"
    evidence_type: declared
  - repository: order-service
    commit: 0123456789abcdef
    path: src/main/java/com/example/order/OrderController.java
    symbol: com.example.order.OrderController
    evidence_type: implemented
relations:
  - type: EXPOSES
    target: api.order.v2
  - type: PARTICIPATES_IN
    target: flow.place-order
  - type: DEPENDS_ON
    target: service.payment
---

# Order Service

## Responsibility

Owns the order lifecycle from creation through fulfilment, cancellation, and closure.

## Interfaces

The service exposes [Order API v2](../apis/order-api-v2.md). It publishes order lifecycle events in the full implementation repository.

## E2E role

The service validates the order, persists the order record, requests payment authorization, and returns the current order state.

## Starter scope

The starter repository includes a minimal payment-service page so the sample dependency graph validates end to end. Replace all sample source references, owners, and contracts with project-specific evidence before production use.
