# Phase 3 Implementation Plan: Hybrid Retrieval

**Project:** ClauseSift  
**Phase:** 3 of the design-defined implementation sequence  
**Status:** Implementation plan  
**Primary design authority:** `docs/design.md`  
**Product intent:** `docs/design-brief.md`  
**Design principles:** `docs/design-principles.md`  

## 1. Objective

Phase 3 adds evaluated semantic retrieval to ClauseSift without changing the authority, identity, edition-safety, context-completeness, conflict, citation, release, or interface semantics established by the lower-phase design.

The Phase 3 implementation must deliver:

1. a replaceable embedding-provider contract;
2. an evidence-backed embedding-model selection process;
3. exactly one deterministic release embedding for every persisted chunk;
4. a safe memory-mapped exact dense-search implementation;
5. deterministic lexical+dense reciprocal-rank fusion (RRF);
6. deterministic query preprocessing, analysis, and retrieval-path classification;
7. Phase 3-specific held-out confirmation and retry governance;
8. Phase 3 release/cache/model-asset/lineage integration;
9. expanded regression evaluation proving hybrid retrieval improves recall without weakening exact/lexical and evidence correctness.

Phase 3 does not add cross-encoder reranking or other Phase 4 high-accuracy behavior.

## 2. Blocking lower-phase prerequisite

Current `docs/design.md` assigns the following ordinary correctness baseline to **Phase 2**:

- deterministic required Evidence Graph context closure;
- deterministic material-conflict closure;
- ordinary strict Evidence Package assembly;
- basic Python, CLI, and MCP retrieval interfaces using that evidence contract.

The already merged Phase 2 implementation-plan set predates that design-boundary change and does not yet describe the full current Phase 2 closure/evidence-service implementation. That mismatch is a lower-phase corrective gap.

Therefore:

- Phase 3 must **not** implement that missing Phase 2 work inside this phase;
- Phase 3 must **not** pretend the stale Phase 2 plan already implements it;
- Phase 3 must **not** move ordinary closure to Phase 4;
- a separately reviewed Phase 2 corrective plan/implementation is a **blocking prerequisite for release-capable Phase 3 runtime integration, downstream evidence-semantics confirmation, activation, and Phase 3 completion**.

Offline Phase 3 benchmark/harness work may proceed earlier against immutable canonical chunk fixtures, provided it does not claim a release-capable hybrid evidence path.

Once the corrected Phase 2 baseline exists, Phase 3 consumes it through stable service/catalog contracts.

## 3. Phase boundary

### 3.1 In scope

Phase 3 implements and validates:

- embedding-provider interface and safe provider implementation;
- deterministic `embedding_text` projection;
- multilingual/cross-language engineering embedding benchmark;
- model selection and immutable decision record;
- one vector per persisted chunk;
- fixed v0.1 `embeddings.f16.npy` release artifact;
- deterministic vector row ordering;
- safe NumPy artifact validation and read-only memory mapping;
- exact dense search;
- deterministic dense top-K ordering;
- canonical source/chunk mapping and metadata filtering;
- current-query embedding only at runtime;
- supervised/lazy query-model loading through the common runtime lifecycle;
- lexical+dense deduplication by canonical evidence identity;
- deterministic RRF;
- deterministic query preprocessing and feature extraction;
- deterministic query classification/path resolution;
- Phase 3-specific held-out campaign governance;
- Phase 3 cache, release, model-asset, and lineage identity;
- comparative lexical/dense/hybrid regression evaluation;
- inherited evidence-semantics integration testing after the Phase 2 corrective prerequisite exists;
- cold/warm/model-free performance measurement;
- release validation, activation, and rollback integration.

### 3.2 Out of scope

Phase 3 does not implement:

- the separately owned Phase 2 corrective context/conflict closure work;
- cross-encoder reranking;
- Phase 4 `high_accuracy` reranking;
- Phase 4 supporting-context expansion;
- Phase 4 table/cross-reference improvements;
- Phase 4 expanded warning/refusal evaluation;
- ANN solely because it is conventional;
- a permanent vector database;
- document-level vectors;
- multiple vectors per chunk;
- LLM query classification;
- LLM query rewriting as an authoritative retrieval step;
- generated source facts, relationships, applicability, precedence, citations, or legal/engineering judgments.

Review feedback requiring those items must be deferred to the owning phase rather than expanding this plan.

## 4. Governing invariants

The implementation must preserve all of the following.

1. Original source bytes remain authoritative.
2. Embeddings, dense scores, and fusion scores are retrieval metadata only.
3. Exact and lexical retrieval remain first-class and independently usable.
4. Canonical document/node/chunk/source identities come from lower-phase artifacts, never vector row numbers or text similarity.
5. Editions remain distinct even when text is identical.
6. Metadata filters and exact identity constraints outrank semantic similarity.
7. One persisted chunk maps to exactly one Phase 3 vector row in v0.1.
8. Document-level vectors do not appear in the v0.1 chunk matrix.
9. SQLite insertion order is never vector row identity.
10. Only the current query is embedded at runtime.
11. Equivalent complete build inputs produce byte-identical canonical release artifacts where the design claims reproducibility.
12. Model/provider changes invalidate dependent artifacts and release identity.
13. Query-preprocessing changes are behavior changes and participate in candidate/release/evaluation identity.
14. Fusion does not invent or merge canonical evidence identities.
15. After the corrected Phase 2 prerequisite exists, exact, lexical, and hybrid seeds enter the same required-context/material-conflict/Evidence Package pipeline.
16. Phase 3 does not add properties to the closed Evidence Package schema without an explicit design/schema version change.
17. Immutable `lineage.json` remains query-independent.
18. Request-specific ranks/scores/fusion/context paths are runtime assembly lineage, not release mutation.
19. All normal work remains bounded, cancelable, deadline-aware, and subject to the common runtime admission/quarantine contract.
20. Quality gates precede performance optimization.
21. The exact production query-preprocessing identity is frozen and implemented before embedding-model or RRF selection begins; changing it invalidates those selection reports.
22. Phase 3 release gates are evaluated on the final frozen user-facing Phase 3 retrieval paths, never satisfied by substituting a diagnostic dense-only or lower-phase lexical result.

## 5. Deliverables

### 5.1 Build-time deliverables

- embedding provider abstraction;
- deterministic embedding-text builder;
- embedding benchmark harness and report;
- selected-model decision artifact;
- chunk embedding builder;
- deterministic vector row-map validator;
- `embeddings.f16.npy`;
- Phase 3 release-manifest fields;
- complete local model-asset identity table/digest;
- Phase 3 cache keys;
- query-independent Phase 3 `lineage.json` additions;
- Phase 3 evaluation/campaign ledger;
- release validation gates.

### 5.2 Runtime deliverables

After the Phase 2 corrective prerequisite exists:

- query preprocessing service;
- lazy query embedder;
- exact dense index/search backend;
- dense-hit mapper;
- metadata-filter application;
- lexical+dense deduplicator;
- RRF fusion service;
- deterministic query analyser/classifier;
- retrieval-path resolver;
- shared-service integration with the corrected Phase 2 evidence pipeline;
- request-scoped retrieval/assembly provenance using the existing Evidence Package schema;
- cold/warm/model-free diagnostics.

### 5.3 Decision/audit artifacts

Retain versioned records of:

- all embedding candidates evaluated;
- exact model/provider revisions and assets;
- benchmark corpus/split identities;
- benchmark configuration;
- per-stratum metrics;
- selected and rejected candidates with rationale;
- candidate-pool and RRF configurations;
- query-preprocessing identity;
- query-classifier identity;
- Phase 3 held-out campaign preregistration and results;
- final release-gate decision.

## 6. Proposed module boundaries

The exact filenames may evolve, but responsibilities must stay separated conceptually:

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
    ├── query_classification.py
    └── campaign.py
```

Builder code owns document-dependent embeddings. Runtime code owns only the current-query embedding. Dense backends return typed candidates, never backend-native objects to public interfaces.

## 7. Work package A — Freeze Phase 3 contracts

Before selecting a model, define strict versioned contracts for:

- embedding provider metadata;
- `embedding_text` projection;
- vector row ordering;
- dense candidate records;
- fusion candidate records;
- query preprocessing;
- query analysis/classification;
- Phase 3 held-out campaign ledger;
- Phase 3 release/cache/lineage dependencies.

The **production query-preprocessing contract is implemented and frozen at this stage**, before model/RRF selection. Query analysis/classification may be implemented later, but the byte transformation that feeds query embedding and any model/RRF selection harness cannot be provisional after selection starts.

### 7.1 Embedding provider

The provider contract must expose enough deterministic metadata to bind build and query behavior:

- provider implementation ID/version;
- model ID;
- exact model revision;
- dimensions;
- provider output dtype;
- normalization behavior;
- input-size limit;
- tokenizer/processor identity;
- complete local asset identity or explicitly approved external request identity;
- configuration hash.

Model-native objects stay inside the provider implementation.

### 7.2 Dense candidate

A dense candidate resolves to existing lower-phase identity and carries only retrieval metadata:

- `document_id`;
- `chunk_id`;
- `source_id`;
- dense rank;
- dense score;
- release/vector artifact identity;
- internal row index only where needed for diagnostics.

The row index is not a public evidence ID.

### 7.3 Fusion candidate

A fused candidate contains:

- canonical document/chunk/source identity;
- participating channels;
- channel ranks/scores;
- deterministic fused score/rank;
- RRF configuration identity;
- resolved retrieval path;
- no generated evidence text.

## 8. Work package B — Deterministic embedding text

Define one canonical `embedding_text` for each lower-phase chunk using only deterministic, approved inputs such as:

- normalized chunk text;
- document code where useful;
- clause/hierarchy context;
- deterministic headings;
- deterministic table headers/units;
- explicitly admitted safe document metadata.

It must exclude:

- filesystem paths;
- timestamps;
- random IDs;
- query-dependent content;
- reviewer comments;
- generated interpretations;
- text from another edition merely because it is similar.

Freeze:

- `embedding_text_schema_version`;
- transformation/configuration hash;
- Unicode normalization behavior;
- deterministic field ordering.

Cache identity uses the design-defined ordered chunk tuple `(document_id, canonical_order, chunk_id, embedding_text_hash)` plus the complete Section 25 dependency set.

Tests must prove stable bytes, correct invalidation, edition separation, and no unrelated-document over-invalidation beyond the declared dependency graph.

## 9. Work package C — Embedding benchmark

No model is selected by popularity or generic benchmark reputation.

**Every benchmark query passes through the already frozen production query-preprocessing implementation and records its exact preprocessing identity.** A model-selection report produced with another preprocessing identity is not reusable.

### 9.1 Candidate shortlist

Benchmark a small replaceable set that can realistically support:

- English technical text;
- Chinese technical text;
- English↔Chinese retrieval;
- HVAC terminology;
- fire-safety terminology;
- short clauses;
- longer contextual chunks.

### 9.2 Required strata

Include at minimum:

- English standards;
- Chinese standards;
- cross-language queries;
- HVAC terminology;
- fire-safety terminology;
- identifiers/product models;
- numbers/units;
- synonyms;
- negation;
- exception queries;
- near-duplicate clauses across editions;
- similar wording with different normative modality;
- unit-equivalent values;
- different values with similar wording;
- wrong-edition semantic hard negatives;
- lexical-perfect cases;
- dense-complementarity cases.

### 9.3 Protocol

For each candidate:

1. freeze model/provider/asset/configuration identity;
2. use the frozen production query-preprocessing implementation/identity for every benchmark query;
3. embed the same immutable benchmark chunk set;
4. verify deterministic row mapping;
5. verify canonical release-byte reproducibility under the admitted build environment;
6. run exact dense search;
7. measure Recall@5 and Recall@20 plus secondary ranking diagnostics;
8. report every required stratum;
9. measure build throughput and artifact size;
10. measure cold load, warm query embedding, and dense search separately;
11. measure peak RSS;
12. retain rejected candidate results.

Selection priority is retrieval correctness, hard-negative/cross-language robustness, reproducibility/safe loading, runtime feasibility, then speed/packaging simplicity.

Any behavior-bearing preprocessing change after selection invalidates the model-selection evidence and requires rerunning model selection before the changed candidate can progress.

## 10. Work package D — Offline embedding artifact

### 10.1 Row order

Rows are exactly ordered by:

```text
(document_id, chunks.canonical_order, chunk_id)
```

Require one-to-one mapping with all persisted chunks, no duplicates, no missing rows, no sentinel rows, no document rows, and no reliance on SQLite physical order.

### 10.2 Fixed v0.1 format

The release artifact is exactly:

```text
embeddings.f16.npy
```

with:

- rank two;
- actual and declared dtype `float16`;
- finite numeric values;
- no object/structured dtype;
- no pickle;
- declared dimensions matching every row;
- normalized vectors when required by the selected metric.

Provider output may be higher precision internally, but canonical conversion to `float16` is a versioned build transform before sealing the release.

### 10.3 Manifest metadata

Bind at minimum:

- artifact relative path;
- byte size and SHA-256;
- scope `chunk`;
- row count;
- dimensions;
- dtype;
- normalization;
- row-order version;
- model/provider identity;
- complete model-asset identity;
- embedding configuration;
- embedding-text version;
- artifact schema version.

## 11. Work package E — Safe artifact validation

Independent validation must reopen the artifact rather than trusting builder memory.

Use bounded semantics equivalent to:

```python
numpy.load(
    path,
    mmap_mode="r",
    allow_pickle=False,
    max_header_size=10000,
)
```

Validate:

- checksum/size;
- bounded header;
- rank/dtype;
- finite values;
- normalization invariant;
- manifest dimensions/row count;
- complete row-map reconstruction;
- read-only behavior;
- supported schema/model/provider identity;
- complete model asset binding;
- query-independent lineage artifact identity.

Any mismatch blocks activation.

## 12. Work package F — Exact dense retrieval

The initial backend uses read-only NumPy memory mapping and exact scoring. ANN is not introduced until measured scale proves it necessary and recall loss is explicitly evaluated.

### 12.1 Query vector validation

Before scoring:

- dimensions match release dimensions;
- values are finite;
- normalization contract holds;
- query model/provider/assets/configuration exactly match release identity;
- zero-norm vectors fail visibly.

### 12.2 Deterministic top-K

Use a versioned total order independent of backend/hash iteration, conceptually:

```text
(score descending,
 document_id,
 chunk canonical_order,
 chunk_id,
 source_id)
```

### 12.3 Metadata filtering

Semantic similarity never substitutes document/edition/jurisdiction/status/type identity. Filter semantics must match the lower-phase service exactly regardless of whether filtering happens before or after score calculation.

A vector row that cannot map one-to-one to catalog identity is a release-integrity failure, not a skippable hit.

## 13. Work package G — Query preprocessing and embedding

Only the current query is embedded at runtime.

The **production query-preprocessing implementation was already frozen before model selection** under Work package A. This work package integrates that exact implementation into runtime query embedding; it does not define or retune it after model/RRF selection.

Query preprocessing is deterministic and release-bound. It must not silently:

- remove negation;
- drop numbers/units;
- replace identifiers with generated synonyms;
- rewrite with an LLM;
- add hidden answer content;
- use a different path in evaluation and production.

The detailed identity/invalidation contract is defined in `phase-3-query-preprocessing-identity.md`.

The lazy model loader reuses the common supervised worker, deadline, cancellation, single-flight, safe-asset, and quarantine contracts. Phase 3 does not create a second timeout or terminal-state implementation.

## 14. Work package H — Reciprocal-rank fusion

Hybrid mode combines lexical and dense ranked candidate lists.

### 14.1 Deduplication

Deduplicate by canonical source/chunk identity, never normalized-text equality. Identical wording in different editions remains distinct.

### 14.2 RRF

The logical unweighted contribution is:

```text
1 / (rrf_k + rank)
```

with one-based ranks and a versioned, benchmark-selected `rrf_k`.

Benchmark bounded candidates for:

- lexical pool size;
- dense pool size;
- final fused pool size;
- `rrf_k`;
- channel weighting only if explicitly admitted and evidence shows plain RRF is insufficient.

RRF/candidate-pool selection uses the same already-frozen production query-preprocessing identity used by model selection. A preprocessing change invalidates the RRF-selection report as well as the model-selection report.

### 14.3 Deterministic ordering

Freeze a complete tie chain using fused score, contributing rank(s), canonical document/chunk/source identity, and no hash-map/backend-native order.

## 15. Work package I — Query analysis and path classification

Use deterministic rules to detect:

- document codes;
- clause numbers;
- editions;
- product model numbers;
- numbers/units;
- document types;
- jurisdiction/discipline terms;
- version-comparison intent;
- source-page intent;
- residual natural-language dominance.

Internal outcomes include at least:

- `exact-dominant`;
- `hybrid-natural-language`;
- `ambiguous`;
- `later-phase-high-accuracy-intent`.

Rules choose channels only. They cannot determine legal authority, applicability, normative force, conflict resolution, or whether required context may be dropped.

Exact-dominant requests preserve exact protections. Explicit hybrid requests fail visibly when dense capability is unavailable; they are not silently relabelled lexical-only results.

## 16. Work package J — Phase 3 held-out campaign

Phase 3 has its own evaluation-governance contract; the Phase 2 retry policy is not implicitly extended.

### 16.1 Data separation

Keep distinct:

- development data;
- model-selection data;
- optional non-decisional screening reserves;
- one final confirmation split;
- reproduction-only replays.

### 16.2 Preregistration

Before final confirmation, persist:

- campaign ID;
- complete frozen candidate identity hash;
- gate families/strata;
- sample-size rules;
- final split identity/hash;
- any screening reserve identities/order;
- review/corpus policy versions.

### 16.3 Decisive-use rules

- the final confirmation split has one decisive use while unseen;
- after observation it is retired for materially changed candidates;
- exact same candidate may replay it only as `reproduction_only`;
- reproduction does not create new independent evidence or reset failure;
- a changed candidate requires fresh decisive data;
- at most two preregistered screening reserves are allowed and they are non-decisional;
- no reserve cherry-picking;
- final-confirmation failure closes the campaign;
- a later campaign requires documented remediation, a new candidate/campaign ID, and genuinely fresh independently reviewed confirmation data.

### 16.4 Ledger

Record campaign/candidate/split identity, role, observed/retired state, first decisive observation, metric results, outcome, and successor/predecessor links. Release validation rejects contradictory or reused decisive evidence.

Tests cover all failure/replay/rotation boundaries, including query-preprocessing-only candidate changes.

## 17. Work package K — Regression evaluation

### 17.1 Blocking gates are bound to production paths

The Phase 3 Wilson gates are **not generic metrics that any retrieval slice may satisfy**. They are release-authorizing gates for the frozen user-facing Phase 3 paths.

For independently labelled applicable cases, the **final frozen classifier-selected production path**—including the exact production query preprocessing, deterministic query analysis/classification, whichever exact/lexical/dense channels it resolves, RRF where selected, metadata filters, and the inherited lower-phase evidence pipeline—must satisfy:

- Recall@20 one-sided 95% Wilson lower bound >= 98%;
- Top-5 one-sided 95% Wilson lower bound >= 95%.

Because `hybrid` is also an explicit user-selectable Phase 3 mode, the **frozen explicit `hybrid` path** must independently satisfy the same two gates on the applicable hybrid-mode confirmation cases.

Dense-only retrieval remains a diagnostic/component benchmark unless a future public contract exposes it as an independent user-facing mode; dense-only results cannot authorize Phase 3 release by substituting for a failing classifier-selected or explicit-hybrid path. Lower-phase exact/lexical gates remain independently required by their owning phase and likewise cannot be counted as Phase 3 path-gate evidence.

Use at least 150 applicable cases for each 98% gate and at least 60 for each 95% gate, expanding samples as needed for critical strata. Where the classifier-selected and explicit-hybrid populations overlap, report them as separately named gate families with explicit denominators rather than pooling them ambiguously.

Always report numerator, denominator, point estimate, lower bound, corpus/split identity, complete candidate identity, and the exact evaluated production-path identity.

### 17.2 Comparative gates

Compare:

- lexical vs dense;
- lexical vs hybrid;
- best lower-phase path vs classifier-selected Phase 3 path.

Do not permit global-average improvement to hide critical regressions in exact document codes, exact clauses, product models, numbers/units, wrong-edition hard negatives, negation, or exceptions.

The comparative tables are diagnostic/complementary evidence; they do not replace the blocking production-path gates in Section 17.1.

### 17.3 Query-classifier evaluation

Create independent expected routing labels and report a confusion matrix. Require zero known cases where deterministic exact anchors are discarded and produce wrong-document/wrong-edition routing.

### 17.4 Downstream evidence semantics

After the corrected Phase 2 prerequisite exists, verify hybrid seed selection does not change/drop:

- required parent scope;
- applicability;
- required definitions/dependencies/exceptions;
- required table context;
- material conflict sides;
- typed context-limit behavior;
- deterministic citations;
- source/document/edition identity;
- Python/CLI/MCP evidence semantics.

## 18. Work package L — Cache and release identity

`docs/design.md` Section 25 is the sole authoritative cache-dependency contract.

Embedding invalidation includes the complete ordered chunk/text identity, embedding scope/row order, exact model/provider/assets, embedding configuration, dependency lock, and toolchain fingerprint where declared.

Vector invalidation includes embedding artifact hash, backend/version, metric/configuration, dependency lock, and toolchain identity where declared.

Phase 3 release/build identity additionally binds behavior-bearing:

- RRF configuration;
- query-preprocessing identity;
- query-analysis/classifier identity;
- candidate-pool configuration;
- Phase 3 gate-result identities.

Cache hits are allowed only when the complete declared dependency set is unchanged.

## 19. Work package M — Evidence Lineage

### 19.1 Immutable `lineage.json`

The sealed release lineage contains only query-independent source/build/release provenance and artifact/configuration references.

Phase 3 adds as applicable:

- embedding-text transformation identity;
- embedding provider/model/revision/configuration and bound assets;
- embedding artifact hash;
- vector backend/metric/configuration;
- vector artifact hash/exact-backend declaration;
- lexical-index artifact identity;
- RRF configuration identity when release-bound;
- query-preprocessing identity when release-bound;
- query-analysis/classifier configuration identity when release-bound.

It must not contain query text, request IDs, candidate ranks/scores, fusion results, selected seed sets, or query-specific context paths.

### 19.2 Runtime Evidence Package provenance uses the existing closed schema

Phase 3 does not add new Evidence Package properties.

For each retrieval channel, use only the existing `assembly.retrievals[]` fields defined by `docs/design.md`:

- `channel`;
- `channel_version`;
- `configuration_sha256`;
- `artifact_set_sha256`;
- `candidate_rank`;
- `score`.

When RRF runs, use only the existing `assembly.fusion` fields:

- `algorithm_id`;
- `configuration_sha256`;
- `rank`;
- `score`.

The package-level `retrieval_mode` records the resolved public mode. Do not add classifier-identity or per-channel RRF-contribution fields to closed objects unless the detailed design first introduces a versioned schema change.

Required context/conflict provenance remains in existing `selection_roles`, `seed_source_ids`, `context_completeness`, `context_paths`, and `conflict_reasons` fields.

## 20. Work package N — Runtime capability and failure behavior

A release is dense-capable only if every required Phase 3 artifact/configuration passes release validation. A **release-capable hybrid evidence service** additionally requires the corrected Phase 2 context/conflict/evidence baseline.

Explicit hybrid requests fail visibly for missing/incompatible dense artifacts, model assets, backend, model-load timeout, vector mismatch, release quarantine, or missing corrected Phase 2 prerequisite.

`auto` may choose only capabilities present in the runtime and active release and follows the design-defined typed warning/fallback rules.

## 21. Work package O — Reproducibility, security, and performance

### 21.1 Reproducibility

Require:

- deterministic row map;
- byte-identical canonical `embeddings.f16.npy` for the same complete admitted build identity;
- stable dense ranking;
- stable RRF ordering;
- stable classifier output;
- stable release validation decision;
- rollback restores matching catalog/vector/model/configuration/lineage state.

### 21.2 Security/privacy

Retain local-first behavior, exhaustive local model-asset hashing, safe non-executable formats/loaders, no arbitrary pickle/model code hooks, no default runtime network access, no sensitive query/source/path leakage, and common admission/cancellation/quarantine behavior.

### 21.3 Performance

Only after quality gates pass, report separately:

- embedding build throughput/artifact size;
- exact dense-search latency excluding query embedding;
- warm query-embedding latency;
- cold model-load latency;
- warm/cold hybrid latency;
- lexical-only latency;
- context/conflict closure latency separately where practical;
- peak RSS and model-load incremental RSS;
- corpus-size/candidate-pool sensitivity.

Do not introduce ANN merely because a synthetic larger corpus is slower; record the measured threshold for future evaluation.

## 22. Test plan

### 22.1 Unit

Test:

- embedding-text determinism;
- production query-preprocessing determinism before model/RRF selection;
- model/provider/asset identity;
- row order;
- float16 conversion;
- matrix header/shape/dtype/finite/normalization checks;
- query-vector validation;
- exact dense search and tie-breaking;
- metadata filters;
- dense mapping;
- RRF/dedup/tie-breaking;
- query features/classification;
- Phase 3 campaign ledger/state transitions;
- Section 25 cache keys;
- closed Evidence Package retrieval/fusion serialization;
- final classifier-selected production-path gate accounting;
- explicit-hybrid production-path gate accounting.

### 22.2 Integration

After the corrected Phase 2 prerequisite exists, test:

- complete Phase 3 release build;
- repeated byte-identical embedding build;
- fresh-process read-only mmap;
- cold/warm query model behavior;
- exact mode remains model-free;
- hybrid retrieval through the shared evidence pipeline;
- wrong-edition hard negatives;
- complete required context/conflicts;
- Python/CLI/MCP equivalence;
- corruption/quarantine;
- activation and rollback.

### 22.3 Negative/boundary

Include:

- zero-norm/wrong-dimension/NaN/Inf query vectors;
- missing/extra/duplicate vector rows;
- non-float16/object/structured dtype;
- >10,000-byte NumPy header;
- writable mmap attempt;
- same text in different editions;
- dense empty after filters;
- explicit hybrid without capability/prerequisite;
- model-load timeout/cancellation/deadline;
- ambiguous exact+natural-language query;
- false identifier-looking token;
- negation;
- numeric/unit semantic hard negatives;
- context-limit overflow;
- one-sided conflict seed;
- observed confirmation split reused by changed candidate;
- second decisive final confirmation in one campaign;
- reproduction-only replay incorrectly treated as new release evidence;
- changed preprocessing identity with stale model/RRF selection report;
- final classifier-selected path failing while dense-only passes;
- explicit hybrid path failing while another evaluated slice passes.

## 23. Implementation sequence

1. Merge/validate the separate Phase 2 corrective prerequisite before release-capable Phase 3 integration or final confirmation.
2. Freeze Phase 3 schemas/interfaces, including the complete production query-preprocessing schema/rules/configuration and test fixtures.
3. Implement and freeze the deterministic production query-preprocessing path; record its identity and make the same implementation available to benchmark harnesses.
4. Implement deterministic `embedding_text` projection.
5. Implement embedding-provider and model-asset identity.
6. Build the embedding benchmark harness around the frozen production preprocessing path.
7. Benchmark/select/freeze the embedding model on selection data using that exact preprocessing identity.
8. Build canonical chunk embeddings.
9. Build/validate deterministic row map.
10. Implement bounded safe artifact loader.
11. Implement exact dense backend and canonical hit mapping.
12. Implement lazy current-query embedding by integrating the already frozen production preprocessing path.
13. Implement lexical+dense deduplication and RRF.
14. Benchmark candidate pools/RRF on selection data using the same frozen production preprocessing identity; any preprocessing change invalidates both model and RRF selection and returns to step 3.
15. Implement deterministic query analysis/classification on top of the already frozen preprocessing path.
16. Integrate classifier-selected/hybrid seeds with the corrected Phase 2 evidence service.
17. Implement Section 25 invalidation and Phase 3 release identity.
18. Implement query-independent lineage additions and closed-schema runtime provenance.
19. Add unit/integration/negative/reproducibility/security tests.
20. Add comparative retrieval and downstream evidence-semantics evaluation.
21. Freeze the complete final production candidate identity, including preprocessing, model, dense backend, candidate pools, RRF, and classifier configuration.
22. Preregister the Phase 3 campaign and the separately named classifier-selected and explicit-hybrid blocking gate families/final confirmation cases.
23. Run the single final decisive confirmation; both the final classifier-selected production path and explicit-hybrid path must meet their applicable Section 17.1 gates.
24. Produce final benchmark/gate/performance/release reports.
25. Validate activation and rollback.
26. Record Phase 4 handoff without implementing Phase 4.

## 24. Acceptance criteria

Phase 3 is complete only when:

1. the separate Phase 2 corrective prerequisite is merged and validated;
2. the embedding provider is replaceable and model-native objects do not leak into canonical/public contracts;
3. the production query-preprocessing path is implemented/frozen before model or RRF selection and is identical between selection, final confirmation, and runtime;
4. model selection is supported by project-specific multilingual/hard-negative evidence bound to that exact preprocessing identity;
5. every persisted chunk has exactly one vector and no non-chunk vector rows exist;
6. vector row order is exactly the versioned canonical order and independently reconstructable;
7. the v0.1 artifact is exactly safe read-only `float16` `embeddings.f16.npy` with bounded header/pickle-disabled loading;
8. complete model/provider/asset identity is bound into build/release/runtime compatibility;
9. deterministic query preprocessing is release-bound and included in frozen candidate identity;
10. identical complete build identity produces byte-identical canonical embedding bytes/hash;
11. exact dense search and top-K ordering are deterministic;
12. dense hits map one-to-one to canonical lower-phase identity;
13. metadata/edition safety is preserved;
14. RRF is versioned, benchmark-selected, deterministic, canonical-ID based, and selected using the same frozen production preprocessing identity;
15. query analysis/classification is deterministic and non-LLM;
16. exact-style queries retain exact/lexical protections;
17. natural-language queries execute the hybrid path when capability exists;
18. explicit hybrid failures are visible, not silently relabelled fallbacks;
19. the **final frozen classifier-selected production path** passes Recall@20 with one-sided 95% Wilson lower bound >= 98% and Top-5 with lower bound >= 95% on its applicable final confirmation cases;
20. the **frozen explicit `hybrid` path** independently passes the same two Wilson gates on applicable explicit-hybrid final confirmation cases;
21. dense-only/component results and lower-phase lexical/exact results cannot substitute for either failing Phase 3 production-path gate;
22. each gate reports numerator, denominator, point estimate, lower bound, corpus/split identity, candidate identity, and evaluated path identity with required sample sizes/stratification;
23. critical exact/numeric/identifier/wrong-edition/negation strata do not regress unacceptably;
24. the Phase 3 campaign retires observed decisive splits, restricts identical-candidate replay to reproduction, has one final decisive confirmation per campaign, and requires fresh decisive data after failed campaigns;
25. Section 25 cache/release invalidation covers every behavior-bearing Phase 3 input;
26. immutable `lineage.json` contains only query-independent Phase 3 transformations/artifacts/configuration identities;
27. request-specific retrieval provenance uses only the existing closed `assembly.retrievals[]`, `assembly.fusion`, package-level `retrieval_mode`, and existing context/conflict fields;
28. no unversioned Evidence Package fields are introduced;
29. hybrid retrieval composes with corrected Phase 2 required context/conflict semantics without weakening citations/source/edition identity;
30. corruption/model integrity failure follows fail-closed/quarantine semantics;
31. cancellation/deadline/model loading uses the common runtime terminal-state implementation;
32. documentation, unit, integration, negative, reproducibility, release, activation, and rollback checks pass;
33. no Phase 2 corrective implementation detail is pulled into Phase 3;
34. no Phase 4 reranking/supporting-context/table/xref/high-accuracy warning/refusal implementation is pulled into Phase 3.

## 25. Phase 3 exit artifacts

The merged plan requires the implementation to produce:

- frozen production query-preprocessing identity and implementation evidence;
- selected model/provider/asset decision record;
- embedding benchmark report bound to that preprocessing identity;
- embedding-text identity;
- canonical embedding artifact metadata/hash;
- row-map identity;
- dense backend/metric identity;
- RRF identity and selection report bound to the same preprocessing identity;
- query-analysis/classifier identity;
- Section 25 cache/build identities;
- query-independent Phase 3 lineage update;
- request-scoped retrieval/fusion assembly provenance using the closed schema;
- lexical/dense/hybrid comparative report;
- final classifier-selected and explicit-hybrid production-path gate reports;
- downstream context/conflict regression report;
- Phase 3 campaign ledger and final confirmation report;
- cold/warm/model-free performance report;
- release-validation and rollback evidence.

## 26. Handoff to Phase 4

After the corrected Phase 2 prerequisite and Phase 3 gates are satisfied, Phase 4 receives:

- exact/lexical retrieval intact;
- dense chunk retrieval;
- lexical+dense RRF;
- deterministic query preprocessing/analysis/classification;
- closed-schema retrieval provenance;
- ordinary Phase 2 required-context/material-conflict closure;
- strict ordinary Evidence Package behavior;
- immutable embedding/vector artifacts;
- release-bound model/configuration identity;
- expanded evaluation evidence.

Phase 4 then adds only the high-accuracy work assigned by current `docs/design.md`:

- cross-encoder reranking;
- supporting-context expansion;
- improved tables/cross-references;
- expanded high-accuracy typed-warning/refusal evaluation.

## 27. Definition of done

The Phase 3 plan PR is ready to merge only when:

- all repository checks pass on the exact final head;
- all actionable Phase 3 review comments are fixed, replied to, and resolved;
- reviewers report no further Phase 3 findings on the exact final head;
- the PR description matches the final plan set;
- the Phase 2 corrective prerequisite is clearly recorded without being implemented inside this PR;
- Phase 4 work remains deferred;
- the final head is merged before beginning the next implementation-plan PR.
