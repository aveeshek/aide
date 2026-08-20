---
id: E2E-SPEC-SAMPLE
status: template
---
# Enterprise Requirements

## E2E-REQ-001
WHEN the initiating user submits a valid request, THE enterprise system SHALL complete the business flow across every participating service and expose an auditable final status.

## E2E-REQ-002
IF a downstream service rejects or times out, THEN THE enterprise system SHALL apply the approved retry or compensation policy without duplicating the business transaction.
