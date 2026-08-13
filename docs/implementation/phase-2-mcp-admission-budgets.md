# Phase 2 MCP Admission Budgets Appendix

**Project:** ClauseSift  
**Phase:** 2 — Exact Retrieval MVP  
**Status:** Normative Phase 2 implementation-plan appendix  
**Primary design authority:** `docs/design.md`  
**Companion protocol plan:** `docs/implementation/phase-2-mcp-protocol-conformance.md`

## 1. Purpose and scope

This appendix completes the bounded-admission contract for MCP surfaces already advertised by Phase 2. It defines the exact process-wide page-response working-set budget and bounded work-request admission required by `docs/design.md` Section 27.

It does **not** add Phase 3 models or Phase 4 evidence semantics. It governs only admission, memory budgeting, saturation behavior, and control-frame liveness for Phase 2 requests.

Where the companion MCP protocol appendix refers generically to request/response-byte admission budgets, this appendix is authoritative and supplies the exact values, reservation formulas, wire routes, and tests.

## 2. Process-wide page-response working-set budget

Phase 2 uses the design's fixed v0.1 page-resource working-set budget:

- **67,108,864 bytes** process-wide.

This budget is separate from:

- the 1,048,576-byte inbound frame limit;
- the 1,048,576-byte non-page outbound frame limit;
- the 33,554,432-byte per-page-resource complete-frame limit;
- the request-count admission limit below.

The budget exists to bound concurrent memory consumption by source bytes plus their serialized page-resource responses.

## 3. Exact page-read reservation formula

Before opening a source file, allocating a source buffer, allocating a base64 value, or allocating an outbound page-resource frame, the page handler computes the exact reservation:

```text
catalog_source_size + 1 + exact_serialized_response_size
```

where:

- `catalog_source_size` is the checksum-verified release/catalog source byte size;
- `+ 1` is the bounded oversize probe required by the source-integrity read contract;
- `exact_serialized_response_size` is the complete JSON-RPC page-resource frame size for the specific request, including request ID echo, canonical URI, JSON syntax, MIME/content wrapper, and base64 output.

The reservation is atomic against the shared 67,108,864-byte process budget.

No source open, source buffer, oversize probe, base64 value, or response frame allocation occurs before reservation succeeds.

## 4. Page-response budget saturation route

If the release-time single-response bound is inconsistent with catalog metadata, the request follows the design's source-integrity failure route rather than treating corrupted release metadata as transient load.

If the individual response is valid but the **process working-set budget is temporarily exhausted** by other admitted page reads, the request is rejected before source open with JSON-RPC server error:

- code: `-32000` on both supported protocol paths;
- code-owned message: `Server busy`;
- safe data:

```json
{
  "code": "feature_unavailable",
  "phase": "runtime",
  "severity": "blocking",
  "reason": "response_byte_budget"
}
```

This is a protocol-level admission result, not a tool execution error and not an empty resource success.

The request never waits in an unbounded memory queue for budget to become available.

## 5. Reservation lifetime and release

A successful page-response reservation remains owned by exactly one admitted request and is released on **every** terminal path, including:

- successful complete response;
- source-integrity failure;
- cancellation win;
- deadline win;
- protocol/resource error after admission;
- process quarantine or other applicable terminal failure.

Terminal-state compare-and-set ownership and budget ownership are coordinated so a losing completion cannot double-release or retain a reservation.

Tests assert the process budget returns exactly to its pre-request value after every terminal outcome.

## 6. Concurrent page boundary tests

Phase 2 must use deterministic concurrency/barrier fixtures to prove:

- one reservation exactly equal to the available process budget is admitted;
- the first reservation that would make the total exceed 67,108,864 bytes is rejected with `-32000` / `response_byte_budget`;
- concurrent reservations can never make the committed total exceed 67,108,864 bytes;
- rejection happens before source open and allocation;
- cancellation of an admitted page read releases its reservation before a later request can consume the freed capacity;
- completion releases its reservation exactly once;
- deadline/error paths release exactly once;
- blocked/slow clients do not cause a second hidden response allocation outside the reserved amount;
- source-size + oversize-probe + exact-frame accounting is used rather than a rough estimate.

## 7. Normal work-request admission limit

Normal Phase 2 work admission is atomic with respect to process release state and uses the schema-validated runtime configuration:

```text
max_in_flight_requests: integer in 1..1024
```

The configured value is validated before the server begins serving requests. Zero, negative, non-integer, and values above 1024 are rejected as invalid runtime configuration.

The admitted-work counter/set includes every Phase 2 work request that has passed protocol-shape validation and successfully acquired normal admission but has not yet reached/released its terminal state according to the design's admission accounting.

## 8. No unbounded decoded work queue

The transport decoder remains able to process framing and protocol control traffic under saturation, but it must **not** place complete work requests into an unbounded decoded queue.

A complete work request encountered while `max_in_flight_requests` is full is rejected immediately at admission. It does not acquire an application request terminal state, does not enter the runtime service, and does not wait behind admitted work.

This preserves bounded memory and prevents ordinary work from starving cancellation/control traffic.

## 9. Request-count saturation route

A work request encountered while the admitted set is full receives the exact both-revision admission error:

- JSON-RPC code: `-32000`;
- message: `Server busy`;
- safe data:

```json
{
  "code": "feature_unavailable",
  "phase": "runtime",
  "severity": "blocking",
  "reason": "max_in_flight"
}
```

After this admission failure:

- no catalog lookup executes;
- no source opens;
- no response working-set reservation executes;
- no later Phase 3/4 model loader executes;
- no application handler runs;
- no work-request terminal state is created that could later race a second response.

## 10. Control-frame liveness under saturation

While either the request-count limit or page-response working-set budget is saturated, the transport remains live for protocol control frames, including cancellation notifications.

Tests must prove that:

- cancellation for an already admitted request is decoded/processed while the work-admission count is full;
- cancellation for an admitted page read is processed while the page-response byte budget is full;
- protocol control frames do not need to acquire normal work admission;
- saturation does not build an unbounded decoded control queue;
- freeing admission or byte budget after cancellation permits a later work request to be admitted according to normal ordering, without replaying a request that was already rejected.

## 11. Interaction between request and byte budgets

Page reads must satisfy both admission gates:

1. normal work admission under `max_in_flight_requests`;
2. exact page-response working-set reservation under 67,108,864 bytes.

The implementation uses a deterministic declared acquisition order and releases any earlier-acquired resource when a later admission step fails. It must never deadlock by acquiring these gates in inconsistent order across handlers.

A page request rejected because normal request admission is already full uses reason `max_in_flight`. A page request that passes normal work admission but cannot reserve its response working set uses reason `response_byte_budget`; that budget rejection wins the admitted request's terminal/admission result according to the design's routing and releases the normal admission slot before returning to steady state.

No source open occurs after either rejection.

## 12. Saturation tests for metadata/list requests

Phase 2 tests use controllable barriers to hold exactly `max_in_flight_requests` metadata/list/page requests pending, then submit one additional valid work request.

Assert:

- first N requests are admitted for configured N;
- N+1 receives `-32000` / `max_in_flight` immediately;
- application-service call count remains N;
- cancellation/control frames remain processable;
- after one admitted request terminates and releases its slot, a later new request can be admitted;
- the previously rejected N+1 request is not queued/replayed automatically;
- exact boundaries for configuration values 1 and 1024 are covered without allocating an unbounded fixture queue.

## 13. Saturation tests for page working set

Use synthetic manifested source sizes and exact serialized response-size fixtures so the budget can be exercised without storing huge real PDFs in the repository.

Assert:

- reservation math exactly includes `source_size + 1 + response_size`;
- exact-total 67,108,864-byte reservations can be admitted;
- one-byte-over aggregate total is rejected;
- two or more concurrent individually valid page requests cannot exceed the shared total;
- `response_byte_budget` is returned before any source open/response allocation;
- cancellation/deadline/success/error release reservations exactly once;
- response reservations are independent of release-file memory maps and unrelated SQLite page cache accounting.

## 14. Metrics and diagnostics

Admission metrics may record bounded operational values such as:

- configured `max_in_flight_requests`;
- current/peak admitted request count;
- configured page-response working-set bytes;
- current/peak reserved response bytes;
- saturation reason counts (`max_in_flight`, `response_byte_budget`).

Diagnostics remain subject to redaction rules and must not include source paths, source text, credentials, or client-controlled JSON-RPC IDs where forbidden by the design.

## 15. Acceptance criteria

Phase 2 MCP admission is not complete unless:

1. `max_in_flight_requests` is schema validated in the exact range 1..1024;
2. normal work admission is atomic and no unbounded decoded work queue exists;
3. request-count saturation returns the exact both-revision `-32000` / `max_in_flight` error before application work;
4. the page-response process working-set budget is exactly 67,108,864 bytes;
5. each page read atomically reserves exactly `catalog_source_size + 1 + exact_serialized_response_size` before source open/allocation;
6. temporary page-budget exhaustion returns the exact both-revision `-32000` / `response_byte_budget` route;
7. reservations are released exactly once on every terminal path;
8. concurrent reservations can never exceed the process budget;
9. cancellation/control frames remain processable under both saturation types;
10. deterministic exact-boundary and concurrent saturation tests prove all of the above without wall-clock sleeps.

These requirements stay strictly within Phase 2 because they bound the public MCP server behavior that Phase 2 already advertises.
