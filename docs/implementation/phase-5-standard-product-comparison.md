# Phase 5 Standard-to-Product Comparison Plan

**Phase:** 5 — Version and Product Intelligence  
**Status:** Normative Phase 5 implementation-plan appendix  
**Authority:** `docs/design.md` Sections 12, 19–22, 29–31, and 35  
**Companion:** `docs/implementation/phase-5-version-product-intelligence.md`

## 1. Purpose

This appendix defines source-grounded comparison between engineering requirements and manufacturer specifications.

ClauseSift may report structured comparison evidence. It does not issue a legal compliance verdict, approve a design, or decide which source controls unless an existing approved precedence rule already does so.

## 2. Comparison positions

A comparison consumes two source-backed positions:

- a standards/code/guideline position; and
- a manufacturer/product position.

Each position retains exact document, edition/status, node/source identity, original source span/text hash, source modality/classification, page lineage, applicability context, and structured comparable value where deterministically available.

## 3. Comparable subject identity

Comparison is allowed only when both positions resolve to the same versioned comparable subject/parameter concept.

The comparable subject may come from:

- an existing exact conflict-comparison key;
- a Phase 5 product-parameter registry ID paired with a design-approved standard requirement concept;
- an explicit reviewed mapping/manifest relation.

Lexical or embedding similarity alone cannot establish comparable subject identity.

## 4. Shared applicability requirement

The engine must prove shared applicability before reporting a direct requirement-versus-product comparison.

Reuse existing source-grounded applicability dimensions, including as relevant:

- jurisdiction;
- effective interval;
- product/equipment class;
- system/application scope;
- exceptions;
- dependencies;
- operating conditions;
- edition/status boundaries.

If shared applicability is unknown, return an explicit internal `applicability_unresolved` comparison state rather than forcing a numeric or normative conclusion.

## 5. Exact numeric comparison

Numeric comparison uses the existing exact decimal/rational unit normalization contract.

Supported deterministic outcomes include:

- `equivalent`;
- `meets_minimum`;
- `below_minimum`;
- `meets_maximum`;
- `above_maximum`;
- `inside_range`;
- `outside_range`;
- `incompatible_sets`;
- `not_comparable`.

These are internal Phase 5 result classes until a public schema is approved.

## 6. Modality and authority boundary

Source modality remains explicit.

A comparison between `required`, `prohibited`, `recommended`, `permitted`, informative material, or manufacturer instructions must preserve the exact classifications and cannot synthesize a stronger modality.

A stricter manufacturer value against a recommended standard value is a source difference, not automatically a compliance result.

## 7. Existing conflict engine reuse

When two positions satisfy the existing Section 20.3 conflict criteria, Phase 5 must reuse the canonical conflict decision/state/dimension/position machinery.

Do not create a parallel Phase 5 conflict type.

In particular:

- incompatible `required` positions with known shared applicability may be confirmed conflict under existing rules;
- unit-equivalent values are explained, not conflicts;
- disjoint scope/jurisdiction/effective interval/equipment class is explained/not comparable;
- exception/amendment/supersession explanations remain governed by existing typed relationships;
- source authority or active status alone does not choose a winner.

## 8. Compliance wording prohibition

The internal service must not emit unqualified generated labels such as `compliant`, `noncompliant`, `approved`, `safe`, or `meets code` unless the detailed design later defines an exact source-grounded contract for them.

The service instead reports the source-backed relationship: for example, manufacturer value `x` versus required minimum `y` under the exact declared scope.

The AI/client remains responsible for interpretation and must preserve warnings/applicability/conflicts.

## 9. Standard requirement projection

A comparable standards position retains:

- source document/edition/status;
- canonical clause/node/source identity;
- exact modality;
- parameter/comparison subject ID;
- exact source value and normalized value where supported;
- unit;
- inequality/range semantics;
- applicability/exception/dependency context;
- source/build lineage.

No generated paraphrase substitutes for original text.

## 10. Manufacturer projection

A comparable manufacturer position uses the Phase 5 structured product-parameter record and retains:

- exact product model/document/edition;
- source value and normalized value;
- unit;
- operating/application conditions;
- manufacturer source modality/classification;
- source/build lineage.

## 11. Condition alignment

Numeric equality is insufficient when operating/application conditions differ.

The comparison engine checks source-backed conditions before comparison. Unknown or mismatched conditions produce an unresolved/not-comparable outcome unless a deterministic rule proves equivalence.

Do not extrapolate a rated value to another duty point or condition.

## 12. Multi-value and range comparison

For ranges, sets, and enumerations, use exact set/range operations under the registered type/unit rules.

Examples:

- minimum required value versus manufacturer range;
- permitted set versus manufacturer supported set;
- required category versus source-backed product category.

An empty admissible intersection under known shared applicability may feed the existing conflict engine. Partial overlap is reported exactly and not simplified into an unsupported pass/fail result.

## 13. Comparison identity

Every comparison record is content-addressed from:

- exact source and product position identities/hashes;
- comparable-subject/parameter registry identity;
- normalized comparison projection;
- applicability/context projection;
- existing conflict/rule configuration identity;
- comparison-rule version/configuration;
- schema version.

A change to either source, mapping, parameter registry, applicability, unit rule, or comparison rule invalidates stale comparison results.

## 14. Candidate generation

Search/ranking models may suggest likely comparable standard/product positions, but final comparison requires exact resolved subject identity and required source-grounded applicability.

Hard negatives include:

- same numeric value for different parameters;
- same parameter label for different equipment classes;
- wrong manufacturer model;
- wrong standard edition;
- similar but non-equivalent units/conditions;
- recommendation versus requirement;
- superseded manufacturer specification.

## 15. Runtime service

The internal runtime service operates over active immutable release artifacts and returns source-grounded comparison records plus all lower-phase warnings/conflicts needed to interpret them.

It does not mutate comparison decisions at query time.

Any future public adapter must wait for a detailed-design schema; `search_product_specifications` and `get_product_parameter` do not imply a public compliance-comparison tool unless the design adds one.

## 16. Evaluation cases

Include independently reviewed fixtures for:

- exact equivalent value with unit conversion;
- manufacturer value above a required minimum;
- manufacturer value below a required minimum;
- maximum/range requirements;
- partial set overlap;
- incompatible required sets;
- standard recommendation versus manufacturer value;
- exception-qualified requirement;
- disjoint product/equipment class;
- wrong jurisdiction/effective period;
- wrong product model/edition;
- missing operating condition;
- conflicting manufacturer documents;
- trusted existing precedence rule;
- no-precedence case;
- semantic candidate false positive.

## 17. Deterministic gates

Require zero failures for:

- wrong comparable subject accepted;
- wrong model/edition/source attribution;
- fabricated applicability/condition;
- incorrect exact unit/range/set comparison;
- existing conflict side dropped;
- unapproved precedence/winner selection;
- generated compliance verdict entering public evidence authority;
- stale comparison record reuse;
- citation/lineage/context regression.

## 18. Semantic quality reporting

For candidate comparable-pair generation and any human-reviewed subject alignment, report by stratum:

- candidate recall;
- final pair precision;
- unresolved rate;
- wrong-subject false positive rate;
- wrong-applicability false positive rate;
- wrong-model/wrong-edition false positive rate.

Use existing reviewer/reliability/held-out governance. No new blocking threshold is invented without design approval.

## 19. Failure behavior

Preserve distinct internal states for:

- no relevant product evidence;
- no relevant standard requirement;
- comparable subject unresolved;
- shared applicability unresolved;
- value/unit/condition not comparable;
- conflict unresolved;
- release-integrity failure.

Public warning/error mappings require a detailed-design contract.

## 20. Definition of done

Standard-to-product comparison is implementation-ready when every comparison is reproducible from exact source-backed positions, subject/applicability identity is proven rather than guessed, supported numeric/set operations are exact, existing conflict/precedence rules are reused, and no product compliance or legal conclusion is invented by the Phase 5 layer.
