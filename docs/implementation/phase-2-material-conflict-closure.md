# Phase 2 Material-Conflict Closure Implementation Plan

**Project:** ClauseSift  
**Phase:** 2 — Exact Retrieval MVP  
**Status:** Normative current-design implementation plan  
**Primary design authority:** `docs/design.md` Sections 19, 20.3, 21, and 29

## 1. Scope

Phase 2 owns build-time material-conflict records and runtime all-side preservation. Ranking must never hide an admitted material disagreement.

This plan does not add Phase 3 dense/RRF retrieval or Phase 4 automatic `high_accuracy` reranking/supporting-context expansion.

## 2. Build-time conflict contract

Use the current closed lifecycle `potential`, `confirmed`, `explained`, and `unresolved` exactly as defined by Section 20.3.

- `potential` is build-diagnostic only and never appears in an admitted runtime release.
- `confirmed` and admissible `unresolved` records remain visible when material.
- `explained` remains audit/comparison/diagnostic metadata.
- unresolved records touching a critical-tier document block release.

Conflict/position identities, comparison projections, required-context projections, decision artifacts, dimensions, ordering, and precedence follow Section 20.3 exactly. A model score, rank, recency, authority name, or stricter-looking wording cannot create final conflict state or precedence.

## 3. Canonical position source cover

For every admitted position, compile the deterministic query-independent source cover over the exact node-qualified spans.

At each first uncovered coordinate:

1. select sources covering the coordinate in the same document/node;
2. prefer scope-contained sources whenever one exists;
3. otherwise permit the design-defined broader-source fallback;
4. apply the exact deterministic ordering;
5. require progress until every position byte is covered.

Persist `conflict_position_sources` and independently recompute it during release validation. Failure to advance or completely cover a position blocks release.

## 4. Runtime discovery

After each required graph pass, discover every admitted material `confirmed`/`unresolved` conflict whose position span intersects a selected source membership.

Use exact catalog span/membership intersection only. Direct metadata filters constrain direct seeds, not required conflict/context attachments.

For each material record, attach every position's canonical cover source in stable order and preserve its real document, edition, status, and source identity.

## 5. Required graph/conflict fixed point

The required fixed point is:

```text
required graph queue drains
  -> material conflicts are inspected in stable order
  -> missing position-cover sources enter required graph queue
  -> required context runs for newly attached sources
  -> repeat until neither graph nor conflict phase adds anything
```

Conflict records are not graph edges. Deduplicate objects only by exact release-scoped identity while retaining every required role/path/reason allowed by the closed schema.

## 6. Phase 2 optional-context handoff

After the required fixed point is complete:

- ordinary exact/lexical search and exact-clause retrieval stop at required context;
- **Phase 2 Python/MCP `get_context(context_level="supporting"|"diagnostic")` may continue into the explicitly requested optional traversal defined by Section 19.1**;
- optional traversal may be truncated only after complete required closure, using the current `truncated_optional`/warning rules;
- automatic supporting-context expansion for ordinary `high_accuracy` search remains Phase 4 scope.

Therefore optional traversal is **not** globally deferred to Phase 4.

## 7. Interface ownership

The shared service is used by:

- Python search, exact-clause retrieval, and `get_context`;
- CLI `search` and `get-clause`;
- MCP `search_evidence`, `get_clause`, and `get_context`.

There is **no CLI `get-context` command** in the current Section 23.1 design.

## 8. Bounds and failure semantics

Enforce all current Section 19 graph/conflict/object/path/step/span/reason/byte bounds.

Required overflow returns `context_limit_exceeded` with no partial Evidence Package.

For explicit Python/MCP optional `get_context`, optional overflow stops before the first over-limit optional candidate, preserves complete required closure, sets `truncated_optional`, and emits the permitted truncation warning.

Release validation proves the largest required closure addressable by `get_clause` fits every declared bound.

## 9. Evidence projection

Conflict-added evidence carries the current `conflict_context` role/reason. Every evidence-bearing success includes the required `conflicts` array using the exact Section 21 closed schema.

Confirmed/unresolved warning behavior and encoded precedence follow the current design. Detector-generated prose never becomes source authority.

## 10. Quality gates

Use Section 29.4 exactly:

- conflict-candidate recall: one-sided 95% Wilson LB >=95%, with the current minimum sample rule;
- applicable confirmed/unresolved precision families: Wilson LB >=98%;
- applicable explained-difference precision families: Wilson LB >=98%;
- conflict position/source/lineage completeness, all-side runtime preservation, ordering, and trusted-precedence serialization: **zero failures across the complete deterministic conflict conformance suite**;
- conflict negative suite: **zero prohibited occurrences**.

Do not replace these with an invented held-out 100% all-side metric.

## 11. Required tests

Cover at minimum:

- confirmed, explained, and unresolved examples;
- critical-vs-standard unresolved behavior;
- n-ary conflicts and multi-source position covers;
- graph -> conflict -> graph fixed point;
- direct filters not erasing required sides;
- required overflow with no partial package;
- Python/MCP `get_context` supporting/diagnostic traversal after the fixed point;
- optional truncation after complete required closure;
- absence of a CLI `get-context` command;
- false precedence and other Section 29.4 negative cases.

## 12. Definition of Done

Phase 2 material-conflict closure is complete only when conflict identities/decisions/covers validate independently; every material side and its required context is preserved; the required fixed point is deterministic; required overflow never returns partial success; explicit Python/MCP supporting/diagnostic `get_context` works after the required fixed point; CLI scope remains `search`/`get-clause`; current conflict serialization/warnings/precedence and Section 29.4 gates pass; and no Phase 3 dense/RRF or Phase 4 automatic high-accuracy supporting-context implementation is introduced here.
