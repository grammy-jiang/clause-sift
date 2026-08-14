# ClauseSift Phase 5 Comparison Normalization Contract

- **Status:** Normative Phase 5 detailed-design extension
- **Parents:** `docs/design-phase-5.md`, `docs/design-phase-5-identities-and-derived-records.md`, `docs/design-phase-5-provenance-and-projections.md`
- **Parent design:** `docs/design.md`
- **Scope:** applicability projection, classification projection, and identity-insensitive cross-edition comparison

This document supersedes the earlier Phase 5 comparison/projection fields where explicitly stated below.

## 1. Corrected classification projection

The `classification_records` field in `EditionComparisonProjection` is replaced by the following closed form:

```json
"classification_records": [
  {
    "node_id": "<node id>",
    "records": [
      {
        "field": "node_type",
        "value": "<exact selected value>",
        "provenance_sha256": "sha256:<hex>"
      },
      {
        "field": "normative_status",
        "value": "<exact selected value>",
        "provenance_sha256": "sha256:<hex>"
      },
      {
        "field": "source_modality",
        "value": "<exact selected value>",
        "provenance_sha256": "sha256:<hex>"
      }
    ]
  }
]
```

There are exactly three nested records for every projected node, in field order `node_type`, `normative_status`, `source_modality`. Outer records are sorted by canonical node order.

For every nested record:

- `value` equals the corresponding canonical `nodes` column;
- `provenance_sha256` equals the exact `node_classifications.provenance_sha256` for `(node_id, field)`;
- release validation independently verifies that the provenance hash covers the complete closed lower-phase classification record and that the record's selected value matches `value`.

No aggregate classification hash exists in Phase 5. The three independent lower-phase provenance records remain distinct.

The `EditionComparisonProjection` hash from `docs/design-phase-5-provenance-and-projections.md` is recomputed over this corrected structure; the previous single `classification_sha256` form is invalid.

## 2. Phase 5 applicability position projection

A standard/product comparison must establish shared applicability from exact source positions. Phase 5 reuses the lower-phase Section 20.3 source-grounded comparison and required-context projection machinery but freezes how those projections are selected and bound for every Phase 5 comparison, including compatible/non-conflicting pairs.

### 2.1 Position projection requirement

For every exact Phase 5 aligned standard position and every ProductParameter source position participating in a comparison, the builder runs the same versioned lower-phase position-projection functions used by Section 20.3 **even when the pair does not become a conflict candidate**:

1. the Section 20.3 comparison projection over that exact source position; and
2. the Section 19 required-context projection used by Section 20.3 conflict classification.

The functions, comparison-rule-set version/configuration, context-rule-set version/configuration, classification provenance, manifest facts, exact source spans, applicability/exception/dependency relationships, scope IDs, jurisdiction IDs, effective interval, product/equipment class, normalized value/unit facts, and any other source-grounded fact consumed by those parent-design projections are exactly the parent-design inputs. Phase 5 does not create a looser alternative projection.

The builder exposes only the two projection hashes to the Phase 5 applicability object; release validation independently recomputes the parent projections from the exact source positions and requires equality.

### 2.2 Standard applicability position

The standard position is selected exactly from the `standard_spans` in the validated `SubjectAlignment` record. The Phase 5 applicability object contains:

```json
{
  "standard_spans": ["<ordered SourceSpan objects>"],
  "comparison_projection_sha256": "sha256:<hex>",
  "required_context_projection_sha256": "sha256:<hex>"
}
```

`standard_spans` is byte-for-byte the ordered array in the alignment record; it is not reselected by retrieval rank.

### 2.3 Product applicability positions

The product positions are selected exactly from the `product_parameter_record_ids` in the Phase 5 comparison. Each referenced ProductParameter resolves to its exact value SourceSpan and validated parameter-model association.

The product array is sorted by raw UTF-8 ProductParameter ID bytes and contains exactly:

```json
{
  "product_parameter_record_id": "<product parameter id>",
  "parameter_source_span": "<exact SourceSpan object>",
  "parameter_model_association_sha256": "sha256:<hex>",
  "comparison_projection_sha256": "sha256:<hex>",
  "required_context_projection_sha256": "sha256:<hex>"
}
```

No other product source may enter the applicability decision.

## 3. Closed shared-applicability projection

For one Phase 5 comparison, construct exactly:

```json
{
  "schema_version": "phase5.applicability_projection.v1",
  "subject_alignment_id": "<alignment id>",
  "standard_position": {
    "standard_spans": ["<SourceSpan objects>"],
    "comparison_projection_sha256": "sha256:<hex>",
    "required_context_projection_sha256": "sha256:<hex>"
  },
  "product_positions": [
    {
      "product_parameter_record_id": "<id>",
      "parameter_source_span": "<SourceSpan object>",
      "parameter_model_association_sha256": "sha256:<hex>",
      "comparison_projection_sha256": "sha256:<hex>",
      "required_context_projection_sha256": "sha256:<hex>"
    }
  ],
  "dimension_results": {
    "jurisdiction": "overlap|disjoint|unknown",
    "effective_interval": "overlap|disjoint|unknown",
    "product_or_equipment_class": "overlap|disjoint|unknown",
    "operating_conditions": "overlap|disjoint|unknown",
    "required_context": "complete|incomplete"
  },
  "shared_applicability_status": "proven|disjoint|unresolved",
  "applicability_rule_id": "<versioned rule id>",
  "applicability_rule_config_sha256": "sha256:<hex>",
  "context_rule_set_version": "<version>",
  "context_rule_set_config_sha256": "sha256:<hex>",
  "conflict_rule_set_version": "<version>",
  "conflict_rule_set_config_sha256": "sha256:<hex>"
}
```

There are no other fields.

### 3.1 Dimension derivation

The five `dimension_results` values are computed only from the exact parent-design position projections named above:

- `jurisdiction` is `overlap` only when the manifested jurisdiction sets prove a non-empty shared value; `disjoint` only when they prove disjointness; missing/insufficient facts are `unknown`;
- `effective_interval` follows the parent conflict rule for exact source-backed effective intervals with the same overlap/disjoint/unknown semantics;
- `product_or_equipment_class` follows the parent conflict rule for manifested/source-grounded product or equipment class;
- `operating_conditions` compares only source-grounded conditions admitted by the parameter/model association, required context, and the versioned Phase 5 applicability rule; absence or unsupported normalization is `unknown`;
- `required_context` is `complete` only when every exact position's parent required-context projection is complete under the active Section 19 rules; otherwise it is `incomplete`.

No similarity, authority name, active status, document type, stricter value, or ranking score changes a dimension result.

### 3.2 Overall status

`shared_applicability_status` is:

1. `disjoint` if any of jurisdiction, effective interval, product/equipment class, or operating conditions is `disjoint`;
2. otherwise `unresolved` if any of those four dimensions is `unknown` or `required_context` is `incomplete`;
3. otherwise `proven`.

This precedence is fixed for v1.

The `shared_applicability_status` stored in the Phase 5 comparison record must exactly equal this computed value. A `proven` comparison cannot be materialized from an incomplete applicability projection.

### 3.3 Applicability projection digest

The exact digest is:

```text
projection_bytes = UTF8(RFC8785_CANONICAL_JSON(Phase5ApplicabilityProjection))
digest = SHA256(ASCII("clausesift.phase5.applicability_projection.v1") || 0x00 || projection_bytes)
applicability_projection_sha256 = "sha256:" + lowercase_hex(digest)
```

This is the only valid meaning of `applicability_projection_sha256` in `phase5_comparison` identity material.

Any source span, manifest applicability fact, required-context edge/occurrence, product-model association, parent projection, applicability rule/configuration, or context/conflict rule-set change therefore changes the digest.

## 4. Final-mapping partition for cross-edition comparison

Identity-insensitive comparison requires an unambiguous mapping role for each compared node.

For one ordered edition pair, release validation requires each eligible canonical node to participate in at most one final non-`unresolved` mapping decision for that pair. A node appearing in competing final mappings makes the mapping set invalid until review resolves the ambiguity.

Define:

```text
mapping_slot(node_id) = clause_mapping_id of that node's unique final mapping
```

For an `added` target or `removed` source, the one-sided mapping ID is still its mapping slot. A node with no final mapping has no mapping slot and cannot participate in an identity-insensitive equality claim; any comparison that needs such a node is `mapping_unresolved` or the relevant relationship subview is unequal as specified below.

## 5. Identity-insensitive normalized edition view

The raw `EditionComparisonProjection` remains the auditable edition-specific projection and keeps document/node/source/edge identities. Difference classification does **not** compare those raw IDs directly.

For each projection side, derive exactly one closed `NormalizedEditionView`:

```json
{
  "schema_version": "phase5.normalized_edition_view.v1",
  "text_segments": [
    {
      "mapping_slot": "<clause mapping id>",
      "segment_ordinal": 0,
      "source_text_sha256": "sha256:<hex>",
      "byte_length": 1
    }
  ],
  "classifications": [
    {
      "mapping_slot": "<clause mapping id>",
      "node_ordinal_within_slot": 0,
      "node_type": "<exact value>",
      "normative_status": "<exact value>",
      "source_modality": "<exact value>"
    }
  ],
  "scope_relations": ["<NormalizedRelation objects>"],
  "reference_version_relations": ["<NormalizedRelation objects>"],
  "numeric_atoms": [
    {
      "mapping_slot": "<clause mapping id>",
      "atom_ordinal": 0,
      "comparison_dimension": "<existing dimension>",
      "operator": "eq|min|max|range|set",
      "canonical_value": "<exact canonical value>",
      "canonical_unit": "<unit or null>"
    }
  ],
  "tables": ["<NormalizedTable objects>"]
}
```

There are no other fields. The normalized view deliberately omits document IDs, editions, node IDs, source IDs, byte offsets, raw edge IDs, manifest hashes, and classification provenance hashes. Those remain in the raw projection for audit/invalidation but are not semantic equality keys across editions.

## 6. Node and span ordering in the normalized view

Within a mapping slot, source-side nodes and target-side nodes each use the corresponding ordered arrays from the accepted `ClauseMapping` record. `node_ordinal_within_slot` is the zero-based index within that side's mapping array.

`text_segments` is built from raw `source_spans` grouped by mapping slot and node ordinal, then ordered by `(mapping_slot UTF-8 bytes, node_ordinal_within_slot, node_text_start, node_text_end)` before edition-specific IDs/offsets are removed. `segment_ordinal` is the dense zero-based order within the mapping slot after that ordering.

A one-to-one `exact_continuation`, `renumbered_continuation`, or `reworded_continuation` therefore has directly comparable ordinals. `split`/`merged` mappings are classified by mapping kind and are never required to satisfy `unchanged` equality.

## 7. Normalized relation signatures

A `NormalizedRelation` is exactly:

```json
{
  "relation_type": "<existing relation type>",
  "source_mapping_slot": "<mapping id>",
  "target_mapping_slot": "<mapping id>",
  "source_member_ordinal": 0,
  "target_member_ordinal": 0
}
```

For each raw validated edge selected into the raw projection:

1. map each endpoint to its unique mapping slot for this ordered edition pair;
2. map each endpoint to its zero-based member ordinal within that side of the accepted mapping;
3. if either endpoint lacks a final mapping slot, the edge has no normalized signature and the corresponding relation subview is marked unequal for cross-edition comparison;
4. otherwise emit the object above.

The normalized relation arrays are sorted by `(relation_type enum order, source_mapping_slot UTF-8 bytes, target_mapping_slot UTF-8 bytes, source_member_ordinal, target_member_ordinal)` and preserve duplicates when distinct raw edges normalize to the same signature.

`scope_relations` contains normalized signatures for exactly `contains`, `precedes`, `applies_subject_to`, `depends_on`, `defines`, and `exception_to`.

`reference_version_relations` contains normalized signatures for exactly `references`, `supersedes`, and `amends`.

## 8. Normalized numeric atoms

Each raw numeric atom is assigned to the mapping slot/member containing its exact SourceSpan. The normalized atom removes source coordinates and retains only the canonical comparison semantics shown in the schema.

`atom_ordinal` is dense within one mapping slot after sorting by `(member ordinal, source byte start, source byte end, comparison_dimension, operator, canonical_value UTF-8 bytes, canonical_unit with null first)`.

The final normalized numeric array is sorted by `(mapping_slot UTF-8 bytes, atom_ordinal)`.

## 9. Normalized table objects

A `NormalizedTable` is exactly:

```json
{
  "table_mapping_slot": "<mapping id>",
  "title_mapping_slots": ["<mapping ids>"],
  "header_mapping_slots": ["<mapping ids>"],
  "row_mapping_slots": ["<mapping ids>"],
  "unit_text_sha256s": ["sha256:<hex>"]
}
```

Every table/title/header/row node must have a unique final mapping slot. If a required member lacks one, the table subview is unequal. Nested mapping-slot arrays preserve the raw canonical structural order; unit hashes preserve raw `unit_source_spans` order and hash the exact unit bytes, not edition-specific coordinates.

Tables are sorted by `table_mapping_slot` UTF-8 bytes.

## 10. Cross-edition equality functions

Comparison uses exact RFC 8785 canonical JSON byte equality of the named normalized subviews; there is no fuzzy equality.

Define:

- `text_equal`: canonical bytes of `text_segments` equal;
- `classification_equal`: canonical bytes of `classifications` equal;
- `scope_equal`: both sides have all required endpoint mappings and canonical bytes of `scope_relations` equal;
- `reference_version_equal`: both sides have all required endpoint mappings and canonical bytes of `reference_version_relations` equal;
- `numeric_equal`: canonical bytes of `numeric_atoms` equal;
- `table_equal`: both sides have all required member mappings and canonical bytes of `tables` equal.

Classification provenance hashes are **not** compared for semantic equality; the selected values are compared, while provenance hashes remain authoritative audit/invalidation data in the raw projection.

## 11. Exact difference-kind decision rules

For one accepted mapping/difference context, Phase 5 emits difference records under these fixed rules. More than one semantic difference record may apply to the same one-to-one mapping.

### 11.1 Mapping-state kinds

- `mapping_unresolved`: no final mapping authority exists for the needed source/target continuation;
- `added`: final mapping kind is `added` and the exhaustive/no-continuation authority contract passes;
- `removed`: final mapping kind is `removed` and the exhaustive/no-continuation authority contract passes;
- `split`: final mapping kind is `split`;
- `merged`: final mapping kind is `merged`;
- `renumbered`: final mapping kind is `renumbered_continuation`.

These mapping-state kinds do not depend on raw ID equality.

### 11.2 One-to-one semantic kinds

For `exact_continuation`, `renumbered_continuation`, or `reworded_continuation` one-to-one mappings:

- `text_changed` iff `text_equal == false`;
- `scope_changed` iff `scope_equal == false` **or** the aligned `node_type` values differ;
- `modality_changed` iff any aligned `normative_status` or `source_modality` value differs;
- `numeric_changed` iff `numeric_equal == false`;
- `table_changed` iff `table_equal == false`;
- `relationship_changed` iff `reference_version_equal == false`;
- `unchanged` iff the mapping kind is `exact_continuation` and all six equality functions are true and aligned `node_type` values are equal.

`renumbered_continuation` always emits `renumbered`; it may additionally emit semantic difference records when another subview differs, but never emits `unchanged` because renumbering itself is a reported version difference.

`reworded_continuation` may emit one or more semantic difference records and never emits `unchanged`.

`replaced` is represented by the mapping state `replaced`; because `EditionDifference` v1 does not expose a separate `replaced` difference kind, the comparison emits the applicable semantic difference records from the normalized subviews plus the referenced `clause_mapping_id`; if the design later needs a public/standalone replaced difference token it requires a schema-version change rather than overloading another kind.

## 12. Normalized-view reproducibility

The normalized view itself is not source authority and need not be stored as a release artifact, but the builder and independent release validator both recompute it from:

- the raw `EditionComparisonProjection`;
- the exact final `ClauseMapping` set for the ordered edition pair;
- this contract version.

The EditionDifference `difference_rule_id` and configuration hash bind this normalization-contract version. Any mapping change, raw projection change, or normalization-contract change invalidates affected EditionDifference records.

## 13. Phase 5 comparison identity correction

The exact `phase5_comparison` identity object from `docs/design-phase-5-identities-and-derived-records.md` continues to contain `applicability_projection_sha256`, but that field now has exactly the meaning and digest from Sections 2–3 of this document.

Release validation rejects:

- a comparison whose stored `shared_applicability_status` differs from the recomputed applicability projection;
- a stale applicability digest after any underlying parent projection/rule/model-association change;
- any `proven` comparison with an unknown/disjoint applicability dimension or incomplete required context;
- any EditionDifference whose difference kind disagrees with the normalized equality/mapping-state rules above;
- any use of raw edition-specific IDs as a substitute for the normalized equality functions.
