# Phase 2 MCP Wire and Resource Contract

**Project:** ClauseSift  
**Phase:** 2 — Exact Retrieval MVP  
**Status:** Normative Phase 2 implementation-plan appendix  
**Primary design authority:** `docs/design.md` Sections 22 and 31  
**Companion protocol plans:** `docs/implementation/phase-2-mcp-protocol-conformance.md`, `docs/implementation/phase-2-mcp-admission-budgets.md`

## 1. Purpose and Phase 2 surface

Phase 2 advertises only MCP surfaces whose complete design contract can be satisfied without Phase 4 Evidence Graph runtime closure.

The public Phase 2 MCP tool surface is:

- `get_document_metadata`;
- `list_documents`;
- `get_page_reference`.

The public Phase 2 MCP resource surface is:

- `standards://document/{document_id}`;
- `standards://page/{document_id}/{page_number}`;
- `standards://release/current`.

The following design resources/tools remain **unadvertised until Phase 4** because their success semantics require final Evidence Package/context behavior:

- `search_evidence`;
- `get_clause`;
- `get_context`;
- `standards://clause/{document_id}/{clause_number}`;
- `standards://source/{source_id}` when exposed as part of the final evidence-oriented MCP contract.

This appendix defines the exact MCP wire shape and resource URI/success behavior only for the Phase 2-advertised subset.

## 2. Tool advertisement contract

Every advertised Phase 2 tool declares all of the following:

- stable tool name;
- non-empty human-readable description;
- strict JSON Schema input contract;
- strict JSON Schema success-output contract;
- read-only annotation consistent with actual behavior.

Every input-schema property has a non-empty description that states, as applicable:

- identifier domain;
- units;
- normalization;
- null/default behavior;
- filter-combination behavior;
- inclusive/exclusive numeric bounds;
- string/list bounds;
- cursor semantics.

All tool input and output objects use `additionalProperties: false` unless the design explicitly specifies a narrower nested extension point. Phase 2 must not advertise unconstrained generic success objects.

## 3. Tool success wire representation

A successful Phase 2 tool call returns the strict tool-specific success object in MCP `structuredContent`.

The same already-validated public success object is serialized exactly once into JSON for the legacy text representation and emitted as exactly one text content block.

The legacy JSON text:

- is derived from the validated public object, not from a second formatting path;
- parses to an object exactly equal to `structuredContent`;
- cannot contain an extra field omitted by `structuredContent`;
- cannot omit a field present in `structuredContent`;
- uses the central outbound serializer and public field allowlist;
- contains no absolute source path, workspace path, raw exception string, credential, or unallowlisted internal field.

Dual-revision tests compare parsed legacy text to `structuredContent` for exact equality on every Phase 2 success tool.

## 4. Phase 2 tool success objects

### 4.1 `get_document_metadata`

Selection: exact opaque `document_id`; no active/latest edition substitution.

Success object:

```text
{
  release,
  document
}
```

`document` is the safe manifest/catalog projection required by `docs/design.md`: exact vocabulary version, document type, normative status, lifecycle status, authority, jurisdictions/disciplines, source hash, review/admission state, and release identity, excluding internal source locators and inferred legal force.

Domain errors:

- malformed input → `identifier_invalid` tool error;
- valid unknown `document_id` → `resource_not_found` tool error.

### 4.2 `list_documents`

Selection: non-null filters are ANDed; exact normalized closed-enum/string values only; stable `(document_code, edition, document_id)` ordering; authenticated release-bound keyset cursor as defined by the Phase 2 plan.

Success object:

```text
{
  release,
  items,
  next_cursor
}
```

Every `items` entry is the same safe document metadata summary used by the document projection contract. `next_cursor` is string or null.

Domain errors:

- malformed filter/limit/cursor → `identifier_invalid`;
- structurally valid cursor bound to another release → `resource_not_found`.

### 4.3 `get_page_reference`

Selection: exact opaque `document_id` + one-based integer page number within manifested page count.

Success object:

```text
{
  release,
  document_id,
  page_number,
  page_label,
  page_uri,
  content_hash
}
```

`page_uri` is the canonical authorized `standards://page/...` URI; `content_hash` is the source-document SHA-256 required by the full-PDF page-resource contract.

Domain errors:

- malformed/out-of-range input → `identifier_invalid`;
- unknown document/unavailable page → `resource_not_found`.

## 5. Tool execution error branch

A well-formed `tools/call` that reaches a known Phase 2 tool but fails semantic validation/execution returns the MCP tool-error branch:

- `isError: true`;
- **no `structuredContent` field**;
- exactly one text content block;
- text is exactly one JSON serialization of the strict shared error object:

```text
{
  code,
  phase,
  severity,
  message,
  details?
}
```

The central serializer validates the error object against a separate strict internal schema using:

- `additionalProperties: false`;
- code-owned message templates;
- per-code allowlists for `details` keys and value types;
- no raw exception strings;
- no arbitrary caller-provided diagnostic messages;
- no paths/credentials/query/source text in details unless the design explicitly allows that field for that diagnostic (none of the Phase 2 cases here authorize path/credential exposure).

A tool error is never represented by a success-schema object carrying an embedded `error` field.

## 6. Protocol error vs tool error separation

Phase 2 conformance distinguishes:

- malformed JSON-RPC / unknown MCP method / invalid MCP request shape → protocol-owned JSON-RPC error;
- unknown tool name or invalid `tools/call` protocol shape → protocol-owned route according to the supported MCP revision;
- known well-formed Phase 2 tool semantic/domain failure → `isError: true` tool result;
- malformed/non-canonical resource URI → protocol JSON-RPC `-32602` on both supported protocol paths;
- canonical unknown resource → revision-specific resource-miss protocol route from `docs/design.md`, never a tool error or empty success;
- page source-integrity failure → both-revision JSON-RPC `-32603` safe resource error, no contents.

Tests assert each condition has exactly one surface.

## 7. Dual-revision tool conformance

The complete Phase 2 tool suite runs under both supported design protocol paths:

- per-request `2026-07-28` path;
- initialized-session `2025-11-25` path.

For every Phase 2 tool and each revision test:

- advertised input schema is strict and descriptive;
- success validates against the advertised success-output schema;
- success has `structuredContent`;
- legacy text parses to the exact same public object;
- error has `isError: true`;
- error has no `structuredContent`;
- error text parses to the strict shared error object;
- no third representation shape appears.

Revision-specific metadata such as result type/cache hints is emitted only where the design assigns it; common success/error semantics do not drift.

## 8. Canonical resource URI generation

Phase 2 resource templates use RFC 6570 simple-string expansion over already normalized semantic values.

For every variable segment:

1. encode the semantic string as UTF-8;
2. leave only RFC 3986 unreserved bytes literal;
3. percent-encode every other byte;
4. use uppercase hexadecimal digits in each percent escape.

A canonical resource emitted by ClauseSift is therefore unique at the byte level for the normalized semantic value.

The runtime never constructs filesystem paths by concatenating a client resource URI segment.

## 9. Canonical resource URI parsing

For a client-supplied Phase 2 resource read, the router:

1. validates the exact route shape/scheme/segment count;
2. decodes each variable segment **exactly once** using strict UTF-8;
3. rejects malformed `%` escapes;
4. rejects invalid UTF-8;
5. re-encodes the decoded semantic segment using the canonical RFC 6570/RFC 3986 rule above;
6. requires the re-encoded bytes to be byte-identical to the client-supplied segment;
7. only after the canonicality check applies field normalization/schema rules;
8. only then performs parameterized catalog lookup.

No catalog lookup occurs for a malformed/non-canonical URI.

## 10. Resource-URI negative fixtures

The Phase 2 suite covers at minimum:

- literal/encoded `/`;
- `%`;
- `?`;
- `#`;
- spaces;
- non-ASCII UTF-8;
- lower-case percent escapes;
- malformed/incomplete escapes;
- invalid UTF-8 byte sequences;
- overlong/invalid route shapes;
- a literal identifier that itself looks like percent-encoded text, proving there is no double decoding;
- canonical value round-trip generation → parse → re-encode equality.

Every malformed or non-canonical route returns JSON-RPC `-32602` on both supported protocol paths with no `contents` and no catalog lookup.

## 11. Phase 2 resource catalogue capabilities

The Phase 2 resource catalogue is immutable for one server process.

Advertised resources are read-only. Phase 2 does not advertise:

- resource subscription;
- list-change notification;
- mutation.

The resource templates/static resource are exactly those listed in Section 1 of this appendix. Unimplemented Phase 4 resource templates must not be listed as a Phase 2 capability.

## 12. Resource success cardinality

Every successful Phase 2 `resources/read` result contains **exactly one** content item.

That content item:

- has `uri` exactly byte-for-byte equal to the canonical requested URI;
- has the exact MIME type assigned below;
- has content bytes/text exactly as assigned below.

No Phase 2 handler returns:

- empty `contents` on success;
- two or more content items;
- a canonical URI different from the requested URI;
- a filesystem path in `uri`;
- a wrapper object around content whose bytes are specified directly by the contract.

## 13. `standards://document/{document_id}` exact success

MCP kind: read-only resource template.

Success content item:

- kind: `TextResourceContents`;
- `mimeType: application/json`;
- `uri`: exact canonical requested URI;
- `text`: UTF-8 RFC 8785 serialization of **the same safe `{release, document}` success object produced by `get_document_metadata`** for the exact document.

The tool success object, after RFC 8785 canonicalization, and the resource `text` bytes must be byte-identical.

Tests compare:

1. call `get_document_metadata(document_id)`;
2. validate its tool success object;
3. RFC 8785 serialize that public object;
4. read canonical document resource;
5. assert exactly one item, exact URI/MIME, and byte equality.

## 14. `standards://release/current` exact success

MCP kind: read-only static resource.

The process snapshots the verified active release at startup; the resource does not change during that process lifetime.

Success content item:

- kind: `TextResourceContents`;
- `mimeType: application/json`;
- `uri: standards://release/current`;
- `text`: UTF-8 RFC 8785 serialization of the strict safe immutable release summary and complete manifest digest required by `docs/design.md`.

The safe release summary contains only public release metadata; it excludes source/workspace paths, credentials, operator lifecycle secrets, and mutable runtime telemetry.

Tests assert canonical byte stability for one process snapshot and checksum/manifest identity agreement.

## 15. `standards://page/{document_id}/{page_number}` exact success

MCP kind: read-only resource template.

Success content item:

- kind: `BlobResourceContents`;
- `mimeType: application/pdf`;
- `uri`: exact canonical requested URI;
- `blob`: base64 encoding of the **complete bounded and handle-verified original PDF bytes**.

Decoding `blob` must reproduce the exact verified source bytes. `get_page_reference.content_hash` equals SHA-256 of those decoded PDF bytes (`documents.source_file_hash`), not a rendered-page hash.

The requested page number is navigation metadata selecting the page URI; Phase 2 does not pretend the returned complete PDF is a rendered single-page derivative.

All frame/working-set/integrity rules from the Phase 2 MCP protocol/admission appendices apply before success is committed.

## 16. Unknown canonical resource routes

A well-formed canonical Phase 2 resource URI that does not resolve never returns an empty success.

Use the design's revision-specific protocol errors:

- `2026-07-28` per-request path: JSON-RPC `-32602` for canonical unknown `standards://` resource;
- `2025-11-25` session path: JSON-RPC `-32002`.

No tool `resource_not_found` object is substituted for these resource protocol routes.

## 17. Page source-integrity failure

For a known canonical page URI, failure of the handle-bound containment/identity/stability/size/hash check returns:

- JSON-RPC `-32603` on both supported protocol paths;
- code-owned message `Source integrity check failed`;
- safe data exactly limited by the design, including:

```json
{
  "code": "source_hash_mismatch",
  "phase": "runtime",
  "severity": "blocking"
}
```

It returns:

- no `contents`;
- no partial base64;
- no path;
- no raw exception text.

Cancellation that already won the request terminal state keeps its no-response outcome instead of emitting this late error.

## 18. Central serializer and public allowlists

All Phase 2 tool/resource public objects pass through one central serializer layer.

For each result type it has an explicit public field allowlist. Unknown internal fields cause fail-closed serialization rather than accidental exposure.

Security tests inject sentinels representing:

- absolute path;
- workspace root;
- credential;
- raw exception text;
- arbitrary internal diagnostic message;
- extra unknown property.

The sentinel must not appear in:

- tool `structuredContent`;
- tool legacy text;
- tool error text;
- document/release resource JSON;
- page-resource error data;
- configured logs where the design forbids it.

## 19. Cross-surface equality tests

Phase 2 must prove equality relationships where the design intentionally exposes the same logical data through different MCP surfaces.

Required fixtures include:

- `get_document_metadata` public object == parsed legacy text;
- RFC 8785 `get_document_metadata` object bytes == document resource `text` bytes;
- `list_documents.items[*]` uses the same safe document summary projection/version;
- `get_page_reference.page_uri` == canonical URI read by the page resource;
- `get_page_reference.content_hash` == SHA-256 of decoded page-resource PDF blob;
- `standards://release/current` digest == active verified release manifest digest.

No equality fixture is implemented by duplicating independently maintained formatters; all project from shared typed public objects.

## 20. Protocol, input, output, and admission inheritance

This wire contract composes with, and does not duplicate/relax, the other Phase 2 MCP appendices:

- exact 1,048,576-byte inbound complete-frame limit;
- exact 65,536-byte RFC 8785 canonical arguments budget;
- exact 1,048,576-byte non-page complete-output limit;
- exact 33,554,432-byte page complete-output limit;
- 67,108,864-byte process page working-set budget;
- `max_in_flight_requests` in 1..1024;
- atomic terminal state for success/error/cancel/deadline;
- cancellation no-response semantics;
- protocol control liveness under saturation;
- redaction and stdout framing rules.

A correct semantic success that violates a framing/admission bound is not emitted as an oversized/partial success.

## 21. Tests

### 21.1 Tool advertisement/wire tests

For each of the three Phase 2 tools and both revisions:

- descriptions non-empty;
- all input-property descriptions non-empty;
- `additionalProperties: false` where required;
- read-only annotations accurate;
- valid success matches advertised schema;
- `structuredContent` exists;
- one legacy text block parses to exactly equal object;
- representative domain errors set `isError: true` and omit `structuredContent`;
- error text matches strict error schema.

### 21.2 URI tests

For document and page templates:

- canonical generation;
- canonical parse/re-encode;
- malformed escape;
- lower-case escape;
- invalid UTF-8;
- reserved characters;
- literal percent-looking identifier;
- no double decoding;
- no catalog lookup before canonicality success.

### 21.3 Resource success tests

- document: exactly one JSON text item, exact URI/MIME, bytes equal canonical metadata tool object;
- release: exactly one JSON text item, exact URI/MIME, canonical safe summary + manifest digest;
- page: exactly one PDF blob item, exact URI/MIME, decoded bytes equal verified original source;
- no empty or multi-item success.

### 21.4 Error-route tests

- malformed URI: both revisions `-32602`, no contents/catalog work;
- canonical unknown resource: revision-specific `-32602`/`-32002`;
- page integrity failure: both revisions `-32603`, exact safe message/data, no contents;
- cancellation-first suppresses later resource success/error;
- saturation routes remain protocol admission errors rather than malformed tool errors.

## 22. Acceptance criteria

Phase 2 MCP wire/resource work is not complete unless:

1. every advertised tool has exact description/input/output/read-only metadata;
2. every tool success uses validated `structuredContent` plus exactly equivalent JSON legacy text;
3. every tool execution error uses `isError: true`, no `structuredContent`, and the strict shared error JSON text;
4. both supported MCP revision paths pass success/error conformance for every Phase 2 tool;
5. advertised resource variables use canonical RFC 6570/RFC 3986 uppercase percent encoding;
6. resource parsing decodes exactly once, strict-UTF8 re-encodes, and rejects non-canonical bytes before catalog lookup;
7. malformed/non-canonical resources use both-revision `-32602`;
8. each resource success contains exactly one content item with exact requested URI;
9. document resource bytes equal RFC 8785 metadata-tool object bytes;
10. release resource is canonical safe release summary + manifest digest;
11. page resource decodes to exact verified original PDF bytes with matching tool content hash;
12. canonical misses and source-integrity failures use the exact protocol routes and never empty/partial contents;
13. central serializers/allowlists prevent path, credential, exception, and unknown-field leakage.

These requirements remain strictly Phase 2 because they complete the wire behavior of MCP surfaces Phase 2 itself advertises, while final evidence-oriented tools/resources remain deferred to Phase 4.
