# Phase 2 Material-Conflict Closure Implementation Plan

**Project:** ClauseSift  
**Phase:** 2 — Exact Retrieval MVP  
**Status:** Normative current-design corrective implementation plan  
**Primary design authority:** `docs/design.md` Sections 19, 20.3, 21, 25-27, 29, and 35  
**Companion:** `docs/implementation/phase-2-required-context-closure.md`

## 1. Purpose

Current `docs/design.md` assigns deterministic material-conflict handling to Phase 2. This plan defines the missing build-time conflict records, release validation, runtime fixed-point closure, Evidence Package projection, warnings, limits, and tests required to bring the already merged Phase 2 plan into conformance with that ownership.

This is corrective Phase 2 work. It does not introduce Phase 3 dense retrieval or Phase 4 reranking/supporting-context behavior.

## 2. Required outcome

A Phase 2 release must make it impossible for exact or lexical ranking to hide an admitted material disagreement.

For every direct retrieval seed, the ordinary evidence service performs:

```text
ranked direct sources
  -> required Evidence Graph closure
  -> find material confirmed/unresolved conflicts intersecting selected sources
  -> attach every compiled position-cover source
  -> run required context closure for newly attached conflict sources
  -> repeat conflict/context closure to a fixed point
  -> serialize all material positions, warnings, and lineage
```

The process is deterministic, bounded, source-faithful, release-scoped, and fail-closed when complete required closure cannot fit the declared limits.

## 3. Conflict model and authority

A conflict is derived release metadata over exact source spans. It is not a symmetric `conflicts_with` graph edge and it never rewrites source text.

The implementation must preserve the design's closed lifecycle:

- `potential` — build-diagnostic only; never present in an admitted runtime release;
- `confirmed` — incompatible compliance sets or normative effects under known shared applicability, proven by an admitted deterministic rule or immutable human review;
- `explained` — a trusted typed explanation such as unit equivalence, exception, amendment, supersession, disjoint applicability, or compatible modalities;
- `unresolved` — evidence is insufficient to prove incompatibility or a valid explanation.

Release policy is exact:

- a complete `confirmed` record may ship and is always visible when material;
- `explained` is retained for audit and appears only for comparison/diagnostic intent;
- `unresolved` may ship only when every touched document is `release_tier: standard` and must emit `conflict_unresolved`;
- any unresolved record touching a `release_tier: critical` document blocks release.

No rank, model score, document recency, authority name, stricter-looking wording, lifecycle status, or document type may choose a winner unless an approved precedence rule explicitly encodes that decision.

## 4. Build-time work package A — Candidate and position identity

Implement content-addressed conflict identity exactly from the current design.

### 4.1 Conflict candidate identity

`conflict_id` is derived from a versioned canonical candidate-identity object containing at minimum:

- conflict identity-schema version;
- detector ID/version/configuration hash;
- conflict rule-set version/configuration hash;
- context rule-set version/configuration hash;
- canonical comparison-key hash;
- canonically ordered dimensions;
- canonically sorted position identities.

Serialize with RFC 8785 and use the design's domain-separated SHA-256 construction and public prefix.

### 4.2 Position identity

Each position identity binds:

- canonical comparison-projection hash;
- required-context-projection hash;
- ordered exact source-span tuples `(document_id, node_id, node_text_start, node_text_end, source_text_sha256)`.

`conflict_position_id` is separately derived from the candidate identity plus the complete position identity.

Changing source bytes, offsets, normalized structured values, applicability/context facts, relation occurrence provenance, detector/rule configuration, or the context configuration must therefore invalidate the affected position and conflict identities.

### 4.3 Tests

Prove that:

- identical complete inputs reproduce identical IDs;
- position order is canonical and independent of insertion order;
- same-offset source edits change position/conflict identity;
- applicability/exception/context changes change required-context projection and therefore identity;
- detector/rule/configuration changes invalidate identity;
- stale decision artifacts cannot attach to a changed candidate.

## 5. Build-time work package B — Required-context projection

Conflict classification consumes a strict required-context projection created before conflict closure.

For every conflict position, materialize every source/manifest/classification and typed-relation fact consumed by deterministic conflict classification, including as applicable:

- exact source-span hashes;
- approved manifest-content hashes;
- canonical classification provenance hashes;
- relationship occurrence/provenance hashes;
- required applicability/exception/dependency context produced by the Phase 2 required-context traversal.

Exclude conflict candidates, states, decisions, and review hashes from this projection so identity is non-recursive.

Release validation independently recomputes the projection and requires exact equality.

## 6. Build-time work package C — Candidate generation and comparison projection

Implement deterministic candidate detection for the initial closed dimensions:

- `edition_version`;
- `source_authority`;
- `jurisdiction`;
- `numeric_threshold`;
- `normative_statement`;
- `applicability`.

A comparison projection is strict, versioned, source-derived, and non-authoritative. It may contain only structured values needed to rerun the named comparison rule, such as:

- normalized subject key;
- source modality;
- exact decimal/rational quantity and canonical unit;
- scope IDs;
- jurisdiction IDs;
- effective interval;
- equipment/product class;
- source-span hash.

Original text and source/build lineage remain authoritative.

The initial implementation must not use an LLM to set a final conflict state. A future model-assisted detector may only propose `potential` candidates under a separately versioned design.

## 7. Build-time work package D — Deterministic classification order

Apply the design's conflict rules in fixed order.

1. Parser extraction disagreements remain parser-validation concerns; they are not release conflicts.
2. Normalize only declared comparable values using versioned unit/normalization rules.
3. Apply typed explanations from validated relations/metadata (`exception_to`, `applies_subject_to`, `supersedes`, `amends`, disjoint trusted scope).
4. Never invent applicability or precedence.
5. Resolve only through admitted deterministic decisions or immutable human review.

The builder must transition every `potential` candidate to exactly one admitted final state before catalog admission.

Natural-language incompatibility not proved by an exact rule remains `unresolved` unless immutable human review confirms or explains it.

## 8. Build-time work package E — Decision artifacts

Every final conflict state is bound to an immutable decision artifact.

Its strict payload records:

- exact `conflict_id`;
- final state;
- explanation code or null;
- precedence status;
- optional controlling position;
- approved precedence-rule ID or null;
- decision origin;
- decision schema version.

A deterministic decision additionally binds the exact classifier rule/configuration. A human-reviewed decision binds the approved review-policy version and reviewer identity.

The content hash is stored separately as `decision_artifact_sha256`.

`precedence_status` is exactly `not_applicable`, `encoded`, or `undetermined`. A controlling position is non-null exactly when precedence is `encoded`, belongs to the same conflict, and is justified by an approved precedence rule.

## 9. Build-time work package F — Canonical position source cover

For every admitted conflict position, compile a query-independent canonical source cover over its exact node-qualified spans.

### 9.1 Coverage scope

Track coverage independently for each tuple:

```text
(document_id,
 node canonical_order,
 node_id,
 node_text_start,
 node_text_end)
```

### 9.2 Candidate eligibility

At the first lexicographically uncovered byte coordinate:

1. consider sources whose `chunk_nodes` membership covers that coordinate in the same document/node;
2. classify a source as scope-contained only when all contributing memberships lie wholly inside the union of position spans for their nodes;
3. if any scope-contained source covers the coordinate, broader sources are ineligible;
4. otherwise broader sources are allowed as the source-faithful fallback.

### 9.3 Deterministic source choice

Order eligible candidates by:

1. greatest clipped advance in the current exact span, descending;
2. least total extraneous UTF-8 membership bytes outside all position spans, ascending;
3. canonical `(chunk-kind rank, chunk canonical_order, chunk_id, source_id)` ascending.

Select the first candidate, add every non-empty exact intersection to the coverage sets, assign the next dense `selection_order`, and repeat.

Failure to advance or cover every required byte blocks release.

Store `conflict_position_sources` exactly as this recomputation. A source is selected at most once per position.

## 10. Catalog persistence

Add the current design's strict conflict tables/records to `knowledge.sqlite`, with foreign keys and uniqueness sufficient to represent and independently validate:

- conflict record;
- ordered dimensions;
- positions and position order;
- exact position spans;
- canonical source-cover rows and `selection_order`;
- final decision artifact hash and decision fields;
- rule/configuration identities;
- triggering/source relationships needed for runtime inclusion reasons.

`potential` records are not persisted in an admitted runtime catalog.

Unknown states, dimensions, precedence values, orphan positions, duplicate orders, invalid source ownership, mismatched span hashes, or incomplete cover rows fail catalog/release validation.

## 11. Release validation

Independent validation must recompute or verify, without trusting builder in-memory state:

- conflict and position IDs;
- candidate/position canonical ordering;
- exact span ownership and source hashes;
- required-context projections;
- deterministic classification/explanation rules;
- decision artifact hashes and policy identity;
- critical/standard unresolved admission policy;
- complete canonical position source cover;
- conflict limits and schema/vocabulary versions;
- lineage and manifest references.

A mismatch blocks activation and leaves the previous active release unchanged.

## 12. Runtime work package G — Material conflict discovery

After each required graph closure, find every admitted `confirmed` or `unresolved` conflict whose position span intersects a selected source membership.

Discovery is based on exact catalog membership/span intersection, not clause labels or text similarity.

For every newly material conflict:

- load every position in stable order;
- load its complete compiled source cover;
- retain the actual document/edition/status of every source;
- preserve all positions even when one side ranked poorly or was filtered out as a retrieval seed.

Metadata filters constrain direct retrieval seeds only; they do not erase required context or conflict attachments.

## 13. Runtime work package H — Graph/conflict fixed point

Implement one deterministic fixed point shared with `phase-2-required-context-closure.md`.

Conceptually:

```text
required graph queue drains
  -> conflicts sorted by conflict_id
  -> positions sorted by position_order
  -> cover rows sorted by selection_order then source_id
  -> missing cover sources enter required graph queue
  -> required closure runs for those new sources
  -> repeat until graph and conflict phases add nothing
```

Required graph traversal and material-conflict closure are therefore mutually recursive only through this bounded outer fixed-point loop; conflict records are not graph edges.

Deduplicate returned source objects by release-scoped `source_id`, while retaining every independent context path, selection role, triggering conflict reason, and position reason.

Only after the required graph-and-conflict fixed point is complete may Phase 4 supporting traversal run in a high-accuracy request.

## 14. Runtime work package I — Bounds and failure semantics

Conflict closure shares the Section 19 request bounds and specifically enforces:

- maximum 64 material conflict records per request;
- at most 16 positions per conflict;
- at most 256 positions total;
- at most 1,024 conflict position spans;
- at most 1,024 conflict inclusion reasons;
- the same 128 expanded-context object, 32 paths/object, 1,024 accepted path-step, semantic-depth, structural-depth, byte, and frame-size bounds used by required closure.

Complete source bytes for selected conflict-cover sources count toward ordinary byte/frame limits.

If any required graph/conflict bound would be exceeded, return `context_limit_exceeded` and publish **no partial Evidence Package**.

Conflict sides are required evidence and are never silently truncated for latency or resource pressure.

Release validation must prove the largest single graph-and-conflict closure addressable by `get_clause` fits all declared bounds.

## 15. Runtime work package J — Evidence roles and lineage

Evidence attached only because of conflict closure has `selection_roles` including `conflict_context`.

Its assembly lineage records a conflict inclusion reason that identifies the triggering source/conflict position using only the closed Section 21 schema.

An independently retrieved source may carry both `retrieval_seed` and `conflict_context` roles.

Do not add ad-hoc provenance fields outside the closed Evidence Package schema.

## 16. Runtime work package K — `conflicts` response projection

Every ordinary evidence-bearing success includes a required `conflicts` array, empty when no material record applies.

For each material record serialize exactly the Section 21 closed shape, including:

- `conflict_id`;
- state;
- ordered dimensions;
- explanation code or null;
- precedence status;
- controlling position ID or null;
- stable ordered positions;
- canonical source IDs for every position;
- exact document/node/byte spans supporting every position.

Do not copy detector-generated prose into the public conflict record.

`confirmed` emits `evidence_conflict`. `unresolved` emits `conflict_unresolved`.

`explained` records appear only for explicit comparison/diagnostic intent and cannot be presented as unresolved disagreement.

## 17. Shared service integration

The final Phase 2 ordinary exact/lexical evidence path is:

```text
validated request
  -> exact and/or lexical direct seed selection
  -> Phase 2 required graph closure
  -> Phase 2 material-conflict closure
  -> graph/conflict fixed point
  -> strict Evidence Package serialization
  -> Python / CLI / MCP projection
```

There is one service implementation. CLI and MCP must not implement alternate conflict rules or SQL queries.

Phase 3 may later replace/extend only seed selection with dense/RRF retrieval; it inherits this exact fixed-point evidence service unchanged.

## 18. Evaluation and release gates

Add deterministic conflict fixtures covering at minimum:

- confirmed numeric incompatibility;
- compatible stricter minima/maxima that are not conflicts;
- exact unit equivalence;
- required versus recommended compatible statements;
- exception explained by `exception_to` and applicability context;
- amendment/supersession explanation;
- disjoint jurisdiction/applicability explanation;
- missing applicability producing `unresolved`;
- critical-document unresolved conflict blocking release;
- standard-only unresolved conflict shipping with warning;
- three-or-more-position conflict;
- one position whose canonical cover requires multiple source chunks;
- a broader chunk used only when no scope-contained cover exists;
- a source participating in several conflicts;
- graph closure that introduces a new conflict, whose attached side introduces additional required context;
- conflict closure reaching the fixed point deterministically.

The final held-out evidence-semantics gate must prove **zero omissions of any required material position** on applicable independently reviewed conflict cases. Missing conflict evidence is a release blocker regardless of aggregate lexical Recall@K.

## 19. Failure injection

Inject and prove fail-closed behavior for:

- corrupted conflict ID/position ID;
- stale decision artifact;
- unknown state/dimension/precedence enum;
- orphan or cross-document-invalid span;
- non-dense/duplicate `position_order`;
- incomplete canonical position cover;
- cover source that cannot advance coverage;
- mismatched required-context projection;
- unresolved conflict touching critical tier;
- graph/conflict fixed-point limit overflow;
- conflict array missing a material admitted record;
- one-sided serialization of a multi-position conflict;
- rollback to a release with a different conflict artifact/configuration.

Every blocking failure prevents activation or returns the design's typed runtime error without publishing partial evidence.

## 20. Implementation sequence

Execute in this order:

1. freeze conflict/position/decision schemas and rule identities;
2. implement canonical comparison and required-context projections;
3. implement deterministic candidate detectors;
4. implement typed explanation and exact confirmation rules;
5. implement immutable human-review decision ingestion;
6. implement conflict/position content-addressed identities;
7. implement canonical position-source cover compiler;
8. persist final conflict records and covers in the catalog;
9. implement independent release validation;
10. implement runtime span-intersection discovery;
11. integrate conflict sources with the required-context priority queue;
12. implement deterministic graph/conflict fixed point;
13. enforce conflict and shared context bounds;
14. implement closed `conflicts` and conflict-context lineage serialization;
15. integrate the shared Python service;
16. project the same behavior through CLI and MCP;
17. add deterministic, negative, corruption, and rollback tests;
18. add held-out all-material-side evidence-semantics gates;
19. update release reports and activation gates;
20. verify Phase 3 seed selection can later reuse this service without changing conflict semantics.

## 21. Acceptance criteria

Phase 2 material-conflict closure is complete only when:

1. every potential candidate transitions before runtime catalog admission;
2. conflict/position IDs are content-addressed and independently reproducible;
3. required-context projections are complete and non-recursive;
4. exact deterministic rules and immutable review are the only final-state authorities admitted by v0.1;
5. unresolved critical conflicts block release;
6. canonical source covers reproduce exactly for every admitted position;
7. a hit on any material side forces every required side into the evidence result;
8. every newly attached conflict source receives its own required graph closure;
9. graph and conflict closure terminate at the deterministic least fixed point;
10. metadata filters cannot erase required conflict/context attachments;
11. bounds fail closed with `context_limit_exceeded` and no partial package;
12. every material conflict is serialized in the required closed `conflicts` array;
13. confirmed/unresolved warnings are correct and deterministic;
14. one shared service supplies Python/CLI/MCP semantics;
15. release validation, held-out all-side conflict gates, corruption tests, activation, and rollback tests all pass;
16. no Phase 3 dense/RRF or Phase 4 reranking/supporting-context behavior is introduced by this corrective plan.
