# Phase 5 Structured Product Parameter Plan

**Phase:** 5 — Version and Product Intelligence  
**Status:** Normative Phase 5 implementation-plan appendix  
**Authority:** `docs/design.md` Sections 12, 14–22, 29–31, and 35  
**Companion:** `docs/implementation/phase-5-version-product-intelligence.md`

## 1. Purpose

This appendix defines source-grounded extraction, normalization, validation, storage, and retrieval of structured manufacturer/product parameters.

The product-parameter layer is a deterministic projection over manufacturer evidence. It does not replace original text, tables, page citations, or document identity.

## 2. Eligible sources

A product parameter may be extracted only from an admitted canonical source belonging to a manufacturer/product specification, manual, data sheet, or other document type already supported by the evidence vocabulary.

The builder must preserve:

- exact `document_id` and edition/status;
- product model identifier when explicitly source-backed or manifest-owned;
- canonical node/source ID;
- source span and text hash;
- page/source lineage;
- source modality/classification provenance;
- applicability/operating conditions needed to interpret the value.

A filename, URL fragment, or model guess is not product identity authority.

## 3. Controlled parameter registry

Phase 5 introduces a versioned internal registry of parameter concepts.

Each registry entry defines:

- stable parameter ID;
- display label(s);
- supported value kind;
- dimensional/unit family when applicable;
- deterministic source-value parser/normalizer ID and version;
- canonical comparison unit where one exists;
- aliases usable only for candidate extraction/search;
- conditions under which normalization is valid;
- unsupported/ambiguous behavior.

The registry is a build/release input and participates in artifact/cache identity.

## 4. Value kinds

The initial internal value kinds should support at least:

- exact scalar numeric;
- bounded numeric range;
- open-ended minimum/maximum;
- enumerated text value;
- boolean/presence state when explicitly source-backed;
- ordered list/set of source-backed values;
- conditional value with source-backed condition;
- table-derived value with inherited header/unit context;
- unparsed/unsupported source value.

The detailed design must freeze the final closed schema before implementation.

## 5. Source value preservation

Every structured record retains the exact source value text and exact source span hash.

Normalized values are secondary deterministic projections. The runtime never returns a normalized scalar without a resolvable source record.

If normalization fails, retain the source-backed parameter mention as unsupported/ambiguous rather than dropping it or guessing.

## 6. Unit normalization

Reuse the project's versioned exact unit registry and decimal/rational conversion contract.

Normalization must:

- reject unknown/ambiguous units;
- preserve the exact source unit token/text;
- record canonical unit only for a supported deterministic conversion;
- avoid floating-point equality as authority when exact rational/decimal comparison is defined;
- preserve ranges and inequality direction;
- preserve conditions that materially change applicability.

## 7. Table-derived parameters

A table value is not self-contained.

Parameter extraction from a table must retain the inherited row/column headers, units, table identity, parent clause/context, and source spans required by the existing table-evidence contract.

A table cell without the required header/unit context cannot be promoted to a normalized product parameter.

## 8. Conditional parameters

Operating conditions such as temperature, pressure, flow regime, voltage, frequency, installation orientation, duty point, or equipment configuration remain attached to the parameter when the source conditions the value on them.

Phase 5 may normalize a condition only through a declared deterministic registry rule. It may not infer missing conditions from another model, adjacent product, or external engineering convention.

## 9. Product model identity

Product model identity must come from reviewed manifest facts or explicit source-backed model identifiers under deterministic extraction rules.

Near-identical model numbers remain distinct unless an approved relationship says otherwise.

Tests must include:

- same family with different suffixes;
- regional variants;
- model-series versus exact-model references;
- superseded product documentation;
- wrong-model near duplicates.

## 10. Extraction pipeline

The offline pipeline is:

1. enumerate eligible manufacturer/product nodes;
2. generate candidate parameter mentions from exact labels, tables, structured patterns, and optional model-assisted candidate detection;
3. resolve candidate to a registry parameter ID or leave unresolved;
4. parse the exact source value through the registered deterministic parser;
5. normalize supported units/value forms;
6. attach exact applicability/condition context;
7. validate source/span/lineage and product identity;
8. materialize the checksummed Phase 5 parameter artifact.

Model-assisted extraction may propose candidates but cannot author final source values or units.

## 11. Parameter identity

A parameter record is content-addressed from all behavior-bearing inputs, including:

- release/document/source/node identity;
- exact source span hash;
- product model identity/provenance;
- parameter-registry version/hash;
- parser/normalizer ID/version/configuration;
- exact source value text/hash;
- normalized value/unit projection;
- applicability/condition projection;
- schema version.

Any source, registry, rule, manifest, or condition change invalidates the old record.

## 12. Duplicate and repeated values

Repeated source statements are not silently collapsed by normalized value equality.

Deduplication may group exact identical parameter records for retrieval convenience only when every authoritative identity/provenance dimension matches. Distinct source positions remain auditable.

## 13. Conflicting manufacturer parameters

Two manufacturer parameter records that disagree are not resolved by recency or model score.

When existing Section 20.3 conflict rules apply, use the same canonical conflict semantics. Otherwise report both source-backed values and their document/model/status/applicability context.

## 14. Search and lookup service

The internal product service supports:

- exact product model filtering;
- exact parameter ID filtering;
- source/document/edition/status filters;
- lexical/high-accuracy retrieval over source-backed parameter context;
- deterministic ordering and pagination under existing runtime contracts.

The Section 22.2 future tools `search_product_specifications` and `get_product_parameter` must not be publicly exposed until the detailed design freezes their schemas.

## 15. Evaluation corpus

Add independently reviewed cases for:

- exact model number retrieval;
- scalar values and units;
- ranges/minima/maxima;
- table-derived values;
- conditional values;
- enumerated/text parameters;
- aliases and synonyms;
- wrong-model hard negatives;
- wrong-edition/superseded data;
- ambiguous unit/value strings;
- unsupported parameters;
- repeated/conflicting manufacturer statements;
- missing operating condition;
- model-assisted candidate false positives.

## 16. Deterministic gates

Require zero failures for:

- fabricated source value or unit;
- wrong model/document/edition attribution;
- missing source/page lineage;
- invalid exact unit conversion;
- loss of required table header/unit context;
- stale parameter artifact reuse after source/registry/rule change;
- model-only final value admission;
- lower-phase citation/context/conflict regression.

## 17. Semantic extraction evaluation

For parameter detection/resolution that is not fully deterministic, report at least:

- mention candidate recall;
- resolved-parameter precision;
- unresolved rate;
- wrong-parameter-ID rate;
- wrong-model attribution rate;
- value-normalization success/error rate by value kind and unit family.

Human semantic labels follow existing blinded review/reliability/held-out governance. New blocking thresholds require detailed-design approval.

## 18. Release and integrity

The Phase 5 parameter registry and materialized parameter artifact are immutable release inputs/artifacts.

Release validation independently verifies:

- schema/registry version compatibility;
- one-to-one source/span ownership;
- source/model/document identity;
- supported normalizer identity;
- exact stored-versus-recomputed normalized values;
- complete artifact-table checksum/size coverage;
- no orphan/stale record.

## 19. Failure behavior

The builder/runtime must distinguish:

- no matching parameter evidence;
- parameter mention found but registry mapping unresolved;
- known parameter with unsupported value form;
- unit unsupported/ambiguous;
- product model identity incomplete;
- applicability/operating condition incomplete;
- release-integrity failure.

Public codes/fields for these states require a design-level schema before exposure.

## 20. Definition of done

Structured product parameters are implementation-ready when the same release inputs deterministically reproduce the same registry-bound source records and normalized values, every value remains traceable to exact manufacturer evidence, ambiguity stays visible, model/product/edition boundaries are exact, and no public product schema is invented outside the detailed design.
