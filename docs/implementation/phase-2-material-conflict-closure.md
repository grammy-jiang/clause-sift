# Phase 2 Material-Conflict Closure Implementation Plan

**Project:** ClauseSift  
**Phase:** 2 — Exact Retrieval MVP  
**Status:** Normative current-design corrective implementation plan  
**Primary design authority:** `docs/design.md` Sections 19, 20.3, 21, 25-27, 29, and 31  
**Companion:** `docs/implementation/phase-2-required-context-closure.md`

## 1. Purpose

Current design assigns deterministic material-conflict handling to Phase 2. The implementation must ensure exact/lexical ranking can never hide an admitted material disagreement.

For every direct seed:

```text
required graph closure
  -> discover material confirmed/unresolved conflicts intersecting selected source membership
  -> attach each position's compiled canonical source cover
  -> run required graph closure for newly attached sources
  -> repeat graph/conflict phases to least fixed point
  -> serialize complete conflicts, warnings, roles, paths, and lineage
```

This is Phase 2 correctness work, not Phase 3 dense/RRF or Phase 4 reranking/supporting-context work.

## 2. Conflict lifecycle and authority

Use the current closed states:

- `potential` — build-diagnostic only; never in an admitted runtime release;
- `confirmed` — incompatible compliance sets/normative effects under known shared applicability, proven by admitted deterministic rule or immutable human review;
- `explained` — trusted typed explanation (unit equivalence, exception, amendment, supersession, disjoint applicability, compatible modalities, etc.);
- `unresolved` — known evidence cannot prove incompatibility or a valid explanation.

Release policy:

- complete `confirmed` may ship and is visible whenever material;
- `explained` is retained for audit and exposed only for comparison/diagnostic intent;
- `unresolved` may ship only when every touched document is standard tier and emits `conflict_unresolved`;
- any unresolved conflict touching a critical-tier document blocks release with the current design's conflict-review-required route.

Ranking/model score/recency/authority/document type/stricter-looking wording never selects a winner. Precedence is `encoded` only through an approved precedence rule.

## 3. Conflict and position identity

`conflict_id` is a content-addressed domain-separated SHA-256 over the versioned canonical candidate identity, including detector/rule/context configuration, comparison-key hash, dimensions, and canonically sorted position identities.

Each position identity binds:

- canonical comparison-projection hash;
- required-context-projection hash;
- ordered exact `(document_id,node_id,node_text_start,node_text_end,source_text_sha256)` spans.

`conflict_position_id` is separately derived from candidate identity plus complete position identity.

Source edits, offsets, normalized comparable values, applicability/exception context, relation provenance, detector/rule/context configuration, or other behavior-bearing changes invalidate affected IDs and stale decisions.

## 4. Required-context projection

Before conflict classification, compute a strict non-recursive required-context projection containing every source/manifest/classification/typed-relation fact consumed by the conflict rule, such as:

- exact source-span hashes;
- approved manifest-content hashes;
- classification provenance hashes;
- relationship occurrence/provenance hashes;
- required applicability/exception/dependency context.

Exclude conflict candidates/states/decisions/review hashes to prevent recursive identity.

Independent release validation recomputes this projection exactly.

## 5. Candidate generation and comparison projection

The initial closed conflict dimensions are:

- `edition_version`;
- `source_authority`;
- `jurisdiction`;
- `numeric_threshold`;
- `normative_statement`;
- `applicability`.

Comparison projections are strict, versioned, non-authoritative source-derived structured values needed to rerun a rule, e.g. normalized subject key, modality, exact decimal/rational quantity + canonical unit, scope/jurisdiction IDs, effective interval, equipment/product class, and source-span hash.

Original text and Evidence Lineage remain authority.

A model cannot set a final conflict state. A future model detector may only propose candidates under a separately versioned design/policy.

## 6. Deterministic classification order

Apply the design's rules in fixed order:

1. parser extraction disagreement remains parser-validation work, not a source conflict;
2. normalize only declared comparable values through versioned registries/rules;
3. apply typed explanations from validated relationships/metadata (`exception_to`, `applies_subject_to`, `supersedes`, `amends`, disjoint scope, etc.);
4. never invent applicability or precedence;
5. resolve final state only through admitted deterministic decisions or immutable human review.

Every `potential` transitions to exactly one final admitted state before runtime catalog admission.

## 7. Decision artifacts

Every final state binds one immutable decision artifact containing exact conflict ID, state, explanation code/null, precedence status, optional controlling position, approved precedence-rule ID/null, decision origin, and decision schema version.

Deterministic decisions bind exact rule/configuration. Human decisions bind approved review-policy version and reviewer identity. Store decision content hash separately.

`precedence_status` is exactly `not_applicable`, `encoded`, or `undetermined`; controlling position is non-null exactly for valid `encoded` precedence and belongs to the same conflict.

## 8. Canonical position source cover

For every admitted position compile a query-independent source cover over exact node-qualified spans:

```text
(document_id,
 node canonical_order,
 node_id,
 node_text_start,
 node_text_end)
```

At the first lexicographically uncovered coordinate:

1. find sources whose `chunk_nodes` membership covers it in the same document/node;
2. mark a source scope-contained only when all contributing memberships lie inside the union of position spans for their nodes;
3. if any scope-contained source covers the coordinate, broader sources are ineligible;
4. otherwise broader sources are allowed as the source-faithful fallback.

Order eligible candidates by greatest clipped advance (descending), least extraneous membership bytes (ascending), then canonical chunk-kind/canonical-order/chunk-ID/source-ID order.

Select the first, add every exact non-empty intersection, assign dense selection order, and repeat. Failure to advance or cover every required byte blocks release.

Persist `conflict_position_sources` exactly as the independent recomputation.

## 9. Catalog persistence and release validation

Persist strict conflict records, dimensions, positions/order, exact spans, canonical source-cover rows/order, decision hashes/fields, and rule/configuration identities with strong ownership/foreign-key/uniqueness constraints.

An admitted runtime catalog contains no `potential` state.

Independent validation recomputes/verifies:

- conflict/position IDs and ordering;
- exact source/span ownership/hashes;
- required-context projection;
- deterministic explanation/confirmation;
- decision artifacts/review policy;
- critical/standard unresolved admission;
- complete canonical position covers;
- schema/vocabulary/rule identities;
- lineage/release references.

Mismatch blocks activation and preserves the prior active release.

## 10. Runtime material-conflict discovery

After each required graph pass, find every admitted `confirmed`/`unresolved` conflict whose position span intersects a selected source membership.

Use exact catalog span/membership intersection, never clause labels/text similarity.

Load all positions and every position's canonical source cover in stable order. Preserve actual document/edition/status for all attached sources even when a side ranked poorly or falls outside direct metadata filters.

Direct filters constrain seeds only, not required conflict/context attachments.

## 11. Graph/conflict fixed point

The shared fixed point is:

```text
required graph queue drains
  -> conflicts by conflict_id
  -> positions by position_order
  -> cover rows by selection_order then source_id
  -> missing cover sources enter required graph queue
  -> required context runs for newly attached sources
  -> repeat until neither phase adds anything
```

Conflict records are not graph edges. Deduplicate returned objects by exact release-scoped source/conflict identity while retaining independent paths/roles/reasons.

Only after required fixed point completion may later Phase 4 optional supporting traversal begin.

## 12. Bounds and failure semantics

Enforce the current conflict/request limits:

- 64 material conflict records/request;
- 16 positions/conflict;
- 256 total conflict positions;
- 1,024 position spans;
- 1,024 inclusion reasons;
- shared 128 expanded objects, 32 paths/object, 1,024 accepted steps, graph depths, byte and MCP frame budgets.

Complete source bytes for conflict-cover sources count toward request/output bounds.

Any required graph/conflict overflow returns `context_limit_exceeded` and **no partial Evidence Package**. Conflict sides are required evidence and are never silently truncated.

Release validation proves the largest single closure addressable by `get_clause` fits all declared bounds.

## 13. Evidence roles, lineage, and conflicts projection

Conflict-added evidence carries `conflict_context` as applicable. An independently retrieved source may also carry `retrieval_seed`.

Assembly lineage records only the current Section 21 closed conflict reason/path fields; do not invent ad-hoc provenance.

Every evidence-bearing success has required `conflicts`, empty when no material record applies. Serialize the exact Section 21 closed shape with conflict ID/state/dimensions/explanation/precedence/positions/canonical source IDs/exact spans.

Do not copy detector-generated prose into the public conflict record.

Confirmed records emit `evidence_conflict`; admitted unresolved records emit `conflict_unresolved`; explained records are not misrepresented as unexplained conflict.

## 14. Shared service integration

The ordinary Phase 2 path is:

```text
exact/lexical seeds
  -> required graph closure
  -> material-conflict closure
  -> fixed point
  -> strict Evidence Package serialization
  -> Python / CLI / MCP evidence tools
```

Phase 3 later changes seed selection only; it inherits this conflict service unchanged.

## 15. Evaluation and release gates

Follow Section 29.4 exactly.

### Probabilistic conflict gates

- conflict-candidate recall: one-sided 95% Wilson LB **>=95%**, at least 60 applicable cases;
- confirmed/unresolved conflict precision: one-sided 95% Wilson LB **>=98%** for each applicable reported state family, at least 150 applicable cases per 98% gate;
- explained-difference precision: one-sided 95% Wilson LB **>=98%** for each applicable explanation-code family, at least 150 applicable cases per 98% gate;
- expand samples when a critical dimension/state/code/hard negative would otherwise be underrepresented.

### Deterministic completeness/all-side gate

Conflict position/source/lineage completeness, all-side runtime preservation, state/dimension ordering, and trusted-precedence serialization must have **zero failures across the complete versioned deterministic conflict conformance suite**.

### Deterministic negative gate

Explained exception/version/jurisdiction/scope/unit/modality cases misreported as confirmed conflict, unresolved/model-only candidate promotion without admissible review, and winner selection without encoded precedence must have **zero occurrences across the complete negative suite**.

These gate forms replace any earlier draft wording that invented a separate held-out 100% all-side metric.

## 16. Test matrix

Cover confirmed numeric incompatibility; compatible stricter minima/maxima; unit equivalence; required-vs-recommended compatibility; exception/amendment/supersession/disjoint-scope explanations; unresolved applicability; critical-vs-standard unresolved behavior; n-ary conflict; multi-source position cover; broader-source fallback; one source in several conflicts; graph -> conflict -> graph fixed point; complete conflict serialization; exact current bounds; and false precedence negatives.

Failure injection covers corrupted IDs, stale decisions, unknown enums, invalid spans/order, incomplete covers, cover no-progress, context-projection mismatch, unresolved critical conflict, overflow, missing/one-sided conflict serialization, and rollback across differing conflict artifacts.

## 17. Implementation sequence

1. freeze conflict/position/decision schemas/rule identities;
2. implement comparison + required-context projections;
3. implement candidate detectors;
4. implement typed explanation/confirmation rules and immutable review ingestion;
5. implement conflict/position IDs;
6. implement canonical position covers;
7. persist final conflict records/covers;
8. independently validate release conflict artifacts;
9. implement runtime span-intersection discovery;
10. integrate conflict sources with required graph queue;
11. implement fixed point/bounds;
12. implement closed conflict/lineage serialization;
13. expose via shared Python/CLI/MCP evidence service;
14. run deterministic and negative conformance suites;
15. run probabilistic conflict recall/precision gates under leakage-safe policy;
16. update reports/activation/rollback gates;
17. verify Phase 3 seeds can reuse the service unchanged.

## 18. Acceptance criteria

Phase 2 material-conflict closure is complete only when:

1. no `potential` reaches an admitted runtime catalog;
2. conflict/position identity is reproducible/content-addressed;
3. required-context projections are complete/non-recursive;
4. final-state authority follows current deterministic/review rules;
5. unresolved critical conflicts block release;
6. canonical position source covers independently reproduce exactly;
7. any material side forces every required side into the result;
8. every conflict-added source receives required graph closure;
9. graph/conflict closure reaches deterministic least fixed point;
10. direct filters cannot erase required sides;
11. bounds fail closed with no partial package;
12. complete material conflicts serialize through the closed schema;
13. warnings/precedence behavior is correct;
14. one service supplies Python/CLI/MCP evidence semantics;
15. Section 29.4 conflict candidate/precision Wilson gates pass;
16. complete deterministic conflict/all-side/precedence conformance and negative suites have zero failures/zero prohibited occurrences;
17. no Phase 3 dense/RRF or Phase 4 reranking/supporting-context work is introduced here.
