# Phase 2 Final Review Clarifications

**Phase:** 2 — Exact Retrieval MVP  
**Status:** Normative Phase 2 clarification  
**Authority:** `docs/design.md` Sections 19, 22, 23, and 29

Where an earlier Phase 2 plan conflicts with this file, this file is authoritative for these contracts.

## Complete Python surface

The Phase 2 Python client exposes all six Section 22.1 methods:

1. `search_evidence`;
2. `get_clause`;
3. `get_context`;
4. `get_document_metadata`;
5. `list_documents`;
6. `get_page_reference`.

Equivalent Python/MCP operations preserve the same normalized fields, ordering, error codes, pagination boundaries, cursor binding, and safe serialization. The CLI remains narrower and does not gain a `get-context` command.

## Exact `get_context` flags

Python and MCP use:

```python
get_context(
    source_id: str,
    context_level: str = "supporting",
    include_parent: bool = True,
    include_applicability: bool = True,
    include_dependencies: bool = True,
    include_definitions: bool = True,
    include_exceptions: bool = True,
    include_notes: bool = True,
    include_tables: bool = True,
    include_references: bool = True,
    include_versions: bool = False,
    include_adjacent: bool = False,
)
```

The closed `context` object always contains all ten arrays: `parents`, `applicability`, `dependencies`, `definitions`, `exceptions`, `notes`, `tables`, `references`, `versions`, and `adjacent`.

A false flag performs no traversal for that family and requires its array to be empty. A true flag may also produce an empty array when no relation exists. Disabled families do not create incomplete-context state. `versions` and `adjacent` stay opt-in even at diagnostic level.

Expansion begins from every node in the selected source chunk's persisted `chunk_nodes.member_order`.

## Phase 2 optional-context precision gate

Because Phase 2 advertises explicit `get_context(context_level="supporting"|"diagnostic")`, Section 29.4 optional-context precision is a Phase 2 blocking gate for those profiles:

- one-sided 95% Wilson lower confidence bound >=95%;
- at least 60 applicable independently labelled cases;
- larger stratified samples when a context rule, relation family, node family, level, language, or hard negative is underrepresented;
- expansion factor reported by mode and node/relation family;
- numerator, denominator, point estimate, lower bound, target, split/corpus/reviewer identity, and frozen candidate identity retained.

This does not pull Phase 4 automatic high-accuracy supporting expansion into Phase 2.

## Held-out/candidate identity

The Phase 2 held-out retry policy also governs optional-context precision. Candidate identity binds all behavior-bearing optional traversal inputs, including context rules/configuration, relation/edge identity, the ten flag defaults/mapping, context-level semantics, depth/object/path/step/output bounds, queue/dedup/cycle/materialization behavior, catalog/context artifacts, and serializer projection.

After decisive labels/results are observed, a behavior-bearing changed candidate cannot obtain fresh authorization from that split. Identical-candidate replay is reproduction-only; later changed candidates require fresh preregistered independent evidence under the existing finite-campaign policy.

## Required tests

Test all six Python methods; Python/MCP parity; exact flag defaults; each family independently disabled with an empty corresponding array; opt-in versions/adjacent behavior; true-with-no-match empty arrays; enabled unresolved-required behavior; and optional-context Wilson boundary/sample/leakage/retry/candidate-identity cases.

Phase 2 is not complete unless all three contracts above pass.