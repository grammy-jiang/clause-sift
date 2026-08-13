# Phase 3 Implementation Plan: Hybrid Retrieval

**Project:** ClauseSift  
**Phase:** 3 of the design-defined implementation sequence  
**Status:** Implementation plan  
**Primary design authority:** `docs/design.md`  
**Phase objective:** Extend the merged Phase 2 exact/lexical retrieval baseline with benchmarked chunk embeddings, deterministic memory-mapped exact dense retrieval, lexical+dense reciprocal-rank fusion, deterministic query classification, and expanded retrieval evaluation—without implementing Phase 4 cross-encoder reranking, Evidence Graph context traversal, or final context-complete evidence-tool behavior.

## 1. Purpose

Phase 3 adds the first semantic retrieval path to ClauseSift while preserving the design's accuracy-first, deterministic, source-grounded architecture.

Phase 2 already establishes the authoritative corpus identity, canonical document model, chunk/source identity, SQLite catalog, exact lookup, lexical retrieval, deterministic citations, immutable release lifecycle, release lineage, and the Phase 2 MCP/runtime baseline. Phase 3 must build on those contracts rather than introduce parallel identities, parallel metadata stores, or a second retrieval model.

The core Phase 3 question is not merely whether embeddings can retrieve semantically similar text. The phase must prove that semantic retrieval improves evidence recall on real engineering questions without degrading edition safety, exact-identifier behavior, deterministic release construction, source traceability, runtime safety, or the ability to reproduce a retrieval decision from immutable release artifacts.

Phase 3 therefore has five design-defined outcomes:

1. select an embedding model using ClauseSift's own multilingual engineering evaluation corpus;
2. generate exactly one release-bound embedding for every persisted chunk;
3. implement deterministic exact dense search over a memory-mapped chunk matrix;
4. fuse lexical and dense rankings using a versioned reciprocal-rank-fusion contract;
5. classify queries deterministically so the runtime can distinguish exact-style and natural-language retrieval needs and prepare the later `auto` mode contract.

The phase also expands regression evaluation so the selected embedding, dense-search, fusion, and query-analysis choices are supported by evidence rather than preference.

## 2. Phase boundary

Phase 3 must remain independently implementable and reviewable. Review comments, fixes, replies, and acceptance criteria for this phase must remain within the Phase 3 boundary.

### 2.1 In scope

Phase 3 implements and validates:

- an embedding-provider interface that does not leak a specific model into the canonical data model;
- candidate embedding-model benchmarking on the Phase 0/Phase 2 evaluation corpus;
- multilingual and cross-language embedding evaluation;
- deterministic `embedding_text` construction from Phase 2 chunks;
- exactly one embedding row per persisted chunk;
- a versioned chunk-vector row-order contract;
- deterministic embedding artifact generation;
- a safe release artifact format for the chunk matrix;
- matrix manifest metadata and release validation;
- NumPy memory-mapped exact dense search as the default small/medium-corpus implementation;
- an explicit abstraction boundary allowing later FAISS exact or validated ANN implementations without changing public evidence identity;
- runtime query embedding for the current query only;
- lazy query-model loading consistent with the common runtime lifecycle already established by the design;
- dense candidate generation and deterministic source/chunk mapping;
- metadata filtering before or during candidate acceptance without edition substitution;
- lexical+dense candidate deduplication;
- versioned reciprocal-rank fusion;
- deterministic tie-breaking and total candidate ordering;
- per-channel retrieval provenance needed for later Evidence Lineage assembly;
- deterministic query feature extraction;
- deterministic query classification for exact-style versus natural-language/hybrid retrieval needs;
- internal resolution of the best Phase 3-capable retrieval path;
- expanded retrieval regression evaluation;
- dense/hybrid quality gates and hard-negative coverage derived from the design's existing retrieval gates;
- cold/warm/model-free performance measurement for the embedding path;
- release/cache invalidation for embedding and vector artifacts;
- Phase 3 release assembly, validation, activation, and rollback integration;
- a clear handoff to Phase 4.

### 2.2 Out of scope

Phase 3 must **not** implement or pull forward:

- cross-encoder reranking;
- Phase 4 `high_accuracy` candidate reranking;
- deterministic Evidence Graph required/supporting/diagnostic context traversal from `docs/design.md` Section 19;
- conflict fixed-point closure at runtime if it is not already part of the merged lower-phase implementation;
- new semantic relationship extraction merely to improve dense search;
- LLM-based query classification;
- LLM-based query rewriting as an authoritative retrieval step;
- arbitrary generated query expansion that becomes source authority;
- approximate nearest-neighbour search solely because it is conventional;
- a permanently running vector database;
- document-level vectors;
- mixed document/chunk embedding matrices;
- multiple embeddings per chunk without a separately versioned future design;
- context-complete `search_evidence`, `get_clause`, `get_context`, clause-resource, or source-resource success behavior that requires Phase 4 context closure;
- final Phase 4 typed warning/refusal behavior;
- Phase 4 table/context improvements;
- Phase 4 cross-reference traversal improvements;
- autonomous engineering interpretation or answer generation.

If review feedback requires any item in this out-of-scope list, the response should identify the later owning phase and defer it rather than expanding this PR.

## 3. Governing design constraints

Phase 3 must preserve the following design decisions.

1. Accuracy remains the first priority; latency optimization cannot silently lower retrieval quality.
2. Original source bytes remain authoritative. Embeddings, vector scores, and fusion scores are non-authoritative retrieval metadata.
3. Every searchable semantic unit remains a Phase 2 chunk/source identity; Phase 3 does not create a parallel evidence entity.
4. ClauseSift v0.1 generates exactly one embedding for every persisted chunk.
5. Document-level embeddings are outside the v0.1 artifact and retrieval contract.
6. The chunk-vector row order is the total order `(document_id, chunks.canonical_order, chunk_id)` using canonical catalog ordering.
7. SQLite insertion order is never used as vector row identity.
8. Changing the embedding model or revision invalidates the affected embedding and downstream vector artifacts.
9. Only the current query is embedded at runtime.
10. Exact vector search is preferred before ANN for the initial local-corpus scale.
11. Approximate search is not introduced until measured latency justifies it and recall loss has been quantified.
12. The public retrieval abstraction must not depend on NumPy, FAISS, or a particular embedding vendor/model.
13. `original_text` is returned as evidence; `normalized_text`, `search_text`, and `embedding_text` remain derived search representations.
14. `embedding_text` never replaces source-faithful evidence text.
15. Explicit document/clause/model/numeric queries remain eligible for exact-mode behavior and must not be forced through embeddings.
16. Natural-language questions are the primary Phase 3 hybrid target.
17. `auto`, when eventually exposed through the final evidence API, may select only capabilities present in both the installed runtime and active release.
18. A dense-retrieval failure cannot silently impersonate a successful hybrid result in an explicit hybrid request.
19. Metadata filters, document identity, edition, jurisdiction, and other Phase 2 authority boundaries remain authoritative over semantic similarity.
20. Fusion combines candidate rankings; it cannot invent a source, document, clause, relationship, or applicability fact.
21. Dense and lexical channels retain independent retrieval provenance so later Evidence Lineage can explain why a source was selected.
22. All release artifacts are immutable, checksummed, validated before activation, and rolled back together.
23. Runtime model assets are safe-loaded under the existing release-integrity rules; pickle-backed arbitrary-code model assets remain prohibited.
24. Lazy model loading, cancellation, deadlines, worker supervision, quarantine, and resource-admission semantics reuse the common runtime contract rather than creating a second implementation.
25. Query classification is deterministic in Phase 3. A model may not decide whether exact evidence protections should be bypassed.
26. No retrieval score is interpreted as engineering confidence, legal authority, applicability, or normative force.
27. Evaluation results, not convenience, determine the selected embedding model, candidate sizes, RRF parameters, and any later performance optimization.

## 4. Prerequisites and Phase 2 handoff

Phase 3 starts only from the merged Phase 2 baseline on `master`.

The implementation must consume, not duplicate, the Phase 2 contracts for:

- approved manifests and document identity;
- canonical `document_id`, `node_id`, `chunk_id`, and `source_id`;
- chunk canonical order;
- `original_text`, `normalized_text`, `search_text`, and `embedding_text` fields or their canonical Phase 2 equivalents;
- classification provenance;
- page/source provenance;
- `knowledge.sqlite` read-only catalog;
- lexical index and lexical retrieval service;
- exact lookup service;
- deterministic source citations;
- release artifact manifest/checksum machinery;
- `build_content_id` and `release_id` identity rules;
- RFC 8785 release lineage;
- cache dependency declarations;
- atomic activation/rollback;
- runtime admission, cancellation, byte-budget, and quarantine behavior;
- Phase 0 evaluation corpus after the reviewed canonical-ID migration.

Before Phase 3 implementation begins, add a compatibility test that opens a valid Phase 2 release and proves that the Phase 3 builder can enumerate the exact canonical chunk sequence without altering the Phase 2 catalog.

## 5. Phase 3 deliverables

The phase should produce the following implementation deliverables.

### 5.1 Build-time deliverables

- embedding-provider interface and selected provider implementation;
- embedding benchmark harness;
- embedding benchmark report and selection record;
- deterministic embedding-text fixture suite;
- chunk embedding builder;
- canonical row-map generator/validator;
- `embeddings.f16.npy` release artifact or the exact filename already standardized by the merged lower-phase release contract;
- vector-artifact metadata in the release manifest;
- Phase 3 lineage entries for embedding/vector artifacts;
- cache keys for embeddings and vector artifacts;
- expanded retrieval evaluation reports;
- Phase 3 release-validation gates.

### 5.2 Runtime deliverables

- query embedder service;
- supervised lazy model-loader integration;
- exact dense-search backend;
- dense candidate mapper;
- lexical+dense deduplicator;
- reciprocal-rank-fusion implementation;
- deterministic query analyser/classifier;
- Phase 3 retrieval-path resolver;
- retrieval provenance records suitable for later Phase 4 Evidence Package assembly;
- performance diagnostics for model-free, cold, and warm hybrid queries.

### 5.3 Decision artifacts

The repository should retain human-readable, versioned records of:

- embedding candidates evaluated;
- exact model identifiers/revisions;
- model artifact hashes or external-provider request parameters if an external provider is ever admitted;
- benchmark corpus version;
- benchmark configuration;
- per-stratum results;
- selected embedding model and rationale;
- rejected candidates and reason;
- dense candidate-pool configuration;
- RRF configuration;
- query-classifier rule-set/configuration version;
- measured quality/latency trade-offs;
- the final Phase 3 gate result.

A benchmark report is evidence for configuration selection; it is not a replacement for immutable release metadata.

## 6. Proposed module boundaries

The exact filenames may change, but responsibilities must remain separated.

```text
src/clausesift/
├── builder/
│   ├── embeddings/
│   │   ├── interface.py
│   │   ├── text.py
│   │   ├── benchmark.py
│   │   ├── build.py
│   │   └── validate.py
│   └── vector/
│       ├── rowmap.py
│       └── validate.py
├── retrieval/
│   ├── dense.py
│   ├── fusion.py
│   ├── query_analysis.py
│   ├── classifier.py
│   └── candidates.py
├── runtime/
│   ├── model_loader.py
│   └── capabilities.py
└── evaluation/
    ├── embedding.py
    ├── retrieval.py
    └── query_classification.py
```

The important architecture rules are:

- the builder owns document-dependent embeddings;
- the runtime owns only current-query embedding;
- dense search consumes immutable release artifacts;
- fusion consumes typed candidate lists rather than backend-native objects;
- query classification consumes normalized request information and deterministic rules;
- evaluation calls public/internal stable interfaces rather than importing backend internals whenever possible.

## 7. Work package A: Freeze the Phase 3 contracts

Before adding a model dependency, write the Phase 3 schemas and interfaces.

### 7.1 Embedding provider interface

Define a narrow provider contract conceptually equivalent to:

```python
class EmbeddingProvider(Protocol):
    model_id: str
    revision: str
    dimensions: int

    def embed_documents(self, texts: Sequence[str]) -> NDArray: ...
    def embed_query(self, text: str) -> NDArray: ...
```

The real interface must additionally expose enough safe metadata for deterministic build identity, including:

- provider implementation ID/version;
- model identifier;
- exact revision;
- vector dimension;
- output dtype before canonical conversion;
- normalization behavior;
- maximum admitted input size;
- tokenizer/model asset identity where applicable;
- configuration hash.

Do not expose model-native objects outside the provider implementation.

### 7.2 Dense candidate contract

A dense hit must resolve to an existing Phase 2 chunk/source and carry only retrieval metadata, for example the logical fields:

- `source_id`;
- `chunk_id`;
- `document_id`;
- channel = `dense`;
- dense rank;
- raw similarity score;
- vector-row index for internal diagnostics only where safe;
- release/vector-artifact identity;
- optional normalized query-analysis metadata.

The vector row index is not a public evidence identifier.

### 7.3 Fusion candidate contract

Fusion should consume per-channel ranked candidate lists and emit a stable candidate object containing:

- source/chunk/document identities;
- every contributing retrieval channel;
- per-channel rank;
- per-channel score where meaningful;
- deterministic fused score;
- deterministic fused rank;
- the RRF configuration identity;
- the resolved Phase 3 retrieval path;
- no generated summary or source mutation.

### 7.4 Query-analysis contract

The deterministic analyser must return a typed object rather than a loose dictionary.

It must represent the design-defined features:

- document codes;
- clause numbers;
- editions;
- product model numbers;
- numbers and units;
- document types;
- jurisdiction filters;
- discipline filters;
- version-comparison intent;
- source-page request intent;
- whether the residual query is natural-language dominant.

Each detected feature must retain enough source-span or normalized-value information to make classification testable.

## 8. Work package B: Embedding-text determinism

Phase 3 must not embed arbitrary presentation strings assembled differently by different code paths.

### 8.1 Canonical `embedding_text`

For each Phase 2 chunk, define one deterministic `embedding_text` projection.

It should use only approved deterministic inputs already present in the canonical chunk/document model, such as:

- normalized chunk text;
- document code when useful;
- clause/hierarchy context when useful;
- deterministic headings;
- deterministic table headers/units already preserved by the chunker;
- deterministic document metadata intentionally admitted by the design.

It must not include:

- mutable filesystem paths;
- release timestamps;
- random IDs;
- query-dependent text;
- generated summaries unless the design later explicitly admits a generated retrieval field;
- reviewer comments;
- model-generated legal interpretations;
- data from another edition merely because it is similar.

### 8.2 Projection identity

Define a versioned `embedding_text_schema_version` and configuration hash.

The embedding cache key must include the ordered tuple specified by the design:

```text
(document_id, canonical_order, chunk_id, embedding_text_hash)
```

plus:

- `embedding_scope: "chunk"`;
- row-order version;
- model identifier/revision;
- provider/configuration identity;
- dependency-lock hash;
- build-toolchain fingerprint where required by the existing release contract.

### 8.3 Determinism tests

Tests must prove:

- identical chunk inputs produce byte-identical `embedding_text`;
- hierarchy metadata order is deterministic;
- Unicode normalization is deterministic;
- table headers/units do not change order across rebuilds;
- a changed chunk text changes `embedding_text_hash`;
- an unrelated document change does not invalidate another chunk's embedding cache entry;
- a changed model/configuration invalidates embeddings even when `embedding_text` is unchanged;
- two editions with identical wording remain distinct chunk identities and row positions.

## 9. Work package C: Embedding-model benchmark

No embedding model is selected by reputation alone.

### 9.1 Candidate shortlist

Create a small replaceable candidate set that can realistically run in the supported local environment and packaging model.

The shortlist should include models that plausibly cover:

- English technical text;
- Chinese technical text;
- cross-language English↔Chinese retrieval;
- engineering terminology;
- short clause-like text;
- longer contextual chunks.

The benchmark harness, not this plan, decides the winner.

### 9.2 Required benchmark strata

The benchmark must include the design-defined categories:

- English standards;
- Chinese standards;
- cross-language queries;
- HVAC terminology;
- fire-safety terminology;
- identifiers and product model numbers;
- numbers and units;
- synonyms;
- negation;
- exception queries.

Add explicit strata for:

- near-duplicate clauses in different editions;
- similar wording with different normative modality;
- same numeric value with different units;
- different numeric values with similar surrounding wording;
- clause-number-only queries that should remain exact-mode dominant;
- manufacturer versus standard terminology;
- hard negatives with strong semantic similarity but wrong document/edition;
- queries where lexical retrieval is already perfect;
- queries where dense retrieval is expected to add recall.

### 9.3 Benchmark protocol

For each candidate model:

1. freeze model ID/revision and provider configuration;
2. build embeddings from the same immutable benchmark chunk set;
3. verify deterministic row mapping;
4. run exact dense search only;
5. measure Recall@K over several K values including 5 and 20;
6. record MRR/NDCG or another ranking diagnostic only as secondary evidence, not a replacement for the design's release gates;
7. report performance by stratum, not only globally;
8. measure build throughput;
9. measure artifact size;
10. measure cold model-load time;
11. measure warm query-embedding latency;
12. measure exact dense-search latency separately from embedding latency;
13. measure peak resident memory;
14. measure packaging/model-asset complexity;
15. retain all candidate results, including failed/rejected models.

### 9.4 Selection criteria

The selected model must be the best evidence-backed trade-off under the project's priority order:

1. retrieval correctness;
2. cross-language and hard-negative robustness;
3. reproducibility/safe loading;
4. runtime feasibility;
5. build/runtime speed;
6. packaging simplicity.

A faster model does not win if it lowers the applicable retrieval confidence bound.

## 10. Work package D: Offline embedding builder

### 10.1 Row enumeration

Read the complete Phase 2 chunk set in the exact total order:

```text
(document_id, chunks.canonical_order, chunk_id)
```

Require:

- dense per-document `canonical_order` as already validated by Phase 2;
- one source per chunk as already required by the catalog;
- no duplicate chunk ID;
- no missing chunk;
- no foreign/cross-document row;
- no dependence on SQLite physical row order.

### 10.2 Exactly one vector per chunk

For v0.1:

- row count must equal chunk count exactly;
- every chunk has one and only one vector row;
- no document vectors are inserted;
- no sentinel row is inserted;
- no padding row is inserted;
- no duplicate embedding row is admitted;
- a zero-length corpus may be rejected by the surrounding release rules rather than represented with ambiguous vector semantics.

### 10.3 Canonical dtype and normalization

The release artifact follows the design's safe numeric matrix contract:

- one numeric rank-two `.npy` matrix;
- chunk-only scope;
- `float16` release representation unless the merged design/release schema specifies a stricter current value;
- no object dtype;
- no structured dtype;
- no pickle;
- no `.npz` fallback;
- normalized vectors when cosine-equivalent dot-product search is selected;
- finite values only;
- no NaN/Inf;
- declared dimensions exactly equal every row's width.

If provider output is higher precision, canonical conversion happens once under a versioned rule and is covered by evaluation.

### 10.4 Artifact metadata

The release manifest records at minimum:

- artifact path;
- SHA-256;
- byte size;
- `embedding_scope: "chunk"`;
- `row_count`;
- `vector_dimensions`;
- `dtype`;
- `normalized`;
- row-order schema/version;
- embedding model ID;
- embedding model revision;
- provider/configuration hash;
- embedding-text schema/version;
- embedding artifact schema/version.

### 10.5 Atomic builder behavior

Write the matrix to a candidate-release temporary location, validate it completely, then seal it into the candidate release. A failed or interrupted build must not modify the currently active release.

## 11. Work package E: Embedding artifact validation

The independent release gate must validate the artifact without trusting builder in-memory state.

Required checks include:

- checksum and byte size;
- safe `.npy` loading with `allow_pickle=False`;
- rank exactly two;
- dtype exactly admitted type;
- finite values;
- normalization invariant within declared numerical tolerance;
- dimensions match manifest;
- row count equals catalog chunk count;
- reconstructed row map is total and one-to-one;
- row ordering exactly matches `(document_id, canonical_order, chunk_id)`;
- embedding scope is exactly `chunk`;
- row-order version supported;
- model/configuration identity supported;
- expected file size consistent with shape/dtype/header contract;
- matrix is read-only at runtime;
- no unexpected sidecar file is required by the loader;
- lineage identifies the embedding transformation and artifact hash.

Corruption, row mismatch, unsupported dtype, or unknown schema blocks activation.

## 12. Work package F: Memory-mapped exact dense search

### 12.1 Default backend

Implement the initial exact backend using a NumPy memory map for small and medium corpora.

The runtime opens the validated matrix read-only and performs exact score computation conceptually equivalent to:

```python
scores = embeddings @ query_vector
```

when vectors are normalized and dot product is the admitted metric.

### 12.2 Backend abstraction

The dense-search service must not expose NumPy arrays through its public service contract.

Use a backend interface such as:

```python
class DenseIndex(Protocol):
    def search(self, query_vector, *, limit, filters) -> list[DenseHit]: ...
```

A future FAISS exact implementation can satisfy the same contract.

ANN remains out of scope unless a separately measured future change proves exact search cannot meet target latency.

### 12.3 Query-vector validation

Before scoring:

- query vector dimensions must equal release dimensions;
- values must be finite;
- vector must satisfy the selected normalization contract;
- model identity used for the query must match the release embedding model/revision/configuration;
- a query vector from another release/model cannot be reused accidentally;
- zero-norm vectors fail visibly rather than producing arbitrary ranking.

### 12.4 Exact top-K selection

Dense top-K selection must be deterministic.

Tie-breaking should use a total order independent of NumPy implementation details, ultimately reducing to canonical release identity such as:

```text
(score descending,
 document_id,
 chunk canonical_order,
 chunk_id,
 source_id)
```

The precise tie rule must be frozen and versioned.

### 12.5 Metadata filtering

Dense similarity never overrides metadata authority.

Candidate filtering must preserve:

- exact selected release;
- document/edition filters;
- lifecycle/status filters;
- jurisdiction/discipline filters;
- document-type filters;
- any other Phase 2 filter semantics already defined.

Filtering may be implemented before scoring where efficient or after score computation where simpler, but result semantics must be identical and tested.

No filter may substitute a newer edition, guessed jurisdiction, or semantically similar document.

## 13. Work package G: Runtime query embedding

Only the current request query is embedded at runtime.

### 13.1 Model loading

Reuse the common runtime lazy-model loader and supervised worker contract from the design and merged Phase 2 runtime plan.

Do not create an embedding-specific timeout subsystem.

The query embedding model must:

- load from checksum-verified allowlisted assets;
- use the exact model ID/revision/configuration named by the active release;
- use safe model formats/loaders admitted by the release contract;
- expose a handle only after the supervised load transitions successfully to ready;
- participate in single-flight loading;
- obey per-attempt model-load deadline;
- obey per-caller overall deadline;
- be cancelled/reaped under existing terminal-state rules;
- trigger release quarantine if a lazy asset integrity check fails.

### 13.2 Query preprocessing

Define one deterministic query-embedding preprocessing path.

It may trim/normalize request whitespace according to the already approved input contract, but it must not:

- silently remove a negation;
- drop numbers/units;
- replace document codes with generated synonyms;
- rewrite the query with an LLM;
- add hidden answer text;
- use a different preprocessing path for evaluation and production.

### 13.3 Query embedding cache

A small in-process cache may be evaluated only if needed. If used, its key must bind:

- exact normalized query bytes;
- model ID/revision;
- embedding preprocessing schema/configuration;
- active release/model compatibility identity where needed.

Cache contents are performance data, not release authority, and may be discarded at any time.

## 14. Work package H: Dense candidate generation

For a hybrid query:

1. validate request and filters;
2. obtain/validate current-query embedding;
3. perform exact dense search against the active release matrix;
4. map row indices through the deterministic row map;
5. map chunks to their unique Phase 2 source rows;
6. apply canonical metadata filters;
7. create typed `dense` candidates;
8. sort deterministically;
9. retain the configured dense candidate pool for fusion.

A row that cannot map one-to-one to the catalog is a release-integrity failure, not a skippable hit.

Dense candidate objects must not copy/modify source text merely to support fusion.

## 15. Work package I: Reciprocal-rank fusion

### 15.1 Phase 3 fusion scope

Phase 3 hybrid mode fuses:

- lexical retrieval;
- dense retrieval.

Do not pull Phase 4 cross-encoder reranking into this stage.

Exact identifier lookup remains available through exact-mode routing. The later high-accuracy pipeline may include exact candidates in a broader fusion stage according to Phase 4.

### 15.2 Deduplication identity

Deduplicate candidates by the canonical evidence identity defined by the Phase 2 service layer—normally the unique source/chunk mapping—not by normalized text equality.

Two different editions with identical text remain two different candidates.

Two chunks with similar text remain distinct unless the Phase 2 identity contract says they are the same source.

### 15.3 RRF formula

Use a versioned RRF configuration rather than hard-coding an undocumented magic number.

The logical contribution of channel `c` for candidate `x` is:

```text
1 / (rrf_k + rank_c(x))
```

where ranks are one-based and `rrf_k` is selected through benchmark/evaluation evidence.

The fused score is the deterministic sum of contributions from channels in which the candidate appears.

### 15.4 Configuration search

Benchmark a bounded set of candidate values for:

- lexical candidate pool size;
- dense candidate pool size;
- `rrf_k`;
- final fused candidate pool size;
- any channel weighting only if the design permits it and evidence shows plain RRF is insufficient.

The starting high-accuracy design guidance of lexical/dense top 30-50 is a hypothesis, not a fixed Phase 3 constant. Select the Phase 3 values using Recall@K and hard-negative evidence.

### 15.5 Deterministic ordering

The final fused ordering must have a complete tie-break chain, for example:

```text
(fused score descending,
 best contributing rank ascending,
 channel-presence rank,
 document_id,
 chunk canonical_order,
 chunk_id,
 source_id)
```

The exact tuple must be frozen by tests and versioned.

Floating-point ties must not depend on hash-map iteration or backend return order.

### 15.6 Fusion provenance

For every fused candidate retain:

- lexical rank/score when present;
- dense rank/score when present;
- RRF contribution by channel;
- fused score;
- fused rank;
- RRF configuration identity;
- lexical-index artifact hash;
- embedding/vector artifact hash;
- query-classifier/resolved-path identity.

This is retrieval provenance. It does not alter source provenance.

## 16. Work package J: Deterministic query analysis

Phase 3 implements the design's deterministic query analysis before mode/path selection.

### 16.1 Feature families

Detect with versioned deterministic rules:

- document codes;
- clause numbers;
- editions;
- product model numbers;
- numbers and units;
- document types;
- jurisdiction terms;
- discipline terms;
- version-comparison intent;
- source-page request intent.

Also compute conservative structural indicators such as:

- query token/scalar length;
- proportion of tokens consumed by recognized identifiers;
- whether meaningful natural-language residual text remains;
- whether the query contains interrogative/question structure;
- whether several documents/concepts appear to be requested;
- whether an exact target is fully specified.

### 16.2 Rule authority

Rules are routing heuristics only.

They may decide which retrieval channels to invoke, but they cannot decide:

- which edition is legally controlling;
- whether a source is applicable;
- whether a clause is normative;
- whether a conflict is resolved;
- whether required context may be omitted;
- whether a dense match is factually correct.

### 16.3 Feature provenance

For each recognized feature retain:

- feature type;
- normalized value;
- source character/byte span where practical;
- rule ID/version;
- confidence as deterministic state (`matched`/`ambiguous`/`not_matched`) rather than an opaque model probability;
- any ambiguity reason.

## 17. Work package K: Query classification and Phase 3 path resolution

### 17.1 Required classifier outcomes

The Phase 3 classifier should distinguish at least:

- **exact-dominant** — explicit document/clause/model/numeric target where exact+lexical retrieval should remain primary;
- **hybrid-natural-language** — natural-language question where lexical+dense fusion is appropriate;
- **ambiguous** — query contains both exact anchors and substantive natural-language intent and requires a conservative documented rule;
- **later-phase-high-accuracy-intent** — query characteristics suggest later applicability-sensitive/cross-document high-accuracy handling, but Phase 3 must not implement Phase 4 behavior.

The public design mode enum remains `auto`, `exact`, `hybrid`, `high_accuracy`; this internal classification vocabulary need not become a public enum.

### 17.2 Conservative routing

Recommended Phase 3 behavior:

- exact-dominant → use existing exact-mode retrieval path;
- hybrid-natural-language → use lexical+dense fusion;
- ambiguous → prefer the path proven by evaluation, with exact anchors preserved as constraints/features rather than discarded;
- later-phase-high-accuracy-intent → record that the classifier identified the intent, but do not implement Phase 4 reranking/context behavior.

Because final ordinary evidence-returning tools require the Section 19 context contract, Phase 3 should expose these routing results through the internal retrieval service/evaluation/diagnostic layer rather than falsely advertise context-complete final MCP evidence responses.

### 17.3 Explicit override preparation

The service layer should accept a typed requested mode/path so Phase 4 can wire the final public override contract without replacing Phase 3 internals.

An explicit Phase 3 hybrid request must fail visibly if the active release or installed runtime lacks dense capability; it must not silently return lexical-only results labelled hybrid.

## 18. Work package L: Regression-evaluation expansion

Phase 3 expands the evaluation corpus and evaluator implementation around semantic retrieval.

### 18.1 Retrieval slices

Evaluate at least:

- lexical alone;
- dense alone;
- hybrid fusion;
- existing exact mode;
- classifier-selected Phase 3 path;
- explicit hybrid path;
- hard-negative subsets;
- multilingual subsets;
- cross-language subsets;
- identifier/numeric subsets;
- negation/exception subsets;
- same-wording/different-edition subsets.

### 18.2 Required primary gates

Use the design's retrieval quality gates on independently labelled applicable cases:

- expected evidence present in Recall@20: one-sided 95% Wilson lower bound >= 98%;
- expected evidence present in Top-5: one-sided 95% Wilson lower bound >= 95%.

For each 98% probabilistic gate require at least 150 applicable cases; for each 95% gate require at least 60 applicable cases, with larger stratified samples when critical query families or hard negatives would otherwise be underrepresented.

Always report:

- numerator;
- denominator;
- point estimate;
- one-sided Wilson lower bound;
- corpus/split identity;
- model/configuration identity.

### 18.3 Comparative gates

In addition to absolute gates, Phase 3 should reject a hybrid configuration that materially regresses a critical Phase 2 exact/lexical stratum merely because the global average improves.

At minimum compare:

- lexical versus dense;
- lexical versus hybrid;
- best Phase 2 path versus classifier-selected Phase 3 path.

Critical regression slices include:

- exact document code;
- exact clause number;
- product model;
- numeric/unit query;
- wrong-edition hard negative;
- negation/exception query.

### 18.4 Query-classifier evaluation

Create independently reviewed expected routing labels for a representative query subset.

Report a confusion matrix for:

- exact-dominant;
- hybrid-natural-language;
- ambiguous;
- later-phase-high-accuracy-intent.

More important than aggregate accuracy, require zero known cases where deterministic exact anchors are discarded and cause a wrong-edition/wrong-document retrieval path.

### 18.5 Leakage control

Embedding model, RRF parameter, candidate-pool, and classifier-rule selection use development/model-selection data only.

The final release gate uses the existing preregistered held-out/confirmation discipline inherited from earlier phases. Do not repeatedly tune against an observed release gate.

## 19. Work package M: Embedding benchmark and held-out data separation

The model-selection workflow must explicitly separate:

1. development cases used while implementing the harness;
2. model-selection/benchmark cases used to compare candidate models and RRF parameters;
3. held-out release-gate cases used only after the candidate configuration is frozen.

The frozen candidate identity includes:

- embedding model ID/revision;
- provider/configuration hash;
- embedding-text version/configuration;
- release vector dtype/normalization rule;
- dense candidate pool size;
- lexical candidate pool size;
- RRF configuration;
- query-analysis rule-set/configuration;
- classifier rule-set/configuration;
- exact dense backend/version;
- relevant dependency-lock/toolchain identity.

Changing any behavior-bearing item creates a new candidate and invalidates prior final-gate evidence according to the existing retry/confirmation policy.

## 20. Work package N: Release/cache integration

### 20.1 Embedding cache key

Use the dependency contract in `docs/design.md` Section 32.

The embedding artifact depends on:

- ordered chunk identity/text hashes;
- embedding scope;
- row-order version;
- embedding model ID/revision;
- model/provider assets or external request parameters;
- embedding configuration;
- dependency lock;
- toolchain fingerprint where required.

### 20.2 Vector artifact cache key

The vector artifact depends on:

- embedding artifact hash;
- backend/engine ID and version;
- distance metric;
- vector-search configuration;
- dependency lock;
- toolchain fingerprint where required.

For the NumPy exact backend, the vector artifact may simply be the validated embedding matrix plus declared backend metadata rather than a second redundant index file. Do not manufacture an index artifact with no function solely for symmetry.

### 20.3 Invalidation tests

Require cache misses after:

- changed source/chunk text;
- changed chunk membership affecting `embedding_text`;
- changed embedding model/revision;
- changed embedding configuration;
- changed embedding-text projection version;
- changed dtype/normalization rule;
- changed row-order version;
- changed vector backend/metric/configuration;
- changed behavior-bearing query/fusion configuration when it is part of release identity.

Require cache hits when only unrelated artifacts change and the declared dependency set is unchanged.

## 21. Work package O: Evidence Lineage extension

Phase 2 already materializes immutable source/build lineage. Phase 3 extends release build provenance with the new retrieval artifacts.

The Phase 3 lineage update must include:

- embedding-text transformation identity;
- embedding provider/model/revision/configuration identity;
- embedding artifact hash;
- vector backend/metric/configuration identity;
- vector artifact hash or exact-backend declaration;
- lexical index hash already present from Phase 2;
- RRF rule/configuration identity where it is admitted as a release behavior input;
- query-analysis/classifier rule-set/configuration identity where required by build/release identity.

Every new build transformation retains the complete transformation tuple required by the merged Phase 2 lineage contract:

```text
kind,
role,
producer,
producer_version,
configuration_sha256,
content_sha256
```

Phase 3 does not add Phase 4 query-specific context-path lineage.

## 22. Work package P: Release manifest and build identity

A Phase 3 candidate release must bind all Phase 3 behavior-bearing artifacts and configuration.

Add or validate manifest fields for:

- embedding artifact metadata;
- model ID/revision;
- vector dimensions;
- dtype;
- normalization state;
- row count;
- embedding scope;
- row-order version;
- vector backend/metric;
- lexical index hash;
- RRF configuration/version;
- query-analysis rule-set/version/hash;
- classifier rule-set/version/hash;
- Phase 3 evaluation/gate result hashes;
- updated `lineage.json` hash.

The exact release-identity dependency graph must avoid recursion: content artifacts are built and hashed before `build_content_id`/`release_id` are derived, following the existing Phase 2 release contract.

## 23. Work package Q: Runtime capability detection

At startup, after ordinary Phase 2 release integrity validation, determine whether the active release supports Phase 3 dense/hybrid capability.

A release is dense-capable only when all required Phase 3 artifacts/configuration are present and valid.

The installed runtime is dense-capable only when:

- required safe model loader/provider dependencies are installed;
- the exact admitted model/provider is supported;
- the exact dense backend is available;
- the runtime supports the release's schema/configuration versions.

The internal capability view distinguishes:

- exact/lexical available;
- dense available;
- hybrid available;
- high-accuracy unavailable until Phase 4.

Do not advertise hybrid success capability merely because an embeddings file exists.

## 24. Work package R: Failure behavior

Phase 3 failures must be explicit and deterministic.

### 24.1 Build failures

Block the candidate release for:

- embedding-model load failure;
- embedding dimension drift;
- NaN/Inf vectors;
- zero/invalid normalized vectors;
- missing/duplicate row;
- non-deterministic row mapping;
- unsupported artifact dtype/schema;
- checksum mismatch;
- evaluation gate failure;
- held-out leakage;
- stale benchmark/selection identity;
- release-lineage mismatch.

### 24.2 Runtime failures

An explicit hybrid request fails rather than silently degrading for:

- missing dense release artifact;
- unsupported embedding model/revision;
- query model load timeout/failure;
- query dimension mismatch;
- vector artifact integrity failure;
- dense backend unavailable;
- release quarantined.

Reuse the common typed runtime error routing and safe detail allowlists already established by the lower-phase runtime contract. Phase 3 must not invent a second error envelope.

### 24.3 `auto` preparation

The classifier/path resolver may record a degraded-capability decision internally for future Phase 4/public wiring, but Phase 3 does not claim the final typed-warning semantics owned by later evidence-tool work.

## 25. Work package S: Performance measurement

Measure performance only after retrieval correctness gates pass.

Report separately:

- embedding build throughput;
- embedding artifact size;
- exact dense-search latency with precomputed query vector;
- warm query-embedding latency;
- cold model-load latency;
- end-to-end warm hybrid candidate latency;
- end-to-end cold hybrid candidate latency;
- lexical-only candidate latency;
- peak RSS with memory-mapped vectors;
- incremental RSS after loading query model;
- page-fault behavior for first dense query where practical;
- candidate-pool sensitivity;
- corpus-size scaling.

Test at representative chunk counts around the design's scale hypotheses when practical:

- <50k chunks;
- 50k-300k synthetic/representative scale where available.

Do not add ANN in this phase solely because a synthetic larger scale is slower. Record the measured threshold for future evaluation.

## 26. Work package T: Determinism and reproducibility

Phase 3 must be reproducible enough to support immutable releases.

Required checks include:

- same input release/build configuration produces the same row map;
- same embedding provider/model/configuration and deterministic model runtime produce byte-identical or explicitly tolerance-governed canonical embedding artifacts according to the provider's admitted reproducibility contract;
- the release artifact after canonical conversion is stable under the admitted build environment;
- exact dense ranking is stable;
- RRF ranking is byte-for-byte/record-for-record deterministic;
- classifier output is deterministic;
- candidate provenance ordering is deterministic;
- repeated release validation produces the same decision;
- rollback restores the previous embedding/vector/fusion configuration together with the previous catalog and lineage.

If a model/provider cannot produce a release artifact reproducibly enough to satisfy the immutable release contract, it must not be selected simply because its retrieval score is high.

## 27. Work package U: Security and privacy

Phase 3 must retain the lower-phase local-first security model.

- local model assets are checksum verified;
- no arbitrary pickle model format;
- no model loader arbitrary-code hooks;
- no network access is introduced at runtime by default;
- an external embedding provider, if ever benchmarked, is not selected without an explicit design/security/privacy decision;
- queries, source text, and credentials are not written to unrestricted logs;
- model paths and workspace paths are not exposed through public retrieval results;
- malformed query inputs are rejected before model work according to the common MCP/input contract;
- cancellation and request-count admission remain processable while a model is loading;
- vector row indices are internal diagnostics, not trusted client-supplied locators.

## 28. Test plan

### 28.1 Unit tests

Cover:

- embedding-text projection;
- provider metadata validation;
- row-order generation;
- matrix normalization;
- matrix shape/dtype validation;
- query-vector validation;
- exact dot-product search;
- deterministic top-K tie-breaking;
- metadata filter semantics;
- dense hit mapping;
- RRF contributions;
- candidate deduplication;
- fused tie-breaking;
- query feature extraction;
- classifier rules;
- candidate provenance serialization;
- cache-key construction.

### 28.2 Integration tests

Cover:

- build valid Phase 3 release from Phase 2 catalog;
- mmap/reopen in a fresh runtime process;
- lazy-load query model;
- warm hybrid retrieval;
- cold hybrid retrieval;
- exact-mode query remains model-free;
- lexical+dense fused result contains correct per-channel provenance;
- wrong-edition high-similarity chunk is filtered/ordered correctly;
- checksum corruption blocks startup;
- model asset corruption quarantines/fails according to the common runtime contract;
- rollback changes the active vector/model configuration atomically with the release.

### 28.3 Boundary/negative tests

Include:

- zero-norm query vector;
- wrong vector dimensions;
- NaN/Inf query/model output;
- duplicate chunk row;
- missing chunk row;
- extra vector row;
- mixed document/chunk scope;
- unsupported dtype;
- writable memory map attempt;
- identical similarity scores across several candidates;
- lexical/dense duplicate source;
- same text in two editions;
- empty dense result after filters;
- model-load timeout;
- cancelled cold hybrid request;
- request deadline during dense search;
- explicit hybrid when runtime dependency absent;
- classifier query with both clause number and natural-language question;
- false identifier-looking token;
- negative wording such as "not permitted";
- numeric/unit query where semantic similarity must not erase exact numeric constraints.

### 28.4 Evaluation tests

Run the complete Phase 3 retrieval gate suite on the frozen held-out confirmation data only after configuration freeze.

## 29. Suggested implementation sequence

Execute in this order so each step has a clear dependency and test boundary.

1. Freeze Phase 3 schemas/interfaces and branch-local test fixtures.
2. Validate the Phase 2 chunk enumeration handoff.
3. Implement deterministic `embedding_text` projection and hashes.
4. Implement embedding-provider abstraction.
5. Build the benchmark harness before selecting a model.
6. Benchmark candidate embedding models on development/model-selection data.
7. Select/freeze the embedding candidate with a decision artifact.
8. Implement canonical offline chunk embedding generation.
9. Implement deterministic row-map generation and independent validation.
10. Implement safe `.npy` release artifact validation.
11. Implement memory-mapped exact dense backend.
12. Implement dense hit → Phase 2 source mapping and filters.
13. Integrate supervised lazy current-query embedding.
14. Implement typed dense candidate provenance.
15. Implement lexical+dense source-identity deduplication.
16. Implement RRF with versioned configuration and deterministic ties.
17. Benchmark candidate pools and RRF parameters on model-selection data.
18. Implement deterministic query feature extraction.
19. Implement deterministic query classification/path resolution.
20. Add comparative exact/lexical/dense/hybrid evaluation.
21. Add cache dependencies and Phase 3 lineage transformations.
22. Add Phase 3 release manifest/build identity inputs.
23. Add release validation/startup validation.
24. Run negative, corruption, cancellation, rollback, and reproducibility suites.
25. Freeze the complete Phase 3 candidate identity.
26. Run the untouched held-out/confirmation retrieval gates under the existing retry policy.
27. Produce final Phase 3 benchmark/gate report.
28. Activate a Phase 3 release in integration tests and verify rollback to Phase 2/earlier release as applicable.
29. Record the Phase 4 handoff without implementing Phase 4.

## 30. Acceptance criteria

Phase 3 is complete only when all applicable criteria below are true.

1. A replaceable embedding-provider contract exists and no model-native object leaks into public canonical/retrieval interfaces.
2. The selected embedding model is supported by a reproducible project-corpus benchmark, including English, Chinese, cross-language, engineering terminology, identifiers, numbers/units, synonyms, negation, and exceptions.
3. Exactly one release embedding exists for every persisted Phase 2 chunk.
4. The vector matrix contains no document-level or sentinel rows.
5. Row order is exactly `(document_id, canonical_order, chunk_id)` and is independently reconstructed at release validation.
6. The matrix is a safe admitted numeric `.npy` artifact, read-only at runtime, with no pickle/object dtype.
7. Manifest shape/dtype/normalization/model/row-order metadata matches the actual artifact exactly.
8. Query embedding uses the exact model/revision/configuration compatible with the active release.
9. Exact dense search is deterministic and memory-mapped.
10. Dense candidates map one-to-one to canonical Phase 2 chunks/sources.
11. Metadata filters preserve document and edition safety.
12. Lexical and dense candidates are deduplicated by canonical source identity, not text similarity.
13. RRF is versioned, benchmark-selected, reproducible, and deterministically ordered.
14. Every fused candidate retains complete lexical/dense/fusion retrieval provenance.
15. Query analysis deterministically detects the design-required feature families.
16. Query classification is deterministic and does not rely on an LLM.
17. Exact-style queries are not forced through dense retrieval.
18. Natural-language queries can execute the Phase 3 lexical+dense hybrid path.
19. Explicit hybrid capability failure is visible rather than silently relabelled lexical retrieval.
20. Phase 3 does not advertise context-complete final evidence tools before Phase 4 can satisfy Section 19.
21. The frozen Phase 3 retrieval candidate passes Recall@20 with one-sided 95% Wilson lower bound >=98% on the applicable held-out confirmation set.
22. The frozen Phase 3 retrieval candidate passes Top-5 with one-sided 95% Wilson lower bound >=95% on the applicable held-out confirmation set.
23. Every probabilistic result reports numerator, denominator, point estimate, and lower confidence bound with required sample sizes/stratification.
24. Critical exact/numeric/identifier/wrong-edition/negation strata have no unacceptable regression hidden by a better global average.
25. Embedding/vector/fusion/classifier changes invalidate the correct caches and release identity.
26. `lineage.json` contains the Phase 3 embedding/vector transformation identities and artifact hashes while preserving Phase 2 source/build provenance.
27. Release validation fails closed for corrupted, mismatched, unsupported, or incompletely mapped vector artifacts.
28. Lazy model integrity failure follows the existing quarantine contract.
29. Cancellation/deadline/model-load behavior uses the common runtime terminal-state implementation.
30. Documentation-quality, unit, integration, negative, reproducibility, release, activation, and rollback tests all pass.
31. No Phase 4 reranker/context traversal/refusal implementation has been pulled into the Phase 3 PR.

## 31. Phase 3 exit artifacts

At merge, the Phase 3 implementation should be able to produce a complete decision/evidence package containing:

- selected embedding model/revision/configuration;
- embedding benchmark report;
- embedding-text schema/configuration;
- embedding artifact metadata/hash;
- deterministic row-map identity;
- exact dense backend/metric/configuration;
- RRF configuration;
- query-analysis/classifier rule-set/configuration;
- cache/build identity hashes;
- updated release lineage;
- comparative lexical/dense/hybrid evaluation report;
- held-out confirmation gate report;
- cold/warm/model-free performance report;
- release validation result;
- rollback validation result.

These artifacts make the Phase 3 choice auditable and reproducible.

## 32. Handoff to Phase 4

Phase 4 receives a stable ranked-candidate layer with:

- exact/lexical Phase 2 retrieval intact;
- dense chunk retrieval;
- lexical+dense RRF;
- deterministic query analysis/classification;
- complete retrieval-channel provenance;
- immutable embedding/vector artifacts;
- release-bound model/configuration identity;
- expanded regression evaluation.

Phase 4 then owns the design-defined high-accuracy work:

- cross-encoder reranking;
- deterministic Evidence Graph required/supporting context traversal;
- table/context improvements;
- cross-reference traversal improvements;
- final context-complete Evidence Package behavior;
- typed warnings/refusal support associated with final evidence assembly.

Phase 3 must not pre-implement those responsibilities merely to make its internal hybrid candidate layer look like the final product.

## 33. Definition of done

The Phase 3 PR is ready to merge only when:

- the implementation remains within the Phase 3 boundary;
- all repository checks pass on the exact PR head;
- the Phase 3 retrieval gates pass on the correctly isolated evaluation data;
- all actionable review comments that are genuinely Phase 3 scope are fixed and replied to;
- all resolved review threads are marked resolved;
- out-of-scope Phase 4 feedback is explicitly deferred rather than implemented;
- reviewers have no further Phase 3 comments on the exact final head;
- the PR description matches the final Phase 3 plan/implementation state;
- the final head is merged into `master` before Phase 4 work begins.
