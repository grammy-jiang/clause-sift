# Phase 4 High-Accuracy Release-Gate Plan

**Project:** ClauseSift  
**Phase:** 4 — High-Accuracy Retrieval  
**Status:** Normative Phase 4 implementation-plan appendix  
**Primary design authority:** `docs/design.md` Sections 29-31  
**Companions:** `docs/implementation/phase-4-high-accuracy-retrieval.md`, `docs/implementation/phase-4-reranker-selection.md`, `docs/implementation/phase-4-supporting-context.md`, `docs/implementation/phase-4-warning-refusal-evaluation.md`

## 1. Purpose

Phase 4 cannot be activated because a reranker "looks better" on a few examples. The final high-accuracy candidate must pass the exact current design gates under leakage-safe decisive evidence while preserving every lower-phase deterministic correctness contract.

This appendix defines:

- frozen Phase 4 candidate identity;
- development/model-selection/decisive split separation;
- high-accuracy retrieval gates;
- optional supporting-context gates;
- warning/refusal-support gates;
- deterministic conformance/negative suites;
- regression, integrity, performance, cancellation, activation, and rollback gates;
- retry/retirement governance after decisive observation.

Where a metric/threshold is already defined by `docs/design.md`, that exact metric/threshold is authoritative; this plan must not silently substitute another value.

## 2. Frozen Phase 4 candidate identity

Before final decisive evaluation, freeze every behavior-bearing input that can change high-accuracy evidence.

At minimum bind:

- Phase 2 release/canonical graph/context/conflict/evidence-service identity;
- Phase 3 embedding model/assets/query preprocessing/dense backend/RRF/candidate-pool/classifier identity;
- exact-channel handling in high-accuracy candidate assembly;
- reranker model ID/revision;
- complete reranker tokenizer/processor/weight asset identity;
- safe loader ID/version;
- candidate-specific winning reranker pair-preprocessing schema/configuration;
- reranker input pool size;
- final direct-seed count;
- high-accuracy fusion/assembly configuration;
- deterministic rerank tie-break/version;
- high-accuracy routing/`auto` resolution configuration;
- supporting-context rule/configuration identity;
- optional-context ordering/bounds where behavior-bearing;
- warning/error/refusal-support rule configuration where separately versioned;
- relevant dependency-lock/toolchain identity;
- release/schema versions.

A behavior-bearing change creates a new Phase 4 candidate and invalidates stale decisive authorization for every affected gate family.

## 3. Data roles

Every Phase 4 evaluation case has a declared role:

- development diagnostics;
- reranker model/preprocessing selection;
- candidate-pool/routing/supporting-context selection;
- non-decisive screening if preregistered;
- final decisive confirmation;
- reproduction-only after decisive observation.

A decisive case cannot also be model/pool/rule tuning data.

Lower-phase held-out cases that have already been observed during Phase 2/3 development/release decisions are not magically fresh Phase 4 decisive evidence merely because Phase 4 reports a different metric.

## 4. Preregistration

Before final decisive data is observed, record:

- campaign ID;
- complete frozen candidate identity/hash;
- gate families;
- decisive split identity/version/hash;
- applicable strata;
- exact design metric/threshold/sample rules;
- reviewer/adjudication/calibration policy versions for semantic labels;
- any finite nondecisive screening sets in exact use order;
- predecessor campaign linkage if applicable.

The preregistration artifact is immutable for that campaign.

## 5. Final user-facing path gate

The blocking retrieval gates apply to the **actual final frozen Phase 4 high-accuracy path returned to users**, not to an easier lower-phase component run.

A passing Phase 3 hybrid path, dense-only path, lexical-only path, or reranker offline score cannot substitute for a failing high-accuracy production path.

The final high-accuracy path must satisfy the current design's expected-evidence retrieval gates, including the current Recall@20 and Top-5 Wilson lower-bound requirements and sample/stratification rules.

Report for each gate:

- numerator;
- denominator;
- point estimate;
- one-sided confidence lower bound;
- target;
- split/corpus/label/reviewer versions;
- frozen Phase 4 candidate identity;
- pass/fail.

## 6. Explicit high-accuracy gate

If the public explicit `high_accuracy` mode can produce a path different from the classifier/`auto`-selected path, it must independently satisfy every applicable blocking high-accuracy retrieval gate.

A good `auto` result cannot authorize a poor explicit high-accuracy path, and vice versa.

## 7. Critical lower-phase regression gates

Phase 4 cannot hide a critical regression behind an improved global high-accuracy average.

Retain lower-phase deterministic/regression coverage for:

- exact document/clause/model anchors;
- numbers/units;
- edition/status filters;
- wrong-edition hard negatives;
- negation/exceptions;
- required context completeness;
- material conflict all-side preservation;
- citation/page/source identity;
- Evidence Package closed-schema conformance;
- Phase 2 explicit Python/MCP `get_context` semantics;
- Phase 3 hybrid mode when selected explicitly;
- capability fallback warnings/errors.

Where a lower-phase mode remains publicly available, Phase 4 must not change its semantics merely by installing the reranker.

## 8. Reranker comparative gate

On independently labelled non-decisive/decisive slices as appropriate, report Phase 3 candidate ordering vs Phase 4 reranked ordering by critical stratum.

Reject a candidate that gains average ranking quality by introducing an unacceptable regression in:

- exact-anchor queries;
- wrong-edition/wrong-document hard negatives;
- numeric/unit questions;
- negation/exception questions;
- critical applicability-sensitive questions;
- conflict-sensitive questions.

Use the current design's primary release metrics as blockers; MRR/nDCG/rank-shift diagnostics are secondary unless explicitly promoted by the detailed design.

## 9. Optional-context precision gate

Automatic Phase 4 supporting-context expansion must pass the **exact current `docs/design.md` Section 29.4 optional-context precision gate**, including its metric definition, one-sided Wilson confidence target, minimum applicable sample size, and stratification expansion rules.

Do not replace this with required-context recall or an invented global attachment metric.

Report by relation/context family so false supporting expansions cannot hide in a global aggregate.

This gate applies to automatic high-accuracy supporting context; Phase 2 required context retains its deterministic zero-failure conformance gate.

## 10. Supporting-context deterministic gates

Require zero failures across complete versioned deterministic suites for:

- required fixed point always completed before supporting traversal;
- only validated supporting edges followed;
- no diagnostic context automatically added;
- accepted optional source retains its required context/conflict consequences;
- optional truncation stops before the first over-bound optional candidate;
- required evidence/conflict sides never removed by optional truncation;
- exact source/edition/status identity preserved;
- supporting path/order/provenance matches the closed schema;
- wrong-edition/unresolved/guessed reference traversal prohibited;
- informative/supporting material not promoted to normative authority.

## 11. Warning/refusal-support gates

Use the exact current design gates for high-accuracy warning/insufficiency/refusal-support behavior.

Where behavior is deterministic, require zero conformance failures for the complete versioned suite.

Where the design defines probabilistic semantic warning/refusal-support metrics, use the exact metric, Wilson target, sample count, stratification, and reviewer reliability requirements.

At minimum decisive/conformance coverage includes:

- no evidence -> `evidence_insufficient`;
- `auto` capability fallback -> `retrieval_capability_unavailable`;
- explicit high-accuracy unavailable -> `feature_unavailable`;
- applicability incomplete;
- required context incomplete/error routes;
- optional context truncated;
- confirmed/unresolved conflict;
- status/version boundary;
- parser/OCR/classification/source-coordinate uncertainty;
- multiple simultaneous warnings;
- high reranker score on wrong/inapplicable source never suppresses warning state.

## 12. Conflict/citation/context inherited blockers

The final high-accuracy package must still pass the lower-phase deterministic blockers for:

- exact citations/document/edition/clause/page;
- required traversal/path/source-status/order;
- prohibited guessed/wrong-edition traversal;
- conflict position/source/lineage completeness and all-side preservation;
- trusted precedence only;
- strict source/build/assembly lineage;
- strict Evidence Package serialization.

A reranker does not lower these requirements.

## 13. Model/release integrity gates

Before activation prove:

- complete reranker asset table/digest;
- exact safe model format/loader compatibility;
- every loader-opened asset size/hash recheck;
- reranker preprocessing/model/release compatibility;
- supported candidate/routing/supporting schema versions;
- query-independent release lineage/configuration binding;
- no missing/extra behavior artifact;
- lazy integrity failure follows quarantine/failure contract.

Any mismatch blocks activation.

## 14. Determinism/reproducibility gates

For identical supported release/runtime/request/configuration inputs, require stable:

- candidate assembly;
- reranker pair bytes/tokenization behavior under the declared deterministic contract;
- reranker output/order under the admitted execution contract;
- total final seed ordering;
- required/supporting context ordering/truncation;
- warning/conflict serialization;
- release validation decision.

If a model/backend cannot satisfy the design's admitted reproducibility/determinism requirements, it is not an eligible implementation simply because its average score is better.

## 15. Protocol/admission/cancellation gates

Run Phase 4 under the existing runtime/MCP constraints:

- strict input/output schemas;
- inbound/argument/output/page budgets;
- request admission limits;
- model-load/rerank/context cancellation/deadline races;
- atomic terminal state;
- no late success after cancel/deadline;
- control-plane liveness during model work;
- stdout framing/redaction;
- no path/credential/raw-exception leak.

High-accuracy work receives no resource-limit exemption.

## 16. Performance gates and reports

Measure performance after quality gates pass.

Report at minimum:

- warm Phase 3 candidate retrieval;
- cold reranker load;
- warm rerank latency by pool size;
- required fixed-point latency;
- supporting traversal latency;
- end-to-end cold/warm high-accuracy latency;
- peak/incremental RSS;
- model asset size;
- output-size/context-growth distribution;
- cancellation/deadline behavior.

If the design defines hard performance targets, enforce the exact current target. Otherwise performance remains a measured decision criterion and cannot override a blocking accuracy/safety gate.

## 17. Decisive-evidence retirement

A final decisive split can authorize one frozen Phase 4 candidate campaign while unseen.

After decisive observation:

- exact same candidate replay is reproduction-only;
- changed reranker/model assets/preprocessing/pools/routing/supporting/warning behavior cannot claim fresh authorization from the observed split;
- a final-confirmation failure closes the campaign for that candidate;
- remediation uses development/model-selection/review data;
- a later candidate requires a fresh preregistered campaign with genuinely fresh decisive evidence;
- do not inspect several unseen reserves and choose the most favorable result.

## 18. Human-review reliability

For semantic relevance/supporting-context/warning/refusal labels, preserve the current blinded reviewer/adjudication/calibration/reliability rules from the detailed design.

An LLM may assist analysis but cannot be the sole release-gate label authority.

A failed reviewer-reliability gate leaves affected semantic product metrics non-passing/exploratory according to current design.

## 19. Release-gate ledger

Persist a deterministic audit record containing:

- campaign/candidate identity;
- split identity/role;
- reviewer/adjudication/calibration identity;
- gate family/stratum;
- numerator/denominator;
- point estimate/lower bound/target where applicable;
- deterministic suite size/failures for count gates;
- pass/fail;
- decisive observation/retirement state;
- raw result/report hashes;
- predecessor/successor campaign linkage.

Release validation rejects missing, contradictory, stale, reused, or insufficient gate evidence.

## 20. Failure injection

Inject and prove non-activation/correct runtime routing for:

- final high-accuracy Recall/Top-K gate failure;
- optional-context precision failure;
- warning/refusal-support gate failure;
- exact/wrong-edition hard-negative regression;
- missing required conflict side;
- reranker asset corruption;
- unsupported loader/model config;
- non-finite/mismatched rerank output;
- optional context admitted partially across overflow;
- required overflow misreported as optional truncation;
- model-load/rerank cancellation/deadline race;
- held-out leakage/reuse;
- insufficient sample/reviewer reliability;
- missing/corrupt gate report;
- activation/rollback mismatch.

Every candidate release failure preserves the previous active release.

## 21. Corrected execution order

1. complete implementation/conformance of high-accuracy path;
2. complete reranker model/preprocessing selection on non-decisive data;
3. complete pool/routing/supporting-context tuning on non-decisive data;
4. freeze complete Phase 4 candidate identity;
5. run deterministic lower-phase/high-accuracy conformance and negative suites;
6. validate decisive split/reviewer/campaign identities;
7. run final high-accuracy retrieval gates;
8. run optional-context precision gate;
9. run applicable warning/refusal-support gates;
10. run protocol/security/cancellation/integrity gates;
11. persist raw/gate reports;
12. enforce every blocker;
13. assemble/checksum/reopen the immutable candidate release;
14. run independent startup/cold/warm smoke validation;
15. validate rollback;
16. activate atomically only after all preceding gates pass.

## 22. Acceptance criteria

Phase 4 release gating is complete only when:

1. final user-facing high-accuracy path passes every applicable current design retrieval gate;
2. explicit high-accuracy mode independently passes when its path differs;
3. critical lower-phase strata do not regress unacceptably;
4. automatic supporting context passes the exact current optional-context precision gate plus deterministic conformance/negative suites;
5. warning/insufficiency/refusal-support behavior passes every current applicable gate;
6. citations/required context/conflicts/lineage/closed schemas remain fully conformant;
7. reranker asset/configuration integrity and deterministic runtime behavior pass;
8. protocol/admission/cancellation/security gates pass;
9. performance is measured/enforced according to current design only after quality;
10. decisive evidence is preregistered, leakage-safe, finite, and retired after observation;
11. failed/missing/insufficient evidence prevents activation and preserves the previous release;
12. the final release/gate ledger makes the Phase 4 decision reproducible and auditable.
