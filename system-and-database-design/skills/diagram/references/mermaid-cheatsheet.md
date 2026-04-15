# Mermaid Cheat Sheet

Reference: https://mermaid.js.org/intro/

Mermaid renders in Markdown on GitHub, GitLab, Notion, Obsidian, Claude Code's own markdown, and more.

## Flowchart / graph

```mermaid
graph TD
  A[Client] -->|HTTPS| B(API Gateway)
  B --> C{Auth OK?}
  C -->|yes| D[Service]
  C -->|no| E[401]
  D --> F[(Postgres)]
  D -.->|async| G[[Queue]]
```

- Directions: `TD` top-down, `LR` left-right, `BT`, `RL`
- Shapes:
  - `A[Rectangle]`
  - `A(Rounded)`
  - `A([Stadium])`
  - `A[[Subroutine]]` (queues, repeated work)
  - `A[(Cylinder)]` (databases)
  - `A((Circle))` (endpoints)
  - `A{Diamond}` (decision)
  - `A>Flag]` (event)
- Arrows:
  - `-->` solid
  - `-.->` dashed (async)
  - `==>` thick (critical path)
  - `-->|label|` edge label
  - `-- label -->` alternative

### Subgraphs

```mermaid
graph LR
  subgraph "Edge"
    CDN --> LB
  end
  subgraph "App"
    LB --> API
    API --> DB[(Postgres)]
  end
```

## Sequence diagram

```mermaid
sequenceDiagram
  autonumber
  participant U as User
  participant A as API
  participant D as DB
  U->>A: POST /orders
  A->>D: INSERT
  D-->>A: ok
  A-->>U: 201
  Note over U,A: 2xx only after fsync
```

- `->>` request, `-->>` response
- `-x` error, `-->)` async
- `Note over`, `loop`, `alt`, `opt`, `par`

## ER diagram (relational schema)

```mermaid
erDiagram
  USER ||--o{ ORDER : places
  ORDER ||--|{ LINE_ITEM : contains
  USER {
    uuid id PK
    string email UK
    string name
  }
  ORDER {
    uuid id PK
    uuid user_id FK
    decimal total
    timestamp created_at
  }
```

Cardinality: `||--o{` one-to-many, `||--||` one-to-one, `}o--o{` many-to-many.

For richer ER (indexes, notes, refs) prefer DBML.

## State diagram

```mermaid
stateDiagram-v2
  [*] --> Pending
  Pending --> Processing: pay
  Processing --> Shipped: fulfill
  Processing --> Cancelled: cancel
  Shipped --> [*]
  Cancelled --> [*]
```

## Class diagram

```mermaid
classDiagram
  class Order {
    +UUID id
    +List~Item~ items
    +decimal total()
  }
  class Item
  Order "1" --> "*" Item
```

## C4 (context / container / component)

Mermaid 10+ supports C4 via `C4Context`. It's a newer feature; check rendering first.

```mermaid
C4Context
  Person(user, "User")
  System_Boundary(s, "Ordering System") {
    System(api, "API")
    SystemDb(db, "Postgres")
  }
  Rel(user, api, "uses", "HTTPS")
  Rel(api, db, "reads/writes", "SQL")
```

## Tips

- Use labels on EVERY edge. Unlabeled arrows hide the protocol and purpose.
- Use consistent shapes for consistent roles (always `[(...)]` for DBs, `[[...]]` for queues).
- Limit to ~15 nodes. Split larger diagrams into overview + detail.
- Use dashed edges for async, solid for sync.
- Group related components with `subgraph`.
- Avoid deep nesting (>2 levels); Mermaid renders awkwardly.

## Gotchas

- Mermaid is whitespace-sensitive in some contexts; spaces in labels may need quotes
- Node IDs can't contain spaces; use `A[Label with spaces]` instead
- HTML entities in labels: use `&lt;`, `&gt;`, `&amp;`
- Long labels wrap poorly; shorten or break into multiple nodes
