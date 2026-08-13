# Phase 2 Release-Gate Appendix

**Project:** ClauseSift  
**Phase:** 2 — Exact Retrieval MVP  
**Status:** Normative Phase 2 implementation-plan appendix  
**Primary design authority:** `docs/design.md`  
**Current-design correction:** `docs/implementation/phase-2-current-design-correction.md`

## 1. Purpose and scope

This appendix defines the evaluation-data separation, blocking quality gates, evidence-semantics gates, activation rules, and failure-injection requirements for the current-design Phase 2 Exact Retrieval MVP.

Phase 2 gates the capabilities it now owns:

- exact clause retrieval;
- lexical retrieval;
- canonical `node_type` classification;
- canonical `normative_status` classification;
- canonical `source_modality` classification;
- deterministic citations/page projections;
- required Evidence Graph context closure;
- material-conflict closure;
- strict ordinary Evidence Package assembly;
- shared Python/CLI/MCP exact/lexical evidence behavior;
- immutable release integrity, activation, and rollback.

This appendix does **not** add Phase 3 embedding/vector/RRF gates or Phase 4 cross-encoder reranking/supporting-context/high-accuracy gates.

Accuracy remains first. A candidate may not activate merely because lexical Recall@K passes if its final ordinary Evidence Package can omit required applicability, exception, table, or material-conflict evidence.

## 2. Evaluation-data separation

Phase 2 consumes the Phase 0 versioned corpus/split manifests and keeps roles distinct.

- **development diagnostics** — reusable during implementation and debugging;
- **benchmark/model-selection** — used to select lexical engine/tokenizer/configuration and other candidate choices that require comparison;
- **held-out/final release evidence** — observed only after the complete applicable Phase 2 behavior-bearing candidate is frozen;
- **calibration/human-review material** — governed by the Phase 0 review methodology and never silently reused as product-metric tuning data.

An item cannot be moved from decisive held-out evidence into development/benchmark data after its output is observed.

Any label/split correction must follow Phase 0 change control and preserve an auditable version history.

Before every decisive run validate:

- split identity and content hash;
- non-overlap requirements;
- label/reviewer/adjudication version;
- complete frozen Phase 2 candidate/rule/release identity;
- applicable sample/stratum counts;
- absence of forbidden prior observation.

A missing or invalid split-integrity record is blocking.

## 3. Frozen Phase 2 candidate identity

Before decisive evidence is observed, freeze every behavior-bearing input needed by the applicable gates.

At minimum bind:

- approved manifest/source corpus identity;
- parser route and parser-validation configuration;
- canonical model/chunk/page-provenance schemas;
- evidence vocabulary and classification rules/review artifacts;
- lexical engine/tokenizer/index/query-compiler configuration;
- exact lookup rule/schema identity;
- relationship occurrence/edge identity schemas and resolver configuration;
- required-context rule-set/configuration and all context bounds;
- material-conflict detector/classifier/decision/cover configuration;
- central Evidence Package schema/serializer version/configuration;
- warning/error routing configuration where behavior-bearing;
- relevant dependency-lock/toolchain identity;
- release/build artifact hashes needed by the design.

A behavior-bearing change to any gate family creates a new candidate for that family and invalidates stale decisive evidence where the result could change.

## 4. Lexical selection and release gating

### 4.1 Candidate selection

Lexical engine/tokenizer/field-weight/query-compiler selection uses development + benchmark/model-selection data only.

Compare candidates using accuracy first, including:

- Recall@5/10/20;
- MRR/nDCG as secondary diagnostics;
- exact-token preservation;
- document/edition/clause/page hit behavior;
- table evidence;
- English/Chinese/cross-language strata;
- punctuation/identifier/number/unit cases;
- hard negatives;
- index size/build/load/query cost only after correctness.

Freeze the selected lexical identity before held-out gating.

### 4.2 Blocking lexical gates

On applicable independently labelled held-out cases:

- Recall@20: one-sided 95% Wilson lower bound **>= 98%**;
- Top-5: one-sided 95% Wilson lower bound **>= 95%**.

Minimum sample rules remain:

- at least 150 applicable cases for each 98% gate;
- at least 60 applicable cases for each 95% gate;
- larger samples when required strata would otherwise be underrepresented.

Report numerator, denominator, point estimate, one-sided lower bound, target, pass/fail, split/corpus/label versions, exclusions, and frozen lexical identity.

A held-out lexical failure blocks activation and does not authorize tuning against the observed split.

## 5. Classification gates

Phase 2 constructs and admits all three canonical classification fields:

- `node_type`;
- `normative_status`;
- `source_modality`.

Develop deterministic rules/reviews on non-decisive data, then freeze:

- vocabulary version/hash;
- classification schema;
- rule/inheritance configurations;
- immutable human-review artifacts where used.

Evaluate independently on applicable held-out classification cases:

1. node-type accuracy — one-sided 95% Wilson lower bound **>= 98%**;
2. normative-status accuracy — one-sided 95% Wilson lower bound **>= 98%**;
3. source-modality accuracy — one-sided 95% Wilson lower bound **>= 98%**.

Each gate needs at least 150 applicable independently labelled cases, expanded for underrepresented origins, inheritance branches, document/node families, languages, ambiguities, and critical hard negatives.

Counts are not pooled across fields.

Probabilistic gates do not replace deterministic conformance, provenance, alias-rejection, unsupported-version, or no-unsupported-promotion checks.

## 6. Exact clause and citation gates

Phase 2 must pass deterministic and independently reviewed end-to-end fixtures proving:

- exact `document_id` + clause resolves only the exact manifested edition;
- the complete Section 14.1 exact-lookup source set is returned as direct seeds;
- no fuzzy clause/edition substitution occurs;
- every source citation matches canonical document/edition/clause/page projections;
- page spans/boxes reproduce the validated source contribution;
- partial-node chunks do not claim the rest of a node;
- unavailable optional boxes remain visible as coordinate incompleteness rather than fabricated coordinates.

Any wrong-edition or wrong-clause substitution is blocking.

## 7. Relationship and required-context deterministic gates

Before activation, run release-validation and runtime fixtures for every current required traversal rule, including:

- `applies_subject_to` forward;
- `depends_on` forward;
- reverse/forward `exception_to` behavior;
- `defines` governing scope;
- `table_row` -> containing table/nearest clause;
- note/footnote -> qualifying source-bearing parent;
- unresolved required references/classification/table structure;
- empty structural targets;
- reconvergent independent paths;
- permitted semantic cycles with deterministic warning;
- release-invalid structural/governing/version cycles;
- actual 64 structural / 8 required-semantic depth behavior;
- 128 object / 32 paths-per-object / 1,024 accepted-step bounds;
- `context_limit_exceeded` with no partial package for required overflow.

Release validation must independently prove the largest single required graph+conflict closure addressable by `get_clause` fits every configured bound.

Failure of any required-context deterministic fixture blocks activation.

## 8. Held-out required-context completeness gate

Phase 2 now owns the ordinary context-complete evidence path. Therefore it requires decisive independently reviewed context evidence in addition to lexical Recall@K.

For every applicable held-out context case define the complete expected **required** obligations: direct seed(s), required source-backed targets, metadata-only required targets, and required relationship/path class where relevant.

The blocking release rule is:

> **Zero known omissions of required context on the complete applicable decisive held-out context set.**

A case fails when the final ordinary Evidence Package:

- omits a required parent/applicability/dependency/definition/exception/table target;
- substitutes the wrong document/edition/node;
- fabricates source text for an empty target;
- reports `complete` despite a known required omission;
- silently truncates required context;
- drops a required independent path when that loss changes the design-required assembly record;
- uses an unvalidated edge or guessed target.

Report at minimum:

- applicable case count;
- passed/failed count;
- each omission category;
- corpus/split/label/reviewer identity;
- context rule/configuration identity;
- release/candidate identity.

This zero-omission gate is deterministic over the reviewed expected set; it is not replaced by a Wilson aggregate that could hide one known correctness failure.

## 9. Conflict build/release deterministic gates

Run fixtures covering the complete Section 20.3 lifecycle and source-cover algorithm:

- confirmed numeric incompatibility;
- compatible stricter minima/maxima;
- exact unit equivalence;
- typed exception explanation;
- amendment/supersession explanation;
- disjoint trusted applicability explanation;
- unresolved missing applicability;
- unresolved critical-tier release block;
- standard-only unresolved admission + warning;
- n-ary conflict;
- content-addressed conflict/position IDs;
- stale decision-artifact rejection;
- exact canonical position source covers;
- scope-contained source preference;
- broader-source fallback only when required;
- independent release recomputation.

Any `potential` candidate in an admitted runtime release is blocking.

## 10. Held-out material-conflict completeness gate

For every applicable independently reviewed decisive conflict case, define all material positions/sides that the ordinary result must preserve.

The blocking release rule is:

> **Zero known omissions of any material confirmed/unresolved conflict position or required source cover on the complete applicable decisive held-out conflict set.**

A case fails when the final result:

- returns only the higher-ranked side;
- omits a position/source because it did not satisfy the direct metadata filter;
- misses a conflict introduced by newly attached required context;
- omits required context of a newly attached conflict side;
- serializes an incomplete `conflicts` record;
- silently chooses precedence not encoded by an approved rule;
- reports success after a required conflict bound overflow.

Keep confirmed and unresolved expectations separately visible in the report.

## 11. Evidence Package serialization gates

The central serializer must pass strict conformance for the current closed schemas.

Validate at minimum:

- root properties and `additionalProperties: false` behavior;
- evidence source/catalog identity;
- exact original text and citation/page projections;
- complete classification records/provenance;
- immutable source/build lineage;
- request-scoped assembly lineage;
- direct retrieval record channels/ranks/scores appropriate to Phase 2;
- exact selection roles and seed IDs;
- context completeness;
- context paths/step edge provenance;
- metadata-only context targets;
- material conflict projection;
- warning schema/order;
- no absolute path/credential/internal mutable locator leakage;
- output/frame-size limits.

Any serializer disagreement with the active release/catalog is blocking.

## 12. Cross-interface equivalence gate

For the same active release and normalized request, the shared Python, CLI machine-readable, and MCP paths must produce semantically identical evidence behavior.

Test at minimum:

- no-match search;
- exact clause;
- lexical search with filters;
- required applicability/exception/table context;
- conflict closure;
- unresolved required warning;
- context-limit error;
- context inspection;
- metadata/list/page operations.

Transport/format wrappers may differ; evidence semantics may not.

A CLI/MCP adapter that omits a warning, context target, conflict side, source identity, or typed error fails the gate.

## 13. Protocol/admission/cancellation gates

Existing Phase 2 MCP protocol/admission appendices remain blocking for:

- JSON-RPC framing;
- strict request/output schemas;
- frame budgets;
- `max_in_flight_requests`;
- page working-set reservation;
- cancellation/deadline terminal-state atomicity;
- late-result suppression;
- stable advertised capability lists;
- authorized resource URI parsing.

The new evidence operations must pass the same concurrency/budget/terminal-state tests; they are not exempt because traversal is more complex.

## 14. Phase 2 complete quality gate

A candidate may activate only when **all** applicable gates pass, including:

- manifest/source/approval;
- parser/comparison/OCR policy;
- canonical/page/chunk/catalog integrity;
- exact lookup/citation;
- lexical Recall@20 Wilson LB >= 98%;
- lexical Top-5 Wilson LB >= 95%;
- node-type Wilson LB >= 98%;
- normative-status Wilson LB >= 98%;
- source-modality Wilson LB >= 98%;
- relationship resolution/release-tier policy;
- required-context deterministic conformance;
- zero held-out required-context omissions;
- conflict deterministic conformance;
- zero held-out material-conflict-side omissions;
- strict Evidence Package serialization;
- Python/CLI/MCP equivalence;
- lineage/release/cache identity;
- protocol/admission/cancellation/security tests;
- static/evaluation reports;
- candidate checksum/read-only smoke validation;
- activation and rollback validation;
- no unresolved Phase 2 blocker.

A missing applicable gate, missing/insufficient reviewed evidence, leakage violation, execution failure, or corrupt/missing report is blocking and is never interpreted as a pass.

Only genuine Phase 3/Phase 4 metrics remain `not_implemented_in_phase_2`.

## 15. Required reports

The Phase 2 decision package must distinguish:

- lexical selection evidence;
- frozen lexical identity;
- held-out lexical gates;
- classification development/review identity;
- held-out classification gates;
- required-context rule/release identity;
- deterministic context conformance;
- held-out required-context completeness results;
- conflict detector/rule/decision/cover identity;
- deterministic conflict conformance;
- held-out material-side completeness results;
- Evidence Package serializer conformance;
- cross-interface equivalence;
- leakage/split-integrity validation;
- protocol/admission/cancellation results;
- release/lineage/cache validation;
- activation/rollback result;
- every blocker and waiver status (the release path must not treat an undocumented waiver as a pass).

No benchmark-selection result may be relabelled as independent final release evidence.

## 16. Split/retry governance for new gate families

The original Phase 2 retry policy was written primarily for lexical/classification gates. The current implementation must explicitly apply leakage-safe decisive-evidence governance to the new context/conflict/evidence gate families.

Before decisive observation, preregister:

- campaign ID;
- complete applicable frozen candidate identity;
- decisive split/version/hash;
- gate family and expected labels;
- review/adjudication policy;
- applicable case/stratum counts.

After a decisive split is observed:

- retain the result permanently;
- an identical-candidate replay is reproduction/diagnostic only;
- a behavior-bearing changed candidate cannot claim independent authorization from the already observed split;
- remediation uses development/review material and then genuinely fresh preregistered decisive evidence according to Phase 0 governance.

The implementation must not create an unbounded stop-on-pass sequence of fresh reserves.

## 17. Failure injection

Inject and verify non-activation/no-partial-success behavior for at least:

- each of the five probabilistic gate failures;
- insufficient sample size;
- decisive-data leakage;
- exact wrong-edition lookup;
- citation/page mismatch;
- unresolved critical reference;
- required-context omission;
- required-context bound overflow;
- stale/invalid conflict decision;
- incomplete conflict source cover;
- unresolved critical conflict;
- one-sided conflict result;
- graph/conflict fixed-point overflow;
- missing context target;
- closed-schema serialization mismatch;
- Python/CLI/MCP semantic disagreement;
- corrupt lineage/catalog/retrieval/context/conflict artifact;
- output budget overflow;
- cancellation/deadline late-success race;
- missing/corrupt gate report.

For every release-time failure:

- candidate activation does not occur;
- previous active release remains unchanged;
- diagnostic/report evidence remains available.

## 18. Corrected execution order

The evaluation/release portion of Phase 2 is:

1. complete/freeze canonical catalog, relationships, context/conflict artifacts, and serializer contracts;
2. select lexical candidate using non-decisive data;
3. freeze lexical behavior;
4. freeze classification behavior;
5. freeze context/conflict/serializer behavior;
6. run deterministic canonical/exact/citation/relationship/context/conflict/serializer tests;
7. run split-integrity validation;
8. run decisive lexical gates;
9. run decisive classification gates;
10. run decisive required-context completeness gate;
11. run decisive material-conflict completeness gate;
12. run Python/CLI/MCP equivalence and protocol/admission/cancellation suites;
13. persist raw evaluation/gate reports;
14. enforce every Phase 2 blocker;
15. finalize static review/decision package;
16. assemble/checksum/reopen the immutable candidate release;
17. run independent startup/read-only smoke validation;
18. validate rollback path;
19. atomically activate only after every prior step passes.

Decisive held-out evidence is a gate, never an optimizer.

## 19. Acceptance additions

Phase 2 is not complete unless:

1. lexical selection and decisive lexical evidence are separated;
2. all five probabilistic lexical/classification gates pass with required samples;
3. exact lookup/citation fixtures are edition/source correct;
4. required-context deterministic conformance passes;
5. the decisive context set has zero known required omissions;
6. material-conflict deterministic conformance passes;
7. the decisive conflict set has zero known material-side omissions;
8. strict Evidence Package conformance passes;
9. Python/CLI/MCP semantics are equivalent;
10. protocol/admission/cancellation bounds pass for the evidence tools;
11. split/leakage/retry governance covers the newly owned gate families;
12. missing/failed evidence prevents activation while preserving the prior release.

These gates are Phase 2-scoped because they validate the ordinary exact/lexical evidence capabilities Phase 2 now constructs and advertises.
