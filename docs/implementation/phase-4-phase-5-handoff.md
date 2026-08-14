# Phase 4 to Phase 5 Handoff

**Phase:** 4 — High-Accuracy Retrieval  
**Status:** Normative Phase 4 handoff clarification  
**Authority:** `docs/design.md` Section 35

This document corrects the Phase 4 plan's final handoff. It supersedes any statement that Phase 4 is the last design-defined implementation phase.

## Existing Phase 5 is part of the current design

Current `docs/design.md` already defines **Phase 5: Version and product intelligence**. Phase 4 therefore does not terminate the implementation-plan sequence and does not require a new design change before Phase 5 planning begins.

After Phase 4 is reviewed and merged, implementation planning proceeds to the existing Phase 5 scope:

- edition comparison;
- clause mapping across editions;
- structured product parameters;
- comparison of standard requirements and manufacturer specifications.

## Phase 4 handoff contract

Phase 5 inherits the validated outputs and invariants of Phases 0–4, including:

- canonical document, edition, clause, node, chunk, and source identities;
- immutable release and lineage contracts;
- exact/lexical/hybrid/high-accuracy retrieval services;
- deterministic required-context and material-conflict closure;
- cross-encoder reranking and high-accuracy supporting-context behavior;
- source-faithful citations and closed Evidence Package schemas;
- current warning/error/refusal-support evaluation contracts;
- release-gate, reproducibility, security, activation, and rollback baselines.

Phase 5 may build version/product intelligence on those foundations, but it must not weaken source authority, invent mappings or product facts, replace exact edition identity with similarity, or silently change lower-phase retrieval/evidence semantics.

## Planning consequence

The complete current design-defined implementation-plan sequence is Phase 0 through Phase 5. Once Phase 4 is merged, create a separate Phase 5 branch and PR and apply the same phase-scoped review/fix/resolve/re-review/merge workflow.
