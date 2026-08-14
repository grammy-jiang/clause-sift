# Phase 5 Review Corrections

**Phase:** 5 — Version and Product Intelligence  
**Status:** Normative Phase 5 implementation-plan correction  
**Detailed design authority:** `docs/design-phase-5.md`  
**Parent authority:** `docs/design.md` Section 35

This document records the first Phase 5 review corrections. Where an earlier Phase 5 implementation-plan sentence conflicts with this document or `docs/design-phase-5.md`, the detailed design contract is authoritative.

## 1. Internal schemas are now frozen

The earlier release/interface gate correctly required Phase 5 internal schemas before implementation, but the first PR head had not yet supplied them.

`docs/design-phase-5.md` now freezes the closed internal v1 contracts for:

- edition families;
- clause mappings and mapping review authority;
- product parameter registry and records;
- standard concept registry;
- standard-to-product subject alignments;
- standard/product comparison records;
- content-addressed identity and invalidation;
- release artifacts and referential validation.

Therefore the internal-schema prerequisite is satisfied by this PR. Public Section 22.2 tools remain a separate prerequisite: no future tool becomes public until `docs/design.md` freezes its wire/API schema.

## 2. Edition-family membership excludes standalone amendments

An edition family contains only successive **full editions of the same work** under the reviewed same-work identity defined by `docs/design-phase-5.md`.

A standalone amendment document is never a family member, even when a validated `amends` edge targets a member. `amends` is consumed only as comparison context for the affected base edition/node.

Whole-edition added/removed/mapping logic must never run by pretending a partial amendment document is a complete edition.

## 3. Manufacturer parameter authority is closed in v1

V1 structured product parameters may be materialized only from a source document whose validated vocabulary value is:

```text
document_type == manufacturer_specification
```

A `technical_manual`, `design_guideline`, research document, code, standard, or other document type cannot be promoted to manufacturer parameter authority merely because it mentions a product.

Supporting another manufacturer-owned document class later requires an explicit reviewed vocabulary/ownership/provenance design change.

## 4. Comparable-subject alignment has a dedicated authority

Phase 5 must not overload any existing manifest/Evidence Graph relation to mean “same comparable engineering parameter”.

`docs/design-phase-5.md` now defines:

- `phase5/standard-concepts.json`, a versioned internal standard-concept registry; and
- `phase5/subject-alignments.jsonl`, a content-addressed source-grounded alignment decision between exact standard source spans/concepts and a product parameter concept.

A deterministic alignment requires an approved exact rule. Otherwise immutable human review is required. Similarity/model output is candidate-generation only.

These alignments are **not** new manifest relationships and do not mutate the Evidence Graph.

## 5. Added/removed requires exhaustive no-continuation authority

A clause cannot become final `added` or `removed` merely because candidate generation did not retrieve a continuation or the current review set did not accept one.

Final `added`/`removed` requires either:

1. exhaustive deterministic mapping coverage proving no continuation exists across the complete eligible node set for the edition pair; or
2. an immutable human `no_continuation` decision explicitly covering that complete edition pair and node.

Otherwise the mapping state remains `unresolved`.

Candidate recall failure must never become authoritative version-difference evidence.

## 6. Required regression fixtures

Add fixtures proving:

- a standalone amendment cannot enter an edition family but still appears as typed amendment comparison context;
- a third-party technical manual mentioning a model cannot become manufacturer parameter authority;
- a `manufacturer_specification` source can produce a parameter record only with exact model/source/span lineage;
- comparable-subject similarity without a valid alignment decision remains unresolved;
- an approved subject-alignment review attaches only to unchanged exact source spans/registry identities;
- missing mapping candidate recall leaves potential addition/removal unresolved;
- exhaustive deterministic no-continuation and immutable human no-continuation decisions can authorize added/removed respectively;
- every Phase 5 internal content-addressed ID changes after a relevant source/registry/rule/review mutation.

## 7. Implementation readiness

With `docs/design-phase-5.md` and these corrections in the same reviewed change set, Phase 5 no longer has an undefined-internal-schema blocker. Implementation may proceed against those frozen internal contracts after this plan is merged.

Public tools remain intentionally blocked until the parent Section 22 design is extended; that does not block implementation/testing of the internal Phase 5 services and release artifacts.
