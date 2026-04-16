# DBML Syntax

Reference: https://dbml.dbdiagram.io/docs/

DBML (Database Markup Language) is a concise syntax for database schema; dbdiagram.io renders it to interactive ER diagrams. It also generates SQL DDL via `dbdocs`.

## Basic table

```dbml
Table users {
  id uuid [pk]
  email varchar [unique, not null]
  name varchar [not null]
  created_at timestamp [default: `now()`]
  deleted_at timestamp [null]

  Note: 'Registered users'
}
```

## Column modifiers

- `[pk]` — primary key
- `[unique]` — unique constraint
- `[not null]` / `[null]`
- `[default: value]` or `[default: `expression`]`
- `[note: 'description']` — column comment
- `[increment]` — auto-increment
- `[ref: > other_table.column]` — inline foreign key

## Composite / complex keys

```dbml
Table order_items {
  order_id uuid
  product_id uuid
  quantity int [not null]

  Indexes {
    (order_id, product_id) [pk]
  }
}
```

## References (foreign keys)

Inline (one-to-many):
```dbml
Table orders {
  id uuid [pk]
  user_id uuid [ref: > users.id]
  total decimal
}
```

Standalone (more flexibility):
```dbml
Ref: orders.user_id > users.id
Ref: "order_items"."order_id" > "orders"."id" [delete: cascade, update: no action]
```

Cardinality markers:
- `>` many-to-one (child > parent)
- `<` one-to-many (parent < child)
- `-` one-to-one
- `<>` many-to-many (prefer an explicit join table)

## Indexes

```dbml
Table events {
  id uuid [pk]
  user_id uuid
  type varchar
  occurred_at timestamp

  Indexes {
    user_id
    (user_id, occurred_at) [name: 'idx_user_time']
    occurred_at [type: btree]
    type [type: hash]
  }
}
```

Types: `btree`, `hash`, `gin`, `gist`, `brin` (Postgres-specific).

## Enums

```dbml
Enum order_status {
  pending
  processing
  shipped
  cancelled
}

Table orders {
  id uuid [pk]
  status order_status [default: 'pending']
}
```

## Table groups (logical grouping for layout)

```dbml
TableGroup "user domain" {
  users
  user_profiles
  user_sessions
}

TableGroup "billing" {
  orders
  order_items
  invoices
}
```

## Notes and docs

```dbml
Project ecommerce {
  database_type: 'PostgreSQL'
  Note: 'E-commerce schema v2. See docs/erd.md.'
}

Table products {
  id uuid [pk]
  sku varchar [unique]
  Note: 'Canonical product catalog. Maintained by catalog team.'
}
```

## Style tips

- Snake_case table and column names (matches Postgres conventions)
- Primary keys: `id uuid [pk]` is a good default (use `bigint` if you really need sequential IDs)
- Always include `created_at` and `updated_at` on entity tables
- Prefer explicit join tables over `<>` for many-to-many (carries join-specific columns)
- Use `Note:` liberally — the diagram becomes documentation
- Group related tables with `TableGroup` for cleaner layout

## Common mistakes

- Forgetting `[not null]` — default is nullable; creates nullable-everywhere schemas
- Forgetting `[pk]` — dbdiagram renders without a visible key marker
- Referencing a non-existent column in `Ref:` — dbdiagram silently drops the ref
- Circular refs without join tables — unreadable diagrams; split with explicit associative entities

## Workflow

1. Write DBML in this plugin via `/system-and-database-design:diagram --format=dbml`
2. Paste into https://dbdiagram.io for interactive layout + sharing
3. Export to PostgreSQL/MySQL/SQL Server DDL if desired
4. Export to PNG/PDF for docs
