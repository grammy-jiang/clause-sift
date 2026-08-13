# Phase 3 Current Design Alignment

**Project:** ClauseSift  
**Phase:** 3 — Hybrid Retrieval  
**Status:** Normative Phase 3 implementation-plan clarification  
**Product-intent authority:** `docs/design-brief.md`  
**Design rulebook:** `docs/design-principles.md`  
**Detailed design authority:** `docs/design.md`  
**Companion plan:** `docs/implementation/phase-3-hybrid-retrieval.md`

## 1. Purpose and precedence

This document aligns Phase 3 with the **current** `master` design authority.

Current `docs/design.md` assigns deterministic required Evidence Graph context closure and material-conflict closure to **Phase 2**, not Phase 4. The already merged Phase 2 implementation-plan documents predate that design-boundary change and therefore contain a known lower-phase planning gap.

Where any earlier Phase 3 text conflicts with this document, this document is authoritative.

This PR does not implement the missing Phase 2 work. It records the prerequisite and Phase 3 composition contract only.

## 2. Design authority hierarchy

Phase 3 must remain consistent with:

1. `docs/design-brief.md` — product intent;
2. `docs/design-principles.md` — durable design rules;
3. `docs/design.md` — exact technical contracts, phase ownership, limits, gates, and tests.

For implementation sequencing, `docs/design.md` is authoritative.

## 3. Current Phase 2 ownership

Current `docs/design.md` Phase 2 includes:

- manifests;
- canonical model;
- standards-aware chunking;
- SQLite catalog;
- clause lookup;
- lexical retrieval;
- deterministic citations;
- deterministic required Evidence Graph context closure;
- deterministic material-conflict closure;
- basic Python, CLI, and MCP retrieval interfaces;
- static review report;
- immutable release;
- candidate validation, activation, and rollback.

Therefore ordinary required-context/material-conflict closure is a lower-phase prerequisite for Phase 3.

## 4. Known Phase 2 implementation-plan gap

The merged Phase 2 implementation-plan set still reflects the older phase boundary and defers the runtime closure/evidence tools.

That stale plan does not change current design ownership. It creates a corrective prerequisite:

> Before Phase 3 implementation can be declared release-capable, a separate Phase 2 corrective implementation-plan/implementation change must bring the Phase 2 baseline into conformance with current `docs/design.md`.

The corrective Phase 2 work must be handled in its own phase-scoped PR and review. It must not be hidden inside this Phase 3 PR.

## 5. Phase 3 responsibility

Once the corrected Phase 2 baseline exists, Phase 3 changes candidate retrieval while preserving the inherited evidence contract.

```text
validated query
  -> deterministic query preprocessing / analysis
  -> exact and/or lexical and/or dense candidate retrieval
  -> lexical+dense RRF where hybrid is selected
  -> deterministic retrieval-seed ordering
  -> inherited Phase 2 required-context closure
  -> inherited Phase 2 material-conflict closure
  -> inherited strict Evidence Package serialization
  -> Python / CLI / MCP response
```

Dense similarity and RRF end at the retrieval-seed boundary. They cannot create source facts, applicability, context relationships, conflict decisions, precedence, or citations.

## 6. Query mode implications

### 6.1 Exact-dominant requests

Exact identifiers, clauses, product/model numbers, and other strong anchors remain exact/lexical-first and model-free when the selected path needs no dense channel.

### 6.2 Hybrid natural-language requests

A validated hybrid path may use:

- lexical retrieval;
- current-query embedding;
- exact dense retrieval;
- deterministic RRF;
- deterministic seed ordering.

Those seeds then pass through the inherited corrected Phase 2 closure/evidence service.

### 6.3 Auto resolution

`auto` may select only capabilities present in both the active release and runtime. Any fallback follows the exact typed warning/failure contract in `docs/design.md`.

### 6.4 Explicit hybrid failure

An explicit hybrid request whose dense capability is unavailable fails through the typed capability contract rather than silently relabelling lexical-only output as hybrid.

## 7. Phase 4 handoff

Current Phase 4 is **High-accuracy retrieval** and adds:

- cross-encoder reranking;
- supporting-context expansion for high-accuracy retrieval;
- improved tables and cross-references;
- expanded typed-warning and refusal evaluation for high-accuracy retrieval.

Phase 4 does not newly introduce the ordinary required-context/material-conflict closure that current design already assigns to Phase 2.

## 8. Evaluation consequences

Phase 3 must evaluate both candidate quality and preservation of inherited evidence semantics once the corrected Phase 2 prerequisite exists.

Required Phase 3 slices include:

- dense Recall@20 / Top-5;
- hybrid Recall@20 / Top-5;
- lexical/dense complementarity;
- exact-anchor preservation;
- wrong-edition/wrong-document resistance;
- metadata-filter correctness;
- deterministic RRF ordering;
- query-preprocessing/classifier identity correctness;
- required parent/applicability/dependency/definition/exception context remains present through hybrid retrieval;
- required table context remains present;
- every material conflict side survives adverse candidate ranks;
- context-limit behavior remains typed failure rather than truncated hybrid success;
- deterministic citations/source/edition identity remain unchanged;
- Python/CLI/MCP project one shared evidence service.

The currently stale Phase 2 plan does not authorize dropping these downstream gates; it means they are blocked until the Phase 2 corrective prerequisite is complete.

## 9. Release and lineage consequences

Phase 3 release identity adds all behavior-bearing hybrid inputs, including:

- embedding model and model-asset identity;
- deterministic query-preprocessing identity;
- embedding artefact identity;
- exact dense backend/configuration;
- query-analysis/classifier configuration;
- RRF/fusion configuration;
- candidate-pool configuration;
- relevant dependency/toolchain identity.

Phase 3 lineage extends the existing evidence lineage with retrieval-channel and derived-artefact provenance; it does not create a parallel lineage model.

## 10. Phase-boundary regression tests

Add Phase 3 integration tests proving, once the corrected Phase 2 prerequisite exists:

1. exact/lexical behavior retains the same required-context/material-conflict semantics after Phase 3 is enabled;
2. a hybrid seed for an isolated requirement receives the inherited required scope/applicability/exception context;
3. a dense hit intersecting one material-conflict position cannot produce a one-sided final package;
4. hybrid ranking cannot erase required conflict sides;
5. context-limit failure remains failure rather than degraded hybrid success;
6. Python, CLI, and MCP project the same hybrid evidence result from the shared service;
7. disabling dense capability leaves exact/lexical semantics unchanged;
8. Phase 3 does not invoke Phase 4 reranker/supporting-context/high-accuracy behavior.

## 11. Phase 3 acceptance

Phase 3 is not complete unless:

1. the separate Phase 2 corrective prerequisite has brought required-context/material-conflict closure into conformance with current `docs/design.md`;
2. evaluated chunk embeddings are built and release-validated;
3. memory-mapped exact dense retrieval is deterministic and safe;
4. deterministic query preprocessing/classification is release-bound;
5. lexical+dense RRF is deterministic and evaluation-backed;
6. exact and lexical retrieval remain first-class;
7. hybrid retrieval composes with the inherited Phase 2 closure without weakening evidence semantics;
8. release/cache/lineage invalidation covers every behavior-bearing Phase 3 input;
9. all Phase 3-specific and inherited integration/release gates pass;
10. Phase 3 does not absorb Phase 4 reranking/supporting-context/high-accuracy work.

## 12. Scope discipline

The Phase 2 corrective prerequisite must be created and reviewed separately. Review of this Phase 3 PR may verify that the prerequisite is correctly declared, but must not expand this PR into implementation details owned by Phase 2.

Likewise, Phase 4 reranking/supporting-context/high-accuracy improvements remain outside this Phase 3 PR.