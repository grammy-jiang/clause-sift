# Phase 2 Held-Out Retry Policy

**Project:** ClauseSift  
**Phase:** 2 — Exact Retrieval MVP  
**Status:** Normative Phase 2 implementation-plan appendix  
**Primary design authority:** `docs/design.md` Sections 29.3-29.4  
**Upstream split policy:** `docs/implementation/phase-0-evaluation-corpus.md`  
**Companion gate plan:** `docs/implementation/phase-2-release-gates.md`

## 1. Purpose

This appendix defines leakage-safe retry, split retirement, reproduction, and fresh-evidence rules for the Phase 2 **probabilistic independently labelled release gates**.

Current Phase 2 probabilistic gate families are:

1. retrieval Recall@20;
2. retrieval Top-5 evidence presence;
3. `node_type` accuracy;
4. `normative_status` accuracy;
5. `source_modality` accuracy;
6. conflict-candidate recall;
7. confirmed/unresolved conflict precision for each applicable state family;
8. explained-difference precision for each applicable explanation-code family.

This policy does **not** convert deterministic zero-failure conformance suites into hidden held-out probabilistic gates. Exact lookup, citation, required traversal, traversal negatives, vocabulary/schema, deterministic conflict completeness/all-side preservation, precedence negatives, Evidence Package conformance, and protocol conformance are complete versioned executable suites governed by reviewed version/change control.

It also does not govern Phase 3 embedding/RRF or Phase 4 supporting-context/reranker gates.

## 2. Core rule

A decisive independently labelled split may reveal whether one frozen candidate passes. Once its decisive labels/results have been exposed, it is evidence history, not a fresh optimizer for a behavior-bearing changed candidate.

Observation includes:

- per-case labels;
- raw outputs paired with labels;
- per-case failure identities;
- aggregate results sufficient to identify/tune failure strata;
- adjudicated semantic conflict/classification labels.

## 3. Split roles

Every case has exactly one declared role for one campaign:

- `development`;
- `benchmark_selection`;
- `screening_nondecisional` where preregistered;
- `final_confirmation`;
- `reproduction_only` after decisive observation.

A final-confirmation item cannot also be candidate-selection data.

Phase 0 calibration cases remain excluded from product metrics and follow their separate blinded-review reliability purpose.

## 4. Gate-specific frozen candidate identity

A candidate identity includes every behavior-bearing input that can change the applicable probabilistic metric.

### 4.1 Retrieval candidate

Bind at minimum:

- approved corpus/catalog/chunk identity;
- lexical engine/version;
- tokenizer/version;
- query normalization/compiler configuration;
- field weights;
- lexical index schema/artifact identity;
- metadata filter behavior that affects evaluated seed presence.

### 4.2 Classification candidate

Bind at minimum:

- evidence vocabulary version/hash;
- classification schema;
- deterministic rule/configuration;
- inheritance configuration;
- ordered immutable reviewed classification artifacts;
- canonical inputs on which classification operates.

### 4.3 Conflict candidate-recall candidate

Bind every behavior-bearing input that can change which conflict candidates are proposed, including:

- conflict identity schema;
- deterministic detector IDs/versions/configuration;
- comparison-key/projection configuration;
- unit/normalization registry identity;
- source/catalog/classification/context inputs consumed by detector eligibility;
- admitted human candidate-input artifacts where applicable.

### 4.4 Conflict precision candidate

For confirmed/unresolved and explained-difference precision also bind:

- conflict/context rule-set versions/configuration;
- required-context projection behavior;
- deterministic explanation/confirmation rules;
- immutable human decision/review-policy artifacts;
- applicability/relationship artifacts used by classification;
- precedence-rule identity where relevant;
- final conflict serialization state/code mapping.

A change to any behavior-bearing field creates a new candidate for every affected probabilistic gate family.

## 5. Preregistration

Before decisive observation record:

- campaign ID;
- exact frozen candidate identity/hash;
- gate family/families;
- decisive split identity/version/hash;
- applicable state/code/stratum families;
- required sample-size rule (150 for 98% gates, 60 for 95% gates, plus stratification expansion);
- reviewer/adjudication policy/version where semantic labels are involved;
- calibration/reliability evidence required by Section 29.3;
- any finite nondecisional screening split identities/order;
- corpus/canonical-ID migration versions.

The preregistration artifact is immutable for that campaign.

## 6. One decisive use while unseen

A final-confirmation split can authorize a release decision only on its first decisive use while unseen for the frozen candidate/campaign.

After decisive scoring it becomes `observed_retired` for fresh authorization of a behavior-bearing changed candidate, whether the result passed or failed.

It remains available for audit/reproduction/regression history.

## 7. Identical-candidate replay

The exact same candidate may rerun the exact same observed split only as `reproduction_only`.

Such a replay:

- cannot produce a second independent pass;
- cannot reset/erase a failure;
- cannot authorize a changed candidate;
- must link to the original decisive event;
- must reproduce the original deterministic raw outputs/metric result where the contract claims determinism, or expose a reproducibility failure.

No post-failure random-seed/environment/retry search is permitted unless a finite repeated-sampling procedure was preregistered before first observation and is explicitly allowed by the design.

## 8. Changed candidate after decisive observation

A behavior-bearing changed candidate cannot use the observed split for fresh authorization.

After a failure:

1. activation remains blocked;
2. retain the result permanently;
3. remediation returns to development/benchmark/review evidence;
4. freeze a new candidate without consulting labels of a fresh decisive split;
5. create the next valid fresh campaign/evidence allocation;
6. preregister candidate + split before observation.

An observed held-out result may inform failure history, but it cannot be repeatedly optimized until the same cases pass while still being called held out.

## 9. Finite campaigns; no stop-on-pass reserve search

Phase 2 must not create an unbounded sequence of decisive reserve splits until one passes.

A campaign has one final decisive confirmation event per jointly exposed decisive split family unless a different **finite** joint statistical test was preregistered before observation.

Failure closes the campaign for that candidate.

Any screening reserves are explicitly nondecisional and cannot authorize release.

A changed candidate after final failure requires a fresh campaign and genuinely fresh decisive evidence.

## 10. Fresh later campaign

Fresh decisive evidence must satisfy the same Phase 0/Section 29.3 ground-truth rules as the original gate data, including:

- independently sourced/labelled applicable cases;
- required blinded reviewers/adjudication;
- calibration/reliability rules;
- no forbidden overlap with development/benchmark/observed decisive cases;
- required sample counts and stratification;
- versioned split/label identities;
- reviewed canonical-ID migration before scoring where applicable;
- preregistration before exposure.

A paraphrase/punctuation change or duplicate of the same underlying source/evidence situation does not automatically become fresh independent evidence.

## 11. Joint exposure and retirement

A split can support several metrics. Retirement is tracked by exposed case/label information, not hidden by renaming a metric.

Examples:

- the same retrieval expected-evidence label may support Recall@20 and Top-5;
- one semantic conflict label may support candidate recall and a state/code precision family;
- one classification case may carry labels for several fields.

The preregistered campaign defines joint exposure/retirement before scoring.

An exposed label cannot be treated as unseen for a different changed candidate merely because the reported metric name changes.

## 12. Deterministic conformance suites are different

The design's zero-failure criteria for exact lookup, citations, required traversal, conflict all-side preservation, precedence negatives, and other deterministic contracts are **complete versioned conformance suites**, not statistical held-out population estimates.

For those suites:

- every fixture/expected output is version-controlled and reviewable;
- implementation changes are rerun against the complete suite as normal regression/conformance work;
- expected results may change only through documented design/source/label corrections, not to accommodate a failing implementation;
- report suite size and every failure;
- no claim of statistical independence is made.

Do not apply the probabilistic split-retirement mechanism mechanically to these executable contract tests.

## 13. Human-review reliability

For semantic classification/conflict gate labels preserve Section 29.3 exactly.

The release-gate workflow must retain:

- blinded independent labels;
- raw agreement before adjudication;
- required kappa or degenerate-case fallback;
- calibration-set result;
- third-reviewer adjudication;
- category counts and coefficient computability;
- final labels and score provenance.

If the reliability gate fails, the affected semantic product metric remains non-passing/exploratory until the rubric/sample is corrected under versioned review.

An LLM may assist analysis but cannot be sole release-gate authority.

## 14. Release-gate ledger

Every decisive probabilistic run records:

- campaign ID;
- candidate identity;
- gate family/state/code family;
- split identity/version/hash;
- split role;
- canonical-ID migration artifact where applicable;
- review/adjudication/calibration identity;
- raw-result hash;
- successes/failures/applicable count;
- point estimate;
- one-sided Wilson lower bound;
- target;
- pass/fail;
- unseen-at-decision flag;
- resulting split state;
- predecessor/successor campaign linkage.

Release validation rejects a purported decisive result when:

- evaluated behavior does not match candidate identity;
- split/labels were already observed by another changed candidate;
- split is reproduction-only/nondecisional;
- campaign/reserve order violates preregistration;
- overlap/leakage is detected;
- sample/stratum requirements are unmet;
- reviewer/reliability/canonical-ID migration evidence is missing;
- a failed campaign is reused for another decisive attempt.

## 15. Tests

Test at minimum:

- first frozen candidate + unseen split -> decisive run allowed;
- identical candidate + observed split -> reproduction-only;
- changed lexical candidate + same observed retrieval split -> rejected;
- changed classification rules + observed classification split -> rejected;
- changed conflict detector + observed candidate-recall split -> rejected;
- changed conflict explanation/classification rules + observed precision split -> rejected;
- fresh candidate + genuinely fresh reviewed split -> allowed;
- below-minimum 150/60 sample -> rejected;
- missing required conflict state/code stratum expansion -> rejected;
- failed reviewer-reliability gate -> release metric non-passing;
- cherry-picked/out-of-order reserve -> rejected;
- several unseen reserve results inspected before candidate selection -> rejected;
- identical-candidate replay mismatch -> reproducibility failure;
- failed decisive gate leaves active release unchanged;
- deterministic conformance suite remains rerunnable after code changes without being mislabelled as a new probabilistic held-out campaign;
- ledger tampering/inconsistent observed state -> release rejection.

## 16. Acceptance criteria

Phase 2 is not complete unless:

1. every probabilistic gate family uses preregistered leakage-safe decisive evidence;
2. candidate identity covers every behavior-bearing input relevant to the metric;
3. observed decisive evidence cannot freshly authorize a changed candidate;
4. identical-candidate replay is reproduction-only;
5. finite campaign/reserve rules prevent stop-on-pass cherry-picking;
6. later campaigns use genuinely fresh independently reviewed evidence;
7. Wilson sample/stratum/reporting rules and Section 29.3 reviewer reliability are enforced;
8. deterministic zero-failure conformance suites remain correctly treated as complete executable contract gates rather than fake probabilistic held-out samples;
9. every decisive result is bound to candidate/split/reviewer/campaign identity;
10. any failed probabilistic gate blocks activation and preserves the previous active release.

The core rule is: **observed decisive statistical evidence is history for that behavior-bearing candidate family, while deterministic conformance suites remain versioned executable contracts rerun in full.**
