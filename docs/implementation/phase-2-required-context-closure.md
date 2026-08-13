# Phase 2 Required-Context Closure Plan

**Project:** ClauseSift  
**Phase:** 2 — Exact Retrieval MVP  
**Status:** Normative current-design plan  
**Primary design authority:** `docs/design.md` Sections 19, 21-23, and 29

## 1. Ownership

Phase 2 owns required Evidence Graph closure for ordinary exact/lexical evidence. It also owns explicit optional context inspection through **Python/MCP `get_context`**.

The boundary is exact:

- ordinary Phase 2 search and exact-clause retrieval run required graph/material-conflict closure and then stop;
- Python/MCP `get_context(required|supporting|diagnostic)` may continue into the explicitly requested supporting/diagnostic traversal after the required fixed point;
- automatic supporting-context expansion of ordinary `high_accuracy` search remains Phase 4;
- there is **no CLI `get-context` command** in Section 23.1.

## 2. Required traversal

Implement the current Section 19 required rules exactly: applicability, dependencies, reverse/forward exceptions, definition scope, table-row table/clause context, and qualifying parent context for notes/footnotes.

Follow only release-validated structural/semantic edges. Unresolved, ambiguous, wrong-edition, or authority-insufficient occurrences are non-navigable and never guessed from labels or similarity.

Seed every canonical member node of every direct source. Use the exact deterministic priority order, complete path-state deduplication, and path-local cycle handling. Target-only visited sets are forbidden because independent reconvergent paths must remain representable.

## 3. Materialization

Source-bearing targets use only canonical source/chunk/node membership and deterministic in-scope source-cover rules.

Empty structural targets remain metadata-only `context_targets`; never fabricate source text, citation, page coordinates, source ID, or source/build lineage.

## 4. Required fixed point

Required completion is:

```text
required graph queue drains
  -> material conflict sides are attached
  -> required context runs for newly attached sides
  -> repeat until neither phase adds anything
```

Only after this fixed point may explicit optional `get_context` traversal begin.

## 5. Bounds

Enforce all current Section 19 bounds, including structural depth 64, required semantic depth 8/seed, supporting depth 1, diagnostic depth 2, 128 expanded objects, 32 paths/object, 1,024 accepted steps, current conflict/position/span/reason limits, and Section 22/MCP byte/frame limits.

Required overflow returns `context_limit_exceeded` with no partial Evidence Package.

Explicit optional Python/MCP `get_context` overflow stops before the first over-limit optional candidate, preserves complete required closure, sets `truncated_optional`, and emits the permitted truncation warning.

## 6. Interfaces

The shared traversal service is used by:

- Python search/clause/context APIs;
- CLI `search` and `get-clause`;
- MCP `search_evidence`, `get_clause`, and `get_context`.

Do not add CLI `get-context`.

## 7. Validation and gates

Independent release validation verifies relationship identity/provenance, materialization, cycle policy, all current bounds, release/cache identity, and the single-clause worst-case closure proof.

Section 29.4 requires zero failures across the complete required-traversal conformance suite and zero accepted edges across the complete prohibited/unresolved/guessed/wrong-edition traversal suite.

Fixtures must include Python/MCP supporting/diagnostic `get_context`, optional truncation after complete required closure, and absence of CLI `get-context`.

## 8. Definition of Done

Phase 2 required context is complete only when ordinary evidence always receives correct required closure; explicit Python/MCP supporting/diagnostic `get_context` works after the required fixed point; CLI remains `search`/`get-clause`; all current bounds and conformance gates pass; and no Phase 3 dense/RRF or Phase 4 automatic high-accuracy supporting-context implementation is introduced here.
