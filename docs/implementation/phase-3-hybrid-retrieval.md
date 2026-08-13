# Phase 3 Implementation Plan: Hybrid Retrieval

**Project:** ClauseSift  
**Phase:** 3 of the design-defined implementation sequence  
**Status:** Implementation plan  
**Primary design authority:** `docs/design.md`  
**Phase objective:** Extend the merged Phase 2 exact/lexical retrieval baseline with benchmarked chunk embeddings, deterministic memory-mapped exact dense retrieval, lexical+dense reciprocal-rank fusion, deterministic query classification, and expanded retrieval evaluation, while composing with the inherited Phase 2 required-context/material-conflict evidence pipeline—without implementing Phase 4 cross-encoder reranking, additional supporting-context expansion, high-accuracy table/cross-reference improvements, or expanded high-accuracy warning/refusal evaluation.

## 1. Purpose

Phase 3 adds the first semantic retrieval path to ClauseSift while preserving the design's accuracy-first, deterministic, source-grounded architecture.

Phase 2 already establishes the authoritative corpus identity, canonical document model, chunk/source identity, SQLite catalog, exact lookup, lexical retrieval, deterministic citations, deterministic required Evidence Graph context closure, material-conflict closure, the shared Python/CLI/MCP evidence interfaces, immutable release lifecycle, release lineage, and the common runtime baseline. Phase 3 must build on those contracts rather than introduce parallel identities, parallel metadata stores, a second evidence pipeline, or a second retrieval model.

The core Phase 3 question is not merely whether embeddings can retrieve semantically similar text. The phase must prove that semantic retrieval improves evidence recall on real engineering questions without degrading edition safety, exact-identifier behavior, deterministic release construction, source traceability, required-context completeness, conflict completeness, runtime safety, or the ability to reproduce a retrieval decision from immutable release artifacts.

Phase 3 therefore has five design-defined outcomes:

1. select an embedding model using ClauseSift's own multilingual engineering evaluation corpus;
2. generate exactly one release-bound embedding for every persisted chunk;
3. implement deterministic exact dense search over a memory-mapped chunk matrix;
4. fuse lexical and dense rankings using a versioned reciprocal-rank-fusion contract;
5. classify queries deterministically so the runtime can distinguish exact-style and natural-language retrieval needs while preserving the shared evidence contract.

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
- per-channel retrieval provenance integrated into the existing Evidence Lineage/evidence-service contract;
- deterministic query feature extraction;
- deterministic query classification for exact-style versus natural-language/hybrid retrieval needs;
- resolution of the best Phase 3-capable retrieval path through the existing shared retrieval service;
- composition of hybrid retrieval seeds with the inherited required-context and material-conflict closure;
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
- additional supporting/diagnostic context expansion beyond the inherited Phase 2 required-context and material-conflict closure;
- reimplementation, weakening, bypass, or alternate semantics for the inherited required-context/material-conflict closure;
- new semantic relationship extraction merely to improve dense search;
- LLM-based query classification;
- LLM-based query rewriting as an authoritative retrieval step;
- arbitrary generated query expansion that becomes source authority;
- approximate nearest-neighbour search solely because it is conventional;
- a permanently running vector database;
- document-level vectors;
- mixed document/chunk embedding matrices;
- multiple embeddings per chunk without a separately versioned future design;
- a separate or weakened `search_evidence`, `get_clause`, `get_context`, resource, or Evidence Package success path that bypasses the inherited context/conflict/evidence contract;
- Phase 4 high-accuracy-specific warning/refusal evaluation expansion;
- Phase 4 supporting-context/table improvements;
- Phase 4 cross-reference high-accuracy improvements;
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
17. `auto` may select only capabilities present in both the installed runtime and active release.
18. A dense-retrieval failure cannot silently impersonate a successful hybrid result in an explicit hybrid request.
19. Metadata filters, document identity, edition, jurisdiction, and other Phase 2 authority boundaries remain authoritative over semantic similarity.
20. Fusion combines candidate rankings; it cannot invent a source, document, clause, relationship, applicability fact, or context edge.
21. Dense and lexical channels retain independent retrieval provenance so the current Evidence Lineage can explain why a source was selected and Phase 4 can extend that provenance for high-accuracy behavior without replacing it.
22. All release artifacts are immutable, checksummed, validated before activation, and rolled back together.
23. Runtime model assets are safe-loaded under the existing release-integrity rules; pickle-backed arbitrary-code model assets remain prohibited.
24. Lazy model loading, cancellation, deadlines, worker supervision, quarantine, and resource-admission semantics reuse the common runtime contract rather than creating a second implementation.
25. Query classification is deterministic in Phase 3. A model may not decide whether exact evidence protections should be bypassed.
26. No retrieval score is interpreted as engineering confidence, legal authority, applicability, or normative force.
27. Evaluation results, not convenience, determine the selected embedding model, candidate sizes, RRF parameters, and any later performance optimization.
28. Every successful exact, lexical, or hybrid retrieval path runs the same inherited required-context, material-conflict, citation, lineage, and Evidence Package semantics after seed selection.

## 4. Prerequisites and Phase 2 handoff

Phase 3 starts only from the merged Phase 2 baseline on `master` as interpreted by the current design authority.

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
- deterministic required Evidence Graph context closure;
- material-conflict closure and complete material-side preservation;
- the shared Python/CLI/MCP evidence-service interfaces;
- strict Evidence Package serialization and typed failure/warning semantics already required by the current lower-phase design;
- release artifact manifest/checksum machinery;
- `build_content_id` and `release_id` identity rules;
- RFC 8785 release lineage;
- cache dependency declarations;
- atomic activation/rollback;
- runtime admission, cancellation, byte-budget, and quarantine behavior;
- Phase 0 evaluation corpus after the reviewed canonical-ID migration.

Before Phase 3 implementation begins, add a compatibility test that opens a valid Phase 2 release and proves that the Phase 3 builder can enumerate the exact canonical chunk sequence without altering the Phase 2 catalog. Add a runtime compatibility fixture proving that an unchanged exact/lexical request retains the same required-context/material-conflict result before and after Phase 3 dense capability is installed.

## 5. Phase 3 deliverables

The phase should produce the following implementation deliverables.

### 5.1 Build-time deliverables

- embedding-provider interface and selected provider implementation;
- embedding benchmark harness;
- embedding benchmark report and selection record;
- deterministic embedding-text fixture suite;
- chunk embedding builder;
- canonical row-map generator/validator;
- `embeddings.f16.npy` release artifact;
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
- Phase 3 retrieval-path resolver integrated with the existing shared retrieval service;
- retrieval provenance records integrated into the current Evidence Lineage/evidence assembly contract;
- inherited required-context/material-conflict closure after Phase 3 seed ranking;
- performance diagnostics for model-free, cold, and warm hybrid queries.

### 5.3 Decision artifacts

The repository should retain human-readable, versioned records of:

- embedding candidates evaluated;
- exact model identifiers/revisions;
- exact local model/tokenizer asset identities and hashes, or external-provider request parameters if an external provider is ever admitted;
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
- fusion/routing ends at retrieval-seed selection and then enters the existing shared context/conflict/evidence pipeline;
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
- complete tokenizer/model asset identity where applicable;
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

plus the complete authoritative dependency set from `docs/design.md` Section 25, including at minimum:

- `embedding_scope: "chunk"`;
- row-order version;
- model identifier/revision;
- complete model/provider asset or external-request identity;
- provider/configuration identity;
- dependency-lock hash;
- build-toolchain fingerprint where required.

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

1. freeze model ID/revision, complete model asset identity, and provider configuration;
2. build embeddings from the same immutable benchmark chunk set;
3. verify deterministic row mapping;
4. verify byte-identical canonical embedding output for repeated equivalent builds under the admitted build environment;
5. run exact dense search only;
6. measure Recall@K over several K values including 5 and 20;
7. record MRR/NDCG or another ranking diagnostic only as secondary evidence, not a replacement for the design's release gates;
8. report performance by stratum, not only globally;
9. measure build throughput;
10. measure artifact size;
11. measure cold model-load time;
12. measure warm query-embedding latency;
13. measure exact dense-search latency separately from embedding latency;
14. measure peak resident memory;
15. measure packaging/model-asset complexity;
16. retain all candidate results, including failed/rejected models.

### 9.4 Selection criteria

The selected model must be the best evidence-backed trade-off under the project's priority order:

1. retrieval correctness;
2. cross-language and hard-negative robustness;
3. byte-reproducibility and safe loading;
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

The v0.1 release artifact follows the design's fixed safe numeric matrix contract:

- filename/artifact kind `embeddings.f16.npy`;
- one numeric rank-two `.npy` matrix;
- chunk-only scope;
- actual and manifest-declared dtype exactly `float16`;
- no object dtype;
- no structured dtype;
- no pickle;
- no `.npz` fallback;
- normalized vectors when cosine-equivalent dot-product search is selected;
- finite values only;
- no NaN/Inf;
- declared dimensions exactly equal every row's width.

If provider output is higher precision, canonical conversion happens once under a versioned rule before sealing the release artifact and is covered by evaluation. A different release dtype requires an explicit future design/release-schema change; it is not a Phase 3 implementation choice.

### 10.4 Artifact metadata

The release manifest records at minimum:

- artifact path;
- SHA-256;
- byte size;
- `embedding_scope: "chunk"`;
- `row_count`;
- `vector_dimensions`;
- `dtype: "float16"`;
- `normalized`;
- row-order schema/version;
- embedding model ID;
- embedding model revision;
- complete model format/loader/tokenizer/weight asset identity required by the release contract;
- provider/configuration hash;
- embedding-text schema/version;
- embedding artifact schema/version.

### 10.5 Atomic builder behavior

Write the matrix to a candidate-release temporary location, validate it completely, then seal it into the candidate release. A failed or interrupted build must not modify the currently active release.

## 11. Work package E: Embedding artifact validation

The independent release gate must validate the artifact without trusting builder in-memory state.

Required checks include:

- checksum and byte size;
- safe loading equivalent to `numpy.load(path, mmap_mode="r", allow_pickle=False, max_header_size=10000)`;
- no fallback retry with a larger or unbounded NumPy header;
- rank exactly two;
- dtype exactly `float16`;
- finite values;
- normalization invariant within declared numerical tolerance;
- dimensions match manifest;
- row count equals catalog chunk count;
- reconstructed row map is total and one-to-one;
- row ordering exactly matches `(document_id, canonical_order, chunk_id)`;
- embedding scope is exactly `chunk`;
- row-order version supported;
- model/configuration and complete model-asset identity supported;
- expected file size consistent with shape/dtype/header contract;
- matrix is read-only at runtime;
- no unexpected sidecar file is required by the loader;
- lineage identifies the embedding transformation and artifact hash.

Corruption, row mismatch, non-`float16` dtype, oversized/malformed header, unknown schema, or incomplete model-asset binding blocks activation.

## 12. Work package F: Memory-mapped exact dense search

### 12.1 Default backend

Implement the initial exact backend using a NumPy memory map for small and medium corpora.

The runtime opens the independently validated matrix read-only under the same bounded safe-loading contract and performs exact score computation conceptually equivalent to:

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

ANN remains out of scope unless a separately measured future change proves exact search cannot meet target latency and its recall loss is explicitly evaluated.

### 12.3 Query-vector validation

Before scoring:

- query vector dimensions must equal release dimensions;
- values must be finite;
- vector must satisfy the selected normalization contract;
- model identity and complete asset/configuration identity used for the query must match the release embedding identity;
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
- use the exact model ID/revision/configuration and complete bound asset set named by the active release;
- use safe model formats/loaders admitted by the release contract;
- recheck every file the loader may open against the manifest byte size/SHA-256 table before deserialization;
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
- model ID/revision and complete model-asset/configuration identity;
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

Exact identifier lookup remains available through exact-mode routing. Phase 4 may consume the stable ranked candidate layer for high-accuracy reranking without replacing Phase 3's identity/fusion contracts.

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

Any high-accuracy candidate-count guidance in the design is a hypothesis for later high-accuracy work, not a fixed Phase 3 constant. Select Phase 3 values using Recall@K and hard-negative evidence.

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

This is retrieval provenance. It does not alter source provenance, required context, material conflicts, or evidence meaning.

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
- **later-phase-high-accuracy-intent** — query characteristics suggest Phase 4 reranking, additional supporting context, or high-accuracy table/cross-reference handling may be useful, but Phase 3 must not implement those Phase 4 additions.

The public design mode enum remains `auto`, `exact`, `hybrid`, `high_accuracy`; this internal classification vocabulary need not become a public enum.

### 17.2 Conservative routing

Recommended Phase 3 behavior:

- exact-dominant → use existing exact-mode retrieval path;
- hybrid-natural-language → use lexical+dense fusion;
- ambiguous → prefer the path proven by evaluation, with exact anchors preserved as constraints/features rather than discarded;
- later-phase-high-accuracy-intent → preserve the intent signal, but do not implement Phase 4 reranking, extra supporting-context expansion, or other high-accuracy-only behavior.

Phase 3 integrates the resolved retrieval path into the existing shared retrieval service. Once retrieval seeds are selected, the inherited Phase 2 required-context and material-conflict closure executes, followed by the existing strict Evidence Package serialization and shared Python/CLI/MCP projection. Hybrid routing must not create a diagnostic-only or weakened evidence path merely because the seed channel is semantic.

### 17.3 Explicit override preparation

The service layer should accept a typed requested mode/path consistent with the current shared retrieval contract so Phase 4 can extend `high_accuracy` without replacing Phase 3 internals.

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

### 18.5 Downstream evidence-semantics regression

Hybrid retrieval evaluation must also prove that changing the seed channel does not weaken the inherited evidence contract. Required regression slices verify:

- required parent scope is retained;
- applicability is retained;
- dependencies/definitions/exceptions are retained when required;
- required table context is retained;
- every material conflict side survives adverse lexical/dense/fusion ranks;
- context-limit behavior remains a typed failure/incomplete-required outcome rather than a truncated hybrid success;
- deterministic citations/source/edition identity are unchanged;
- Python/CLI/MCP expose the same evidence semantics for the same resolved request.

### 18.6 Leakage control

Embedding model, RRF parameter, candidate-pool, and classifier-rule selection use development/model-selection data only.

The final release gate uses the existing preregistered held-out/confirmation discipline inherited from earlier phases. Do not repeatedly tune against an observed release gate.

## 19. Work package M: Embedding benchmark and held-out data separation

The model-selection workflow must explicitly separate:

1. development cases used while implementing the harness;
2. model-selection/benchmark cases used to compare candidate models and RRF parameters;
3. held-out release-gate cases used only after the candidate configuration is frozen.

The frozen candidate identity includes:

- embedding model ID/revision and complete model-asset identity;
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

Use the authoritative dependency contract in `docs/design.md` Section 25 — **Build cache and invalidation**.

The Phase 3 implementation inherits the complete Section 25 chunk-embedding dependency entry, including the ordered chunk identity/text hashes, embedding scope, row-order version, exact model/provider asset or external request identity, embedding configuration, dependency lock, and build-toolchain fingerprint. The abbreviated list here is not a substitute for that authoritative table.

### 20.2 Vector artifact cache key

Use the complete Section 25 vector-index dependency entry.

The vector artifact depends on at least:

- embedding artifact hash;
- backend/engine ID and version;
- distance metric;
- vector-search configuration;
- dependency lock;
- toolchain fingerprint where required.

For the NumPy exact backend, the vector artifact may simply be the validated embedding matrix plus declared backend metadata rather than a second redundant index file. Do not manufacture an index artifact with no function solely for symmetry.

### 20.3 Invalidation tests

Require cache misses after every behavior-bearing dependency identified by Section 25 changes, including:

- changed source/chunk text;
- changed chunk membership affecting `embedding_text`;
- changed embedding model/revision or any bound model asset;
- changed embedding configuration;
- changed embedding-text projection version;
- changed dtype/normalization rule;
- changed row-order version;
- changed vector backend/metric/configuration;
- changed dependency lock/toolchain identity where declared;
- changed behavior-bearing query/fusion configuration when it is part of release identity.

Require cache hits only when the complete declared dependency set is unchanged.

## 21. Work package O: Evidence Lineage extension

Phase 2 already materializes immutable source/build lineage and the runtime already has the evidence-assembly lineage contract. Phase 3 extends that provenance with the new retrieval artifacts and channels.

The Phase 3 lineage update must include:

- embedding-text transformation identity;
- embedding provider/model/revision/configuration and complete bound asset identity;
- embedding artifact hash;
- vector backend/metric/configuration identity;
- vector artifact hash or exact-backend declaration;
- lexical index hash already present from Phase 2;
- RRF rule/configuration identity where it is admitted as a release behavior input;
- query-analysis/classifier rule-set/configuration identity where required by build/release identity;
- lexical/dense/fusion channel rank/score/contribution metadata for selected retrieval seeds as required by the existing runtime lineage contract.

Every new build transformation retains the complete transformation tuple required by the merged Phase 2 lineage contract:

```text
kind,
role,
producer,
producer_version,
configuration_sha256,
content_sha256
```

Phase 3 does not add Phase 4 reranker or extra supporting-context-specific provenance, but it must preserve all inherited required-context/material-conflict assembly lineage.

## 22. Work package P: Release manifest and build identity

A Phase 3 candidate release must bind all Phase 3 behavior-bearing artifacts and configuration.

Add or validate manifest fields for:

- embedding artifact metadata;
- model ID/revision;
- complete local model format/loader/tokenizer/weight asset table and aggregate digest where local assets are used;
- vector dimensions;
- `dtype: "float16"`;
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

The exact release-identity dependency graph must avoid recursion: content artifacts are built and hashed before `build_content_id`/`release_id` are derived, following the existing release contract.

## 23. Work package Q: Runtime capability detection

At startup, after ordinary lower-phase release integrity validation, determine whether the active release supports Phase 3 dense/hybrid capability.

A release is dense-capable only when all required Phase 3 artifacts/configuration are present and valid.

The installed runtime is dense-capable only when:

- required safe model loader/provider dependencies are installed;
- the exact admitted model/provider and complete asset identity are supported;
- the exact dense backend is available;
- the runtime supports the release's schema/configuration versions.

The capability view distinguishes:

- exact/lexical available;
- dense available;
- hybrid available;
- `high_accuracy` available only to the extent already defined by the current design/runtime; Phase 4-specific reranker/supporting-context enhancements remain unavailable until implemented.

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
- non-byte-reproducible canonical embedding artifact for identical complete build identity;
- unsupported artifact dtype/schema;
- oversized/malformed NumPy header;
- checksum mismatch;
- incomplete/stale model-asset binding;
- evaluation gate failure;
- held-out leakage;
- stale benchmark/selection identity;
- release-lineage mismatch.

### 24.2 Runtime failures

An explicit hybrid request fails rather than silently degrading for:

- missing dense release artifact;
- unsupported embedding model/revision or asset set;
- query model load timeout/failure;
- query dimension mismatch;
- vector artifact integrity failure;
- dense backend unavailable;
- release quarantined.

Reuse the common typed runtime error routing and safe detail allowlists already established by the lower-phase runtime contract. Phase 3 must not invent a second error envelope or a context-incomplete semantic-success branch.

### 24.3 `auto` capability resolution

The classifier/path resolver may choose only installed-and-release-supported capabilities. If `auto` selects a non-dense path because dense capability is unavailable, the decision must follow the current design's capability/warning semantics and still enter the same inherited context/conflict/evidence pipeline. An explicit hybrid request does not silently degrade.

## 25. Work package S: Performance measurement

Measure performance only after retrieval correctness and evidence-semantics gates pass.

Report separately:

- embedding build throughput;
- embedding artifact size;
- exact dense-search latency with precomputed query vector;
- warm query-embedding latency;
- cold model-load latency;
- end-to-end warm hybrid candidate latency;
- end-to-end cold hybrid candidate latency;
- lexical-only candidate latency;
- inherited required-context/material-conflict closure latency separately where practical;
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

Phase 3 must satisfy immutable-release reproducibility.

Required checks include:

- same input release/build configuration produces the same row map;
- same complete build identity produces byte-identical canonical `embeddings.f16.npy` bytes and SHA-256 across fresh admitted build processes/environments;
- numerical tolerance is used only for numerical invariants such as normalization checks, never as a substitute for artifact byte equality;
- the release artifact after canonical conversion is byte-stable under the admitted build environment;
- exact dense ranking is stable;
- RRF ranking is byte-for-byte/record-for-record deterministic;
- classifier output is deterministic;
- candidate provenance ordering is deterministic;
- repeated release validation produces the same decision;
- rollback restores the previous embedding/vector/fusion configuration together with the previous catalog, context/conflict artifacts, and lineage.

If a model/provider cannot produce a byte-identical canonical release artifact for the same complete build identity, it must not be selected simply because its retrieval score is high.

## 27. Work package U: Security and privacy

Phase 3 must retain the lower-phase local-first security model.

- local model assets are checksum verified exhaustively;
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
- provider metadata and complete asset-identity validation;
- row-order generation;
- canonical float16 conversion;
- matrix normalization;
- matrix shape/dtype/header validation;
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
- cache-key construction against the Section 25 dependency contract.

### 28.2 Integration tests

Cover:

- build valid Phase 3 release from Phase 2 catalog;
- byte-identical repeated embedding build;
- mmap/reopen in a fresh runtime process with bounded safe `.npy` loading;
- lazy-load exact bound query model asset set;
- warm hybrid retrieval;
- cold hybrid retrieval;
- exact-mode query remains model-free;
- lexical+dense fused result contains correct per-channel provenance;
- wrong-edition high-similarity chunk is filtered/ordered correctly;
- hybrid seed result receives inherited required context and material-conflict closure;
- Python/CLI/MCP project identical evidence semantics after hybrid seed selection;
- checksum corruption blocks startup;
- model asset corruption/quarantine follows the common runtime contract;
- rollback changes the active vector/model configuration atomically with the release while restoring the matching catalog/context/conflict/lineage artifacts.

### 28.3 Boundary/negative tests

Include:

- zero-norm query vector;
- wrong vector dimensions;
- NaN/Inf query/model output;
- duplicate chunk row;
- missing chunk row;
- extra vector row;
- mixed document/chunk scope;
- non-`float16` release dtype;
- NumPy header over 10,000 bytes;
- object/structured dtype or pickle-backed matrix attempt;
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
- numeric/unit query where semantic similarity must not erase exact numeric constraints;
- hybrid seed whose required context exceeds bounds, proving the existing typed failure path is retained;
- hybrid seed intersecting one material conflict side, proving all required sides remain present.

### 28.4 Evaluation tests

Run the complete Phase 3 retrieval gate suite on the frozen held-out confirmation data only after configuration freeze, including the downstream evidence-semantics regressions from Section 18.5.

## 29. Suggested implementation sequence

Execute in this order so each step has a clear dependency and test boundary.

1. Freeze Phase 3 schemas/interfaces and branch-local test fixtures.
2. Validate the Phase 2 chunk enumeration and shared evidence-service handoff.
3. Implement deterministic `embedding_text` projection and hashes.
4. Implement embedding-provider abstraction and complete model-asset identity.
5. Build the benchmark harness before selecting a model.
6. Benchmark candidate embedding models on development/model-selection data.
7. Select/freeze the embedding candidate with a decision artifact.
8. Implement canonical offline chunk embedding generation to byte-stable `embeddings.f16.npy`.
9. Implement deterministic row-map generation and independent validation.
10. Implement bounded safe `.npy` release artifact validation.
11. Implement memory-mapped exact dense backend.
12. Implement dense hit → Phase 2 source mapping and filters.
13. Integrate supervised lazy current-query embedding with complete asset recheck.
14. Implement typed dense candidate provenance.
15. Implement lexical+dense source-identity deduplication.
16. Implement RRF with versioned configuration and deterministic ties.
17. Benchmark candidate pools and RRF parameters on model-selection data.
18. Implement deterministic query feature extraction.
19. Implement deterministic query classification/path resolution.
20. Compose Phase 3 seed selection with the inherited required-context/material-conflict closure and shared Python/CLI/MCP service.
21. Add comparative exact/lexical/dense/hybrid and downstream evidence-semantics evaluation.
22. Add full Section 25 cache dependencies and Phase 3 lineage transformations.
23. Add Phase 3 release manifest/build identity inputs including complete model-asset binding.
24. Add release validation/startup validation.
25. Run negative, corruption, cancellation, rollback, and reproducibility suites.
26. Freeze the complete Phase 3 candidate identity.
27. Run the untouched held-out/confirmation retrieval gates under the existing retry policy.
28. Produce final Phase 3 benchmark/gate report.
29. Activate a Phase 3 release in integration tests and verify rollback to an earlier release as applicable.
30. Record the corrected Phase 4 handoff without implementing Phase 4.

## 30. Acceptance criteria

Phase 3 is complete only when all applicable criteria below are true.

1. A replaceable embedding-provider contract exists and no model-native object leaks into public canonical/retrieval interfaces.
2. The selected embedding model is supported by a reproducible project-corpus benchmark, including English, Chinese, cross-language, engineering terminology, identifiers, numbers/units, synonyms, negation, and exceptions.
3. Exactly one release embedding exists for every persisted Phase 2 chunk.
4. The vector matrix contains no document-level or sentinel rows.
5. Row order is exactly `(document_id, canonical_order, chunk_id)` and is independently reconstructed at release validation.
6. The v0.1 matrix is exactly `embeddings.f16.npy`, actual/declared `float16`, safe-loaded read-only with `allow_pickle=False` and `max_header_size=10000`, with no object/structured dtype.
7. Manifest shape/dtype/normalization/model/complete-asset/row-order metadata matches the actual artifact exactly.
8. Query embedding uses the exact model/revision/configuration and complete asset identity compatible with the active release.
9. Same complete build identity produces byte-identical canonical embedding artifact bytes and SHA-256.
10. Exact dense search is deterministic and memory-mapped.
11. Dense candidates map one-to-one to canonical Phase 2 chunks/sources.
12. Metadata filters preserve document and edition safety.
13. Lexical and dense candidates are deduplicated by canonical source identity, not text similarity.
14. RRF is versioned, benchmark-selected, reproducible, and deterministically ordered.
15. Every fused candidate retains complete lexical/dense/fusion retrieval provenance.
16. Query analysis deterministically detects the design-required feature families.
17. Query classification is deterministic and does not rely on an LLM.
18. Exact-style queries are not forced through dense retrieval.
19. Natural-language queries can execute the Phase 3 lexical+dense hybrid path.
20. The Phase 3 hybrid path is exposed through the existing shared retrieval service/interfaces and preserves the inherited required-context/material-conflict closure, strict Evidence Package semantics, citations, lineage, typed failures, and edition/source identity.
21. Explicit hybrid capability failure is visible rather than silently relabelling lexical retrieval.
22. The frozen Phase 3 retrieval candidate passes Recall@20 with one-sided 95% Wilson lower bound >=98% on the applicable held-out confirmation set.
23. The frozen Phase 3 retrieval candidate passes Top-5 with one-sided 95% Wilson lower bound >=95% on the applicable held-out confirmation set.
24. Every probabilistic result reports numerator, denominator, point estimate, and lower confidence bound with required sample sizes/stratification.
25. Critical exact/numeric/identifier/wrong-edition/negation strata have no unacceptable regression hidden by a better global average.
26. Hybrid retrieval does not drop required scope/applicability/dependencies/definitions/exceptions/table context or any material conflict side.
27. Embedding/vector/fusion/classifier changes invalidate the complete correct Section 25 caches and release identity.
28. `lineage.json` contains the Phase 3 embedding/vector transformation identities, complete model-asset identity, artifact hashes, and retrieval-channel provenance while preserving lower-phase source/build/assembly provenance.
29. Release validation fails closed for corrupted, mismatched, unsupported, incompletely mapped, non-byte-reproducible, or incompletely bound vector/model artifacts.
30. Lazy model integrity failure follows the existing quarantine contract.
31. Cancellation/deadline/model-load behavior uses the common runtime terminal-state implementation.
32. Documentation-quality, unit, integration, negative, reproducibility, release, activation, and rollback tests all pass.
33. No Phase 4 reranker, extra supporting-context expansion, Phase 4 table/cross-reference improvement, or high-accuracy warning/refusal evaluation implementation has been pulled into the Phase 3 PR.

## 31. Phase 3 exit artifacts

At merge, the Phase 3 implementation should be able to produce a complete decision/evidence package containing:

- selected embedding model/revision/configuration and complete model-asset identity;
- embedding benchmark report;
- embedding-text schema/configuration;
- byte-identical embedding artifact metadata/hash;
- deterministic row-map identity;
- exact dense backend/metric/configuration;
- RRF configuration;
- query-analysis/classifier rule-set/configuration;
- cache/build identity hashes;
- updated release and runtime retrieval lineage;
- comparative lexical/dense/hybrid evaluation report;
- downstream required-context/material-conflict semantics regression report;
- held-out confirmation gate report;
- cold/warm/model-free performance report;
- release validation result;
- rollback validation result.

These artifacts make the Phase 3 choice auditable and reproducible.

## 32. Handoff to Phase 4

Phase 4 receives a stable shared evidence pipeline with:

- exact/lexical Phase 2 retrieval intact;
- dense chunk retrieval;
- lexical+dense RRF;
- deterministic query analysis/classification;
- complete retrieval-channel provenance;
- inherited deterministic required-context and material-conflict closure;
- strict ordinary Evidence Package behavior already preserved across retrieval modes;
- immutable embedding/vector artifacts;
- release-bound model/configuration/asset identity;
- expanded regression evaluation.

Phase 4 then owns only the current design-defined high-accuracy additions:

- cross-encoder reranking;
- additional supporting-context expansion for high-accuracy retrieval;
- high-accuracy table improvements;
- high-accuracy cross-reference improvements;
- expanded typed-warning and refusal evaluation for high-accuracy retrieval.

Phase 4 does **not** newly introduce ordinary required-context/material-conflict closure or the basic strict Evidence Package contract; Phase 3 inherits and preserves those lower-phase correctness guarantees.

Phase 3 must not pre-implement the Phase 4 additions merely to make its hybrid candidate layer appear more accurate.

## 33. Definition of done

The Phase 3 PR is ready to merge only when:

- the implementation remains within the Phase 3 boundary;
- all repository checks pass on the exact PR head;
- the Phase 3 retrieval and downstream evidence-semantics gates pass on the correctly isolated evaluation data;
- all actionable review comments that are genuinely Phase 3 scope are fixed and replied to;
- all resolved review threads are marked resolved;
- out-of-scope Phase 4 feedback is explicitly deferred rather than implemented;
- reviewers have no further Phase 3 comments on the exact final head;
- the PR description matches the final Phase 3 plan/implementation state;
- the final head is merged into `master` before any later-phase work begins.
