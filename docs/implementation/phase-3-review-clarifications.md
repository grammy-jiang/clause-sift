# Phase 3 Review Clarifications

**Project:** ClauseSift  
**Phase:** 3 — Hybrid retrieval  
**Status:** Normative Phase 3 implementation-plan clarification  
**Primary design authority:** `docs/design.md`  
**Companion plans:** `docs/implementation/phase-3-hybrid-retrieval.md`, `docs/implementation/phase-3-current-design-alignment.md`, `docs/implementation/phase-3-query-preprocessing-identity.md`

## 1. Purpose and precedence

This document closes the final Phase 3 review findings while preserving the implementation ownership defined by current `docs/design.md`.

Where an earlier Phase 3 statement conflicts with this clarification, this document is authoritative for Phase 3 implementation.

It does not implement missing Phase 2 work inside Phase 3 and does not reassign Phase 2 correctness requirements to Phase 4.

## 2. Frozen candidate identity includes query preprocessing

The frozen Phase 3 candidate identity used for model-selection separation, held-out confirmation, retry governance, cache/release identity, and reproducibility includes **query-preprocessing identity as a required behavior-bearing input**.

The complete frozen identity therefore includes, in addition to the items already enumerated by `phase-3-hybrid-retrieval.md` Section 19:

- query-preprocessing schema/rule-set version;
- Unicode normalization policy/version;
- whitespace/trim policy/version;
- query text canonicalization configuration hash;
- identifier/number/unit extraction preprocessing version where it changes downstream routing or embedding input;
- exact normalized-query construction version;
- hash of the complete release-bound query-preprocessing configuration.

This identity is the same contract defined in `phase-3-query-preprocessing-identity.md`; it is not optional metadata.

A behavior-bearing query-preprocessing change after a candidate is frozen creates a new candidate and invalidates prior final-gate evidence under the existing held-out/retry policy, even when the embedding model, RRF parameters, and classifier rules are unchanged.

Tests must prove that changing each behavior-bearing preprocessing component changes the frozen candidate/release identity and prevents reuse of stale confirmation evidence.

## 3. Current detailed-design ownership of required closure

Current `docs/design.md` explicitly places all of the following in **Phase 2: Exact retrieval MVP**:

- deterministic required Evidence Graph context closure;
- deterministic material-conflict closure;
- basic Python, CLI, and MCP retrieval interfaces that use those correctness semantics.

Current Phase 4 is limited to high-accuracy improvements such as cross-encoder reranking, supporting-context expansion, improved tables/cross-references, and expanded high-accuracy warning/refusal evaluation.

Therefore Phase 3 must not move ordinary required-context or material-conflict closure to Phase 4.

## 4. Identified lower-phase implementation-plan gap

The already merged Phase 2 implementation-plan documents were written before the current design-boundary change and still defer runtime required-context/material-conflict closure to Phase 4.

That is a **lower-phase implementation-plan gap** relative to current `docs/design.md`.

Phase 3 must not hide this gap by:

- silently implementing Phase 2 closure inside Phase 3;
- pretending the old Phase 2 plan already contains the closure;
- reassigning the closure to Phase 4;
- weakening Phase 3 integration/evidence correctness gates.

Instead, a separate Phase 2 corrective implementation-plan PR must reconcile the merged Phase 2 plan with current `docs/design.md` and define the missing Phase 2 required-context/material-conflict closure work.

That corrective PR is outside this Phase 3 PR's implementation scope.

## 5. Blocking prerequisite for Phase 3 implementation execution

The Phase 3 implementation plan may be reviewed and merged as a plan, but **Phase 3 implementation execution may not be declared complete or release-capable until the Phase 2 corrective prerequisite has been merged and the required closure baseline exists**.

Before a Phase 3 release candidate can pass its final integration gate, the repository must provide a validated lower-phase service/catalog baseline that performs:

- required parent scope closure;
- applicability closure;
- required dependency/definition/exception closure;
- required table context;
- deterministic material-conflict closure;
- bounded context traversal/failure semantics;
- ordinary strict Evidence Package assembly through the shared Python/CLI/MCP service layer.

Phase 3 consumes that baseline; it does not reimplement it.

## 6. Correct Phase 3 runtime composition

Once the Phase 2 corrective prerequisite exists, Phase 3 changes candidate retrieval only:

```text
validated query
  -> deterministic query preprocessing / analysis
  -> exact and/or lexical and/or dense candidate retrieval
  -> lexical+dense RRF where hybrid is selected
  -> deterministic retrieval-seed ordering
  -> inherited validated Phase 2 required-context closure
  -> inherited validated Phase 2 material-conflict closure
  -> inherited strict Evidence Package serialization
  -> Python / CLI / MCP response
```

Dense similarity and RRF stop at the retrieval-seed boundary. They cannot create or weaken source facts, applicability, context relations, conflicts, citations, or precedence.

## 7. Phase 3 regression obligation

Phase 3 must prove both candidate-retrieval quality and preservation of the lower-phase evidence contract once the prerequisite baseline exists.

Blocking regression slices include:

- dense and hybrid Recall@20 / Top-5;
- exact-anchor preservation;
- edition/document identity preservation;
- deterministic RRF ordering;
- query-preprocessing/classifier identity correctness;
- required parent/applicability/dependency/definition/exception context remains present after hybrid seed selection;
- required table context remains present;
- every material conflict side survives adverse lexical/dense/fusion ranks;
- context-limit behavior remains the inherited typed failure rather than truncated hybrid success;
- Python/CLI/MCP remain projections of one shared evidence service.

These downstream tests are not removed merely because the currently merged Phase 2 plan is stale; they become executable after the separate Phase 2 corrective prerequisite is merged.

## 8. Correct Phase 4 handoff

Phase 4 does **not** own ordinary required-context/material-conflict closure under current `docs/design.md`.

Phase 4 adds the high-accuracy improvements assigned by the design:

- cross-encoder reranking;
- supporting-context expansion for high-accuracy retrieval;
- improved tables and cross-references;
- expanded typed-warning and refusal evaluation for high-accuracy retrieval.

Phase 3 therefore hands a context-complete ordinary evidence path plus hybrid retrieval provenance into Phase 4 only after the Phase 2 prerequisite has been corrected and implemented.

## 9. Phase 3 acceptance correction

Phase 3 is complete only when:

1. query-preprocessing identity is part of every frozen candidate/release/evaluation identity where behavior depends on it;
2. embedding model selection and held-out confirmation remain leakage-safe;
3. chunk embeddings and exact vector search satisfy their release contracts;
4. query classification/routing is deterministic and release-bound;
5. lexical+dense fusion is deterministic and evaluation-backed;
6. exact/lexical behavior remains first-class;
7. the current-design Phase 2 required-context/material-conflict baseline exists through a separately reviewed Phase 2 corrective plan/implementation;
8. hybrid retrieval composes with that baseline without weakening evidence semantics;
9. all Phase 3-specific and inherited integration/release gates pass;
10. Phase 3 does not absorb Phase 4 reranking/supporting-context/high-accuracy work.

These corrections remain Phase 3-scoped: they define a blocking prerequisite and Phase 3 composition contract without implementing another phase's missing work.