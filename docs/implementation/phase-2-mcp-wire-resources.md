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

## 2. Common tool advertisement and wire rules

Every advertised tool has:

- stable name and non-empty description;
- strict descriptive JSON Schema input;
- strict success-output schema;
- accurate read-only annotation;
- closed objects with `additionalProperties: false` where required by the design.

A successful tool returns its validated public object in `structuredContent` and exactly one legacy JSON text block derived from that same object. Parsing the legacy text must produce an object exactly equal to `structuredContent`.

A known tool's domain failure returns:

- `isError: true`;
- no `structuredContent`;
- exactly one text block containing the strict shared error object.

Protocol errors remain JSON-RPC protocol errors rather than tool-error objects.

All public serialization goes through central allowlists. Absolute paths, workspace roots, credentials, raw exceptions, mutable internal locators, and unknown internal fields fail closed rather than leaking.

## 3. Common request bounds

Enforce the current Section 22 bounds before expensive work, including:

- query: trimmed 1-4096 Unicode scalars and no more than 16,384 encoded UTF-8 bytes;
- opaque `document_id`/`source_id`: 1-128 and `^[a-z0-9][a-z0-9._:-]{0,127}$`;
- clause/document-code/edition/jurisdiction/discipline/status/type/mode/context-level strings: 1-128 plus applicable closed enums;
- each filter array: at most 64 unique items;
- `search_evidence`: at most 256 total filter values;
- result limit: 1-100;
- cursor: at most 4096 plus authenticated release binding;
- page number: positive 32-bit and within manifested page count.

Apply the applicable limit both before and after field-specific normalization.

## 4. `search_evidence`

Phase 2 seed selection uses the installed exact/identifier and lexical capabilities, then always enters required graph-and-material-conflict closure.

Filters constrain direct seeds; they never erase required context/conflict attachments.

Success root is exactly:

```text
{
  query,
  retrieval_mode,
  release,
  context_completeness,
  evidence,
  context_targets,
  conflicts,
  warnings
}
```

No match is a `complete` success with empty evidence/context-target/conflict arrays.

Representative errors:

- invalid/over-limit arguments -> `identifier_invalid`;
- explicit unavailable later mode -> `feature_unavailable`;
- required closure overflow -> `context_limit_exceeded` with no partial package;
- relevant release-integrity failure -> `release_integrity_failed` through the design-defined route.

## 5. `get_clause`

Selection is exact `document_id` + exact normalized clause number. No fuzzy clause lookup, same-number cross-edition lookup, or latest-edition substitution is permitted.

Every source in the exact Section 14.1 lookup set is a direct `retrieval_seed`; required graph/conflict closure then runs from the complete direct set.

Success root is exactly:

```text
{
  release,
  context_completeness,
  evidence,
  context_targets,
  conflicts,
  warnings
}
```

Unknown document/clause is `resource_not_found`; required overflow is `context_limit_exceeded` with no partial success.

## 6. `get_context`

Selection is exact `source_id` plus the closed `context_level` enum:

- `required`;
- `supporting`;
- `diagnostic`.

Each level includes preceding levels. Relation-family include flags narrow this explicit inspection request but do not change automatic required closure of search/clause results.

Success root is exactly:

```text
{
  release,
  source_id,
  context_completeness,
  evidence,
  context_targets,
  context,
  conflicts,
  warnings
}
```

`context` always includes arrays for parents, applicability, dependencies, definitions, exceptions, notes, tables, references, versions, and adjacent. Disabled/not-found families are empty arrays rather than absent fields.

## 7. Metadata/list/page tools

### `get_document_metadata`

Exact document ID, no edition substitution. Success is `{release, document}` using the safe manifest/catalog projection.

### `list_documents`

Uses exact normalized filters, stable design ordering, and release-bound authenticated cursor. Success is `{release, items, next_cursor}`.

### `get_page_reference`

Exact document ID + valid one-based page. Success is `{release, document_id, page_number, page_label, page_uri, content_hash}`.

No tool exposes the internal source locator or filesystem path.

## 8. Evidence-item MCP invariants

`search_evidence`, `get_clause`, and `get_context` use the single Section 21 Evidence Package serializer from `phase-2-evidence-service.md`.

The MCP adapter cannot:

- omit required context/conflict evidence for payload convenience;
- fabricate source-backed evidence for empty structural targets;
- drop typed warnings;
- add ad-hoc fields outside closed schemas;
- transform original source text into generated answer text;
- implement alternate traversal/conflict rules.

A complete success that cannot fit the applicable output/frame contract fails through the design-defined route rather than producing a partial/oversized result.

## 9. Dual-revision tool conformance

Run all six tools under both supported design protocol paths:

- per-request `2026-07-28`;
- initialized-session `2025-11-25`.

For every tool/revision verify:

- advertised input/output schemas;
- success `structuredContent`;
- exact legacy-text object equality;
- domain error `isError: true` with no structured content;
- no revision-specific semantic drift.

## 10. Canonical resource URI generation and parsing

Generate resource variable segments by UTF-8 encoding normalized semantic values, leaving only RFC 3986 unreserved bytes literal and percent-encoding all other bytes with uppercase hex.

For client-supplied resource reads:

1. validate exact route shape;
2. decode each variable exactly once using strict UTF-8;
3. reject malformed percent escapes/invalid UTF-8;
4. re-encode canonically;
5. require byte-identical supplied/canonical segment;
6. apply field schema/normalization;
7. only then perform parameterized catalog lookup.

No resource URI is converted to a filesystem path by string concatenation.

Negative fixtures cover encoded separators, `%`, `?`, `#`, spaces, non-ASCII, lowercase escapes, malformed escapes, invalid UTF-8, route overlength, and percent-looking literal IDs without double decoding.

## 11. Resource catalogue and cardinality

The resource catalogue is immutable for one server process and advertises only implemented read-only resources/templates. v0.1 does not advertise subscription or list-change notification.

Every successful `resources/read` contains exactly one content item whose `uri` is byte-identical to the canonical requested URI and whose MIME/payload exactly matches the resource contract.

Unknown canonical resources never return an empty success.

## 12. Document resource

`standards://document/{document_id}` returns one `TextResourceContents` item with `mimeType: application/json`.

Its `text` is RFC 8785 UTF-8 serialization of the same safe `{release, document}` object returned by `get_document_metadata`.

The canonicalized tool object and resource bytes must be equal.

## 13. Clause resource

`standards://clause/{document_id}/{clause_number}` is a context-complete evidence resource.

It uses the same exact lookup set and required graph/conflict closure as `get_clause`, and returns the exact strict JSON resource payload defined by Section 22.3.

No fuzzy/edition substitution is allowed.

If complete required closure exceeds a resource bound, follow the design's resource error route and return no contents.

## 14. Source resource — raw validated source text

`standards://source/{source_id}` is **not** an Evidence Package wrapper.

For every successful source read, return exactly one `TextResourceContents` item with:

- `uri`: exact canonical requested URI;
- `mimeType: text/plain;charset=utf-8`;
- `text`: exactly the selected source chunk's validated `original_text` bytes decoded as UTF-8 according to the canonical source-text contract.

There is no JSON wrapper and no citation, lineage, context, conflict, warning, or metadata envelope around this resource text.

The source resource is a raw source-inspection surface. Context-complete evidence semantics remain available through `search_evidence`, `get_clause`, and `get_context` rather than changing this resource's canonical byte contract.

Tests must prove:

- returned text is byte-for-byte the validated `original_text` UTF-8 payload;
- no separator/wrapper/newline is added by the resource adapter;
- MIME type is exact;
- unknown source uses the revision-specific resource-miss protocol route;
- no internal source locator/path is exposed.

## 15. Page resource

`standards://page/{document_id}/{page_number}` returns one `BlobResourceContents` item with `mimeType: application/pdf` according to the design's verified original-PDF contract.

The requested page is navigation metadata selecting the canonical URI; the returned content is the exact design-defined verified PDF bytes, not a falsely labelled page-render derivative.

All handle-bound containment/identity/stability/size/hash checks, page working-set reservation, complete-output limit, and terminal-state rules run before success is committed.

## 16. Current release resource

`standards://release/current` snapshots the verified active release for process lifetime and returns the strict safe immutable release summary/manifest digest defined by Section 22.3.

It contains no filesystem locators, credentials, mutable telemetry, or operator secrets.

## 17. Resource miss and integrity errors

Malformed/non-canonical URI -> protocol invalid-params route before catalog lookup.

Well-formed canonical unknown resource -> revision-specific resource-miss route defined by Section 22.4 (including `-32602`/`-32002` where assigned), never an empty success or tool-style error object.

Page/source integrity failure follows the design's safe protocol/internal-error route with no contents, no partial payload, no path, and no raw exception.

Cancellation terminal-state precedence is preserved if cancellation already won.

## 18. Cross-surface equality and non-equality

Where two surfaces intentionally project the same logical object, derive both from one typed public representation and assert equality, including:

- tool structured success == parsed legacy text;
- canonical document-metadata tool bytes == document-resource text;
- list item document summaries use the same safe projection;
- page reference URI/hash agree with page-resource identity/verified bytes;
- release resource digest agrees with active verified release manifest;
- clause tool/resource agree where Section 22 defines equivalent evidence payloads.

The source resource is intentionally **not** equal to an evidence-item JSON projection: its canonical contract is raw `original_text` only.

## 19. Protocol/admission inheritance

Evidence tools/resources inherit all existing Phase 2 MCP constraints, including:

- 1,048,576-byte inbound complete-frame limit;
- 65,536-byte canonical arguments budget;
- 1,048,576-byte non-page complete-output limit;
- 33,554,432-byte page complete-output limit;
- 67,108,864-byte process page working-set budget;
- `max_in_flight_requests` 1..1024;
- atomic success/error/cancel/deadline terminal state;
- cancellation no-response semantics;
- control-plane liveness under saturation;
- stdout framing/redaction rules.

Required graph/conflict traversal receives no exemption.

## 20. Conformance tests

### Tool tests

For every tool/revision:

- strict advertisement/schema;
- exact success/error shapes;
- legacy/structured equality;
- boundary/one-over request tests;
- no-match search;
- required context/conflict closure;
- explicit later-mode unavailable behavior;
- no-partial required overflow.

### Evidence semantics tests

- exact clause plus required context;
- lexical search plus applicability/exception/table context;
- material conflict all-side preservation;
- empty context target;
- unresolved-required warnings/completeness;
- source/status/edition preservation;
- Python/CLI/MCP source/build/assembly lineage equality.

### Resource tests

- canonical URI round trip and negative cases;
- exactly one content item;
- document/release/page/ clause exact contracts;
- source exact raw `text/plain;charset=utf-8` contract;
- source byte equality with `original_text`;
- resource-miss routing;
- page/source integrity failure;
- cancellation/admission/output-budget races.

## 21. Acceptance criteria

Phase 2 MCP wire/resource work is complete only when:

1. all six current Phase 2 tools are advertised only with complete current-design semantics;
2. search/clause/context tools use the shared context/conflict-complete evidence service;
3. explicit later unsupported capabilities fail visibly;
4. dual-revision tool schemas/success/errors conform;
5. legacy text equals structured success exactly;
6. resource URIs are canonical/safe;
7. document/clause/page/release resources obey exact Section 22 contracts;
8. `standards://source/{source_id}` returns only exact raw validated `original_text` with exact `text/plain;charset=utf-8` MIME and no wrapper;
9. required context/conflict evidence is never dropped from evidence tools for payload convenience;
10. public allowlists prevent path/credential/internal leakage;
11. protocol/admission/cancellation/frame budgets apply to all new evidence operations;
12. no Phase 3 dense/RRF or Phase 4 reranking/supporting-context behavior is pulled into Phase 2.
