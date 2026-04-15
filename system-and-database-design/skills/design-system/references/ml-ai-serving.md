# ML / AI Serving

Authoritative sources: Chip Huyen "Designing Machine Learning Systems", Google Cloud ML production guides, OpenAI/Anthropic API docs, Pinecone/Weaviate/pgvector docs, LangChain production patterns.

## Serving topology

### Inline inference

Model runs inside the service that needs it.
- **Pro**: simple, low latency, one deploy
- **Con**: couples model lifecycle to service lifecycle; limits scale flexibility
- **Use when**: small models (< 1 GB), CPU-servable, low QPS

### Dedicated model service

Separate service wraps the model with an HTTP/gRPC API.
- **Pro**: independent scale, separate deploy cadence, one model → many clients, GPU pooling
- **Con**: extra hop; serialization cost
- **Use when**: GPU needed, multiple consumers, independent release cadence
- Products: KServe, Seldon, BentoML, Ray Serve, Triton, Vertex AI, SageMaker

### Managed LLM APIs

Anthropic, OpenAI, Google, etc. hosted endpoints.
- **Pro**: zero ops; SOTA models
- **Con**: external dep (latency, rate limits, outages); per-token cost; data residency
- **Use when**: you're not training your own; latency and cost fit

## Sync vs async

- **Sync (request/response)** — user-facing interactive inference (<1 s for small models, <10 s for LLMs with streaming tokens)
- **Async (job queue)** — batch embedding, long-running generation, image/video processing; return a job ID; poll or webhook on completion
- **Streaming** — LLM token-by-token; Server-Sent Events; critical for UX on long outputs

## Feature stores

Centralized store of model inputs (features) with:
- **Offline store** (warehouse/lakehouse) for training
- **Online store** (low-latency KV) for inference
- **Consistency** between training and serving (same transforms applied both paths)

Why: prevents training/serving skew (the #1 cause of silent model degradation).

Products: Feast, Tecton, Vertex AI Feature Store, Databricks Feature Store.

Use only when:
- You have 10+ models sharing features, OR
- You have sophisticated ML teams with training/serving skew incidents

For one or two models, a well-tested transform library is sufficient.

## Vector databases / embedding stores

Store dense vector representations; retrieve by similarity (cosine, Euclidean, dot product).

| Option | Style | Good for |
|---|---|---|
| **pgvector** (Postgres extension) | Embedded in your DB | Small-to-medium scale; consistency with existing Postgres data; up to ~10M vectors |
| **Qdrant, Weaviate, Milvus, Chroma** | Dedicated OSS | Millions to billions of vectors; filtering + vector search |
| **Pinecone, Turbopuffer** | Managed | Zero ops; pay per query |
| **Elasticsearch, OpenSearch** | Hybrid text+vector | When you need BM25 + vector rerank together |
| **DuckDB + VSS** | Local/analytical | Offline workloads, data-science notebooks |

Key decisions:
- **Index type**: HNSW (default), IVF, ScaNN — trade recall vs latency vs memory
- **Distance metric**: cosine for normalized embeddings, dot product for unnormalized, L2 for Euclidean spaces
- **Filtering**: pre-filter (filter then search) vs post-filter (search then filter) — pre-filter scales better with high-cardinality filters
- **Embedding dim**: 384 / 768 / 1024 / 1536 / 3072 — larger = better quality but more memory and slower

## RAG (Retrieval-Augmented Generation)

Pipeline: query → retrieve relevant chunks → stuff into LLM context → generate.

Quality pipeline:
1. **Chunking** — semantic boundaries beat fixed windows; 200-1000 tokens per chunk; 10-20% overlap
2. **Embedding** — use a model trained for retrieval (e.g., BAAI/bge-*, text-embedding-3-large, voyage)
3. **Retrieval** — top-k vector search (k=10-20), often with BM25 hybrid
4. **Reranking** — cross-encoder rerank of the top 20 → top 5; big quality win for cheap compute
5. **Prompt construction** — cite sources; include instructions; budget tokens for answer
6. **Generation** — LLM; stream output
7. **Evaluation** — RAGAS or similar; track groundedness, answer relevance, context relevance

Anti-patterns:
- Chunking by arbitrary token count (breaks semantic units)
- Retrieving top-3 without rerank (usually noisy)
- Stuffing too much into context (degrades performance AND costs more)

## Prompt caching (LLM APIs)

Anthropic, OpenAI, Gemini support caching of reusable prompt prefixes. Massive cost/latency wins for:
- System prompts that don't change per-request
- Static context (documents, schemas, code)

Use cache_control markers on static content; keep dynamic content at the end.

## LLM ops

- **Versioning** — every prompt template in version control; rollback is just a deploy
- **Evaluation** — golden dataset + automated scoring (LLM-as-judge + deterministic checks); run on every prompt change
- **Guardrails** — input validation, output schema enforcement (JSON mode, constrained generation), PII redaction, toxicity classifiers
- **Cost attribution** — tag every call with feature/user; detect runaway costs
- **Observability** — log prompt, model, tokens, latency, cost per request; tools: Langfuse, Helicone, Phoenix

## Model lifecycle

1. **Training** — offline; versioned datasets; reproducible runs (MLflow, W&B)
2. **Evaluation** — held-out test set; business metrics, not just accuracy
3. **Canary** — shadow or small-traffic rollout; monitor business KPIs
4. **Monitoring** — data drift, prediction drift, accuracy decay; set SLIs
5. **Retraining** — scheduled or triggered by drift

## Latency budget for AI features

| Interaction | Target |
|---|---|
| Embedding 1 query | < 50 ms |
| Vector search (10M vectors, HNSW) | < 100 ms |
| LLM first-token (Claude / GPT-4 class) | < 1 s |
| LLM streaming rate | > 30 tokens/sec (hides total duration from user) |

Every step matters; retrieve in parallel where possible; stream tokens always for >1 s generations.

## See also

- `data-engineering.md` — feature stores overlap; embeddings are derived data
- `observability.md` — ML-specific SLIs need regular metrics + drift monitors
- `../claude-api` skill (if available) — for detailed Claude API / SDK guidance
