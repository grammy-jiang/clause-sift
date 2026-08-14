# Phase 4 Performance Reporting Clarification

**Phase:** 4 — High-Accuracy Retrieval  
**Status:** Normative Phase 4 clarification  
**Authority:** `docs/design.md` Section 30

This clarification closes the final Phase 4 performance-review finding. It does not change phase ownership.

## Required per-stage measurements

The high-accuracy performance report must measure every executed stage separately rather than collapsing the complete pre-rerank path into one aggregate latency.

At minimum, record separate series for:

- exact lookup / exact candidate retrieval;
- lexical retrieval;
- dense retrieval;
- fusion and high-accuracy candidate assembly;
- cross-encoder reranking;
- context expansion, with required and supporting work separately visible when the implementation records them as distinct stages;
- total Python, CLI, or MCP tool latency.

For **every executed stage** and for total tool latency, report:

- p50;
- p95;
- p99;
- maximum;
- sample count;
- error rate;
- cancellation rate.

Segment every series by:

- tool or operation;
- concrete resolved retrieval mode;
- the Section 27 runtime load state.

Cold, warm, and model-free calls are separate series. Aggregate averages must not hide model-load latency, slow exact/fusion stages, tail latency, errors, or cancellation regressions.

Candidate-pool size, model bytes, RSS, and context-growth diagnostics may be reported in addition to these series, but never replace them.

## Conformance tests

Reject a Phase 4 performance report when:

- any executed stage is omitted;
- p50, p95, p99, maximum, sample count, error rate, or cancellation rate is missing;
- tool, resolved-mode, or load-state segmentation is collapsed;
- cold, warm, and model-free samples are pooled into one series;
- exact or fusion latency is hidden inside an undifferentiated pre-rerank measurement.

Quality gates remain blocking before performance optimisation.