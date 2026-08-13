# Phase 3 Review Clarifications

**Project:** ClauseSift  
**Phase:** 3 — Hybrid retrieval  
**Status:** Normative Phase 3 implementation-plan clarification  
**Primary design authority:** `docs/design.md`  
**Companion plans:** `docs/implementation/phase-3-hybrid-retrieval.md`, `docs/implementation/phase-3-current-design-alignment.md`, `docs/implementation/phase-3-query-preprocessing-identity.md`

## 1. Purpose and precedence

This document closes two Phase 3 review findings on the final approval PR.

Where the existing Phase 3 plan set conflicts with either clarification below, this document is authoritative for Phase 3 implementation. It does not add Phase 4 work to Phase 3.

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

## 3. Phase boundary for required-context and conflict closure

Phase 3 must **not** claim that the committed Phase 2 implementation plan already provides runtime required-context traversal, material-conflict fixed-point closure, or final context-complete evidence tools.

The committed Phase 2 implementation plan deliberately deferred those runtime capabilities. The detailed design's implementation sequence assigns the full high-accuracy Evidence Graph traversal/context expansion work to Phase 4.

Therefore the Phase 3 deliverable is:

1. exact/lexical retrieval remains available from the Phase 2 retrieval primitives;
2. Phase 3 adds evaluated dense retrieval;
3. Phase 3 adds deterministic query analysis/routing;
4. Phase 3 adds deterministic lexical+dense fusion and produces a canonical hybrid **seed candidate set**;
5. Phase 3 validates seed recall, ranking/fusion behavior, identity, release integrity, and interface-independent internal service semantics;
6. Phase 4 consumes those seeds and implements the final required-context traversal, material-conflict closure, cross-encoder reranking/supporting-context behavior, final Evidence Package assembly, and context-complete evidence-facing API/MCP success contracts.

Phase 3 may define the typed handoff required by Phase 4, but it must not implement or advertise the missing Phase 4 closure as though it had been inherited from Phase 2.

## 4. Correction to downstream evidence-semantics regression wording

The Phase 3 main plan's Section 18.5 language about proving required parent scope, applicability, dependencies/definitions/exceptions, table context, conflict closure, and final Python/CLI/MCP evidence equivalence is **not a Phase 3 blocking gate for capabilities not yet implemented**.

For Phase 3, the blocking regression obligation is limited to proving that the hybrid seed subsystem preserves the information needed by the later Phase 4 closure pipeline:

- canonical `document_id`, `chunk_id`, and `source_id` are preserved;
- document edition and metadata filters are preserved;
- exact-hit identity is never silently replaced by a semantic near-match;
- all contributing retrieval-channel ranks/scores/artefact hashes remain attributable;
- fusion never removes a source solely because another edition has similar text;
- the seed set is deterministic under identical release/query/configuration inputs;
- the Phase 4 handoff contains enough canonical identity and retrieval provenance to run required context/conflict closure later;
- no Phase 3 public surface falsely claims `context_completeness: complete` or a final Evidence Package when the Phase 4 closure has not run.

Context-completeness, conflict-closure, final citation-package equivalence, refusal/answerability, and high-accuracy evidence semantics remain Phase 4 acceptance criteria.

## 5. Product-intent documents vs technical implementation ownership

`docs/design-brief.md` and `docs/design-principles.md` describe product intent and durable rules. They require the dependable product baseline to return required context and material conflicts, but they do not by themselves prove that a lower implementation phase has already built the necessary runtime traversal.

`docs/design.md` remains the technical authority for implementation ownership and phase sequencing. When a product-level requirement spans several phases, an implementation plan must not treat the requirement as already implemented merely because it is required by the product baseline.

If the project later decides that required-context/conflict closure must be moved earlier than Phase 4, that is a detailed-design/phase-boundary change and should be made explicitly in the design and corresponding implementation plan rather than inferred inside this Phase 3 PR.

## 6. Phase 3 acceptance correction

Phase 3 is complete only when:

1. query-preprocessing identity is part of every frozen candidate/release/evaluation identity where behavior depends on it;
2. embedding model selection and held-out confirmation remain leakage-safe;
3. chunk embeddings and exact vector search satisfy their release contracts;
4. query classification/routing is deterministic and release-bound;
5. lexical+dense fusion is deterministic and evaluation-backed;
6. hybrid seed retrieval preserves canonical source/document/edition identity and complete retrieval provenance;
7. the seed handoff to Phase 4 is strict and versioned;
8. Phase 3 does not advertise final context-complete evidence semantics that require Phase 4 traversal/assembly;
9. all Phase 3-specific regression/release gates pass.

These corrections stay strictly inside Phase 3 scope: they tighten Phase 3 candidate identity and remove an invalid claim that a later-phase capability already exists.
