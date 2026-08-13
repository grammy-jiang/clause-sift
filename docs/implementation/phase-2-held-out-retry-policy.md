# Phase 2 Held-Out Retry Policy

**Project:** ClauseSift  
**Phase:** 2 — Exact Retrieval MVP  
**Status:** Normative Phase 2 implementation-plan appendix  
**Primary design authority:** `docs/design.md`  
**Upstream split policy:** `docs/implementation/phase-0-evaluation-corpus.md`  
**Companion gate plan:** `docs/implementation/phase-2-release-gates.md`

## 1. Purpose and precedence

This appendix defines the retry/rotation policy for Phase 2 held-out release gates after any held-out result has been observed.

It is deliberately limited to Phase 2 lexical and canonical-classification gates. It does not define Phase 3 embedding/fusion gates or Phase 4 reranking/context/conflict/refusal gates.

Where `phase-2-release-gates.md` says that remediation may produce a newly frozen candidate and proceed to another release-gate evaluation, this appendix is authoritative: **a materially changed candidate may not obtain a new release decision from the same already-observed held-out split.**

## 2. One decisive use of an unseen held-out split

Before the first release-gate evaluation for a candidate family, the project preregisters the held-out rotation policy and exact split identities that may be used.

For one frozen candidate, one previously unseen held-out split may be used for the release decision. Once any result from that split is exposed to implementers, maintainers, selection code, or candidate-development workflows, that split becomes **observed**.

An observed split remains useful for:

- audit and reproduction of the original result;
- regression history;
- forensic analysis of failures;
- verifying that identical candidate bytes reproduce the identical score.

It is no longer valid as fresh evidence for selecting or approving a materially changed candidate.

## 3. Candidate identity

A candidate identity is the deterministic hash of all Phase 2 behavior-bearing inputs relevant to the gate.

For lexical gates this includes at minimum:

- lexical engine/version;
- tokenizer/version;
- field weights;
- normalization and query-compiler configuration;
- lexical index schema/version;
- canonical chunk/search-text inputs;
- any other behavior-bearing lexical configuration.

For classification gates this includes at minimum:

- evidence-vocabulary version/hash;
- classification schema;
- deterministic classification rule set/configuration;
- inheritance rule set/configuration;
- ordered immutable reviewed classification artefacts;
- canonical-model inputs on which those rules operate.

A change to any behavior-bearing input creates a new candidate for held-out purposes even when the change was motivated by a different dataset.

## 4. Identical-candidate replay

The exact same candidate identity may be rerun on the exact same observed held-out split only for deterministic reproduction/audit.

Such a replay:

- must be labelled `reproduction_only`;
- must not create a new independent release-gate decision;
- must reproduce the original raw outputs and gate result under the declared deterministic contract, or else expose a reproducibility failure;
- cannot turn an original failure into a pass through repeated attempts, random seeds, environment changes, or selective reporting.

If the implementation is intentionally nondeterministic in a way the design permits, the preregistered gate procedure must define the complete repeated-sampling protocol **before** the first held-out observation. Phase 2 must not invent repeated trials after seeing a failure.

## 5. Materially changed candidate after a held-out failure

When a held-out gate fails:

1. activation is blocked;
2. the failed split is marked observed/retired for new-candidate release decisions;
3. remediation returns to development and benchmark/model-selection evidence;
4. a new candidate is frozen without consulting hidden labels from any unused reserve split;
5. the next release decision uses the next preregistered unused reserve split, or a newly replenished independently labelled blinded split that satisfies all Phase 0 sample-size and stratification requirements;
6. the rotation/replenishment event and split versions are recorded before the new candidate is evaluated.

The failed held-out result may inform high-level diagnosis, but it cannot become an oracle for repeatedly choosing candidates until one passes the same cases.

## 6. Reserve-split preregistration

If the project expects more than one candidate attempt, it must preregister a deterministic reserve policy before the first held-out result is seen.

A valid policy records:

- ordered reserve split identifiers or a deterministic blinded allocation procedure;
- the gate families each reserve split covers;
- minimum applicable sample counts;
- required strata;
- who controls label visibility;
- when a reserve split becomes observed/retired;
- how replenishment obtains independent labels;
- how overlap with development, benchmark, previous held-out, and calibration data is rejected.

The implementation may not inspect several reserve splits and choose the one on which a candidate performs best.

## 7. Replenished held-out data

A replenished held-out split must satisfy the same ground-truth and review requirements as the original Phase 0 release-gate data, including:

- independently sourced/labelled applicable cases;
- applicable two-reviewer/adjudication methodology;
- required calibration/reliability rules;
- no forbidden overlap with development/benchmark or previously observed held-out cases;
- required per-gate sample sizes and stratification;
- versioned split and label identities;
- Phase 2 canonical-ID migration completed and reviewed before scoring.

Replenishment is not achieved by paraphrasing an already observed query, trivially changing punctuation, or duplicating the same source case while preserving the answer.

## 8. Gate-family isolation

Observation status is tracked at the case/split level and cannot be hidden by renaming the metric.

The five Phase 2 probabilistic gate families are:

1. lexical Recall@20;
2. lexical Top-5 evidence presence;
3. `node_type` accuracy;
4. `normative_status` accuracy;
5. `source_modality` accuracy.

A case whose expected evidence/classification has been exposed through one gate cannot be treated as unseen for another candidate merely because a different metric is being reported from the same label.

Where one split legitimately supports several gate families, the preregistered policy must define their joint exposure/retirement semantics before evaluation.

## 9. Release-gate ledger

Every decisive held-out run records:

- candidate identity;
- gate family;
- split version;
- canonical-ID migration artefact hash;
- raw-result hash;
- sample counts;
- Wilson result where applicable;
- decision (`pass` or `fail`);
- whether the split was previously unseen at decision time;
- resulting split state (`observed_retired`);
- next eligible reserve policy reference.

A release validator rejects a purported decisive gate result when:

- the candidate identity does not match the evaluated bytes/configuration;
- the split had already been observed by a different candidate;
- the split was eligible only for reproduction;
- reserve order was bypassed;
- split overlap/leakage is detected;
- the canonical-ID migration was not reviewed before scoring.

## 10. Tests

Phase 2 must test at minimum:

- first frozen candidate + unseen split -> decisive run allowed;
- identical candidate + same observed split -> reproduction-only allowed, no new decision;
- changed lexical candidate + same observed split -> decisive run rejected;
- changed classification rule set + same observed split -> decisive run rejected;
- changed candidate + next preregistered unseen reserve -> decisive run allowed;
- changed candidate + reserve chosen out of preregistered order -> rejected;
- replenished split with overlap -> rejected;
- replenished split below required sample size -> rejected;
- replenished split without required independent review -> rejected;
- multiple reserve results inspected before candidate choice -> rejected;
- failed gate leaves active release unchanged;
- retry uses a reviewed canonical-ID migration for the new held-out split.

## 11. Acceptance criteria

Phase 2 is not complete unless:

1. the held-out retry/rotation policy is preregistered before first decisive evaluation;
2. every decisive candidate uses an unseen eligible held-out split;
3. an observed split cannot produce a fresh decision for a materially changed candidate;
4. identical-candidate replay is clearly non-decisional and used only for reproducibility;
5. reserve/replenished splits preserve Phase 0 independence, review, sample-size, and stratification rules;
6. reserve order cannot be cherry-picked after observing results;
7. every decisive result is bound to candidate identity, split identity, and reviewed canonical-ID migration;
8. a failure blocks activation and does not permit repeated optimization against the same held-out cases.

The core rule is simple: **a held-out release gate may reveal whether one frozen candidate passes; once revealed, it is evidence history, not a reusable optimizer for the next candidate.**
