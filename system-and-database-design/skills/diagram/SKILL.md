---
name: diagram
description: Generates Mermaid, Excalidraw JSON, or DBML diagrams. Use when the user asks to "diagram X", "draw the architecture", "generate an ER diagram", "create a sequence diagram", or invokes /diagram. Accepts a free-text description with `--format` and `--save` flags.
argument-hint: "<description> [--format=mermaid|excalidraw|dbml] [--save=./path.ext]"
allowed-tools: Read, Write, Grep
---

# diagram

Convert a description into a syntactically valid diagram. Broken syntax is worse than no diagram.

## Process

1. **Parse args.** Flags: `--format=mermaid|excalidraw|dbml`, `--save=<path>`. Default `mermaid`. Infer from description when possible: ER / schema → DBML, whiteboard → Excalidraw, else Mermaid.
2. **Pick the diagram type** (Mermaid only): flowchart (`graph TD`), sequence, ER, state, class, C4.
3. **Load the format reference** and **one example** before writing:
   - Mermaid → `references/mermaid-cheatsheet.md` + `examples/mermaid-c4.md`
   - Excalidraw → `references/excalidraw-json-schema.md` + `examples/excalidraw-microservices.json`
   - DBML → `references/dbml-syntax.md` + `examples/dbml-ecommerce.dbml`
4. **Generate with rules:**
   - Label every edge (protocol + purpose)
   - Group related components (subgraphs / TableGroups)
   - ≤15 nodes per diagram; split larger designs into layered views
   - Top-to-bottom for request flows, left-to-right for pipelines
   - Dashed for async, solid for sync
   - DBML: include `Indexes {}` where they matter + `Note:` per table
5. **Validate before returning:**
   - Mermaid: unclosed nodes, missing direction, mismatched brackets
   - DBML: every `Ref:` references existing tables
   - Excalidraw: valid JSON; every binding `elementId` exists
6. **Output** in a fenced block with the correct language tag (```mermaid / ```json / ```dbml). Excalidraw: add "File → Open → paste." DBML: add "paste at https://dbdiagram.io."
7. If `--save=<path>` was given, write the file. Otherwise offer to save.
