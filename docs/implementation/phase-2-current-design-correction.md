# Phase 2 Current-Design Correction

**Project:** ClauseSift  
**Phase:** 2 — Exact Retrieval MVP  
**Status:** Normative Phase 2 implementation-plan correction  
**Primary design authority:** `docs/design.md`  
**Corrective companions:**

- `docs/implementation/phase-2-required-context-closure.md`
- `docs/implementation/phase-2-material-conflict-closure.md`
- `docs/implementation/phase-2-evidence-service.md`

## 1. Purpose and precedence

The merged Phase 2 implementation-plan set was reviewed and merged before the current `docs/design.md` phase boundary was finalized. It therefore contains statements that defer ordinary required-context traversal, material-conflict closure, final ordinary Evidence Package assembly, and the basic evidence-returning interfaces to Phase 4.

Those statements are now stale.

Current `docs/design.md` assigns the ordinary exact/lexical evidence baseline to **Phase 2**, including:

- deterministic required Evidence Graph context closure;
- deterministic material-conflict closure;
- strict ordinary Evidence Package assembly;
- basic Python, CLI, and MCP retrieval interfaces using those semantics.

This correction is authoritative wherever the existing Phase 2 plan set conflicts with that current ownership.

The three detailed corrective companion plans above define the missing implementation work. Existing Phase 2 documents remain authoritative for unchanged contracts such as manifests, parser integration, canonical model, chunks, SQLite, lexical retrieval, package/bootstrap, release lifecycle, MCP framing/admission, immutable lineage, activation, and rollback.

## 2. Exact stale statements superseded

### 2.1 Main Phase 2 objective

Any Phase 2 objective saying the milestone excludes runtime Evidence Graph traversal is superseded.

The corrected objective is:

> Build the first deterministic ClauseSift compiler and read-only runtime around approved manifests, the canonical Evidence Graph/catalog, exact and lexical seed retrieval, deterministic citations, **required graph-and-material-conflict closure**, strict ordinary Evidence Package assembly, shared Python/CLI/MCP evidence surfaces, static review reports, immutable releases, activation, and rollback—without implementing Phase 3 dense/RRF retrieval or Phase 4 high-accuracy reranking/supporting-context enhancements.

### 2.2 Main Phase 2 purpose

Any statement that Phase 2 is only a direct-retrieval milestone is superseded to the extent that it implies a user-facing exact/lexical result may omit required context/conflict closure.

Phase 2 remains the **Exact Retrieval MVP** because its candidate selection is exact/lexical. The evidence returned from those seeds is nevertheless context-complete according to the current ordinary contract.

### 2.3 Main Phase 2 in-scope list

Add the following current-design responsibilities to Phase 2 scope:

- complete release-validated Evidence Graph relations needed by required traversal;
- closed required-context rule set;
- deterministic required-first traversal and source materialization;
- material-conflict build records and canonical position covers;
- runtime graph/conflict least fixed point;
- strict `context_targets` and `conflicts` projections;
- central Evidence Package serialization/validation;
- complete ordinary `search_evidence`, `get_clause`, and `get_context` semantics;
- shared Python/CLI/MCP evidence behavior;
- end-to-end context/conflict/evidence release gates.

### 2.4 Main Phase 2 out-of-scope list

Remove ordinary deterministic Evidence Graph traversal, required-context closure, material-conflict closure, final ordinary Evidence Package assembly, and the basic evidence tools from the Phase 2 out-of-scope list.

Phase 2 remains out of scope for:

- chunk embeddings;
- vector search;
- embedding-model selection;
- lexical+dense RRF;
- semantic/hybrid retrieval;
- query-embedding model loading;
- cross-encoder reranking;
- Phase 4 high-accuracy candidate reranking;
- Phase 4 additional supporting-context expansion;
- Phase 4 table/cross-reference high-accuracy improvements beyond the ordinary correctness baseline;
- Phase 4 expanded high-accuracy warning/refusal evaluation;
- ANN unless introduced by a later separately approved design.

### 2.5 "Do not expose incomplete final evidence tools" section

The old compatibility strategy—keeping only direct retrieval primitives and withholding `search_evidence`/`get_clause` because closure was allegedly Phase 4—is superseded.

The corrected rule is the opposite:

> Phase 2 must not expose **incomplete** direct retrieval as if it were an Evidence Package. Its public ordinary exact/lexical evidence surfaces must run required graph/conflict closure and strict serialization. Direct lookup/lexical functions may remain internal primitives, but they do not substitute for the public evidence contract.

### 2.6 Cross-reference traversal statements

Any old Phase 2 text saying cross-reference/relationship rows are compiled now but not traversed until Phase 4 is superseded for **required** traversal.

Phase 2 runtime traverses only the exact current Section 19 required rules. Phase 4 later adds supporting-context high-accuracy behavior; diagnostic traversal remains explicit inspection behavior.

### 2.7 CLI statements

Any statement describing Phase 2 `clausesift search` or `get-clause` as a direct/diagnostic context-incomplete milestone command is superseded.

The commands must call the shared context-complete evidence service.

### 2.8 MCP statements

Any statement that Phase 2 must advertise only metadata/list/page/release surfaces and return `feature_unavailable` for ordinary `search_evidence`, `get_clause`, `get_context`, clause/source evidence resources is superseded where those surfaces are part of current Section 22 Phase 2 behavior.

They must be implemented with the exact current success/error schemas and closure semantics.

`feature_unavailable` remains correct only for genuinely unavailable later capabilities such as an explicit `hybrid`/reranker-dependent mode in a Phase 2-only runtime.

### 2.9 Release-gate statements

Any gate appendix statement that treats runtime required context, material conflict, or ordinary Evidence Package correctness as Phase4-only or `not_implemented_in_phase_2` is superseded.

Those are Phase 2 blocking correctness gates under the current design.

### 2.10 Phase 4 handoff statements

Any handoff saying Phase 4 newly introduces deterministic required-context traversal, material-conflict closure, or the ordinary evidence tools is superseded.

Phase 4 receives those as lower-phase invariants.

## 3. Corrected Phase 2 architecture

The Phase 2 runtime path is:

```text
validated request
  -> deterministic query analysis available without semantic model
  -> exact/identifier and/or lexical seed retrieval
  -> deterministic required Evidence Graph closure
  -> deterministic material-conflict closure
  -> repeat graph/conflict closure to least fixed point
  -> strict ordinary Evidence Package assembly
  -> Python / CLI / MCP projection
```

The candidate-selection stage and the evidence-correctness stage are separate.

A later Phase 3 hybrid path changes only seed retrieval/ranking before entering this same evidence service.

A later Phase 4 high-accuracy path adds reranking/supporting context around the same ordinary required baseline.

## 4. Corrected Phase 2 build pipeline

After existing parser/canonical/page/chunk/catalog work, Phase 2 additionally builds and validates:

1. complete structural relation projections;
2. exact semantic cross-reference occurrences and uniquely resolved, origin-authorized navigable edges;
3. edge/occurrence identities and provenance;
4. executable required-context rule configuration and release identity;
5. material-conflict candidates and required-context comparison projections;
6. final conflict decision records;
7. canonical conflict-position source covers;
8. context/conflict catalog records and indexes needed by runtime closure;
9. complete source/build lineage references;
10. independent release validation and single-clause worst-case closure proof.

The release is assembled only after these artifacts and Phase 2 evidence gates pass.

## 5. Corrected Phase 2 runtime responsibilities

Phase 2 runtime owns:

- active-release validation;
- exact/lexical seed retrieval;
- exact metadata filtering;
- required context traversal;
- material-conflict fixed point;
- strict source-backed evidence/context-target/conflict projection;
- warnings/completeness/error routing;
- metadata/list/page/release surfaces;
- authorized page-resource access;
- shared Python service;
- CLI projection;
- MCP projection;
- cancellation/deadline/admission/output-budget behavior already specified by existing appendices.

Phase 2 runtime does not need an embedding or reranker model.

## 6. Corrected package/module structure

Extend the existing recommended structure with explicit Phase 2 ownership such as:

```text
src/clausesift/
├── builder/
│   ├── references/
│   ├── context/
│   ├── conflicts/
│   └── release/
├── runtime/
│   ├── retrieval/
│   ├── context/
│   ├── conflicts/
│   ├── evidence/
│   └── release.py
├── mcp/
└── evaluation/
```

Exact filenames may differ. The mandatory boundaries are:

- relationship/context/conflict compilation is build-time and query-independent where the design says so;
- runtime traverses only verified release data;
- one evidence service owns closure and serialization;
- adapters do not reimplement graph/conflict logic;
- source authority remains separate from retrieval metadata.

## 7. Corrected implementation sequence

The full Phase 2 sequence is now:

1. package/dependency/workspace bootstrap;
2. manifest schema, registration, source verification, approval, relations;
3. change detection;
4. Phase 1 parser routing/validation integration;
5. canonical model and evidence vocabulary;
6. classification provenance;
7. page provenance;
8. standards-aware chunking and exact lookup sets;
9. strict relationship occurrence extraction/resolution and graph edge identities;
10. SQLite catalog with all graph/relationship invariants;
11. lexical engine benchmark/selection and immutable lexical index;
12. deterministic citations and source/build lineage;
13. **required-context rule compilation and source-cover support**;
14. **material-conflict detection/classification/decision records and position covers**;
15. **independent graph/context/conflict release validation**;
16. exact/lexical direct seed service;
17. **required graph traversal**;
18. **material-conflict fixed-point closure**;
19. **strict Evidence Package serializer**;
20. **shared Python evidence API**;
21. **context-complete CLI retrieval**;
22. **context-complete MCP evidence tools/resources**;
23. metadata/list/page/release surfaces;
24. Phase 2 split-integrity, lexical, classification, context, conflict, citation, and end-to-end evidence gates;
25. immutable release assembly/checksums/read-only smoke validation;
26. activation/rollback and runtime startup validation;
27. protocol/admission/cancellation/failure-injection suites;
28. final Phase 2 report and handoff to Phase 3.

Steps 13-22 are the material current-design corrective addition.

## 8. Corrected Phase 2 release gates

Phase 2 activation requires all previously valid gates plus the current ordinary evidence correctness gates.

At minimum the final candidate must pass:

- manifest/source/parser/canonical/page/chunk/catalog integrity;
- lexical held-out Recall@20 and Top-5 gates;
- `node_type`, `normative_status`, and `source_modality` classification gates;
- exact clause-set completeness;
- citation/page accuracy;
- relationship resolution and release-tier policy;
- deterministic required-context rule fixtures;
- **zero required-context omissions on the applicable independently reviewed context gate**;
- deterministic material-conflict record/cover fixtures;
- **zero material-side omissions on the applicable independently reviewed conflict gate**;
- `context_targets` correctness;
- typed warning/completeness correctness;
- Python/CLI/MCP semantic equivalence;
- release schema/hash/lineage validation;
- required single-clause closure bound proof;
- corruption/failure injection;
- read-only smoke validation;
- activation and rollback.

A missing applicable evidence-semantics gate, missing reviewed cases, execution failure, or insufficient release evidence is blocking rather than silently skipped.

## 9. Evaluation-data governance

Existing Phase 0/Phase 2 split integrity and retry/rotation governance remains in force for the lexical/classification gates it currently covers.

For the newly Phase2-owned context/conflict/evidence gates:

- use independently reviewed expected context/conflict labels from the Phase 0 corpus;
- keep development/diagnostic material separate from decisive release evidence;
- preregister the exact candidate/rule/release identity and decisive split before observation;
- do not tune traversal/conflict rules against observed decisive cases;
- changing a behavior-bearing context/conflict/serializer rule invalidates stale decisive evidence;
- retain all failures in the audit trail.

If an existing retry policy document is narrower than these newly added gate families, the implementation must extend it explicitly rather than pretending the old lexical-only wording covers them.

## 10. Corrected Definition of Done

Phase 2 is complete only when all applicable current-design responsibilities pass.

Specifically:

1. all approved source/manifests compile deterministically into a validated canonical release;
2. exact lookup and lexical retrieval are deterministic and edition-safe;
3. required graph relationships are complete enough to satisfy release policy;
4. every ordinary exact/lexical evidence seed receives required-context closure;
5. every material conflict is closed to all required positions;
6. graph/conflict fixed point is deterministic and bounded;
7. required overflow fails with `context_limit_exceeded` and no partial package;
8. strict Evidence Package serialization reproduces source/catalog/lineage facts exactly;
9. ordinary `search_evidence`, `get_clause`, and `get_context` meet current design semantics;
10. Python, CLI, and MCP use one shared evidence service;
11. all Phase 2 deterministic and held-out gates pass;
12. immutable release assembly, activation, startup, and rollback validation pass;
13. no Phase 3 dense/RRF or Phase 4 high-accuracy additions have been pulled into this phase.

## 11. Corrected handoff to Phase 3

Phase 3 receives a stable lower-phase service with:

- exact/lexical seed retrieval;
- canonical IDs and edition-safe metadata filtering;
- strict relationship/context/conflict artifacts;
- deterministic required graph/conflict closure;
- ordinary strict Evidence Package behavior;
- complete source/build/assembly lineage;
- Python/CLI/MCP evidence interfaces;
- release/cache/integrity/activation/rollback contracts.

Phase 3 adds only its design-owned semantic seed-selection capabilities:

- embedding benchmark/selection;
- chunk embeddings;
- exact dense retrieval;
- lexical+dense RRF;
- deterministic Phase 3 query preprocessing/classification;
- Phase 3 evaluation/release identity.

Its seeds enter the Phase 2 evidence service unchanged.

## 12. Corrected handoff to Phase 4

Phase 4 receives both the Phase 2 ordinary evidence baseline and the Phase 3 hybrid seed path.

Current Phase 4 adds only the high-accuracy improvements assigned by `docs/design.md`, including:

- cross-encoder reranking;
- supporting-context expansion for high-accuracy retrieval;
- improved high-accuracy table/cross-reference behavior;
- expanded high-accuracy warning/refusal evaluation.

Phase 4 does **not** newly introduce ordinary required-context closure, material-conflict closure, basic Evidence Package assembly, or the basic evidence tools.

## 13. Corrective plan-set authority map

Read the Phase 2 documents with this precedence:

1. current `docs/design.md`;
2. this `phase-2-current-design-correction.md` for phase ownership and corrected orchestration;
3. `phase-2-required-context-closure.md` for required graph closure;
4. `phase-2-material-conflict-closure.md` for conflict build/runtime closure;
5. `phase-2-evidence-service.md` for final ordinary Evidence Package/shared interfaces;
6. existing Phase 2 appendices for all unchanged detailed contracts;
7. the original `phase-2-exact-retrieval-mvp.md` where it does not conflict with items 1-5.

An implementer must not choose an older statement merely because it is more convenient.

## 14. Scope discipline for review

Review of this corrective PR must remain Phase 2-scoped.

Valid review topics include whether the corrected Phase 2 plan now completely implements the ordinary exact/lexical evidence behavior assigned by the current design and whether the existing Phase 2 documents remain internally consistent after this correction.

Do not require Phase 3 embeddings/RRF or Phase 4 reranking/supporting-context implementation details in this PR.
