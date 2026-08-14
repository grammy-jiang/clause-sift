# ClauseSift Phase 5 Detailed Design Contract

- **Status:** Normative detailed-design extension
- **Parent authority:** `docs/design.md` Section 35
- **Scope:** Phase 5 — Version and Product Intelligence
- **Public-interface authority:** `docs/design.md` Section 22

## 1. Purpose and authority

`docs/design.md` Section 35 defines four Phase 5 capabilities but intentionally does not define the internal data contracts needed to implement them. This document freezes those **internal** contracts so Phase 5 implementation is not blocked by undefined schemas.

This document does **not** promote any Section 22.2 future tool to the public API. `compare_document_versions`, `search_product_specifications`, and `get_product_parameter` remain non-public until `docs/design.md` freezes their public schemas.

Where a Phase 5 implementation-plan document conflicts with this detailed design, this document is authoritative for the internal Phase 5 contracts below. All lower-phase contracts in `docs/design.md` remain authoritative.

## 2. Design invariants

Phase 5 shall preserve these invariants:

1. every edition/document/node/source keeps its lower-phase canonical identity;
2. standalone amendment documents are never treated as full editions;
3. semantic similarity may generate candidates but cannot create authoritative mappings or product facts;
4. manufacturer product parameters originate only from manufacturer-authoritative sources admitted by the current vocabulary;
5. standard/product subject alignment is a reviewed, source-grounded decision, not a new manifest relationship;
6. `added`/`removed` is authoritative only after exhaustive deterministic proof or immutable human no-continuation review;
7. all derived records are release-scoped, content-addressed, checksummed, and invalidated by every behavior-bearing input change;
8. Phase 5 does not create a second conflict or precedence system;
9. original source text/page/lineage remains authoritative;
10. runtime Phase 5 services are read-only.

## 3. Release artifacts

Phase 5 adds these internal release artifacts:

- `phase5/edition-families.jsonl`;
- `phase5/clause-mappings.jsonl`;
- `phase5/parameter-registry.json`;
- `phase5/product-parameters.jsonl`;
- `phase5/standard-concepts.json`;
- `phase5/subject-alignments.jsonl`;
- `phase5/comparisons.jsonl`;
- `reports/phase5-evaluation.json`.

Every runtime-opened artifact appears in the existing exhaustive release artifact table with relative path, media type, exact byte size, and SHA-256. The artifacts use RFC 8785 canonical JSON objects; JSONL records are canonicalized individually and ordered by their declared stable identity.

No Phase 5 artifact is runtime authority unless startup/release validation proves schema version, checksum, lower-phase ownership, and all cross-record references.

## 4. Common internal identity rules

All Phase 5 IDs use the project's opaque-ID grammar and are release-stable for identical inputs.

A content-addressed Phase 5 ID is a domain-separated SHA-256 over an RFC 8785 canonical identity object. The identity object includes its `identity_schema_version` and every behavior-bearing source/rule/review input required by the record type.

The stored ID format is:

```text
<kind>:sha256:<64-lowercase-hex>
```

The exact `<kind>` prefixes are:

- `edition_family`;
- `clause_mapping`;
- `product_parameter`;
- `subject_alignment`;
- `phase5_comparison`.

A changed source hash, manifest fact, classification provenance, lower-phase relationship, registry entry, normalizer, rule configuration, review artifact, or internal schema version changes the affected Phase 5 identity.

## 5. Edition-family contract

### 5.1 Membership authority

An edition family represents successive full editions of the **same work**. Membership requires a reviewed same-work identity consisting of:

- exact normalized document code/family key owned by approved manifest/catalog identity; and
- distinct edition values; and
- an admitted `supersedes` relationship chain or other explicit reviewed same-work edition relationship permitted by the lower-phase design.

A standalone `amendment` document is not an edition-family member even when it has an `amends` edge to a family member. `amends` is consumed as version-comparison context only.

Title similarity, filename similarity, clause-number similarity, or embedding similarity cannot establish family membership.

### 5.2 EditionFamily record

Each line in `phase5/edition-families.jsonl` is exactly:

```json
{
  "schema_version": "phase5.edition_family.v1",
  "edition_family_id": "edition_family:sha256:<hex>",
  "work_key": "<reviewed canonical work key>",
  "members": [
    {
      "document_id": "<document id>",
      "edition": "<exact edition>",
      "status": "<existing status enum>",
      "source_sha256": "sha256:<hex>"
    }
  ],
  "supersedes_edge_ids": ["<edge id>"]
}
```

`members` is ordered by the existing deterministic edition/version ordering rule and then `document_id`. It contains at least two full-edition documents. `supersedes_edge_ids` contains only lower-phase validated edges whose endpoints are members.

`work_key` is reviewed document-family identity, not a generated title summary.

### 5.3 Edition-family identity

The `edition_family_id` identity object contains:

- `identity_schema_version`;
- `work_key`;
- ordered member `(document_id, edition, status, source_sha256)` tuples;
- ordered `supersedes_edge_ids`;
- lower-phase document-identity/schema version.

Standalone amendment identities are excluded from the family ID.

## 6. Clause-mapping contract

### 6.1 Closed mapping kinds

The internal v1 mapping kind enum is exactly:

- `exact_continuation`;
- `renumbered_continuation`;
- `reworded_continuation`;
- `split`;
- `merged`;
- `replaced`;
- `removed`;
- `added`;
- `unresolved`.

These are internal values only until a public schema is approved.

### 6.2 Mapping record

Each `phase5/clause-mappings.jsonl` record is exactly:

```json
{
  "schema_version": "phase5.clause_mapping.v1",
  "clause_mapping_id": "clause_mapping:sha256:<hex>",
  "edition_family_id": "<edition family id>",
  "source_document_id": "<document id>",
  "target_document_id": "<document id>",
  "source_node_ids": ["<node id>"],
  "target_node_ids": ["<node id>"],
  "mapping_kind": "<closed enum>",
  "decision_origin": "deterministic_rule|human_review",
  "rule_id": "<rule id or null>",
  "rule_config_sha256": "sha256:<hex>|null",
  "review_artifact_sha256": "sha256:<hex>|null",
  "source_span_hashes": ["sha256:<hex>"],
  "target_span_hashes": ["sha256:<hex>"]
}
```

The source and target documents must be distinct members of the same edition family. Source/target node arrays are non-empty except:

- `removed`: target array is empty;
- `added`: source array is empty;
- `unresolved`: both sides identify the reviewed/candidate source and target sets when known; one side may be empty only when the unresolved question is potential addition/removal.

### 6.3 Deterministic mapping authority

`decision_origin: deterministic_rule` is permitted only for a design-reviewed rule that proves the mapping entirely from lower-phase source-grounded identity/structure/version data. The v1 deterministic rules may cover exact unchanged continuation and explicitly proven renumbering.

`reworded_continuation`, `split`, `merged`, and `replaced` require `human_review` unless a later detailed-design revision adds an exact deterministic rule.

### 6.4 Human review artifact

A mapping review artifact is immutable canonical JSON containing:

- review schema/policy version;
- exact mapping candidate identity;
- complete source/target node sets and span hashes;
- selected mapping kind;
- reviewer identity;
- adjudicator identity or null;
- decision content hash.

The artifact cannot attach to changed source/target spans.

### 6.5 Added/removed authority

`added` or `removed` is final only when one of these is true:

1. an exhaustive deterministic mapping rule proves no continuation exists across the complete eligible node set for the edition pair; or
2. an immutable human `no_continuation` review decision explicitly covers the complete source/target edition pair and the node in question.

Candidate-generation non-recall, top-N absence, or lack of an accepted mapping is insufficient. Without exhaustive/no-continuation authority, the record remains `unresolved`.

### 6.6 Mapping identity

The `clause_mapping_id` identity object includes:

- edition family ID;
- source/target document IDs;
- ordered source/target node IDs and exact span hashes;
- mapping kind;
- decision origin;
- rule ID/config hash or review artifact hash;
- mapping schema version.

## 7. Product parameter authority

### 7.1 Eligible manufacturer source

V1 product-parameter extraction is allowed only when the source document has:

```text
document_type == manufacturer_specification
```

under the existing Section 12.2 vocabulary/provenance contract.

`technical_manual`, `design_guideline`, research literature, code, standard, or other document types are not manufacturer parameter authority in v1 even if they mention a product. Supporting them later requires a reviewed manufacturer/product-ownership design contract and vocabulary/provenance rule.

### 7.2 Parameter registry entry

`phase5/parameter-registry.json` is a canonical JSON object:

```json
{
  "schema_version": "phase5.parameter_registry.v1",
  "entries": [
    {
      "parameter_id": "<stable controlled id>",
      "display_name": "<non-authoritative label>",
      "value_kind": "scalar|range|minimum|maximum|enum|boolean|set|conditional|text",
      "unit_dimension": "<unit dimension or null>",
      "canonical_unit": "<unit or null>",
      "normalizer_id": "<normalizer id>",
      "normalizer_version": "<version>",
      "aliases": ["<candidate-generation alias>"]
    }
  ]
}
```

Entries are sorted by `parameter_id`; aliases are sorted and retrieval-only. Registry labels/aliases do not become source facts.

### 7.3 ProductParameter record

Each `phase5/product-parameters.jsonl` record is exactly:

```json
{
  "schema_version": "phase5.product_parameter.v1",
  "product_parameter_id": "product_parameter:sha256:<hex>",
  "document_id": "<manufacturer specification document id>",
  "edition": "<exact edition>",
  "source_id": "<source id>",
  "node_id": "<node id>",
  "source_span_sha256": "sha256:<hex>",
  "product_model_id": "<source/manifest-backed exact model id>",
  "parameter_id": "<registry parameter id>",
  "source_value_text": "<exact source value text>",
  "value_kind": "<registry value kind>",
  "normalized_value": "<canonical typed value or null>",
  "source_unit": "<source unit text or null>",
  "canonical_unit": "<registry unit or null>",
  "condition_source_ids": ["<source ids>"],
  "normalizer_id": "<id>",
  "normalizer_version": "<version>"
}
```

`normalized_value` is null when deterministic normalization is unsupported or ambiguous. The record remains source-grounded through `source_value_text` and its source span.

### 7.4 Product parameter identity

The identity object includes:

- manufacturer document/edition/source/node/span hash;
- exact product model ID/provenance hash;
- parameter-registry hash and parameter ID;
- exact source value text hash;
- normalized typed value/unit projection;
- condition source IDs/hashes;
- normalizer ID/version;
- product-parameter schema version.

## 8. Standard concept and subject-alignment authority

### 8.1 Why a separate reviewed contract is required

The existing manifest relationship types do not encode “same comparable engineering parameter”. Phase 5 therefore must not overload `depends_on`, `applies_subject_to`, `supersedes`, or `amends` for subject alignment.

V1 uses a separate reviewed, source-grounded standard concept registry and alignment artifact.

### 8.2 StandardConcept registry

`phase5/standard-concepts.json` is:

```json
{
  "schema_version": "phase5.standard_concept_registry.v1",
  "entries": [
    {
      "standard_concept_id": "<stable controlled id>",
      "value_kind": "scalar|range|minimum|maximum|enum|boolean|set|conditional|text",
      "unit_dimension": "<unit dimension or null>",
      "canonical_unit": "<unit or null>",
      "comparison_rule_id": "<versioned deterministic comparison rule>"
    }
  ]
}
```

The registry describes comparison semantics only; it does not assert that any source clause represents a concept.

### 8.3 Subject alignment decision

A source-to-product comparable-subject alignment is represented in `phase5/subject-alignments.jsonl`:

```json
{
  "schema_version": "phase5.subject_alignment.v1",
  "subject_alignment_id": "subject_alignment:sha256:<hex>",
  "standard_document_id": "<document id>",
  "standard_node_ids": ["<node id>"],
  "standard_span_hashes": ["sha256:<hex>"],
  "standard_concept_id": "<registry id>",
  "product_parameter_id": "<registry parameter id>",
  "decision_origin": "deterministic_rule|human_review",
  "rule_id": "<rule id or null>",
  "rule_config_sha256": "sha256:<hex>|null",
  "review_artifact_sha256": "sha256:<hex>|null"
}
```

This record aligns a **standard concept** to a **product parameter concept**. It is not an Evidence Graph edge and does not modify the manifest relation vocabulary.

A deterministic alignment is allowed only when an approved exact source annotation/rule proves the concept. Otherwise immutable human review is required. Similarity/model score may generate candidates only.

### 8.4 Alignment identity and invalidation

The alignment identity object includes:

- standard document/node/span hashes;
- standard-concept registry hash/ID;
- parameter-registry hash/ID;
- rule/config hash or review artifact hash;
- alignment schema version.

Any source, registry, rule, or review change invalidates the alignment.

## 9. Standard/product comparison record

Each `phase5/comparisons.jsonl` record is exactly:

```json
{
  "schema_version": "phase5.comparison.v1",
  "phase5_comparison_id": "phase5_comparison:sha256:<hex>",
  "subject_alignment_id": "<alignment id>",
  "standard_source_ids": ["<source ids>"],
  "product_parameter_record_ids": ["<product parameter ids>"],
  "shared_applicability_status": "proven|unresolved|disjoint",
  "comparison_outcome": "equivalent|meets_minimum|below_minimum|meets_maximum|above_maximum|inside_range|outside_range|incompatible_sets|not_comparable",
  "comparison_rule_id": "<rule id>",
  "comparison_rule_config_sha256": "sha256:<hex>",
  "conflict_ids": ["<existing conflict ids>"]
}
```

When `shared_applicability_status` is `unresolved` or `disjoint`, `comparison_outcome` must be `not_comparable` unless an existing lower-phase deterministic rule explicitly authorizes another exact result.

`conflict_ids` can contain only validated existing Section 20.3 conflict identities. Phase 5 does not allocate a parallel conflict record.

The comparison identity includes every referenced source/parameter/alignment identity, exact applicability/context projection hash, comparison rule/configuration, conflict IDs, and schema version.

## 10. Validation and referential rules

Release validation independently verifies:

- every edition-family member exists and is a full-edition document;
- no standalone amendment appears as a family member;
- every mapping source/target belongs to the referenced family and edition pair;
- added/removed decisions have exhaustive deterministic or human no-continuation authority;
- every product parameter source is `manufacturer_specification` and source/span/model identity matches the lower-phase catalog;
- parameter registry/value-kind/unit/normalizer compatibility;
- every subject alignment references existing source nodes and registry entries;
- no subject alignment is represented as an unsupported manifest/Evidence Graph relation;
- every comparison references valid alignment/parameter/source records and existing conflict IDs only;
- every content-addressed ID recomputes exactly;
- no missing/extra/unknown schema fields are admitted;
- all records are sorted under their schema's deterministic ordering rule.

A validation mismatch blocks candidate release activation.

## 11. Cache invalidation

Phase 5 cache keys include exactly the behavior-bearing dependencies of the artifact being cached.

At minimum:

- edition families invalidate on document identity/edition/status/source/version-edge change;
- clause mappings invalidate on family/source/node/span/mapping-rule/review change;
- product parameters invalidate on source/model/registry/normalizer/condition change;
- standard concepts invalidate on registry/comparison-rule change;
- subject alignments invalidate on source span, either registry, rule, or review change;
- comparisons invalidate on alignment, source/parameter, applicability/context, comparison-rule, or conflict-decision change.

A changed lower-phase release ID invalidates every Phase 5 runtime artifact unless byte-identical dependency closure proves reuse through the existing cache identity rules.

## 12. Model boundary

Models may propose:

- clause-mapping candidates;
- parameter mentions;
- standard-concept/parameter alignment candidates.

A model may not directly finalize:

- edition-family membership;
- clause mapping;
- added/removed state;
- product source value/unit/model identity;
- standard concept alignment;
- applicability;
- comparison outcome where exact deterministic inputs are absent;
- conflict or precedence state.

## 13. Public-interface boundary

This detailed design intentionally freezes **internal** Phase 5 artifacts only.

The following remain future tools under `docs/design.md` Section 22.2 and are not public in Phase 5 until their exact schemas are added to the parent design:

- `compare_document_versions`;
- `search_product_specifications`;
- `get_product_parameter`.

Internal service implementations must not expose these artifact schemas as de facto public contracts.

## 14. Versioning

Any incompatible change to a Phase 5 internal schema increments its explicit schema version and changes candidate/release identity.

Unknown Phase 5 schema versions fail release/startup validation visibly. There is no best-effort interpretation of a newer schema by an older runtime.

## 15. Definition of design completeness

The internal Phase 5 design is complete for implementation when:

- all record schemas above are frozen and closed;
- all referential and content-addressed identities are independently recomputable;
- amendment-versus-edition-family behavior is unambiguous;
- manufacturer source authority is restricted to the current vocabulary contract;
- added/removed authority cannot depend on candidate non-recall;
- comparable-subject alignment has a dedicated reviewed contract rather than abusing manifest relations;
- invalidation covers every behavior-bearing input;
- public tools remain blocked until the parent Section 22 contract is extended.
