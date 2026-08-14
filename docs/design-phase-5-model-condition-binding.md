# ClauseSift Phase 5 Model-to-Condition Binding Contract

- **Status:** Normative Phase 5 detailed-design correction
- **Parents:** `docs/design-phase-5-provenance-and-projections.md`, `docs/design-phase-5-selected-model-comparison.md`
- **Parent design:** `docs/design.md`
- **Scope:** source-grounded per-model applicability and operating-condition binding for product parameters

This document supersedes the earlier Phase 5 parameter/model association shape that stored one flat model-ID set alongside condition sources that were not assigned to individual models.

## 1. Parameter/model association is per-model

The final v1 `phase5.parameter_model_association.v1` record is exactly:

```json
{
  "schema_version": "phase5.parameter_model_association.v1",
  "association_sha256": "sha256:<hex>",
  "parameter_source_span": "<SourceSpan object>",
  "model_bindings": [
    {
      "product_model_id": "product_model:sha256:<hex>",
      "model_binding_evidence_spans": ["<SourceSpan objects>"],
      "condition_source_ids": ["<source ids>"],
      "condition_evidence_spans": ["<SourceSpan objects>"]
    }
  ],
  "decision_origin": "deterministic_rule|human_review",
  "rule_id": "<rule id or null>",
  "rule_config_sha256": "sha256:<hex>|null",
  "review_artifact_sha256": "sha256:<hex>|null"
}
```

There is no top-level `product_model_ids` field and no unscoped condition list.

`model_bindings` is non-empty, contains at most one entry per ProductModel ID, and is sorted by raw UTF-8 `product_model_id` bytes.

Within each binding:

- `model_binding_evidence_spans` is the complete exact source-grounded evidence that proves the parameter occurrence applies to that concrete model;
- `condition_source_ids` contains only condition/context sources that apply to that concrete model for this parameter occurrence;
- `condition_evidence_spans` contains the exact source spans that establish those conditions and their applicability to the concrete model.

The two condition arrays may be empty only when the source-backed parameter is unconditional for that model under the admitted rule/review decision.

No condition may be attached to a model binding merely because it occurs in the same document, table, section, or model family.

## 2. Model-binding authority

A deterministic association rule may create one model binding only when exact source structure proves both:

1. the parameter value applies to the named ProductModel; and
2. every included condition source/span applies to that same ProductModel/value occurrence.

Examples may include a validated table column headed by one exact model identifier, or a source block whose explicit model scope governs both the parameter and condition rows.

If source structure leaves model-to-condition ownership ambiguous, immutable human review is required. The review artifact binds:

- exact `parameter_source_span`;
- complete ProductModel identities;
- each model's `model_binding_evidence_spans`;
- each model's `condition_source_ids` and `condition_evidence_spans`;
- rule/review policy version and source hashes.

A review for a shared parameter value cannot authorize a condition for a model that was not explicitly included in that model's reviewed binding.

## 3. Association digest

`association_sha256` is recomputed exactly as:

```text
association_object = record_without_association_sha256
association_bytes = UTF8(RFC8785_CANONICAL_JSON(association_object))
digest = SHA256(
  ASCII("clausesift.phase5.parameter_model_association.v1")
  || 0x00
  || association_bytes
)
association_sha256 = "sha256:" + lowercase_hex(digest)
```

Changing one model's condition sources/evidence changes the association digest even if the parameter value and other model bindings are unchanged.

## 4. ProductParameter correction

The final v1 ProductParameter record continues to reference:

```json
"parameter_model_association_sha256": "sha256:<hex>"
```

but the earlier ProductParameter `condition_source_ids` field is removed. Conditions are authoritative only through the validated per-model binding in the referenced association.

The exact `product_parameter` identity object likewise contains the association digest but no independent flat condition-source array. This prevents a ProductParameter identity from carrying conditions whose model ownership is undefined.

Source/table/header context that is not a model-specific operating/applicability condition remains represented through the existing lower-phase source/context lineage rather than this association.

## 5. Selected-model lookup

For a Phase 5 comparison with:

```text
selected_product_model_id = M
```

each referenced ProductParameter resolves its association and selects exactly the unique `model_bindings[]` entry whose `product_model_id == M`.

If no such entry exists, that ProductParameter is ineligible for the comparison.

For all referenced ProductParameters, the comparison's selected-model eligibility is therefore:

```text
all(
  exactly_one_model_binding(parameter.association, M)
  for parameter in comparison.product_parameter_record_ids
)
```

The earlier conceptual intersection of flat model-ID arrays is superseded by this exact per-record binding rule.

## 6. Applicability projection correction

For each product position in `phase5.applicability_projection.v1`, the final shape is corrected to include the selected model's binding state:

```json
{
  "product_parameter_record_id": "<id>",
  "parameter_source_span": "<SourceSpan object>",
  "parameter_model_association_sha256": "sha256:<hex>",
  "selected_product_model_id": "product_model:sha256:<hex>",
  "selected_model_condition_source_ids": ["<source ids>"],
  "selected_model_condition_evidence_spans": ["<SourceSpan objects>"],
  "comparison_projection_sha256": "sha256:<hex>",
  "required_context_projection_sha256": "sha256:<hex>"
}
```

The selected condition arrays are copied byte-for-byte from the unique model binding for the comparison's top-level `selected_product_model_id`. They are not unions over the association's other model bindings.

`selected_model_condition_source_ids` is deduplicated and sorted by the existing evidence/source ordering rule. `selected_model_condition_evidence_spans` uses the existing SourceSpan ordering rule.

The top-level applicability projection's selected model must equal every product-position `selected_product_model_id`.

Because these fields are part of the closed applicability object, the existing applicability digest automatically binds the exact selected-model conditions/evidence.

## 7. Condition evaluation is model-local

The `operating_conditions`, `application_scope`, `exception_effect`, and `dependency_effect` reducers may consume manufacturer-side condition facts only from the selected model binding of each referenced ProductParameter plus the lower-phase required-context projection for those exact condition sources.

They must not consume:

- condition sources from another model binding in the same association;
- model-family conditions not proven to apply to the selected concrete model;
- nearby table/section conditions lacking an exact binding rule/review;
- conditions from a ProductParameter that is itself ineligible for the selected model.

If selected-model condition ownership is incomplete or unresolved, the applicable dimension is `unknown`, which prevents `shared_applicability_status: proven` under the existing reducer.

## 8. Section 20.3 integration correction

The Phase-5-aligned Section 20.3 conflict-candidate input for the manufacturer/product side includes only:

- ProductParameters eligible for the selected model; and
- condition/applicability context from those ProductParameters' selected-model bindings.

The candidate-generation configuration identity binds the selected ProductModel ID, association digests, and exact selected-binding condition projection. A model-B condition cannot participate in a model-A conflict candidate even when the underlying ProductParameter source value is shared.

## 9. Required fixtures

Add fixtures proving:

- one shared value applies to A and B but only B has a high-temperature condition: A's comparison contains no B condition;
- one shared value has different operating ranges for A and B: separate A/B applicability digests and comparison IDs are produced;
- a table heading proves a value applies to A and B but a footnote condition explicitly applies only to B;
- ambiguous condition ownership forces human review or an unresolved applicability state rather than condition sharing;
- changing only B's condition does not change A's selected condition content, but changes the association digest and therefore invalidates/rebuilds affected records under the normal dependency closure;
- a ProductParameter with no selected-model binding is rejected from that model's comparison;
- a model-A Section 20.3 aligned conflict input cannot contain a condition source assigned only to model B.

## 10. Release validation additions

Independent release validation rejects:

- duplicate ProductModel IDs in one association's `model_bindings`;
- a model binding whose ProductModel belongs to a different manufacturer specification document from the parameter source;
- condition sources/evidence that do not resolve to source-grounded records in the same governed manufacturer context;
- a ProductParameter carrying the superseded flat `condition_source_ids` field;
- a comparison product position without exactly one binding for its selected model;
- selected-model condition arrays that differ from the referenced association binding;
- an applicability/conflict input containing conditions from any non-selected model binding.
