# Phase 4 Warning, Insufficiency, and Refusal-Support Evaluation Plan

**Project:** ClauseSift  
**Phase:** 4 — High-Accuracy Retrieval  
**Status:** Normative Phase 4 implementation-plan appendix  
**Primary design authority:** `docs/design.md` Sections 21-22, 29, and 31  
**Companion:** `docs/implementation/phase-4-high-accuracy-retrieval.md`

## 1. Purpose

ClauseSift returns source-grounded structured evidence, not a generated engineering answer. Phase 4 therefore does not add a prose answer/refusal generator.

Its warning/refusal work has a narrower and more important purpose: prove that the high-accuracy evidence path emits the exact typed evidence state, warnings, and errors required for a downstream AI/client to **refuse or qualify an answer when evidence is insufficient, incomplete, conflicting, truncated, or unavailable**.

Phase 4 expands evaluation coverage of these conditions after reranking and automatic supporting-context expansion are introduced.

## 2. Authority boundary

Warnings and errors describe the state of evidence/retrieval/runtime execution. They do not become source facts.

Phase 4 must not:

- generate a legal/engineering conclusion from a warning code;
- hide original source evidence behind a generated explanation;
- let a reranker decide applicability/conflict/precedence;
- convert model confidence into evidence confidence;
- create free-form refusal text as a new public authority unless a future design explicitly defines such a schema.

The existing Evidence Package and typed error/warning schemas remain authoritative.

## 3. High-accuracy warning preservation

Every lower-phase warning that applies to a returned item/result remains present after high-accuracy reranking/supporting expansion.

High-accuracy mode cannot suppress a warning because:

- the reranker score is high;
- a better-ranked source exists;
- optional context was truncated;
- a similar active edition exists;
- a model appears confident.

Warnings remain deterministically tied to source/build/assembly/evidence state.

## 4. Capability warning/error cases

### 4.1 Explicit high-accuracy unavailable

An explicit `mode="high_accuracy"` request that cannot execute the required active-release/runtime capability fails with the current `feature_unavailable` route.

It must not return hybrid/exact content labelled high accuracy.

### 4.2 `auto` fallback

When `auto` would use high accuracy but dense/reranker capability is unavailable and a lower supported path is selected, the successful response includes `retrieval_capability_unavailable` under the current design.

Silent fallback is invalid.

### 4.3 Lazy integrity failure

A model asset/hash/loader integrity failure follows the current release-integrity/quarantine contract. It cannot be converted into a generic no-evidence warning or silent lower mode when the explicit requested mode cannot be satisfied.

## 5. Evidence-insufficient cases

A valid search with no adequate direct evidence remains a source-faithful success/error state according to the current design and includes `evidence_insufficient` where specified.

Phase 4 adds no reranker trick that turns an empty/insufficient candidate set into plausible evidence.

Evaluation includes:

- truly no relevant source;
- only wrong-edition near duplicates;
- only topically similar but inapplicable material;
- query outside corpus scope;
- filters eliminating all applicable direct seeds;
- high-accuracy reranker unable to create relevance from no valid candidate.

## 6. Applicability-incomplete cases

Where the source is relevant but applicability remains incomplete under the current manifest/graph/classification rules, preserve `applicability_incomplete` and any related current completeness/warning state.

The reranker/supporting traversal cannot infer project-specific applicability from similarity, source authority, stricter wording, or model score.

Evaluation should include:

- missing project/equipment class applicability;
- known requirement with unresolved applicability edge/metadata;
- manufacturer/standard provisions whose shared applicability is not known;
- jurisdiction scope incomplete or unknown;
- exception condition incomplete.

## 7. Required-context incomplete cases

Phase 2 owns required-context correctness. Phase 4 must prove its high-accuracy path does not suppress or obscure lower-phase failures/warnings, including:

- unresolved required cross-reference;
- required table structure anomaly;
- unresolved classification needed by a required rule;
- required context bound overflow;
- required conflict side unable to fit.

A required bound overflow remains `context_limit_exceeded`, not `truncated_optional`.

## 8. Optional-context truncation cases

`context_truncated` is valid only after complete required graph/conflict closure and only when supporting/diagnostic optional traversal stops before an over-bound optional candidate.

High-accuracy evaluation proves:

- required evidence remains complete;
- rejected optional candidate is not partially returned;
- no later lower-priority optional candidate appears after truncation;
- completeness is `truncated_optional`;
- safe configured/observed details match current allowlists;
- clients can distinguish optional truncation from required incompleteness.

## 9. Conflict warning cases

High-accuracy ranking never erases material conflicts.

Evaluate:

- `evidence_conflict` for confirmed material disagreement;
- `conflict_unresolved` for admitted unresolved conflict;
- complete all-side preservation after reranking;
- conflict induced by an accepted supporting source;
- encoded precedence only through approved rule;
- no winner selection from rerank/rank/source authority/recency.

A high reranker score for one side cannot downgrade the conflict warning.

## 10. Version/status boundary cases

When high-accuracy retrieval/supporting traversal returns superseded/withdrawn/historical context under current rules, preserve exact status/edition identity and applicable status-boundary warnings.

Do not silently substitute an active edition or omit a boundary warning merely to make the package look simpler.

## 11. Parser/OCR/classification/source-coordinate warnings

High-accuracy mode retains item/result diagnostics for:

- parser comparison differences;
- OCR use/low confidence under current policy;
- unresolved classification;
- source coordinate incompleteness;
- table structure anomaly;
- unresolved optional reference when the current requested relation semantics call for it.

Reranking cannot reinterpret these as model confidence.

## 12. Deterministic answerability/refusal-support matrix

Build a reviewed evaluation matrix mapping evidence situations to the **existing** expected ClauseSift output behavior.

Each case records:

- expected success vs typed tool/protocol error;
- expected `context_completeness`;
- expected evidence/context/conflict cardinality constraints;
- required warning codes;
- prohibited warning codes;
- whether a downstream client should treat the package as insufficient/incomplete/conflicting for a confident answer under the current client guidance;
- exact source/edition/context expectations.

The matrix is evaluation metadata, not a new public answerability field unless the detailed design defines one.

## 13. Evaluation categories

Include at least:

1. sufficient evidence, no material warning;
2. no evidence -> `evidence_insufficient`;
3. auto capability fallback -> `retrieval_capability_unavailable`;
4. explicit high-accuracy unavailable -> `feature_unavailable`;
5. applicability incomplete;
6. required cross-reference unresolved;
7. required table structure incomplete;
8. optional supporting context truncated;
9. confirmed conflict;
10. unresolved conflict;
11. historical/status boundary;
12. parser/OCR/classification/source-coordinate uncertainty;
13. no-answer query with tempting semantic hard negatives;
14. high reranker score on an inapplicable/wrong-edition source;
15. multiple simultaneous warnings where none may be dropped.

## 14. Warning correctness metrics

Use the exact warning/refusal-support gates defined by current detailed design for the applicable Phase 4 families.

Where the design defines deterministic warning behavior, require zero conformance failures across the complete versioned suite.

Where the design defines independently labelled probabilistic precision/recall behavior, use its exact metric, Wilson confidence target, minimum sample size, and stratification rules rather than inventing alternate thresholds.

Every metric report includes numerator, denominator, point estimate/confidence bound where applicable, target, case category, corpus/split/reviewer identity, and frozen Phase 4 candidate identity.

## 15. False-positive warning negatives

Prove zero prohibited behavior in deterministic negative fixtures where current design requires exact warnings/errors, including:

- `evidence_insufficient` emitted despite adequate expected evidence;
- `applicability_incomplete` omitted when required facts are incomplete;
- `context_truncated` used for required overflow;
- capability warning omitted on auto fallback;
- capability warning emitted when full requested capability executed normally;
- conflict warning omitted because one side reranked lower;
- conflict warning emitted for an explained difference where ordinary output should not present unexplained conflict;
- high-accuracy unavailable silently degraded;
- raw exception/model-loader path leaked in details.

## 16. Multi-warning ordering and deduplication

Freeze current warning ordering/deduplication semantics from the central serializer.

Tests include results where:

- one item has source-coordinate + OCR warning;
- result has applicability incomplete + conflict;
- auto fallback coexists with evidence insufficient;
- optional truncation coexists with advisory source diagnostics;
- the same warning condition is reached by multiple context paths.

Do not deduplicate distinct source-bound warnings merely because codes match.

## 17. Cross-interface equality

For overlapping high-accuracy-capable public surfaces, prove the same underlying request/resolved mode returns the same evidence semantics and warning set through the shared service.

Adapters may format human-readable CLI text differently, but machine-readable output cannot suppress warning/error/completeness information.

MCP legacy text and `structuredContent` remain exact object equivalents.

## 18. Logging and privacy

Warning/refusal evaluation must not introduce unsafe logs.

Do not write unrestricted:

- full query/source text;
- credentials;
- absolute source/model paths;
- raw exception strings;
- private model-loader diagnostics.

Public warning detail keys remain per-code allowlisted.

## 19. Failure-injection tests

Inject:

- missing reranker assets;
- lazy asset hash mismatch;
- model-load timeout;
- cancellation/deadline race;
- no candidates;
- wrong-edition only candidates;
- unresolved required relationship;
- optional bound overflow;
- required bound overflow;
- conflict side dropped by a buggy candidate reducer;
- warning serialization extra property;
- adapter intentionally dropping one warning;
- raw exception/path sentinel.

Every case must route to the exact current success/warning/error contract.

## 20. Held-out governance

Do not tune warning/refusal thresholds/rules against final decisive cases.

Freeze all behavior-bearing inputs—including reranker/routing/supporting-context configuration and warning-rule configuration—before decisive evaluation.

Observed decisive semantic labels become evidence history under the project's leakage/retry governance. Deterministic conformance fixtures remain versioned executable contracts whose expected outputs change only through reviewed design/source/label corrections.

## 21. Suggested implementation sequence

1. enumerate current warning/error/completeness contracts used by high accuracy;
2. build the reviewed answerability/refusal-support evaluation matrix;
3. add high-accuracy capability warning/error tests;
4. add no-evidence/applicability/context/conflict/status/uncertainty fixtures;
5. integrate rerank/supporting stages without changing warning authority;
6. add multi-warning ordering/deduplication tests;
7. add cross-interface equality tests;
8. add security/redaction failure injection;
9. freeze all behavior-bearing high-accuracy warning/routing configuration;
10. run deterministic suites;
11. run any current design-defined probabilistic warning/refusal-support gates on decisive data;
12. include final results in the Phase 4 decision/release report.

## 22. Acceptance criteria

Phase 4 warning/refusal-support work is complete only when:

1. high-accuracy reranking never suppresses lower-phase evidence warnings;
2. explicit unavailable vs auto fallback routes are exact and non-silent;
3. no-evidence cases preserve `evidence_insufficient` and cannot be "rescued" by semantic similarity;
4. incomplete applicability/required context remains visible;
5. optional truncation is distinguishable from required incompleteness;
6. conflict/status/parser/OCR/classification/source-coordinate warnings remain correct;
7. no reranker score becomes evidence confidence/authority;
8. all deterministic warning/error/refusal-support conformance and negative suites pass;
9. every applicable current design probabilistic gate passes under correct sample/reviewer/leakage rules;
10. overlapping interfaces preserve warning/completeness/error semantics;
11. public/logging detail remains safe and allowlisted;
12. no generated answer/refusal prose becomes a new source of authority.
