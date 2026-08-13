# Phase 2 MCP Wire and Resource Contract

**Project:** ClauseSift  
**Phase:** 2 — Exact Retrieval MVP  
**Status:** Normative Phase 2 implementation-plan appendix  
**Primary design authority:** `docs/design.md` Sections 19-22 and 31  
**Evidence service:** `docs/implementation/phase-2-evidence-service.md`  
**Protocol companions:** `phase-2-mcp-protocol-conformance.md`, `phase-2-mcp-admission-budgets.md`

## 1. Purpose

Phase 2 exposes the current-design ordinary exact/lexical evidence behavior through MCP without changing the semantics of the shared evidence service.

The Phase 2 tool surface is:

- `search_evidence`;
- `get_clause`;
- `get_context`;
- `get_document_metadata`;
- `list_documents`;
- `get_page_reference`.

The Phase 2 resource catalogue contains the current design's read-only document, clause, source, page, and current-release resources/templates.

A Phase 2-only runtime does not claim Phase 3 dense/hybrid or Phase 4 reranker/supporting-context high-accuracy capability. Explicit unavailable later modes fail visibly.

### 1.1 Protocol-companion scope correction

`phase-2-mcp-protocol-conformance.md` and `phase-2-mcp-admission-budgets.md` remain normative for their transport, framing, argument/output-budget, admission, cancellation, deadline, terminal-state, and protocol-control rules.

They predate the current Phase 2 surface boundary. Any older statement in those companions that limits Phase 2 to metadata/list/page/release surfaces, or defers `search_evidence`, `get_clause`, `get_context`, clause/source resources, or ordinary Evidence Graph traversal to Phase 4, is superseded by current `docs/design.md`, `phase-2-current-design-correction.md`, and this wire/resource contract.

Implementers apply the companions' stable transport/admission rules to the complete current six-tool Phase 2 surface. Their old tool/resource list is not phase-scope authority.

## 2. Common tool advertisement and wire rules

Every advertised tool has a stable name/description, strict descriptive input schema, strict success schema, accurate read-only annotation, and closed output objects where required by the design.

A successful call returns its validated public object in `structuredContent` and exactly one legacy JSON text block derived from the same object. Parsing the legacy text must equal `structuredContent` exactly.

A known tool's domain failure returns `isError: true`, no `structuredContent`, and exactly one strict JSON error text block. Protocol errors remain JSON-RPC protocol errors.

All public serialization uses central allowlists; absolute paths, workspace roots, credentials, raw exceptions, mutable internal locators, and unknown internal fields fail closed.

## 3. Common request bounds

Apply the current Section 22 bounds before expensive work, including query 1-4096 scalars and at most 16,384 UTF-8 bytes; opaque IDs 1-128 with the design pattern; exact filter strings 1-128 plus closed enums; each filter list at most 64 unique values; at most 256 total `search_evidence` filter values; result limit 1-100; cursor at most 4096 plus authenticated release binding; and page number within the manifested positive 32-bit range.

Validate applicable bounds before and after field-specific normalization.

## 4. Evidence tools

### `search_evidence`

Phase 2 uses exact/identifier and lexical direct seeds, then always runs required graph-and-material-conflict closure. Filters constrain direct seeds, not required attachments.

Success is exactly `{query, retrieval_mode, release, context_completeness, evidence, context_targets, conflicts, warnings}`. No match is a complete empty success. Invalid input, explicit unavailable mode, required closure overflow, and integrity failures use the exact design routes; required overflow never produces a partial package.

### `get_clause`

Use exact document ID + exact normalized clause. Select the complete Section 14.1 lookup set as direct seeds and run required graph/conflict closure. No fuzzy or edition substitution. Success is exactly `{release, context_completeness, evidence, context_targets, conflicts, warnings}`.

### `get_context`

Use exact `source_id` plus closed `required`/`supporting`/`diagnostic` level. Success is exactly `{release, source_id, context_completeness, evidence, context_targets, context, conflicts, warnings}`; `context` always contains the design-required relation-family arrays.

All evidence tools use the single Section 21 serializer and cannot drop required context/conflict evidence, fabricate empty-node source evidence, drop warnings, or add ad-hoc schema fields.

## 5. Metadata/list/page tools

`get_document_metadata`, `list_documents`, and `get_page_reference` keep their current exact safe catalog/page contracts. No surface exposes an internal source locator or filesystem path.

## 6. Dual-revision conformance

Run all six tools under both supported protocol paths (`2026-07-28` per-request and `2025-11-25` initialized-session). For each tool/revision verify strict schemas, success `structuredContent`, exact legacy-text equality, strict domain-error representation, and no semantic drift.

## 7. Canonical resource URI rules

Generate variable segments by UTF-8 encoding normalized semantic values, leaving only RFC 3986 unreserved bytes literal and percent-encoding all other bytes with uppercase hex.

For reads, validate exact route shape, strict-decode exactly once, reject malformed escapes/UTF-8, re-encode canonically, require byte equality, then apply field schema/normalization before parameterized catalog lookup. Never concatenate a client URI segment into a filesystem path.

## 8. Resource catalogue and success cardinality

The resource catalogue is immutable for one process and advertises only implemented read-only document, clause, source, page, and current-release resources/templates. v0.1 does not advertise subscription/list-change notification.

Every successful read returns exactly one content item with the exact canonical requested URI and exact MIME/payload required by Section 22. Unknown canonical resources never return empty success.

## 9. Document resource

`standards://document/{document_id}` returns one JSON `TextResourceContents` whose text is RFC 8785 serialization of the same safe `{release, document}` public object as `get_document_metadata`.

## 10. Clause resource

`standards://clause/{document_id}/{clause_number}` uses the same exact lookup set and required graph/conflict closure as `get_clause`, returning the exact strict JSON resource payload defined by Section 22.3. No fuzzy/edition substitution is allowed.

## 11. Source resource — raw validated source text

`standards://source/{source_id}` is not an Evidence Package wrapper.

A successful read returns exactly one `TextResourceContents` with:

- exact canonical requested `uri`;
- exact `mimeType: text/plain;charset=utf-8`;
- `text` exactly equal to the selected source chunk's validated `original_text` under the canonical UTF-8 source-text contract.

There is no JSON wrapper and no citation, lineage, context, conflict, warning, or metadata envelope.

Tests prove byte-for-byte text equality, exact MIME, no added separator/newline/wrapper, correct unknown-source resource-miss route, and no internal locator exposure.

## 12. Page resource

`standards://page/{document_id}/{page_number}` returns one `application/pdf` blob resource according to the verified original-PDF contract. Page number is navigation metadata; all handle-bound containment/identity/stability/size/hash, working-set, output-budget, and terminal-state checks run before success.

## 13. Current release resource

`standards://release/current` snapshots the verified active release for process lifetime and returns the strict safe immutable release summary/manifest digest, excluding paths, credentials, mutable telemetry, and operator secrets.

## 14. Resource misses and integrity failures

Malformed/non-canonical URI uses protocol invalid-params before catalog lookup. Canonical unknown resources use the revision-specific Section 22.4 resource-miss route, never empty success or a tool-style error object. Page/source integrity failure uses the safe design protocol/internal-error route with no contents/partial payload/path/raw exception. Cancellation terminal-state precedence remains authoritative.

## 15. Cross-surface equality and intentional non-equality

Where surfaces represent the same logical public object, derive them from one typed representation and test equality: tool structured vs legacy text, document tool vs document resource, page-reference URI/hash vs page resource, release digest vs current-release resource, and clause tool/resource where Section 22 defines equivalent payloads.

The source resource is intentionally not equal to evidence-item JSON: its canonical contract is raw `original_text` only.

## 16. Protocol/admission inheritance

Apply the existing transport/admission companions to every current evidence operation, including the 1,048,576-byte inbound frame, 65,536-byte canonical arguments, 1,048,576-byte non-page output, 33,554,432-byte page output, 67,108,864-byte page working-set, `max_in_flight_requests` 1..1024, atomic terminal state, cancellation no-response semantics, control-plane liveness, and stdout/redaction rules.

Required graph/conflict traversal receives no exemption.

## 17. Conformance tests

Tool tests cover strict schemas, exact success/error shapes, legacy/structured equality, boundary/one-over inputs, no-match search, required graph/conflict closure, unsupported later modes, and no-partial required overflow.

Evidence tests cover exact clause, lexical context, material conflict all-side preservation, empty context target, unresolved-required warnings, source/status/edition preservation, and Python/CLI/MCP lineage equality.

Resource tests cover canonical URI round trip/negatives, one-item cardinality, exact document/clause/page/release contracts, exact raw source MIME/bytes, resource-miss routing, integrity failure, and cancellation/admission/output-budget races.

## 18. Acceptance criteria

Phase 2 MCP wire/resource work is complete only when:

1. all six current Phase 2 tools are advertised with complete current-design semantics;
2. evidence tools use the shared context/conflict-complete service;
3. explicit later unsupported capabilities fail visibly;
4. dual-revision tool schemas/success/errors conform;
5. legacy text equals structured success exactly;
6. resource URIs are canonical/safe;
7. document/clause/page/release resources obey exact Section 22 contracts;
8. source resources return only exact raw validated `original_text` with exact `text/plain;charset=utf-8` MIME and no wrapper;
9. older protocol/admission companion surface-scope statements are treated as superseded while their transport/admission rules remain authoritative;
10. required evidence is never dropped for payload convenience;
11. public allowlists prevent path/credential/internal leakage;
12. transport/admission/cancellation/frame budgets apply to all current evidence operations;
13. no Phase 3 dense/RRF or Phase 4 reranking/supporting-context behavior is pulled into Phase 2.
