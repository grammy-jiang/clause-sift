# Phase 2 Lineage and Release-Provenance Contract

**Project:** ClauseSift  
**Phase:** 2 — Exact Retrieval MVP  
**Status:** Normative Phase 2 implementation-plan appendix  
**Primary design authority:** `docs/design.md` Section 7.2  
**Companion:** `docs/implementation/phase-2-evidence-service.md`

## 1. Purpose and scope

Phase 2 creates the first immutable ClauseSift release and now also implements the ordinary exact/lexical Evidence Package path. It therefore owns both:

- immutable **source/build/release provenance** materialized in canonical `lineage.json`; and
- request-scoped **retrieval/assembly provenance** added at runtime to each Evidence Package without mutating the release.

These dimensions are separate and non-interchangeable.

`lineage.json` never contains query-specific ranks, selected seeds, request IDs, or context paths. The runtime never fabricates source/build provenance outside the verified release.

Phase 3/4 later add their own release artifacts/configurations and request-stage metadata only through the existing versioned contracts.

## 2. Build materialization point

Materialize `lineage.json` after every Phase 2 query-independent artifact that contributes to source/build/release provenance is finalized and before `build_content_id` is derived.

Current Phase 2 ordering is:

1. validate approved manifests/source bytes;
2. complete parser-neutral outputs and passing comparison/validation;
3. build canonical nodes/classifications;
4. build page provenance;
5. build chunks/sources/catalog;
6. compile/validate relationship/context/conflict artifacts;
7. build selected lexical index;
8. finalize all other Phase 2 release artifacts/configuration references;
9. materialize and independently validate canonical `lineage.json`;
10. hash it and include the hash in build-content identity inputs;
11. run complete Phase 2 gates;
12. assemble/checksum/reopen the immutable candidate release;
13. activate only after every gate succeeds.

No release/build identity is accepted when mandatory lineage is absent.

## 3. Canonical serialization and identity

`lineage.json` uses a versioned strict schema and RFC 8785 canonical JSON.

It contains no:

- self-hash;
- `build_content_id` or `release_id` that would create recursive identity;
- random run ID;
- wall-clock timestamp;
- source locator/path;
- source text;
- credential;
- raw exception or temporary path;
- runtime query/request data.

The later release manifest binds lineage relative path, schema, byte size, SHA-256, `build_content_id`, and `release_id` under the existing non-recursive dependency graph.

## 4. Document and source coverage

`lineage.json` contains exactly one document record for every admitted manifested/catalog document and exactly one source-lineage record for every catalog `sources` row beneath its owning document.

Independent release validation requires exact set equality and rejects:

- missing/extra/duplicate document;
- missing/extra/duplicate source;
- wrong document/source/chunk/node ownership;
- reference to a non-existent catalog identity;
- release-mismatched lineage.

Every runtime source-backed item can therefore join one exact `source_id` to one verified source/build lineage record.

## 5. Source provenance

For every source-backed record bind enough immutable data to prove where quoted bytes came from without replacing source authority.

At minimum retain/reconstruct:

- stable document/source/chunk IDs;
- approved manifest-content hash;
- exact source hash and byte size;
- ordered contributing canonical node IDs;
- exact contributed node byte spans;
- exact intersections with validated node page spans;
- page numbers and validated boxes where available;
- coordinate-status derivation;
- source/chunk/document ownership.

Source spans are recomputed from authoritative chunk membership + page mappings; they are not a second freely writable copy.

## 6. Build provenance

Bind the exact deterministic build derivation required by Section 7.2, including as applicable:

- lineage schema;
- ordered parser roles and parser ID/version/configuration;
- parser-neutral artifact hashes;
- passing parser-validation/comparison report;
- OCR admitted asset/configuration identity;
- evidence vocabulary version/hash;
- complete per-node classification records, values, origins, support, rule/review identity, provenance hashes;
- canonical model transformation;
- page-provenance transformation;
- chunk projection;
- relationship resolution;
- conflict analysis;
- catalog artifact identity;
- diagnostic OCR/parser comparison state;
- every release artifact/configuration reference required by the current design.

A comparator remains validation provenance; it never silently merges source facts.

## 7. Phase 2 retrieval/context/conflict artifact provenance

The immutable release binds query-independent identities for every behavior-bearing Phase 2 artifact/configuration it admits, including:

- lexical engine/tokenizer/index configuration and artifact hash set;
- graph edge/occurrence identity schema versions;
- relationship resolver/configuration and artifacts;
- required-context rule-set/configuration and applicable ordering/bounds;
- material-conflict detector/rule/decision/cover artifact/configuration identities;
- evidence vocabulary;
- central Evidence Package schema/serializer identity where release-bound.

Phase 2 has no dense/vector/RRF/reranker artifact and must not fabricate placeholders for them.

When later phases add new release artifacts, they produce a new immutable release/lineage/build identity rather than mutating the activated Phase 2 release.

## 8. Query-independent `lineage.json` boundary

The sealed release file must not contain request-specific:

- query text;
- lexical candidate rank/score for one request;
- selected seed list;
- context paths selected by one request;
- conflict inclusion reasons triggered by one request;
- request/cancellation/deadline state;
- runtime resolved mode for one request.

Those values belong only to request-scoped assembly lineage in the returned Evidence Package.

## 9. Runtime startup validation

Before accepting evidence work, runtime validates the manifest + complete lineage/catalog graph.

At minimum verify:

- supported lineage schema;
- exact manifest-declared lineage path/hash/size;
- one-to-one document/source coverage;
- source -> chunk -> document ownership;
- referenced parser/canonical/page/vocabulary/classification artifacts;
- per-node classification equality with the catalog;
- lexical/context/conflict/retrieval artifact references;
- supported rule/configuration versions;
- no missing/extra/unknown fields;
- no release-mismatched identity.

Failure is `release_integrity_failed`; runtime does not reconstruct lineage opportunistically or fall back to filesystem provenance.

## 10. Request-scoped retrieval provenance

For each direct exact/lexical retrieval seed, runtime assembly lineage uses only the existing Section 21 closed fields.

As applicable record:

- selection role `retrieval_seed`;
- exact originating seed source IDs;
- `assembly.retrievals[]` records using the closed exact/lexical channels, channel/configuration/artifact-set identity, candidate rank, and finite/null score as allowed;
- no dense/fusion/rerank record when those stages did not run.

A retrieval rank/score is non-authoritative selection metadata; it never becomes source provenance or applicability/conflict authority.

## 11. Request-scoped context lineage

For sources/targets attached by required traversal, assembly lineage retains:

- selection roles (`expanded_context` as applicable);
- seed source IDs;
- context completeness;
- every accepted context path;
- each path step's stable edge identity, canonical relation direction/endpoints, validated origin groups/occurrences, and rule ID through the existing closed schema.

Metadata-only `context_targets` carry their exact accepted paths but no fabricated source/build lineage.

The same source reached through several independent accepted paths retains every in-bound path up to the declared bound.

## 12. Request-scoped conflict lineage

Evidence attached due to material-conflict fixed-point closure carries `conflict_context` as applicable and the exact closed conflict inclusion reason(s) defined by Section 21.

An independently retrieved source may carry both direct and conflict roles.

The response-level `conflicts` array projects complete material records separately; conflict reasons never rewrite source/build lineage.

## 13. Current Phase 2 public Evidence Lineage

Phase 2 ordinary `search_evidence`, `get_clause`, and `get_context` already return the complete Section 21 lineage shape required for the behaviors they execute.

The public item lineage has three dimensions:

1. source provenance from the immutable release;
2. build provenance from immutable release lineage/catalog artifacts;
3. request-scoped assembly provenance generated by the shared evidence service.

There is no longer a Phase 2 rule that leaves context paths empty merely because traversal was deferred: current Phase 2 implements required traversal and must report the real accepted paths.

## 14. Central serializer validation

Before returning a source-backed evidence item, the serializer independently verifies that:

- enclosing `document_id`/`source_id` select the same lineage record;
- source spans equal canonical chunk/page intersections;
- public page/box projections equal lineage source spans;
- canonical node IDs/classification records equal the verified catalog;
- build transformation artifact identities equal the verified `lineage.json` records;
- context/conflict rule identities match the active manifest/release;
- retrieval records name admitted artifact sets;
- context paths use validated graph edges/occurrences;
- conflict reasons match returned conflict positions;
- no closed-object extra property is emitted.

Mismatch fails closed.

## 15. Build-content/cache invalidation

Canonical `lineage.json` SHA-256 is a deterministic input to build/release identity.

Invalidate it and affected downstream release identity after any lineage-bearing change, including:

- source bytes/size/hash;
- approved manifest content;
- parser route/version/configuration or passing validation report;
- vocabulary/classification value/provenance;
- canonical/page/chunk transformations;
- relationship/context/conflict artifacts/configuration;
- lexical artifact/configuration;
- catalog identity;
- lineage schema.

A different runtime query changes only request assembly lineage, not immutable `lineage.json`.

## 16. Rollback continuity

Activation/rollback always switch catalog + all retrieval/context/conflict artifacts + `lineage.json` + manifest/configuration as one immutable release.

The runtime never joins an active catalog to lineage from another release even when document/source IDs look similar.

## 17. Static review report

Report safe audit information including:

- document/source lineage counts;
- lineage schema/hash;
- catalog coverage equality;
- parser/build artifact summary;
- vocabulary/classification-provenance consistency;
- lexical artifact binding;
- graph/context/conflict artifact/configuration binding;
- coordinate completeness;
- blocking lineage errors;
- admitted OCR/parser comparison diagnostics.

The report is diagnostic; release lineage/source/catalog remain deterministic authority.

## 18. Tests

### Determinism

- byte-identical rebuild -> byte-identical `lineage.json`;
- source/manifest/parser/classification/page/chunk/relationship/context/conflict/lexical behavior change -> correct invalidation;
- timestamps/run IDs do not change bytes;
- runtime query does not mutate release lineage.

### Coverage/integrity

Reject missing/extra/duplicate/wrong-owner document/source records, nonexistent node/chunk IDs, mismatched source/manifest/parser/classification/page/retrieval/context/conflict artifacts, unsupported lineage schema, or lineage from another release.

### Runtime assembly

Fixtures cover:

- exact direct seed retrieval record;
- lexical direct seed rank/score;
- required applicability/exception/table context path;
- reconvergent independent paths;
- metadata-only context target;
- conflict-context source and inclusion reason;
- one source with several roles;
- no dense/fusion/rerank record in Phase 2-only mode;
- serializer rejection of an invalid edge/occurrence/conflict reason.

### Startup/rollback

- lineage validates before evidence work;
- invalid lineage blocks startup;
- no partial/fallback provenance is served;
- activation validates lineage before pointer switch;
- rollback restores matching catalog/artifacts/lineage as one release.

## 19. Acceptance criteria

Phase 2 is not complete unless:

1. every candidate release contains canonical checksummed `lineage.json`;
2. every manifested document/catalog source has exactly one matching lineage record;
3. source/build provenance fully reproduces the Phase 2 canonical derivation;
4. lexical/relationship/context/conflict artifacts/configuration are explicitly bound without fake later-phase placeholders;
5. lineage hash participates in release identity;
6. independent release/startup validation proves catalog/artifact/lineage consistency;
7. ordinary Phase 2 Evidence Packages add real request-scoped direct/context/conflict assembly lineage through the current closed schema;
8. immutable `lineage.json` remains query-independent;
9. invalid/missing provenance blocks startup/activation/serialization;
10. rollback restores lineage and all matching release artifacts atomically;
11. no Phase 3/4 provenance is fabricated before the corresponding stage actually exists.
