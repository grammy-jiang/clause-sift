# Phase 2 Canonical-ID Migration Appendix

**Project:** ClauseSift  
**Phase:** 2 — Exact Retrieval MVP  
**Status:** Normative Phase 2 implementation-plan appendix  
**Primary design authority:** `docs/design.md`  
**Upstream ground truth:** `docs/implementation/phase-0-evaluation-corpus.md`  
**Companion plan:** `docs/implementation/phase-2-exact-retrieval-mvp.md`

## 1. Purpose and boundary

Phase 0 intentionally created source-grounded evaluation identities before the production canonical model existed. Phase 2 is the first phase that creates authoritative production `document_id`, `node_id`, `chunk_id`, and `source_id` values. Therefore Phase 2 must perform a versioned, reviewed, fail-closed migration from the Phase 0 provisional/source-grounded locators to canonical Phase 2 IDs **before any retrieval, citation, classification, or release-gate score compares expected IDs with runtime output**.

This appendix implements only identity reconciliation needed by Phase 2 evaluation. It does not add Phase 3 retrieval or Phase 4 traversal behavior.

## 2. Inputs

The migration consumes the exact frozen versions of:

- Phase 0 corpus manifest and `corpus_document_id` records;
- source SHA-256 and source byte-size records;
- document code and edition labels;
- provisional evidence locators;
- printed clause/table/appendix/definition identifiers where present;
- one-based PDF page number and printed page label where present;
- exact expected source-span hash or evidence-label membership;
- Phase 0 context/classification/conflict ground-truth records that reference provisional evidence;
- Phase 2 approved manifests;
- Phase 2 canonical catalog and page-provenance artefact;
- Phase 2 chunk/source rows;
- exact schema/vocabulary versions for both sides.

The migration never accepts local filenames as identity and never uses modification time.

## 3. Document identity mapping

Create a versioned mapping from each Phase 0 `corpus_document_id` to exactly one canonical Phase 2 `document_id`.

A mapping is accepted only when all required source-grounded identity fields agree, including:

- source SHA-256;
- edition/revision identity;
- document code where Phase 0 provides it;
- source byte size where recorded;
- manifested source identity constraints;
- any other Phase 0 immutable document discriminator declared by the migration schema.

The migration must fail for that record when:

- no canonical document matches;
- more than one canonical document matches;
- source hash differs;
- edition differs;
- document code conflicts;
- an expected immutable discriminator conflicts.

There is no `latest` fallback, fuzzy title match, filename fallback, or similarity-based choice.

## 4. Evidence locator mapping

For every Phase 0 expected evidence locator, resolve canonical identity only through the mapped canonical document and exact source-grounded constraints.

The resolver may use, when present in the frozen Phase 0 label:

- canonical document mapping;
- exact normalized clause/table/appendix/definition identifier;
- one-based page number;
- printed page label;
- exact expected UTF-8 source-span hash;
- exact evidence-label membership;
- source-coordinate constraints;
- source text hash rather than a generated paraphrase.

The output records the canonical Phase 2 identities needed by applicable evaluators, including:

- `document_id`;
- `node_id` or ordered node IDs where the expected evidence spans several canonical nodes;
- `chunk_id`/`source_id` membership accepted as equivalent expected retrieval evidence;
- exact source spans/page mappings used to prove the mapping;
- the Phase 0 locator revision and Phase 2 catalog/release-build identity from which the mapping was derived.

The migration must not select the first plausible chunk. When several Phase 2 retrieval representations validly cover the same Phase 0 source evidence, the migration records the complete explicitly allowed canonical expected set according to the Phase 0 label semantics, rather than picking one representation because the current retrieval system ranks it highly.

## 5. Fail-closed conditions

A Phase 0 locator remains unresolved and blocks every dependent Phase 2 release-gate case if any of the following occurs:

- no canonical node/source satisfies all exact constraints;
- more than one semantically incompatible canonical target satisfies a supposedly exact locator;
- source SHA-256 differs;
- edition differs;
- expected text/span hash differs;
- page or clause identity cannot be reconciled;
- UTF-8 span boundaries are invalid;
- the only apparent match requires fuzzy text similarity, an LLM inference, edition substitution, or a guessed cross-reference;
- a source representation includes out-of-scope evidence that would make the expected label ambiguous;
- the mapping depends on an unreviewed change to Phase 0 ground truth.

An unresolved mapping is never converted into `not_applicable` merely to keep a denominator small. The evaluation readiness report lists it as a blocking ground-truth migration failure until corrected through the proper Phase 0 label/change-control process or Phase 2 canonical-build correction.

## 6. Migration artefact

Persist a deterministic, versioned migration artefact containing at minimum:

- migration schema version;
- Phase 0 corpus/question/label versions;
- Phase 2 manifest/catalog/schema/vocabulary identities;
- ordered document mappings;
- ordered evidence mappings;
- old provisional locators;
- new canonical IDs and exact supporting source spans;
- mapping rule ID/version;
- mapping status;
- safe reason code for every unresolved/ambiguous record;
- deterministic content hash.

Operational reviewer names/timestamps may live in a separate review/audit envelope if needed; they must not create nondeterminism in the canonical mapping bytes.

The migration artefact is evaluation ground-truth infrastructure, not runtime source authority and not a second canonical catalog.

## 7. Human-reviewed migration diff

Before the migrated labels become eligible for Phase 2 scoring, produce a human-reviewable diff showing for every changed identity:

- Phase 0 provisional locator;
- mapped document/edition;
- mapped canonical node/source identities;
- exact source-span/page evidence proving the mapping;
- ambiguity/unresolved status;
- whether one Phase 0 evidence label maps to one or several allowed Phase 2 source representations.

The review gate requires explicit approval of the complete migration set used by an evaluation split. A tool-generated or LLM-generated match cannot self-approve.

Any mapping changed after review invalidates that reviewed migration artefact and every evaluation result bound to its hash.

## 8. Held-out leakage boundary

Canonical-ID migration is necessary label reconciliation, not model/retrieval tuning. Held-out release-gate labels must remain protected under the Phase 0 split policy.

For held-out cases:

- migration tooling may access the hidden labels in the controlled evaluation path;
- implementation-time lexical/classification selection code may not read those labels or the migrated expected IDs;
- migration review is performed independently of candidate ranking output;
- the resolver must not use current retrieval scores/ranks as a matching feature;
- only after the candidate configuration is frozen may the evaluator join returned IDs to the already reviewed held-out canonical mapping.

A mapping produced by inspecting a candidate's ranked output is contaminated and cannot serve as release-gate ground truth.

## 9. Evaluation ordering gate

The Phase 2 evaluation sequence is therefore:

1. finish/freeze the Phase 2 canonical catalog, page provenance, chunks, and sources;
2. generate the Phase 0 → Phase 2 canonical-ID migration artefact using source-grounded exact rules only;
3. human-review and approve the migration diff for each evaluation split;
4. block if any required gate case remains unresolved/ambiguous;
5. perform development/benchmark selection using only the allowed non-held-out split roles;
6. freeze the candidate lexical and classification configurations;
7. run held-out evaluation by joining returned canonical IDs against the pre-reviewed canonical ground truth;
8. persist results bound to the migration artefact hash.

No Phase 2 retrieval metric is release-authoritative if its expected IDs were mapped ad hoc during or after scoring.

## 10. Tests

### 10.1 Positive migration tests

Cover:

- one exact document mapping;
- two editions of the same document code mapping to distinct canonical IDs;
- exact clause locator mapping;
- page + text-hash mapping;
- table/row evidence mapping;
- one Phase 0 evidence span legitimately covered by several Phase 2 retrieval representations;
- byte-identical rebuild reproducing the same migration bytes/hash.

### 10.2 Negative migration tests

Reject/block:

- source-hash mismatch;
- wrong edition;
- ambiguous document;
- missing document;
- ambiguous exact locator;
- text-hash mismatch;
- wrong page;
- fuzzy-only match;
- retrieval-rank-assisted mapping;
- LLM-only mapping;
- unreviewed mapping change;
- incomplete mapping for a release-gate case.

### 10.3 Gate tests

Prove that:

- lexical Recall/Top-5 scoring cannot run release-authoritatively before the applicable migration artefact is reviewed;
- classification scoring cannot run release-authoritatively before applicable node identities/labels are reconciled;
- citation deterministic tests use the same canonical document/edition/page mapping;
- a migration failure prevents activation and leaves the prior active release unchanged;
- evaluation results record the exact migration artefact hash.

## 11. Acceptance criteria

Phase 2 is not complete unless:

1. every Phase 0 document used by an applicable Phase 2 gate maps to exactly one canonical `document_id` or is a recorded blocking migration failure;
2. every expected evidence label used for Phase 2 retrieval/citation scoring has an approved source-grounded canonical mapping;
3. no accepted mapping relies on fuzzy retrieval, model output, filename coincidence, or edition substitution;
4. the complete migration diff is independently reviewed before scoring;
5. held-out mapping is completed without exposing expected IDs to candidate-selection/tuning code;
6. unresolved/ambiguous required mappings block the dependent gate rather than disappearing from its denominator;
7. release-authoritative Phase 2 results bind the exact reviewed migration artefact hash.

This migration is a Phase 2 responsibility because Phase 2 creates the production canonical identities that Phase 0 intentionally could not know.
