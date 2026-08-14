# ClauseSift Phase 5 Conflict-Position Source-Cover Contract

- **Status:** Normative Phase 5 detailed-design correction
- **Parents:** `docs/design-phase-5-condition-projection-binding.md`, `docs/design-phase-5-condition-review-and-conflict-identity.md`, `docs/design-phase-5-selected-model-comparison.md`
- **Parent design:** `docs/design.md` Sections 19, 20.3, and 21
- **Scope:** complete source-backed proposition spans and canonical conflict source cover for Phase-5-aligned manufacturer positions

This document closes the remaining Phase 5 gap between condition/context identity and the parent Section 20.3 all-side evidence contract. Phase 5 does not create a second conflict-cover mechanism. Instead it freezes the complete exact span set of the selected-model manufacturer position before invoking the existing Section 20.3 source-cover algorithm.

## 1. A Phase 5 manufacturer conflict position is the complete proposition

For a Phase-5-aligned standard/manufacturer conflict candidate, the manufacturer-side position is not only the ProductParameter value substring. The source-grounded proposition also includes the evidence that binds the value to the selected concrete ProductModel and every selected-model condition that changes the meaning/applicability of that value.

For one ProductParameter `P` and selected ProductModel `M`, define the **Phase5AlignedProductPositionSpanSet** as the exact union of:

1. `P`'s exact parameter value `SourceSpan`;
2. the selected model binding's complete `model_binding_evidence_spans` proving that `P` applies to `M`;
3. every selected-model `ConditionBinding.condition_spans`;
4. every selected-model `ConditionBinding.model_scope_evidence_spans`.

No span from any other model binding is admitted.

Condition comparison/required-context projections remain identity/invalidation inputs as defined by the earlier Phase 5 contracts, but the raw source spans above are also part of the canonical conflict position so they cannot influence conflict classification while disappearing from returned all-side evidence.

## 2. Closed span-role projection

Before deduplication into the parent conflict position, the builder constructs exactly:

```json
{
  "schema_version": "phase5.aligned_product_position_spans.v1",
  "product_parameter_record_id": "<product parameter id>",
  "selected_product_model_id": "product_model:sha256:<hex>",
  "parameter_model_association_sha256": "sha256:<hex>",
  "spans": [
    {
      "role": "parameter_value|model_binding|condition|condition_model_scope",
      "condition_ordinal": 0,
      "span": "<SourceSpan object>"
    }
  ]
}
```

There are no other fields.

`condition_ordinal` is:

- `0` for `parameter_value` and `model_binding` roles;
- the zero-based ordinal of the selected-model condition in the authoritative ordered `ConditionBinding[]` array for `condition` and `condition_model_scope` roles.

The `spans` array is generated in this exact role order:

1. the single `parameter_value` span;
2. selected binding `model_binding_evidence_spans` in SourceSpan order;
3. for each selected condition in authoritative condition order:
   - that condition's `condition_spans` in SourceSpan order;
   - that condition's `model_scope_evidence_spans` in SourceSpan order.

The role projection is an internal reproducibility object. It does not replace or modify the public conflict schema.

## 3. Canonical conflict-position span set

The existing Section 20.3 manufacturer conflict position receives a deduplicated exact span set derived from Section 2.

Two role entries are the same canonical position span only when their complete `SourceSpan` objects are byte-for-byte identical. If one physical source span serves several roles, it appears once in the parent position span set while the Phase 5 role projection retains all roles.

The deduplicated parent position spans are sorted by:

```text
(document_id UTF-8 bytes,
 node canonical order,
 node_text_start,
 node_text_end,
 source_text_sha256 UTF-8 bytes)
```

Every span must belong to the same governed `manufacturer_specification` document as the ProductParameter and selected ProductModel. A cross-document model/condition span is invalid for the v1 product position.

The parameter value remains the source of the normalized comparison value/dimension. Supplemental spans do not create additional numeric values; they complete the proposition's model/condition scope.

## 4. Position identity binding

The Phase-5-aligned Section 20.3 product position/candidate identity is corrected to bind both:

- the existing composite comparison/required-context projection hashes from `docs/design-phase-5-condition-review-and-conflict-identity.md`; and
- the exact canonical position span set from Section 3 above.

The Phase 5 candidate configuration also binds the canonical hash of the complete role projection from Section 2:

```text
role_bytes = UTF8(RFC8785_CANONICAL_JSON(Phase5AlignedProductPositionSpanSet))
role_digest = SHA256(
  ASCII("clausesift.phase5.aligned_product_position_spans.v1")
  || 0x00
  || role_bytes
)
role_projection_sha256 = "sha256:" + lowercase_hex(role_digest)
```

Changing a condition span, model-binding span, condition/model ownership, selected model, or span role therefore changes the Phase 5 aligned candidate inputs and the canonical position span set.

## 5. Reuse the existing Section 20.3 source-cover algorithm

For the canonical product position spans from Section 3, the builder runs the **unchanged parent Section 20.3 canonical position source-cover algorithm** over every exact node-qualified byte interval.

At each first uncovered coordinate, it:

1. selects admitted sources covering that coordinate in the same document/node;
2. prefers scope-contained sources whenever one exists;
3. otherwise uses only the parent-design broader-source fallback;
4. applies the exact existing deterministic source ordering;
5. requires forward progress until every byte of every canonical product-position span is covered.

The resulting sources are persisted through the existing `conflict_position_sources` contract for the manufacturer position. Phase 5 does not add a parallel source-cover table or runtime-only attachment list.

Release validation independently recomputes this source cover from the complete Phase 5 product-position span set and rejects any gap, non-advancing cover, extra/missing source, wrong order, or source outside the governing manufacturer document/position spans.

## 6. Runtime all-side preservation

The existing Phase 2/Section 20.3 runtime conflict fixed point remains unchanged.

When a Phase-5-aligned material conflict is discovered, runtime attaches every canonical `conflict_position_sources` source for every position. Because the manufacturer position cover now spans the parameter value, selected-model binding evidence, condition text, and condition model-scope evidence, those source-backed records are necessarily included in the conflict evidence package even if a condition is not otherwise reachable through an Evidence Graph edge.

Every newly attached cover source enters the existing required graph queue. Its own required context and material conflicts are processed by the existing graph → conflict → graph fixed point.

Thus a model-local condition may not affect a conflict decision unless the source evidence supporting that condition is also reproducibly materialized into all-side evidence.

## 7. Interaction with condition-specific context projections

The position span cover and condition projections serve different required purposes:

- the canonical span/source cover guarantees that the condition/model-scope **source evidence itself** is present;
- each condition's comparison projection binds source-grounded comparison/classification facts;
- each condition's required-context projection binds its Section 19 applicability/exception/dependency/context consequences.

A source-cover success does not replace condition context traversal, and a condition projection hash does not replace source materialization. Both must validate.

If a selected condition has required context outside the condition/model-scope spans, the condition's required-context projection and the existing required fixed point attach those additional graph/conflict consequences. The canonical conflict position source cover is responsible for the proposition's own explicit source spans, not every transitive required-context source.

## 8. No unrelated context promotion

The Phase 5 position span set is closed to the four role families in Section 1.

It must not include:

- nearby prose merely because it is in the same clause/table;
- condition evidence from another ProductModel binding;
- optional supporting/diagnostic context;
- model-generated explanation text;
- sources selected by retrieval rank rather than exact span coverage.

This prevents Phase 5 from expanding a conflict position into arbitrary surrounding manufacturer material.

## 9. Required fixtures

Add fixtures proving:

- a selected-model condition outside the ProductParameter value span and unreachable by graph edges is covered by `conflict_position_sources` and returned in all-side evidence;
- a condition model-scope span is covered even when the condition text itself omits the model identifier;
- the same physical span serving `model_binding` and `condition_model_scope` roles is deduplicated once in the parent position span set but retains both roles in the role projection;
- a ProductParameter value shared by models A and B yields different canonical product-position span sets when their selected-model condition/model-scope evidence differs;
- a model-B condition/source can never enter model-A position spans or cover sources;
- changing one condition span or model-scope span changes the aligned candidate/position identity and forces source-cover recomputation;
- an exact condition span with no admitted covering source blocks release rather than allowing a conflict with missing evidence;
- newly attached condition cover sources enter the normal required graph/conflict fixed point and preserve their own required context.

## 10. Release validation additions

Independent release validation rejects:

- a Phase-5-aligned product conflict position whose exact span set differs from the closed role-derived span set;
- a role projection whose selected model/association differs from the comparison/applicability records;
- a condition/model-scope span from another model or document;
- any byte of any canonical product-position span lacking deterministic source cover;
- missing/extra/misordered `conflict_position_sources` relative to the recomputed parent algorithm;
- a material conflict whose manufacturer position uses condition projections but omits the corresponding condition/model-scope spans from the position source cover;
- a runtime/evaluation fixture that drops a Phase 5 product-position cover source from all-side evidence.
