# Phase 2 Required-Context Closure Plan

**Project:** ClauseSift  
**Phase:** 2 — Exact Retrieval MVP  
**Status:** Normative current-design Phase 2 implementation-plan appendix  
**Primary design authority:** `docs/design.md` Sections 7.1, 17, 19-22, 25-27, 29, and 31

## 1. Purpose

Phase 2 owns deterministic **required** Evidence Graph closure for every ordinary exact/lexical evidence result. A seed is not a safe final result when its meaning depends on governing scope, applicability, definitions, dependencies, exceptions, required table context, or a material conflict side.

Phase 2 must either return the complete bounded required closure or fail visibly. It must not silently return the seed alone.

This plan does not add Phase 3 semantic retrieval or Phase 4 high-accuracy supporting-context expansion.

## 2. Context classes and Phase 2 boundary

Use the current closed classes:

1. `required` — omission can change scope, applicability, normative meaning, a value, or an exception's subject;
2. `supporting` — useful corroboration/navigation but not required for ordinary interpretation;
3. `diagnostic` — inspection-only adjacency/version material.

Ordinary Phase 2 `search_evidence` and `get_clause` run required closure only.

`get_context` may explicitly request `required`, `supporting`, or `diagnostic`, where each level includes preceding levels under the current design. That inspection capability does not make Phase 4 supporting-context expansion part of ordinary Phase 2 search.

## 3. Release-bound context identity

Every active release binds every behavior-bearing context input, including:

- edge identity schema;
- occurrence identity schema;
- context rule-set version/configuration hash;
- Evidence Vocabulary version/hash;
- relation-type rank/order;
- structural/semantic depth bounds;
- object/path/step/conflict/position/reason bounds;
- target materialization/source-cover algorithm version;
- ordering/tie-break behavior where separately versioned.

A behavior change invalidates the appropriate context/cache/downstream release identity according to Section 25.

## 4. Navigable relationship prerequisite

Runtime traverses only release-validated relationships.

### Structural

- `contains`: immediate parent -> immediate child;
- `precedes`: canonical immediate-next relation where diagnostic traversal requests it.

Structural hierarchy cycles are release-invalid.

### Semantic

The closed initial vocabulary is:

- `references`;
- `depends_on`;
- `exception_to`;
- `defines`;
- `supersedes`;
- `amends`;
- `applies_subject_to`.

A semantic occurrence is navigable only after unique resolution and required origin-authority checks. Every navigable edge has a stable canonical-direction `edge_id`; supporting occurrences retain stable `cross_reference_id` and origin-group provenance.

An unresolved/ambiguous/authority-insufficient occurrence has no navigable edge and is never followed by text similarity, clause-label guessing, document-code heuristics, or latest-edition substitution.

## 5. Closed required rules

### 5.1 Applicability

For requirement/clause/subclause/paragraph/table-row/exception nodes, follow `applies_subject_to` forward as required. Include every uniquely resolved admitted target and recursively run its required rules.

### 5.2 Dependencies

For requirement/clause/subclause/paragraph/table-row/exception nodes, follow `depends_on` forward to the current design's admitted dependency endpoint types and recursively run required rules.

A definition required by actual term use must be compiled as the appropriate dependency; runtime does not reverse-scan all scoped definitions.

### 5.3 Exceptions

For requirement/clause/subclause/paragraph/table-row nodes, follow `exception_to` in reverse to every explicit limiting exception, then run the exception's required rules.

For an exception, follow `exception_to` forward to the exact affected source-bearing target and stop that relation after the target while still running the exception's applicability/dependency rules.

Sibling position or semantic similarity cannot create an exception.

### 5.4 Definition scope

For a definition, follow `defines` forward to the exact governing scope and stop that relation there. A definition is never treated as globally applicable solely because it was retrieved.

### 5.5 Table row

For a table row, reverse `contains` reaches the containing table and nearest addressable clause. Materialization preserves validated table title, headers, units, and the row; unrelated sibling rows are not attached merely by proximity.

If required table structure cannot be supplied safely, retain source-faithful evidence, mark `incomplete_required`, and emit the current table-structure diagnostic. Never invent headers/units.

### 5.6 Note/footnote parent

A note/footnote follows reverse `contains` to the nearest source-bearing parent it qualifies. Its own normative status/modality is preserved; attachment never promotes informative material.

## 6. Seed construction

For every direct source chunk:

1. enumerate canonical member nodes in `chunk_nodes.member_order`;
2. create one seed state per member node;
3. preserve final direct candidate rank and source ID;
4. keep exact document/chunk/node/source identity;
5. label the direct source `retrieval_seed` in assembly lineage.

Do not collapse several member nodes into a guessed clause or infer a different node from text.

## 7. Required priority queue

Use the exact total order:

```text
(context-class rank,
 seed final rank,
 seed source_id,
 path length,
 ordered relation-type ranks,
 target document_id,
 target node canonical_order,
 ordered edge IDs)
```

Every queue entry retains origin seed, context class, full ordered edge/node prefix, current target, semantic depth, and deterministic path identity material.

No hash-map/SQLite physical order may affect dequeue behavior.

## 8. Path-state deduplication

Deduplicate only the full traversal state:

```text
(seed_source_id,
 context_class,
 ordered edge-ID sequence,
 current target_document_id,
 current target_node_id)
```

Do not use a target-only visited set.

Independent paths that reconverge on one target remain distinct states and can both continue. Materialized objects may deduplicate by exact release-scoped source/node identity while retaining all accepted in-bound paths up to the declared path bound.

## 9. Cycle handling

Use path-local node/edge tracking.

For an allowed semantic `references`/`depends_on` cycle, retain the finite accepted prefix, do not enqueue the repeated step, and emit one deterministically keyed `context_cycle_detected` warning.

Structural/governing/amendment/supersession cycles are release-invalid and must not reach runtime.

Traversal uses explicit bounded state rather than Python recursion depth as a safety mechanism.

## 10. Target materialization

### 10.1 Source-bearing target

Materialize only from canonical source/chunk/node membership. Each rule declares ordered node-qualified source intervals rather than one ambiguous flat range.

A selected source's contributed memberships must be in the declared target scope for their nodes. Use deterministic source-cover selection and require progress/complete declared coverage.

Do not choose a broader unrelated chunk when a scope-contained source can cover the target.

### 10.2 Empty structural target

A valid empty structural target is a metadata-only `context_targets` record with exact document/node/edition/status/heading/classification projections and accepted paths.

Never fabricate `original_text`, citation, page span, bounding box, source ID, or source/build lineage for an empty node.

## 11. Completeness and warnings

`complete` means all required graph/conflict obligations are satisfied within bounds.

`incomplete_required` is used only under current design conditions where source-faithful evidence can be returned while required resolution/classification/structure remains incomplete, with the required typed warnings.

`truncated_optional` is only for explicit supporting/diagnostic traversal after complete required closure; it never hides a required obligation.

## 12. Exact runtime bounds

Implement the current values:

| Bound | Value |
| --- | --- |
| Structural path depth | 64 |
| Required semantic path depth | 8 per seed |
| Supporting semantic path depth | 1 |
| Diagnostic semantic path depth | 2 |
| Expanded context objects | 128 unique objects/request, excluding direct seeds |
| Paths per returned context object | 32 |
| Total accepted path steps | 1,024 |
| Material conflict records | 64/request |
| Positions per conflict | 16 |
| Total conflict positions | 256 |
| Conflict position spans | 1,024/request |
| Conflict inclusion reasons | 1,024/request |

The complete output must also satisfy Section 22/MCP byte/frame budgets.

## 13. Bound semantics

A required graph/conflict candidate that would exceed a required depth/object/path/step/conflict/position/reason/byte bound causes `context_limit_exceeded` and **no partial Evidence Package success**.

For an explicit optional traversal, stop before the first optional over-bound candidate in deterministic order, retain complete required closure, set `truncated_optional`, and emit the permitted `context_truncated` details.

## 14. Graph/conflict least fixed point

Required closure is not complete after one graph pass.

1. drain the required graph queue;
2. discover every material conflict intersecting selected source memberships;
3. add every missing compiled conflict-position cover source as required `conflict_context`;
4. enqueue required graph context for those new sources;
5. repeat until neither graph nor conflict phase adds anything;
6. only then consider requested optional context.

Conflict records are not graph edges and do not consume semantic graph depth, but conflict-added objects/paths/reasons/bytes count against their explicit bounds.

## 15. Release validation

Independent release validation must:

- validate all structural/semantic endpoints/directions;
- recompute edge/occurrence identity and provenance groups;
- validate the closed context rule/configuration and endpoint classifications;
- recompute target source covers used by conformance fixtures;
- reject release-invalid cycles;
- verify context artifact/cache/release identities;
- prove the largest single required graph+conflict closure addressable by `get_clause` fits every depth/object/path/step/conflict/position/reason/byte bound;
- run the complete deterministic traversal conformance and negative suites before activation.

## 16. Final subgraph ordering and lineage

After fixed-point closure:

- deduplicate source evidence only by exact release-scoped `source_id`;
- deduplicate metadata-only targets by exact `(document_id,node_id)`;
- preserve every accepted independent path within bounds;
- preserve actual edition/status/jurisdiction/type;
- never deduplicate by text similarity or clause label.

Request assembly lineage records exact selection roles, origin seed IDs, accepted context paths/steps/origin groups/rule IDs, completeness, warnings, and conflict reasons through the Section 21 closed schema. It never mutates `lineage.json`.

## 17. Shared service integration

Required closure is one service used by Python, CLI, `search_evidence`, `get_clause`, and `get_context` where the requested families require it.

The clause resource uses the exact Section 22 context-complete clause-resource contract. The raw source resource remains a separate Section 22.3 contract returning only source `original_text`; it does **not** run or wrap required closure.

Adapters cannot reimplement traversal or omit required context for presentation convenience.

## 18. Evaluation and conformance

Phase 2 follows Section 29.4 exactly:

- required context, lineage paths, source status, and deterministic ordering: **zero failures across the complete versioned traversal conformance suite**;
- prohibited, unresolved, guessed, or wrong-edition traversal: **zero accepted edges across the complete versioned negative suite**.

These are deterministic complete-suite count gates, not invented probabilistic held-out 100% gates.

Fixtures cover every required rule, exact/ambiguous/unresolved resolution, reconvergent paths, cycles, target materialization, exact max/one-over bounds, graph-conflict fixed point, and multi-seed overflow.

## 19. Acceptance criteria

Phase 2 required-context closure is complete only when:

1. every ordinary exact/lexical evidence seed runs the current versioned required rule set;
2. only release-validated navigable edges are followed;
3. exact queue ordering/path-state dedup/cycle rules are deterministic;
4. source-backed targets use canonical in-scope source cover;
5. empty targets remain metadata-only;
6. all current numeric bounds and required-vs-optional semantics are enforced;
7. graph/conflict closure reaches the least fixed point;
8. required overflow returns no partial Evidence Package;
9. unresolved required facts are visible, never guessed;
10. document/edition/status identity is preserved;
11. assembly lineage retains exact accepted paths/reasons;
12. release validation proves the single-clause closure bound;
13. Python/CLI/MCP evidence tools share one traversal service;
14. the complete deterministic traversal and negative conformance suites have zero failures/zero prohibited accepted edges;
15. no Phase 3 dense/RRF or Phase 4 ordinary supporting-context implementation is pulled into this Phase 2 plan.
