# Mermaid C4 — Ordering System

A compact C4 context + container example rendered in Mermaid. Paste into any Mermaid-capable renderer.

## Context diagram

```mermaid
C4Context
  title Context diagram — Ordering System

  Person(customer, "Customer", "Places orders via web or mobile")
  Person(ops, "Operations", "Handles fulfillment + support")

  System(ordering, "Ordering System", "Accepts orders, manages inventory, handles payment")

  System_Ext(payments, "Stripe", "Payment processing")
  System_Ext(email, "SendGrid", "Transactional email")
  System_Ext(warehouse, "Warehouse WMS", "Fulfillment provider API")

  Rel(customer, ordering, "Browses, orders", "HTTPS")
  Rel(ops, ordering, "Manages orders", "HTTPS")
  Rel(ordering, payments, "Authorizes + captures", "HTTPS / JSON")
  Rel(ordering, email, "Sends receipts", "HTTPS")
  Rel(ordering, warehouse, "Dispatches fulfillment", "HTTPS / JSON")
```

## Container diagram

```mermaid
C4Container
  title Container diagram — Ordering System

  Person(customer, "Customer")

  System_Boundary(ordering, "Ordering System") {
    Container(web, "Web App", "Next.js", "Customer-facing SPA")
    Container(api, "API", "Node.js / Express", "Public REST API")
    Container(worker, "Order Worker", "Node.js", "Processes queued orders async")
    ContainerDb(db, "Primary DB", "PostgreSQL", "Orders, customers, inventory")
    ContainerDb(cache, "Cache", "Redis", "Sessions, product catalog cache")
    Container(queue, "Queue", "Kafka", "Order events + outbox")
  }

  System_Ext(payments, "Stripe")
  System_Ext(warehouse, "Warehouse WMS")

  Rel(customer, web, "Uses", "HTTPS")
  Rel(web, api, "Calls", "HTTPS / JSON")
  Rel(api, db, "Reads/writes", "SQL")
  Rel(api, cache, "Reads/writes", "RESP")
  Rel(api, queue, "Publishes order events", "Kafka protocol")
  Rel(api, payments, "Authorizes", "HTTPS")
  Rel(worker, queue, "Consumes", "Kafka protocol")
  Rel(worker, db, "Updates state", "SQL")
  Rel(worker, warehouse, "Dispatches", "HTTPS")
```

## Notes

- C4 support in Mermaid is newer — test rendering before relying on it in a presentation
- Keep **Context** to < 10 boxes; **Container** to < 15
- Always label edges with the protocol / synchrony — this is where most design mistakes hide
- For **Component** and **Code** levels, prefer a second diagram rather than cramming everything into one
