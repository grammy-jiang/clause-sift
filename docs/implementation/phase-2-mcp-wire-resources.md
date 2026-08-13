# Phase 2 MCP Wire and Resource Contract

**Project:** ClauseSift  
**Phase:** 2 — Exact Retrieval MVP  
**Status:** Normative Phase 2 implementation-plan appendix  
**Primary design authority:** `docs/design.md` Sections 19-22 and 31  
**Current-design correction:** `docs/implementation/phase-2-current-design-correction.md`  
**Evidence service:** `docs/implementation/phase-2-evidence-service.md`  
**Protocol companions:** `phase-2-mcp-protocol-conformance.md`, `phase-2-mcp-admission-budgets.md`

## 1. Purpose and current Phase 2 surface

Current `docs/design.md` assigns the ordinary context-complete exact/lexical evidence path to Phase 2. Therefore Phase 2 advertises the basic MCP evidence tools/resources it can now satisfy completely.

The Phase 2 tool surface is:

- `search_evidence`;
- `get_clause`;
- `get_context`;
- `get_document_metadata`;
- `list_documents`;
- `get_page_reference`.

The Phase 2 resource surface includes the current design-defined read-only release/document/page templates plus the clause/source evidence resources defined by Section 22 when implemented in the same context-complete evidence service.

A Phase 2-only runtime does **not** claim Phase 3 dense/hybrid capability or Phase 4 reranker/supporting-context high-accuracy capability. An explicit unavailable later mode fails with `feature_unavailable` rather than silently degrading.

The MCP transport never exposes a context-incomplete direct-retrieval substitute for `search_evidence` or `get_clause`.

## 2. Tool advertisement contract

Every advertised tool declares:

- stable name;
- non-empty description;
- strict JSON Schema input;
- strict success-output schema;
- accurate read-only annotation;
- `additionalProperties: false` on closed objects;
- complete property descriptions including identifier domains, normalization, bounds, null/default semantics, filter combination, pagination, and mode/context-level behavior.

The tool/resource list is stable for one process lifetime. No resource subscription/list-change notification is advertised by v0.1.

## 3. Common request bounds

Apply the current Section 22 input rules before retrieval or expensive work.

At minimum:

- query: trimmed 1-4096 scalars and at most 16,384 encoded UTF-8 bytes;
- opaque `document_id`/`source_id`: 1-128 and `^[a-z0-9][a-z0-9._:-]{0,127}$`;
- clause/document-code/edition/jurisdiction/discipline/status/type/mode/context-level values: 1-128 plus applicable closed enums;
- filter arrays: at most 64 unique items each;
- `search_evidence`: at most 256 total filter values;
- result limit: 1-100;
- cursor: at most 4096 plus authenticated release binding;
- page number: positive 32-bit and not above manifested page count.

Validate applicable limits both before and after field normalization.

Invalid input is rejected before model loading, traversal, page allocation, or catalog work beyond what validation requires.

## 4. Common success wire representation

A successful tool call returns its strict public success object in `structuredContent`.

The same already validated object is serialized once to JSON for exactly one legacy text content block.

Parsed legacy text must equal `structuredContent` exactly.

Both representations use one central public serializer/allowlist and contain no absolute paths, workspace roots, credentials, raw exceptions, or unknown internal fields.

## 5. Common tool error branch

A well-formed call to a known tool that fails semantic/domain execution returns:

- `isError: true`;
- no `structuredContent`;
- exactly one JSON text content block containing the strict shared error object.

The strict error object is:

```text
{
  code,
  phase,
  severity,
  message,
  details?
}
```

Messages are code-owned; detail keys/types are per-code allowlisted. Raw exception strings, paths, credentials, query/source text, and arbitrary diagnostics are not emitted unless explicitly admitted by the design.

Protocol errors remain protocol JSON-RPC errors; tool domain errors are not disguised as success objects with an embedded `error` property.

## 6. `search_evidence`

### 6.1 Selection semantics

Validate the bounded query and exact filters.

Values are ORed within each filter list; filter categories are ANDed. `status: null` removes the default active-only filter.

Resolve `mode` only among installed + release-supported capabilities.

In Phase 2 the successful ordinary path uses exact/identifier and lexical direct seeds. Every seed then runs Phase 2 required graph-and-material-conflict closure.

Direct metadata filters constrain retrieval seeds, not required context/conflict attachments.

### 6.2 Success object

Return exactly:

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

`evidence` contains ordered direct, expanded-context, and conflict-context source-backed items using the Section 21 closed schema.

`context_targets` contains metadata-only accepted empty structural nodes.

`conflicts` contains every material admitted conflict record applicable to the returned evidence subgraph.

No match is a `complete` success with empty evidence/context-target/conflict arrays.

### 6.3 Domain errors

At minimum:

- malformed/over-limit query or filters -> `identifier_invalid`;
- explicit unsupported mode -> `feature_unavailable`;
- required graph/conflict closure overflow -> `context_limit_exceeded`;
- active/lazy release integrity failure -> `release_integrity_failed`.

No partial Evidence Package is emitted after a required closure overflow.

## 7. `get_clause`

### 7.1 Selection

Use exact opaque `document_id` plus normalized exact `clause_number`.

No fuzzy clause match, latest-edition substitution, or same-number cross-edition fallback is allowed.

Select the complete Section 14.1 exact-lookup source set as direct `retrieval_seed` items, then run required graph/conflict closure from every direct source.

### 7.2 Success

Return exactly the Section 22 clause success root:

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

For a found clause, `evidence` is non-empty. Direct and attached roles remain distinguishable in assembly lineage.

### 7.3 Errors

- malformed input -> `identifier_invalid`;
- unknown document/clause -> `resource_not_found`;
- required closure overflow -> `context_limit_exceeded`.

## 8. `get_context`

### 8.1 Selection

Use exact `source_id` and closed `context_level`:

- `required`;
- `supporting`;
- `diagnostic`.

Each level includes preceding levels. Relation-family booleans independently control explicit inspection families but never retroactively weaken required closure of another search/clause result.

### 8.2 Success

Return exactly the current root containing:

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

`context` always contains required arrays:

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

Disabled/not-found families are empty arrays rather than omitted fields.

Conflict closure preserves every material side reached through enabled families.

### 8.3 Errors

- malformed source/context-level input -> `identifier_invalid`;
- unknown source -> `resource_not_found`;
- required closure overflow -> `context_limit_exceeded`.

## 9. `get_document_metadata`

Selection: exact opaque `document_id`, with no latest/active substitution.

Success:

```text
{
  release,
  document
}
```

`document` is the safe exact manifest/catalog projection defined by the design and excludes internal source locators and inferred legal force.

Errors:

- malformed input -> `identifier_invalid`;
- unknown document -> `resource_not_found`.

## 10. `list_documents`

Selection uses exact normalized filters, stable current-design ordering, and authenticated release-bound keyset cursor.

Success:

```text
{
  release,
  items,
  next_cursor
}
```

Every item uses the same safe document summary projection; cursor is string or null.

Errors:

- malformed filter/limit/cursor -> `identifier_invalid`;
- valid cursor bound to another/unavailable release -> `resource_not_found`.

## 11. `get_page_reference`

Selection: exact `document_id` + one-based page within manifested page count.

Success:

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

`page_uri` is canonical authorized `standards://page/...`; `content_hash` is the verified source-document hash used by the page resource contract.

Errors:

- malformed/out-of-range -> `identifier_invalid`;
- unknown document/unavailable page -> `resource_not_found`.

## 12. Evidence success-schema invariants

For `search_evidence`, `get_clause`, and `get_context`, all source-backed items use the single Section 21 serializer from `phase-2-evidence-service.md`.

The MCP adapter must not:

- omit required context/conflict items to reduce payload;
- flatten metadata-only context targets into fabricated evidence;
- drop typed warnings;
- add ad-hoc classifier/traversal fields outside the closed schema;
- expose internal paths or SQL IDs;
- transform original source text into a generated summary.

If a valid complete success would violate an output/frame budget, route the design-defined typed/protocol failure rather than emitting partial/oversized content.

## 13. Dual-revision conformance

Run the complete Phase 2 tool suite under both supported protocol paths defined by the design:

- per-request `2026-07-28` path;
- initialized-session `2025-11-25` path.

For every advertised tool and revision prove:

- strict descriptive input schema;
- strict success schema;
- valid success `structuredContent`;
- legacy text exact-object equality;
- domain error `isError: true` with no structured content;
- one strict error JSON text representation;
- no revision-specific semantic drift.

Revision-specific metadata is emitted only where the detailed design assigns it.

## 14. Canonical resource URI generation

Resource templates use RFC 6570 simple-string expansion over normalized semantic values.

For every variable segment:

1. UTF-8 encode the semantic string;
2. leave only RFC 3986 unreserved bytes literal;
3. percent-encode all others;
4. use uppercase hex.

The runtime never concatenates client URI segments into filesystem paths.

## 15. Canonical resource URI parsing

For a client resource read:

1. validate exact scheme/route/segment count;
2. strict-decode each variable exactly once;
3. reject malformed `%` escapes and invalid UTF-8;
4. re-encode canonically;
5. require byte-for-byte equality with the supplied segment;
6. apply field normalization/schema rules;
7. only then perform parameterized catalog lookup.

No catalog lookup occurs after URI canonicality failure.

Negative fixtures cover encoded separators, `%`, `?`, `#`, spaces, non-ASCII, lower-case escapes, malformed escapes, invalid UTF-8, overlong routes, and percent-looking literal identifiers without double decoding.

## 16. Resource catalogue

The process advertises only resources it fully implements. The catalogue is immutable for the process lifetime.

Current categories include:

- document metadata resource;
- page resource;
- current release resource;
- clause evidence resource when defined by Section 22;
- source evidence resource when defined by Section 22.

Clause/source evidence resources must call/project the same context-complete Phase 2 evidence service; they cannot reintroduce the old direct-only semantics.

## 17. Resource success cardinality

Every successful `resources/read` contains exactly one content item with:

- URI byte-identical to canonical requested URI;
- exact assigned MIME type;
- exact assigned text/blob content.

Never return empty contents, multiple content items, a different URI, or a filesystem path on success.

## 18. Document resource

`standards://document/{document_id}` returns one JSON text resource.

Its text is RFC 8785 UTF-8 serialization of the same safe `{release, document}` public object produced by `get_document_metadata`.

Tests assert byte equality after canonicalizing the tool public object.

## 19. Release resource

`standards://release/current` snapshots the verified active release for process lifetime and returns one strict safe JSON summary/manifest digest.

Exclude source/workspace paths, credentials, mutable telemetry, and operator lifecycle secrets.

## 20. Page resource

`standards://page/{document_id}/{page_number}` returns one `application/pdf` blob resource according to the current design's complete verified source-PDF contract.

The requested page is navigation metadata; the content bytes are the design-defined verified PDF bytes, not a falsely labelled page derivative.

All handle-bound containment/identity/stability/size/hash checks, page working-set reservation, frame limits, and cancellation terminal-state rules apply before success is committed.

## 21. Clause/source evidence resources

Where Section 22 exposes clause/source resources, implement them as exact canonical projections of the shared evidence service.

### Clause resource

- canonical document ID + exact clause selector;
- same direct exact-lookup set and required graph/conflict closure as `get_clause`;
- strict context-complete evidence JSON;
- no fuzzy/edition substitution.

### Source resource

- exact source ID in the active release;
- source-backed item plus current-design context/evidence semantics defined for that resource;
- exact original text/citation/lineage;
- no hidden filesystem locator.

Resource/tool equality fixtures use one shared typed public object/serializer where the design defines the same logical representation.

## 22. Unknown canonical resources

A well-formed canonical resource that does not resolve never returns empty success.

Use the design's revision-specific protocol route (including `-32602`/`-32002` where assigned), not a tool-style `resource_not_found` object.

Malformed/non-canonical URIs return the appropriate invalid-params protocol error before catalog lookup.

## 23. Page source-integrity failure

For a known canonical page resource whose handle-bound verification fails:

- return the design's safe internal/protocol error route (`-32603` where specified);
- emit no contents or partial base64;
- expose no path/raw exception;
- preserve cancellation terminal-state precedence if cancellation already won.

## 24. Central serializer and allowlists

All tool/resource public objects pass one central serializer layer.

Each result type has an explicit field allowlist. Unknown internal fields fail closed.

Security tests inject sentinels for:

- absolute path;
- workspace root;
- credential;
- raw exception;
- arbitrary internal diagnostic;
- extra unknown property.

No sentinel may reach tool success/error, resource JSON/blob metadata, or logs where forbidden.

## 25. Cross-surface equality tests

Required equality relationships include:

- tool `structuredContent` == parsed legacy JSON for every tool;
- document metadata tool canonical bytes == document resource text;
- list items use the same safe document summary projection;
- page-reference URI == canonical page resource URI;
- page-reference content hash == verified source bytes hash returned by page resource contract;
- release resource digest == active verified release manifest digest;
- get-clause/associated clause resource use the same exact evidence service result where schemas are defined as equivalent;
- get-context/search/source-resource paths cannot disagree about the same source's immutable source/build lineage.

Do not implement equality by maintaining separate formatters.

## 26. Protocol/admission inheritance

This wire contract composes with existing Phase 2 MCP protocol/admission appendices without relaxing them, including:

- 1,048,576-byte inbound complete-frame limit;
- 65,536-byte RFC 8785 canonical argument budget;
- 1,048,576-byte non-page complete-output limit;
- 33,554,432-byte page complete-output limit;
- 67,108,864-byte process page working-set budget;
- `max_in_flight_requests` 1..1024;
- atomic success/error/cancel/deadline terminal state;
- cancellation no-response semantics;
- protocol-control liveness under saturation;
- stdout framing and redaction rules.

Required graph/conflict traversal must fit inside these same request/output/lifecycle contracts.

## 27. Conformance tests

### Tool tests

For all six tools under both revisions:

- advertisement and strict schemas;
- exact success/error branch shape;
- legacy/structured equality;
- boundary/one-over input tests;
- no unknown output properties;
- correct mode/capability behavior;
- no-match search success;
- required context/conflict closure;
- context-limit no-partial failure.

### Evidence semantics tests

- exact clause plus required context;
- lexical search plus applicability/exception/table context;
- confirmed/unresolved conflict all sides;
- empty context target;
- unresolved required warning/completeness;
- status boundary preservation;
- source/citation/lineage equality across Python/CLI/MCP.

### Resource tests

- canonical URI generation/parse;
- exactly one success content;
- tool/resource equality where defined;
- unknown canonical route errors;
- page integrity failure;
- cancellation and budget races;
- clause/source resource context completeness.

## 28. Acceptance criteria

Phase 2 MCP wire/resource implementation is complete only when:

1. all six current Phase 2 tools are advertised only when their complete current-design semantics are implemented;
2. ordinary search/clause/context success is context/conflict complete according to the shared evidence service;
3. explicit later unsupported capabilities fail visibly rather than silently degrading;
4. all tool success/error schemas are strict and dual-revision conformant;
5. legacy text and structured success are exactly equal;
6. resource URI handling is canonical and safe;
7. document/page/release plus current clause/source resources obey exact success/error contracts;
8. context/conflict evidence cannot be dropped for payload convenience;
9. public allowlists prevent path/credential/internal leakage;
10. protocol/admission/cancellation/frame budgets apply to the new evidence operations;
11. cross-interface/resource equality tests pass;
12. no Phase 3 dense/RRF or Phase 4 reranking/supporting-context behavior is pulled into this Phase 2 corrective scope.
