---
name: teach
description: This skill should be used when the user asks to "explain this violation", "teach me about clean code", "why is this bad", "what's wrong with long functions", "explain single responsibility", "what does DRY mean", "teach me about interfaces", "explain this principle", "why do we need interfaces", "what is OOP", or when the user wants to understand the reasoning behind a clean code rule. Provides a clear explanation with a book citation, counter-example, and how to fix it.
argument-hint: "[violation-type: file-too-long | function-too-long | too-many-parameters | deep-nesting | bad-naming | missing-interface | dry-violation | comments | human-readability]"
allowed-tools: Read
version: 0.1.0
---

# Clean Code Teach

Explain a clean code principle clearly — why it matters, what the rule is, where it comes from, and how to apply it. Always include a book citation, a counter-example showing the problem, and a clean version showing the solution.

## Structure of Every Teaching Response

Always follow this format:

```
## [Principle Name]

**The rule:** [One-sentence rule]

**Why it matters:**
[2-3 sentences on real impact — bugs, maintenance cost, onboarding time]

**Book reference:**
[Title, Chapter/Page] — [Short quote]

**The problem (before):**
[Code example showing the violation]

**The fix (after):**
[Code example showing the clean version]

**Remember:** [One memorable takeaway]
```

## Mapping Arguments to Principles

When `$ARGUMENTS` is provided, map to the corresponding principle:

| Argument | Principle |
|---|---|
| `file-too-long`, `monolith`, `long-file` | Single Responsibility — file level |
| `function-too-long`, `long-function` | Do One Thing |
| `too-many-parameters`, `parameters`, `params` | Parameter Objects |
| `deep-nesting`, `nesting` | Guard Clauses |
| `bad-naming`, `naming`, `names` | Intention-Revealing Names |
| `missing-interface`, `interface`, `interfaces` | Dependency Inversion |
| `dry-violation`, `dry`, `duplication` | DRY |
| `comments`, `commenting` | Self-Documenting Code |
| `human-readability`, `readability`, `readable` | Optimize for the Reader |
| `solid` | All SOLID principles overview |
| `oop` | OOP principles overview |
| `srp` | Single Responsibility Principle |
| `open-closed`, `ocp` | Open/Closed Principle |
| `liskov`, `lsp` | Liskov Substitution Principle |
| `interface-segregation`, `isp` | Interface Segregation Principle |
| `dependency-inversion`, `dip` | Dependency Inversion Principle |

## When No Argument Is Provided

If `$ARGUMENTS` is empty, ask the user which principle they want to learn about. Present the list:

```
Which clean code principle would you like to learn about?

1. **file-too-long** — Why monolith files are dangerous
2. **function-too-long** — Why functions must do one thing
3. **too-many-parameters** — Why parameter count matters
4. **deep-nesting** — How guard clauses simplify code
5. **bad-naming** — Why names are the most important documentation
6. **missing-interface** — Why TypeScript interfaces matter
7. **dry-violation** — The cost of duplicated logic
8. **comments** — When to comment and when not to
9. **human-readability** — The ultimate test for clean code
10. **solid** — All 5 SOLID principles

Or ask any question: "why do functions need to be short?"
```

## Context-Aware Teaching

When teaching, adapt the examples to the user's language:

- Detect the project language from recent files or conversation context
- Show TypeScript examples for TS projects, Python for Python, Java for Java
- If the user showed you a specific piece of code, use that as the "before" example

## Connecting Principles to the Books

Always cite from one of the three source books:

- **"The Art of Clean Code"** (Mayer) — focuses on practical day-to-day clean code habits
- **"Code Complete 2nd Ed."** (McConnell) — focuses on the craft and quantitative research
- **"OOP vs. Functional Programming"** — focuses on design patterns and paradigm choices

Use exact chapter references when available. See `references/principles.md` for all citations.

## Teaching SOLID (Overview)

When asked about SOLID as a whole:

```
## SOLID Principles

**S — Single Responsibility**
A class has one reason to change. If you need "and" to describe it, split it.

**O — Open/Closed**  
Open for extension, closed for modification. Add behavior through new classes, not by editing existing ones.

**L — Liskov Substitution**
Subtypes must be substitutable for their base types without breaking correctness.

**I — Interface Segregation**
Don't force clients to depend on methods they don't use. Keep interfaces small and focused.

**D — Dependency Inversion**
Depend on abstractions (interfaces), not concretions (classes). High-level modules don't import low-level ones.

Ask /cleancode:teach [s|o|l|i|d] for a deep dive into any principle.
```

## Additional Resources

### Reference Files

- **`references/principles.md`** — Full principle explanations with detailed book citations, counter-examples in multiple languages, and fix strategies for every violation type. Read this to get the full teaching content for any principle.
