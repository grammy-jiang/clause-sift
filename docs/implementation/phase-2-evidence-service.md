# Phase 2 Evidence Service and Public Surface Implementation Plan

**Project:** ClauseSift  
**Phase:** 2 — Exact Retrieval MVP  
**Status:** Normative current-design corrective implementation plan  
**Primary design authority:** `docs/design.md` Sections 7.2, 17, 19-22, 26-27, 29, and 31  
**Companions:** `phase-2-required-context-closure.md`, `phase-2-material-conflict-closure.md`, `phase-2-mcp-wire-resources.md`

## 1. Purpose

Current `docs/design.md` assigns Phase 2 the ordinary context-complete exact/lexical evidence path. Phase 2 therefore owns one shared service that takes exact/lexical direct seeds through required graph closure, material-conflict fixed-point closure, strict Evidence Package serialization, and Python/CLI/MCP projection.

This plan does not add Phase 3 dense/RRF seed retrieval or Phase 4 reranking/supporting-context high-accuracy behavior.

## 2. One shared service

The only ordinary evidence pipeline is:

```text
validated request
  -> exact/identifier and/or lexical direct seed selection
  -> required Evidence Graph closure
  -> material-conflict closure
  -> repeat graph/conflict closure to least fixed point
  -> strict Evidence Package serializer
  -> typed Python result/error
  -> CLI/MCP adapters
```

Adapters do not reimplement SQL, traversal, conflict, warning, pagination, or serialization logic.

Internal direct lookup/search primitives may exist for implementation/testing, but they are not public substitutes for context-complete evidence.

## 3. Phase 2 retrieval capabilities

Phase 2 supports the exact/lexical capabilities available before semantic retrieval.

- explicit `exact` uses the exact/lexical path defined by current design;
- `auto` resolves only to capabilities present in the installed runtime and active release;
- when `auto` would have used a later dense/reranker capability but that capability is unavailable and the runtime falls back to the available Phase 2 exact/lexical path, the successful result **must include the typed `retrieval_capability_unavailable` warning** required by the design;
- explicit unsupported later modes fail with `feature_unavailable` rather than being relabelled as successful Phase 2 results.

The capability warning is part of the success contract, not an optional diagnostic log. Clients must be able to distinguish a full-capability result from an `auto` fallback.

Required context/conflict correctness is independent of mode speed.

## 4. Request-validation boundary

Validate the current Section 22 field/aggregate bounds before expensive work.

At minimum preserve:

- query 1-4096 trimmed Unicode scalars and <=16,384 encoded UTF-8 bytes;
- opaque IDs 1-128 and the exact public opaque-ID pattern;
- exact lookup/filter strings 1-128 plus applicable closed enums;
- filter arrays <=64 unique values each;
- `search_evidence` <=256 total filter values;
- result limit 1-100;
- cursor <=4096 plus authenticated release binding;
- page number within the manifested positive 32-bit range.

Apply the applicable limit before and after field-specific normalization. Invalid requests do not reach retrieval/model/page work.

## 5. Direct seed selection

### 5.1 Exact clause

`get_clause` validates exact document ID/clause, resolves the exact canonical clause with no fuzzy/edition substitution, selects every source in the complete Section 14.1 exact-lookup set, marks them direct `retrieval_seed` items, and then runs required graph/conflict closure from the complete set.

### 5.2 Search

`search_evidence` uses installed exact/identifier and lexical seed channels for the resolved Phase 2 mode.

Metadata filters are exact. Values are ORed within a list and categories are ANDed. The current design's default status behavior applies; explicit null removes the default status filter where defined.

Filters constrain direct seeds only. Required context/conflict attachments preserve their actual edition/status/jurisdiction/type even when those values fall outside a direct-seed filter.

### 5.3 No match

A valid search with no direct matches is still a successful result, not a not-found error. It must return:

- `context_completeness: complete`;
- empty `evidence`;
- empty `context_targets`;
- empty `conflicts`;
- a typed **`evidence_insufficient` warning** as required by the current design.

`warnings: []` is not valid for this no-match condition. The warning is the client-visible signal that the successful search did not find adequate evidence.

## 6. Required graph/conflict handoff

Every evidence-bearing Phase 2 request enters the fixed point defined by the required-context and material-conflict appendices.

Success occurs only after:

- required graph closure has satisfied or visibly represented all admitted required obligations;
- every material confirmed/unresolved conflict side required by the current release has been attached;
- newly attached conflict sources receive their own required closure;
- graph/conflict closure reaches the deterministic fixed point;
- all applicable bounds pass;
- central strict serialization passes.

If complete required closure would exceed a declared bound, return `context_limit_exceeded` and publish no partial Evidence Package.

## 7. Evidence Package roots

`search_evidence` returns exactly `{query, retrieval_mode, release, context_completeness, evidence, context_targets, conflicts, warnings}`.

`get_clause` returns exactly `{release, context_completeness, evidence, context_targets, conflicts, warnings}`.

`get_context` returns exactly `{release, source_id, context_completeness, evidence, context_targets, context, conflicts, warnings}`.

Unknown root properties fail closed.

## 8. Source-backed evidence item

Every `evidence[]` item uses the current closed Section 21 schema and is source-faithful.

The serializer verifies exact source/document/chunk/node ownership; document/edition/status projections; canonical classifications/provenance; exact `original_text`; page spans/boxes/citation; complete source/build/assembly lineage; typed warnings; and closed public fields.

Generated summaries never replace source text.

## 9. Lineage dimensions

Source provenance binds approved manifest/source identity and exact contributed canonical-node/page spans.

Build provenance binds release artifact hashes, vocabulary/classification provenance, canonical/parser/page/chunk/relationship/conflict transformations, and graph/context/conflict rule identities. Immutable `lineage.json` remains query-independent.

Assembly provenance uses only current closed fields such as selection roles, seed source IDs, context completeness, exact/lexical retrieval records, context paths, and conflict reasons. Phase 2 never fabricates dense/fusion/rerank records.

## 10. Context targets

A valid required traversal may reach an empty structural node with no source text. Represent it only in `context_targets` using the exact safe catalog/manifest projection and accepted paths. Never fabricate original text/citation/page/source lineage for an empty node.

## 11. Conflicts

Every evidence-bearing success includes the required `conflicts` array, empty when no material record applies.

Reject missing records/positions/source covers, one-sided conflict projection, wrong span/source ownership, invalid state/dimension/order, false precedence, or generated conflict prose presented as source authority.

## 12. Completeness and errors

Use only `complete`, `incomplete_required`, and `truncated_optional` under their exact design conditions. Required bound overflow is `context_limit_exceeded` with no partial success.

## 13. Typed warnings

Implement the exact diagnostics needed by ordinary Phase 2 evidence, including source-coordinate/parser/OCR uncertainty, classification unresolved, context incomplete/cycle/status boundary, cross-reference unresolved, table anomaly, applicability/evidence insufficiency, `evidence_conflict`, `conflict_unresolved`, and `retrieval_capability_unavailable` where applicable.

Two warning cases are explicitly mandatory:

1. an `auto` request that falls back because a later dense/reranker capability is unavailable returns `retrieval_capability_unavailable`;
2. a valid no-match search returns `evidence_insufficient` even though the response is otherwise a `complete` empty success.

Warnings use code-owned messages and closed safe details.

## 14. Evidence tools

`search_evidence`, `get_clause`, and `get_context` implement current Section 22 semantics directly and all call the shared service. Metadata/list/page tools remain exact safe projections without invented evidence semantics.

## 15. MCP resources are separate contracts

MCP resources obey `phase-2-mcp-wire-resources.md` and Section 22.3 exactly.

- the clause resource is context-complete where the design specifies it;
- **the source resource is not an Evidence Package projection**: `standards://source/{source_id}` returns only validated source chunk `original_text` with exact `text/plain;charset=utf-8` MIME and no wrapper;
- document/release/page resources keep their own exact MIME/payload contracts.

A richer evidence tool does not alter a resource's canonical byte contract.

## 16. CLI and Python API

The typed Python API is the canonical service layer. CLI search/get-clause/get-context use the same evidence service and machine-readable output cannot drop evidence semantics, warnings, context targets, conflicts, or typed errors.

Do not expose a second public direct-evidence API that could be mistaken for complete ordinary evidence.

## 17. Central serializer

One serializer checks release identity; source/catalog ownership; original text/citation/page projections; classifications/provenance; source/build/assembly lineage; selection roles/seeds/retrieval records; context completeness/paths/targets; conflicts/reasons; warnings; deterministic ordering; public allowlists; and output/frame bounds.

Disagreement fails closed.

## 18. Release/runtime integrity

Evidence work opens only a validated immutable active release. Startup/release validation verifies all schema/artifact/rule versions needed by exact/lexical retrieval plus graph/context/conflict/serializer behavior. Rollback restores the matching catalog/index/relationship/context/conflict/lineage/configuration set atomically.

## 19. Evaluation alignment

Phase 2 evaluation follows `phase-2-release-gates.md` exactly.

- retrieval Recall@K and classification/conflict candidate/precision families use the design's probabilistic Wilson gates;
- required-context/path/status/order correctness is a zero-failure complete deterministic traversal conformance suite;
- conflict position/source/lineage completeness and all-side runtime preservation is a zero-failure complete deterministic conflict conformance suite;
- strict Evidence Package/interface behavior is deterministic conformance.

Do not invent a separate held-out 100% context/all-side gate in place of Section 29.4.

## 20. Required conformance fixtures

Include exact clause with/without expansion, lexical dependency/definition, exception+condition, table context, empty target, unresolved standard/critical cases, confirmed/unresolved conflicts, graph-conflict fixed point, required overflow, **no-match success with mandatory `evidence_insufficient`**, **`auto` fallback with mandatory `retrieval_capability_unavailable`**, filter/status preservation, Python/CLI/MCP equivalence, and raw source resource byte/MIME contract.

## 21. Negative/security fixtures

Cover malformed IDs/overlimits/extra properties, forged sources, resource URI attacks, path leakage, invalid graph edges, fabricated context-target source fields, citation/page mismatch, missing conflict side, false precedence, output-budget overflow, cancellation/deadline late-success races, **no-match success missing `evidence_insufficient`**, and **auto fallback missing `retrieval_capability_unavailable`**.

## 22. Implementation sequence

1. complete/validate graph/context/conflict release contracts;
2. implement exact/lexical seed service;
3. implement required graph/conflict fixed point;
4. implement evidence/context-target/conflict projections;
5. implement completeness/warning/error routing, including mandatory no-match and auto-fallback warnings;
6. implement central serializer;
7. expose typed Python service;
8. project through CLI/MCP tools;
9. implement each MCP resource according to its independent exact contract;
10. run protocol/security conformance and current Section 29.4 gates;
11. run activation/rollback validation.

## 23. Acceptance criteria

Phase 2 evidence-service work is complete only when exact/lexical seeds are deterministic/edition-safe; every ordinary evidence seed enters complete required graph/conflict closure; central strict serialization passes; evidence tools meet Section 22; **every no-match search includes `evidence_insufficient`**, **every applicable `auto` capability fallback includes `retrieval_capability_unavailable`**; metadata/list/page remain safe; source/build/assembly lineage is correct; empty targets are not fabricated; all material sides are preserved; completeness/warnings/errors match design; required overflow yields no partial package; Python/CLI/MCP evidence semantics are equivalent; MCP resources obey their independent exact contracts (especially raw source text); current Section 29.4 gates and protocol/security/activation/rollback conformance pass; and no Phase 3 dense/RRF or Phase 4 reranking/supporting-context implementation is pulled into Phase 2.
