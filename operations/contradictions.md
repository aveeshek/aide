# Knowledge contradictions

No unresolved contradictions are recorded in the starter data.

Use this format when evidence conflicts:

```yaml
- id: contradiction.order.payment-api-version
  status: open
  subject: service.order
  claim_a:
    evidence_type: declared
    source: order-service/docs/hld/order-service.md
    statement: Order Service calls Payment API v1.
  claim_b:
    evidence_type: implemented
    source: order-service/src/payment_client.py
    statement: Order Service calls Payment API v2.
  owner: team-commerce
  opened_at: 2026-07-22
```
