# Phase 2 Held-Out Retry Policy

**Project:** ClauseSift  
**Phase:** 2 — Exact Retrieval MVP  
**Status:** Normative Phase 2 implementation-plan appendix  
**Primary design authority:** `docs/design.md`  
**Upstream split policy:** `docs/implementation/phase-0-evaluation-corpus.md`  
**Companion gate plan:** `docs/implementation/phase-2-release-gates.md`

## 1. Purpose and precedence

This appendix defines leakage-safe retry, split-retirement, reserve/replenishment, and reproduction rules for **all decisive Phase 2 held-out gate families** after any decisive result is observed.

Current Phase 2 gate families include:

- lexical retrieval;
- canonical classification;
- required-context completeness;
- material-conflict completeness;
- any end-to-end ordinary Evidence Package gate that consumes independently reviewed decisive labels.

It does not govern Phase 3 embedding/fusion selection or Phase 4 high-accuracy reranking/supporting-context gates.

Where another Phase 2 document can be read as allowing a materially changed candidate to reuse an already observed decisive split for fresh authorization, this policy is authoritative: **it may not.**

## 2. Core rule

A decisive held-out split may reveal whether one frozen candidate passes. Once revealed, it becomes evidence history, not a reusable optimizer for a materially changed candidate.

Observation includes exposure of labels, expected context/conflict sides, raw per-case outputs, aggregate scores sufficient to identify failures, or any other information that could guide remediation.

## 3. Campaign roles

Every Phase 2 evaluation case used in a release campaign has exactly one declared role for that campaign:

- `development`;
- `benchmark_selection`;
- `screening_nondecisional` where explicitly preregistered;
- `final_confirmation`;
- `reproduction_only` after decisive observation.

A final-confirmation case cannot simultaneously be model/rule selection data.

## 4. Frozen candidate identity

A candidate identity is the deterministic hash of all behavior-bearing inputs relevant to the gate family.

### 4.1 Lexical identity

Include at minimum:

- lexical engine/version;
- tokenizer/version;
- field weights;
- normalization/query-compiler configuration;
- lexical index schema/version;
- canonical chunk/search-text identity;
- other behavior-bearing lexical configuration.

### 4.2 Classification identity

Include at minimum:

- evidence-vocabulary version/hash;
- classification schema;
- deterministic classification rule/configuration;
- inheritance rule/configuration;
- ordered immutable reviewed classification artifacts;
- canonical-model inputs on which those rules operate.

### 4.3 Required-context identity

Include every behavior-bearing input that can change required closure, including:

- edge identity schema;
- occurrence identity schema;
- relationship resolver/configuration where it changes navigability;
- context rule-set version/configuration;
- relation-type ordering;
- context materialization/source-cover version;
- structural/semantic/object/path/step bounds;
- evidence vocabulary/classifications consumed by rule eligibility;
- release graph/catalog identity.

### 4.4 Material-conflict identity

Include at minimum:

- conflict identity schema;
- detector/rule/configuration identity;
- context rule/configuration consumed by conflict classification;
- comparison projection/unit normalization identity;
- immutable decision/review-policy artifacts;
- canonical position/source-cover algorithm identity;
- conflict limits and catalog/release identity.

### 4.5 Evidence Package identity

For a decisive end-to-end Evidence Package gate also bind:

- exact/lexical seed behavior;
- required-context identity;
- material-conflict identity;
- central serializer/schema/configuration;
- warning/completeness routing behavior;
- release/build/source identity;
- interface-neutral shared evidence service identity.

A behavior-bearing change creates a new candidate for every affected decisive gate family even when the change was motivated by another dataset.

## 5. Preregistration

Before any decisive Phase 2 final-confirmation data is observed, record:

- campaign ID;
- frozen candidate identity hash(es);
- gate family/families;
- exact decisive split identity/hash;
- expected labels/obligations version;
- review/adjudication policy and artifacts;
- applicable sample-size/stratification requirements;
- any allowed nondecisional screening split identities and exact order;
- corpus/canonical-ID migration versions;
- rules for candidate replay and campaign closure.

The preregistration artifact is immutable for that campaign.

## 6. One decisive use while unseen

A final-confirmation split may authorize release evidence only on its first decisive evaluation while unseen for the frozen candidate/campaign.

After that evaluation, whether it passes or fails, it becomes `observed_retired` for fresh authorization of a materially changed candidate.

It remains useful for:

- audit;
- reproduction;
- regression history;
- forensic diagnosis;
- confirming deterministic re-execution of the exact same candidate.

## 7. Identical-candidate replay

The exact same candidate identity may rerun the same observed split only as `reproduction_only`.

Such a replay:

- cannot create a second independent pass;
- cannot erase/reset an original failure;
- cannot authorize a changed candidate;
- must remain linked to the original decisive event;
- must reproduce the original result under deterministic contracts or expose a reproducibility failure.

No repeated attempts, random seeds, environment changes, or selective reporting may convert a failed decisive event into a pass unless a preregistered nondeterministic protocol was explicitly admitted before first observation.

## 8. Changed candidate after decisive observation

A changed candidate cannot use the observed split for fresh pass/fail authorization.

This includes changes to lexical configuration, classification rules, required-context behavior, conflict rules/decisions/covers, serializer behavior, or any upstream source/catalog/release input that changes the applicable expected result.

After a failure:

1. activation remains blocked;
2. the result is retained permanently;
3. remediation returns to development/benchmark/review evidence;
4. a new candidate is frozen without consulting hidden labels from a fresh decisive split;
5. a new campaign or the next valid preregistered path obtains genuinely fresh decisive evidence;
6. the new split and candidate are preregistered before observation.

## 9. Finite campaign and no stop-on-pass sequence

Phase 2 must not permit an unlimited sequence of decisive reserve splits until one passes.

A release campaign has one final decisive confirmation event for each jointly exposed decisive split family unless the preregistered statistical procedure explicitly defines a different finite joint test before observation.

Failure closes that campaign for the failed candidate.

Any screening reserves are nondecisional, finite, preregistered, and cannot authorize activation.

A materially changed candidate after final failure requires a fresh campaign and fresh decisive evidence.

## 10. Reserve-split preregistration

If nondecisional reserves/screening sets are used, preregister:

- exact identities/order or deterministic blinded allocation procedure;
- gate families supported;
- purpose (`screening_nondecisional` only unless explicitly a later fresh campaign);
- minimum applicable samples/strata;
- who controls label visibility;
- retirement semantics;
- overlap rejection;
- replenishment process.

Implementers cannot inspect several unseen splits and choose the most favorable one.

## 11. Fresh later campaign

A later campaign after decisive failure must use genuinely fresh independently reviewed decisive evidence satisfying Phase 0 governance.

Requirements include:

- independently sourced/labelled applicable cases;
- required two-reviewer/adjudication methodology where Phase 0 specifies it;
- no forbidden overlap with development/benchmark/previously observed decisive cases;
- required samples/strata;
- versioned split and label identities;
- reviewed canonical-ID migration before scoring where applicable;
- preregistration before observation.

Paraphrasing an observed query, punctuation changes, or duplicating the same underlying source case does not create fresh decisive evidence.

## 12. Gate-family exposure semantics

Observation is tracked at the case/split evidence level, not hidden by renaming metrics.

The Phase 2 decisive families include:

1. lexical Recall@20;
2. lexical Top-5;
3. `node_type` accuracy;
4. `normative_status` accuracy;
5. `source_modality` accuracy;
6. required-context completeness;
7. material-conflict completeness;
8. end-to-end Evidence Package correctness where separately labelled.

Where one split exposes labels used by several families, the preregistered policy defines their joint retirement before evaluation.

For context/conflict gates, observing expected required targets, expected conflict sides, or per-case omission diagnostics counts as observation even if no scalar metric is reported.

## 13. Release-gate ledger

Every decisive run records at minimum:

- campaign ID;
- candidate identity;
- gate family;
- split identity/version/hash;
- split role;
- reviewed canonical-ID migration artifact where applicable;
- raw-result hash;
- sample counts;
- Wilson result for probabilistic gates;
- zero-omission counts/details for context/conflict gates;
- pass/fail;
- whether split was unseen at decision time;
- resulting split state;
- predecessor/successor campaign linkage.

Release validation rejects a purported decisive result when:

- candidate identity does not match evaluated behavior;
- split was already observed by a different candidate;
- split is reproduction-only/nondecisional;
- reserve/campaign order is invalid;
- overlap/leakage is detected;
- required independent review/migration evidence is missing;
- a final-failure campaign is reused for another decisive attempt.

## 14. Context/conflict-specific anti-leakage rules

Do not tune required traversal or conflict behavior against a decisive omission list.

After decisive context/conflict failure, implementers may retain high-level failure history, but the exact observed expected-target/position labels cannot become the training/selection set for repeated candidate attempts while still being called held out.

Changes such as:

- adding a required edge rule;
- changing endpoint eligibility;
- changing context source-cover ordering;
- changing conflict detection/explanation;
- altering canonical position cover;
- changing serializer omission behavior;

create a changed candidate and require fresh decisive evidence for affected families.

## 15. Tests

Test at minimum:

- first frozen candidate + unseen decisive split -> allowed;
- identical candidate + same observed split -> reproduction-only, no new decision;
- changed lexical candidate + same observed split -> rejected;
- changed classification rules + same observed split -> rejected;
- changed context rule only + same observed context split -> rejected;
- changed conflict rule/decision/cover only + same observed conflict split -> rejected;
- changed serializer that affects context/conflict projection + same observed end-to-end split -> rejected;
- fresh later campaign + genuinely new reviewed split -> allowed;
- out-of-order/cherry-picked reserve -> rejected;
- replenished split with overlap -> rejected;
- replenished split below sample/stratum requirement -> rejected;
- missing independent review -> rejected;
- multiple unseen reserve results inspected before candidate choice -> rejected;
- final failure closes campaign;
- failed gate leaves active release unchanged;
- reproduction mismatch exposes reproducibility failure;
- ledger tampering/inconsistent observed state blocks release.

## 16. Acceptance criteria

Phase 2 is not complete unless:

1. retry/retirement governance covers every decisive Phase 2 gate family now owned by current design;
2. preregistration occurs before decisive observation;
3. every decisive changed candidate uses genuinely unseen eligible evidence;
4. observed evidence cannot authorize a materially changed candidate;
5. identical-candidate replay is reproduction-only;
6. campaign/reserve use is finite and cannot become stop-on-pass cherry-picking;
7. later campaigns use fresh independently reviewed evidence;
8. every decisive result is bound to candidate/split/campaign identity and applicable review/migration evidence;
9. context/conflict expected-label exposure is treated as observation even without a scalar score;
10. any gate failure blocks activation and preserves the prior active release.

The operational rule remains simple: **once decisive evidence has been revealed, it is history for that candidate family, not a reusable optimizer for the next candidate.**
