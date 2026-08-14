# Phase 4 Review Clarifications

**Project:** ClauseSift  
**Phase:** 4 — High-Accuracy Retrieval  
**Status:** Normative Phase 4 review clarification  
**Primary design authority:** `docs/design.md`

## 1. Precedence and scope

This document resolves the current Phase 4 review findings without changing Phase ownership. Where an earlier Phase 4 sentence conflicts with a clarification below, this document is authoritative for Phase 4 implementation.

It does not move Phase 2 required-context/material-conflict work or Phase 3 dense/RRF work into Phase 4.

## 2. Phase 2 corrective prerequisite is blocking

Phase 4 depends on the **current-design Phase 2 baseline**, not merely on the originally merged Phase 2 plan.

Before Phase 4 implementation can be declared complete or release-capable, the repository's `master` baseline must contain the Phase 2 corrective plan that brings all of the following into Phase 2 as required by current `docs/design.md`:

- deterministic required Evidence Graph closure;
- deterministic material-conflict fixed-point closure;
- strict ordinary Evidence Package assembly;
- current ordinary Python/CLI/MCP evidence semantics;
- explicit Phase 2 Python/MCP `get_context` supporting/diagnostic traversal after required closure.

Phase 4 must not compensate for a missing lower-phase baseline by reimplementing those services. The Phase 4 release gate must verify that the active lower-phase release/service contract already provides them before high-accuracy reranking or automatic supporting-context expansion is admitted.

The corrective Phase 2 work is reviewed and merged independently; Phase 4 only consumes and regression-tests it.

## 3. No-evidence search is a successful result

A valid search with no adequate evidence is **not a tool/protocol error**.

It is a successful Evidence Package result using the current design's empty-evidence shape and includes the typed `evidence_insufficient` warning.

Therefore any earlier Phase 4 wording such as "success/error state" for a no-evidence search is superseded. The error branch remains reserved for the design-defined failures such as malformed input, explicit unavailable capability, deadline, integrity, or required-context limit failure.

High-accuracy reranking must never manufacture evidence merely to avoid the successful empty-evidence state.

## 4. Expanded-context object bound counts both object forms

The Section 19 limit of **128 expanded context objects per request, excluding direct retrieval seeds**, is one shared bound over:

1. source-backed expanded evidence items; **plus**
2. metadata-only `context_targets`.

It is not 128 evidence items plus an additional 128 metadata targets.

Required and optional traversal share this request-level object budget. A candidate object consumes the budget exactly once under its canonical release-scoped object identity even when several accepted paths reach it.

Required expansion that would exceed the shared bound fails with `context_limit_exceeded` and no partial Evidence Package. Optional supporting/diagnostic expansion stops before the first over-bound optional candidate and uses the design-defined optional truncation semantics.

## 5. Exact optional-truncation value

The serialized `context_completeness` value for optional truncation is exactly:

```json
"truncated_optional"
```

The implementation-plan prose may refer to the concept without quotes, but every schema, fixture, assertion, and serialized example must use the exact string value above.

## 6. Phase 4 automatic supporting expansion boundary

Phase 4 owns **automatic supporting-context expansion for the high-accuracy search path** after reranking and complete Phase 2 required graph/conflict closure.

This must remain distinct from Phase 2's explicit Python/MCP `get_context(context_level="supporting"|"diagnostic")` inspection operation.

Phase 4 automatic expansion:

1. starts only after the lower-phase required graph/conflict fixed point is complete;
2. uses only release-validated supporting relations/rules;
3. cannot repair or hide an `incomplete_required` lower-phase state;
4. cannot erase material conflict sides;
5. is subject to the same shared context-object/path/step/output bounds;
6. may yield `"truncated_optional"` only when required closure remains complete and the optional traversal itself reaches a permitted optional bound.

## 7. Required regression fixtures

Add Phase 4 fixtures proving:

- Phase 4 refuses activation when the current-design Phase 2 corrective baseline is absent;
- the same request succeeds after the validated Phase 2 prerequisite is present;
- a no-match high-accuracy search returns successful empty evidence plus `evidence_insufficient`, never a tool error;
- 127 source-backed expanded objects plus one metadata-only target exactly reaches the shared 128-object limit;
- one additional optional object is rejected/truncated according to optional semantics;
- one additional required object produces `context_limit_exceeded` and no partial success;
- optional-truncation serialization uses exactly `"truncated_optional"`;
- explicit Phase 2 `get_context(supporting|diagnostic)` remains available independently of Phase 4 automatic high-accuracy expansion.

## 8. Acceptance correction

Phase 4 cannot be considered complete unless the Phase 2 corrective prerequisite is present and validated, no-evidence behavior remains successful-with-warning, the 128 expanded-object bound is enforced across both source-backed evidence and metadata-only targets, and every optional truncation uses the exact `"truncated_optional"` contract.
