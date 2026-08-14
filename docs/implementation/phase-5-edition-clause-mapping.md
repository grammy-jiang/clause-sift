# Phase 5 Edition Comparison and Clause Mapping Plan

**Phase:** 5 — Version and Product Intelligence  
**Status:** Normative Phase 5 implementation-plan appendix  
**Authority:** `docs/design.md` Sections 12, 19–22, 29–31, and 35  
**Companion:** `docs/implementation/phase-5-version-product-intelligence.md`

## 1. Purpose

This appendix defines how ClauseSift may compare explicitly related editions and map clauses across them without collapsing edition identity or turning similarity into authority.

## 2. Inputs

Only validated release data may participate:

- canonical document/node/source identity;
- exact edition/status metadata;
- source hashes and page lineage;
- approved `supersedes` and `amends` relationships;
- canonical structural relationships;
- source modality/classification provenance;
- required-context and material-conflict projections.

An unrelated document is never admitted because its title, clause number, or embedding is similar.

## 3. Edition-family validation

The builder constructs an edition-family candidate only from approved version relationships and reviewed document identity.

Validation rejects:

- a version edge whose endpoints do not match the catalog relationship;
- a family containing unrelated document codes without an explicit approved relationship;
- cycles that violate the existing version-relation policy;
- unknown or unsupported status/edition metadata;
- a mapping family that crosses a release/document boundary not admitted by the source/manifests.

Family membership is a grouping aid; every member keeps its own `document_id` and edition.

## 4. Comparison units

Comparison occurs over canonical source-grounded nodes, not arbitrary generated summaries.

A comparison unit retains:

- document/node identity;
- node type and clause identity where addressable;
- exact source text/span hash;
- ordered child/relationship projection where relevant;
- classification/modality provenance;
- source/page lineage.

Whole-clause comparison may aggregate a deterministic ordered set of source-backed nodes, but no aggregate obtains a new source identity.

## 5. Deterministic difference classes

The initial internal difference classes are closed and versioned:

- `unchanged`;
- `text_changed`;
- `added`;
- `removed`;
- `renumbered`;
- `split`;
- `merged`;
- `scope_changed`;
- `modality_changed`;
- `numeric_changed`;
- `table_changed`;
- `relationship_changed`;
- `mapping_unresolved`.

These are internal Phase 5 decision values until a public schema is approved in the detailed design.

## 6. Exact unchanged detection

`unchanged` requires exact source-grounded equality under the versioned comparison projection.

Normalized whitespace or Unicode may aid candidate generation but cannot erase a source-byte/text-hash difference from the audit record.

An exact unchanged comparison still reports the distinct source/target edition identities.

## 7. Numeric and unit comparison

Reuse the existing exact decimal/rational and unit-registry rules from material-conflict analysis.

Report exact equal values only after declared unit conversion. Unsupported units or ambiguous values are not coerced.

Numeric difference classification does not itself establish material conflict, compliance, or precedence.

## 8. Candidate mapping generation

Candidate mappings may be generated from:

1. exact addressable clause identity where version relationships permit it;
2. source-backed structural continuity;
3. deterministic renumbering metadata/rules;
4. lexical/dense/high-accuracy similarity as non-authoritative candidate generation;
5. reviewed amendment/supersession annotations.

Candidate generation must retain the full candidate set needed for audit and hard-negative evaluation; a model top-1 is never silently accepted.

## 9. Final mapping decision

A final mapping decision has one of the internal mapping kinds:

- `exact_continuation`;
- `renumbered_continuation`;
- `reworded_continuation`;
- `split`;
- `merged`;
- `replaced`;
- `removed`;
- `added`;
- `unresolved`.

Deterministic decisions require a versioned rule whose complete source-grounded inputs prove the mapping.

Semantic decisions such as reworded, split, merged, or replaced mappings require immutable human review unless an exact future design rule proves them.

## 10. Split and merge mappings

Split/merge mappings preserve cardinality explicitly.

A source node may map to several target nodes and several source nodes may map to one target node, but each side remains independently identifiable and source-backed.

The mapping decision records the complete ordered source and target node sets. It cannot invent a synthetic clause that replaces the original nodes.

## 11. Removed and added clauses

A clause is `removed` or `added` only relative to a declared edition pair/family and after the mapping candidate process proves there is no accepted continuation under the frozen rules/review set.

Absence from the top-N similarity candidates is insufficient evidence of removal/addition.

## 12. Mapping identity

Every mapping decision is content-addressed from:

- source/target edition/document/node IDs;
- exact source-span hashes;
- mapping candidate-generation version/configuration;
- deterministic rule version/configuration or human-review artifact hash;
- relevant version relationship IDs/provenance;
- mapping-schema version.

A changed source, relationship, rule, or review invalidates the mapping.

## 13. Mapping review artifact

A human mapping review records:

- candidate identity;
- chosen mapping kind;
- complete source/target node set;
- reviewer identity under the repository review policy;
- review-policy version;
- optional adjudication identity;
- decision artifact hash.

Free-form reviewer rationale may remain in governed review material but must not become public source authority.

## 14. Edition comparison output service

The internal service accepts an explicit source edition and target edition/family pair and returns deterministic comparison records bound to the active release.

Until `compare_document_versions` receives a design-frozen public schema, adapters may not expose an implementation-plan-only wire format.

## 15. Interaction with context and conflicts

For each mapped/differing source position, Phase 5 may inspect the existing required-context and conflict projections.

It must preserve:

- both edition identities;
- all material conflict sides;
- unresolved/incomplete context warnings;
- source status and applicability boundaries.

A mapping cannot be used as a shortcut that navigates an unresolved cross-reference or manufactures applicability in the target edition.

## 16. Evaluation fixtures

Include at least:

- exact unchanged clause across editions;
- pure renumbering;
- text change with same clause number;
- identical wording in unrelated documents as hard negative;
- one-to-many split;
- many-to-one merge;
- removed and newly added provisions;
- amendment-driven replacement;
- numeric/unit change;
- table header/unit/cell change;
- modality change;
- applicability/scope change;
- wrong-edition near duplicate;
- unresolved semantic mapping requiring review;
- stale mapping after source edit.

## 17. Deterministic gates

Require zero failures for:

- cross-family mapping admission;
- wrong source/target edition identity;
- lost page/source lineage;
- stale mapping reuse after behavior-bearing changes;
- model-only final mappings;
- incorrect exact unit equality;
- accidental mapping identity reuse across distinct releases;
- lower-phase conflict/context/citation regression.

## 18. Semantic mapping evaluation

For reviewed semantic mapping cases, report by mapping kind:

- candidate recall;
- accepted mapping precision;
- unresolved rate;
- split/merge cardinality accuracy;
- wrong-edition/wrong-family false-positive rate.

Use the repository's blinded human-review, adjudication, reliability, and held-out rules. Do not create a blocking numeric threshold unless the detailed design approves it.

## 19. Failure behavior

Do not guess when:

- the edition family is ambiguous;
- candidate mappings are materially tied or insufficient;
- the source has changed since review;
- required source identity is unavailable;
- a mapping decision has not passed its required review.

The internal service returns an explicit unresolved state/report; any future public warning/error shape requires design approval.

## 20. Definition of done

Edition comparison and clause mapping are implementation-ready when the builder/runtime can deterministically reproduce the same edition families, candidates, accepted mappings, difference classes, identities, lineage, and validation decisions from the same release inputs, while semantic mappings remain review-governed and every original edition/node stays independently authoritative.
