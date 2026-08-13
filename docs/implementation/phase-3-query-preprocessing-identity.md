# Phase 3 Query Preprocessing Identity

**Project:** ClauseSift  
**Phase:** 3 — Hybrid Retrieval  
**Status:** Normative Phase 3 implementation-plan clarification  
**Primary design authority:** `docs/design.md` Sections 16, 17, 25, 26, and 27  
**Companion plan:** `docs/implementation/phase-3-hybrid-retrieval.md`

## 1. Purpose and precedence

The deterministic preprocessing applied immediately before current-query embedding is behavior-bearing retrieval configuration. A preprocessing change can change the query vector, dense ranking, RRF result, selected retrieval seeds, and therefore the evidence returned for the same request.

It is therefore insufficient to bind query preprocessing only into an optional in-process query-embedding cache key.

Where the companion Phase 3 plan omits query-preprocessing identity from the frozen candidate, release/build identity, cache invalidation, lineage, or release-gate evidence, this clarification is authoritative.

This is entirely Phase 3 scope. It does not add reranking, supporting-context expansion, or any other Phase 4 capability.

## 2. Canonical query-preprocessing contract

Phase 3 defines one versioned deterministic query-embedding preprocessing projection.

Its identity contains at minimum:

- `query_preprocessing_schema_version`;
- `query_preprocessing_rule_set_version`;
- `query_preprocessing_configuration_sha256`;
- the exact normalization implementation/producer version when that behavior is not already completely identified by the rule-set version;
- any deterministic tokenizer-facing prefix/suffix/template identity required by the selected embedding model;
- any model-required query/document role marker identity;
- the exact canonicalization rule used to derive the bytes submitted to the embedding provider.

The configuration hash is computed over the versioned canonical behavior-bearing configuration, not over mutable file paths or a prose description.

## 3. Authority boundary

Query preprocessing may perform only the deterministic operations admitted by the design and selected configuration.

It must not silently:

- remove or invert negation;
- drop numbers or units;
- remove exact document, clause, edition, or product-model anchors;
- replace identifiers with generated synonyms;
- add generated answer text;
- perform LLM rewriting;
- infer applicability, authority, normative force, or precedence;
- use a different preprocessing path in evaluation than in production.

The resulting query-preprocessing bytes are retrieval input only. They do not become source evidence or alter the authoritative query/request fields retained for diagnostics and provenance.

## 4. Frozen Phase 3 candidate identity

The **complete frozen candidate identity** used for benchmark selection and held-out confirmation includes the query-preprocessing identity alongside the other Phase 3 behavior-bearing inputs.

At minimum it includes:

- embedding model ID and revision;
- complete bound model/tokenizer asset identity;
- embedding provider/configuration identity;
- document `embedding_text` schema/configuration identity;
- **query-preprocessing schema/rule/configuration identity**;
- canonical release dtype and normalization rule;
- vector row-order identity;
- exact dense backend/metric/configuration;
- lexical and dense candidate-pool sizes;
- RRF configuration;
- query-analysis rule-set/configuration;
- classifier rule-set/configuration;
- relevant dependency-lock/toolchain identity.

Changing query preprocessing therefore creates a **new Phase 3 candidate**. Prior held-out gate results from the old preprocessing may not authorize the new candidate.

## 5. Release and build identity

The active release must bind the exact query-preprocessing behavior under which its hybrid retrieval configuration was evaluated.

The release manifest and/or its versioned behavior-configuration artifact records, as required by the existing release schema:

- query-preprocessing schema version;
- rule-set version;
- configuration SHA-256;
- producer/version identity where applicable;
- any selected model-required query-template/role-marker identity;
- the hash of the complete canonical behavior object if the release schema uses one aggregate retrieval-configuration artifact.

These values are inputs to `build_content_id`/release identity through the existing non-recursive release dependency graph.

A runtime whose supported query-preprocessing contract does not match the active release fails capability/release validation rather than applying a locally convenient preprocessing rule.

## 6. Cache identity and invalidation

The optional in-process query-embedding cache remains keyed by the exact normalized/preprocessed query bytes and model identity, but that is only a runtime optimization.

Separately, the authoritative build/release dependency model must treat query-preprocessing identity as behavior-bearing retrieval configuration.

A change to any of the following invalidates the relevant Phase 3 candidate/release evidence and every cache or derived result whose semantics depend on the query vector:

- preprocessing schema version;
- preprocessing rule-set version;
- preprocessing configuration hash;
- preprocessing producer/version when behavior-bearing;
- model-required query prefix/suffix/template/role marker;
- canonical query-byte projection rule.

The invalidation suite must demonstrate that a preprocessing change cannot reuse prior held-out confirmation evidence or a stale behavior identity merely because the document embedding matrix itself is unchanged.

## 7. Evaluation binding

Every model-selection, RRF-selection, query-classifier comparison, and final held-out retrieval-gate report records the exact query-preprocessing identity used to generate query embeddings.

The final gate report binds at minimum:

- candidate identity/hash;
- query-preprocessing schema version;
- query-preprocessing configuration hash;
- embedding model/asset identity;
- dense/RRF/classifier configuration identity;
- evaluation corpus/split identity;
- numerator, denominator, point estimate, and one-sided confidence bound for each applicable gate.

A report generated under preprocessing configuration A cannot authorize configuration B.

## 8. Evidence Lineage and retrieval provenance

Phase 3 retrieval provenance must be sufficient to reproduce why a dense/hybrid seed was selected.

For model-assisted dense retrieval, the release-bound retrieval lineage/configuration therefore identifies the query-preprocessing schema/configuration together with the embedding model/vector/RRF identities.

The public evidence item need not expose internal preprocessing bodies or mutable paths; safe version/hash identities are sufficient. Source provenance remains unchanged.

## 9. Tests

Phase 3 must include tests proving:

1. identical validated request + identical preprocessing identity produces byte-identical embedding-provider query input;
2. evaluation and production use the same preprocessing function/configuration;
3. changing preprocessing configuration changes the frozen candidate identity even when all document embeddings are unchanged;
4. changed preprocessing invalidates prior held-out release-gate authorization;
5. changed preprocessing invalidates the optional query-embedding cache where applicable;
6. runtime startup/capability validation rejects an unsupported or mismatched release-bound preprocessing version;
7. negation, numbers/units, exact identifiers, and edition anchors survive every admitted preprocessing rule according to the design contract;
8. the release manifest/build identity records the exact preprocessing version/hash;
9. retrieval lineage/provenance records the safe preprocessing identity for dense/hybrid selections;
10. rollback restores the earlier query-preprocessing identity together with the earlier model/vector/RRF/release configuration.

## 10. Acceptance criteria

Phase 3 is not complete unless:

1. query preprocessing has one deterministic versioned contract;
2. its schema/rule/configuration identity is part of the complete frozen Phase 3 candidate identity;
3. its identity is bound into the release/build identity;
4. model-selection and held-out gate reports record it;
5. a preprocessing change cannot reuse prior held-out authorization;
6. cache and invalidation tests cover it;
7. runtime capability validation requires the release-bound preprocessing contract;
8. retrieval provenance identifies it safely without changing source authority.
