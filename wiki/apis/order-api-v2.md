---
id: api.order.v2
kind: API
type: API
title: Order API v2
status: approved
review_status: approved
owner: team-commerce
version: v2
last_verified_at: 2026-07-22
source_refs:
  - repository: order-service
    commit: 0123456789abcdef
    path: contracts/openapi/order-api-v2.yaml
    pointer: "#/paths/~1orders/post"
    evidence_type: contracted
relations:
  - type: DERIVED_FROM
    target: service.order
  - type: PARTICIPATES_IN
    target: flow.place-order
---

# Order API v2

## `POST /orders`

Creates an order request. The authoritative request and response fields are the OpenAPI document referenced in frontmatter; this page summarizes the intent and must not replace the contract.

## Design constraints

- Requests must include an idempotency key.
- Clients must handle asynchronous downstream payment outcomes.
- Breaking changes require a new major contract version.
