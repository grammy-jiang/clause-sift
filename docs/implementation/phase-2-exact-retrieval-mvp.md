# Phase 2 Implementation Plan: Exact Retrieval MVP

**Project:** ClauseSift  
**Phase:** 2 of the design-defined implementation sequence  
**Status:** Canonical current-design implementation plan  
**Primary design authority:** `docs/design.md`  
**Product intent:** `docs/design-brief.md`  
**Design principles:** `docs/design-principles.md`

## 1. Objective

Phase 2 builds the first complete ordinary ClauseSift evidence runtime. Candidate selection remains deterministic exact/identifier + lexical retrieval, while every successful ordinary evidence result already satisfies current-design required context, material-conflict, lineage, warning, and Evidence Package semantics.

Phase 2 delivers package/workspace/release infrastructure; approved manifests/source verification; parser routing and canonical Evidence Graph/catalog; evidence vocabulary/classification/page provenance; standards-aware chunks/exact lookup sets; stable relationship occurrence/edge identities; lexical indexing; exact/lexical seed retrieval; deterministic citations/lineage; required graph closure; material-conflict fixed-point closure; strict ordinary Evidence Package serialization; shared Python/CLI/MCP evidence behavior; current Section 22 tools/resources; current Section 29.4 quality gates; and immutable release validation/activation/rollback.

Phase 2 does not implement Phase 3 embeddings/vector/RRF or Phase 4 cross-encoder reranking/automatic high-accuracy supporting-context expansion.

## 2. Canonical Phase 2 plan set

Detailed appendices include:

- `docs/implementation/phase-2-required-context-closure.md`;
- `docs/implementation/phase-2-material-conflict-closure.md`;
- `docs/implementation/phase-2-evidence-service.md`;
- `docs/implementation/phase-2-release-gates.md`;
- `docs/implementation/phase-2-held-out-retry-policy.md`;
- `docs/implementation/phase-2-lineage-release-contract.md`;
- `docs/implementation/phase-2-mcp-wire-resources.md`;
- `docs/implementation/phase-2-mcp-protocol-conformance.md`;
- `docs/implementation/phase-2-mcp-admission-budgets.md`;
- `docs/implementation/phase-2-release-lifecycle-guardrails.md`;
- `docs/implementation/phase-2-canonical-id-migration.md`;
- `docs/implementation/phase-2-contract-clarifications.md`;
- `docs/implementation/phase-2-current-design-correction.md`.

Current `docs/design.md` is highest authority. Current corrective appendices supersede older Phase 2 statements that deferred ordinary required context/conflict/evidence behavior to Phase 4. Protocol/admission appendices remain authority for transport/budget/cancellation mechanics; their older surface lists are not current phase-scope authority.

## 3. Phase boundary

### In scope

Phase 2 implements and validates:

- package/workspace/dependency profiles;
- manifest schema/safe load/approval/source verification/change detection;
- selected Phase 1 parser routes/comparison/OCR policy;
- canonical nodes/hierarchy/sequence, evidence vocabulary/classification provenance;
- page provenance and deterministic chunks/source identities/exact lookup sets;
- semantic cross-reference occurrences and canonical navigable edge identities;
- SQLite Evidence Graph/catalog/conflict/lineage/release records;
- lexical engine selection/index plus exact/lexical direct seed retrieval and metadata filtering;
- deterministic citations;
- required graph traversal/materialization/bounds;
- material-conflict build records/canonical position covers/runtime fixed point;
- strict Evidence Package/context-target/conflict/warning serialization;
- typed Python evidence API;
- CLI `search` and `get-clause` through the shared evidence service;
- MCP `search_evidence`, `get_clause`, `get_context`, metadata/list/page tools, and current design resources;
- **explicit Python/MCP `get_context(required|supporting|diagnostic)` traversal, including optional truncation after complete required closure**;
- immutable release/cache/lineage/activation/rollback;
- current deterministic/probabilistic quality gates;
- protocol/admission/cancellation/security/failure-injection tests.

### Out of scope

Phase 2 does not implement chunk embeddings/vector search; embedding-model selection/query embedding; lexical+dense RRF/hybrid seed retrieval; cross-encoder reranking; automatic supporting-context expansion of ordinary `high_accuracy` search; Phase 4 high-accuracy table/cross-reference improvements beyond ordinary required correctness; Phase 4 expanded high-accuracy warning/refusal evaluation; ANN solely for convention; model-generated authoritative graph/conflict facts; or engineering/legal conclusions absent from approved sources/metadata/rules.

## 4. Governing invariants

1. Original source bytes and approved manifest facts remain authoritative.
2. Canonical document/edition/node/chunk/source identities are never replaced by similarity.
3. Exact clause lookup never substitutes another edition or fuzzy clause.
4. Ranking selects direct seeds only; it cannot erase required context/conflict sides.
5. Only release-validated typed relationships are navigable.
6. Required closure follows the current closed rule set and deterministic queue/path/bound semantics.
7. Material conflicts are n-ary derived release records, not a shortcut graph edge.
8. No score/recency/authority/stricter-looking text creates conflict precedence without an approved rule.
9. Required graph + conflict closure reaches a deterministic least fixed point.
10. Required evidence is never silently truncated.
11. Empty structural targets remain metadata-only.
12. Immutable `lineage.json` is query-independent; assembly lineage is runtime-only.
13. Evidence/warning/conflict/lineage schemas are closed.
14. Python/CLI/MCP overlapping evidence operations use one service.
15. **Python/MCP own `get_context`; current CLI has no `get-context` command.**
16. MCP resources preserve independent Section 22 payload contracts; source resource is raw `original_text`, not an Evidence Package wrapper.
17. A failed candidate never changes the active release.
18. Probabilistic held-out evidence is a gate, not an optimizer; deterministic conformance suites remain complete executable contracts.

## 5. Build work packages

### A — Package/workspace/source governance

Implement standard package/import/CLI names, base-runtime vs build/OCR dependency separation, idempotent safe workspace initialization, closed manifest schema, explicit approval artifacts, raw-vs-semantic manifest hashes, exact source hash/size/page validation, relations, and build-time revalidation.

### B — Parser/canonical model/page provenance

Bind selected Phase 1 parser/comparator/OCR routes. Build canonical node tree, stable IDs, vocabulary/classifications/provenance, page spans/boxes, standards-aware chunks, source memberships, and exact clause lookup sets. Parser disagreement follows comparison policy; field-level source-fact merging is forbidden.

### C — Relationships/catalog/lexical retrieval

Compile structural/semantic occurrence records, unique origin-authorized navigable edges, stable occurrence/edge IDs, and unresolved tier policy. Persist the logical Evidence Graph relationally in `knowledge.sqlite`. Select/freeze lexical behavior on non-decisive data and build immutable index artifacts.

### D — Citations/lineage/release identities

Build deterministic citations and canonical query-independent `lineage.json`; bind lexical/relationship/context/conflict artifacts/configuration into current Section 25 cache/release identity; independently validate catalog/artifact/lineage consistency.

### E — Required context

Implement `phase-2-required-context-closure.md`: closed required rules, deterministic priority/path-state/cycle handling, source/context-target materialization, required graph/conflict fixed point, current numeric bounds, no-partial required overflow, and deterministic traversal/negative gates.

After complete required closure, **Python/MCP `get_context` may explicitly continue to supporting/diagnostic traversal in Phase 2**. Automatic supporting expansion of ordinary high-accuracy search remains Phase 4.

### F — Material conflicts

Implement `phase-2-material-conflict-closure.md`: conflict/position identities, required-context comparison projection, deterministic/review decision authority, canonical position covers, tier admission, runtime all-side fixed point, optional handoff for explicit Python/MCP `get_context`, strict conflict serialization, and Section 29.4 conflict gates.

### G — Evidence service and interfaces

Implement `phase-2-evidence-service.md`: one service for direct seeds -> required fixed point -> optional traversal when explicitly requested -> central strict serializer -> typed public result.

Interface ownership is exact:

- Python: search, exact clause retrieval, context inspection;
- CLI Section 23.1: `clausesift search` and `clausesift get-clause` for evidence retrieval; **no CLI `get-context`**;
- MCP: `search_evidence`, `get_clause`, `get_context` plus metadata/list/page tools;
- resources: exact independent Section 22 resource contracts, including raw source text.

## 6. Runtime bounds and failure semantics

Enforce current Section 19/22 bounds: structural depth 64; required semantic depth 8/seed; supporting depth 1; diagnostic depth 2; 128 expanded objects; 32 paths/object; 1,024 accepted steps; 64 conflicts/request; 16 positions/conflict; 256 total positions; 1,024 conflict spans; 1,024 conflict reasons; and current MCP frame/admission budgets.

Required overflow -> `context_limit_exceeded` with no partial Evidence Package. Explicit optional Python/MCP `get_context` overflow stops before the first over-bound optional candidate, preserves complete required closure, sets `truncated_optional`, and emits the permitted warning.

No-match search remains complete empty success with mandatory `evidence_insufficient`. Successful `auto` fallback caused by unavailable later dense/reranker capability includes `retrieval_capability_unavailable`.

## 7. Quality gates

`docs/implementation/phase-2-release-gates.md` maps Section 29.4 exactly.

Deterministic complete-suite gates cover exact lookup, citations, unsupported conclusions, required traversal/path/status/order, prohibited traversal, vocabulary/schema/provenance, classification/source-authority negatives, conflict all-side/order/precedence, conflict negatives, Evidence Package/interface/resource/protocol conformance, **Python/MCP context-level semantics**, and **absence of CLI `get-context`**.

Probabilistic gates include Recall@20 >=98% Wilson LB (>=150 applicable), Top-5 >=95% (>=60), three classification >=98% gates, conflict-candidate recall >=95%, and applicable confirmed/unresolved/explained precision >=98% families with current sample/stratification/reviewer rules.

Do not invent a separate statistical held-out 100% context/all-side gate; those correctness obligations are current deterministic complete-suite gates.

## 8. Held-out/release lifecycle

Probabilistic decisive evidence follows `phase-2-held-out-retry-policy.md`: preregistration, behavior-bearing candidate identity, one decisive unseen use, reproduction-only replay, finite campaigns, and genuinely fresh later evidence. Deterministic conformance suites remain versioned executable contracts rerun in full after implementation changes.

Candidate release assembly occurs only after all required artifacts/reports/gates pass. Reopen/checksum/startup validation is independent. Activation is atomic; rollback restores the matching catalog/index/graph/context/conflict/lineage/configuration set.

## 9. Implementation sequence

1. package/workspace/dependencies;
2. manifest/source approval/change detection;
3. parser routing/comparison/OCR;
4. canonical model/vocabulary/classification/page provenance;
5. chunks/exact lookup;
6. relationship occurrence/resolution/edge IDs;
7. SQLite catalog integrity;
8. lexical selection/index;
9. citations/query-independent lineage;
10. required-context compilation/validation;
11. conflict compilation/decisions/position covers;
12. independent graph/context/conflict release validation;
13. exact/lexical direct seed runtime;
14. required graph/conflict fixed point;
15. explicit supporting/diagnostic optional traversal for Python/MCP `get_context`;
16. central Evidence Package serializer;
17. typed Python API;
18. CLI `search` and `get-clause`;
19. MCP evidence/metadata tools and resources;
20. deterministic conformance suites;
21. probabilistic retrieval/classification/conflict gates;
22. protocol/admission/cancellation/security/failure injection;
23. final reports;
24. candidate assembly/reopen/startup/rollback validation;
25. atomic activation;
26. Phase 3 handoff verification.

## 10. Definition of Done

Phase 2 is complete only when approved sources deterministically compile to a validated immutable release; exact/lexical seed retrieval is edition-safe; every ordinary seed receives complete required graph/conflict closure; Python/MCP explicit supporting/diagnostic `get_context` works after the required fixed point; CLI scope remains exactly search/get-clause; strict Evidence Package/resource contracts match Section 21-23; mandatory no-match/capability warnings are present; every applicable Section 29.4 deterministic/probabilistic gate passes; protocol/admission/cancellation/security conformance passes; activation/rollback is atomic; and no Phase 3 dense/RRF or Phase 4 automatic high-accuracy supporting-context implementation is hidden in Phase 2.

## 11. Handoff

Phase 3 inherits exact/lexical seed retrieval, canonical IDs/filters, graph/context/conflict artifacts, deterministic required fixed point, explicit Python/MCP context inspection, strict ordinary Evidence Package service, interfaces/resources, lineage/release lifecycle, and Phase 2 quality/protocol/security baseline. Phase 3 adds semantic seed selection (embeddings/dense/RRF/query preprocessing/classification) only.

Phase 4 inherits the complete Phase 2 ordinary baseline plus Phase 3 hybrid retrieval and adds cross-encoder reranking, automatic supporting-context expansion for high-accuracy search, high-accuracy table/cross-reference improvements, and expanded high-accuracy warning/refusal evaluation.

## 12. Review scope

Review/fixes remain Phase 2 current-design planning only. Do not require Phase 3 dense/RRF or Phase 4 reranking/automatic high-accuracy supporting-context implementation details in this PR.
