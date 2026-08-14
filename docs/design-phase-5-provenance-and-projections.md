# ClauseSift Phase 5 Provenance and Projection Contract

- **Status:** Normative Phase 5 detailed-design extension
- **Parents:** `docs/design-phase-5.md`, `docs/design-phase-5-identities-and-derived-records.md`
- **Parent design:** `docs/design.md`
- **Scope:** same-work authority, product-model provenance, exact mapping/alignment spans, value binding, and edition comparison projections

This document supersedes any earlier Phase 5 field that carried an authoritative work/model/span/value fact without the exact provenance required below.

## 1. New reviewed authority artifacts

The Phase 5 release/build input set adds these immutable reviewed artifacts:

```text
phase5/edition-family-registrations.jsonl
phase5/product-models.jsonl
phase5/parameter-model-associations.jsonl
```

They are checksummed release/build inputs under the same exhaustive artifact-table and canonical-JSON rules as the other Phase 5 artifacts.

## 2. Same-work edition-family registration

A bare `work_key` is insufficient authority. Edition-family membership is authorized by an immutable reviewed registration.

### 2.1 Registration record

Each `phase5/edition-family-registrations.jsonl` record is exactly:

```json
{
  "schema_version": "phase5.edition_family_registration.v1",
  "work_key": "<reviewed stable work key>",
  "document_ids": ["<full-edition document ids>"],
  "document_identity_sha256s": ["sha256:<hex>"],
  "review_policy_version": "<version>",
  "reviewer_id": "<reviewer id>",
  "adjudicator_id": "<id or null>",
  "decision_sha256": "sha256:<hex>"
}
```

`document_ids` is sorted by raw UTF-8 ID bytes for the registration artifact. `document_identity_sha256s` is positionally aligned and is the existing lower-phase reviewed document/manifest identity hash for that document. Every listed document must be a full edition of the same work. Standalone amendments are forbidden.

`decision_sha256` is the SHA-256 of the UTF-8 RFC 8785 canonical JSON bytes of the same record with `decision_sha256` omitted. Review identity fields are part of the decision and therefore invalidate the registration when changed.

### 2.2 Edition-family binding

The `EditionFamily` record and `edition_family` identity object are corrected to add:

```json
"family_registration_sha256": "sha256:<hex>"
```

The `work_key` and member set must byte-for-byte match the referenced reviewed registration. The family cannot exist from a generated title/code grouping alone.

## 3. Authoritative product-model provenance

The lower-phase catalog does not define product-model identity. Phase 5 therefore introduces a source-grounded ProductModel record rather than accepting a bare `product_model_id` string.

### 3.1 Product-model ID derivation

Product-model records use the common Phase 5 ID algorithm with:

```text
K = product_model
ASCII domain = "clausesift.phase5.product_model.v1" || 0x00
```

`product_model` is added to the closed Phase 5 ID-kind set.

### 3.2 SourceSpan object

Where this document says `SourceSpan`, the object is exactly:

```json
{
  "document_id": "<document id>",
  "node_id": "<node id>",
  "node_text_start": 0,
  "node_text_end": 1,
  "source_text_sha256": "sha256:<hex>"
}
```

Offsets are inclusive/exclusive UTF-8-byte offsets into canonical node text and satisfy the lower-phase span/page-lineage rules. SourceSpan arrays are sorted by `(document_id UTF-8 bytes, node canonical order, node_text_start, node_text_end, source_text_sha256)`.

### 3.3 ProductModel record

Each `phase5/product-models.jsonl` record is exactly:

```json
{
  "schema_version": "phase5.product_model.v1",
  "product_model_id": "product_model:sha256:<hex>",
  "manufacturer_document_id": "<manufacturer_specification document id>",
  "model_identifier_text": "<exact source-backed model identifier>",
  "model_identifier_spans": ["<SourceSpan objects>"],
  "decision_origin": "deterministic_rule|human_review",
  "rule_id": "<id or null>",
  "rule_config_sha256": "sha256:<hex>|null",
  "review_artifact_sha256": "sha256:<hex>|null"
}
```

The manufacturer document must validate as `document_type == manufacturer_specification`. Every model span must belong to that same document.

A deterministic rule may establish model identity only from an exact model-label/value structure defined by a reviewed rule. Ambiguous series/model variants require immutable human review. A filename or query token is not model authority.

### 3.4 Product-model identity object

The exact identity object is:

```json
{
  "identity_schema_version": "phase5.product_model.identity.v1",
  "manufacturer_document_id": "<id>",
  "model_identifier_text_sha256": "sha256:<hex>",
  "model_identifier_spans": ["<ordered SourceSpan objects>"],
  "decision_origin": "deterministic_rule|human_review",
  "rule_id": "<id or null>",
  "rule_config_sha256": "sha256:<hex>|null",
  "review_artifact_sha256": "sha256:<hex>|null"
}
```

`model_identifier_text_sha256` hashes exactly `UTF8(model_identifier_text)`.

## 4. Exact parameter-to-model association

A manufacturer specification can contain several model variants. The ProductParameter value occurrence therefore requires an explicit association to the model(s) for which the source says the value applies.

### 4.1 Association record

Each `phase5/parameter-model-associations.jsonl` record is exactly:

```json
{
  "schema_version": "phase5.parameter_model_association.v1",
  "association_sha256": "sha256:<hex>",
  "parameter_source_span": "<SourceSpan object>",
  "product_model_ids": ["<product_model ids>"],
  "association_evidence_spans": ["<SourceSpan objects>"],
  "decision_origin": "deterministic_rule|human_review",
  "rule_id": "<id or null>",
  "rule_config_sha256": "sha256:<hex>|null",
  "review_artifact_sha256": "sha256:<hex>|null"
}
```

`product_model_ids` is non-empty, deduplicated, and sorted by raw UTF-8 ID bytes. Every model belongs to the same manufacturer specification document as the parameter source span. `association_evidence_spans` contains the exact headers/labels/section text that establish which models the value applies to; it may include the model identifier spans themselves.

`association_sha256` is SHA-256 of:

```text
ASCII("clausesift.phase5.parameter_model_association.v1") || 0x00 || UTF8(RFC8785_CANONICAL_JSON(record_without_association_sha256))
```

If a table row/column deterministically binds a value to one model, a reviewed structural rule may authorize it. Ambiguous shared values require human review. There is no implicit “all models in the document” default.

### 4.2 ProductParameter correction

The ProductParameter schema is corrected to remove the bare `product_model_id` field and instead require:

```json
"parameter_model_association_sha256": "sha256:<hex>"
```

Exact-model lookup joins through the validated association record. If one value explicitly applies to several models, the one source value record remains single and the association contains the complete model set; adapters may project per-model matches without inventing duplicate source evidence.

The `product_parameter` identity object replaces `product_model_id` with `parameter_model_association_sha256`.

## 5. Product parameter value is byte-for-byte bound to the cited span

For every ProductParameter record, let:

```text
cited_bytes = canonical_node_utf8[node_text_start:node_text_end]
value_bytes = UTF8(source_value_text)
```

Release validation requires all of these equalities:

```text
cited_bytes == value_bytes
SHA256(cited_bytes) == source_text_sha256
SHA256(value_bytes) == source_value_text_sha256
```

The deterministic parser/normalizer receives exactly `source_value_text`; it may not normalize text outside the cited range. A nearby real span cannot validate a fabricated or different source value.

If source formatting requires inherited table/header context, that context is represented separately by existing source/context IDs; the parameter's value span itself still exactly equals `source_value_text`.

## 6. Exact mapping source/target spans

Phase 5 mapping candidates, mapping decisions, and mapping review artifacts are corrected to replace parallel node-ID/span-hash arrays with exact `SourceSpan` arrays:

```json
"source_spans": ["<SourceSpan objects>"],
"target_spans": ["<SourceSpan objects>"]
```

For a given mapping side, every SourceSpan document ID must equal that side's document ID. Candidate/mapping identity objects include the complete ordered SourceSpan arrays. Human mapping review binds those exact spans plus the mapping-universe digest.

This prevents identical text occurrences in one node from becoming interchangeable mapping evidence.

## 7. Exact standard spans for subject alignment

The SubjectAlignment schema is corrected to replace:

```text
standard_node_ids + standard_span_hashes
```

with:

```json
"standard_spans": ["<SourceSpan objects>" ]
```

Every standard span belongs to `standard_document_id`. The exact `subject_alignment` identity object includes the complete ordered SourceSpan array. Deterministic rules and human review artifacts bind the same exact coordinates.

The Phase-5-aligned Section 20.3 path consumes these exact tuples directly when deriving conflict positions/source covers, so identical wording at different locations cannot produce an ambiguous conflict origin.

## 8. Frozen edition comparison projection

`source_projection_sha256` and `target_projection_sha256` in an EditionDifference record are derived from one exact closed projection schema. Implementers may not select an ad-hoc set of “relevant” facts.

### 8.1 EditionComparisonProjection schema

For one side's mapped node set, construct exactly:

```json
{
  "schema_version": "phase5.edition_projection.v1",
  "source_spans": ["<SourceSpan objects>"],
  "classification_records": [
    {
      "node_id": "<node id>",
      "classification_sha256": "sha256:<existing exact classification provenance hash>"
    }
  ],
  "structural_edge_ids": ["<edge ids>"],
  "applicability_edge_ids": ["<edge ids>"],
  "dependency_edge_ids": ["<edge ids>"],
  "exception_edge_ids": ["<edge ids>"],
  "reference_edge_ids": ["<edge ids>"],
  "version_edge_ids": ["<edge ids>"],
  "numeric_atoms": [
    {
      "source_span": "<SourceSpan object>",
      "comparison_dimension": "<existing closed comparison dimension>",
      "operator": "eq|min|max|range|set",
      "canonical_value": "<exact canonical decimal/rational/set encoding>",
      "canonical_unit": "<unit or null>"
    }
  ],
  "table_records": [
    {
      "table_node_id": "<node id>",
      "table_source_ids": ["<source ids>"],
      "title_node_ids": ["<node ids>"],
      "header_node_ids": ["<node ids>"],
      "row_node_ids": ["<node ids>"],
      "unit_source_spans": ["<SourceSpan objects>"]
    }
  ]
}
```

There are no other fields.

### 8.2 Deterministic projection selection

For the node set represented by one EditionDifference side:

1. `source_spans` is the complete ordered set of source-bearing canonical-node text intervals admitted for those nodes under the lower-phase source mapping; no padding outside the nodes is added;
2. `classification_records` contains exactly one record for every projected node with the lower-phase classification-provenance hash required by the canonical catalog/lineage contract, sorted by node canonical order;
3. each edge array contains every validated edge of that relationship family with at least one endpoint in the projected node set and whose other endpoint is required by the existing direct comparison/context projection rule; arrays are deduplicated and sorted by raw UTF-8 edge-ID bytes;
4. `numeric_atoms` contains every value atom produced by the existing exact Section 20.3 numeric/set parser for the projected spans, sorted by `(source_span order, comparison_dimension, operator, canonical_value UTF-8 bytes, canonical_unit UTF-8 bytes with null first)`;
5. `table_records` contains every table node in the projected node set plus its existing required title/header/row/unit context, sorted by table node canonical order; nested ID arrays use lower-phase canonical node/source order and unit spans use SourceSpan order.

The relationship families are fixed as:

- structural: `contains`, `precedes`;
- applicability: `applies_subject_to`;
- dependency: `depends_on`, `defines` under the existing typed endpoint rules;
- exception: `exception_to`;
- reference: ordinary resolved `references`;
- version: `supersedes`, `amends`.

Unresolved references are not converted to edge IDs; their effect remains visible through the lower-phase warning/diagnostic state and cannot be guessed into the projection.

### 8.3 Projection hash bytes

The exact projection digest is:

```text
projection_bytes = UTF8(RFC8785_CANONICAL_JSON(EditionComparisonProjection))
digest = SHA256(ASCII("clausesift.phase5.edition_projection.v1") || 0x00 || projection_bytes)
projection_sha256 = "sha256:" + lowercase_hex(digest)
```

No document ID, edition string, or Phase 5 difference kind is inserted into the projection hash; those are already bound by the EditionDifference identity. The projection is the deterministic source-grounded content/structure/classification view of that side.

### 8.4 Difference rules consume fixed projection fields

Each closed difference kind has a fixed field family:

- `unchanged`: all projection fields equal under the rule's cross-edition identity-insensitive comparison;
- `text_changed`: `source_spans` source-text bytes differ after accepted mapping while relevant non-text interpretation is separately reported when changed;
- `scope_changed`: structural/applicability/dependency/exception arrays differ;
- `modality_changed`: `classification_records` differ in the exact source-modality/normative-status projections identified by the lower-phase classification hashes;
- `numeric_changed`: `numeric_atoms` differ;
- `table_changed`: `table_records` differ;
- `relationship_changed`: reference/version edge arrays differ;
- `renumbered`, `split`, `merged`, `added`, `removed`, `mapping_unresolved`: mapping state/cardinality/no-continuation authority determines the kind, while projection hashes bind any present side.

A versioned `difference_rule_id` and configuration hash may choose reporting granularity but may not change which projection fields exist or how they are hashed.

## 9. Product-model and projection release validation

Release validation now also requires:

- every ProductModel identifier span byte-for-byte contains the declared exact `model_identifier_text` under its rule/review contract;
- every parameter-model association references existing ProductModel records in the same `manufacturer_specification` document as the parameter source;
- every ProductParameter association exists and its parameter source span exactly matches the ProductParameter value span;
- every ProductParameter cited byte range equals `UTF8(source_value_text)` as Section 5 requires;
- every mapping/subject-alignment SourceSpan recomputes its exact substring hash and page-lineage projection;
- every edition projection is independently recomputed from the lower-phase catalog/graph/source mappings under Section 8 and hashes exactly;
- every EditionDifference rule consumes only the fixed projection/state fields assigned above.

Any mismatch blocks candidate activation.
