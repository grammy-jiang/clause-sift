# Phase 2 Current-Design Correction

**Project:** ClauseSift  
**Phase:** 2 — Exact Retrieval MVP  
**Status:** Normative Phase 2 implementation-plan correction  
**Primary design authority:** `docs/design.md`

## 1. Why this correction exists

The original merged Phase 2 plan was written before the current implementation-phase boundary in `docs/design.md` was finalized. It therefore deferred ordinary required Evidence Graph traversal, material-conflict closure, strict ordinary Evidence Package assembly, and basic evidence-returning Python/CLI/MCP surfaces to Phase 4.

That old boundary is no longer valid.

Current design assigns Phase 2:

- deterministic required Evidence Graph closure;
- deterministic material-conflict closure;
- strict ordinary Evidence Package assembly;
- basic context-complete exact/lexical Python/CLI/MCP evidence behavior.

This document records the superseded statements and the current authority map. The canonical main plan is `phase-2-exact-retrieval-mvp.md`.

## 2. Current detailed companions

The current corrective implementation detail lives in:

- `phase-2-required-context-closure.md`;
- `phase-2-material-conflict-closure.md`;
- `phase-2-evidence-service.md`;
- `phase-2-release-gates.md`;
- `phase-2-held-out-retry-policy.md`;
- `phase-2-lineage-release-contract.md`;
- `phase-2-mcp-wire-resources.md`.

Existing Phase 2 parser, cache/release, MCP framing/admission, canonical-ID, lifecycle, and other appendices remain normative for unchanged contracts.

## 3. Superseded old Phase 2 statements

The following interpretations are explicitly superseded.

### 3.1 Phase 2 is only context-incomplete direct retrieval

Superseded. Phase 2 seed selection is exact/lexical, but successful ordinary evidence runs current required graph/conflict closure and strict Evidence Package assembly.

### 3.2 Required graph traversal belongs to Phase 4

Superseded. Current ordinary required traversal belongs to Phase 2. Phase 4 later adds supporting-context high-accuracy behavior.

### 3.3 Material-conflict runtime closure belongs to Phase 4

Superseded. Current conflict build records, position covers, fixed-point all-side runtime preservation, and strict conflict projection belong to Phase 2.

### 3.4 Public evidence tools must be withheld until Phase 4

Superseded. Phase 2 implements current ordinary `search_evidence`, `get_clause`, and `get_context` semantics through one shared service. Metadata/list/page tools remain safe exact projections.

### 3.5 Phase 2 CLI search/get-clause are direct diagnostic substitutes

Superseded. They use the same context-complete ordinary evidence service as Python/MCP.

### 3.6 Phase 2 MCP advertises only metadata/list/page/release

Superseded. Current Phase 2 exposes the six-tool surface defined by `phase-2-mcp-wire-resources.md` when complete semantics are implemented.

`phase-2-mcp-protocol-conformance.md` and `phase-2-mcp-admission-budgets.md` remain authoritative for transport/framing/budget/cancellation/admission behavior only. Any old surface list or statement deferring ordinary evidence tools/traversal to Phase 4 is not current phase-scope authority.

### 3.7 All source resources are Evidence Package projections

Superseded/incorrect. The current Section 22 resource contracts are independent. In particular `standards://source/{source_id}` is raw validated `original_text` with exact `text/plain;charset=utf-8` MIME and no wrapper. Rich context/lineage is provided by evidence tools and other resource types only where Section 22 explicitly defines it.

### 3.8 Context/conflict quality is Phase4-only

Superseded. Phase 2 must pass the Section 29.4 gates owned by ordinary required context and conflict behavior.

## 4. Corrected architecture

```text
validated request
  -> exact/identifier and/or lexical seed retrieval
  -> deterministic required graph closure
  -> deterministic material-conflict closure
  -> repeat graph/conflict closure to least fixed point
  -> strict ordinary Evidence Package serialization
  -> Python / CLI / MCP evidence tools
```

MCP resources separately obey their exact Section 22.3 payload/MIME contracts.

Phase 3 changes seed selection by adding dense/RRF. Phase 4 adds reranking/supporting-context high-accuracy behavior. Neither should duplicate the Phase 2 ordinary evidence service.

## 5. Corrected Phase 2 build work

After existing manifest/parser/canonical/page/chunk/catalog foundations, Phase 2 also builds/validates:

1. semantic occurrence resolution + stable occurrence/edge IDs;
2. executable required-context configuration;
3. conflict candidates/required-context comparison projections;
4. final conflict decisions;
5. canonical position source covers;
6. context/conflict catalog indexes/records;
7. query-independent lineage references for retrieval/context/conflict artifacts;
8. independent graph/context/conflict release validation;
9. single-clause worst-case closure bound proof.

## 6. Corrected runtime work

Phase 2 runtime owns:

- exact/lexical direct seeds and filters;
- required graph queue/path state/cycles/materialization;
- material-conflict discovery/canonical covers/fixed point;
- context targets/conflicts/warnings/completeness;
- central strict Evidence Package serialization;
- shared Python evidence API;
- context-complete CLI evidence commands;
- current six MCP tools and exact resources;
- immutable release startup validation/rollback.

No embedding or reranker model is needed by the Phase 2 exact/lexical path.

## 7. Corrected quality-gate ownership

Use Section 29.4 exactly; do not invent substitute gate types.

### Deterministic complete-suite gates now owned by Phase 2

- exact clause lookup: zero failures;
- document/edition/clause/page citations: zero failures;
- unsupported deterministic conclusions: zero observed failures;
- required context/lineage paths/source status/ordering: zero failures in complete traversal conformance suite;
- prohibited/unresolved/guessed/wrong-edition traversal: zero accepted edges in complete negative suite;
- vocabulary/schema/classification-provenance conformance: zero failures;
- classification/source-authority negative suite: zero prohibited occurrences;
- conflict position/source/lineage completeness, all-side preservation, state/dimension order, trusted precedence: zero failures in complete conflict conformance suite;
- conflict explanation/promotion/false-winner negative suite: zero prohibited occurrences.

### Probabilistic Phase 2 gates

- Recall@20: Wilson LB >=98%, >=150 applicable cases;
- Top-5: Wilson LB >=95%, >=60;
- node-type/normative-status/source-modality: Wilson LB >=98%, >=150 each;
- conflict-candidate recall: Wilson LB >=95%, >=60;
- confirmed/unresolved conflict precision: Wilson LB >=98% for each applicable state family, >=150 each;
- explained-difference precision: Wilson LB >=98% for each applicable explanation-code family, >=150 each.

Optional-context precision remains later supporting-context/high-accuracy scope.

The deterministic required-context/all-side criteria are complete versioned conformance count gates, not separate held-out 100% statistical gates.

## 8. Corrected evaluation governance

`phase-2-held-out-retry-policy.md` governs the probabilistic gates above: preregistration, candidate identity, one decisive unseen use, reproduction-only replay, finite campaigns, and fresh later evidence.

Deterministic conformance suites remain versioned executable contracts rerun in full. Expected outputs change only through reviewed design/source/label corrections, never to make an implementation pass.

Where semantic labels are used, Section 29.3 blinded review/calibration/reliability/adjudication rules remain mandatory.

## 9. Corrected implementation sequence

1. package/workspace/dependencies;
2. manifest/source approval/change detection;
3. parser routing/validation/OCR;
4. canonical model/vocabulary/classification/page provenance;
5. chunks/exact lookup;
6. relationship occurrences/edge identity;
7. SQLite graph/catalog integrity;
8. lexical selection/index;
9. deterministic citations + query-independent lineage;
10. required-context compilation/validation;
11. conflict detection/decisions/canonical position covers;
12. independent graph/context/conflict release validation;
13. exact/lexical direct seed runtime;
14. required graph traversal;
15. material-conflict fixed point;
16. central Evidence Package serializer;
17. Python/CLI/MCP evidence tools + exact resources;
18. deterministic conformance suites;
19. probabilistic retrieval/classification/conflict gates;
20. protocol/admission/cancellation/security/failure injection;
21. reports;
22. candidate assembly/reopen/startup/rollback validation;
23. atomic activation;
24. Phase 3 handoff.

## 10. Definition of Done

Phase 2 is complete only when the current ordinary exact/lexical evidence service, required graph/conflict fixed point, strict Evidence Package, current tools/resources, Section 29.4 gates, release integrity, protocol/security, activation, and rollback all pass without pulling Phase 3 dense/RRF or Phase 4 reranking/supporting-context implementation into Phase 2.

## 11. Handoff to Phase 3

Phase 3 receives exact/lexical seed retrieval, canonical IDs/filters, validated relationship/context/conflict artifacts, deterministic required graph/conflict closure, strict ordinary Evidence Package service, Python/CLI/MCP evidence interfaces, lineage/cache/release lifecycle, and Phase 2 quality/protocol/security baseline.

Phase 3 adds semantic seed selection only: embedding benchmark/assets, exact dense retrieval, lexical+dense RRF, deterministic Phase 3 query preprocessing/classification, and Phase 3 release/evaluation identity.

## 12. Handoff to Phase 4

Phase 4 receives the complete ordinary Phase 2 evidence baseline plus Phase 3 hybrid retrieval. It adds cross-encoder reranking, supporting-context high-accuracy expansion, improved high-accuracy table/cross-reference behavior, and expanded high-accuracy warning/refusal evaluation.

Phase 4 does not newly introduce ordinary required-context closure, material-conflict closure, basic Evidence Package assembly, or the basic evidence tools.

## 13. Authority order

Read Phase 2 in this order:

1. current `docs/design.md`;
2. canonical current `phase-2-exact-retrieval-mvp.md`;
3. current required-context/material-conflict/evidence-service/release-gates/held-out/lineage/MCP wire appendices;
4. older Phase 2 appendices for unchanged contracts only.

An older statement is not authoritative merely because it is more convenient.

## 14. Review scope

Review this correction only for Phase 2 current-design correctness/internal consistency. Do not require Phase 3 dense/RRF or Phase 4 reranking/supporting-context implementation detail in this corrective PR.
