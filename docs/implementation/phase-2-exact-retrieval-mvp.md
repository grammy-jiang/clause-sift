# Phase 2 Implementation Plan: Exact Retrieval MVP

**Project:** ClauseSift  
**Phase:** 2 of the design-defined implementation sequence  
**Status:** Canonical current-design implementation plan  
**Primary design authority:** `docs/design.md`  
**Product intent:** `docs/design-brief.md`  
**Design principles:** `docs/design-principles.md`

## 1. Objective

Phase 2 builds the first complete ordinary ClauseSift evidence runtime.

Its candidate selection remains deliberately simple and deterministic: exact identifiers, exact clause lookup, metadata filters, and lexical retrieval. The evidence returned from those seeds, however, must already satisfy the current design's ordinary correctness contract.

Phase 2 therefore delivers:

1. package/workspace/release infrastructure;
2. approved manifests and source verification;
3. production parser routing and canonical document model;
4. evidence vocabulary/classification/page provenance;
5. standards-aware chunks and exact lookup sets;
6. SQLite Evidence Graph/catalog persistence;
7. lexical indexing and exact/lexical seed retrieval;
8. deterministic citations and immutable source/build lineage;
9. release-validated structural/semantic relationship identities;
10. deterministic **required Evidence Graph context closure**;
11. deterministic **material-conflict closure to a fixed point**;
12. strict ordinary **Evidence Package** serialization;
13. one shared Python/CLI/MCP evidence service;
14. immutable validated release assembly, activation, and rollback;
15. decisive Phase 2 retrieval/classification/context/conflict/evidence gates.

Phase 2 does **not** implement Phase 3 embeddings/vector/RRF retrieval or Phase 4 cross-encoder reranking/supporting-context high-accuracy enhancements.

## 2. Canonical Phase 2 plan set

This main plan orchestrates the detailed Phase 2 appendices. Read them together with current `docs/design.md`.

Existing detailed appendices remain normative for their subject areas, including:

- `phase-2-release-gates.md` — current Phase 2 decisive/evidence release gates;
- `phase-2-canonical-id-migration.md` — canonical-ID migration before scoring;
- `phase-2-held-out-retry-policy.md` — decisive-evidence retirement/retry governance for all current Phase 2 gate families;
- `phase-2-release-lifecycle-guardrails.md` — finite campaign/lifecycle/activation guardrails;
- `phase-2-mcp-protocol-conformance.md` — JSON-RPC/MCP framing, cancellation, terminal-state conformance;
- `phase-2-mcp-admission-budgets.md` — request/page working-set admission;
- `phase-2-lineage-release-contract.md` — immutable source/build lineage and release identity;
- `phase-2-mcp-wire-resources.md` — current context-complete Phase 2 MCP tools/resources;
- `phase-2-contract-clarifications.md` — canonical URI/lineage clarifications;
- `phase-2-required-context-closure.md` — required graph traversal/materialization/bounds;
- `phase-2-material-conflict-closure.md` — conflict records/covers/fixed-point closure;
- `phase-2-evidence-service.md` — final ordinary Evidence Package/shared service;
- `phase-2-current-design-correction.md` — audit map from the older boundary to this canonical current plan.

Where an older appendix contains a statement explicitly superseded by one of the current corrective documents, the current design/corrective contract wins.

## 3. Phase boundary

### 3.1 In scope

Phase 2 implements and validates:

- Python package/bootstrap and dependency profiles;
- local workspace initialization and path safety;
- human-reviewed manifest schema, safe loading, approval binding, source hashing/change detection;
- manifest relations and edition-safe document identities;
- production integration of selected Phase 1 parser routes, comparison, OCR policy, and fail-closed parser gates;
- canonical Evidence Graph node model;
- exact evidence vocabulary and classification provenance;
- canonical hierarchy/sequence relationships;
- page provenance and source-span/box mappings;
- standards-aware chunks, memberships, stable IDs, exact clause lookup sets;
- semantic cross-reference occurrence extraction/resolution and stable occurrence/edge identity;
- SQLite catalog schema/integrity for documents, nodes, chunks, sources, relationships, conflicts, lineage references, and release metadata;
- lexical-engine benchmark/selection/indexing;
- exact and lexical direct seed selection;
- metadata filters with edition/status safety;
- deterministic citations;
- deterministic required-context traversal;
- deterministic conflict build records and canonical position source covers;
- runtime graph/conflict least fixed point;
- strict source-backed evidence and metadata-only context-target projection;
- strict conflict projection;
- typed warnings/completeness/error routing;
- one central Evidence Package serializer;
- shared Python evidence API;
- context-complete CLI retrieval;
- context-complete MCP evidence tools/resources;
- metadata/list/page/release surfaces;
- immutable lineage/release assembly;
- read-only startup validation;
- atomic activation/rollback;
- Phase 2 held-out and deterministic release gates;
- protocol/admission/cancellation/security/failure-injection suites.

### 3.2 Out of scope

Phase 2 does not implement:

- chunk embeddings;
- vector search;
- embedding-model selection;
- query embedding;
- lexical+dense RRF/fusion;
- semantic/hybrid seed retrieval;
- cross-encoder reranking;
- Phase 4 high-accuracy reranking;
- Phase 4 additional supporting-context expansion for ordinary high-accuracy answers;
- Phase 4 table/cross-reference high-accuracy improvements beyond ordinary required correctness;
- Phase 4 expanded high-accuracy warning/refusal evaluation;
- ANN solely because it is conventional;
- LLM-generated authoritative relationships/classifications/conflict decisions;
- engineering/legal conclusions absent from approved source/rules.

## 4. Governing invariants

Phase 2 must preserve all of the following.

1. Original source bytes and approved manifest facts remain authoritative.
2. Document/edition/node/chunk/source identities are canonical and never replaced by text similarity.
3. SQLite physical row order is never semantic identity.
4. Parser uncertainty and unresolved references remain visible/fail according to release tier.
5. Exact clause lookup never substitutes another edition or fuzzy clause.
6. Lexical ranking chooses seeds only; ranking cannot erase required context/conflicts.
7. Required context follows only release-validated typed relationships and a closed versioned rule set.
8. Material conflicts are n-ary derived release records, not a `conflicts_with` graph shortcut.
9. No rank/model/recency/authority metadata chooses conflict precedence without an approved rule.
10. Required graph and conflict closure form one deterministic bounded least fixed point.
11. Required evidence is never silently truncated.
12. Empty structural context targets never become fabricated source evidence.
13. Immutable `lineage.json` remains query-independent; request assembly lineage is added at runtime.
14. Evidence Package/root/item/lineage/conflict/warning objects remain closed schemas.
15. Python, CLI, and MCP are projections of one evidence service.
16. A failed candidate never mutates the active release.
17. Held-out decisive evidence is a gate, not an optimizer.
18. Performance optimization follows correctness gates.

## 5. Recommended module boundaries

A practical implementation may use:

```text
src/clausesift/
├── config/
├── model/
├── builder/
│   ├── manifests/
│   ├── parsers/
│   ├── canonical/
│   ├── page_provenance/
│   ├── chunking/
│   ├── references/
│   ├── context/
│   ├── conflicts/
│   ├── catalog/
│   ├── lexical/
│   ├── lineage/
│   ├── reports/
│   ├── cache/
│   └── release/
├── runtime/
│   ├── catalog/
│   ├── query/
│   ├── retrieval/
│   ├── context/
│   ├── conflicts/
│   ├── evidence/
│   └── release.py
├── mcp/
└── evaluation/
```

Exact filenames may differ. Mandatory boundaries:

- build-only parser/OCR modules are absent from base runtime startup imports;
- parser-native objects never leak into catalog/runtime contracts;
- relationship/context/conflict compilation is deterministic and release-scoped;
- runtime traverses only validated release artifacts;
- adapters never reimplement SQL/traversal/conflict/serialization logic;
- release validation is independent of build mutation.

## 6. Work package A — Package, workspace, and dependencies

Implement distribution/import/CLI naming and versioned dependency profiles.

The base runtime must start against a prepared Phase 2 release without importing heavy parser/OCR build-only packages.

Workspace initialization is idempotent, does not overwrite approved data, and uses containment/symlink/reparse/regular-file safety checks.

Proprietary source documents are never packaged in the Python distribution.

## 7. Work package B — Manifest governance and source approval

Implement the closed current manifest schema and safe YAML loading.

Validate exact lowercase SHA-256 syntax and every human-readable exact key before/after its field-specific normalization.

Maintain independent:

- raw manifest bytes hash for forensic lifecycle history;
- schema-normalized manifest content hash for semantic approval/build identity.

Every build revalidates approved content hash plus exact source hash/size.

Semantic manifest/source changes require renewed approval; formatting-only manifest changes do not alter semantic release identity.

Manifest-owned identity/status/jurisdiction/discipline/normative facts cannot be changed by parser/ranker/model output.

## 8. Work package C — Parser routing and canonical model

Consume Phase 1 parser-neutral routes and comparison/OCR policy.

Every document has one canonical primary route. Critical-tier documents use the required independent comparator and release-blocking comparison policy.

No field-level merge silently combines parser outputs.

Build the canonical node tree, stable node IDs, exact evidence vocabulary/classification records, and complete provenance.

Unsupported node/classification values remain explicit or block according to design; they are never promoted to a stronger value by convenience.

## 9. Work package D — Page provenance and source spans

Persist deterministic node-to-page mappings and optional validated boxes.

Coordinate incompleteness is represented explicitly; it does not erase valid source text.

Later source/chunk citations and Evidence Lineage derive page projections by exact intersection with validated contributed node spans.

The central serializer independently verifies page/citation projections.

## 10. Work package E — Standards-aware chunks and exact lookup

Construct deterministic chunks preserving:

- original/normalized/search/embedding text projections where the canonical schema reserves them;
- complete chunk-to-node membership and member order;
- chunk canonical order;
- one canonical source identity per source row;
- exact contributed node byte intervals.

Exact clause lookup materializes the complete Section 14.1 source set for the exact document/clause and no other edition.

Chunk IDs and source IDs are stable under byte-identical deterministic rebuilds.

## 11. Work package F — Relationship occurrence and Evidence Graph compilation

Compile structural `contains`/`precedes` relationships from validated canonical structure.

Extract and resolve semantic occurrences for the current closed relation vocabulary, including:

- `references`;
- `depends_on`;
- `exception_to`;
- `defines`;
- `supersedes`;
- `amends`;
- `applies_subject_to`.

Every occurrence has stable `cross_reference_id`; every navigable normalized edge has stable `edge_id` in canonical direction.

Only uniquely resolved and origin-authorized relationships become navigable.

Unresolved occurrences remain non-navigable evidence and follow release-tier/warning policy.

## 12. Work package G — SQLite catalog and integrity gates

Persist the logical Evidence Graph relationally in `knowledge.sqlite`.

Enforce at minimum:

- foreign-key ownership;
- canonical document/node/chunk/source identities;
- dense canonical orders where required;
- exact chunk membership coverage/invariants;
- source/page span ownership;
- relationship endpoint/origin/status invariants;
- exact vocabulary/classification projections;
- conflict/position/cover records;
- release schema/version compatibility.

Independent catalog validation reconstructs critical identities and blocks release on any mismatch.

## 13. Work package H — Lexical retrieval

Benchmark/select one lexical engine/tokenizer/configuration using non-decisive data.

Freeze complete behavior identity and build immutable index artifacts.

The runtime maps lexical hits to canonical source/chunk/document IDs, applies exact metadata filters, and uses deterministic total ordering.

Exact identifiers/numbers/units/edition safety cannot be sacrificed for tokenization convenience.

Lexical retrieval supplies seeds only; final evidence correctness is owned by later Phase 2 closure stages.

## 14. Work package I — Deterministic citations and lineage

Build deterministic source citations from exact catalog/page provenance.

Materialize canonical RFC 8785 `lineage.json` with query-independent source/build/release provenance and complete transformation identities.

Runtime joins verified lineage to catalog rows and adds request-scoped assembly provenance without mutating the release.

Every public evidence item remains reproducible to source bytes/page and build transformations.

## 15. Work package J — Required context closure

Implement `phase-2-required-context-closure.md` in full.

Key obligations include:

- current closed required rule set;
- required-first deterministic priority queue;
- path-state, not target-only, deduplication;
- path-local cycle detection;
- source-backed target materialization;
- metadata-only empty targets;
- deterministic source-cover selection;
- current numeric bounds;
- typed incompleteness/warnings;
- release proof that single-clause required graph+conflict closure fits all bounds.

Ordinary exact/lexical search/clause operations always run required closure.

## 16. Work package K — Material conflict compilation and closure

Implement `phase-2-material-conflict-closure.md` in full.

Build-time responsibilities include:

- conflict/position content-addressed identities;
- required-context comparison projections;
- deterministic candidate detectors and explanation/confirmation rules;
- immutable decision artifacts;
- critical/standard unresolved admission policy;
- canonical conflict-position source covers.

Runtime responsibilities include exact span-intersection discovery, all-position attachment, required context for newly attached sides, and deterministic graph/conflict fixed point.

A result cannot silently choose the top-ranked conflict side.

## 17. Work package L — Shared ordinary evidence service

Implement `phase-2-evidence-service.md`.

The service pipeline is:

```text
validated request
  -> exact/identifier and/or lexical direct seeds
  -> required graph closure
  -> material conflict closure
  -> repeat to least fixed point
  -> central strict Evidence Package serializer
  -> typed Python result/error
```

Direct seed primitives may remain internal/test interfaces, but they do not substitute for public complete evidence.

## 18. Work package M — Evidence Package serializer

Build one central fail-closed serializer/validator for current closed schemas.

Verify:

- root properties;
- source/document/chunk/node/catalog ownership;
- exact original text/citation/page projections;
- classifications/provenance;
- source/build/assembly lineage;
- selection roles/seeds;
- retrieval records supported by Phase 2 mode;
- context completeness and paths;
- metadata-only context targets;
- material conflicts/reasons/positions/spans;
- typed warnings;
- output budgets and public field allowlists.

Any mismatch is a failure, not a best-effort success.

## 19. Work package N — Python, CLI, and MCP interfaces

The typed Python API is the shared implementation beneath adapters.

Phase 2 CLI search/get-clause/get-context commands expose complete ordinary evidence semantics; they are no longer labelled context-incomplete diagnostics.

MCP implements the current six-tool exact/lexical surface and current design resources through `phase-2-mcp-wire-resources.md`.

Protocol framing, dual-revision support, admission, cancellation/deadlines, page working-set budgets, redaction, and terminal-state rules remain exactly as specified by existing MCP appendices.

## 20. Work package O — Release identity, cache, validation, activation

Use current Section 25 dependency declarations for every artifact.

Release identity binds all behavior-bearing Phase 2 inputs, including graph/context/conflict/serializer rule/configuration and schema identities.

Candidate release assembly occurs only after every required report/gate exists.

Independent validation reopens/checksums/recomputes critical identities and runs read-only smoke tests.

Activation is atomic. Failure preserves the previous active release. Rollback restores the entire matching catalog/index/graph/context/conflict/lineage/configuration set.

## 21. Evaluation and decisive evidence

Phase 2 release gating follows the current `phase-2-release-gates.md` and `phase-2-held-out-retry-policy.md`.

Required blocking families include:

- lexical Recall@20 and Top-5 Wilson gates;
- three canonical classification Wilson gates;
- exact clause/citation deterministic correctness;
- required relationship/context deterministic conformance;
- zero known required-context omissions on decisive reviewed context cases;
- conflict deterministic conformance;
- zero known material-conflict-side omissions on decisive reviewed conflict cases;
- strict Evidence Package serialization;
- Python/CLI/MCP semantic equivalence;
- release/protocol/admission/security/rollback gates.

Decisive evidence cannot be reused as a changed-candidate optimizer.

## 22. Core test matrix

### Build/catalog tests

- manifest safe load/approval/source change;
- parser route/comparison/OCR policy;
- canonical node/classification identity;
- page span/box mapping;
- chunk/source/membership ordering;
- relationship occurrence/edge identity;
- unresolved critical/standard relation behavior;
- conflict ID/position/cover recomputation;
- release/cache/lineage identity.

### Retrieval tests

- exact document/clause;
- lexical exact identifiers/numbers/units;
- metadata filters/status null behavior;
- same wording across editions remains distinct;
- no match complete empty result;
- deterministic ties.

### Required context tests

- applicability;
- dependencies/definitions;
- forward/reverse exception handling;
- table row/table/clause context;
- note/footnote parent;
- empty structural target;
- reconvergent paths;
- semantic cycle warning;
- unresolved required relation;
- all current bounds and no-partial overflow.

### Conflict tests

- confirmed numeric conflict;
- compatible/explained cases;
- unresolved critical vs standard;
- n-ary conflict;
- canonical source covers;
- graph -> conflict -> graph fixed point;
- metadata filter cannot erase attached sides;
- no silent precedence.

### Interface tests

- strict Evidence Package schema;
- typed warnings/errors;
- Python/CLI/MCP equivalence;
- dual MCP revisions;
- URI canonicality/resources;
- cancellation/deadline races;
- admission/frame/page budgets;
- security/redaction/path non-leakage.

## 23. Failure semantics

Phase 2 must fail visibly and preserve source/release safety.

Examples:

- malformed request -> typed/protocol validation error;
- unavailable later mode -> `feature_unavailable`;
- unknown document/clause/source -> correct not-found route;
- required closure bound overflow -> `context_limit_exceeded`, no partial Evidence Package;
- release/artifact integrity mismatch -> fail/quarantine according to design;
- unresolved critical relationship/conflict -> release blocker;
- closed-schema serialization disagreement -> fail closed;
- cancellation/deadline winner suppresses late success;
- activation failure leaves previous release unchanged.

## 24. Recommended implementation sequence

Execute in dependency order:

1. bootstrap package/workspace/dependency profiles;
2. manifest/source approval and change detection;
3. production parser routing/comparison/OCR integration;
4. canonical model/vocabulary/classification;
5. page provenance;
6. standards-aware chunks/exact lookup sets;
7. relationship occurrence/resolution/edge identities;
8. SQLite catalog/integrity gates;
9. lexical benchmark/selection/index;
10. deterministic citations and immutable source/build lineage;
11. required-context rule/configuration compilation;
12. material-conflict detection/classification/position covers;
13. independent graph/context/conflict release validation;
14. exact/lexical direct seed service;
15. required graph runtime traversal;
16. material-conflict runtime closure/fixed point;
17. central Evidence Package serializer;
18. typed Python service;
19. CLI evidence commands;
20. MCP evidence tools/resources plus metadata/list/page/release surfaces;
21. split-integrity and deterministic conformance suites;
22. decisive lexical/classification/context/conflict/evidence gates;
23. protocol/admission/cancellation/security/failure injection;
24. final reports;
25. immutable candidate assembly/checksum/reopen/startup smoke validation;
26. rollback validation;
27. atomic activation;
28. final Phase 2 handoff verification for Phase 3.

## 25. Definition of Done

Phase 2 is complete only when:

1. source/manifests/parsers compile to a validated canonical immutable release;
2. exact/lexical seed retrieval is deterministic, source-grounded, and edition-safe;
3. every ordinary evidence seed runs complete required-context closure;
4. every material conflict closes to every required position/cover side;
5. graph/conflict fixed point terminates deterministically within declared bounds;
6. required bound overflow produces no partial success;
7. strict Evidence Package serialization matches source/catalog/lineage exactly;
8. `search_evidence`, `get_clause`, and `get_context` implement current Section 22 ordinary semantics;
9. metadata/list/page/release and evidence resources are safe/canonical;
10. Python, CLI, and MCP share one evidence service;
11. all deterministic/probabilistic/decisive Phase 2 gates pass;
12. all protocol/admission/cancellation/security tests pass;
13. release activation and rollback are atomic/reproducible;
14. Phase 3 can replace/extend seed selection without changing ordinary evidence correctness;
15. no Phase 3 dense/RRF or Phase 4 reranking/supporting-context implementation is hidden inside this phase.

## 26. Handoff to Phase 3

Phase 3 inherits:

- exact/lexical direct retrieval;
- canonical IDs and filters;
- validated graph/relationship artifacts;
- required graph/conflict closure;
- strict ordinary Evidence Package service;
- Python/CLI/MCP evidence surfaces;
- lineage/cache/release/activation/rollback contracts;
- Phase 2 evaluation/protocol/security baseline.

Phase 3 adds only its semantic candidate-selection scope: model benchmark, chunk embeddings, exact dense retrieval, lexical+dense RRF, deterministic Phase 3 query preprocessing/classification, and its own release/evaluation identities.

Its selected seeds enter this Phase 2 evidence service unchanged.

## 27. Handoff to Phase 4

Phase 4 inherits the complete ordinary Phase 2 evidence baseline plus Phase 3 hybrid retrieval.

Current Phase 4 owns:

- cross-encoder reranking;
- supporting-context expansion for high-accuracy retrieval;
- improved high-accuracy table/cross-reference behavior;
- expanded high-accuracy warning/refusal evaluation.

Phase 4 does **not** newly introduce ordinary required-context closure, material-conflict closure, basic Evidence Package assembly, or the basic evidence tools.

## 28. Review scope

Review comments/fixes for this corrective Phase 2 plan must remain inside Phase 2.

A review may require missing detail necessary for the ordinary exact/lexical evidence contract, but must not require Phase 3 embeddings/RRF or Phase 4 reranking/supporting-context implementation in this PR.
