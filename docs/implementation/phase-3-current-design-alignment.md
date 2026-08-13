# Phase 3 Current Design Alignment

**Project:** ClauseSift  
**Phase:** 3 — Hybrid Retrieval  
**Status:** Normative Phase 3 implementation-plan clarification  
**Product-intent authority:** `docs/design-brief.md`  
**Design rulebook:** `docs/design-principles.md`  
**Detailed design authority:** `docs/design.md`  
**Companion plan:** `docs/implementation/phase-3-hybrid-retrieval.md`

## 1. Purpose and precedence

This document aligns the Phase 3 implementation plan with the current repository design authority while preserving the implementation-phase ownership actually defined by `docs/design.md` and the already merged Phase 2 implementation plan.

Where an earlier Phase 3 document claims that Phase 2 already implemented runtime required-context traversal, material-conflict closure, or final context-complete evidence tools, that claim is superseded by this document.

This clarification changes only Phase 3 planning. It does not add Phase 2 implementation work and does not pull Phase 4 implementation into Phase 3.

## 2. Design authority hierarchy

Phase 3 must remain consistent with all three design levels:

1. `docs/design-brief.md` defines product intent;
2. `docs/design-principles.md` defines durable decision rules;
3. `docs/design.md` defines technical contracts and implementation ownership.

The brief and principles require the finished product to preserve required context and material conflicts. They do not, by themselves, prove that those runtime capabilities were already implemented by an earlier phase.

For implementation sequencing, `docs/design.md` remains authoritative.

## 3. Actual Phase 2 prerequisite available to Phase 3

The merged Phase 2 plan provides the deterministic exact/lexical retrieval foundation that Phase 3 extends, including:

- approved manifests and canonical document identity;
- canonical nodes/chunks/sources and edition-safe identities;
- page/source provenance and deterministic citations;
- SQLite catalog persistence and release validation;
- exact clause/direct lookup primitives;
- lexical retrieval primitives;
- immutable release, activation, rollback, integrity, and runtime admission contracts;
- Phase 2 build/source lineage;
- basic metadata/list/page/release runtime/MCP surfaces that do not require final context closure.

Phase 2 deliberately does **not** provide the final runtime required-context traversal, material-conflict fixed-point closure, or context-complete evidence-facing tools.

Phase 3 must not pretend otherwise.

## 4. Phase 3 responsibility

Phase 3 changes candidate retrieval only.

Its runtime responsibility is:

```text
validated query
  -> deterministic query preprocessing and analysis
  -> exact and/or lexical and/or dense candidate retrieval
  -> lexical+dense RRF where hybrid is selected
  -> deterministic canonical hybrid seed candidate set
  -> strict Phase 4 handoff
```

The hybrid seed set retains canonical document/chunk/source identity and complete retrieval provenance so later stages can perform context and conflict closure without reconstructing or guessing identity.

Dense similarity and RRF are retrieval metadata only. They never create source facts, applicability, precedence, context relationships, or citations.

## 5. Phase 3 public-surface boundary

Phase 3 may expose internal/service diagnostics needed to test hybrid retrieval, but it must not advertise a final success contract that claims context-complete Evidence Package semantics before the Phase 4 closure pipeline exists.

In particular, Phase 3 must not newly claim successful final implementations of:

- context-complete `search_evidence`;
- context-complete `get_clause`;
- `get_context`;
- final clause/source evidence resources;
- final Evidence Package assembly;
- complete query-specific assembly lineage;
- material-conflict fixed-point closure.

Existing Phase 2 exact/lexical primitives and metadata/page/release surfaces remain available according to their own contracts.

## 6. Query mode implications

### 6.1 Exact-dominant requests

Exact identifiers, explicit clauses, product/model numbers, and other strong anchors remain eligible for exact/lexical-first processing and remain model-free when the chosen path does not require dense retrieval.

### 6.2 Hybrid natural-language requests

A Phase 3 hybrid request may use:

- lexical retrieval;
- current-query embedding;
- exact dense retrieval over the memory-mapped chunk matrix;
- deterministic RRF;
- deterministic retrieval-seed ordering.

The result of Phase 3 is the strict seed handoff, not a claim that required graph context has already been attached.

### 6.3 Auto resolution

`auto` may select only capabilities actually available in the active release/runtime. A dense-capability failure may fall back only where the detailed design explicitly permits `auto` fallback, with the required typed warning.

### 6.4 Explicit hybrid failure

An explicit hybrid request whose dense capability cannot execute fails through the design's typed capability contract rather than silently becoming lexical-only.

## 7. Phase 4 handoff

Phase 4 consumes the Phase 3 seed candidate set and owns the later high-accuracy/evidence-completeness pipeline defined by the detailed design, including as applicable:

- cross-encoder reranking;
- deterministic required Evidence Graph context traversal;
- material-conflict closure;
- supporting-context expansion;
- improved table/cross-reference handling;
- final Evidence Package assembly;
- final context-complete evidence-facing Python/CLI/MCP semantics;
- high-accuracy warning/refusal evaluation.

Phase 3 must provide a versioned handoff containing enough canonical identity and retrieval provenance for Phase 4 to perform these operations deterministically.

## 8. Phase 3 evaluation consequence

Phase 3 blocking evaluation focuses on the retrieval stage that Phase 3 actually implements.

Required slices include:

- dense Recall@20 / Top-5;
- hybrid Recall@20 / Top-5;
- lexical-vs-dense complementarity;
- exact-anchor preservation;
- wrong-edition/wrong-document resistance;
- metadata-filter correctness;
- deterministic RRF ordering;
- query-classifier/routing correctness;
- query-preprocessing identity/invalidation correctness;
- source/chunk/document identity preservation in the seed handoff;
- retrieval-provenance completeness.

Phase 3 does **not** claim blocking proof of context closure, conflict fixed-point completeness, final Evidence Package equivalence, or refusal/answerability behavior that has not yet been implemented.

Those become blocking when the owning Phase 4 capability exists.

## 9. Release and lineage consequence

Phase 3 release identity adds the behavior-bearing inputs introduced by hybrid retrieval, including:

- embedding model and model-asset identity;
- deterministic embedding/query preprocessing identity;
- embedding artefact identity;
- exact dense backend/configuration;
- query-analysis/classifier configuration;
- RRF/fusion configuration;
- candidate-pool configuration;
- relevant dependency/toolchain identity.

Phase 3 extends release build lineage with the corresponding derived retrieval artefacts and channel provenance.

It does not invent Phase 4 context-path/assembly lineage early.

## 10. Phase-boundary regression tests

Add Phase 3 tests proving:

1. hybrid seed retrieval preserves canonical `document_id`, `chunk_id`, and `source_id`;
2. exact anchors are never silently replaced by semantic near-matches;
3. different editions remain distinct through lexical/dense fusion;
4. metadata filters apply consistently to lexical and dense candidate paths;
5. all contributing channel ranks/scores/artefact hashes remain attributable after deduplication/fusion;
6. identical release/query/configuration inputs produce identical seed ordering;
7. disabling dense capability leaves Phase 2 exact/lexical primitives unchanged;
8. Phase 3 does not invoke or claim Phase 4 context traversal, conflict closure, reranker, supporting-context, or final Evidence Package behavior;
9. the Phase 4 handoff has a strict versioned schema and all canonical IDs/provenance needed for later closure.

## 11. Phase 3 acceptance corrections

Phase 3 is complete only when:

1. evaluated chunk embeddings are built and release-validated;
2. memory-mapped exact dense retrieval is deterministic and safe;
3. deterministic query preprocessing/classification is release-bound;
4. lexical+dense RRF is deterministic and evaluation-backed;
5. exact and lexical retrieval remain first-class;
6. hybrid seed retrieval preserves edition-safe canonical identity and complete retrieval provenance;
7. Phase 3 release/cache/lineage invalidation includes every behavior-bearing hybrid input;
8. the Phase 4 seed handoff is strict and versioned;
9. Phase 3 does not advertise context-complete evidence semantics that require Phase 4;
10. all Phase 3-specific release and regression gates pass.

## 12. Scope discipline

If a reviewer identifies a missing capability that is necessary only for Phase 4 context traversal, reranking, conflict closure, supporting context, final Evidence Package assembly, or refusal/high-accuracy behavior, record/defer it to Phase 4 rather than expanding this Phase 3 PR.

If the detailed design itself later changes implementation ownership and moves one of those capabilities earlier, that must be an explicit design/phase-boundary change before the Phase 3 plan is expanded.
