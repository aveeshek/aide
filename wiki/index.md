---
id: knowledge.ftgo
kind: Index
title: FTGO Engineering Knowledge
status: approved
review_status: approved
owner: aide-ftgo-cohort
source_refs:
  - repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/docker-compose.yaml
    evidence_type: implemented
relations:
  - type: CONTAINS
    target: service.ftgo.gateway
  - type: CONTAINS
    target: service.ftgo.user
  - type: CONTAINS
    target: service.ftgo.restaurant
  - type: CONTAINS
    target: service.ftgo.location
  - type: CONTAINS
    target: service.ftgo.order
  - type: CONTAINS
    target: service.ftgo.feedback
last_verified_at: 2026-08-24
---

# FTGO Engineering Knowledge

Canonical engineering knowledge for the FTGO reference application.

This baseline contains deterministic runtime topology extracted from Docker Compose evidence at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

## Current knowledge scope

The current Graph Engineering baseline covers:

- application services
- PostgreSQL and MongoDB instances
- Redis components
- RabbitMQ
- explicit runtime dependencies derived from Compose configuration

API endpoints, message producers and consumers, schemas, database models, tests, and business flows will be added through subsequent deterministic extraction passes.

## Governance

The pages referenced by this index were generated as candidates from source evidence and promoted to canonical knowledge after review.

Canonical Markdown is authoritative. Neo4j is a rebuildable projection of this approved knowledge.