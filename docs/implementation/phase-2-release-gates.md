# Phase 2 Release-Gate Appendix

**Project:** ClauseSift  
**Phase:** 2 — Exact Retrieval MVP  
**Status:** Normative Phase 2 implementation-plan appendix  
**Primary design authority:** `docs/design.md` Section 29.4  
**Companion plan:** `docs/implementation/phase-2-exact-retrieval-mvp.md`

## 1. Purpose

This appendix maps the current design's initial quality gates to the capabilities implemented by Phase 2.

Phase 2 owns exact/lexical seed retrieval, the canonical evidence vocabulary/classifications, required context, material-conflict compilation/runtime preservation, deterministic citations, strict ordinary Evidence Packages, and the basic Python/CLI/MCP evidence surfaces. All current-design gates for those capabilities are therefore Phase 2 blocking gates.

Phase 2 does not own Phase 3 dense/RRF gates or Phase 4 reranker/supporting-context/high-accuracy gates. In particular, `optional-context precision` remains a later high-accuracy/supporting-context gate rather than a Phase 2 ordinary required-context gate.

No implementation-plan document may replace the design's exact gate type or threshold with a locally invented stronger/weaker metric.

## 2. Evaluation-data separation

Phase 2 uses the Phase 0 versioned evaluation corpus and keeps development/model-selection evidence separate from decisive release-gate evidence.

Before a decisive probabilistic gate run, freeze every behavior-bearing input relevant to that gate and record:

- candidate identity/hash;
- corpus/split/label versions;
- reviewer/adjudication evidence where required;
- applicable sample/stratum counts;
- exact metric/gate target.

Observed decisive data cannot be reused as fresh authorization for a behavior-bearing changed candidate; `phase-2-held-out-retry-policy.md` defines retirement/reproduction rules.

Deterministic zero-failure gates use the complete versioned deterministic conformance suite named by the design. They are count gates over that complete suite, not claims that a finite confidence interval proves population perfection.

## 3. Exact clause lookup gate

Blocking design gate:

> **Exact clause lookup success: zero failures across the complete versioned deterministic lookup suite.**

The suite must cover at minimum:

- exact `document_id` and clause resolution;
- complete Section 14.1 exact-lookup source set;
- no fuzzy clause substitution;
- no cross-edition/same-number substitution;
- deterministic source/chunk ordering;
- absent document/clause not-found routing.

Report complete suite size and every failure.

## 4. Retrieval gates

After lexical candidate selection is complete and frozen, run the current probabilistic evidence-presence gates on independently labelled applicable cases.

### 4.1 Recall@20

- one-sided 95% Wilson lower confidence bound **>= 98%**;
- at least **150** applicable independently labelled cases;
- larger stratified samples when a critical query family/hard negative would otherwise be underrepresented.

### 4.2 Top-5

- one-sided 95% Wilson lower confidence bound **>= 95%**;
- at least **60** applicable independently labelled cases;
- larger stratified samples as required by the design.

For every result report numerator, denominator, point estimate, one-sided lower bound, target, split/corpus/label versions, exclusions, and frozen lexical configuration identity.

A lower bound below target blocks activation and does not authorize tuning against the observed decisive split.

## 5. Citation and version-selection gate

Blocking design gate:

> **Document, edition, clause, and page citation accuracy: zero failures across the complete versioned deterministic citation suite.**

The suite validates executable equality against the active catalog/source lineage, including:

- exact document/edition/source identity;
- clause projection;
- page start/end;
- source-span/page-span intersections;
- available bounding-box projection;
- deterministic citation string;
- no source/page fabrication when boxes are incomplete.

Wrong-edition or wrong-source citation is always blocking.

## 6. Unsupported deterministic conclusions gate

Blocking design gate:

> **Unsupported deterministic conclusions in the golden set: zero observed failures.**

Phase 2 evidence/adapter behavior must not turn retrieval rank, document authority, recency, source modality, conflict score, or attachment into a deterministic engineering/legal conclusion unsupported by the source/approved metadata/rules.

This gate complements, rather than replaces, the vocabulary/conflict/precedence negative suites below.

## 7. Required-context traversal conformance gate

Blocking design gate:

> **Required context, lineage paths, source status, and deterministic ordering: zero failures across the complete versioned traversal conformance suite.**

The complete suite must exercise the current Phase 2 required rules and runtime contract, including:

- `applies_subject_to` forward;
- `depends_on` forward;
- reverse/forward `exception_to`;
- `defines` governing scope;
- table row -> containing table/nearest addressable clause;
- note/footnote -> qualifying parent;
- exact metadata-only empty `context_targets`;
- reconvergent independent paths;
- path-state ordering/deduplication;
- source/edition/status preservation;
- graph/conflict fixed-point composition;
- exact current structural/semantic/object/path/step bounds;
- `context_limit_exceeded` with no partial required Evidence Package.

Report the complete suite size and every failure.

## 8. Traversal negative gate

Blocking design gate:

> **Prohibited, unresolved, guessed, or wrong-edition traversal: zero accepted edges across the complete versioned negative suite.**

Fixtures include:

- unresolved occurrence followed by guessed clause/document text;
- ambiguous target followed anyway;
- wrong endpoint category;
- source-text `supersedes`/`amends` without manifest authority;
- invalid cycle admitted as navigable;
- wrong-edition same clause label;
- similarity-based graph target invention;
- unclassified node used as a typed endpoint it cannot satisfy.

Every accepted prohibited edge blocks release.

## 9. Vocabulary/schema deterministic gate

Blocking design gate:

> **Core vocabulary/schema, document-dimension separation, classification provenance/inheritance, public round trip, legacy-alias rejection, unsupported-version rejection, and extension-isolation conformance: zero failures across the complete deterministic vocabulary suite.**

This gate remains distinct from probabilistic semantic classification accuracy.

## 10. Classification probabilistic gates

Evaluate each field independently on its applicable independently labelled classification corpus:

1. `node_type` accuracy — one-sided 95% Wilson lower bound **>= 98%**;
2. `normative_status` accuracy — one-sided 95% Wilson lower bound **>= 98%**;
3. `source_modality` accuracy — one-sided 95% Wilson lower bound **>= 98%**.

Each 98% gate requires at least **150** applicable independently labelled cases, expanded when a classification field/origin/inheritance branch/document/node family/language/ambiguity/hard negative would otherwise be underrepresented.

Counts cannot be pooled across fields.

## 11. Classification/source-authority negative gate

Blocking design gate:

> **Zero occurrences** across the complete negative suite of:
>
> - `unclassified`/`unknown` promoted to a stronger classification;
> - informative material promoted by attachment/ranking;
> - source modality reported as project-specific legal force.

This applies through the final Evidence Package/adapters, not only catalog construction.

## 12. Conflict-candidate recall gate

Phase 2 owns build-time conflict candidate generation under current design, so the design's conflict-candidate recall gate is Phase 2 blocking.

- one-sided 95% Wilson lower confidence bound **>= 95%**;
- at least **60** applicable independently labelled cases;
- larger stratified samples when conflict dimension/detector/hard-negative coverage would otherwise be inadequate.

A model-only future detector is not needed to satisfy Phase 2; evaluate the admitted current deterministic/human-input candidate mechanisms.

## 13. Conflict precision gates

Evaluate the applicable conflict families separately.

### 13.1 Confirmed/unresolved conflict precision

For each reported state family covered by the release corpus:

- one-sided 95% Wilson lower confidence bound **>= 98%**;
- at least **150** applicable independently labelled cases per 98% gate, expanded for critical strata.

### 13.2 Explained-difference precision

For each reported explanation-code family covered by the release corpus:

- one-sided 95% Wilson lower confidence bound **>= 98%**;
- at least **150** applicable independently labelled cases per 98% gate, expanded as necessary.

Always report numerator, denominator, point estimate, lower bound, target, state/code family, split/corpus/reviewer identity, and frozen conflict rule/configuration identity.

## 14. Deterministic conflict completeness and precedence gate

Blocking design gate:

> **Conflict position/source/lineage completeness, all-side runtime preservation, state/dimension ordering, and trusted-precedence serialization: zero failures across the complete deterministic conflict conformance suite.**

The complete suite includes:

- content-addressed conflict/position IDs;
- exact spans/source ownership;
- required-context projection;
- deterministic decision artifact binding;
- canonical per-position source cover;
- n-ary conflict ordering;
- runtime span-intersection discovery;
- every material side present regardless of seed rank/filter;
- required context of newly attached sides;
- graph/conflict least fixed point;
- exact `conflicts` array and assembly reasons;
- encoded precedence only through an approved rule;
- all current conflict limits and no-partial overflow behavior.

Report complete suite size and every failure.

## 15. Conflict negative gate

Blocking design gate:

> **Zero occurrences** across the complete negative suite of:
>
> - explained exception/version/jurisdiction/scope/unit/modality cases misreported as confirmed conflict;
> - unresolved or model-only candidates promoted without admissible review;
> - winner selection without encoded precedence.

Also reject any `potential` conflict in an admitted runtime release.

## 16. Evidence Package and interface conformance

Phase 2's ordinary evidence path must pass deterministic conformance for:

- strict root/item/lineage/context-target/conflict/warning schemas;
- `additionalProperties: false` behavior;
- exact source/catalog projections;
- immutable source/build lineage plus request-scoped assembly lineage;
- no fabricated empty-node source evidence;
- context/conflict completeness states/errors;
- Python/CLI/MCP semantic equivalence;
- canonical resource contracts;
- public-field redaction/path safety.

A mismatch that changes or drops required evidence semantics is blocking.

The source resource remains a separate raw-source contract; it is not an Evidence Package wrapper.

## 17. MCP/protocol/admission/cancellation conformance

Existing Phase 2 MCP appendices remain blocking for the now-expanded evidence tools, including:

- both supported protocol revisions;
- strict input/output schemas;
- 1,048,576-byte inbound complete-frame limit;
- 65,536-byte canonical arguments budget;
- 1,048,576-byte non-page output limit;
- 33,554,432-byte page output limit;
- 67,108,864-byte page working-set budget;
- `max_in_flight_requests` 1..1024;
- cancellation/deadline atomic terminal state;
- late-result suppression;
- resource URI canonicality;
- safe diagnostic routing/redaction.

Traversal/conflict work gets no exemption from these bounds.

## 18. Phase 2 complete quality gate

A candidate release may activate only when every applicable Phase 2 gate passes:

- manifest/source/approval integrity;
- parser/comparison/OCR release policy;
- canonical/page/chunk/catalog integrity;
- exact lookup zero-failure suite;
- Recall@20 Wilson LB >= 98%;
- Top-5 Wilson LB >= 95%;
- citation/version-selection zero-failure suite;
- unsupported deterministic conclusion zero-failure gate;
- required-context/path/status/order zero-failure suite;
- prohibited/guessed traversal zero-accepted-edge suite;
- vocabulary/schema deterministic zero-failure suite;
- three 98% classification Wilson gates;
- classification/source-authority negative zero-occurrence suite;
- conflict-candidate recall Wilson LB >= 95%;
- confirmed/unresolved conflict precision Wilson LB >= 98% for each applicable family;
- explained-difference precision Wilson LB >= 98% for each applicable code family;
- deterministic conflict completeness/all-side/precedence zero-failure suite;
- conflict negative zero-occurrence suite;
- strict Evidence Package/interface conformance;
- lineage/release/cache identity;
- MCP/protocol/admission/cancellation/security conformance;
- candidate checksum/read-only startup smoke validation;
- activation and rollback validation;
- no unresolved Phase 2 release blocker.

A missing applicable gate, insufficient applicable sample size, leakage violation, evaluation execution failure, or missing/corrupt gate report is blocking and is never interpreted as a pass.

## 19. Statistical reporting rules

For all probabilistic retrieval/classification/conflict gates:

- use independent labelled cases and one-sided 95% Wilson intervals;
- require at least 150 applicable cases for each 98% gate;
- require at least 60 applicable cases for each 95% gate;
- increase samples when a critical query/classification/context-rule/conflict dimension/state/hard negative would otherwise be underrepresented;
- never report a percentage without numerator and denominator;
- fail when the lower bound misses target.

The deterministic 100%/zero-failure gates report complete suite size and every failure rather than a confidence interval.

## 20. Human-review reliability

Where a Phase 2 metric depends on semantic human labels, preserve the design's blinded-review/adjudication policy:

- initial release-gate items receive two blinded independent reviewers;
- later releases use the design's preregistered stratified second-review coverage plus every failure/uncertain case;
- calibration set is versioned, blinded, excluded from product metrics, and covers every rubric category as required;
- agreement/kappa/fallback rules follow Section 29.3 exactly;
- failed reliability blocks the affected semantic gate;
- an LLM may assist analysis but cannot be the sole gate authority.

## 21. Retry/retirement governance

`phase-2-held-out-retry-policy.md` governs decisive probabilistic evidence for retrieval/classification/conflict candidate/precision families.

Once a decisive split's labels/results are observed:

- identical-candidate replay is reproduction-only;
- a behavior-bearing changed candidate cannot claim fresh authorization from that observed split;
- remediation returns to development/model-selection/review data;
- later decisive authorization requires fresh preregistered evidence under Phase 0 governance;
- reserve/campaign use is finite and cannot become stop-on-pass cherry-picking.

Deterministic conformance suites are versioned executable suites rather than hidden probabilistic held-out samples; changes to their expected contract must be reviewed/versioned rather than silently edited to make a candidate pass.

## 22. Failure injection

Inject and verify correct non-activation/no-partial behavior for at least:

- each probabilistic lower-bound failure;
- insufficient probabilistic sample size;
- decisive-data leakage;
- exact lookup/citation wrong edition;
- required-context/path/order failure;
- prohibited guessed traversal;
- required closure overflow;
- vocabulary/classification negative failure;
- stale/invalid conflict decision;
- incomplete position source cover;
- unresolved critical conflict;
- one-sided conflict result;
- false precedence selection;
- conflict precision/recall gate failure;
- strict Evidence Package schema/projection mismatch;
- Python/CLI/MCP semantic mismatch;
- source-resource payload/MIME mismatch;
- release/lineage/artifact corruption;
- output/admission budget violation;
- cancellation/deadline late success;
- missing/corrupt gate report.

For every release-time failure the candidate is not activated and the previous active release remains unchanged.

## 23. Corrected execution order

The evaluation/release portion of Phase 2 is:

1. complete/freeze canonical catalog, graph, context, conflict, lineage, lexical, and serializer contracts;
2. select/freeze lexical configuration on non-decisive data;
3. freeze classification behavior;
4. freeze conflict candidate/classifier/explanation behavior;
5. run all complete deterministic exact/citation/traversal/vocabulary/conflict/evidence/MCP conformance suites;
6. validate decisive split/reviewer/candidate identities;
7. run retrieval Wilson gates;
8. run three classification Wilson gates;
9. run conflict candidate-recall and applicable conflict precision Wilson gates;
10. persist raw results and complete deterministic-suite reports;
11. enforce every blocker;
12. finalize static decision/review report;
13. assemble/checksum/reopen the immutable candidate release;
14. run independent startup/read-only smoke validation;
15. validate rollback;
16. atomically activate only after every preceding step passes.

Decisive probabilistic evidence is a gate, not an optimizer.

## 24. Acceptance criteria

Phase 2 is not complete unless:

1. every current-design Phase 2 deterministic gate passes with zero failures/zero prohibited occurrences as specified;
2. retrieval and classification Wilson gates meet the exact thresholds/sample rules;
3. conflict-candidate recall and conflict precision Wilson gates meet the exact thresholds/sample rules;
4. strict Evidence Package and interface conformance passes;
5. protocol/admission/cancellation/security conformance passes;
6. decisive probabilistic evidence is leakage-safe and retirement-governed;
7. missing/failed evidence blocks activation while preserving the previous release;
8. no Phase 3 dense/RRF or Phase 4 reranking/supporting-context quality gate is misclassified as Phase 2.
