# Phase 3 Final Review Corrections

**Project:** ClauseSift  
**Phase:** 3 — Hybrid Retrieval  
**Status:** Normative Phase 3 implementation-plan correction  
**Primary design authority:** `docs/design.md`  
**Companion plans:** `docs/implementation/phase-3-hybrid-retrieval.md`, `docs/implementation/phase-3-query-preprocessing-identity.md`, `docs/implementation/phase-3-release-identity-clarifications.md`

## 1. Purpose and precedence

This document closes the remaining Phase 3 review findings without expanding Phase 3 into Phase 2 corrective implementation work or Phase 4 high-accuracy implementation work.

Where the existing Phase 3 plan set conflicts with a rule below, **this document is authoritative for Phase 3**. It supersedes the stale wording identified below in the main Phase 3 plan and replaces the intermediate review/alignment addenda created during earlier approval cycles.

The corrections are limited to:

1. truthful Phase 2 prerequisite wording;
2. Phase 3-specific held-out confirmation/retry/rotation rules;
3. immutable build-time lineage versus per-query retrieval/assembly lineage;
4. the final acceptance implications of those corrections.

## 2. Phase 2 prerequisite correction

Current `docs/design.md` assigns deterministic required Evidence Graph context closure, deterministic material-conflict closure, and the ordinary shared evidence interfaces to **Phase 2**.

The already merged Phase 2 implementation-plan documents predate that current phase boundary and do not yet contain the full runtime closure/evidence-service implementation plan. That is a lower-phase corrective gap; it is not permission to move the work into Phase 3 or Phase 4.

### 2.1 Superseded main-plan statement in Section 1

The main plan sentence beginning with:

> Phase 2 already establishes ...

must **not** be read as a claim that the merged Phase 2 implementation plan already implements required-context/material-conflict closure.

The authoritative replacement meaning is:

> Current `docs/design.md` assigns Phase 2 ownership of the canonical exact/lexical baseline, deterministic required-context closure, material-conflict closure, and ordinary shared evidence interfaces. The merged Phase 2 implementation-plan set predates that current design boundary. Phase 3 may develop retrieval-only components against immutable canonical chunk fixtures, but release-capable Phase 3 runtime integration, downstream evidence-semantics confirmation, activation, and completion are blocked until a separately reviewed Phase 2 corrective plan/implementation supplies and validates the missing lower-phase closure/evidence-service baseline.

### 2.2 Superseded main-plan prerequisite wording in Section 4

The Section 4 wording that Phase 3 simply “starts only from the merged Phase 2 baseline” is incomplete.

The authoritative prerequisite is:

1. the merged Phase 2 canonical identity, chunk, catalog, exact, lexical, citation, release, integrity, and lineage contracts remain reusable;
2. a separate Phase 2 corrective plan/implementation must bring ordinary required-context/material-conflict closure and the basic shared evidence service into conformance with current `docs/design.md`;
3. Phase 3 consumes that corrected lower-phase service and must not duplicate it;
4. Phase 3 release-capable integration and final confirmation are blocked until that prerequisite exists;
5. offline embedding/fusion benchmark work may proceed earlier only against immutable canonical fixtures and may not claim a complete Phase 3 release path.

### 2.3 Phase 3 composition after prerequisite satisfaction

Once the corrected Phase 2 prerequisite exists, the Phase 3 runtime composition is:

```text
validated query
  -> deterministic query preprocessing / analysis
  -> exact and/or lexical and/or dense candidate retrieval
  -> lexical+dense RRF where hybrid is selected
  -> deterministic retrieval-seed ordering
  -> Phase 2-owned required-context closure
  -> Phase 2-owned material-conflict closure
  -> ordinary strict Evidence Package assembly
  -> shared Python / CLI / MCP projection
```

Dense similarity, query classification, and RRF end at seed selection. They cannot create source facts, applicability, context relations, conflict decisions, precedence, or citations.

## 3. Frozen Phase 3 candidate identity

The frozen Phase 3 candidate identity includes every behavior-bearing input that can change retrieval or routing behavior, including:

- embedding model ID/revision and complete model-asset identity;
- provider/configuration hash;
- `embedding_text` schema/version/configuration;
- canonical release vector dtype and normalization rule;
- exact dense backend/version/metric/configuration;
- dense candidate-pool size;
- lexical candidate-pool size;
- final fused candidate-pool size;
- RRF rule/configuration;
- deterministic query-preprocessing schema/rule/configuration identity;
- normalized-query construction identity;
- query-analysis rule-set/configuration;
- classifier rule-set/configuration;
- relevant dependency-lock/toolchain identity where declared by the design.

A change to any behavior-bearing identity creates a different candidate and invalidates previously decisive Phase 3 final-gate evidence for the changed candidate.

## 4. Phase 3 held-out confirmation and retry authority

The Phase 2 held-out retry document is explicitly Phase 2-scoped. It does not implicitly govern Phase 3 embedding, dense, fusion, preprocessing, or classifier gates.

This section is the normative Phase 3 retry/rotation policy.

### 4.1 Split roles

Every evaluation case used by Phase 3 has exactly one declared campaign role:

- `development`;
- `model_selection`;
- `screening_nondecisional`;
- `final_confirmation`;
- `reproduction_only` after an observed split is replayed for the exact same candidate.

A decisive confirmation split cannot also be model-selection data.

### 4.2 Preregistration

Before any decisive Phase 3 confirmation data is observed, record:

- campaign ID;
- complete frozen candidate identity hash;
- gate families;
- applicable strata;
- required sample-size rules;
- final confirmation split identity/hash;
- any optional screening-reserve identities in exact use order;
- corpus/review-policy versions;
- independent label/review evidence required by Phase 0.

The preregistration artifact is immutable for that campaign.

### 4.3 One decisive use while unseen

A final confirmation split may authorize Phase 3 release evidence only on its first decisive evaluation while unseen for the frozen candidate/campaign.

After that evaluation, whether it passes or fails, the split is `observed` and retired for decisive use by any materially changed candidate.

### 4.4 Identical-candidate replay

The exact same frozen candidate may replay an observed split only to reproduce or diagnose the recorded result.

Such a run is labelled `reproduction_only` and:

- cannot create a second independent pass;
- cannot reset a failure;
- cannot change the original decision;
- cannot by itself authorize release;
- remains linked to the original decisive observation in the campaign ledger.

### 4.5 Changed candidates require fresh decisive evidence

A changed candidate may not use an observed Phase 3 final-confirmation split for pass/fail evidence.

This includes changes to:

- embedding model or any model asset;
- provider or embedding configuration;
- embedding/query preprocessing;
- vector dtype/normalization representation;
- dense backend/metric;
- candidate pools;
- RRF;
- query analysis/classifier;
- any other behavior-bearing frozen identity.

### 4.6 Finite campaign; no stop-on-pass sequence

A Phase 3 release campaign has exactly **one final decisive confirmation split**.

Failure of that final confirmation ends the campaign. A materially changed candidate cannot simply advance to another decisive reserve in the same campaign until something passes.

If screening reserves are used, at most two are allowed and they are explicitly **non-decisional**. They may help diagnose a frozen candidate before final confirmation, but they cannot authorize release.

### 4.7 Fresh later campaign

After final-confirmation failure:

1. retain the failed result permanently in the audit trail;
2. perform remediation only on development/model-selection evidence;
3. freeze a new candidate;
4. create a new campaign ID;
5. supply a newly created or replenished, independently labelled and reviewed confirmation split meeting Phase 0 sample/stratification rules;
6. preregister the new split before observation.

A later campaign without genuinely fresh decisive evidence is invalid.

### 4.8 No reserve cherry-picking

If screening/reserve splits exist, their identities and order are preregistered. Implementers cannot inspect several unseen splits and choose the most favorable result.

### 4.9 Campaign ledger

Persist a deterministic Phase 3 gate ledger containing at minimum:

- campaign ID;
- candidate identity hash;
- split identity/hash;
- split purpose;
- observed state;
- retired state;
- first decisive observation event;
- gate numerator/denominator/point estimate/Wilson bound;
- campaign outcome;
- predecessor/successor campaign linkage where applicable.

Release validation rejects contradictory split state, missing preregistration, reuse of an observed decisive split by a changed candidate, or a second final decisive attempt in one campaign.

### 4.10 Required retry-policy tests

Tests must prove:

- changed candidate + observed confirmation split is rejected;
- exact same candidate replay is `reproduction_only`;
- screening evidence cannot authorize release;
- a second final confirmation in one campaign is rejected;
- final-confirmation failure closes the campaign;
- a later campaign without fresh reviewed confirmation data is rejected;
- out-of-order reserve use is rejected;
- a query-preprocessing-only candidate change invalidates prior decisive evidence;
- ledger tampering blocks release.

## 5. Main-plan leakage-control correction

The main Phase 3 plan wording that the final release gate uses an “existing ... discipline inherited from earlier phases” is superseded.

The authoritative rule is:

> Embedding model, RRF parameter, candidate-pool, query-preprocessing, and classifier selection use development/model-selection data only. Phase 3 final confirmation follows Section 4 of this correction document. The Phase 2 retry policy is not implicitly extended to Phase 3.

Any later reference in the main plan to an “existing retry policy” for Phase 3 means this Phase 3-specific policy.

## 6. Evidence Lineage correction

Phase 3 has two provenance dimensions that must remain separate.

### 6.1 Immutable build-time `lineage.json`

The sealed release `lineage.json` contains only query-independent source/build/release provenance and release-artifact references.

Phase 3 may add:

- embedding-text transformation identity;
- embedding provider/model/revision/configuration;
- complete bound model-asset identity;
- embedding artifact hash;
- vector backend/metric/configuration identity;
- vector artifact hash or exact-backend declaration;
- lexical-index hash;
- RRF rule/configuration identity when it is release behavior;
- deterministic query-preprocessing identity when release-bound;
- query-analysis/classifier rule/configuration identity when release-bound.

Each new build transformation retains the complete transformation identity tuple required by the design:

```text
kind,
role,
producer,
producer_version,
configuration_sha256,
content_sha256
```

`lineage.json` must **not** contain request-specific:

- query text;
- lexical rank/score;
- dense rank/score;
- RRF contribution;
- fused rank/score;
- selected seed set;
- request ID;
- query-specific context path.

### 6.2 Runtime retrieval and assembly lineage

For each request, runtime Evidence Package assembly lineage records the per-query dimension, including as applicable:

- every contributing retrieval channel;
- release artifact hashes/configuration identities used by the channel;
- lexical rank/score;
- dense rank/score;
- per-channel RRF contribution;
- fused score/rank;
- resolved path/classifier identity;
- originating seed identity and selection role;
- accepted context/conflict paths and rule IDs after the corrected Phase 2 prerequisite exists.

This provenance is request-scoped and never mutates the immutable release.

## 7. Main-plan lineage correction

The main plan list that places lexical/dense/fusion rank/score/contribution metadata inside “the Phase 3 lineage update” must be interpreted according to Section 6 above:

- query-independent artifact/configuration identities belong in `lineage.json`;
- per-query rank/score/contribution metadata belongs in runtime assembly lineage.

Any acceptance criterion saying `lineage.json` contains “retrieval-channel provenance” is superseded by the more precise split above.

## 8. Cache-authority consistency

`docs/design.md` Section 25 — **Build cache and invalidation** — is the authoritative Phase 3 cache-dependency contract.

The companion Phase 3 main plan already points current embedding/vector cache work to Section 25. No outstanding Section 32 correction is implied by this plan set.

## 9. Corrected Phase 3 acceptance additions

Phase 3 cannot be declared complete unless all of the following are true:

1. the separate Phase 2 corrective prerequisite has supplied the current-design ordinary context/conflict/evidence baseline;
2. query-preprocessing identity is part of the frozen candidate and release/evaluation identities wherever behavior depends on it;
3. Phase 3 held-out confirmation follows the finite campaign policy in Section 4;
4. observed decisive splits are retired for changed candidates;
5. identical-candidate replays are reproduction-only;
6. failed final confirmation closes the campaign;
7. a later campaign uses fresh independently reviewed decisive evidence;
8. immutable `lineage.json` contains only query-independent source/build/release provenance and artifact/configuration identities;
9. per-query retrieval ranks/scores/fusion contributions live only in runtime assembly lineage;
10. hybrid retrieval composes with the corrected Phase 2 evidence pipeline without weakening edition/source/context/conflict semantics;
11. Phase 4 remains limited to the high-accuracy additions assigned by current `docs/design.md`.

## 10. Phase 3 review scope

These corrections are entirely Phase 3-scoped. They define Phase 3 evaluation governance, provenance ownership, and the boundary to a lower-phase prerequisite.

They do **not** specify the implementation details of the Phase 2 corrective closure work and do **not** implement Phase 4 reranking/supporting-context/high-accuracy behavior.

## 11. Superseded intermediate addenda

The intermediate review files `phase-3-current-design-alignment.md` and `phase-3-review-clarifications.md` are superseded by this document and should not remain as parallel normative authorities in the final Phase 3 plan set.
