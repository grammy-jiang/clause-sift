# Phase 4 Cold-Load Progress Notification Clarification

**Phase:** 4 — High-Accuracy Retrieval  
**Status:** Normative Phase 4 clarification  
**Authority:** `docs/design.md` Section 27

Phase 4 high-accuracy calls inherit the runtime lazy-model lifecycle contract. A cold MCP request that triggers lazy loading of the query-embedding model and/or cross-encoder reranker must support the design's progress-notification behavior.

## Progress-token gating

When the MCP caller supplied a valid progress token for the request:

- lazy model loading emits protocol-conformant progress notifications associated with that exact client-supplied token so the client can distinguish model loading from a stalled call;
- the notification describes load progress only and does not expose model paths, credentials, source text, query text, internal exceptions, or release-private state;
- progress reporting does not create another response channel and does not change the eventual tool success/error schema.

When the caller supplied **no progress token**, the server emits **no progress notification** for that request. It must not invent a token or send uncorrelated progress.

## Lifecycle precedence

Progress notifications do not extend or reset:

- the caller's overall tool-call deadline;
- the shared model-load attempt deadline;
- single-flight/load-queue ordering;
- cancellation semantics;
- the atomic Section 22 terminal-state winner;
- quarantine/integrity behavior.

Once cancellation, deadline, quarantine, success, or another error has won the request's terminal transition, no progress behavior may revive the request or cause an additional terminal result. A caller detached from a shared load attempt receives no request-specific progress after its terminal outcome.

## Required tests

Add deterministic integration coverage for:

- cold `high_accuracy` with a progress token and a lazy reranker load -> progress is observable under the supplied token before the terminal result;
- cold `high_accuracy` with no progress token -> zero progress notifications;
- a high-accuracy call that lazily needs both query embedding and reranker assets -> every emitted progress event remains bound to the same request token;
- warm and model-free calls do not fabricate cold-load progress;
- cancellation/deadline while loading prevents any late terminal response and prevents request-specific progress after the terminal winner;
- progress payloads pass the same redaction/non-leakage rules as other runtime diagnostics.

These tests use controllable loaders/barriers rather than wall-clock sleeps.
