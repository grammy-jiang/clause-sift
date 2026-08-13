# Phase 2 Evidence Service and Public Surface Implementation Plan

**Project:** ClauseSift  
**Phase:** 2 — Exact Retrieval MVP  
**Status:** Normative current-design corrective implementation plan  
**Primary design authority:** `docs/design.md` Sections 7.2, 17, 19-22, 26-27, 29, 31, and 35  
**Companions:** `phase-2-required-context-closure.md`, `phase-2-material-conflict-closure.md`

## 1. Purpose

Current `docs/design.md` requires Phase 2 to provide the ordinary context-complete exact/lexical evidence path and the basic Python, CLI, and MCP retrieval interfaces that expose it.

The already merged Phase 2 plan predates that boundary and intentionally withheld final evidence tools until a later phase. This corrective plan closes that gap.

Phase 2 now owns:

- ordinary exact/lexical seed retrieval;
- required Evidence Graph closure;
- material-conflict fixed-point closure;
- strict Evidence Package assembly;
- the shared Python evidence service;
- ordinary CLI retrieval;
- the basic MCP tools/resources whose success contracts are defined by the design.

Phase 2 still does not own Phase 3 dense/RRF retrieval or Phase 4 cross-encoder reranking/supporting-context enhancements.

## 2. One service, several adapters

Implement exactly one domain service for evidence-bearing operations.

Conceptually:

```text
Python API / CLI / MCP
        |
        v
request validation and mode resolution
        |
        v
shared evidence service
        |
        +--> exact lookup / lexical retrieval
        +--> required context closure
        +--> material-conflict closure
        +--> strict Evidence Package serializer
        |
        v
immutable active release
```

CLI and MCP adapters are projections of the same service. They must not duplicate SQL, traversal, warning, conflict, pagination, or serialization logic.

## 3. Phase 2 retrieval modes

Phase 2 implements the ordinary capabilities available before semantic retrieval:

- explicit `exact` mode;
- `auto` resolving to the best Phase 2-capable exact/lexical path;
- no successful explicit `hybrid` or Phase 4-enhanced `high_accuracy` unless the installed runtime and active release actually contain those later capabilities.

An explicit unavailable mode returns `feature_unavailable` rather than silently degrading.

When `auto` cannot use a later optional capability because it is absent, behavior follows the design's capability/warning contract and still uses the same Phase 2 evidence service.

Required context/conflict correctness never depends on mode speed.

## 4. Request-validation boundary

Validate all request fields before retrieval work.

Preserve the design's exact public bounds, including:

- query: trimmed `minLength: 1`, `maxLength: 4096`, encoded value at most 16,384 UTF-8 bytes;
- opaque IDs: `minLength: 1`, `maxLength: 128`, pattern `^[a-z0-9][a-z0-9._:-]{0,127}$`;
- exact lookup/filter strings: 1-128 Unicode scalars plus closed-enum validation where applicable;
- filter arrays: at most 64 unique values each;
- `search_evidence`: at most 256 values across all filter arrays;
- result limit: 1-100;
- cursor: at most 4096 characters plus authenticated release-bound syntax;
- page number: positive 32-bit range and within manifested page count.

The same bound is checked before and after the field's specified normalization. Over-limit input cannot become valid merely because trimming or normalization shortens it.

Reject invalid requests before loading models, touching expensive retrieval services, or allocating page working sets.

## 5. Shared direct seed selection

Phase 2 retains direct primitives internally, but they are now components of the final ordinary evidence path rather than public substitutes for it.

### 5.1 Exact clause seeds

`get_clause`:

1. validates exact `document_id` and `clause_number`;
2. resolves the canonical clause node with no fuzzy or edition substitution;
3. selects exactly the complete Section 14.1 exact-lookup chunk/source set;
4. marks those sources `retrieval_seed`;
5. runs required graph/conflict closure from every direct source.

### 5.2 Search seeds

`search_evidence` Phase 2 seed selection combines the exact/identifier and lexical behavior available in the resolved mode.

Metadata filters use exact normalized catalog values. Values are ORed within a filter list and filter categories are ANDed. Default status behavior follows the design; explicit null status removes the active-only default.

Filters constrain direct seeds only. Required context and material conflict attachments retain their actual source metadata even when they fall outside the direct-seed filter.

### 5.3 No-match semantics

No direct match is a successful `complete` response with empty `evidence`, `context_targets`, and `conflicts`, not a transport/domain error.

## 6. Required graph/conflict closure handoff

Every evidence-bearing Phase 2 request passes direct seeds through the shared fixed point specified by the two companion corrective plans.

The service returns success only after:

- complete required graph closure;
- complete material-conflict closure;
- graph/conflict fixed point;
- deterministic object/path/reason ordering;
- bound checks;
- strict serialization validation.

If complete required closure does not fit a declared bound, return `context_limit_exceeded` and no partial Evidence Package.

Phase 2 does not run Phase 4 supporting context on ordinary exact/lexical requests.

## 7. Evidence Package root contract

Every evidence-bearing success uses the current closed root shape.

`search_evidence` returns:

```text
query
retrieval_mode
release
context_completeness
evidence[]
context_targets[]
conflicts[]
warnings[]
```

`get_clause` returns the same evidence-bearing structure except for fields the design omits from that tool's root contract.

`get_context` returns its design-defined root fields and required relation-family arrays.

Unknown root properties fail strict serialization rather than being emitted opportunistically.

## 8. Source-backed evidence item

Every `evidence[]` item is source-faithful and uses only the Section 21 closed schema.

The implementation must populate and independently verify the design-owned projections, including:

- exact `source_id` and `document_id`;
- document code and edition;
- document type/normative status/lifecycle status;
- clause and heading path;
- canonical node classifications;
- constant untrusted-source content-trust marker;
- exact original source text;
- page start/end and available boxes;
- deterministic citation;
- complete source/build/assembly lineage;
- typed per-item warnings.

The central serializer recomputes catalog-bound projections and fails closed on disagreement.

Generated summaries never replace `original_text`.

## 9. Evidence Lineage

Use the current three-dimension lineage model without creating parallel provenance.

### 9.1 Source provenance

Bind the approved manifest/source identity and exact contributed canonical-node/page spans.

### 9.2 Build provenance

Bind:

- build/release artifact hashes;
- evidence vocabulary;
- exact classification records/provenance;
- canonical node/chunk identities;
- transformation artifact identities;
- graph/context/conflict rule-set identities;
- diagnostic state.

Immutable `lineage.json` remains query-independent.

### 9.3 Assembly provenance

Runtime adds request-scoped selection reasons using only the existing closed fields:

- `selection_roles`;
- `seed_source_ids`;
- `context_completeness`;
- retrieval records for direct seeds;
- fusion/rerank only when that stage actually exists in the resolved later mode;
- `context_paths`;
- `conflict_reasons`.

Phase 2 lexical/exact execution never fabricates dense/fusion/rerank records.

## 10. Context targets

A required traversal may reach an accepted empty structural node with no source text.

Such a target appears in `context_targets`, not as fabricated evidence.

Each strict record contains only the design's safe catalog/manifest projection and one or more accepted context paths. It has no `original_text`, source locator, citation, page coordinate, source lineage, or generated prose.

The serializer validates that every target is reachable through the retained path and that every required accepted empty target is present.

## 11. Conflict projection

The root `conflicts` array is required on evidence-bearing success and follows `phase-2-material-conflict-closure.md`.

Every material admitted record is complete and stable-ordered. The serializer rejects:

- missing material conflicts;
- extra non-material records in an ordinary request;
- missing positions;
- one-sided source sets;
- mismatched position spans;
- invalid precedence projections;
- generated conflict prose presented as source fact.

## 12. Context completeness

Use exactly the design's closed states:

- `complete`;
- `incomplete_required` where the design allows a source-faithful incomplete result for unresolved/uncertain required facts;
- `truncated_optional` only where an optional Phase 4/diagnostic traversal was requested and was deterministically truncated.

A hard required bound overflow is not `incomplete_required`; it is the `context_limit_exceeded` tool error with no partial success.

The result-level value is the deterministic worst state across the returned evidence subgraph according to the design ordering.

## 13. Typed warnings

Warnings are data, not log-only diagnostics.

Phase 2 must implement every warning needed by its ordinary exact/lexical/context/conflict behavior, including as applicable:

- source coordinate incompleteness;
- parser/OCR uncertainty propagated by source/build lineage;
- unresolved classification;
- required context incomplete;
- unresolved cross-reference;
- table structure anomaly;
- context status boundary;
- context cycle detected;
- material `evidence_conflict`;
- `conflict_unresolved`;
- applicability/evidence insufficiency required by the current design.

Warnings use only the closed code/phase/severity/message/source/details schema and safe detail keys. Adapters may not invent prose warnings with different semantics.

## 14. `search_evidence`

Implement the Section 22 semantic contract directly.

### Selection

- bounded query;
- exact metadata filters;
- resolved Phase 2 mode;
- exact/lexical direct seeds;
- required graph-and-conflict closure for every seed.

### Success

Return a strict root containing the ordered direct, expanded-context, and conflict-context evidence items; empty-node context targets; material conflicts; and typed warnings.

### Domain errors

At minimum route exactly:

- malformed/over-limit input -> `identifier_invalid`;
- explicit unavailable mode -> `feature_unavailable`;
- required closure overflow -> `context_limit_exceeded`;
- release integrity failure -> `release_integrity_failed`.

No match remains a complete empty success.

## 15. `get_clause`

Implement exact document/clause semantics with no fuzzy clause lookup or edition substitution.

Every source in the exact-lookup set is a direct seed. Run required graph/conflict closure from the complete seed set.

Unknown document/clause is `resource_not_found`.

Success must contain non-empty source-backed evidence for a valid found clause plus any required attached context/conflict sources.

## 16. `get_context`

Implement exact `source_id` lookup and the closed `context_level` enum:

- `required`;
- `supporting`;
- `diagnostic`.

Each level includes all preceding levels. Relation-family booleans intentionally narrow this explicit inspection request, but they do not alter the automatic required closure previously performed by search/clause operations.

The response `context` object always contains the required arrays:

- `parents`;
- `applicability`;
- `dependencies`;
- `definitions`;
- `exceptions`;
- `notes`;
- `tables`;
- `references`;
- `versions`;
- `adjacent`.

Disabled or unavailable families are empty arrays rather than missing properties.

Conflict closure preserves every material side reached through enabled families.

## 17. Metadata/list/page tools

Retain and align the already planned Phase 2 tools:

- `get_document_metadata`;
- `list_documents`;
- `get_page_reference`.

These tools remain direct catalog/page projections and do not run evidence closure unless the design explicitly requires it.

No absolute filesystem path, raw source locator, credential, or inferred legal force may appear in public output.

## 18. Resources

Advertise the design's initial resources/templates only when implemented and validate their canonical URI spelling.

Resource reads use the same active release/catalog authority and strict safety rules as tools.

Source/clause evidence resources, where defined by Section 22, must project the same context-complete source/evidence semantics rather than a separate partial implementation.

Page resources remain authorized page access, never arbitrary filesystem reads.

Release resources expose safe immutable release metadata only.

## 19. MCP server behavior

Reuse the existing Phase 2 MCP protocol/admission plans for:

- JSON-RPC framing;
- strict argument/output schema validation;
- bounded frames;
- cancellation/deadlines;
- request admission;
- byte budgets;
- terminal-state atomicity;
- stable tool/resource lists for process lifetime.

The correction changes **which Phase 2 evidence tools are implemented successfully**, not the transport safety contract.

A runtime process advertises only implemented capabilities. A later release pointer change becomes visible after restart according to the design; in-session lists do not mutate silently.

## 20. CLI behavior

Phase 2 `clausesift search` and `clausesift get-clause` are no longer labelled as context-incomplete diagnostic substitutes.

They call the shared context-complete evidence service and expose the same source/context/conflict semantics as Python/MCP.

Human-readable formatting may differ, but a machine-readable mode must retain every semantic field needed to reproduce the shared result and must not suppress blocking warnings/conflicts.

`get-context`, metadata/list/page, release inspection, activation, and rollback commands follow the same shared service/release authority.

## 21. Python API

Expose typed service/result objects rather than backend-native SQLite rows.

The Python public API is the canonical reusable implementation beneath CLI and MCP, including:

- search;
- exact clause retrieval;
- context inspection;
- metadata/list/page access;
- release metadata where public;
- typed domain errors.

Do not provide a second public "direct" evidence API whose success could be mistaken for complete ordinary evidence. Lower-level exact/lexical primitives may remain internal/testing interfaces.

## 22. Central serializer

Implement one strict Evidence Package serializer/validator.

Before returning any evidence-bearing success it independently checks at minimum:

- release ID consistency;
- item document/source identity and catalog ownership;
- source text and citation projection;
- page-span/box projection;
- canonical classifications and provenance;
- transformation/build lineage references;
- selection roles and seed IDs;
- retrieval record channels/ranks/scores supported by the resolved mode;
- context completeness;
- context paths/edge provenance;
- conflict reasons;
- required context targets;
- material conflict array completeness;
- warning schema/ordering;
- output/frame bounds.

Serialization failure is fail-closed; adapters cannot bypass it.

## 23. Ordering

Freeze deterministic total orders for all output collections according to the detailed design.

At minimum preserve stable ordering for:

- direct retrieval seeds;
- expanded/conflict evidence items;
- selection roles;
- context paths and path steps;
- context targets;
- conflict records/positions/source IDs/spans;
- warnings;
- documents/list pagination.

Never rely on SQLite physical order, Python hash iteration, or backend return order.

## 24. Release and runtime integrity

The evidence service opens only a fully validated immutable active release.

Startup validation checks every schema/artifact/rule version needed to execute ordinary evidence semantics.

A lazy integrity failure for any later optional model follows quarantine rules; Phase 2 exact/lexical operation itself must not require a semantic model.

Rollback restores catalog, relationship/context/conflict artifacts, `lineage.json`, lexical index, rule/configuration identities, and the active pointer as one release.

## 25. Evaluation

Extend Phase 2 evaluation beyond direct lexical hits.

The final user-facing exact/lexical evidence path must be evaluated end to end for:

- correct direct source/edition/clause;
- citation/page correctness;
- required scope/applicability;
- required dependencies/definitions/exceptions;
- required table context;
- context target materialization;
- material conflict all-side completeness;
- warnings/completeness states;
- Python/CLI/MCP semantic equivalence.

Lexical Recall@K remains a seed-retrieval gate, not proof of Evidence Package correctness.

## 26. Required conformance fixtures

Include end-to-end fixtures for:

1. exact clause with no expansion;
2. exact clause requiring parent/applicability context;
3. lexical hit requiring definition/dependency context;
4. exception plus its condition;
5. table-row seed requiring table/clause context;
6. empty structural target represented only in `context_targets`;
7. unresolved required reference on standard tier producing visible incomplete state/warning;
8. the corresponding critical-tier release blocker;
9. confirmed material conflict forcing all positions;
10. standard-tier unresolved conflict;
11. required graph/conflict fixed-point expansion;
12. context-limit failure with no partial response;
13. no-match complete empty response;
14. status/edition filter preserving direct seed constraints while required attachments retain actual metadata;
15. CLI/Python/MCP byte-equivalent semantic projections after transport/format normalization.

## 27. Negative/security fixtures

Prove rejection of:

- malformed IDs and over-limit strings/arrays;
- extra JSON properties;
- unsupported enum values;
- forged/foreign source IDs;
- path traversal/resource URI tricks;
- absolute-path leakage;
- context path using a non-validated edge;
- context target with source-bearing fields;
- source item with mismatched citation/page spans;
- missing required conflict side;
- one-sided conflict serialization;
- output over frame limit;
- request cancellation/deadline race publishing a later success.

## 28. Implementation sequence

1. complete the Phase 2 required-context and material-conflict corrective data contracts;
2. implement build/release validation for required graph/conflict artifacts;
3. implement the shared exact/lexical seed service;
4. implement required graph/conflict fixed point;
5. implement strict source-backed evidence projection;
6. implement context-target projection;
7. implement conflict projection;
8. implement typed warning/completeness routing;
9. implement the central strict serializer;
10. expose the typed Python service;
11. update CLI search/clause/context to use it;
12. update MCP tools/resources to use it;
13. run protocol/admission/cancellation conformance;
14. add cross-interface equivalence tests;
15. add end-to-end evidence-semantics evaluation;
16. add corruption, failure-injection, activation, and rollback tests;
17. update Phase 2 release reports/gates;
18. verify later Phase 3 seed retrieval can enter this service without schema or semantics changes.

## 29. Acceptance criteria

Phase 2 evidence-service correction is complete only when:

1. exact/lexical direct seed retrieval remains deterministic and edition-safe;
2. every evidence-bearing exact/lexical success performs complete required graph/conflict closure;
3. one central serializer enforces the current closed Evidence Package contract;
4. `search_evidence`, `get_clause`, and `get_context` implement the current Section 22 semantics rather than returning feature-unavailable/partial direct evidence for ordinary Phase 2 capabilities;
5. metadata/list/page surfaces remain safe and exact;
6. source/build/assembly lineage is complete and separated correctly;
7. context targets are represented without fabricated evidence;
8. every material conflict side is present;
9. typed warnings/completeness/error routing matches the design;
10. required bound overflow returns `context_limit_exceeded` with no partial package;
11. Python, CLI, and MCP use the same evidence service and produce semantically identical results;
12. strict request/output/protocol/admission/cancellation bounds pass conformance tests;
13. held-out end-to-end evidence correctness, activation, and rollback gates pass;
14. no Phase 3 dense/RRF or Phase 4 reranking/supporting-context implementation is pulled into this corrective Phase 2 work.
