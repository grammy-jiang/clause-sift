# Phase 2 Lineage and Release-Provenance Contract

**Project:** ClauseSift  
**Phase:** 2 — Exact Retrieval MVP  
**Status:** Normative Phase 2 implementation-plan appendix  
**Primary design authority:** `docs/design.md` Section 7.2  
**Companion plan:** `docs/implementation/phase-2-exact-retrieval-mvp.md`

## 1. Purpose and scope

Phase 2 creates the first immutable ClauseSift releases, canonical catalog, source records, lexical retrieval artefact, and read-only runtime. Therefore every Phase 2 release must already contain the release-scoped deterministic **Evidence Lineage build artefact** required by `docs/design.md` Section 7.2.

Phase 2 does not yet implement Phase 4's complete per-request Evidence Package assembly paths. This appendix separates the two concerns exactly as the design does:

- **builder responsibility in Phase 2:** materialize source provenance + build provenance + references to every retrieval artefact actually admitted by the Phase 2 release as canonical `lineage.json`;
- **later Phase 3/4 responsibility:** extend the immutable release with newly admitted semantic/vector/model artefacts when those phases rebuild the release, and add query-specific retrieval/assembly provenance at runtime without mutating `lineage.json`.

`lineage.json` is not deferred merely because the final Evidence Package is deferred.

## 2. Materialization point in the Phase 2 build

The builder materializes `lineage.json` only after all Phase 2 retrieval artefacts are finalized and before deriving `build_content_id`.

For the Phase 2 milestone, the ordering is:

1. validate approved manifests and exact source bytes;
2. complete parser-neutral outputs and passing parser-validation report;
3. build canonical nodes and classification-provenance records;
4. build authoritative page-provenance mappings;
5. build chunks/source rows and validated SQLite catalog;
6. build the selected, frozen lexical index;
7. finalize every other Phase 2 release artefact that contributes to source/build/retrieval provenance;
8. materialize and validate canonical `lineage.json`;
9. hash `lineage.json`;
10. include that hash among deterministic `build_content_id` inputs;
11. run the Phase 2 evaluation/release gates;
12. assemble the immutable release manifest containing the lineage path/hash/schema metadata;
13. validate and activate only after all later Phase 2 release gates pass.

No `build_content_id` or release identity is derived from a release that omits required lineage.

## 3. Canonical serialization and identity

`lineage.json` uses a versioned strict schema and RFC 8785 canonical JSON serialization.

The artefact:

- contains no self-hash;
- contains no `build_content_id`;
- contains no `release_id`;
- contains no random operational run ID;
- contains no wall-clock timestamp;
- contains no source locator/path;
- contains no source text;
- contains no credential;
- contains no raw exception string or parser temporary path.

The release manifest later binds:

- lineage relative path;
- lineage schema version;
- lineage byte size;
- lineage SHA-256;
- `build_content_id`;
- `release_id`.

This avoids recursive identity while making lineage a mandatory checksummed release artefact.

## 4. Exactly one document record per manifested document

`lineage.json` contains exactly one top-level lineage record for every manifested document admitted to the candidate catalog.

Release validation requires exact set equality between:

- manifested/catalog document IDs; and
- lineage document IDs.

Missing, duplicate, extra, or wrong-release document records are blocking `release_validation_failed` conditions.

Each document record binds at minimum the safe deterministic identities needed by the design, including:

- `document_id`;
- approved `manifest_content_hash`;
- exact source-file SHA-256 and byte size;
- exact evidence-vocabulary version/hash;
- ordered selected parser route provenance;
- passing parser-validation report hash;
- canonical-model/classification artefact identities;
- page-provenance artefact identity;
- catalog identity relevant to the document;
- retrieval artefact references admitted for this release.

Human-readable source paths are not lineage fields.

## 5. Exactly one source-lineage record per catalog source

Beneath each document, `lineage.json` contains exactly one source-lineage record for every catalog `sources` row owned by that document.

Release validation requires one-to-one equality between catalog `source_id` values and lineage source records. It rejects:

- missing source lineage;
- extra lineage source;
- duplicate source record;
- source assigned to the wrong document;
- source/chunk ownership mismatch;
- lineage referring to a non-existent chunk/node;
- lineage from another release/catalog identity.

The runtime can therefore join any Phase 2 direct retrieval `source_id` to exactly one verified release-scoped source/build lineage record.

## 6. Source provenance fields

For every source-backed record, the lineage artefact binds source provenance sufficient to prove where the quoted/retrieved bytes came from without replacing the source as authority.

Record at minimum:

- stable `document_id`;
- stable `source_id`;
- stable `chunk_id`;
- approved manifest-content hash;
- exact source-file hash and size;
- ordered contributing node IDs;
- exact ordered UTF-8 chunk membership spans;
- the authoritative page-span intersections derived from `node_page_spans`;
- validated page numbers;
- validated boxes when available;
- coordinate-status derivation inputs;
- source/chunk ownership identities.

The ordered source spans are recomputed as the exact intersections of `chunk_nodes` membership with `node_page_spans`; lineage does not trust a second independently writable page/span copy.

## 7. Build provenance fields

Each source lineage record binds the exact build derivation that produced its canonical representation.

Record or reference at minimum:

- lineage schema version;
- ordered parser roles;
- parser identity/version/configuration hash for every selected role;
- parser-neutral content hashes;
- passing parser-validation-report hash;
- OCR configuration/declared local-asset digests where applicable;
- exact evidence-vocabulary version/hash;
- the three classification records for every contributing canonical node;
- each classification value, origin, supporting provenance hash, and applicable deterministic rule/review identity;
- canonical-model artefact hash/version;
- normalization/classification transformation versions;
- page-provenance artefact hash/version;
- chunking artefact/version/configuration hash;
- stable node/chunk/source identities;
- diagnostic build uncertainty such as admitted OCR/comparison state;
- candidate catalog hash or deterministic catalog identity.

A comparator is validation provenance only. It never becomes a silent field-level source merge.

## 8. Phase 2 retrieval-artefact provenance

Phase 2 has lexical retrieval but intentionally no dense embedding/vector/fusion/reranker artefacts.

The lineage schema represents **the complete set of retrieval artefacts actually admitted by the current release**, not fictional placeholders.

For Phase 2 this set contains the checksummed lexical retrieval artefact and its exact identity, including:

- lexical engine/version;
- tokenizer/version;
- lexical configuration hash;
- lexical schema/index version;
- ordered search-text/metadata input hash set or upstream chunk artefact hash;
- lexical artefact SHA-256/byte size;
- selected Phase 2 capability-set version.

The release capability metadata and lineage schema make absence of Phase 3 features explicit. Phase 2 must not fabricate zero hashes, empty model names, or dummy vector/model artefacts merely to satisfy a later feature set.

When Phase 3 adds embeddings/vector/fusion, that change produces new retrieval artefacts and a new `lineage.json`, `build_content_id`, and release identity. It does not mutate an activated Phase 2 release in place.

## 9. Rule/configuration bindings required before later traversal

The design binds release identity to behavior-bearing rule/configuration versions. Phase 2 records the exact versions/hashes already admitted by its canonical graph/catalog and release validation, even when the corresponding Phase 4 runtime traversal surface is not advertised yet.

This includes applicable schema/configuration identities for:

- edge identity;
- relationship occurrence identity;
- evidence vocabulary;
- conflict/cross-reference compilation artefacts admitted to the Phase 2 catalog;
- context/conflict rule-set/configuration values that are release inputs under the design, where the Phase 2 builder already compiles/validates them for later use.

Recording a configuration identity is not the same as implementing Phase 4 traversal. Phase 2 does not emit runtime context paths or claim that required closure is available.

## 10. Phase 2 runtime join

At startup, after verifying the release manifest and before accepting a query, the runtime validates the complete `lineage.json` artefact and joins it to the checksum-verified catalog.

It verifies at minimum:

- supported lineage schema version;
- manifest-declared lineage path/hash/size;
- exact one-to-one document coverage;
- exact one-to-one source coverage;
- source→chunk→document ownership;
- referenced canonical/page/parser/vocabulary/classification artefact hashes;
- exact per-node classification agreement with the catalog;
- retrieval-artefact references present in the immutable release;
- no missing/extra/unknown fields under the strict schema;
- no release-mismatched identity.

Any failure is `release_integrity_failed` at startup. The server must not continue with a partial lineage file, rebuild lineage in memory, or silently fall back to path-based provenance.

## 11. Direct Phase 2 retrieval provenance

Phase 2 direct exact/lexical retrieval services can return or internally expose their source records for CLI/evaluation without claiming the final Phase 4 Evidence Package.

When provenance is requested by a Phase 2 diagnostic/evaluation surface, it must be derived by joining the selected `source_id` to the verified immutable lineage record plus typed per-request direct-selection metadata.

For a Phase 2 direct result:

- source/build provenance comes from `lineage.json`;
- lexical channel/rank/score may be attached as non-authoritative per-request selection metadata;
- a direct seed may identify itself as the originating source;
- context-path arrays remain empty/not-advertised because Phase 4 traversal is not implemented;
- no model score, generated summary, or query classification becomes source provenance.

The final Section 21 lineage object and complete retrieval/assembly path contract is enabled only when the Phase 4 Evidence Package is implemented. Phase 2 nevertheless preserves all immutable source/build facts required to construct it later.

## 12. Build-content and cache invalidation

The SHA-256 of canonical `lineage.json` is a deterministic input to Phase 2 `build_content_id` and downstream release assembly.

A change to any lineage-bearing input invalidates the lineage artefact and affected release identity, including:

- source bytes/hash/size;
- approved manifest content;
- parser route/version/configuration;
- passing parser-validation report;
- vocabulary/classification value or provenance;
- canonical transformation;
- page mapping;
- chunk/source identity or membership;
- catalog identity;
- lexical retrieval artefact/version/configuration;
- lineage schema;
- admitted behavior-bearing relationship/conflict/context configuration.

A different runtime query does not alter `lineage.json`.

## 13. Rollback continuity

An immutable release and its `lineage.json` are activated and rolled back together.

Rollback to an older release restores that release's:

- source hashes;
- manifest hashes;
- parser/build provenance;
- canonical/catalog identities;
- lexical artefact references;
- lineage hash.

The runtime never joins the active catalog to lineage from another release, even when filenames or document IDs look similar.

## 14. Static review report

The Phase 2 static review report includes a lineage section that allows an operator to audit, without exposing sensitive paths/text:

- document/source lineage counts;
- schema/version/hash;
- catalog-vs-lineage coverage check;
- parser role/hash summary;
- vocabulary/classification-provenance consistency;
- lexical retrieval artefact binding;
- page-coordinate completeness summary;
- every blocking lineage validation failure;
- any advisory OCR/parser comparison state.

The report is diagnostic; `lineage.json` plus source/manifest/catalog remain the deterministic release inputs.

## 15. Tests

### 15.1 Deterministic materialization

Test:

- byte-identical rebuild produces byte-identical `lineage.json`;
- same filename with changed source bytes changes lineage/release identity;
- lexical index regeneration with changed inputs changes lineage;
- byte-identical lexical artefact under unchanged declared inputs preserves lineage;
- operational run IDs/timestamps never change lineage bytes.

### 15.2 Coverage/integrity failures

Reject:

- missing document record;
- extra document record;
- missing/extra/duplicate source record;
- wrong source ownership;
- nonexistent node/chunk;
- wrong source/manifest hash;
- wrong parser/report hash;
- wrong classification value/origin/provenance;
- wrong page mapping/span;
- missing or wrong lexical artefact reference;
- unknown lineage schema/version/field;
- lineage from another release.

### 15.3 Startup and rollback

Prove:

- runtime validates lineage before accepting Phase 2 queries/MCP work;
- invalid lineage fails startup with `release_integrity_failed`;
- no partial/fallback provenance is served;
- activation validates lineage before pointer switch;
- rollback restores catalog + lineage from the same old release;
- active release bytes remain read-only during runtime provenance assembly.

### 15.4 Source-span reconstruction

Fixtures include:

- one node/one page;
- multiple nodes in one chunk;
- chunk spanning several pages;
- complete page-and-box mappings;
- page-only mappings with missing optional boxes;
- OCR-admitted source;
- admitted below-threshold parser comparison difference.

The derived lineage spans must exactly equal the authoritative chunk-membership/page-span intersections.

## 16. Acceptance criteria

Phase 2 is not complete unless:

1. every candidate release contains canonical checksummed `lineage.json`;
2. lineage is materialized after Phase 2 retrieval artefacts and before `build_content_id`;
3. every manifested document appears exactly once;
4. every catalog source appears exactly once beneath its owning document;
5. every source record carries source/build provenance sufficient to reproduce its Phase 2 canonical derivation;
6. the Phase 2 lexical retrieval artefact is explicitly bound and absent Phase 3 artefacts are not fabricated;
7. the release manifest records lineage schema/path/hash/size;
8. lineage hash participates in build/release identity;
9. release validation and runtime startup independently verify lineage/catalog/classification/retrieval-artifact consistency;
10. invalid/missing lineage blocks activation/startup;
11. rollback restores lineage and catalog as one immutable release;
12. Phase 2 direct-result provenance is joined from verified lineage without claiming Phase 4 runtime assembly semantics.

This requirement remains strictly Phase 2 because Phase 2 creates and serves the immutable release whose provenance later phases build upon.
