# Phase 2 Release-Gate Appendix

**Project:** ClauseSift  
**Phase:** 2 — Exact Retrieval MVP  
**Status:** Normative Phase 2 implementation-plan appendix  
**Primary design authority:** `docs/design.md`  
**Companion plan:** `docs/implementation/phase-2-exact-retrieval-mvp.md`

## 1. Purpose and scope

This appendix defines the Phase 2 evaluation-data separation, probabilistic release gates, and activation/failure tests that apply to the Exact Retrieval MVP.

It is intentionally limited to capabilities implemented in Phase 2:

- lexical retrieval;
- canonical `node_type` classification;
- canonical `normative_status` classification;
- canonical `source_modality` classification;
- the deterministic Phase 2 conformance suites already defined by the companion plan.

It does **not** add Phase 3 embedding/vector/fusion gates or Phase 4 reranking, runtime Evidence Graph traversal, optional-context, conflict-runtime, or refusal gates.

Where the companion Phase 2 plan can be read as allowing lexical engine/tokenizer selection to use the held-out release-gate sample, or as omitting the three probabilistic classification gates, this appendix is authoritative and narrows/corrects that interpretation. In particular, it supersedes the sequencing implications of the companion plan's lexical-selection, Phase 2 evaluation, quality-gate, failure-injection, acceptance-criteria, and recommended-sequence sections only to the extent necessary to implement the rules below.

## 2. Evaluation split separation is mandatory

Phase 2 consumes the Phase 0 versioned split manifests and keeps the following roles distinct:

- **development diagnostics** — may be inspected repeatedly while implementing lexical query handling, deterministic classification rules, normalization, and other Phase 2 behavior;
- **benchmark/model-selection split** — may be used to compare lexical engines, tokenizers, field weights, and other candidate configurations;
- **held-out release-gate split** — must remain outside engine/tokenizer/configuration/classification-rule tuning and is evaluated only after the applicable candidate behavior is frozen;
- **calibration split** — remains governed by the Phase 0 human-review methodology and is not a product-metric tuning set.

An item cannot be silently moved from the held-out release-gate split into development or benchmark data after its output is observed. Any Phase 0-permitted label or split correction requires the Phase 0 change-control procedure and an auditable version change where meaning changes.

The implementation must validate split membership before every benchmark or release-gate run. A benchmark-selection command must refuse to consume held-out release-gate labels. A release-gate command must identify the exact held-out split version it evaluated.

## 3. Lexical selection and lexical release gating are separate operations

### 3.1 Candidate selection

Lexical engine/tokenizer/configuration selection uses only development diagnostics and the dedicated benchmark/model-selection split.

Candidate comparison may use:

- Recall@5/10/20;
- MRR;
- nDCG;
- exact-token preservation;
- document/edition/clause/page hit diagnostics;
- table-evidence hit diagnostics;
- English, Chinese, and cross-language strata;
- punctuation, identifier, number, and unit behavior;
- index size/build time/load time/query latency;
- packaging and reproducibility observations.

Accuracy remains the first decision criterion. Packaging or speed cannot justify a known material quality regression.

After selection, freeze and record at minimum:

- lexical engine identity and version;
- tokenizer identity and version;
- field weights;
- normalization/query-compiler configuration;
- index schema/version;
- benchmark split version;
- source/corpus versions used for selection;
- the selected configuration hash.

No held-out release-gate result may be used to choose between candidates or tune the frozen candidate.

### 3.2 Held-out lexical release gates

Only after the lexical candidate is frozen does Phase 2 evaluate the untouched held-out release-gate split.

The following design gates are blocking:

- expected evidence present in **Recall@20**: one-sided 95% Wilson lower confidence bound **at least 98%**;
- expected evidence present in **Top 5**: one-sided 95% Wilson lower confidence bound **at least 95%**.

Phase 0 sample-size requirements apply independently:

- at least **150 applicable independently labelled cases** for the 98% Recall@20 gate;
- at least **60 applicable independently labelled cases** for the 95% Top-5 gate;
- larger samples when required strata would otherwise be underrepresented.

The report for each gate contains:

- successes;
- failures;
- total applicable cases;
- point estimate;
- one-sided 95% Wilson lower bound;
- target;
- pass/fail;
- corpus/question/label/split versions;
- excluded/not-applicable count and reasons;
- selected lexical configuration hash.

A held-out failure blocks Phase 2 activation. It does **not** authorize iterative tuning against that held-out sample. Remediation must return to development/benchmark evidence, produce a newly frozen candidate, and follow the Phase 0 leakage/change-control policy before another release-gate evaluation.

## 4. Classification selection and release gating are separate operations

Phase 2 constructs and admits all three canonical classification fields:

- `node_type`;
- `normative_status`;
- `source_modality`.

Therefore all three design classification-accuracy gates apply in Phase 2.

### 4.1 Rule development and freezing

Deterministic source-format rules, inheritance rules, manifest/source-marker handling, and reviewed classification decisions are developed and validated against development/benchmark material, not the held-out release-gate sample.

Before held-out evaluation, freeze and record:

- evidence-vocabulary version and hash;
- classification schema version;
- deterministic classification rule-set version/configuration hash;
- inheritance-rule version/configuration hash;
- ordered immutable human-review artefact hashes where applicable;
- held-out classification split version.

Retrieval rank, document recency, or model output cannot alter the frozen classifications.

### 4.2 Three independent probabilistic blocking gates

Evaluate each field independently on its applicable, independently labelled held-out classification corpus:

1. **node-type accuracy** — one-sided 95% Wilson lower confidence bound **at least 98%**;
2. **normative-status accuracy** — one-sided 95% Wilson lower confidence bound **at least 98%**;
3. **source-modality accuracy** — one-sided 95% Wilson lower confidence bound **at least 98%**.

Each gate requires at least **150 applicable independently labelled cases**, with larger stratified samples when a classification field, origin, inheritance branch, document/node family, language, ambiguity class, or critical hard negative would otherwise be underrepresented.

Counts may not be pooled across the three fields to satisfy the minimum. Each field receives its own numerator, denominator, point estimate, Wilson lower bound, target, and pass/fail result.

The three probabilistic gates are in addition to, not replacements for, deterministic conformance requirements such as:

- exact vocabulary/schema conformance;
- classification-provenance/inheritance fidelity;
- legacy-alias rejection;
- unsupported-version rejection;
- deterministic recomputation equality;
- zero promotion of `unclassified`/`unknown` to an unsupported stronger value;
- no inference of project-specific legal force from source modality.

Any one of the three Wilson lower bounds below 98% blocks Phase 2 activation.

## 5. Phase 2 quality gate

An Exact Retrieval MVP candidate may be activated only when **all** applicable Phase 2 gates pass, including:

- manifest/source/parser/canonical/page/chunk/catalog/integrity gates from the companion plan;
- deterministic exact-clause and citation suites;
- deterministic evidence-vocabulary/classification/provenance suites;
- held-out lexical Recall@20 Wilson lower bound >= 98%;
- held-out lexical Top-5 Wilson lower bound >= 95%;
- held-out `node_type` Wilson lower bound >= 98%;
- held-out `normative_status` Wilson lower bound >= 98%;
- held-out `source_modality` Wilson lower bound >= 98%;
- durable static/evaluation reports;
- candidate checksum/read-only smoke validation;
- no unresolved Phase 2 release blocker.

A missing applicable sample, insufficient sample size, leakage violation, evaluation-execution failure, or missing gate report is blocking; it is never interpreted as a pass.

Phase 3/4-only metrics remain explicitly `not_implemented_in_phase_2` and cannot be used either to pass or fail this milestone.

## 6. Required reports

The Phase 2 evaluation artefact and static review report must distinguish:

- lexical candidate-selection results on the benchmark split;
- the frozen lexical configuration identity;
- held-out lexical release-gate results;
- classification development/conformance results;
- the frozen classification-rule identities;
- held-out classification release-gate results for each of the three fields;
- leakage/split-integrity validation;
- sample counts and underrepresented strata;
- deterministic conformance failures separately from probabilistic estimates.

No report may present benchmark-selection performance as held-out release evidence.

## 7. Tests required by this appendix

### 7.1 Split-integrity tests

Test that:

- lexical selection rejects held-out release-gate items;
- classification-rule tuning rejects held-out release-gate items;
- release-gate evaluation records the exact held-out split version;
- overlap forbidden by Phase 0 split policy is detected;
- a post-observation split/label mutation without required version/change-control evidence is rejected.

### 7.2 Wilson boundary tests

For each of the five probabilistic Phase 2 gates, test:

- exact pass boundary;
- first failing result below the required lower bound;
- minimum applicable sample count;
- one-under minimum sample count;
- excluded/not-applicable accounting;
- stratification-driven sample expansion;
- numerator/denominator reporting.

The five gates are:

1. lexical Recall@20 >= 98%;
2. lexical Top 5 >= 95%;
3. node-type accuracy >= 98%;
4. normative-status accuracy >= 98%;
5. source-modality accuracy >= 98%.

### 7.3 Activation/failure injection

Inject and prove blocking behavior for:

- lexical Recall@20 held-out gate failure;
- lexical Top-5 held-out gate failure;
- node-type held-out gate failure;
- normative-status held-out gate failure;
- source-modality held-out gate failure;
- insufficient sample size for any applicable gate;
- held-out leakage into candidate selection/tuning;
- evaluation execution failure;
- missing/corrupt gate report.

For every failure:

- the candidate release is not activated;
- the previous active release remains unchanged;
- diagnostics/report data remain available;
- no gate is silently skipped or downgraded to advisory.

## 8. Corrected Phase 2 execution order

The Phase 2 evaluation/release portion of the implementation sequence is:

1. complete and freeze the Phase 2 catalog and deterministic build artefacts;
2. compare lexical candidates using development + benchmark/model-selection data only;
3. choose and freeze one lexical engine/tokenizer/configuration;
4. build the candidate lexical index from that frozen configuration;
5. complete/freeze the Phase 2 deterministic classification rule/review inputs;
6. run deterministic conformance/regression suites;
7. run split-integrity validation;
8. evaluate the frozen lexical candidate on the untouched held-out release split;
9. evaluate the frozen classification behavior on the independently labelled held-out classification split for all three fields;
10. persist the raw evaluation results and gate reports;
11. enforce all Phase 2 blocking gates;
12. finalize the Phase 2 static report;
13. assemble/validate/reopen the immutable candidate release;
14. run read-only smoke tests;
15. activate only after every preceding gate succeeds.

The held-out release sample is a gate, not an optimizer.

## 9. Acceptance additions

In addition to the companion plan's Phase 2 acceptance criteria, Phase 2 is not complete unless:

1. lexical candidate selection and held-out lexical release evaluation use distinct Phase 0 split roles;
2. the frozen lexical candidate meets the 98% Recall@20 and 95% Top-5 one-sided Wilson lower-bound gates on untouched held-out data;
3. `node_type`, `normative_status`, and `source_modality` each meet an independent 98% one-sided Wilson lower-bound gate on applicable independently labelled held-out data;
4. every applicable 98% gate has at least 150 cases and every applicable 95% gate has at least 60 cases, increased when stratification requires it;
5. split-integrity/leakage validation passes;
6. all five probabilistic gate reports retain numerator, denominator, lower bound, target, versions, and exclusions;
7. failure or insufficient evidence for any gate prevents activation without changing the previous active release.

These requirements remain strictly Phase 2 because they gate only capabilities Phase 2 itself constructs and advertises.
