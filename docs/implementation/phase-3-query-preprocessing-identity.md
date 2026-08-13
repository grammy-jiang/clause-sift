# Phase 3 Query Preprocessing Identity

**Project:** ClauseSift  
**Phase:** 3 — Hybrid Retrieval  
**Status:** Normative Phase 3 implementation-plan clarification  
**Primary design authority:** `docs/design.md` Sections 16, 17, 25, 26, and 27  
**Companion plan:** `docs/implementation/phase-3-hybrid-retrieval.md`

## 1. Purpose and precedence

The deterministic preprocessing applied immediately before current-query embedding is behavior-bearing retrieval configuration. A preprocessing change can change the query vector, dense ranking, RRF result, selected retrieval seeds, and therefore the evidence returned for the same request.

Embedding candidates may require different query instructions, prefixes, templates, tokenizer-facing separators, or query/document role markers. Phase 3 therefore does **not** freeze one global model-specific query projection before candidate model identity is known.

Instead:

1. Phase 3 first freezes one generic preprocessing schema/framework and the rules for constructing candidate-specific projections;
2. each embedding candidate then freezes its own complete model-specific query/document preprocessing projection **before that candidate is benchmarked**;
3. benchmark selection chooses the complete `(model/provider/assets/configuration, preprocessing projection)` pair;
4. only the winning candidate's already-evaluated projection becomes the production projection;
5. that winning projection is carried unchanged into RRF selection, final confirmation, release identity, and runtime.

Where the companion Phase 3 plan omits this distinction, this clarification is authoritative.

This is entirely Phase 3 scope. It does not add reranking, supporting-context expansion, or any other Phase 4 capability.

## 2. Generic preprocessing framework

Before embedding-model benchmarking begins, Phase 3 defines and implements one versioned deterministic **preprocessing framework**, not one global candidate projection.

The framework defines the closed set of behavior-bearing projection fields and canonical hashing/serialization rules that a candidate may use, including at minimum:

- `query_preprocessing_schema_version`;
- `query_preprocessing_rule_set_version`;
- normalization implementation/producer identity;
- Unicode normalization policy;
- whitespace/trim policy;
- canonical query-byte construction rule;
- identifier/number/unit preservation rules;
- model-required prefix/suffix/instruction/template fields;
- query role-marker fields;
- corresponding document role-marker or embedding-side role convention where required;
- supported separator/control-token policy where explicitly admitted by the model/tokenizer contract;
- deterministic configuration hashing rules.

The framework must be implemented before candidate benchmarking so every candidate projection is built, serialized, hashed, and evaluated through the same deterministic machinery.

## 3. Candidate-specific preprocessing projection

For each embedding candidate, once the candidate's provider/model/revision/tokenizer/asset identity and declared preprocessing requirements are known, construct and freeze a complete model-specific projection before the first benchmark query is embedded.

Its identity contains at minimum:

- generic preprocessing schema version;
- generic rule-set version;
- candidate projection schema/version where separately versioned;
- `query_preprocessing_configuration_sha256`;
- exact normalization producer/version when behavior-bearing;
- exact query prefix/suffix/instruction/template identity required by that candidate;
- exact query role-marker identity;
- exact corresponding document role-marker/embedding-role identity where required;
- separator/control-token policy where applicable;
- exact canonicalization rule used to derive bytes submitted to the provider;
- exact tokenizer/provider behavior identity needed to interpret those bytes.

The configuration hash is computed over the complete canonical behavior-bearing projection, not mutable paths or prose descriptions.

A candidate benchmark run is invalid if the candidate-specific projection was not frozen before that run.

## 4. Authority boundary

Every candidate projection may perform only deterministic operations admitted by the generic framework and design.

It must not silently:

- remove or invert negation;
- drop numbers or units;
- remove exact document, clause, edition, or product-model anchors;
- replace identifiers with generated synonyms;
- add generated answer text;
- perform LLM rewriting;
- infer applicability, authority, normative force, or precedence;
- select or mutate a prefix/template in response to held-out results.

The resulting preprocessed bytes are retrieval input only. They do not become source evidence or alter authoritative request fields.

## 5. Candidate identity and model-selection binding

The **model-selection candidate identity** is the complete candidate pair, not a model alone.

At minimum it binds:

- embedding provider/model ID and revision;
- complete bound model/tokenizer asset identity;
- embedding provider/configuration identity;
- document `embedding_text` schema/configuration identity;
- candidate-specific query-preprocessing identity;
- corresponding document role/projection identity where required by the model;
- canonical release dtype and normalization rule;
- vector row-order identity;
- exact dense backend/metric/configuration when part of the evaluated candidate;
- relevant dependency-lock/toolchain identity.

Changing the candidate-specific preprocessing projection creates a new candidate even if the model assets are unchanged.

Benchmark comparison selects a complete model+projection pair. A preprocessing projection may not be optimized after observing decisive held-out results and then attached retroactively to a previously benchmarked model.

## 6. Winning production projection

After model-selection data choose the winning candidate pair, the winner's already-evaluated query/document preprocessing projection becomes the **production preprocessing projection**.

The winning projection is then reused unchanged for:

- RRF/candidate-pool selection;
- query-classifier integration tests where dense embeddings are used;
- final Phase 3 confirmation;
- active-release behavior identity;
- runtime current-query embedding;
- rollback compatibility.

A behavior-bearing change to the winning projection after model selection invalidates the model-selection report. A behavior-bearing change after RRF selection invalidates both model- and RRF-selection evidence. The changed configuration is a new Phase 3 candidate and must repeat the applicable selection process before final confirmation.

Thus “evaluation and production use the same preprocessing” means **the winning candidate's frozen projection** is identical between the evidence that selected/confirmed the winner and production. It does not mean every rejected model candidate had to use one universal projection.

## 7. Release and build identity

The active release binds the exact winning preprocessing behavior under which its Phase 3 hybrid configuration was selected and confirmed.

The release manifest and/or versioned retrieval-configuration artifact records:

- generic preprocessing schema/rule-set versions;
- winning candidate projection identity/configuration SHA-256;
- producer/version identity where applicable;
- winning model-required query template/prefix/role-marker identity;
- corresponding document-role/projection identity where required;
- hash of the complete canonical behavior object where the release schema uses an aggregate artifact.

These values participate in build/release identity through the existing non-recursive dependency graph.

A runtime whose supported preprocessing framework or winning projection identity does not match the active release fails validation/capability checks rather than applying local convenience behavior.

## 8. Cache identity and invalidation

An optional in-process query-embedding cache is keyed by exact winning-projection output bytes plus the compatible model/release identity.

Separately, the authoritative build/release dependency model treats the winning preprocessing identity as behavior-bearing retrieval configuration.

A change to any of the following invalidates every dependent candidate/release/cache result:

- preprocessing schema version;
- rule-set version;
- winning projection configuration hash;
- preprocessing producer/version when behavior-bearing;
- model-required prefix/suffix/instruction/template;
- query or document role marker;
- separator/control-token policy where applicable;
- canonical query-byte projection rule.

The invalidation suite must prove a preprocessing change cannot reuse prior selection/final-confirmation evidence merely because document embeddings or model assets are unchanged.

## 9. Evaluation binding

### 9.1 Candidate benchmark reports

Every embedding-candidate benchmark report records that candidate's exact frozen preprocessing projection identity.

Candidate A and candidate B may legitimately have different projections when their model contracts require different instructions/role markers. Comparisons remain valid because each pair is frozen before evaluation and fully identified.

### 9.2 RRF-selection reports

RRF and candidate-pool tuning run only after a winning model+projection pair is selected. Every RRF-selection report records the winning projection identity and must use it unchanged.

### 9.3 Final confirmation

The final Phase 3 gate report binds at minimum:

- complete final candidate identity/hash;
- winning preprocessing schema/rule-set/projection identity;
- embedding model/asset identity;
- dense/RRF/classifier configuration identity;
- evaluation corpus/split identity;
- evaluated production-path identity;
- numerator, denominator, point estimate, and one-sided confidence bound for each applicable gate.

A report generated under winning projection A cannot authorize projection B.

## 10. Evidence Lineage and retrieval provenance

The winning preprocessing identity is query-independent behavior configuration and may be referenced safely by immutable release/build lineage according to the canonical Phase 3 plan.

Request-specific retrieval ranks/scores remain runtime Evidence Package assembly provenance using the existing closed schema. This clarification does not add new public Evidence Package fields.

Source provenance remains unchanged.

## 11. Tests

Phase 3 must include tests proving:

1. the generic preprocessing framework deterministically constructs candidate projections;
2. each candidate projection is frozen before the candidate's first benchmark query;
3. identical request + identical candidate projection produces byte-identical provider query input;
4. candidates with different required prefixes/templates/role markers receive distinct frozen identities;
5. model-selection reports bind the exact candidate-specific projection used;
6. the winning projection is reused byte-for-byte/identity-for-identity in RRF selection and runtime;
7. changing the winning projection after model selection invalidates model-selection evidence;
8. changing it after RRF selection invalidates both model- and RRF-selection evidence;
9. changed preprocessing invalidates prior held-out authorization and optional query-embedding caches;
10. runtime validation rejects unsupported or mismatched release-bound preprocessing identities;
11. negation, numbers/units, exact identifiers, and edition anchors survive every admitted candidate projection;
12. release/build identity records the exact winning projection version/hash;
13. rollback restores the earlier winning preprocessing identity together with the earlier model/vector/RRF/release configuration.

## 12. Acceptance criteria

Phase 3 is not complete unless:

1. one deterministic versioned generic preprocessing framework exists before model benchmarking;
2. every embedding candidate freezes its complete model-specific preprocessing projection before benchmarking;
3. model selection chooses the complete model+preprocessing pair;
4. the winning pair's projection is carried unchanged into RRF selection, final confirmation, release identity, and production;
5. candidate and winning projection identities participate in the appropriate selection/release/evaluation records;
6. a behavior-bearing projection change cannot reuse stale model/RRF/held-out authorization;
7. cache and invalidation tests cover candidate/winning preprocessing identity;
8. runtime capability validation requires the release-bound winning projection contract;
9. retrieval provenance identifies the winning preprocessing safely without changing source authority or the closed Evidence Package schema.
