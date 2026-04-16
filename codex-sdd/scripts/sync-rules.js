#!/usr/bin/env node

import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";

const packageRoot = path.resolve(import.meta.dirname, "..");
const repoRoot = path.resolve(packageRoot, "..");
const templatesDir = path.join(packageRoot, "templates");

const sourceCandidates = {
  skill: [
    path.join(repoRoot, "system-and-database-design/skills/design-principles/SKILL.md"),
    path.join(repoRoot, "sdd/skills/design-principles/SKILL.md"),
    path.join(repoRoot, "claude-code/skills/design-principles/SKILL.md"),
    path.join(repoRoot, "skills/design-principles/SKILL.md"),
  ],
  capPacelc: [
    path.join(repoRoot, "system-and-database-design/skills/design-principles/references/cap-pacelc.md"),
    path.join(repoRoot, "sdd/skills/design-principles/references/cap-pacelc.md"),
    path.join(repoRoot, "claude-code/skills/design-principles/references/cap-pacelc.md"),
    path.join(repoRoot, "skills/design-principles/references/cap-pacelc.md"),
  ],
  capDecision: [
    path.join(repoRoot, "system-and-database-design/skills/design-principles/references/cap-vs-pacelc-decision.md"),
    path.join(repoRoot, "sdd/skills/design-principles/references/cap-vs-pacelc-decision.md"),
    path.join(repoRoot, "claude-code/skills/design-principles/references/cap-vs-pacelc-decision.md"),
    path.join(repoRoot, "skills/design-principles/references/cap-vs-pacelc-decision.md"),
  ],
  consensus: [
    path.join(repoRoot, "system-and-database-design/skills/design-principles/references/consensus.md"),
    path.join(repoRoot, "sdd/skills/design-principles/references/consensus.md"),
    path.join(repoRoot, "claude-code/skills/design-principles/references/consensus.md"),
    path.join(repoRoot, "skills/design-principles/references/consensus.md"),
  ],
  consistency: [
    path.join(repoRoot, "system-and-database-design/skills/design-principles/references/consistency-models.md"),
    path.join(repoRoot, "sdd/skills/design-principles/references/consistency-models.md"),
    path.join(repoRoot, "claude-code/skills/design-principles/references/consistency-models.md"),
    path.join(repoRoot, "skills/design-principles/references/consistency-models.md"),
  ],
  dataStructures: [
    path.join(repoRoot, "system-and-database-design/skills/design-principles/references/data-structures-at-scale.md"),
    path.join(repoRoot, "sdd/skills/design-principles/references/data-structures-at-scale.md"),
    path.join(repoRoot, "claude-code/skills/design-principles/references/data-structures-at-scale.md"),
    path.join(repoRoot, "skills/design-principles/references/data-structures-at-scale.md"),
  ],
  tradeoffs: [
    path.join(repoRoot, "system-and-database-design/skills/design-principles/references/trade-off-catalog.md"),
    path.join(repoRoot, "sdd/skills/design-principles/references/trade-off-catalog.md"),
    path.join(repoRoot, "claude-code/skills/design-principles/references/trade-off-catalog.md"),
    path.join(repoRoot, "skills/design-principles/references/trade-off-catalog.md"),
  ],
};

async function readFirstExisting(paths) {
  for (const filePath of paths) {
    try {
      return {
        filePath,
        content: await readFile(filePath, "utf8"),
      };
    } catch (error) {
      if (error.code !== "ENOENT") {
        throw error;
      }
    }
  }

  throw new Error(`Could not find any source file:\n${paths.join("\n")}`);
}

function findSection(content, heading) {
  const headingPattern = new RegExp(`^## ${heading}$`);
  const lines = content.split(/\r?\n/);
  const startIndex = lines.findIndex((line) => headingPattern.test(line.trim()));

  if (startIndex === -1) {
    return "";
  }

  const sectionLines = [];
  for (const line of lines.slice(startIndex + 1)) {
    if (line.trim().startsWith("## ")) {
      break;
    }

    sectionLines.push(line);
  }

  return sectionLines.join("\n").trim();
}

function buildAgentsTemplate() {
  return `# System and Database Design Instructions

Source of truth: .sdd-principles.md
Package: sdd-codex

## Purpose

Use these instructions whenever the user asks for architecture, database design, distributed-systems trade-offs, reliability, scaling, consistency, consensus, idempotency, or design review. Be concrete, quantitative when possible, and explicit about trade-offs.

## Trigger Topics

Apply this guidance when the user mentions CAP, PACELC, linearizable, serializable, causal, eventual, read-your-writes, monotonic reads, Raft, Paxos, quorum, Byzantine, ACID, BASE, snapshot isolation, phantom read, write skew, lost update, idempotency, delivery guarantees, Bloom filters, HyperLogLog, Count-Min sketches, Merkle trees, vector clocks, Lamport clocks, or hybrid logical clocks.

## Answer Shape for Principles

When explaining a principle, answer in four parts:

1. Precise one-sentence definition.
2. Intuition with a minimal example, preferably a 3-node or single-request scenario.
3. Production failure the concept prevents or exposes.
4. Decision guidance with named systems or concrete design choices.

Always caveat distributed-systems claims. Prefer "under partition this design gives up X because Y" over universal statements.

## Core Design Rules

### CAP and PACELC

- CAP only matters during a network partition: choose consistency by rejecting or delaying, or choose availability by serving potentially divergent data.
- Do not describe systems as CA. Partitions are part of the model.
- PACELC is the everyday framing: if partitioned, choose consistency or availability; else choose latency or consistency.
- Classify each data store by partition behavior and normal-operation behavior, for example PC/EC, PC/EL, PA/EL.

### Consistency Models

- Pick the weakest consistency model the user-visible semantics tolerate.
- Linearizability is for locks, uniqueness, account debits, inventory decrement, and compare-and-swap.
- Session guarantees are enough for many user workflows: read-your-writes, monotonic reads, and writes-follow-reads.
- Eventual consistency only promises convergence when writes stop; it does not give a time bound.
- If ordering matters to users, consider causal consistency or consistent-prefix instead of raw eventual consistency.

### Consensus and Quorums

- Do not roll your own consensus. Use etcd, ZooKeeper, Consul, a database that already implements it, or a managed coordination service.
- Use consensus stores for coordination, not high-volume primary data.
- Prefer 3 or 5 nodes. Larger quorums usually add latency without much practical fault-tolerance benefit.
- For split-brain risk, leader election is not enough; require fencing tokens or another monotonic ownership proof.
- Quorum reads and writes need W + R > N for strong read-after-write behavior.

### Idempotency and Delivery

- Retries turn partial failures into duplicate side effects unless write operations are idempotent.
- External write APIs should accept idempotency keys when clients may retry.
- Internal async workflows need deduplication at every boundary that can redeliver.
- "Exactly once" usually means at-least-once delivery plus idempotent processing and transactional offset/state updates.
- Use outbox or saga patterns for cross-service workflows instead of pretending a distributed transaction is free.

### Probabilistic Sketches

- Bloom filter: "definitely absent or maybe present"; use for negative lookup avoidance and duplicate prechecks.
- HyperLogLog: approximate distinct counts with fixed memory; use for unique visitors or cardinality dashboards.
- Count-Min sketch: approximate frequencies; use for heavy hitters, rate-limit estimation, and stream analytics.
- Merkle tree: compare large replicated datasets by hashes; use for anti-entropy and content verification.
- State the approximation cost: false positives, no item identity, overestimation, or hash-tree maintenance.

## Workflow Mappings

Codex does not have Claude plugin slash commands. Treat the system-and-database-design commands, such as /system-and-database-design:design-system, as natural-language behaviors:

- When the user asks to design a system, produce a design doc with requirements, assumptions, capacity math, components, data layer, APIs, async behavior, resilience, observability, security, deployment, and rejected alternatives.
- When the user asks to design a database, start from workload and top queries. Default to Postgres unless the workload requires NoSQL. Cover schema, indexes, transactions, consistency, replication, sharding, schema evolution, and operations.
- When the user asks to review architecture, inspect only available evidence. Classify findings as pass, risk, violation, or unknown. Sort risks by severity and propose executable fitness functions.
- When the user asks for a diagram, default to Mermaid unless they request DBML or Excalidraw JSON. Keep diagrams small, label edges, group related components, and validate syntax before returning.

## System Design Skeleton

Use this shape for system design requests:

1. Requirements: functional, non-functional, constraints, assumptions.
2. Capacity estimates: QPS, storage, bandwidth, hot working set.
3. High-level architecture: components plus Mermaid sketch.
4. Data model: store choice, sharding key, replication, cache.
5. API: endpoints, RPCs, events, or sockets.
6. Async and real-time behavior.
7. Resilience and failure modes.
8. Observability: SLOs, SLIs, logs, metrics, traces.
9. Security: authn, authz, secrets, TLS, encryption.
10. Deployment and rollout.
11. Trade-offs and alternatives rejected.

## Database Design Skeleton

Use this shape for database requests:

1. Workload: read/write ratio, top queries, volume, transactional boundaries, consistency.
2. Store choice: engine and concrete justification.
3. Schema: tables or collections, constraints, keys, indexes.
4. Transactions and consistency: isolation per operation.
5. Scale strategy: replication, sharding, hotspots, cache.
6. Schema evolution: expand-contract, backfill, rollback.
7. Operations: backup, PITR, RPO/RTO, restore drills.
8. Trade-offs and alternatives considered.

## Review Stance

- Be direct and evidence-based.
- Do not invent findings that are not supported by files, docs, or pasted text.
- Treat missing information as unknown, not as a violation.
- Focus on issues that fail in production: scale, correctness, reliability, security, compliance, and operability.
- Put critical and high-severity findings first.

## Practical Default

Choose the simplest design that satisfies current and next-year non-functional requirements. Default to a modular monolith and Postgres until team boundaries, scale, workload shape, or availability requirements justify more distributed machinery.
`;
}

function buildPrinciplesTemplate(sources) {
  const capConcepts = findSection(sources.capPacelc.content, "Concepts \\(DDIA ch\\. 9 subset\\)");
  const pacelc = findSection(sources.capPacelc.content, "PACELC");
  const consistencyPicking = findSection(sources.consistency.content, "Picking a level");
  const consensusGuidance = findSection(sources.consensus.content, "Practical guidance");
  const dataStructures = [
    findSection(sources.dataStructures.content, "Bloom filter .+"),
    findSection(sources.dataStructures.content, "HyperLogLog .+"),
    findSection(sources.dataStructures.content, "Count-Min Sketch .+"),
    findSection(sources.dataStructures.content, "Merkle tree .+"),
  ].filter(Boolean).join("\n\n");
  const tradeoffs = findSection(sources.tradeoffs.content, "1\\. Consistency .+");

  return `# SDD Principles Reference

This reference is installed by sdd-codex so PRs and design docs can link to one compact distributed-systems guide.

## CAP and PACELC

${capConcepts}

${pacelc}

## Consistency Models

${findSection(sources.consistency.content, "Concepts")}

${consistencyPicking}

## Consensus

${findSection(sources.consensus.content, "Concepts")}

${consensusGuidance}

## Idempotency and Delivery

- Retries are required in real systems, so duplicate side effects are the normal failure mode to design against.
- Add idempotency keys to external write APIs where clients can retry after timeouts.
- Deduplicate internal messages at every boundary that can redeliver.
- Use outbox or saga patterns when one business action spans services.
- Treat "exactly once" claims as a composition of idempotent handlers, durable state, and offset or event tracking.

## Probabilistic Data Structures

${dataStructures}

## Trade-off Catalog

${tradeoffs}

## Example: Multi-region Checkout

Inventory decrement and payment authorization should be CP/EC or single-region strongly consistent because stale reads can oversell stock or charge incorrectly. Product catalog reads can be PA/EL because stale descriptions rarely violate correctness. Cart reads usually need session guarantees so users see their own writes. Cross-service checkout should use an idempotency key at the public API, an outbox event after the order transaction commits, and compensating actions for payment or fulfillment failure.
`;
}

const sources = {
  skill: await readFirstExisting(sourceCandidates.skill),
  capPacelc: await readFirstExisting(sourceCandidates.capPacelc),
  capDecision: await readFirstExisting(sourceCandidates.capDecision),
  consensus: await readFirstExisting(sourceCandidates.consensus),
  consistency: await readFirstExisting(sourceCandidates.consistency),
  dataStructures: await readFirstExisting(sourceCandidates.dataStructures),
  tradeoffs: await readFirstExisting(sourceCandidates.tradeoffs),
};

await mkdir(templatesDir, { recursive: true });
await writeFile(path.join(templatesDir, "AGENTS.md"), `${buildAgentsTemplate().trimEnd()}\n`);
await writeFile(path.join(templatesDir, ".sdd-principles.md"), `${buildPrinciplesTemplate(sources).trimEnd()}\n`);

console.log(`Synced design principles from ${path.relative(repoRoot, sources.skill.filePath)}`);
console.log(`Synced CAP/PACELC from ${path.relative(repoRoot, sources.capPacelc.filePath)}`);
console.log(`Synced consistency models from ${path.relative(repoRoot, sources.consistency.filePath)}`);
console.log(`Synced consensus from ${path.relative(repoRoot, sources.consensus.filePath)}`);
console.log(`Synced sketches from ${path.relative(repoRoot, sources.dataStructures.filePath)}`);
console.log(`Synced trade-offs from ${path.relative(repoRoot, sources.tradeoffs.filePath)}`);
