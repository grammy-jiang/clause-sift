# Phase 2 Required-Context Closure Plan

**Project:** ClauseSift  
**Phase:** 2 — Exact Retrieval MVP  
**Status:** Normative current-design Phase 2 implementation-plan appendix  
**Primary design authority:** `docs/design.md` Sections 7.1, 17, 19, 20, 21, 22, 25-27, and 31  

## 1. Purpose

Current `docs/design.md` assigns deterministic required Evidence Graph context closure to Phase 2. This appendix defines the implementation work needed to bring the Phase 2 plan into conformance with that current boundary.

The implementation must make ordinary exact/lexical evidence safe to interpret without relying on Phase 3 semantic retrieval or Phase 4 high-accuracy supporting context.

Required closure is correctness work, not an optional presentation feature. If a retrieved requirement is incomplete without its governing scope, applicability condition, dependency, definition, exception, table context, or material conflict side, ClauseSift must either return the complete bounded closure or fail visibly. It must never silently return the seed alone.

## 2. Scope

### 2.1 In scope

Phase 2 implements:

- release-validated Evidence Graph structural/semantic relationship consumption;
- the closed v0.1 required-context rule set;
- deterministic required-first traversal;
- path-state rather than target-only traversal deduplication;
- path-local cycle detection;
- source-backed target materialization;
- metadata-only materialization for accepted empty structural targets;
- deterministic source-cover selection for graph targets;
- required-context completeness states and warnings;
- exact current-design traversal bounds;
- fixed-point composition with material-conflict closure;
- deterministic ordering/deduplication of the returned bounded evidence subgraph;
- release-time proofs that exact-clause required closure fits declared bounds;
- runtime fail-closed behavior when required closure cannot fit;
- runtime assembly lineage for accepted paths;
- integration with exact and lexical seed retrieval and the shared Evidence Package service.

### 2.2 Out of scope

This Phase 2 work does not implement:

- dense retrieval;
- embeddings;
- RRF;
- cross-encoder reranking;
- Phase 4 supporting-context expansion for ordinary high-accuracy answers;
- diagnostic context unless explicitly requested by `get_context` and already part of the public Phase 2 context-inspection contract;
- LLM-generated or probabilistic navigable graph edges;
- arbitrary graph queries uploaded by callers;
- inference of missing applicability or relationships from similarity.

## 3. Required-context classes

Implement the exact current-design context classes:

1. `required` — omission may change scope, applicability, normative meaning, a value, or the subject of an exception;
2. `supporting` — useful corroboration/navigation that is not required for ordinary interpretation;
3. `diagnostic` — inspection-only adjacency/version material.

Automatic Phase 2 `search_evidence` and `get_clause` success paths run **required** closure. They do not require Phase 4 supporting expansion.

`get_context` uses the closed context-level enum `required`, `supporting`, `diagnostic`, where each level includes all preceding classes and defaults to the design-defined value. Relation-family include flags on explicit inspection calls may narrow only that explicit inspection request; they never disable automatic required closure for ordinary evidence-returning operations.

## 4. Release-bound context identity

Every release must bind the complete behavior-bearing context contract before activation.

At minimum record and validate:

- `edge_identity_schema_version`;
- `occurrence_identity_schema_version`;
- `context_rule_set_version`;
- canonical context configuration SHA-256;
- exact Evidence Vocabulary version/hash;
- relation-type rank/order identity;
- structural/semantic path-depth limits;
- object/path/step/conflict/position/reason bounds;
- materialization/source-cover algorithm version;
- path-order/tie-break version where separately identified.

Changing any behavior-bearing value invalidates the appropriate context/cache/downstream artifacts and changes build/release identity according to Section 25.

## 5. Navigable relationship prerequisite

Runtime traversal consumes only release-validated graph relationships.

### 5.1 Structural relationships

Use only canonical release-validated structural relationships, including:

- `contains` in parent -> immediate child direction;
- `precedes` in canonical immediate-next direction where diagnostic traversal asks for it.

Structural ownership cycles are release-invalid.

### 5.2 Semantic relationships

Only uniquely resolved, origin-authorized semantic edges are navigable:

- `references`;
- `depends_on`;
- `exception_to`;
- `defines`;
- `supersedes`;
- `amends`;
- `applies_subject_to`.

Every navigable edge uses its canonical direction and stable `edge_id`; every semantic supporting occurrence retains stable `cross_reference_id` and origin-group provenance.

A non-resolved occurrence has no navigable `edge_id` and is never followed by matching document code, edition, clause label, text similarity, or latest-status heuristics.

## 6. Closed required traversal rules

Implement the v0.1 required rules exactly and version them as executable configuration.

### 6.1 Applicability

For `requirement`, `clause`, `subclause`, `paragraph`, `table_row`, or `exception`:

- follow `applies_subject_to` forward as required;
- include every uniquely resolved admitted applicability target;
- recursively execute required rules on the accepted target.

Missing/unresolved required applicability never proves applicability is absent.

### 6.2 Dependencies

For `requirement`, `clause`, `subclause`, `paragraph`, `table_row`, or `exception`:

- follow `depends_on` forward as required;
- accept only uniquely resolved definition/requirement/clause/subclause/table/document endpoints admitted by the design;
- recursively execute required rules.

A definition needed because the source actually uses a governed term must be represented by a compiled dependency; runtime reverse-scanning all definitions in scope is forbidden.

### 6.3 Exceptions

For `requirement`, `clause`, `subclause`, `paragraph`, or `table_row`:

- follow `exception_to` in reverse;
- include every exception that explicitly limits that node;
- then run the exception's own required rules.

For an `exception` node:

- follow `exception_to` forward to the exact affected source-bearing target;
- stop further traversal of that relation after the target;
- still run the exception's applicability/dependency rules.

Sibling position or text similarity never creates an exception relation.

### 6.4 Definition scope

For a `definition` seed/required node:

- follow `defines` forward as required;
- include the exact governing scope;
- stop that relation after the governing scope.

A definition is never presented as globally applicable merely because its text was retrieved.

### 6.5 Table row context

For a `table_row`:

- follow reverse `contains` to the containing table and nearest addressable clause;
- materialize the validated whole-table representation needed to preserve title, headers, units, and the row;
- stop at the nearest addressable clause;
- do not attach unrelated sibling rows merely because they share a table.

A row with missing required structural context remains source-faithful but is `incomplete_required` and emits the typed table-structure diagnostic; headers/units are never inferred.

### 6.6 Note/footnote parent

For `note` or `footnote`:

- follow reverse `contains` to the nearest source-bearing parent it qualifies;
- preserve the note/footnote's own normative status/modality;
- attachment must never promote informative material to normative evidence.

### 6.7 Supporting/diagnostic rules

Implement supporting/diagnostic rule metadata because `get_context` and Phase 4 reuse the same rule engine, but ordinary Phase 2 exact/lexical answers stop after required closure.

The Phase 2 runtime must not silently run supporting/diagnostic traversal as a latency-dependent substitute for Phase 4 behavior.

## 7. Seed construction

For every directly returned source chunk:

1. enumerate every canonical member node through `chunk_nodes` in `member_order`;
2. create one seed record per member node;
3. preserve direct source ID and final candidate rank;
4. label the direct source role as retrieval seed;
5. keep exact document/chunk/node/source identities from the active release.

Seed construction must not collapse several member nodes to one guessed clause or infer a different node from source text.

## 8. Required traversal priority queue

Implement the exact total-order priority key:

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

Required entries are exhausted before supporting or diagnostic entries.

Every queue entry stores:

- originating seed source;
- context class;
- complete ordered edge/node prefix;
- current target document/node;
- semantic-depth state;
- deterministic path identity material.

No unordered set/dictionary iteration may affect dequeue order.

## 9. Path-state deduplication

Deduplicate traversal states only by the complete state:

```text
(seed_source_id,
 context_class,
 ordered edge-ID sequence,
 current target_document_id,
 current target_node_id)
```

Do **not** use a target-only visited set.

Two different accepted paths that reconverge on the same target remain distinct path states and may both continue through later required edges. Materialized evidence/context objects may deduplicate by release-scoped source or node identity, but every accepted independent path must remain available in assembly lineage subject to the path-count bound.

## 10. Cycle handling

Use path-local node/edge tracking.

When a permitted semantic cycle would repeat a path-local node:

- retain the finite accepted prefix;
- do not enqueue the repeated step;
- emit one deterministically keyed `context_cycle_detected` warning;
- continue processing other in-bound paths.

Structural/governing/amendment/supersession cycles are release-invalid and must never reach runtime.

Cycle handling must never depend on recursion depth of Python call stacks; use explicit bounded traversal state.

## 11. Materialization rules

### 11.1 Source-bearing target

Materialize source-backed evidence from canonical `sources`/`chunk_nodes`/node spans only.

Every target rule declares an ordered set of node-qualified intervals:

```text
(node canonical_order,
 node_id,
 node_text_start,
 node_text_end)
```

Do not flatten a multi-node target into one ambiguous byte interval.

### 11.2 Eligible source cover

A catalog source is eligible only when every membership interval contributing to the chunk lies within the declared scope interval for the same node.

Use a deterministic source-cover algorithm that prefers source-faithful scope coverage and does not silently add unrelated text merely because a broader chunk happens to contain the target.

The implementation must guarantee progress and complete declared target coverage or fail closed.

### 11.3 Metadata-only target

When an accepted target is a valid empty structural node with no source-backed materialization:

- return a `context_targets` metadata record rather than fabricated evidence;
- preserve exact document/node identity, heading/structural metadata, edition/status, and accepted traversal paths;
- do not synthesize source text, citation spans, or bounding boxes.

A required empty target that cannot be represented with the exact catalog projection/path means context is not complete.

## 12. Completeness states and warnings

Implement the design's context completeness values and warning propagation.

### 12.1 Complete

`complete` means every required graph/context/conflict obligation has been satisfied within the declared bounds.

### 12.2 Incomplete required

Use `incomplete_required` when source-faithful evidence exists but a required relation/classification/structure cannot be completed safely, including relevant cases such as:

- unresolved required cross-reference;
- unresolved classification needed to decide/execute a required rule;
- required table structure anomaly;
- missing required materialization target.

Emit all design-required typed warnings, including the specific root diagnostic plus `context_incomplete` where required.

### 12.3 Optional truncation

`truncated_optional` is allowed only when required closure is complete and an explicit supporting/diagnostic traversal stops before an optional candidate that would exceed a bound.

Ordinary Phase 2 exact/lexical success cannot use optional truncation to hide required context.

## 13. Exact runtime bounds

Implement and test the current design limits:

| Bound | Required Phase 2 value |
| --- | --- |
| Structural path depth | 64 edges |
| Required semantic path depth | 8 edges per seed |
| Supporting semantic path depth | 1 |
| Diagnostic semantic path depth | 2 |
| Expanded context objects | 128 unique objects per request, excluding direct seeds |
| Paths per returned context object | 32 |
| Total accepted path steps | 1,024 |
| Material conflict records | 64 per request |
| Positions per conflict | 16 |
| Total conflict positions | 256 |
| Conflict position spans | 1,024 per request |
| Conflict inclusion reasons | 1,024 per request |

The complete serialized output must also satisfy the existing MCP/output frame budgets.

## 14. Bound enforcement semantics

### 14.1 Required closure

Evaluate bounds while candidates/path states are enqueued/materialized.

If a required graph/conflict closure would exceed any depth/object/path/step/conflict/position/reason/byte bound:

- return `context_limit_exceeded`;
- emit no partial Evidence Package success;
- release all request-local resources;
- retain the active release unchanged.

Required evidence is never silently truncated.

### 14.2 Optional context

For an explicit supporting/diagnostic request only:

- process optional candidates in deterministic priority order;
- stop immediately before the first candidate that would exceed a bound;
- retain the complete required closure;
- set `context_completeness: truncated_optional`;
- emit `context_truncated` with only the safe configured/observed counts allowed by the design.

## 15. Required closure and material-conflict fixed point

Required closure is not complete after the required graph queue drains once.

The Phase 2 runtime must compose graph traversal and material-conflict closure to a least fixed point:

1. process required graph path states until the required queue is empty;
2. identify every material conflict intersecting selected source memberships;
3. add missing compiled conflict-position cover sources as required `conflict_context`;
4. enqueue required graph context for each newly added source;
5. repeat graph and conflict phases until neither adds a source/record;
6. only then consider optional supporting/diagnostic traversal.

Conflict records themselves are not graph edges and do not consume semantic graph depth, but conflict-added sources/paths/reasons/bytes count against the explicit bounds.

The separate Phase 2 material-conflict appendix defines conflict build/runtime details.

## 16. Release-time validation

Release validation independently proves the context runtime can safely serve the release.

At minimum:

- validate every structural/semantic edge endpoint and direction;
- validate all stable edge/occurrence identities and origin groups;
- validate the closed context rule configuration against supported schema versions;
- recompute required source covers for all rule-materializable targets used by release tests;
- reject release-invalid cycles;
- validate classification/type eligibility for rule endpoints;
- prove the largest single required graph+conflict closure addressable by `get_clause` fits every configured depth/object/path/step/conflict/position/reason/byte bound;
- verify context-related artifact/cache hashes in the release manifest;
- run deterministic context fixtures before activation.

A release that cannot prove the single-clause required-closure bound is not activatable.

## 17. Ordering and deduplication of final evidence subgraph

After fixed-point closure:

- deduplicate source-backed evidence by exact release-scoped `source_id`;
- deduplicate metadata-only targets by exact `(document_id, node_id)` identity;
- preserve every accepted independent traversal path up to the per-object path bound;
- preserve direct seed rank/role independently from context role;
- never deduplicate by text similarity, clause number, document code, or normalized wording;
- preserve actual document edition/status/jurisdiction/type on every attached item.

Cross-document context never substitutes an active/newer edition for the exact stored edge target.

## 18. Runtime assembly lineage

For every source-backed or metadata-only returned object, retain the exact request-scoped assembly reasons required by the Evidence Package schema:

- selection role (`retrieval_seed`, `expanded_context`, or `conflict_context` as applicable);
- originating seed source IDs;
- complete accepted context paths;
- each path step's stable `edge_id`, canonical endpoints, relation type, and validated `origin_groups`/occurrence IDs;
- any conflict inclusion reason where applicable;
- context completeness state and typed warnings.

This request-specific lineage never mutates immutable release `lineage.json`.

## 19. Shared service integration

Required closure must be one shared service layer used by:

- Python API;
- CLI evidence commands;
- MCP `search_evidence`;
- MCP `get_clause`;
- MCP `get_context` where enabled families require required closure;
- clause/source resource projections that the design exposes as context-complete evidence surfaces.

Adapters must not reimplement traversal or silently omit context to fit a presentation format.

## 20. Test matrix

### 20.1 Rule tests

Test every v0.1 required rule in both positive and negative directions:

- applicability forward;
- dependency forward;
- reverse exception;
- exception forward target;
- definition -> scope;
- table-row -> whole table + nearest clause;
- note/footnote -> nearest source-bearing parent.

### 20.2 Resolution tests

Test:

- resolved exact same-document target;
- resolved cross-document target;
- wrong-edition same clause label not followed;
- unresolved document/clause/node;
- ambiguous edition/node;
- authority-insufficient occurrence;
- release-tier critical vs standard behavior.

### 20.3 Path tests

Test:

- reconvergent independent paths retained;
- path-state dedup prevents duplicate identical state;
- target-only visited-set regression fixture;
- allowed semantic cycle warning/stop;
- forbidden structural/governing cycle release failure;
- deterministic queue order under shuffled DB insertion/order.

### 20.4 Materialization tests

Test:

- exact atomic node source;
- complete clause/subtree source cover;
- whole-table source projection;
- empty governing scope metadata target;
- no eligible source -> incomplete/failure behavior;
- no broad unrelated chunk chosen when a scope-contained source exists.

### 20.5 Bound tests

For every numeric bound test exact maximum and first over-limit value.

Required over-limit cases return one `context_limit_exceeded` tool error and no partial success.

Optional over-limit cases retain required closure and return deterministic optional truncation only where optional traversal was explicitly requested.

### 20.6 Integration fixtures

Include at minimum:

- requirement + applicability;
- requirement + exception + exception condition;
- definition + governing scope;
- table row + headers/units + clause;
- dependency chain to depth boundary;
- cross-document dependency with exact edition;
- unresolved required reference;
- unclassified node needed by required rule;
- material conflict side that introduces another required context path;
- several retrieval seeds whose combined closure exceeds a bound.

## 21. Acceptance criteria

Phase 2 required-context closure is complete only when:

1. every ordinary exact/lexical evidence seed runs the versioned required rule set;
2. only release-validated structural/resolved semantic edges are navigable;
3. traversal uses the exact deterministic priority key;
4. traversal deduplicates complete path state, not target alone;
5. cycle handling is deterministic and bounded;
6. source-backed targets are materialized only from canonical in-scope source cover;
7. valid empty structural targets use metadata-only `context_targets`, never fabricated text;
8. all exact numeric bounds are enforced with the required-vs-optional semantics above;
9. required graph/context plus material conflicts reach a fixed point before success;
10. a required over-limit condition returns `context_limit_exceeded` with no partial Evidence Package;
11. unresolved required information is visible through completeness/warnings rather than guessed;
12. exact document/edition/status identity is preserved for every attached object;
13. request-scoped assembly lineage retains every accepted path/reason within bounds;
14. release validation independently proves the single-clause required-closure bound;
15. Python/CLI/MCP call the same traversal/evidence service;
16. the regression corpus demonstrates that required scope/applicability/definitions/dependencies/exceptions/table context are never lost from applicable ordinary evidence results.
