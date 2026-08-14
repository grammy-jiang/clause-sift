# ClauseSift Phase 5 Selected-Model Comparison Contract

- **Status:** Normative Phase 5 detailed-design correction
- **Parents:** `docs/design-phase-5.md`, `docs/design-phase-5-provenance-and-projections.md`, `docs/design-phase-5-comparison-normalization.md`, `docs/design-phase-5-final-corrections.md`
- **Parent design:** `docs/design.md`
- **Scope:** concrete product-model identity for Phase 5 standard/product comparisons

This document supersedes any earlier Phase 5 comparison field that permits product-parameter records from several model associations to be combined without naming the exact product model being compared.

## 1. Every comparison targets one concrete product model

A v1 Phase 5 standard/product comparison is always about exactly one validated `ProductModel` record.

The Phase 5 comparison schema is corrected to require:

```json
"selected_product_model_id": "product_model:sha256:<hex>"
```

The selected model must resolve to one valid `phase5/product-models.jsonl` record whose manufacturer document is the same `manufacturer_specification` document that owns every product parameter used by the comparison.

There is no implicit document-wide model, model-series default, or “all associated models” comparison in v1.

If a caller/internal workflow wants to compare several concrete models, the service produces one independently identified comparison record per selected model. An adapter may group those records only after each model-specific comparison has been built and validated; the grouped presentation does not become a new comparison authority.

## 2. Corrected Phase5Comparison record

The `phase5.comparison.v1` record is corrected to exactly include the selected model:

```json
{
  "schema_version": "phase5.comparison.v1",
  "phase5_comparison_id": "phase5_comparison:sha256:<hex>",
  "subject_alignment_id": "<alignment id>",
  "selected_product_model_id": "product_model:sha256:<hex>",
  "standard_source_ids": ["<source ids>"],
  "product_parameter_record_ids": ["<product parameter ids>"],
  "shared_applicability_status": "proven|unresolved|disjoint",
  "comparison_outcome": "equivalent|meets_minimum|below_minimum|meets_maximum|above_maximum|inside_range|outside_range|incompatible_sets|not_comparable",
  "comparison_rule_id": "<rule id>",
  "comparison_rule_config_sha256": "sha256:<hex>",
  "conflict_ids": ["<existing Section 20.3 conflict ids>"]
}
```

No other field changes.

## 3. Product-parameter coverage rule

Every ProductParameter referenced by `product_parameter_record_ids` resolves through its `parameter_model_association_sha256`.

Release validation requires:

1. `selected_product_model_id` is present in that association's exact `product_model_ids` array;
2. every associated ProductModel used for this selected-model check belongs to the same manufacturer specification document as the parameter source;
3. every parameter/model association evidence span remains valid under the exact source-span/rule-or-review contract;
4. the ProductParameter's operating/application conditions used by the comparison apply to the selected model under that association.

A parameter association may legitimately cover several models, but a Phase 5 comparison consumes that parameter only in the context of the single `selected_product_model_id` named by the comparison.

A ProductParameter whose association does not contain the selected model is ineligible for that comparison and must not contribute a value, condition, applicability fact, conflict position, or output.

## 4. No mixed-model value assembly

The builder must not assemble one comparison from parameters that cannot all be proven to apply to the same selected model.

For a candidate set of product parameters:

```text
eligible_models = intersection(all referenced association.product_model_ids)
```

The requested/selected model must be a member of `eligible_models`. If the intersection does not contain the selected model, no direct comparison for that selected model is materialized from that parameter set.

The builder must not union values from model A and conditions from model B, even when both models occur in the same manufacturer specification or share a family prefix.

## 5. Corrected applicability projection

`phase5.applicability_projection.v1` is corrected to require the top-level field:

```json
"selected_product_model_id": "product_model:sha256:<hex>"
```

The product-position entry remains bound to each exact ProductParameter record and association. For every product position, applicability projection validation requires that its association contains the same top-level selected model.

All model-sensitive dimensions are evaluated for that selected model only, including:

- `product_or_equipment_class`;
- `operating_conditions`;
- `application_scope`;
- `exception_effect` where manufacturer/model applicability is relevant;
- `dependency_effect` where the product-side prerequisite is model-specific.

A condition sourced only for another model cannot contribute to the selected model's applicability state.

The applicability digest remains the existing domain-separated RFC 8785 digest, but the canonical hashed object now includes `selected_product_model_id`; selecting a different model therefore changes `applicability_projection_sha256` even when the source parameter text is shared.

## 6. Corrected comparison identity object

The exact `phase5_comparison` identity object is corrected to:

```json
{
  "identity_schema_version": "phase5.comparison.identity.v1",
  "subject_alignment_id": "<id>",
  "selected_product_model_id": "product_model:sha256:<hex>",
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

The common Phase 5 domain/hash algorithm remains unchanged. A different selected model necessarily produces a different comparison ID.

## 7. Section 20.3 conflict integration is model-specific

The Phase-5-aligned Section 20.3 conflict-candidate path may consume only product positions whose ProductParameter association contains the comparison's `selected_product_model_id`.

The selected model ID is included in the Phase-5-aligned comparable-subject/conflict-input configuration bound to the candidate-generation configuration hash. It is not added as a new public Section 20.3 conflict field, but changing the selected model changes the aligned candidate input/configuration identity and therefore prevents a conflict decision for model A from being reused for model B.

A conflict/source cover must never include a manufacturer parameter that is valid only for another model.

## 8. Runtime/internal service behavior

The internal Phase 5 comparison service requires a resolved concrete ProductModel before it can build a direct standard/product comparison.

When a search/query identifies only a product series or an ambiguous set of models, the internal result remains model-unresolved and no model-specific numeric/compliance-like comparison is produced until one concrete ProductModel is selected by source-grounded identity.

This does not create or freeze a public Section 22.2 argument; public request semantics remain blocked until the parent public schema is designed.

## 9. Required fixtures

Add fixtures proving:

- one parameter association covers models A and B; the same source value can participate in separate A and B comparison records with different comparison IDs;
- parameter P1 covers A and B while P2 covers only B: a B comparison may use both, but an A comparison cannot use P2;
- two model variants share a source parameter label but have different operating conditions; no condition crosses model identity;
- a model-series mention without an exact ProductModel leaves comparison model identity unresolved;
- a stale parameter/model association cannot validate after the selected ProductModel source/review identity changes;
- a model-A conflict candidate cannot be reused as the conflict authority for model B;
- every applicability projection recomputes to a different digest when the selected model changes.

## 10. Release validation additions

Independent release validation rejects:

- a comparison with a missing or unknown selected model;
- a selected model whose manufacturer document does not own every referenced product parameter;
- any referenced ProductParameter whose association does not contain the selected model;
- a product-side applicability/condition fact sourced only for another model;
- an applicability projection whose selected model differs from the comparison record;
- a comparison identity that omits or mismatches the selected model;
- a Phase-5-aligned conflict input containing product positions outside the selected model;
- one comparison record that blends several concrete selected models.
