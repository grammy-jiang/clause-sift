# ClauseSift Phase 5 Condition Review and Conflict-Identity Contract

- **Status:** Normative Phase 5 detailed-design correction
- **Parents:** `docs/design-phase-5-model-condition-binding.md`, `docs/design-phase-5-condition-projection-binding.md`, `docs/design-phase-5-selected-model-comparison.md`
- **Parent design:** `docs/design.md`
- **Scope:** immutable review authority for grouped conditions and Section 20.3 identity invalidation

This document supersedes the earlier Phase 5 condition-review wording that bound removed flat condition arrays, and it freezes how the complete selected-model condition projection enters the existing Section 20.3 conflict identity path.

## 1. Immutable condition-review artifact

When `decision_origin == human_review` for a `phase5.parameter_model_association.v1` record, `review_artifact_sha256` must identify one immutable canonical `ParameterModelAssociationReview` artifact with exactly this shape:

```json
{
  "schema_version": "phase5.parameter_model_association_review.v1",
  "parameter_source_span": "<SourceSpan object>",
  "model_bindings": [
    {
      "product_model_id": "product_model:sha256:<hex>",
      "model_binding_evidence_spans": ["<SourceSpan objects>"],
      "conditions": ["<ConditionBinding objects>"]
    }
  ],
  "review_policy_version": "<version>",
  "reviewer_id": "<reviewer id>",
  "adjudicator_id": "<id or null>",
  "decision_sha256": "sha256:<hex>"
}
```

There are no other fields.

The `model_bindings` array and each nested `conditions` array use exactly the ordering and closed schemas defined by `docs/design-phase-5-model-condition-binding.md` and `docs/design-phase-5-condition-projection-binding.md`.

The superseded flat review fields `product_model_ids`, `condition_source_ids`, and `condition_evidence_spans` are invalid in a v1 review artifact.

## 2. Review digest and byte-for-byte binding

For a review artifact, let:

```text
review_object = artifact_without_decision_sha256
review_bytes = UTF8(RFC8785_CANONICAL_JSON(review_object))
decision_digest = SHA256(
  ASCII("clausesift.phase5.parameter_model_association_review.v1")
  || 0x00
  || review_bytes
)
decision_sha256 = "sha256:" + lowercase_hex(decision_digest)
```

The file/artifact SHA-256 referenced by `review_artifact_sha256` is the SHA-256 of the complete RFC 8785 canonical artifact bytes including `decision_sha256`.

Release validation requires the association record's:

- `parameter_source_span`; and
- complete ordered `model_bindings` array, including every complete ordered `ConditionBinding`

to be byte-for-byte identical to those in the reviewed artifact.

An association cannot reuse a review artifact after regrouping condition spans, moving one condition to another model binding, changing model-scope evidence, reordering a behavior-bearing condition grouping, or changing any reviewed source span.

## 3. Deterministic association authority

When `decision_origin == deterministic_rule`, the same final grouped `model_bindings` shape is authoritative, but the association must bind the exact reviewed deterministic rule/configuration that produced every model binding and complete `ConditionBinding` grouping.

Release validation reruns the rule from the exact source spans and requires byte-for-byte equality of the resulting `model_bindings`. A deterministic rule that only proves a flat model set or flat condition set is insufficient for the v1 association schema.

## 4. Composite product-position comparison projection

For every selected-model ProductParameter position that is offered to the Phase-5-aligned Section 20.3 conflict builder, construct exactly one `Phase5AlignedProductComparisonProjection`:

```json
{
  "schema_version": "phase5.aligned_product_comparison_projection.v1",
  "product_parameter_record_id": "<product parameter id>",
  "selected_product_model_id": "product_model:sha256:<hex>",
  "parameter_model_association_sha256": "sha256:<hex>",
  "parameter_value_comparison_projection_sha256": "sha256:<hex>",
  "selected_model_conditions": ["<SelectedModelConditionProjection objects>"]
}
```

There are no other fields.

`parameter_value_comparison_projection_sha256` is the independently recomputed parent Section 20.3 comparison-projection hash rooted at the exact ProductParameter value position.

`selected_model_conditions` is byte-for-byte the complete ordered array from the closed Phase 5 applicability product position for the same selected model. It therefore contains every condition's exact source/model-scope spans plus its independent comparison and required-context projection hashes.

The exact composite digest is:

```text
projection_bytes = UTF8(RFC8785_CANONICAL_JSON(Phase5AlignedProductComparisonProjection))
digest = SHA256(
  ASCII("clausesift.phase5.aligned_product_comparison_projection.v1")
  || 0x00
  || projection_bytes
)
comparison_projection_sha256 = "sha256:" + lowercase_hex(digest)
```

For the Phase-5-aligned Section 20.3 product position, this composite digest is the position's comparison-projection identity. The unwrapped parameter-value projection hash alone is not sufficient.

## 5. Composite product-position required-context projection

For the same selected-model product position, construct exactly one `Phase5AlignedProductRequiredContextProjection`:

```json
{
  "schema_version": "phase5.aligned_product_required_context_projection.v1",
  "product_parameter_record_id": "<product parameter id>",
  "selected_product_model_id": "product_model:sha256:<hex>",
  "parameter_model_association_sha256": "sha256:<hex>",
  "parameter_value_required_context_projection_sha256": "sha256:<hex>",
  "selected_model_conditions": [
    {
      "condition_source_id": "<source id>",
      "condition_spans": ["<SourceSpan objects>"],
      "model_scope_evidence_spans": ["<SourceSpan objects>"],
      "required_context_projection_sha256": "sha256:<hex>"
    }
  ]
}
```

There are no other fields.

The condition array preserves the exact selected-model condition order but contains only the fields needed to bind required-context identity. Each condition hash is independently recomputed from that condition's exact position under the active Section 19 rules.

The exact composite digest is:

```text
projection_bytes = UTF8(RFC8785_CANONICAL_JSON(Phase5AlignedProductRequiredContextProjection))
digest = SHA256(
  ASCII("clausesift.phase5.aligned_product_required_context_projection.v1")
  || 0x00
  || projection_bytes
)
required_context_projection_sha256 = "sha256:" + lowercase_hex(digest)
```

For the Phase-5-aligned Section 20.3 product position, this composite digest is the position's required-context projection identity. The unwrapped parameter-value required-context hash alone is invalid for this path.

## 6. Existing Section 20.3 candidate identity remains canonical

Phase 5 does not create a new conflict ID schema.

Instead, the existing Section 20.3 conflict position/candidate identity consumes the corrected product-position `comparison_projection_sha256` and `required_context_projection_sha256` from Sections 4–5 above, along with the existing exact source span, comparison dimension/value, rule/configuration, applicability, and source-cover inputs required by the parent design.

Because both composite hashes include the selected ProductModel, association digest, and complete ordered selected-model condition projection, any change to a model-local condition's:

- source span;
- model-scope evidence;
- comparison projection;
- required-context projection;
- exception/dependency/applicability edge;
- association grouping;
- selected model

changes at least one existing Section 20.3 position/candidate identity input. The old conflict candidate/decision therefore cannot be reused.

## 7. Corrected Phase-5-aligned comparison-key projection

The Phase-5-aligned comparable-subject key remains a semantic subject key and does not absorb mutable condition context. It continues to bind the validated subject alignment and controlled concept IDs.

Condition/context invalidation is carried by the existing Section 20.3 position projection hashes corrected above. This preserves the parent design's separation between comparable-subject identity and source-position/context identity.

The selected ProductModel remains bound through the Phase-5-aligned candidate configuration and the composite product-position projection hashes; a model-A product position cannot share those projection hashes with model B.

## 8. Applicability/comparison consistency

For every ProductParameter used by a Phase 5 comparison, release validation requires the `selected_model_conditions` array used in:

1. the closed Phase 5 applicability projection;
2. `Phase5AlignedProductComparisonProjection`; and
3. `Phase5AlignedProductRequiredContextProjection`

to derive from the same exact selected model binding in the same `parameter_model_association_sha256`.

The comparison projection uses the complete condition objects. The required-context composite uses the exact required-context subset projection shown above. Any mismatch blocks release activation.

## 9. Required fixtures

Add fixtures proving:

- two reviewed conditions with identical flat source/evidence sets but different grouping cannot reuse the same review artifact;
- moving one condition from model A to model B changes the review/association digest and invalidates both selected-model projection chains;
- a condition-specific exception edge changes only the condition required-context hash while the parameter value span is unchanged, and still changes the canonical Section 20.3 conflict candidate/decision identity;
- a condition-specific comparison fact changes the condition comparison hash and therefore the composite product comparison hash;
- copying the parameter-value comparison/required-context hash into the Phase-5-aligned conflict position is rejected;
- applicability, conflict input, and reviewed association all reference the same exact ordered ConditionBinding grouping.

## 10. Release validation additions

Independent release validation rejects:

- a human review artifact containing superseded flat condition fields;
- an association whose grouped `model_bindings` differ from its human review artifact or deterministic rule output;
- a Phase-5-aligned product conflict position that uses the raw parameter-value projection hash instead of the required composite digest;
- a composite digest whose selected-model condition array differs from the applicability projection;
- a stale conflict candidate/decision after any selected-model condition projection/grouping change;
- reuse of a review artifact after any ConditionBinding regrouping or model reassignment.
