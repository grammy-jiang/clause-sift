# ClauseSift Phase 5 Final Comparison Corrections

- **Status:** Normative Phase 5 detailed-design correction
- **Parents:** `docs/design-phase-5.md`, `docs/design-phase-5-identities-and-derived-records.md`, `docs/design-phase-5-comparison-normalization.md`
- **Parent design:** `docs/design.md`
- **Scope:** applicability relationship semantics and replaced-mapping difference state

Where this document conflicts with an earlier Phase 5 comparison rule, this document is authoritative.

## 1. Applicability projection relationship-state correction

The `dimension_results` object in `phase5.applicability_projection.v1` is corrected to exactly:

```json
{
  "jurisdiction": "overlap|disjoint|unknown",
  "effective_interval": "overlap|disjoint|unknown",
  "product_or_equipment_class": "overlap|disjoint|unknown",
  "operating_conditions": "overlap|disjoint|unknown",
  "application_scope": "included|excluded|unknown",
  "exception_effect": "not_excluded|excluded|unknown",
  "dependency_effect": "satisfied|unsatisfied|unknown",
  "required_context": "complete|incomplete"
}
```

No other dimension-result field is valid in v1.

## 2. Source authority for the three relationship-state dimensions

The builder derives these values only from the exact standard/product position comparison projections and required-context projections already bound into the applicability object.

### 2.1 `application_scope`

`application_scope` evaluates the complete validated `applies_subject_to` facts and manifested/structural scope consumed by the active Section 19/20 applicability rules for both exact positions.

It is:

- `included` only when the active deterministic applicability rule proves that the selected product/model/equipment/application subject lies within every required applicable scope for the compared standard position and the manufacturer position does not establish a disjoint scope;
- `excluded` only when a validated source/manifest applicability fact proves that the selected subject lies outside a required scope or the two positions' source-grounded application scopes are disjoint;
- `unknown` when the exact source-grounded facts are missing, unresolved, or insufficient to prove either result.

Textual proximity, shared labels, retrieval rank, document type, or model similarity never produces `included`.

### 2.2 `exception_effect`

`exception_effect` evaluates every applicable validated `exception_to` relationship reached by the exact required-context projections for the compared positions.

It is:

- `excluded` when a source-grounded exception applies to the selected subject/condition and, under the active deterministic exception rule, removes or qualifies the compared requirement so that the direct standard/product comparison is not applicable;
- `not_excluded` when all required exception relationships are resolved and the active rule proves that no applicable exception excludes the selected comparison;
- `unknown` when an exception relationship, its applicability condition, or the selected subject/condition is unresolved.

A merely present exception does not automatically exclude the comparison; its source-grounded applicability must be evaluated through the existing required-context/applicability rules.

### 2.3 `dependency_effect`

`dependency_effect` evaluates every required validated `depends_on` relationship and governing `defines`/required-context obligation that the active comparison depends upon.

It is:

- `satisfied` only when every required dependency relevant to the comparison is resolved and its source-grounded condition is satisfied for the selected subject/condition under the active deterministic rule;
- `unsatisfied` when a resolved required dependency proves that the selected comparison's prerequisite is not met;
- `unknown` when a required dependency or its condition is unresolved or cannot be evaluated from admitted source-grounded facts.

A completed graph traversal does not imply `satisfied`; completion only proves that all required reachable records were processed.

## 3. Corrected overall shared-applicability reducer

The v1 reducer is exactly:

1. return `disjoint` if any of these is true:
   - `jurisdiction == disjoint`;
   - `effective_interval == disjoint`;
   - `product_or_equipment_class == disjoint`;
   - `operating_conditions == disjoint`;
   - `application_scope == excluded`;
   - `exception_effect == excluded`;
   - `dependency_effect == unsatisfied`;
2. otherwise return `unresolved` if any of these is true:
   - any overlap dimension is `unknown`;
   - `application_scope == unknown`;
   - `exception_effect == unknown`;
   - `dependency_effect == unknown`;
   - `required_context == incomplete`;
3. otherwise return `proven`.

`shared_applicability_status: proven` therefore requires all four overlap dimensions to be `overlap`, `application_scope: included`, `exception_effect: not_excluded`, `dependency_effect: satisfied`, and `required_context: complete`.

A Phase 5 comparison with `shared_applicability_status != proven` must use `comparison_outcome: not_comparable`, except that existing canonical Section 20.3 conflict/explanation records remain independently visible under their own parent-design contract. Phase 5 never turns an excluded/unresolved applicability state into a direct numeric product conclusion.

The applicability-projection hash algorithm and all other fields remain exactly as defined by `docs/design-phase-5-comparison-normalization.md`; the corrected `dimension_results` object above is part of the hashed canonical bytes, so any exception/dependency/scope-state change invalidates the comparison identity.

## 4. `replaced` is a closed EditionDifference kind

The `phase5.edition_difference.v1` `difference_kind` enum is corrected to exactly:

- `unchanged`;
- `text_changed`;
- `added`;
- `removed`;
- `renumbered`;
- `split`;
- `merged`;
- `replaced`;
- `scope_changed`;
- `modality_changed`;
- `numeric_changed`;
- `table_changed`;
- `relationship_changed`;
- `mapping_unresolved`.

The exact `edition_difference` identity object therefore admits `replaced` as a normal closed enum value; no other identity field changes.

## 5. Exact replacement mapping cardinality and difference rule

A final `ClauseMapping` with `mapping_kind: replaced` must have:

- at least one `source_span` / source node; and
- at least one `target_span` / target node.

It may be one-to-one, one-to-many, many-to-one, or many-to-many. Human review remains required for v1 `replaced` authority unless a later detailed-design revision adds an exact deterministic replacement rule.

For every final `replaced` ClauseMapping, the builder emits **exactly one mandatory mapping-state EditionDifference** with:

```text
difference_kind = replaced
clause_mapping_id = that replacement mapping ID
source_node_ids = the complete ordered source-node set from the mapping
target_node_ids = the complete ordered target-node set from the mapping
source_projection_sha256 = the projection hash for the complete source side
target_projection_sha256 = the projection hash for the complete target side
difference_rule_id = phase5.replaced.v1
```

The associated rule-configuration hash binds this contract version and the active projection/normalization versions.

V1 does **not** emit `text_changed`, `scope_changed`, `modality_changed`, `numeric_changed`, `table_changed`, or `relationship_changed` records for a `replaced` mapping. Those semantic sub-differences are intentionally not authoritative for arbitrary replacement cardinalities in v1. Clients/reviewers may inspect the two source-grounded projections, but the persisted difference classification is the single `replaced` state.

If a future design needs structured sub-differences inside a replacement, it must add a versioned replacement-comparison schema/rule rather than applying the one-to-one rules implicitly.

## 6. Corrected mapping-state difference rules

The mapping-state section of `docs/design-phase-5-comparison-normalization.md` is corrected to:

- `mapping_unresolved` when required final mapping authority is absent;
- `added` for a final `added` mapping with exhaustive/no-continuation authority;
- `removed` for a final `removed` mapping with exhaustive/no-continuation authority;
- `split` for a final `split` mapping;
- `merged` for a final `merged` mapping;
- `replaced` for a final `replaced` mapping under Section 5 above;
- `renumbered` for a final `renumbered_continuation` mapping.

The one-to-one semantic rules remain limited to `exact_continuation`, `renumbered_continuation`, and `reworded_continuation`. The earlier sentence that attempted to represent `replaced` only through those semantic rules is superseded and invalid.

## 7. Release validation additions

Independent release validation now rejects:

- `shared_applicability_status: proven` when an applicable exception excludes the comparison;
- `proven` when an application-scope fact excludes or leaves scope unknown;
- `proven` when a required dependency is unsatisfied or unknown;
- a direct non-`not_comparable` Phase 5 outcome when shared applicability is not proven;
- a `replaced` mapping with an empty source or target side;
- a `replaced` mapping without exactly one mandatory `difference_kind: replaced` EditionDifference;
- semantic sub-difference records attached to a `replaced` mapping under v1;
- a `replaced` difference whose source/target node sets or projection hashes differ from the referenced ClauseMapping/projections.
