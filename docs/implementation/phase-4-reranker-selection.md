# Phase 4 Reranker Selection and Runtime Plan

**Project:** ClauseSift  
**Phase:** 4 — High-Accuracy Retrieval  
**Status:** Normative Phase 4 implementation-plan appendix  
**Primary design authority:** `docs/design.md` Sections 17-18, 25-27, 29-31  
**Companion:** `docs/implementation/phase-4-high-accuracy-retrieval.md`

## 1. Purpose

Phase 4 introduces the first query-time cross-encoder reranker. The model is an implementation component, not source authority.

The goal is to improve ordering of the already source-grounded exact/lexical/dense candidate pool on realistic engineering questions while preserving exact anchors, edition safety, deterministic evidence identity, release integrity, and the Phase 2 evidence pipeline.

No reranker is chosen by reputation or generic benchmark score alone.

## 2. Reranker interface

Define a replaceable narrow interface that accepts typed canonical rerank candidates and returns one score per candidate without exposing backend-native model objects.

The implementation identity includes at minimum:

- provider/implementation ID/version;
- model ID;
- exact revision;
- tokenizer/processor identity;
- input pair schema/version;
- model-specific query/candidate preprocessing identity;
- maximum token/input lengths;
- truncation policy;
- score semantics/version;
- safe loader ID/version;
- complete local asset identity;
- dependency/configuration hash.

The interface cannot mutate source/candidate identity or emit generated source facts.

## 3. Candidate-specific preprocessing

Different cross-encoders may require different prefixes, separators, role markers, pair order, or max-length behavior.

Before benchmarking each model candidate, freeze that candidate's complete deterministic preprocessing projection.

A projection may use only approved deterministic candidate inputs such as:

- normalized query bytes from the Phase 3 query-preprocessing contract;
- source/chunk search representation admitted by the design;
- deterministic heading/clause/document-code context;
- deterministic table title/header/unit context already present in the canonical representation.

It must not include:

- hidden generated answers;
- another edition's text;
- mutable paths/timestamps;
- reviewer comments;
- LLM query rewriting;
- inferred applicability/precedence.

Selection chooses a **model + preprocessing projection** pair. The winner's projection is reused unchanged in pool tuning, final confirmation, and production.

A later behavior-bearing preprocessing change creates a new candidate and invalidates old decisive evidence.

## 4. Benchmark candidate set

Benchmark a small replaceable shortlist that can run safely in the supported local runtime.

Candidate feasibility must consider:

- English technical text;
- Chinese technical text where the selected model claims support;
- cross-language engineering queries where applicable;
- long technical clauses/tables;
- local CPU/runtime feasibility;
- model asset size;
- cold load time;
- warm pair-scoring throughput;
- safe non-executable model format availability;
- packaging/license/governance constraints.

A candidate lacking safe reproducible local assets is not eligible merely because its ranking quality is strong.

## 5. Benchmark corpus strata

Use ClauseSift project cases, including:

- natural-language HVAC/fire-safety questions;
- cross-document questions;
- applicability-sensitive questions;
- exception/negation cases;
- numbers/units;
- exact document/clause/model anchors inside natural-language queries;
- same wording in different editions;
- near-duplicate wrong-document clauses;
- table rows with similar values but different units/scope;
- resolved cross-reference questions;
- manufacturer vs standard terminology;
- material-conflict cases;
- no-answer/evidence-insufficient cases;
- cases where Phase 3 hybrid order is already correct;
- cases where reranking is expected to improve Top-K placement.

Report results by stratum, not only globally.

## 6. Benchmark protocol

For every candidate model+preprocessing pair:

1. freeze complete model/provider/assets/preprocessing identity;
2. use identical frozen lower-phase release and candidate-generation configuration;
3. generate the same rerank candidate pools;
4. score candidates deterministically;
5. apply the same total tie-break contract;
6. measure expected-evidence Recall/Top-K and secondary ranking diagnostics;
7. measure wrong-edition/wrong-document hard-negative displacement;
8. measure exact-anchor survival;
9. measure per-stratum changes relative to Phase 3 hybrid ordering;
10. measure warm pair-scoring latency/throughput by pool size;
11. measure cold model load;
12. measure peak/incremental RSS;
13. measure asset/package size;
14. retain failed/rejected candidate results.

Never tune one model using another model's final-confirmation data.

## 7. Candidate-pool benchmark

After selecting the model+preprocessing pair using non-decisive data, benchmark a bounded set of high-accuracy pool configurations.

Include configurations around the design's starting guidance:

- lower-phase lexical/dense candidate ranges;
- reranker input pool around 20-30;
- final direct seed count around 8-12;
- exact-channel handling;
- high-accuracy fusion/assembly identity.

Do not assume the initial numbers are optimal. Choose the smallest/fastest configuration only among candidates that preserve the required quality/hard-negative gates.

## 8. Exact anchors and hard constraints

The reranker may change rank but cannot override authoritative exact constraints.

Tests must prove:

- an exact selected document/edition filter is never substituted;
- exact clause/product/model anchors survive candidate assembly/reranking according to the frozen routing contract;
- wrong-edition identical text remains distinct and cannot be silently promoted as the requested edition;
- exact numeric/unit constraints are not erased by semantic similarity;
- reranker score is never treated as applicability, normative status, or precedence.

## 9. Deterministic scoring

Validate every inference result:

- output count equals candidate count;
- candidate identity remains one-to-one;
- all scores are finite;
- candidate ordering into the model is deterministic;
- batch partitioning cannot alter final output;
- total output order has a frozen tie-break ending in canonical source identity.

If the backend cannot satisfy the project's deterministic/reproducibility contract under supported execution, it is not an eligible Phase 4 implementation.

## 10. Safe local asset binding

The active release/configuration binds the complete ordered asset set that the reranker loader may open.

Record at minimum:

- stable release-relative safe asset name;
- asset role;
- format;
- exact byte size;
- SHA-256;
- model/revision;
- tokenizer/processor assets;
- loader name/version;
- aggregate ordered asset digest;
- model/preprocessing configuration hash.

No loader-opened local file may be omitted from the exhaustive binding.

Admit only safe non-executable formats/loaders allowed by current design. Pickle-backed arbitrary-code model formats remain prohibited unless the design is explicitly revised.

## 11. Runtime lazy loading

Reuse the common supervised model lifecycle.

Required behavior:

- validate release capability before claiming high-accuracy availability;
- recheck all loader assets before deserialization;
- single-flight concurrent load;
- per-attempt load deadline;
- per-caller overall deadline;
- cancellation/worker cleanup through common terminal-state code;
- ready handle published only after successful load;
- lazy integrity mismatch follows release quarantine/failure policy;
- no stdout logging outside MCP framing.

Do not create a reranker-specific cancellation/timeout subsystem.

## 12. Capability semantics

A release/runtime is high-accuracy-capable only when every required lower-phase retrieval component plus the exact admitted reranker capability is available and compatible.

Explicit `high_accuracy` cannot silently degrade to hybrid/exact.

If an explicit request cannot execute the required high-accuracy model/capability, return the current `feature_unavailable` route.

If `auto` cannot use high accuracy because a required capability is unavailable and resolves lower, include `retrieval_capability_unavailable`.

## 13. Release/cache identity

Phase 4 behavior identity includes reranker model/revision/assets, preprocessing pair schema/configuration, loader identity, input pool/final seed configuration, exact-channel handling, tie-break version, routing changes, dependency lock/toolchain identity, and every other behavior-bearing high-accuracy input.

A change creates a new Phase 4 candidate and invalidates stale final-gate evidence.

Model assets/configuration are release-bound even when the model is loaded lazily at runtime.

## 14. Rerank assembly provenance

Use only the existing closed Section 21 `rerank` object and lower-phase retrieval/fusion records.

Record the exact admitted:

- model ID/revision;
- rerank configuration hash;
- artifact-set hash;
- final rerank rank;
- finite rerank score.

Do not add model explanation strings, token attributions, hidden chain-of-thought, or arbitrary new score arrays to the public schema.

## 15. Failure behavior

Explicit failures include:

- missing/unsupported reranker capability;
- corrupt/missing model asset;
- model-load deadline;
- cancellation;
- non-finite score;
- output count/identity mismatch;
- unsupported preprocessing/schema;
- release/model configuration mismatch;
- integrity/quarantine failure.

No failure may produce a response labelled `high_accuracy` after silently bypassing the reranker.

## 16. Test plan

### Unit

- preprocessing serialization;
- asset-table/digest identity;
- safe-loader allowlist;
- candidate input mapping;
- score validation;
- deterministic total ordering;
- exact-anchor preservation;
- candidate identity mismatch rejection;
- candidate/cache/release invalidation.

### Integration

- cold load then rerank;
- warm rerank;
- concurrent single-flight load;
- explicit high_accuracy success;
- explicit unavailable failure;
- auto typed fallback;
- model asset corruption/quarantine;
- exact/wrong-edition hard negative;
- rollback to release without Phase 4 capability.

### Boundary/failure

- zero/one/max candidate pool;
- configured pool one over bound;
- max-length pair truncation;
- NaN/Inf scores;
- missing/extra output score;
- duplicate source candidate;
- load timeout/cancellation race;
- request deadline during rerank;
- unsafe model format;
- asset hash/size mismatch.

## 17. Selection record

Persist a versioned decision artifact with:

- all model/preprocessing candidates;
- exact versions/assets/configurations;
- benchmark corpus/split versions;
- per-stratum metrics;
- hard-negative results;
- latency/memory/asset size;
- selected pair and rationale;
- rejected candidates and reasons;
- selected candidate-pool/final-seed configuration;
- final frozen Phase 4 candidate identity.

The record is audit evidence, not source evidence.

## 18. Acceptance criteria

Reranker work is complete only when:

1. candidate-specific preprocessing is frozen before benchmark;
2. one model+preprocessing pair is selected on project-specific non-decisive evidence;
3. exact anchors/edition constraints survive reranking;
4. scores/order are deterministic and finite;
5. complete safe local assets/loader identity are release-bound;
6. lazy load/cancellation/deadline/quarantine semantics reuse common runtime contracts;
7. candidate-pool/final-seed values are evaluation-backed, not latency guesses;
8. explicit/auto capability behavior is typed and non-silent;
9. closed rerank provenance schema is used exactly;
10. behavior-bearing changes invalidate stale candidate/evidence identity;
11. all Phase 4 rerank quality/security/performance gates pass;
12. no reranker output becomes source, applicability, conflict, or precedence authority.
