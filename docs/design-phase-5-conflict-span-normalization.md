# ClauseSift Phase 5 Conflict-Span Normalization Contract

- **Status:** Normative Phase 5 detailed-design correction
- **Parent:** `docs/design-phase-5-conflict-position-cover.md`
- **Parent design:** `docs/design.md` Section 20.3
- **Scope:** canonical non-overlapping manufacturer position spans derived from overlapping Phase 5 evidence roles

This document supersedes Section 3 of `docs/design-phase-5-conflict-position-cover.md` where exact duplicate role spans were deduplicated but partially overlapping spans were not normalized.

## 1. Preserve role evidence before normalization

The `phase5.aligned_product_position_spans.v1` role projection remains unchanged and preserves every original role entry exactly as source-grounded:

- `parameter_value`;
- `model_binding`;
- `condition`;
- `condition_model_scope`.

Partially overlapping or enclosing role spans remain separate entries in that internal role projection. Role identity/auditability is therefore never lost by parent-position normalization.

Every original role `SourceSpan` is independently validated against canonical node bytes, source/chunk membership, page lineage, selected ProductModel ownership, association/review authority, and condition grouping before normalization.

## 2. Parent position spans are the interval union

The exact spans supplied to the existing Section 20.3 manufacturer conflict position are the deterministic **strict-overlap interval union** of all validated role spans.

Normalization is performed independently for each `(document_id, node_id)` pair. Spans from different documents or nodes are never merged.

For one document/node group:

1. sort original role spans by `(node_text_start, node_text_end, source_text_sha256 UTF-8 bytes)`;
2. initialize an empty output list;
3. for each span in sorted order:
   - if the output list is empty, start a new interval;
   - if `span.node_text_start < current.node_text_end`, merge it into the current interval by setting `current.node_text_end = max(current.node_text_end, span.node_text_end)`;
   - otherwise (`span.node_text_start >= current.node_text_end`), finalize the current interval and start a new one;
4. finalize the last interval.

The overlap comparison is **strict**. Exactly adjacent spans where `next.start == current.end` remain separate non-overlapping parent spans because Section 20.3 permits non-overlapping adjacency and there is no source-authority reason to invent a larger contiguous role interval.

This algorithm naturally collapses exact duplicates, containment, and transitive overlap chains into one maximal interval.

## 3. Merged SourceSpan construction

For every normalized interval, construct one parent-facing `SourceSpan` exactly:

```json
{
  "document_id": "<document id>",
  "node_id": "<node id>",
  "node_text_start": 0,
  "node_text_end": 1,
  "source_text_sha256": "sha256:<hex>"
}
```

`document_id`, `node_id`, `node_text_start`, and `node_text_end` are the normalized interval identity.

`source_text_sha256` is independently recomputed as:

```text
merged_bytes = canonical_node_utf8[node_text_start:node_text_end]
source_text_sha256 = "sha256:" + lowercase_hex(SHA256(merged_bytes))
```

It is never copied from one of the constituent role spans unless that role span is byte-for-byte the normalized interval.

Because intervals are merged only when they overlap in the same canonical node, the merged interval is the exact continuous byte union and introduces no gap not covered by at least one original span.

## 4. Deterministic parent ordering

After per-node normalization, the complete parent Section 20.3 position span array is sorted by:

```text
(document_id UTF-8 bytes,
 node canonical order,
 node_text_start,
 node_text_end,
 source_text_sha256 UTF-8 bytes)
```

Release validation requires every pair of consecutive spans in the same document/node to satisfy:

```text
previous.node_text_end <= next.node_text_start
```

Any overlap in the stored parent position is invalid.

## 5. Role-to-normalized-span reproducibility

For audit and independent validation, each original role entry deterministically maps to exactly one normalized parent span whose interval fully contains the role interval.

The mapping is recomputed; it is not stored as an independent authority field.

Validation requires:

- every role span is contained by exactly one normalized parent span;
- every normalized parent span contains at least one role span;
- the union of original role byte intervals equals the union of normalized parent byte intervals;
- no normalized interval includes a byte that is outside that union.

Thus normalization changes representation only; it does not expand or shrink the proposition evidence.

## 6. Position/candidate identity correction

The Phase-5-aligned Section 20.3 position/candidate identity binds:

1. the complete unchanged role-projection hash from `docs/design-phase-5-conflict-position-cover.md`; and
2. the normalized non-overlapping parent position span array defined here.

Changing role grouping/ownership can therefore change the role-projection hash even when the interval union remains the same, while changing source intervals changes the normalized span array and source-cover inputs.

The parameter value used for comparison remains the original exact ProductParameter value span and normalized value. A merged parent proposition interval must never be reparsed as the numeric/product parameter value.

## 7. Source cover runs after normalization

The existing Section 20.3 canonical source-cover algorithm runs only after this normalization, over the final non-overlapping parent position spans.

For each normalized span it must cover every byte under the unchanged parent rules. A source may cover all or part of several original roles because they overlap; that does not erase the original role projection or condition/model authority.

`conflict_position_sources` remains the single canonical persisted source-cover result. No Phase 5 parallel cover table is introduced.

## 8. Required fixtures

Add fixtures proving:

- the model-binding span strictly contains the parameter value span and normalizes to one parent span;
- a condition span overlaps the tail of a model-binding span and transitively merges into one maximal parent interval;
- two exactly adjacent role spans remain two parent spans;
- exact duplicate role spans collapse into one parent span while both role entries remain in the role projection;
- one physical span carrying multiple roles has one parent source cover but multiple audited roles;
- merged interval hashes are recomputed from the complete canonical node substring;
- no normalized interval contains a gap outside the union of source role spans;
- source cover and all-side evidence remain complete after normalization;
- a deliberately stored overlapping parent span array fails release validation.

## 9. Release validation additions

Independent release validation rejects:

- any original role span whose canonical substring hash is invalid;
- any stored parent position span array that differs from the recomputed strict-overlap union;
- any parent span overlap after normalization;
- any merged span hash that differs from the exact canonical node byte interval;
- any original role span not contained by exactly one normalized parent span;
- any normalized parent span containing bytes outside the union of original role spans;
- source-cover rows computed from pre-normalized overlapping spans rather than the final parent span array.
