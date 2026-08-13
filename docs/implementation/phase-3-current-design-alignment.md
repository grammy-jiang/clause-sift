# Phase 3 Current Design Alignment

**Project:** ClauseSift  
**Phase:** 3 — Hybrid Retrieval  
**Status:** Normative Phase 3 implementation-plan clarification  
**Current product-intent authority:** `docs/design-brief.md`  
**Current design rulebook:** `docs/design-principles.md`  
**Current detailed design authority:** `docs/design.md`  
**Companion plan:** `docs/implementation/phase-3-hybrid-retrieval.md`

## 1. Purpose and precedence

While the Phase 3 PR was under review, `master` advanced from the Phase 2 merge commit to a new design baseline that added `docs/design-brief.md`, added `docs/design-principles.md`, and revised `docs/design.md` implementation-phase boundaries.

This clarification aligns the Phase 3 plan with that **current** design baseline without adding implementation work owned by another phase.

Where the Phase 3 main plan or earlier Phase 3 clarification implies a different lower-phase prerequisite, public-pipeline boundary, or Phase 4 handoff, this document is authoritative.

It does **not** amend the already merged Phase 2 implementation-plan documents. Any separate Phase 2 documentation alignment required because the governing design changed after Phase 2 merged must be handled outside this Phase 3 PR.

## 2. Current design authority hierarchy

Phase 3 implementation decisions must remain consistent with all three current design levels:

1. `docs/design-brief.md` owns product intent;
2. `docs/design-principles.md` owns durable decision rules;
3. `docs/design.md` owns exact technical contracts, implementation choices, limits, gates, and tests.

For Phase 3, the particularly relevant design principles are:

- DP-01 — original sources remain authoritative;
- DP-03 — identity and provenance are deterministic;
- DP-04 — required context is correctness;
- DP-06 — compile offline and serve read-only;
- DP-07 — canonical evidence is separate from acceleration;
- DP-08 — publish only complete verified releases;
- DP-09 — components remain replaceable behind contracts;
- DP-10 — validate before use and fail closed;
- DP-11 — work is bounded and terminal;
- DP-13 — exact and lexical retrieval remain first-class;
- DP-14 — models are bounded assistants;
- DP-15 — Python, CLI, and MCP expose one strict evidence contract;
- DP-16 — behavior is versioned and deterministic;
- DP-17 — representative evidence selects components;
- DP-18 — proof matches the claim;
- DP-20 — optimize only after quality gates pass.

No Phase 3 optimization or semantic-retrieval improvement may weaken required context, edition safety, source fidelity, or public evidence semantics.

## 3. Revised Phase 2 prerequisite inherited by Phase 3

The current `docs/design.md` Phase 2 contract now includes, in addition to the earlier exact/lexical baseline:

- deterministic required Evidence Graph context closure;
- deterministic material-conflict closure;
- basic Python, CLI, and MCP retrieval interfaces that already return the required context-complete evidence semantics for the first usable path.

Therefore Phase 3 must treat the following as **lower-phase prerequisites**, not Phase 4 work:

- required parent scope;
- applicability context;
- dependencies;
- definitions;
- exceptions;
- required table context;
- every material conflict side;
- the bounded required-context traversal/closure rules needed to produce a safe first-release Evidence Package;
- the shared Python/CLI/MCP runtime service layer that exposes those semantics.

Phase 3 does not reimplement these lower-phase rules. It consumes them through their stable service/catalog contracts.

## 4. Correct Phase 3 runtime composition

The Phase 3 hybrid path changes **candidate retrieval**, not evidence meaning.

The Phase 3 runtime composition is:

```text
validated query
  -> deterministic query analysis / mode resolution
  -> exact and/or lexical and/or dense candidate retrieval
  -> lexical+dense RRF where hybrid is selected
  -> deterministic retrieval-seed ordering
  -> inherited Phase 2 required-context closure
  -> inherited Phase 2 material-conflict closure
  -> inherited strict Evidence Package serialization
  -> Python / CLI / MCP response
```

Dense similarity and RRF end at the retrieval-seed boundary. They do not authorize omission, weakening, or reinterpretation of the inherited required-context and conflict-closure stages.

If the inherited required closure cannot complete inside its declared bounds, Phase 3 follows the same typed failure/incomplete-required behavior as the current first-release contract. It must not return a semantically incomplete hybrid success merely because candidate retrieval succeeded.

## 5. Public Phase 3 hybrid capability

The current design no longer supports the main plan's earlier implication that Phase 3 hybrid behavior should remain only an internal diagnostic service until Phase 4.

Phase 3 may and should extend the **existing shared retrieval service** with the validated hybrid candidate path so that the already established Python, CLI, and MCP interfaces can use it without changing evidence semantics.

The public/service behavior must preserve:

- one request-validation path;
- one metadata-filter contract;
- one release identity;
- one canonical evidence/source identity system;
- one required-context/material-conflict closure implementation;
- one Evidence Package schema and serializer;
- one typed error/warning contract appropriate to the current design;
- deterministic citations and lineage.

Hybrid support must not create a separate "semantic search API" with weaker context or serialization guarantees.

## 6. Retrieval mode implications

Phase 3 query classification and mode resolution operate above the inherited evidence-assembly pipeline.

### 6.1 Exact-dominant requests

Exact identifiers, explicit clauses, model numbers, and other exact anchors remain eligible for exact/lexical-first behavior and must remain model-free where the selected mode requires no semantic channel.

### 6.2 Hybrid natural-language requests

A validated hybrid request may use:

- lexical retrieval;
- current-query embedding;
- exact dense retrieval;
- RRF;
- deterministic retrieval-seed ordering.

The resulting seeds then undergo the same required context and conflict closure as any other successful retrieval path.

### 6.3 Auto resolution

`auto` may select only capabilities present in both the installed runtime and active release. When it selects hybrid retrieval, the final result remains subject to the same required-context and conflict closure as exact/lexical retrieval.

### 6.4 Explicit hybrid failure

If an explicit hybrid request cannot execute because the active release or runtime lacks the validated dense capability, it must fail under the design's typed capability/failure contract rather than silently relabel a lexical-only result as hybrid.

## 7. Correct Phase 4 handoff

The current `docs/design.md` Phase 4 scope is **High-accuracy retrieval** and now consists of:

- cross-encoder reranking;
- **supporting-context expansion** for high-accuracy retrieval;
- improved tables and cross-references;
- expanded typed-warning and refusal evaluation for high-accuracy retrieval.

Phase 4 does **not** newly introduce the deterministic required-context or material-conflict closure needed for ordinary safe evidence. Those are already lower-phase correctness requirements.

Accordingly, every Phase 3 statement that says or implies any of the following is superseded:

- "required Evidence Graph traversal begins in Phase 4";
- "final context-complete evidence tools cannot be advertised until Phase 4";
- "Phase 3 hybrid results should remain diagnostic/internal solely because required context is unavailable";
- "Phase 4 owns ordinary required-context closure".

The correct handoff is:

```text
Phase 3
  -> validated exact/lexical/dense candidate retrieval
  -> deterministic lexical+dense RRF
  -> deterministic query classification/mode resolution
  -> inherited required context + material conflicts
  -> ordinary strict Evidence Package

Phase 4 adds
  -> cross-encoder reranking
  -> additional supporting context for high_accuracy
  -> higher-accuracy table/cross-reference handling
  -> expanded warning/refusal evaluation
```

## 8. Evaluation consequences

Phase 3 retrieval evaluation must not measure candidate recall in isolation and then ignore downstream evidence correctness.

In addition to lexical/dense/hybrid Recall@20 and Top-5 candidate gates, integration/regression suites must verify that using the hybrid channel does not alter or drop:

- required parent scope;
- applicability;
- dependencies;
- definitions;
- exceptions;
- required table context;
- material conflict sides;
- deterministic citations;
- source identity;
- edition identity;
- required typed warnings/failures;
- Evidence Package ordering and lineage rules inherited from the current lower-phase runtime.

Hybrid retrieval may change which seeds are found and their candidate rank. It may not change the deterministic meaning attached to a selected seed.

## 9. Release and lineage consequences

Phase 3 release identity still adds embedding, model-asset, dense-backend, RRF, and query-classifier behavior-bearing inputs as described by the Phase 3 plan and clarifications.

The release must also remain compatible with the already compiled lower-phase context/conflict rules and artifacts required by current `docs/design.md`.

Phase 3 lineage adds retrieval-channel and derived-artifact provenance without creating a second evidence lineage model.

## 10. Phase-boundary regression tests

Add Phase 3 integration tests proving:

1. the same exact/lexical query before and after enabling Phase 3 retains required-context/material-conflict semantics;
2. a hybrid natural-language query whose direct seed is an isolated requirement receives the inherited required parent/applicability/exception context;
3. a dense hit intersecting one side of a material conflict cannot produce a one-sided final package;
4. hybrid candidate ranking cannot remove a required conflict side;
5. a context-limit failure remains a failure rather than degrading to a context-incomplete hybrid success;
6. Python, CLI, and MCP project the same hybrid result from the shared service layer;
7. disabling dense capability leaves exact/lexical evidence semantics unchanged;
8. Phase 3 does not invoke Phase 4 supporting-context or reranker behavior.

## 11. Phase 3 acceptance corrections

Phase 3 is not complete unless, in addition to the existing Phase 3 criteria:

1. the hybrid path composes with the inherited required-context and material-conflict closure;
2. hybrid retrieval is available through the existing shared retrieval service/interfaces where the current design exposes retrieval modes;
3. exact/lexical first-class behavior remains intact;
4. candidate retrieval never bypasses required context or conflict completeness;
5. downstream Evidence Package semantics remain identical across exact/lexical/hybrid paths except for retrieval provenance/rank metadata that legitimately differs;
6. current Phase 4 responsibility is described as reranking plus **supporting** context/high-accuracy improvements, not ordinary required-context closure;
7. no Phase 2 implementation detail is added to this PR beyond declaring the current prerequisite contract.

## 12. Separate lower-phase alignment note

The governing design changed after the Phase 2 implementation-plan PR had already merged. This Phase 3 clarification does not silently rewrite Phase 2 history and does not expand the current PR into Phase 2 scope.

Before implementation execution relies on the complete plan set, the repository should separately reconcile any merged Phase 2 implementation-plan text that still reflects the older phase boundary. That reconciliation must be its own phase-scoped documentation change and review, not a Phase 3 review fix.
