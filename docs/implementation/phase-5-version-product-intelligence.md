# Phase 5 Implementation Plan: Version and Product Intelligence

**Project:** ClauseSift  
**Phase:** 5 — Version and Product Intelligence  
**Status:** Canonical implementation plan  
**Primary design authority:** `docs/design.md`  
**Product intent:** `docs/design-brief.md`  
**Design principles:** `docs/design-principles.md`

## 1. Objective

Phase 5 implements the final current-design intelligence layer named by `docs/design.md` Section 35:

1. edition comparison;
2. clause mapping across editions;
3. structured product parameters;
4. comparison of standard requirements and manufacturer specifications.

Phase 5 builds on the source-grounded Evidence Graph and retrieval/release contracts established by Phases 0–4. It does not create a generated-answer system and does not transfer source authority to a model.

## 2. Design boundary

Phase 5 consumes, without redefining:

- canonical document, edition, clause, node, chunk, source, relationship, and lineage identity;
- `supersedes` and `amends` relationships and all existing status/edition rules;
- exact/lexical/hybrid/high-accuracy retrieval;
- required-context and material-conflict closure;
- immutable releases, deterministic build identity, validation, activation, rollback, and audit rules;
- the closed Evidence Package and warning/error contracts;
- current human-review, held-out, security, performance, and reproducibility requirements.

Phase 5 must not:

- merge two editions into one canonical document identity;
- infer legal force, precedence, applicability, or controlling requirements from similarity;
- silently treat semantically similar clauses as mapped;
- convert generated product summaries into source facts;
- overwrite manufacturer statements with standard requirements or vice versa;
- treat a model score as evidence confidence;
- add public fields or tools whose schemas are not frozen by the design.

## 3. Public-interface prerequisite

`docs/design.md` Section 22.2 currently lists future tools including:

- `compare_document_versions`;
- `search_product_specifications`;
- `get_product_parameter`.

Their complete public input/output schemas are not yet frozen in the same way as the existing Section 22.1 tool surface.

Therefore Phase 5 implementation may build and validate the internal version/product services and release artifacts described here, but a new public Python/MCP/CLI surface must not ship until `docs/design.md` explicitly freezes the relevant schema, limits, warnings/errors, and cross-interface behavior.

This is a contract prerequisite, not permission to invent an implementation-plan-only public API.

## 4. Phase 5 architecture

The Phase 5 build path is:

```text
validated lower-phase release inputs
  -> edition-family registration
  -> deterministic comparison candidate generation
  -> clause-mapping candidate generation
  -> exact/rule-based comparison and mapping
  -> reviewed semantic mapping decisions where needed
  -> product-parameter extraction and normalization
  -> standard/manufacturer comparable-value projection
  -> deterministic conflict/difference classification
  -> Phase 5 validation and evaluation
  -> immutable Phase 5 release artifacts
```

At runtime, Phase 5 services read only the active immutable release. Runtime requests do not create or mutate mappings, parameters, or comparison decisions.

## 5. Edition families

Edition comparison starts only from explicitly related documents.

An edition family is established from reviewed document identity and version relationships already admitted by the canonical catalog, including exact document code/family identity and approved `supersedes`/`amends` relationships.

Do not create an edition family from title similarity, embedding similarity, filename similarity, or matching clause numbers alone.

Every edition-family record remains release-scoped and preserves the original `document_id`, edition, status, source hash, and source lineage of each member.

## 6. Edition comparison

Edition comparison reports source-grounded differences between two explicitly selected editions without choosing which edition governs a project.

The comparison engine should classify deterministic source differences such as:

- unchanged source-backed content;
- exact text change;
- added or removed clause/node;
- changed source modality;
- changed numeric value or unit after exact declared normalization;
- changed applicability/scope relationship;
- changed exception, note, table, or cross-reference structure;
- amendment/supersession relationship already encoded by the source/manifests;
- mapping unavailable or unresolved.

A difference is not automatically a material conflict. Existing Section 20.3 conflict rules remain authoritative for conflict classification.

## 7. Clause mapping across editions

Clause mapping is a reviewed relationship between canonical nodes in two editions. It is not identity reuse.

Each mapping retains:

- source and target `document_id`;
- source and target canonical node identity;
- exact source spans/hashes used by the mapping decision;
- mapping kind;
- decision origin;
- rule/model configuration identity when applicable;
- immutable review artifact identity for human-reviewed semantic decisions;
- mapping-schema version.

The initial mapping kinds should remain a closed internal enum such as exact continuation, renumbered continuation, split, merged, replaced, removed, added, and unresolved. Any public exposure of these values requires the public-schema prerequisite in Section 3.

## 8. Mapping authority

Deterministic mappings may be accepted only when exact structural/version rules prove them.

Examples include:

- explicitly encoded amendment/supersession relation plus exact unchanged canonical source hash;
- deterministic renumbering proven by reviewed source metadata and exact source identity;
- one-to-one structural continuation proven by a versioned rule whose required inputs are all source-grounded.

Semantic similarity may generate mapping candidates but cannot finalize a mapping. Non-deterministic split/merge/reworded mappings require immutable reviewed decisions under the repository's human-review policy.

No mapping may erase the original clause/node identity in either edition.

## 9. Structured product parameters

Product parameters are source-grounded structured projections of manufacturer evidence.

A parameter record must preserve:

- exact manufacturer document and edition/model identity;
- source node/source ID and source span hash;
- product model identifier when source-backed;
- parameter key from a versioned controlled registry;
- exact source value text;
- normalized comparable value only when a declared deterministic normalizer supports it;
- exact unit and canonical unit when conversion is supported;
- applicability/operating condition needed to interpret the value;
- extraction/normalization rule identity;
- source/build lineage.

Unknown, ambiguous, range, conditional, multi-value, or non-convertible values remain explicit rather than being guessed into a scalar.

## 10. Product-parameter registry

Phase 5 introduces a versioned internal controlled registry for supported parameter concepts and deterministic normalization rules.

The registry must:

- use stable parameter IDs independent of display labels;
- declare allowed value types and unit dimensions;
- declare aliases only as retrieval/extraction aids, not source facts;
- identify exact normalizer/parser versions;
- fail visibly on an unsupported or ambiguous unit/value form;
- participate in release/build identity and cache invalidation.

Adding or changing a behavior-bearing parameter definition creates a new candidate/release identity.

## 11. Standard-versus-manufacturer comparison

A standard/manufacturer comparison is allowed only when both positions have a declared comparable subject and known shared applicability.

Comparison must reuse existing source modality, jurisdiction, effective interval, equipment/product class, exception, dependency, and conflict rules.

The engine may deterministically report:

- equivalent comparable values;
- manufacturer value stricter than a minimum requirement;
- manufacturer value below a minimum requirement;
- manufacturer value within or outside a permitted range;
- unit-equivalent values;
- incompatible required sets;
- applicability not proven;
- comparison not supported.

It must not infer compliance, approval, legal precedence, or project suitability beyond the exact source-backed comparison.

## 12. Relationship to material conflicts

Phase 5 does not create a second conflict engine.

Where standard/manufacturer positions meet the existing Section 20.3 material-conflict definition, the result must reference or produce the same canonical conflict semantics and all-side preservation rules.

Where positions are merely different but compatible, disjoint in applicability, recommendation-versus-requirement, or otherwise explained under current rules, Phase 5 reports the source-grounded difference without inventing a conflict.

## 13. Candidate and decision identity

Every Phase 5 comparison, mapping, and structured-parameter artifact is content-addressed from all behavior-bearing inputs.

Identity inputs include, as applicable:

- source/document/node/span hashes;
- edition/status and encoded version relationships;
- vocabulary and classification provenance;
- relationship/context configuration;
- parameter-registry version/hash;
- unit-registry version/hash;
- candidate-generation rule/model identity;
- mapping/comparison rule identity;
- immutable human-review artifact hash;
- schema version.

A changed source, manifest, classification, mapping rule, parameter rule, unit rule, or review decision invalidates stale Phase 5 artifacts.

## 14. Model use

Models may assist only in candidate generation or reviewer workflow for:

- likely clause mapping pairs;
- likely parameter mentions;
- likely comparable standard/manufacturer positions.

Model output is never final authority. A model cannot directly set a mapping, source parameter value, normalized unit, applicability fact, conflict state, or precedence decision unless a future design explicitly creates such a reviewed probabilistic contract.

## 15. Release artifacts

Phase 5 should add versioned, checksummed release artifacts for its internal data rather than mutating lower-phase authority.

The detailed design must freeze exact artifact names/schemas before implementation. The implementation should keep separate logical artifacts for:

- edition-family/version-comparison data;
- clause-mapping decisions;
- structured product-parameter projections;
- Phase 5 evaluation/gate reports.

All files the runtime may open must appear in the exhaustive release artifact table with byte size, media type, and SHA-256.

## 16. Lineage and auditability

Every client-visible Phase 5 result must resolve back to existing source/build lineage.

Phase 5 derived records add only derivation/decision metadata. They never replace the original text or page citation.

For reviewed mappings or semantic product comparisons, retain reviewer-policy version, reviewer/adjudication identity, decision artifact hash, and exact candidate/source identity without putting unrestricted private notes into the public result.

## 17. Warnings and failure behavior

Phase 5 must fail visibly or return typed incomplete states for:

- unresolved clause mapping;
- ambiguous edition family;
- unsupported parameter/value/unit form;
- product model identity incomplete;
- applicability not proven;
- comparison not supported;
- stale mapping/parameter artifact;
- release-integrity mismatch.

New public warning/error codes require a design-level schema decision before exposure. Until then, internal validation/reporting must preserve the distinction without overloading unrelated lower-phase codes.

## 18. Evaluation corpus expansion

Extend the versioned evaluation corpus with independently reviewed Phase 5 cases covering:

- unchanged, renumbered, reworded, split, merged, removed, and added clauses;
- false mapping hard negatives with similar wording or identical clause numbers across unrelated editions;
- amendments and superseded editions;
- product model numbers;
- scalar, range, enum, conditional, table-derived, and unit-convertible product parameters;
- ambiguous/unsupported parameter values;
- standard/manufacturer equivalent, stricter, insufficient, incompatible, disjoint-applicability, and unresolved comparisons;
- wrong-model/wrong-edition product hard negatives.

Decisive labels follow the existing blinded human-review and held-out governance rules.

## 19. Quality gates

Phase 5 release gating must include:

- zero deterministic identity/source-lineage violations;
- zero wrong-edition or cross-family mapping acceptance in deterministic conformance fixtures;
- zero unreviewed semantic mapping decisions admitted as final;
- zero fabricated product parameter values/units/applicability;
- exact unit conversion equality for supported deterministic conversions;
- exact preservation of lower-phase Evidence Package, conflict, citation, warning, and release behavior;
- versioned semantic mapping and product-comparison quality metrics with preregistered independently reviewed decisive data;
- regression coverage for every existing lower-phase public mode.

Do not invent numeric thresholds where current design has not defined them. Any new blocking semantic threshold must be approved in `docs/design.md` before release gating depends on it.

## 20. Performance and resource reporting

Measure Phase 5 build and runtime stages under the current Section 30 reporting contract.

At minimum report separate distributions for:

- edition-family lookup;
- clause-mapping lookup;
- product-parameter lookup/search;
- standard/manufacturer comparable-set assembly;
- comparison classification;
- total tool/service latency.

For every executed runtime stage, preserve p50/p95/p99/maximum, sample count, error rate, cancellation rate, resolved mode/tool segmentation, and relevant cold/warm/model-free state.

## 21. Security and trust boundaries

Phase 5 inherits all lower-phase path, serialization, logging, MCP framing, resource, cancellation, admission, and release-integrity requirements.

Manufacturer text, model numbers, parameter labels, and source values remain untrusted source content. They must never become filenames, SQL fragments, dynamic imports, log-field names, or schema keys without deterministic validation/escaping.

## 22. Implementation sequence

1. freeze the detailed internal Phase 5 artifact schemas and controlled parameter registry in the detailed design;
2. freeze public schemas for any Section 22.2 tool promoted into Phase 5;
3. implement edition-family validation from reviewed version relationships;
4. implement deterministic edition-difference projection;
5. implement mapping candidate generation;
6. implement deterministic mapping rules and immutable human mapping review inputs;
7. implement structured product-parameter extraction/normalization;
8. implement standard/manufacturer comparable-value projection using existing applicability/conflict rules;
9. add Phase 5 release artifacts, lineage bindings, cache invalidation, and validation;
10. add internal/runtime services and only design-approved public adapters;
11. build deterministic and semantic evaluation suites;
12. run security/reproducibility/performance/regression gates;
13. assemble, checksum, reopen, smoke-test, and rollback-test the candidate release;
14. activate only after every applicable gate passes.

## 23. Definition of done

Phase 5 planning is complete when implementation has an unambiguous path to:

- compare explicitly related editions without mixing identities;
- map clauses across editions with deterministic or reviewed authority;
- expose source-grounded structured product parameters without fabricated values;
- compare standard/manufacturer comparable positions without inventing applicability, precedence, compliance, or conflict;
- preserve exact source/edition/page lineage for every result;
- invalidate stale Phase 5 decisions on every behavior-bearing input change;
- keep all lower-phase retrieval/evidence/release contracts unchanged;
- pass deterministic, semantic, security, reproducibility, performance, and rollback gates;
- expose no new public schema until the detailed design freezes it.

Phase 5 is the final current-design phase identified by Section 35. Any scope beyond these four capabilities requires an explicit design change.
