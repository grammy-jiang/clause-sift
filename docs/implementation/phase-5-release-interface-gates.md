# Phase 5 Release, Interface, and Governance Gates

**Phase:** 5 — Version and Product Intelligence  
**Status:** Normative Phase 5 implementation-plan appendix  
**Authority:** `docs/design.md` Sections 22, 24–31, 34–37  
**Companion:** `docs/implementation/phase-5-version-product-intelligence.md`

## 1. Purpose

Phase 5 adds derived version/product intelligence while preserving ClauseSift's existing authority, release, protocol, and regression guarantees.

This appendix defines the blocking gates for public-interface promotion, immutable release integration, semantic review, security, reproducibility, performance, and rollback.

## 2. Public-tool schema gate

Section 22.2 names future tools including `compare_document_versions`, `search_product_specifications`, and `get_product_parameter`, but their complete public contracts are not currently frozen.

Before any of these tools becomes public, the detailed design must define at least:

- exact method/tool name and interface ownership;
- strict input schema, closed enums, limits, defaults, and pagination/cursor rules;
- strict success result schema and field ordering/normalization rules;
- error/warning mapping and safe detail allowlists;
- release-binding and active-release semantics;
- source/page/resource references;
- cross-interface equivalence requirements;
- MCP `structuredContent`/legacy-text behavior where applicable;
- cancellation/deadline/progress behavior;
- inbound/output size limits;
- compatibility behavior for supported MCP eras.

Until that design change lands, internal services may be implemented and tested, but no adapter may publish an ad-hoc public schema.

## 3. Internal schema gate

Phase 5 also needs design-frozen internal schemas for:

- edition-family/version comparison artifacts;
- clause-mapping candidate/decision artifacts;
- product-parameter registry and materialized records;
- standard/product comparison projections;
- Phase 5 evaluation/gate reports.

Implementation begins only after these schemas and their versioning/invalidation rules are reviewed in the detailed design.

## 4. Frozen candidate identity

A Phase 5 release candidate binds every behavior-bearing input, including:

- lower-phase release ID and artifact hashes;
- Phase 5 internal schema versions;
- edition-family/version-rule configuration;
- clause-mapping candidate-generation rules/models/configurations;
- human mapping-review policy/version/artifacts;
- product-parameter registry and parser/normalizer versions;
- unit registry;
- standard/product comparable-subject rules;
- applicability/context/conflict rule identities;
- new model/dependency/toolchain identity where introduced;
- public-interface schema version when applicable;
- evaluation split/corpus/reviewer-policy identities.

A behavior-bearing change creates a new candidate identity and invalidates affected decisive evidence/caches.

## 5. Release artifact integration

Every Phase 5 runtime-opened file is immutable and appears in the exhaustive release artifact table with exact path, media type, byte size, and SHA-256.

Release assembly validates all Phase 5 artifacts before activation and records their schema/configuration identities in the existing reproducible build/release chain.

Runtime startup verifies Phase 5 artifacts before enabling Phase 5 capability. It must not partially enable a product/version feature after an integrity mismatch.

## 6. Backward compatibility

Installing a Phase 5-capable release must not change the semantics of existing Section 22.1 tools or lower-phase CLI behavior.

Regression tests prove that identical lower-phase requests retain:

- normalized fields/order;
- evidence/source/citation identity;
- context/conflict/warning behavior;
- pagination/cursor semantics;
- explicit mode behavior;
- supported MCP compatibility.

A new Phase 5 artifact may enrich only a design-approved Phase 5 service/tool; it cannot silently alter ordinary evidence retrieval.

## 7. Deterministic conformance blockers

Require zero failures across complete versioned deterministic suites for:

- edition-family identity and version relationship validation;
- source/target edition separation;
- exact deterministic mapping rules;
- mapping invalidation after source/rule/review changes;
- product model/source/span ownership;
- deterministic parameter parsing/normalization;
- exact supported unit/range/set comparison;
- standard/product subject/applicability validation;
- conflict/precedence reuse;
- source/page/lineage preservation;
- strict internal/public schema closure;
- artifact checksum/schema validation;
- lower-phase regression suites.

## 8. Semantic review gates

Semantic tasks include reworded/split/merged clause mapping, parameter concept resolution when not deterministic, and comparable-subject alignment.

They follow the existing blinded human-label/reviewer/adjudication/reliability contract.

For each semantic family, persist:

- case/split identity;
- raw independent labels;
- reviewer/calibration/adjudication identity;
- candidate identity;
- numerator/denominator and metric definition;
- stratum;
- final decision and report hash.

No LLM-only label may authorize release.

## 9. Held-out governance

Phase 5 decisive evidence follows the existing finite-campaign/retirement rules.

After a decisive split is observed:

- identical candidate replay is reproduction-only;
- changed mapping/product/comparison behavior cannot reuse the observed split as fresh authorization;
- remediation uses development/review data;
- a later changed candidate requires fresh preregistered independent evidence.

Do not repeatedly inspect unseen reserves until a favorable result appears.

## 10. No invented thresholds

Where the current detailed design defines a metric threshold, use it exactly.

Where Phase 5 introduces a new semantic metric but no release threshold exists, report the metric and evidence without inventing a blocker. A new numeric release threshold requires a reviewed detailed-design change.

Deterministic correctness/safety invariants remain zero-failure blockers regardless of semantic threshold availability.

## 11. Security gates

Phase 5 inherits all existing security controls and adds adversarial fixtures for:

- hostile product/model/parameter labels;
- malformed unit/value text;
- extremely long model identifiers and parameter values at exact bounds;
- source text resembling JSON/schema/control instructions;
- SQL/path/format-string injection attempts through source content;
- unsafe reviewer/import artifacts;
- stale or mismatched Phase 5 artifact hashes;
- cross-document/cross-model identity confusion;
- public output/log path or credential leakage.

Source-controlled strings remain data, never code/schema authority.

## 12. Dependency and licensing governance

Any new third-party model, parser, unit library, or data dependency introduced by Phase 5 must have:

- identified owner;
- pinned identity/version where behavior-bearing;
- license/usage/redistribution decision record;
- required legal/governance review;
- safe-loading/security review where applicable;
- package/profile placement consistent with existing dependency-separation rules.

An unresolved licensing/security decision blocks selection/release of that component.

## 13. Packaging gates

Phase 5 must not force optional heavy intelligence dependencies into the base runtime unless the detailed design explicitly changes packaging profiles.

Clean-install tests prove:

- base package remains installable and lower-phase runtime works;
- any new approved optional profile installs every required Phase 5 dependency;
- `all` includes the supported Phase 5 optional components;
- model-free/lower-phase startup does not import optional Phase 5-heavy dependencies;
- unavailable Phase 5 capability fails through the design-defined route rather than import traceback or implicit installation.

A new optional extra name requires design approval.

## 14. Cancellation, deadline, and progress

Every Phase 5 runtime operation uses the existing atomic terminal-state, admission, cancellation, and deadline contract.

If a Phase 5 operation triggers an approved lazy model load, MCP progress notifications follow the existing token-gated progress rule: emit only when the client supplied a progress token.

No late success may follow cancellation/deadline. No partial mutable Phase 5 state exists at runtime.

## 15. Performance reporting

For each Phase 5 public/internal runtime operation, report the Section 30 required stage distributions.

At minimum separate:

- edition-family/version artifact lookup;
- mapping candidate/decision lookup;
- product-parameter lookup/search;
- comparable-subject/applicability assembly;
- comparison classification;
- any model stage;
- total tool/service latency.

For each executed stage and total operation report p50/p95/p99/maximum, sample count, error rate, cancellation rate, and relevant tool/mode/load-state segmentation.

Quality gates precede optimization.

## 16. Resource limits

Phase 5 schemas define explicit maximums before public release for:

- compared editions/documents per request;
- mapped clause/node records returned;
- product model/filter list sizes;
- parameter records/page size;
- comparison pair counts;
- inbound argument aggregate size;
- output frame size.

The implementation reuses central bounded parsing/serialization/admission infrastructure rather than creating unbounded in-memory joins.

## 17. Failure injection

Inject at least:

- stale mapping after source edit;
- stale parameter after registry/unit-rule edit;
- edition-family mismatch;
- wrong-model attribution;
- missing source span/lineage;
- invalid normalized numeric value;
- unsupported unit;
- unreviewed semantic mapping;
- applicability missing for standard/product comparison;
- conflicting positions with dropped side;
- artifact corruption;
- public schema extra/missing property;
- deadline/cancellation during comparison/model work;
- dependency unavailable;
- rollback to a pre-Phase-5 release.

Every failure preserves the previous active release when candidate validation/activation fails.

## 18. Activation and rollback

Phase 5 candidate activation follows the existing immutable release protocol.

Before pointer switch:

1. all deterministic/semantic/security/package/performance-required reports are present;
2. every Phase 5 artifact checksum/schema is valid;
3. startup/reopen smoke validation passes;
4. lower-phase regression smoke passes;
5. Phase 5 capability smoke passes only for design-approved public/internal surfaces;
6. rollback is validated.

Activation is atomic; rollback restores the earlier release and its capability set without mutating either release.

## 19. Phase completion gate

Phase 5 implementation planning is not complete merely because documents exist.

The phase can be declared ready for implementation only when:

- every Section 35 capability has an explicit source-grounded implementation path;
- internal schemas and any promoted public tool schemas are frozen at design level;
- semantic decisions have immutable review governance;
- deterministic and semantic gate families are defined;
- release/artifact/cache invalidation is complete;
- lower-phase behavior cannot regress silently;
- security/dependency/licensing/package/performance/cancellation/rollback rules are covered.

After Phase 5, any new major capability lies outside the current Section 35 sequence and requires an explicit design change.
