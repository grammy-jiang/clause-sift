# ClauseSift Phase 5 Model-Local Condition Projection Contract

- **Status:** Normative Phase 5 detailed-design correction
- **Parents:** `docs/design-phase-5-model-condition-binding.md`, `docs/design-phase-5-comparison-normalization.md`
- **Parent design:** `docs/design.md`
- **Scope:** exact model-local condition positions and independently recomputable context projections

This document supersedes the earlier Phase 5 model-binding/applicability shape where condition source IDs and evidence spans were present but each condition's own Section 19/20 projection identity was not explicitly bound.

## 1. ConditionBinding object

Every model-local condition attached to a parameter/model association is represented by one closed `ConditionBinding` object:

```json
{
  "condition_source_id": "<source id>",
  "condition_spans": ["<SourceSpan objects>"],
  "model_scope_evidence_spans": ["<SourceSpan objects>"]
}
```

There are no other fields.

`condition_source_id` must resolve to one lower-phase source record in the same governed manufacturer specification as the parameter/model association.

`condition_spans` is non-empty and contains the exact source-grounded text interval(s) expressing the operating/applicability condition itself. Every span must be covered by the referenced source record's lower-phase chunk/node membership and page-lineage mapping.

`model_scope_evidence_spans` is non-empty unless the exact condition text itself contains the complete concrete ProductModel scope. It contains the exact source span(s) proving that this condition belongs to the enclosing `model_bindings[].product_model_id` rather than another model in the document.

Both span arrays use the existing Phase 5 SourceSpan deterministic ordering rule.

## 2. Corrected parameter-model association shape

Inside each `model_bindings[]` entry of `phase5.parameter_model_association.v1`, the fields:

```text
condition_source_ids
condition_evidence_spans
```

are removed and replaced by:

```json
"conditions": ["<ConditionBinding objects>"]
```

The final model-binding entry is therefore:

```json
{
  "product_model_id": "product_model:sha256:<hex>",
  "model_binding_evidence_spans": ["<SourceSpan objects>"],
  "conditions": ["<ConditionBinding objects>"]
}
```

`conditions` is sorted by `(condition_source_id UTF-8 bytes, first condition span SourceSpan order, remaining canonical JSON bytes)` and contains no exact duplicate canonical object.

A condition is model-local authority only through this binding. The same source condition may appear in several model bindings only when each binding independently contains the exact source/model-scope evidence proving that it applies to that model.

The existing `association_sha256` algorithm hashes this corrected structure; any condition span/model-scope ownership change therefore changes the association digest.

## 3. Independent condition position projections

For every `ConditionBinding` selected for a concrete ProductModel comparison, the builder constructs a `SelectedModelConditionProjection` exactly:

```json
{
  "condition_source_id": "<source id>",
  "condition_spans": ["<SourceSpan objects>"],
  "model_scope_evidence_spans": ["<SourceSpan objects>"],
  "comparison_projection_sha256": "sha256:<hex>",
  "required_context_projection_sha256": "sha256:<hex>"
}
```

The two projection hashes are independently recomputed for the exact condition position rather than inherited from the ProductParameter value span.

### 3.1 Comparison projection

`comparison_projection_sha256` is the exact parent Section 20.3 comparison projection over:

- `condition_source_id`;
- the complete ordered `condition_spans`;
- the exact classification provenance and source-grounded facts applicable to those condition spans;
- the active comparison rule-set version/configuration.

The builder invokes the same versioned parent comparison-projection function used by the Phase 5 applicability contract for standard/product positions. The function receives these condition positions as its exact source position and may not substitute the ProductParameter value span.

### 3.2 Required-context projection

`required_context_projection_sha256` is the exact Section 19 required-context projection rooted at the condition position(s), including every required applicability, exception, dependency, definition, table/context, resolved-reference, and conflict consequence reachable under the active lower-phase rules.

The projection function uses the exact `condition_source_id` and `condition_spans` as the seed position. If the condition has its own exception/dependency/applicability context, that context is therefore independently included and hashed even when it is not reachable from the parameter value span.

The existing lower-phase context-rule-set version/configuration, edge/occurrence identities, classification/manifest facts, and source hashes are behavior-bearing inputs. Any relevant context-edge/occurrence/source/configuration change changes this projection hash.

## 4. Corrected selected-model product position in applicability projection

The product-position entry in `phase5.applicability_projection.v1` is corrected to exactly:

```json
{
  "product_parameter_record_id": "<id>",
  "parameter_source_span": "<SourceSpan object>",
  "parameter_model_association_sha256": "sha256:<hex>",
  "selected_product_model_id": "product_model:sha256:<hex>",
  "selected_model_conditions": ["<SelectedModelConditionProjection objects>"],
  "comparison_projection_sha256": "sha256:<hex>",
  "required_context_projection_sha256": "sha256:<hex>"
}
```

The earlier flat fields:

```text
selected_model_condition_source_ids
selected_model_condition_evidence_spans
```

are invalid.

`selected_model_conditions` is built by taking exactly the `conditions` array from the unique association model binding whose `product_model_id` equals the applicability object's top-level selected model, then independently computing the two projection hashes for each condition.

The array preserves the corrected association's deterministic condition order.

Because the complete `selected_model_conditions` array is inside the closed applicability projection, the existing domain-separated applicability digest binds:

- condition source identity;
- exact condition text positions;
- exact evidence proving model ownership;
- condition-specific Section 20.3 comparison projection;
- condition-specific Section 19 required-context projection.

## 5. Reducer inputs

The Phase 5 applicability reducer may consume a model-local condition only through its `SelectedModelConditionProjection`.

For each selected condition:

- operating-condition comparison uses only the source-grounded facts in that condition's exact comparison projection;
- application-scope/exception/dependency effects use the condition's own required-context projection in addition to the parameter value position's required-context projection;
- unresolved required condition context produces the existing `unknown`/`incomplete` result and prevents `shared_applicability_status: proven`;
- a condition-specific applicable exception or unsatisfied dependency can produce the existing `excluded`/`unsatisfied` state even when the ProductParameter value span's context is otherwise complete.

The reducer must not infer condition context by scanning nearby source text or by assuming that context reachable from the value span covers the condition.

## 6. Section 20.3 aligned conflict input

When Phase 5 feeds a selected-model product position into the existing Section 20.3 conflict builder, the aligned candidate input binds the complete ordered `selected_model_conditions` projection array.

Any conflict candidate/decision for the selected model is therefore invalidated when:

- a selected condition source/span changes;
- model-scope evidence changes;
- a condition-specific exception/dependency/applicability edge changes;
- the active comparison/context rule configuration changes.

A conflict decision created before such a change cannot be reused solely because the ProductParameter value bytes are unchanged.

## 7. Required fixtures

Add fixtures proving:

- one model-local condition has its own `exception_to` edge that is not reachable from the parameter value span; the condition projection captures it and prevents a false `proven` applicability result;
- one condition has a required `depends_on` prerequisite that changes from satisfied to unsatisfied while the value span is unchanged; applicability/comparison IDs change;
- the same condition text occurs twice in one node for different model scopes; exact SourceSpan/model-scope evidence keeps the bindings distinct;
- a condition source with an unresolved required reference produces an independently incomplete condition required-context projection;
- changing one condition's context edge changes the association/applicability/conflict dependency chain without changing unrelated models' selected condition content;
- release validation rejects a selected condition whose projection hashes were copied from the ProductParameter value span rather than recomputed from the condition position.

## 8. Release validation additions

Independent release validation rejects:

- the superseded flat model-binding condition fields;
- a ConditionBinding with an empty condition span set;
- a condition span not covered by its declared source/page lineage;
- a condition lacking exact model-scope evidence when the condition text itself does not prove the model scope;
- duplicate/misordered ConditionBinding objects;
- a selected-model applicability condition not present in the referenced association's selected model binding;
- a condition comparison/required-context projection hash that does not independently recompute from that condition's exact position;
- an applicability digest that omits or alters any selected-model condition projection;
- a Section 20.3 aligned input that omits the selected condition projection dependency.
