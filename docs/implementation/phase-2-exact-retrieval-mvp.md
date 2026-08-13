# Phase 2 Implementation Plan: Exact Retrieval MVP

**Project:** ClauseSift  
**Phase:** 2 of the design-defined implementation sequence  
**Status:** Canonical current-design implementation plan  
**Primary design authority:** `docs/design.md`  
**Product intent:** `docs/design-brief.md`  
**Design principles:** `docs/design-principles.md`

## 1. Objective

Phase 2 builds the first complete ordinary ClauseSift evidence runtime.

Candidate selection remains deterministic exact/identifier + lexical retrieval. But every successful ordinary evidence result already satisfies current-design required context, material-conflict, lineage, warning, and Evidence Package semantics.

Phase 2 delivers:

- package/workspace/release infrastructure;
- approved manifests/source verification;
- parser routing and canonical Evidence Graph/catalog;
- evidence vocabulary/classification/page provenance;
- standards-aware chunks and exact lookup sets;
- stable relationship occurrence/edge identities;
- lexical index and exact/lexical direct seed retrieval;
- deterministic citations and immutable source/build lineage;
- deterministic required Evidence Graph closure;
- deterministic material-conflict fixed-point closure;
- strict ordinary Evidence Package serialization;
- one shared Python/CLI/MCP evidence service;
- current Section 22 tools/resources;
- current Section 29.4 Phase 2 quality gates;
- immutable release validation/activation/rollback.

Phase 2 does not implement Phase 3 embeddings/vector/RRF or Phase 4 cross-encoder reranking/supporting-context high-accuracy enhancements.

## 2. Canonical plan set

Detailed Phase 2 appendices include:

- `phase-2-required-context-closure.md`;
- `phase-2-material-conflict-closure.md`;
- `phase-2-evidence-service.md`;
- `phase-2-release-gates.md`;
- `phase-2-held-out-retry-policy.md`;
- `phase-2-lineage-release-contract.md`;
- `phase-2-mcp-wire-resources.md`;
- `phase-2-mcp-protocol-conformance.md`;
- `phase-2-mcp-admission-budgets.md`;
- `phase-2-release-lifecycle-guardrails.md`;
- `phase-2-canonical-id-migration.md`;
- `phase-2-contract-clarifications.md`;
- `phase-2-current-design-correction.md`.

Current `docs/design.md` is highest authority. The current corrective appendices supersede older Phase 2 statements that deferred ordinary required context/conflict/evidence behavior to Phase 4.

The protocol/admission appendices remain authority for transport/budget/cancellation rules; older tool/resource-scope statements in them are not current phase-scope authority.

## 3. In scope

Phase 2 implements and validates:

- distribution/package/workspace/dependency profiles;
- manifest schema, safe load, approval, source hash/size, relation entries, change detection;
- selected Phase 1 parser routes/comparison/OCR policy;
- canonical nodes/hierarchy/sequence and evidence vocabulary/classification provenance;
- node page spans and optional validated boxes;
- deterministic chunks/memberships/source IDs/exact lookup sets;
- semantic cross-reference occurrence extraction/resolution and canonical edge IDs;
- SQLite Evidence Graph/catalog/conflict/lineage/release records;
- lexical engine benchmark/selection/index;
- exact/lexical direct seed service and exact metadata filters;
- deterministic citations;
- required graph traversal/materialization/bounds;
- material-conflict build records/source covers/runtime fixed point;
- strict Evidence Package/context-target/conflict/warning serialization;
- Python evidence API;
- context-complete CLI evidence commands;
- current six-tool MCP surface and design resources;
- immutable release/cache/lineage/activation/rollback;
- current Phase 2 deterministic/probabilistic quality gates;
- protocol/admission/cancellation/security/failure-injection tests.

## 4. Out of scope

Phase 2 does not implement:

- chunk embeddings or vector search;
- embedding-model selection/query embedding;
- lexical+dense RRF or hybrid seed retrieval;
- cross-encoder reranking;
- Phase 4 supporting-context expansion for high-accuracy search;
- Phase 4 high-accuracy table/cross-reference improvements beyond ordinary required correctness;
- Phase 4 expanded high-accuracy warning/refusal evaluation;
- ANN solely because it is conventional;
- model-generated authoritative graph/conflict facts;
- engineering/legal conclusions absent from approved sources/metadata/rules.

## 5. Governing invariants

1. Original source bytes and approved manifest facts remain authoritative.
2. Document/edition/node/chunk/source IDs are canonical and never substituted by text similarity.
3. Exact clause lookup never chooses another edition or fuzzy clause.
4. Ranking selects seeds only; it cannot erase required context/conflict sides.
5. Only release-validated typed relationships are navigable.
6. Required closure follows a closed versioned rule set and exact deterministic queue/order/bounds.
7. Material conflicts are n-ary derived records, not a shortcut graph edge.
8. No score/recency/authority/stricter-looking text selects conflict precedence without an approved encoded rule.
9. Required graph + material conflict closure reaches a deterministic least fixed point.
10. Required evidence is never silently truncated.
11. Empty structural targets are metadata-only, never fabricated source evidence.
12. Immutable `lineage.json` remains query-independent; request assembly lineage is runtime-only.
13. Evidence/warning/conflict/lineage schemas are closed.
14. Python, CLI, and MCP evidence tools use one service.
15. MCP resources preserve their independent canonical payload contracts; notably the source resource is raw `original_text`, not an Evidence Package wrapper.
16. A failed candidate never changes the active release.
17. Probabilistic held-out evidence is a gate, not an optimizer; deterministic conformance suites remain complete executable contracts.

## 6. Implementation architecture

```text
approved manifests + exact source bytes
  -> parser routing/comparison/OCR
  -> canonical Evidence Graph + page provenance
  -> chunks/sources + relationships
  -> SQLite catalog
  -> lexical index
  -> required context + conflict build artifacts
  -> immutable lineage/release artifacts

runtime request
  -> strict validation
  -> exact/lexical direct seeds
  -> required graph closure
  -> material conflict closure
  -> least fixed point
  -> strict Evidence Package serializer
  -> Python / CLI / MCP evidence tools
```

Resources such as raw source/page/document/current-release follow their own Section 22 resource contract rather than being forced into an Evidence Package shape.

## 7. Work packages

### A — Package/workspace/dependencies

Implement the standard package/import/CLI names, build/runtime dependency separation, idempotent workspace initialization, and path containment/symlink/reparse/regular-file safety. Base runtime must not import heavy parser/OCR build-only packages.

### B — Manifest/source governance

Implement closed safe manifest schema, exact field bounds/enums, raw-vs-semantic manifest hashes, explicit approval artifacts, source hash/size/page verification, and build-time revalidation. Manifest-owned identity/status/applicability facts cannot be changed by parser/ranker/model output.

### C — Parser/canonical model

Bind selected Phase 1 canonical/comparator/OCR routes. Critical documents satisfy comparison policy. Build canonical node tree, stable IDs, evidence vocabulary/classifications, and complete provenance. No parser field-level merge silently creates source facts.

### D — Page provenance/chunks

Persist deterministic node-page intervals/optional boxes; create standards-aware chunks/memberships/source IDs and exact Section 14.1 clause lookup sets. IDs/order are deterministic and independent of SQLite physical order.

### E — Relationships/Evidence Graph

Compile structural `contains`/`precedes` and semantic `references`, `depends_on`, `exception_to`, `defines`, `supersedes`, `amends`, `applies_subject_to` occurrences. Only uniquely resolved origin-authorized semantic occurrences become navigable edges. Unresolved rows remain non-navigable and follow tier policy.

### F — Catalog and lexical retrieval

Persist/independently validate documents/nodes/chunks/sources/memberships/pages/relationships/conflicts/lineage references. Select/freeze a lexical engine on non-decisive data, build immutable index artifacts, and implement deterministic exact/lexical seed ordering/filter behavior.

### G — Citations and lineage

Build deterministic source citations and canonical query-independent `lineage.json`. Runtime adds request-scoped exact/lexical retrieval/context/conflict assembly lineage through the current closed schema only.

### H — Required context

Implement `phase-2-required-context-closure.md`: closed required rules, exact queue order/path-state dedup/cycle handling, source/materialization/context-target rules, current numeric bounds, no-partial required overflow, deterministic graph/conflict composition, and complete deterministic traversal/negative conformance.

### I — Material conflict

Implement `phase-2-material-conflict-closure.md`: content-addressed conflict/position IDs, required-context comparison projection, deterministic/human-reviewed decision authority, canonical position source covers, tier admission, runtime all-side closure/fixed point, conflict serialization, probabilistic conflict candidate/precision gates, and deterministic all-side/precedence conformance.

### J — Evidence service

Implement `phase-2-evidence-service.md`: one service for direct seeds -> required graph/conflict fixed point -> central strict serializer -> typed Python results/errors.

### K — CLI/MCP

CLI search/get-clause/get-context use the same evidence service. MCP implements the current six evidence/metadata tools and exact Section 22 resources. The source resource remains raw validated `original_text` with `text/plain;charset=utf-8`. Protocol/admission companions apply their transport rules to the complete current surface.

### L — Release lifecycle

Bind every behavior-bearing Phase 2 artifact/configuration to Section 25 dependency/release identity; run independent release/startup validation; assemble/checksum/reopen only after gates; atomically activate; rollback restores the matching catalog/index/graph/context/conflict/lineage/configuration set.

## 8. Exact runtime context bounds

Phase 2 enforces the current values:

- structural depth 64;
- required semantic depth 8 per seed;
- supporting depth 1;
- diagnostic depth 2;
- 128 expanded objects/request excluding direct seeds;
- 32 paths/context object;
- 1,024 accepted path steps;
- 64 conflicts/request;
- 16 positions/conflict;
- 256 total positions;
- 1,024 conflict position spans;
- 1,024 conflict inclusion reasons;
- current Section 22/MCP byte/frame/admission bounds.

Required overflow returns `context_limit_exceeded` with no partial Evidence Package.

## 9. Quality gates

Phase 2 follows `phase-2-release-gates.md`, which maps Section 29.4 exactly.

### Deterministic zero-failure/zero-occurrence gates

- exact clause lookup complete deterministic suite;
- document/edition/clause/page citation suite;
- unsupported deterministic conclusions golden set;
- required context/lineage paths/source status/order traversal suite;
- prohibited/unresolved/guessed/wrong-edition traversal negative suite;
- vocabulary/schema/provenance/round-trip/version/extension suite;
- classification/source-authority negative suite;
- conflict position/source/lineage/all-side/order/precedence deterministic suite;
- conflict explanation/promotion/false-winner negative suite;
- strict Evidence Package/interface/protocol conformance as applicable.

### Probabilistic Wilson gates

- Recall@20 LB >=98%, >=150 applicable cases;
- Top-5 LB >=95%, >=60;
- node-type LB >=98%, >=150;
- normative-status LB >=98%, >=150;
- source-modality LB >=98%, >=150;
- conflict-candidate recall LB >=95%, >=60;
- confirmed/unresolved conflict precision LB >=98% for each applicable state family, >=150 each;
- explained-difference precision LB >=98% for each applicable explanation-code family, >=150 each.

Increase samples when required strata/hard negatives would otherwise be underrepresented. Preserve Section 29.3 blinded-review/reliability rules for semantic labels.

Do not invent a separate held-out 100% required-context/all-side gate: those are complete deterministic conformance count gates under current design.

## 10. Held-out retry governance

`phase-2-held-out-retry-policy.md` applies to the probabilistic release gates. Once decisive statistical evidence is observed, a behavior-bearing changed candidate cannot claim fresh authorization from the same split; identical-candidate replay is reproduction-only; later campaigns require fresh preregistered independent evidence.

Deterministic conformance suites remain complete versioned executable contracts rerun in full after code changes; expected outputs change only through reviewed source/design/label corrections.

## 11. Test matrix

Build/catalog: manifest/approval/source change, parser comparison/OCR, canonical/classification, page spans, chunk/source membership, relationship IDs/resolution, conflict IDs/covers, release/cache/lineage identity.

Retrieval: exact document/clause, identifiers/numbers/units, filters/status null, same wording across editions, no-match complete success, deterministic ties.

Required context: applicability, dependencies/definitions, exception directions, table/note context, empty target, reconvergent paths, cycles, unresolved required relation, exact max/one-over bounds.

Conflict: confirmed/explained/unresolved, tier behavior, n-ary records, source covers, graph-conflict fixed point, direct-filter non-erasure, no false precedence.

Interfaces: strict Evidence Package, typed warnings/errors, Python/CLI/MCP equality, both MCP revisions, canonical resources including raw source bytes, cancellation/deadline, admission/frame/page budgets, redaction/path non-leakage.

## 12. Failure semantics

Examples:

- malformed request -> exact validation route;
- explicit unavailable later mode -> `feature_unavailable`;
- unknown document/clause/source -> exact not-found/resource-miss route;
- required closure overflow -> `context_limit_exceeded`, no partial Evidence Package;
- unresolved critical relationship/conflict -> release blocker;
- release/schema/lineage/catalog mismatch -> fail closed;
- cancellation/deadline winner suppresses late success;
- source/page resource integrity mismatch -> safe resource error/no content;
- any failed release gate -> no activation, previous release unchanged.

## 13. Implementation sequence

1. package/workspace/dependencies;
2. manifest/source approval/change detection;
3. parser routing/comparison/OCR;
4. canonical model/vocabulary/classification;
5. page provenance;
6. chunks/exact lookup;
7. relationship occurrence/resolution/edge IDs;
8. SQLite catalog/integrity;
9. lexical benchmark/selection/index;
10. citations/query-independent lineage;
11. required-context compilation/validation;
12. conflict compilation/decisions/position covers;
13. independent graph/context/conflict release validation;
14. exact/lexical direct seed service;
15. required graph runtime;
16. material-conflict runtime fixed point;
17. central Evidence Package serializer;
18. typed Python API;
19. CLI evidence commands;
20. MCP evidence tools/resources + metadata/list/page/release;
21. deterministic conformance suites;
22. probabilistic retrieval/classification/conflict gates under leakage-safe policy;
23. protocol/admission/cancellation/security/failure injection;
24. final reports;
25. candidate assembly/checksum/reopen/startup validation;
26. rollback validation;
27. atomic activation;
28. Phase 3 handoff verification.

## 14. Definition of Done

Phase 2 is complete only when:

1. approved source/manifests deterministically compile to one validated immutable release;
2. exact/lexical seed retrieval is edition-safe/deterministic;
3. every ordinary evidence seed runs complete current required closure;
4. every material conflict closes to all required positions/sources;
5. graph/conflict fixed point and all bounds are deterministic;
6. required overflow never returns partial success;
7. strict Evidence Package serialization matches source/catalog/lineage exactly;
8. current evidence tools/resources satisfy exact Section 22 contracts, including raw source resource bytes/MIME;
9. Python/CLI/MCP evidence tools use one service;
10. every applicable Section 29.4 deterministic/probabilistic Phase 2 gate passes;
11. protocol/admission/cancellation/security conformance passes;
12. activation/rollback is atomic and reproducible;
13. no Phase 3 dense/RRF or Phase 4 reranking/supporting-context implementation is hidden here.

## 15. Handoff to Phase 3

Phase 3 inherits exact/lexical seed retrieval, canonical IDs/filters, validated graph/relationship/context/conflict artifacts, deterministic required graph/conflict closure, strict ordinary Evidence Package service, Python/CLI/MCP evidence interfaces, lineage/cache/release/activation/rollback, and Phase 2 quality/protocol/security baseline.

Phase 3 adds embedding benchmark/selection, chunk embeddings, exact dense retrieval, lexical+dense RRF, deterministic Phase 3 query preprocessing/classification, and Phase 3 release/evaluation identity. Its seeds enter the Phase 2 evidence service unchanged.

## 16. Handoff to Phase 4

Phase 4 inherits the complete ordinary Phase 2 evidence baseline plus Phase 3 hybrid retrieval. It adds cross-encoder reranking, supporting-context high-accuracy expansion, high-accuracy table/cross-reference improvements, and expanded high-accuracy warning/refusal evaluation. It does not newly introduce ordinary required context, material conflicts, basic Evidence Package assembly, or basic evidence tools.

## 17. Review scope

Review/fixes stay within Phase 2 current-design planning. Do not require Phase 3 dense/RRF or Phase 4 reranking/supporting-context implementation details in this PR.
