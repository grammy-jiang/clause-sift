# Phase 2 MCP Protocol Conformance Appendix

**Project:** ClauseSift  
**Phase:** 2 — Exact Retrieval MVP  
**Status:** Normative Phase 2 implementation-plan appendix  
**Primary design authority:** `docs/design.md`  
**Companion plan:** `docs/implementation/phase-2-exact-retrieval-mvp.md`

## 1. Purpose and scope

Phase 2 advertises a deliberately limited MCP/runtime surface: metadata, document listing, page reference/resource, release metadata, and the common protocol/runtime foundation needed by later phases. Because those surfaces are already public MCP behavior, Phase 2 must satisfy the design's transport framing, input-argument bounds, output budgets, cancellation, deadline, and single-terminal-response rules now.

This appendix does **not** enable Phase 4 `search_evidence`, `get_clause`, `get_context`, clause-resource context closure, reranking, or Evidence Graph traversal. It applies the common protocol contract only to Phase 2-advertised requests and resources.

Where the companion plan says only “bounded input frame handling” or otherwise leaves these protocol details implicit, this appendix is authoritative.

## 2. Complete inbound JSON-RPC frame bound

The stdio decoder enforces the exact design limit:

- maximum complete inbound JSON-RPC frame: **1,048,576 bytes**.

The bound is checked at the framing/transport layer before parsing or allocation beyond the declared bound.

For an oversized complete frame the server:

1. drains the oversized frame to the transport boundary;
2. emits JSON-RPC `-32600` with a null ID according to the design's protocol-error route;
3. invokes no MCP request handler, runtime service, catalog lookup, source open, model loader, or application callback;
4. does not truncate and attempt to parse a prefix.

Exact-max and one-byte-over fixtures are required.

## 3. I-JSON and duplicate-key validation

After a bounded frame is decoded, request payload processing rejects before application work:

- duplicate JSON object keys;
- strings containing lone surrogate values rather than Unicode scalar values;
- non-finite numbers;
- integers outside the interoperable range `[-9007199254740991, 9007199254740991]`;
- malformed JSON/MCP request shapes through their protocol-owned routes.

A malformed or rejected value cannot be normalized into an accepted value after the fact.

## 4. Canonical aggregate argument budget

Every well-formed Phase 2 `tools/call` request uses the design's shared argument budget.

After strict input-schema validation, serialize the complete parsed `params.arguments` value with RFC 8785 JSON Canonicalization Scheme. The canonical UTF-8 byte sequence must be at most:

- **65,536 bytes**.

The server rejects a one-byte-over canonical argument payload before:

- normalization;
- cursor decoding beyond syntactic/authentication validation needed by the input contract;
- query planning;
- catalog access;
- source-file access;
- any later Phase 3/4 model loading.

For the Phase 2 tool-input surface, I-JSON/JCS rejection or aggregate-budget failure uses the design's typed `identifier_invalid` tool-result route rather than exception leakage, truncation, or partial processing.

The exact RFC 8785 bytes are the authoritative aggregate-boundary fixture; tests must not estimate the size from source JSON text.

## 5. Field bounds inherited by Phase 2 surfaces

Every Phase 2 input continues to enforce the applicable shared design bounds before and after field normalization, including:

- opaque `document_id`: 1–128 characters, pattern `^[a-z0-9][a-z0-9._:-]{0,127}$`;
- document code, edition, discipline, lifecycle status, document type, and other applicable normalized exact strings: 1–128 Unicode scalar values unless a stricter closed enum applies;
- cursor: 1–4,096 Unicode scalar values plus authenticated cursor syntax and release binding;
- result/page limit where applicable: integer 1–100;
- page number: integer 1–2,147,483,647 and no greater than the manifested page count;
- all integers must also satisfy the I-JSON interoperable integer range where that range is narrower or otherwise applicable.

The runtime never publishes a catalog lookup/filter/cursor value that its own public schemas reject. Registration, canonical/catalog validation, cursor generation, and release validation must prove that invariant.

## 6. Non-page outbound JSON-RPC frame budget

Every Phase 2 non-page response, including tool successes, tool errors, protocol responses, document/release text-resource results, and document-list pages, must fit the exact complete-frame design limit:

- maximum complete non-page JSON-RPC response frame: **1,048,576 bytes**.

The measurement includes the complete serialized JSON-RPC envelope, request ID echo, result/error syntax, structured/text content, and all other emitted bytes.

The central outbound serializer calculates the complete frame size before committing serialization/output. It must never:

- truncate an item array to make an oversized success look valid unless the public pagination contract selected that smaller page before result construction;
- emit a partial frame;
- allocate or stream an already-known over-budget success;
- silently omit fields from the strict output schema.

For catalog-derived success shapes, release validation must prove that every maximum valid Phase 2 success can fit the bound under its declared pagination/field limits. A release whose static/catalog-derived success cannot satisfy the advertised bound is blocked with the applicable release-validation failure; runtime must not discover this only after activation.

## 7. Page resource response budget

The Phase 2 `standards://page/{document_id}/{page_number}` resource uses the separate design budget:

- maximum complete page-resource JSON-RPC frame: **33,554,432 bytes**.

The complete-frame calculation includes:

- request ID echo;
- canonical resource URI;
- JSON syntax;
- base64 expansion of the complete verified original PDF bytes;
- all content/MIME wrapper bytes.

Registration/release validation computes the worst case for each admitted PDF using the recorded source size, `4 * ceil(size / 3)` base64 expansion, the longest canonical page URI for that document, and the worst-case serialized request ID permitted by the inbound-frame contract. A document whose worst-case response can exceed the page-resource bound fails release admission.

Runtime recomputes the exact complete-frame size before allocating/reading/encoding the source and never truncates a page resource.

Exact-at and one-byte-over release-admission tests are required.

## 8. Release-time bounded-success proof

Before activation, Phase 2 release validation must execute deterministic size proofs for every public Phase 2 success family, including at minimum:

- `get_document_metadata` maximum safe document projection;
- `list_documents` with the maximum configured page size and worst-case valid fields/cursor;
- `get_page_reference`;
- `standards://document/{document_id}`;
- `standards://release/current`;
- `standards://page/{document_id}/{page_number}` using its separate bound.

The proof records:

- output schema/version;
- maximum fixture/input identity;
- configured page/result limit;
- observed worst-case complete-frame bytes;
- applicable byte limit;
- pass/fail.

A catalog/source change that can increase a response beyond the admitted proof invalidates the relevant release artefact/validation result.

## 9. Boundary and no-application-work tests

Phase 2 tests must cover exact maximum and one-over behavior for every applicable bound and prove the application layer is not called after early rejection.

At minimum:

- inbound frame at 1,048,576 bytes accepted if otherwise valid;
- inbound frame at 1,048,577 bytes follows oversized-frame protocol route with no handler call;
- canonical argument bytes at 65,536 accepted if otherwise valid;
- canonical argument bytes at 65,537 produce `identifier_invalid` with no catalog/service call;
- cursor exact-max and one-over;
- ID/string exact-max and one-over, including multibyte Unicode for scalar-counted fields;
- page number exact limits and manifested-page one-over;
- non-page complete output exact-max and one-over validation;
- page-resource complete output exact-max and one-over release admission;
- no partial response for any over-budget output.

Use spies/barriers to assert that rejected inputs do not reach the runtime service, catalog, source open, or later optional model loader.

## 10. One atomic terminal state per admitted work request

Every admitted Phase 2 work request owns one atomic terminal state initialized to `pending`.

The terminal contenders are:

- successful completion;
- typed tool/application error or protocol-owned resource failure as applicable;
- honored cancellation;
- server-enforced deadline;
- any Phase 2 process-integrity/quarantine terminal event that the design routes through the same admitted-request race.

Each contender attempts exactly one compare-and-set transition from `pending` to its terminal state. The first successful transition is authoritative. Every later/losing completion is discarded **before serialization or frame commitment**.

Equal monotonic timestamps never require a wall-clock tie-breaker: compare-and-set ownership is the decision.

## 11. Cancellation semantics

When a valid MCP cancellation notification targets an in-progress Phase 2 request:

1. the server resolves the applicable request/session protocol revision;
2. cancellation races for the request's atomic terminal state;
3. when cancellation wins, active work stops promptly at documented cooperative cancellation points;
4. temporary resources, source handles, byte-budget reservations, catalog cursors, and other per-request resources are released;
5. the server records the non-response cancellation event/metric;
6. **no cancellation tool/resource response is emitted**;
7. any later success/error/deadline completion loses the terminal race and is discarded before serialization;
8. no duplicate or partial response is emitted.

Cancellation/control frames remain processable while request or response-byte admission budgets are saturated, consistent with the common MCP admission design.

## 12. Completion-first and cancellation-first races

Tests must deterministically exercise both race directions without wall-clock sleeps.

### Completion wins first

A barrier-controlled request completes and commits its terminal success/error transition before cancellation races. The normal one response may be emitted. Later cancellation observes a non-pending request and emits no second response.

### Cancellation wins first

Cancellation commits its terminal transition first. The work is stopped/released, and a later application completion is discarded before serialization. Zero tool/resource responses are emitted for that request after the cancellation win.

### Equal-time scheduling

Arrange cancellation and completion on controlled barriers so they may become runnable at the same logical instant. Assert exactly one terminal transition and no duplicate response regardless of scheduler ordering.

## 13. Deadline race

The Phase 2 runtime uses the same atomic terminal state for server-enforced request deadlines.

Tests deterministically cover:

- completion-first vs deadline;
- deadline-first vs completion;
- cancellation-first vs deadline;
- deadline-first vs cancellation;
- equal-time scheduling without wall-clock sleeps.

When deadline wins on a tool call, emit exactly the design's typed `request_deadline_exceeded` tool-error result and no partial/later result. When cancellation has already won, it retains its non-response outcome.

## 14. Page-resource cancellation and byte reservations

Page-resource reads are specifically included because they can hold source and response-byte resources.

A cancellable page read must not:

- continue reading/encoding after cancellation has authoritatively won except for bounded cleanup needed to release resources;
- leak source handles;
- retain source/response byte-budget reservations;
- emit a partial base64 resource;
- emit a late `-32603` or success after cancellation won.

Barrier tests cover cancellation before source open, during bounded read, before hash/encode, and before response commit.

## 15. Catalog/list cancellation

A long or deliberately blocked `list_documents`/metadata operation must honor cancellation through the same terminal-state mechanism.

Tests ensure:

- SQLite statements/cursors are released or interrupted safely;
- no next cursor is emitted from a canceled request;
- a cancellation win cannot later emit a successful page;
- a completed page cannot receive a duplicate cancellation result.

## 16. Dual-revision conformance

The Phase 2 protocol suite runs the applicable framing, resource, error, cancellation, and terminal-state cases against both supported MCP protocol paths described by the design:

- per-request `2026-07-28` behavior where applicable;
- initialized-session `2025-11-25` behavior where applicable.

Revision-specific wire differences remain those of `docs/design.md`; the single-terminal-state and no-duplicate-response invariants are common.

Phase 2 must not invent a third compatibility profile.

## 17. Logging and redaction during protocol failures

Oversized frames, malformed inputs, cancellation, deadlines, and response-budget failures must preserve the design's redaction rules:

- no credential values;
- no absolute/internal paths;
- no raw exception strings;
- no client-controlled JSON-RPC ID in configured sinks where the design forbids it;
- query/evidence content absent by default;
- no partial response body copied into an operator error record.

MCP stdout remains exclusively valid protocol frames.

## 18. Acceptance criteria

Phase 2 MCP/runtime protocol work is not complete unless:

1. inbound frames are capped at exactly 1,048,576 bytes before application work;
2. duplicate keys and non-I-JSON values are rejected through the declared routes;
3. canonical `params.arguments` bytes are capped at exactly 65,536 bytes before normalization/catalog work;
4. every non-page complete response is proven and enforced to fit 1,048,576 bytes;
5. every admitted page-resource response is proven and enforced to fit 33,554,432 bytes;
6. release validation proves every catalog-derived Phase 2 success family can fit its applicable bound;
7. exact-max/one-over fixtures exist for all applicable shared bounds;
8. every admitted work request has one atomic terminal state;
9. cancellation stops/reclaims work and emits no cancellation response when it wins;
10. losing success/error/deadline completions are discarded before serialization;
11. completion-first, cancellation-first, deadline-first, and equal-scheduling races are barrier-tested without wall-clock sleeps;
12. Phase 2 page and catalog requests are covered by cancellation/resource-release tests;
13. no late, partial, or duplicate MCP response can pass the conformance suite.

These requirements stay within Phase 2 because they govern the protocol correctness of MCP surfaces Phase 2 already advertises; they do not implement the Phase 4 evidence semantics layered on top later.
