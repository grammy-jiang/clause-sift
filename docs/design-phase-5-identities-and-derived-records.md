# ClauseSift Phase 5 Identity and Derived-Record Contract

- **Status:** Normative Phase 5 detailed-design extension
- **Parent:** `docs/design-phase-5.md`
- **Parent design:** `docs/design.md`
- **Scope:** exact identity bytes, edition differences, mapping candidates, source coordinates, and conflict integration

This document closes the remaining Phase 5 internal-design gaps found during review. Where it conflicts with an earlier Phase 5 internal sentence, this document is authoritative.

## 1. Exact content-addressed ID algorithm

Every Phase 5 content-addressed ID is derived by the same byte-level algorithm.

For record kind `K`, define:

```text
domain_bytes = ASCII("clausesift.phase5." + K + ".v1") || 0x00
identity_bytes = UTF8(RFC8785_CANONICAL_JSON(identity_object))
digest = SHA256(domain_bytes || identity_bytes)
id = K + ":sha256:" + lowercase_hex(digest)
```

The NUL byte is part of the domain separator. No newline, BOM, length prefix, alternate JSON serialization, or Unicode normalization is inserted. Strings in `identity_object` are the already validated exact strings supplied by the lower-phase/Phase 5 schema. Integers are I-JSON-safe JSON integers. Arrays are ordered exactly as specified below before canonical serialization. Objects are closed: no unknown identity field is permitted.

The exact `K` values are:

- `edition_family`;
- `edition_difference`;
- `mapping_candidate`;
- `clause_mapping`;
- `product_parameter`;
- `subject_alignment`;
- `phase5_comparison`.

Independent release validation recomputes every ID from the exact object below and rejects any mismatch.

## 2. `edition_family` identity object

The identity object is exactly:

```json
{
  "identity_schema_version": "phase5.edition_family.identity.v1",
  "work_key": "<reviewed exact work key>",
  "members": [
    {
      "document_id": "<id>",
      "edition": "<exact edition>",
      "status": "<existing status enum>",
      "source_sha256": "sha256:<hex>"
    }
  ],
  "supersedes_edge_ids": ["<edge id>"]
}
```

`members` is sorted by the parent design's deterministic edition/version order, then `document_id`. `supersedes_edge_ids` is sorted by raw UTF-8 edge-ID bytes. Standalone amendment documents are excluded.

## 3. Frozen edition-difference artifact

The Phase 5 artifact list is extended with:

```text
phase5/edition-differences.jsonl
```

Each record describes one source-grounded before/after difference for one ordered edition pair.

### 3.1 Closed difference-kind enum

The v1 enum is exactly:

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

### 3.2 EditionDifference record

Each canonical JSONL record is exactly:

```json
{
  "schema_version": "phase5.edition_difference.v1",
  "edition_difference_id": "edition_difference:sha256:<hex>",
  "edition_family_id": "<family id>",
  "source_document_id": "<document id>",
  "target_document_id": "<document id>",
  "clause_mapping_id": "<mapping id or null>",
  "difference_kind": "<closed enum>",
  "source_node_ids": ["<node id>"],
  "target_node_ids": ["<node id>"],
  "source_projection_sha256": "sha256:<hex>|null",
  "target_projection_sha256": "sha256:<hex>|null",
  "difference_rule_id": "<rule id>",
  "difference_rule_config_sha256": "sha256:<hex>"
}
```

The source and target documents must be distinct full-edition members of the referenced family. Node arrays are ordered by canonical node order. For `added`, `source_node_ids` is empty and the target array is non-empty; for `removed`, the reverse applies. `added`/`removed` still require the exhaustive/no-continuation authority defined by `docs/design-phase-5.md`.

The projection hashes are hashes of closed source-grounded comparison projections. They include exact node/span text hashes, classification/modality provenance, relevant structured numeric/table values, and relevant relationship/context identities used by the selected difference rule. A missing side uses JSON `null`, never a fabricated empty projection.

### 3.3 `edition_difference` identity object

The exact identity object is:

```json
{
  "identity_schema_version": "phase5.edition_difference.identity.v1",
  "edition_family_id": "<family id>",
  "source_document_id": "<id>",
  "target_document_id": "<id>",
  "clause_mapping_id": "<id or null>",
  "difference_kind": "<enum>",
  "source_node_ids": ["<ordered ids>"],
  "target_node_ids": ["<ordered ids>"],
  "source_projection_sha256": "sha256:<hex>|null",
  "target_projection_sha256": "sha256:<hex>|null",
  "difference_rule_id": "<id>",
  "difference_rule_config_sha256": "sha256:<hex>"
}
```

Records are ordered in the artifact by `(source_document_id, target_document_id, source first-node canonical order or max sentinel, target first-node canonical order or max sentinel, difference_kind, edition_difference_id)`.

## 4. Frozen mapping-candidate universe

The Phase 5 artifact list is extended with:

```text
phase5/mapping-candidates.jsonl
```

A reviewed semantic mapping decision must bind the exact candidate universe and candidate-generation configuration that the reviewer saw.

### 4.1 MappingCandidate record

Each record is exactly:

```json
{
  "schema_version": "phase5.mapping_candidate.v1",
  "mapping_candidate_id": "mapping_candidate:sha256:<hex>",
  "edition_family_id": "<family id>",
  "source_document_id": "<document id>",
  "target_document_id": "<document id>",
  "source_node_ids": ["<node ids>"],
  "target_node_ids": ["<node ids>"],
  "candidate_kind": "continuation|renumbering|rewording|split|merge|replacement|possible_removal|possible_addition",
  "generation_channels": ["exact_rule|structural_rule|lexical|dense|reranker|review_seed"],
  "candidate_generator_id": "<id>",
  "candidate_generator_config_sha256": "sha256:<hex>",
  "source_span_hashes": ["sha256:<hex>"],
  "target_span_hashes": ["sha256:<hex>"]
}
```

The two channel enums are closed as shown. `generation_channels` is deduplicated and sorted in the enum order above. Source/target nodes are canonical-order sorted. Candidate records never constitute final mapping authority.

### 4.2 `mapping_candidate` identity object

The exact identity object is:

```json
{
  "identity_schema_version": "phase5.mapping_candidate.identity.v1",
  "edition_family_id": "<family id>",
  "source_document_id": "<id>",
  "target_document_id": "<id>",
  "source_node_ids": ["<ordered ids>"],
  "target_node_ids": ["<ordered ids>"],
  "candidate_kind": "<enum>",
  "generation_channels": ["<ordered enum values>"],
  "candidate_generator_id": "<id>",
  "candidate_generator_config_sha256": "sha256:<hex>",
  "source_span_hashes": ["<ordered hashes aligned to source nodes/spans>"],
  "target_span_hashes": ["<ordered hashes aligned to target nodes/spans>"]
}
```

### 4.3 Mapping-universe digest

For each ordered `(edition_family_id, source_document_id, target_document_id)` pair, the builder creates a mapping-universe object:

```json
{
  "schema_version": "phase5.mapping_universe.v1",
  "edition_family_id": "<family id>",
  "source_document_id": "<id>",
  "target_document_id": "<id>",
  "eligible_source_node_ids": ["<all eligible source nodes in canonical order>"],
  "eligible_target_node_ids": ["<all eligible target nodes in canonical order>"],
  "mapping_candidate_ids": ["<all candidate ids sorted by raw UTF-8 id bytes>"],
  "candidate_generator_id": "<id>",
  "candidate_generator_config_sha256": "sha256:<hex>"
}
```

`mapping_universe_sha256` is SHA-256 of the UTF-8 RFC 8785 canonical JSON bytes of this object, represented as `sha256:<64-lowercase-hex>`.

A human mapping review and a human `no_continuation` decision must record this exact `mapping_universe_sha256`. Any candidate-generator/configuration change, eligible-node change, or candidate-set change invalidates the old review.

## 5. Corrected `clause_mapping` identity object

The exact `clause_mapping` identity object is:

```json
{
  "identity_schema_version": "phase5.clause_mapping.identity.v1",
  "edition_family_id": "<family id>",
  "source_document_id": "<id>",
  "target_document_id": "<id>",
  "source_node_ids": ["<canonical-order ids>"],
  "target_node_ids": ["<canonical-order ids>"],
  "source_span_hashes": ["<ordered hashes>"],
  "target_span_hashes": ["<ordered hashes>"],
  "mapping_kind": "<closed mapping enum>",
  "decision_origin": "deterministic_rule|human_review",
  "mapping_universe_sha256": "sha256:<hex>",
  "rule_id": "<id or null>",
  "rule_config_sha256": "sha256:<hex>|null",
  "review_artifact_sha256": "sha256:<hex>|null"
}
```

Even deterministic mappings bind the universe digest so reproducibility reports can identify the exact candidate environment, although deterministic authority still comes from the exact rule rather than the candidate rank.

The human review artifact schema from `docs/design-phase-5.md` is corrected to require both `mapping_candidate_ids` reviewed and the `mapping_universe_sha256`.

## 6. Exact product-parameter source coordinates

The `ProductParameter` record is corrected to replace the ambiguous scalar span digest with exact node-qualified byte coordinates.

It contains:

```json
{
  "node_id": "<node id>",
  "node_text_start": 0,
  "node_text_end": 1,
  "source_text_sha256": "sha256:<hex>"
}
```

`node_text_start` is inclusive, `node_text_end` is exclusive, both are UTF-8-byte offsets into the exact canonical node text under the same lower-phase byte-span convention used by source/conflict records, and `0 <= start < end <= node_text_byte_length`.

The builder independently verifies that hashing exactly `node_text[start:end]` produces `source_text_sha256`, that the source/chunk membership covers the full interval, and that the lower-phase node-page mappings cover the interval without gaps. Repeated identical value strings at different byte ranges therefore remain distinct source occurrences.

### 6.1 Corrected `product_parameter` identity object

The exact identity object is:

```json
{
  "identity_schema_version": "phase5.product_parameter.identity.v1",
  "document_id": "<manufacturer specification document id>",
  "edition": "<exact edition>",
  "source_id": "<source id>",
  "node_id": "<node id>",
  "node_text_start": 0,
  "node_text_end": 1,
  "source_text_sha256": "sha256:<hex>",
  "product_model_id": "<exact governed model id>",
  "parameter_registry_sha256": "sha256:<hex>",
  "parameter_id": "<registry id>",
  "source_value_text_sha256": "sha256:<hex>",
  "value_kind": "<closed kind>",
  "normalized_value": "<canonical typed value or null>",
  "source_unit": "<exact unit or null>",
  "canonical_unit": "<canonical unit or null>",
  "condition_source_ids": ["<ids sorted by raw UTF-8 id bytes>"],
  "normalizer_id": "<id>",
  "normalizer_version": "<version>"
}
```

## 7. Exact `subject_alignment` identity object

The exact identity object is:

```json
{
  "identity_schema_version": "phase5.subject_alignment.identity.v1",
  "standard_document_id": "<id>",
  "standard_node_ids": ["<canonical-order ids>"],
  "standard_span_hashes": ["<aligned ordered hashes>"],
  "standard_concept_registry_sha256": "sha256:<hex>",
  "standard_concept_id": "<id>",
  "parameter_registry_sha256": "sha256:<hex>",
  "product_parameter_id": "<registry concept id>",
  "decision_origin": "deterministic_rule|human_review",
  "rule_id": "<id or null>",
  "rule_config_sha256": "sha256:<hex>|null",
  "review_artifact_sha256": "sha256:<hex>|null"
}
```

The review artifact binds the same exact source spans and both registry hashes.

## 8. Phase 5 alignment feeds the existing Section 20.3 conflict builder

A validated Phase 5 subject alignment may establish a comparable-subject key that did not exist in lower-phase source metadata. It must not bypass conflict generation.

The build order is therefore:

```text
validate Phase 5 registries
  -> validate/finalize subject alignments
  -> derive aligned Section 20.3 comparison keys
  -> run the existing Section 20.3 conflict candidate/state/decision/source-cover pipeline
  -> run required conflict closure/release validation
  -> materialize Phase 5 standard/product comparison records referencing those canonical conflicts
```

### 8.1 Aligned comparison-key projection

For a standard/product pair admitted by a `subject_alignment_id`, the Section 20.3 canonical comparison-key object is extended for this Phase 5 path with the closed fields:

```json
{
  "comparison_key_schema_version": "section20.3.phase5_alignment.v1",
  "subject_alignment_id": "<alignment id>",
  "standard_concept_id": "<standard concept id>",
  "product_parameter_id": "<parameter registry concept id>"
}
```

Its RFC 8785 canonical JSON hash is the canonical comparison-key hash consumed by the **existing** conflict candidate identity. The conflict record itself keeps the existing Section 20.3 schema, dimensions, position/source-cover requirements, decision authority, precedence rules, warnings, and all-side preservation semantics.

Phase 5 does not allocate a parallel conflict identity. Instead, alignment expands the source-grounded candidate inputs to the existing builder before conflict materialization.

If an aligned pair contains incompatible `required` positions with known shared applicability and meets the parent design's confirmation rules, the canonical Section 20.3 conflict must exist before the Phase 5 comparison is materialized. The Phase 5 comparison then references that conflict ID.

If shared applicability is unresolved, the aligned pair cannot be deterministically confirmed solely because values differ; existing unresolved/conflict policy remains authoritative.

## 9. Exact `phase5_comparison` identity object

The exact identity object is:

```json
{
  "identity_schema_version": "phase5.comparison.identity.v1",
  "subject_alignment_id": "<id>",
  "standard_source_ids": ["<ids sorted by existing evidence source order>"],
  "product_parameter_record_ids": ["<ids sorted by raw UTF-8 id bytes>"],
  "applicability_projection_sha256": "sha256:<hex>",
  "shared_applicability_status": "proven|unresolved|disjoint",
  "comparison_outcome": "equivalent|meets_minimum|below_minimum|meets_maximum|above_maximum|inside_range|outside_range|incompatible_sets|not_comparable",
  "comparison_rule_id": "<id>",
  "comparison_rule_config_sha256": "sha256:<hex>",
  "conflict_ids": ["<canonical Section 20.3 ids sorted by raw UTF-8 id bytes>"]
}
```

Every conflict ID must resolve to a conflict generated/validated before this comparison record, including conflicts whose comparable-subject key came from the Phase 5 alignment path above.

## 10. Release validation additions

In addition to `docs/design-phase-5.md`, validation now requires:

- `phase5/edition-differences.jsonl` complete schema/order/ID recomputation;
- `phase5/mapping-candidates.jsonl` complete schema/order/ID recomputation;
- every human mapping/no-continuation review binds the exact current mapping-universe digest;
- every product parameter byte range hashes to the declared source span and resolves through lower-phase page lineage;
- every aligned incompatible required pair is offered to Section 20.3 before Phase 5 comparison materialization;
- every Phase 5 comparison conflict reference resolves to a validated canonical Section 20.3 conflict;
- all seven Phase 5 ID kinds recompute byte-for-byte under Section 1.

Any mismatch blocks candidate release activation.
