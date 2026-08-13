# Phase 2 Implementation Plan: Exact Retrieval MVP

**Project:** ClauseSift  
**Phase:** 2 of the design-defined implementation sequence  
**Status:** Implementation plan  
**Primary design authority:** `docs/design.md`  
**Phase objective:** Build the first deterministic ClauseSift knowledge-base compiler and read-only runtime around approved manifests, the canonical document model, standards-aware chunks, SQLite catalog persistence, exact clause lookup, lexical retrieval, deterministic source citations, basic CLI/MCP surfaces, static review reports, immutable milestone releases, atomic activation, and rollback—without implementing Phase 3 semantic retrieval or Phase 4 high-accuracy Evidence Graph traversal.

## 1. Purpose

Phase 2 turns the Phase 0 evaluation baseline and Phase 1 parser-routing evidence into the first functioning ClauseSift software stack.

This is the first phase that builds a persistent knowledge base and queries it. Its primary purpose is to prove that ClauseSift can deterministically compile engineering documents into a trustworthy local catalog and retrieve exact or lexical source evidence without relying on embeddings or an LLM.

The phase must establish the foundations that every later retrieval capability depends on:

- package and workspace structure;
- approved manifest registration;
- deterministic canonical evidence nodes;
- classification provenance;
- page/source provenance;
- standards-aware chunking;
- stable identifiers;
- relational integrity;
- exact clause lookup;
- lexical candidate retrieval;
- deterministic citations;
- immutable releases;
- read-only runtime loading;
- safe CLI/MCP adapters;
- repeatable validation and rollback.

Phase 2 is an **exact-retrieval milestone**, not the completed v0.1 high-accuracy product. The design explicitly states that semantic retrieval is not required for the earliest exact-retrieval milestone. Phase 3 adds dense retrieval and fusion. Phase 4 adds cross-encoder reranking, deterministic Evidence Graph context traversal, strengthened table/cross-reference behavior, typed warnings, and refusal support.

## 2. Phase boundary

### 2.1 In scope

Phase 2 implements:

- Python package/bootstrap and optional build/runtime dependency boundaries;
- local workspace initialization;
- source registration and human-reviewed manifest handling;
- manifest schema v2 validation and approval binding;
- source hashing and change detection;
- integration of the Phase 1 selected parser routes;
- parser-validation gate consumption;
- deterministic canonical document-model construction;
- ClauseSift Engineering Evidence Vocabulary materialization and validation;
- deterministic node classification/provenance rules needed by the canonical model;
- clause/node tree construction;
- node-level page provenance and bounding-box mapping;
- standards-aware chunks and source rows;
- basic deterministic cross-reference extraction/resolution needed to populate the Phase 2 catalog, without runtime graph traversal;
- SQLite `knowledge.sqlite` catalog schema and integrity gates;
- exact clause lookup sets;
- lexical-engine benchmark and selection;
- lexical index creation and loading;
- metadata filtering;
- direct exact and lexical retrieval services;
- source-faithful direct evidence projections and deterministic citations;
- safe document/page metadata lookup;
- basic CLI commands;
- basic MCP protocol/server surfaces that do not require Phase 4 context traversal;
- static build/review reports for Phase 2 artefacts;
- content-addressed build caches for Phase 2 artefacts;
- immutable exact-retrieval milestone releases;
- release manifest/checksum validation;
- read-only runtime startup validation;
- atomic active-pointer update and rollback;
- Phase 2 regression evaluation and quality gates;
- packaging tests and runtime/build dependency separation.

### 2.2 Explicitly out of scope

Phase 2 must not implement:

- chunk embeddings;
- vector search;
- embedding-model selection;
- rank fusion or reciprocal-rank fusion;
- semantic/hybrid retrieval;
- query-embedding model loading;
- cross-encoder reranking;
- high-accuracy retrieval mode;
- deterministic Evidence Graph context traversal;
- required/supporting/diagnostic context closure at runtime;
- conflict fixed-point runtime closure;
- final all-side conflict serialization;
- Phase 4 refusal policy;
- Phase 4 typed runtime warning completion;
- ANN indexes;
- product/version intelligence from the later design phase.

The Phase 2 implementation must not create placeholder results that claim those capabilities work.

## 3. Critical compatibility rule: do not expose incomplete final evidence tools

The final design makes `search_evidence` and `get_clause` success semantics depend on required context closure from `docs/design.md` Section 19. That traversal is owned by Phase 4.

Therefore Phase 2 must separate **direct retrieval primitives** from the final evidence-returning public MCP tools.

### 3.1 Direct retrieval primitives implemented now

The runtime service layer implements internal/public-Python primitives such as:

```text
lookup_clause_direct(document_id, clause_number)
search_lexical_direct(query, filters, limit)
get_source_direct(source_id)
list_documents(...)
get_document_metadata(document_id)
get_page_reference(document_id, page_number)
```

The literal function names may change, but their semantics must remain clearly different from the final `docs/design.md` Section 22 context-complete tools.

These primitives return direct source candidates and deterministic citation/provenance projections. They do not claim that required applicability, exception, dependency, conflict, or supporting context has already been closed.

### 3.2 CLI diagnostic retrieval

Phase 2 may expose `clausesift search` and `clausesift get-clause` as exact-retrieval milestone commands backed by the direct retrieval primitives.

Their help and structured output must explicitly identify them as direct Phase 2 retrieval rather than the final context-complete Evidence Package contract.

The later Phase 4 implementation may layer final evidence assembly over these primitives without changing source IDs, canonical node identities, exact clause identities, source text, or citation provenance.

### 3.3 Basic MCP surfaces implemented now

Phase 2 should fully implement and advertise only MCP surfaces whose success semantics do not require Phase 4 traversal, for example:

- `get_document_metadata`;
- `list_documents`;
- `get_page_reference`;
- `standards://document/{document_id}`;
- `standards://page/{document_id}/{page_number}`;
- `standards://release/current`.

The final `search_evidence`, `get_clause`, `get_context`, clause resource, and source/evidence assembly surfaces are not advertised as successful Phase 2 capabilities until their `docs/design.md` Sections 19, 21, and 22 contracts can be satisfied.

If a compatibility stub is required by an implementation experiment, it must return the design-defined `feature_unavailable` error and must not emit a partial success object.

### 3.4 Why this boundary is mandatory

This prevents two unacceptable outcomes:

1. silently returning evidence without context that the design says is required; or
2. pulling Phase 4 Evidence Graph traversal into Phase 2 merely to satisfy a premature API surface.

## 4. Inputs from earlier phases

### 4.1 Phase 0 inputs

Phase 2 consumes:

- representative corpus identities and hashes;
- source rights/governance records;
- golden questions and evidence labels;
- exact document/edition/clause/page expectations;
- vocabulary/classification fixtures;
- table fixtures;
- multilingual lexical-retrieval cases;
- hard negatives;
- held-out/release-gate splits;
- reviewer/adjudication provenance.

Phase 2 must not rewrite ground truth to make the implementation pass.

### 4.2 Phase 1 inputs

Phase 2 consumes:

- parser-neutral schema and deterministic serialization;
- adapter interface;
- isolated parser execution runner;
- selected primary parser route recommendations;
- independent comparator recommendations;
- OCR-route recommendations;
- configured alternative-route recommendations;
- parser validation/comparison rules;
- parser report format;
- deterministic parser artefact identities;
- unresolved parser thresholds/gaps.

Production manifests and builder routing bind those Phase 1 outputs to actual documents in this phase.

## 5. Recommended implementation structure

A practical Phase 2 package structure is:

```text
src/
└── clausesift/
    ├── __init__.py
    ├── cli.py
    ├── errors.py
    ├── config/
    │   ├── workspace.py
    │   ├── schemas.py
    │   └── defaults.py
    ├── model/
    │   ├── vocabulary.py
    │   ├── documents.py
    │   ├── nodes.py
    │   ├── classifications.py
    │   ├── chunks.py
    │   ├── provenance.py
    │   └── citations.py
    ├── builder/
    │   ├── registration.py
    │   ├── manifests.py
    │   ├── parsers/
    │   ├── normalisation/
    │   ├── canonical.py
    │   ├── page_provenance.py
    │   ├── chunking/
    │   ├── references/
    │   ├── catalog/
    │   ├── lexical/
    │   ├── reports/
    │   ├── cache/
    │   └── release/
    ├── runtime/
    │   ├── catalog/
    │   ├── query/
    │   ├── retrieval/
    │   ├── evidence/
    │   └── release.py
    ├── mcp/
    │   ├── server.py
    │   ├── schemas.py
    │   ├── tools.py
    │   └── resources.py
    └── evaluation/

tests/
├── unit/
├── integration/
├── regression/
└── fixtures/
```

Module names may be simplified, but the following boundaries are mandatory:

- build-only parser/OCR modules are not imported by runtime startup;
- SQLite/runtime query code does not depend on parser-native objects;
- CLI and MCP adapters call shared services rather than reimplementing SQL/retrieval logic;
- release validation is separate from build mutation;
- source authority, canonical representation, and derived indexes remain distinct.

## 6. Work package 2.1: Package and dependency bootstrap

### 6.1 Distribution contract

Implement the design names:

- PyPI distribution: `clausesift`;
- Python import: `clausesift`;
- CLI executable: `clausesift`.

### 6.2 `pyproject.toml`

Define:

- supported Python version;
- package metadata;
- CLI entry point;
- runtime dependencies;
- build extras;
- OCR extras;
- test/dev dependencies;
- package data limited to software schemas/configuration, never user standards.

The exact minimum Python version is a governance/open decision and must be recorded rather than guessed if not yet approved.

### 6.3 Dependency profiles

Preserve the intended separation:

- base runtime: SQLite/catalog, selected lexical runtime, CLI, MCP, schemas;
- `build`: parser adapters, builder, report dependencies;
- `ocr`: heavyweight OCR dependencies/assets;
- later `rerank` dependencies remain Phase 4 and must not be added merely for convenience;
- `all` may not silently pull unimplemented Phase 3/4 code paths into normal runtime startup.

### 6.4 Import-boundary test

A clean base installation must be able to:

- import `clausesift`;
- run metadata/list/direct exact runtime tests against a prepared Phase 2 release;
- start the basic MCP server;
- execute CLI runtime commands;

without importing Docling, MinerU, OCR modules, or other build-only packages.

## 7. Work package 2.2: Workspace initialization

### 7.1 Workspace layout

`clausesift init <workspace>` creates a deterministic layout such as:

```text
workspace/
├── corpus/
│   ├── inbox/
│   ├── originals/
│   └── manifests/
├── cache/
├── build/
├── releases/
├── state/
└── active.json
```

Do not place proprietary source bytes inside the installed Python package.

### 7.2 Idempotence

Initialization must be idempotent:

- existing approved files are not overwritten;
- schema/configuration files are checked for compatibility;
- unexpected conflicting files produce a visible error;
- no implicit migration runs without a versioned migration policy.

### 7.3 Path safety

Workspace roots are resolved once and stored in configuration. All later source/release paths are resolved beneath approved roots and checked for containment, symlink/junction/reparse escape, and regular-file expectations where applicable.

## 8. Work package 2.3: Manifest schema v2

### 8.1 Closed schema

Implement the design's human-reviewed manifest with unknown fields rejected.

Required Phase 2 fields include the design-owned values such as:

- `manifest_schema_version`;
- `evidence_vocabulary_version`;
- `document_id`;
- `title`;
- `document_code`;
- `edition`;
- `authority`;
- `document_type`;
- `normative_status`;
- `release_tier`;
- `jurisdictions`;
- `disciplines`;
- `status`;
- effective-date fields where supported by the design schema;
- `relations`;
- `reference_edition_overrides`;
- `language`;
- `source_file`;
- `sha256`.

Do not introduce legacy composite aliases.

### 8.2 Safe YAML loading

Manifest loading must:

- reject custom/unsafe YAML tags;
- reject duplicate mapping keys;
- reject unknown fields;
- validate types before business logic;
- normalize only according to field-specific rules;
- never execute constructors from manifest content.

### 8.3 Hash forms

Use the exact canonical SHA-256 syntax required by the design:

```text
sha256:<64 lowercase hex characters>
```

Reject:

- bare digests;
- uppercase hex;
- whitespace;
- wrong length;
- zero/missing source hash in an admitted manifest.

### 8.4 Exact public key bounds

Validate `document_code`, `edition`, jurisdictions, disciplines, and other exposed exact keys both before and after field normalization against the design's 1-128 Unicode-scalar bound.

Never truncate or hash a human-readable lookup key to make it fit.

### 8.5 Closed enums

Implement exact values for:

- document type;
- lifecycle `status`;
- `release_tier`;
- document-level normative status;
- language fields if schema-controlled.

Unknown lifecycle status is `document_status_unknown`, not a best-effort mapping.

## 9. Work package 2.4: Manifest registration and approval

### 9.1 Raw and semantic hashes

Registration computes separately:

- `manifest_bytes_hash` over exact manifest bytes for forensic provenance;
- `manifest_content_hash` over schema-normalized canonical content.

A formatting-only manifest change does not alter semantic approval or Phase 2 semantic cache identity.

### 9.2 Source verification

Registration computes and records:

- exact source SHA-256;
- positive source byte size;
- source page count;
- source identity/relative locator.

The calculated source digest must match the manifest value before approval is admitted.

### 9.3 Approval artefact

Define an immutable local approval record binding:

- manifest schema version;
- `manifest_content_hash`;
- source SHA-256;
- source size;
- evidence-vocabulary version;
- reviewer/approval identity;
- approval artefact schema version.

The approval mechanism must be explicit and auditable. A builder never treats the existence of a manifest file itself as approval.

### 9.4 Build-time revalidation

Every build:

1. safe-loads current manifest;
2. re-canonicalizes it;
3. verifies approved content hash;
4. recomputes source hash and size;
5. rejects semantic manifest/source changes without renewed approval.

## 10. Work package 2.5: Manifest relations

### 10.1 Strict relation entries

Implement the design's `manifest-relation.v1` shape and canonical set semantics.

Each relation has exactly the defined fields and supports only the admitted v0.1 manifest relation types.

### 10.2 Canonical ordering

Normalize `relations` by RFC 8785 canonical entry bytes:

- YAML order is ignored;
- duplicates are invalid;
- stored/hashed order is deterministic.

### 10.3 Selector validation

Validate document-root versus addressable-clause selector combinations exactly as defined.

Phase 2 may resolve these relations into catalog cross-reference/edge records, but it does not traverse them at runtime. Traversal is Phase 4.

## 11. Work package 2.6: Build change detection

Compare the registered/approved corpus to the prior build inputs and classify:

- added documents;
- source-byte changes;
- semantic manifest changes;
- raw-byte-only manifest changes;
- removed documents;
- unchanged inputs.

A removed or changed document must invalidate every Phase 2 artefact whose declared dependency includes it.

Do not use filename or modification time as semantic identity.

## 12. Work package 2.7: Integrate Phase 1 parser routing

### 12.1 Production route binding

Bind approved manifest/source characteristics to the Phase 1 selected routing configuration.

Every document has exactly one configured `canonical_primary` route.

Every `release_tier: critical` document has exactly one independent comparator from a distinct implementation family.

### 12.2 Fail-closed behavior

A parser failure or blocking comparison failure:

- produces/retains the durable parser-validation report;
- produces no canonical model for that document;
- prevents downstream Phase 2 catalog/index/release assembly;
- leaves the active release unchanged.

Do not silently invoke a different fallback parser after failure.

### 12.3 Configured alternative routes

A Phase 1 fallback/alternative recommendation becomes an explicit routing configuration selected before parse, never a runtime exception handler.

### 12.4 Primary output only

After applicable parser gates pass, canonical construction receives exactly the configured primary parser-neutral artefact.

Comparator fields are never merged into it.

## 13. Work package 2.8: Evidence vocabulary artefact

### 13.1 Materialize `evidence-vocabulary.json`

Generate the exact `docs/design.md` Section 12.2 core vocabulary as deterministic RFC 8785 JSON containing the design-required:

- semantic version;
- enum order/definitions;
- cardinalities;
- classification-origin rules;
- inheritance rules;
- relation/endpoint contract version/hash needed by the current milestone.

### 13.2 Hash binding

The vocabulary SHA-256 is bound into:

- canonical model identity;
- catalog validation;
- reports;
- evaluation results;
- release manifest.

### 13.3 Runtime validation

The Phase 2 runtime has an explicit supported vocabulary-version allowlist.

It fails startup instead of guessing when the active release contains:

- unsupported core version;
- unknown core token;
- vocabulary hash mismatch;
- catalog/vocabulary disagreement;
- forbidden legacy alias.

## 14. Work package 2.9: Canonical node model

### 14.1 Node fields

Implement the design's canonical fields:

```text
node_id
document_id
node_type
normative_status
source_modality
classification_provenance
parent_node_id
previous_node_id
next_node_id
heading
heading_path
clause_number
original_text
normalized_text
parser_source
parser_confidence
attributes
```

Page bounds and boxes are derived from page-provenance rows, not writable node scalars.

### 14.2 One root per document

Every canonical document has exactly one root node:

- `node_type: document`;
- null parent;
- dense deterministic tree ownership.

All other nodes have exactly one parent in the same document.

### 14.3 Canonical order

Persist a dense zero-based or design-defined deterministic canonical order with no gaps/duplicates.

Parent order must precede child order where the design requires it.

### 14.4 Addressable clauses

A non-null `clause_number` means the node is independently exact-addressable.

Requirements:

- canonical normalized value;
- unique `(document_id, clause_number)`;
- descendants do not copy an ancestor number merely for display;
- no fuzzy/latest-edition substitution.

### 14.5 Stable node IDs

Define deterministic node identity from stable document/source/canonical inputs.

An unchanged source, approved manifest, parser artefact, canonical configuration, and classification input must reproduce identical node IDs.

## 15. Work package 2.10: Canonical text normalization

### 15.1 `original_text`

Preserve source-faithful evidence text.

Do not silently:

- paraphrase;
- translate;
- summarize;
- normalize units;
- repair numeric values;
- merge separate source statements.

### 15.2 `normalized_text`

Allow deterministic transformations such as approved:

- line-break repair;
- whitespace normalization;
- hyphenation repair;
- Unicode normalization where specified.

Every transformation is versioned and testable.

### 15.3 Search enrichment

Generate deterministic `search_text` later from normalized source text plus approved metadata/hierarchy context.

Embedding-specific text remains structurally possible but Phase 3 owns actual embedding use/model formatting.

## 16. Work package 2.11: Classification provenance

### 16.1 Three required node classifications

Every canonical node carries one admitted record for:

- `node_type`;
- `normative_status`;
- `source_modality`.

### 16.2 Closed origins

Use only design-defined origins such as:

- `manifest`;
- `source_marker`;
- `deterministic_rule`;
- `inherited`;
- `human_reviewed`.

### 16.3 No LLM authority

An LLM may propose a review candidate outside the deterministic build, but it cannot directly write an admitted classification.

### 16.4 Narrow inheritance

Implement the exact `docs/design.md` Section 12.2 inheritance rules:

- node type never inherits;
- `mixed`/`unknown` do not become child normative status by generic inheritance;
- source modality never inherits from parent/proximity;
- note/footnote classification is independent;
- document facts stay document facts.

### 16.5 Standard versus critical unresolved classification

For `release_tier: standard`, unresolved source-bearing nodes remain conservative `unclassified`/`unknown` with `classification_unresolved` diagnostics.

For `release_tier: critical`, unresolved required classification blocks Phase 2 release admission.

## 17. Work package 2.12: Canonical tree validation

Validate before page/chunk construction:

- exactly one document root;
- every non-root has one valid same-document parent;
- no parent self-edge;
- no parent cycle;
- every node reachable exactly once from root;
- no disconnected component;
- canonical ordering consistency;
- previous/next links reciprocal;
- previous/next are immediate canonical-order neighbours or null at boundaries;
- unique addressable clause keys;
- heading-path determinism.

A malformed canonical tree is blocking.

## 18. Work package 2.13: Node-level page provenance

### 18.1 Separate artefact

Build a versioned page-provenance artefact after canonical construction and before chunking.

### 18.2 Required mapping

For every non-empty source-bearing node, persist ordered mappings containing:

- `node_id`;
- same-document ownership;
- half-open UTF-8 byte start/end within `nodes.original_text`;
- one-based page number;
- mapping order;
- optional validated bounding box;
- coordinate-system metadata/version.

### 18.3 Exact partition

Mappings for each non-empty node must form an exact, dense, non-overlapping partition of its original UTF-8 bytes.

Reject:

- gaps;
- overlap;
- duplicate coverage;
- out-of-order spans;
- non-code-point boundaries;
- page outside manifested source page count;
- invalid box geometry.

### 18.4 Empty structural nodes

An empty structural node has no fabricated zero-length page-span row.

Displayed page context may later derive from covered descendants.

### 18.5 Coordinate incompleteness

A missing optional box does not erase valid source text/page identity. Preserve page-only provenance so later Phase 4 can emit the appropriate warning.

## 19. Work package 2.14: Standards-aware chunker

### 19.1 Boundary priority

Implement the design's preferred order:

1. complete clause/subclause;
2. complete requirement plus directly attached exception/note metadata where appropriate;
3. complete table or independent row;
4. semantically complete paragraph;
5. token-limit split only as last resort.

Fixed-size character windows are not the primary strategy.

### 19.2 Chunk fields

Implement:

```text
chunk_id
document_id
citation_node_id
chunk_kind
canonical_order
parent_chunk_id
previous_chunk_id
next_chunk_id
original_text
search_text
embedding_text
```

Ordered member nodes/spans live in `chunk_nodes`.

### 19.3 Membership intervals

Each member records:

- `node_id`;
- dense member order;
- half-open UTF-8 byte span;
- same-document ownership.

Spans must align with code-point boundaries.

### 19.4 Chunk text reconstruction

`chunks.original_text` is reconstructed deterministically from ordered memberships and the versioned source-faithful separator.

The validator independently recomputes it byte-for-byte.

### 19.5 Citation anchor

Derive `citation_node_id` as the deepest common ancestor of every member node.

Do not store independently editable heading path/node type/clause/page values on the chunk when they are projections from canonical/catalog data.

### 19.6 Addressable-ancestor consistency

Every retrievable member in one chunk must resolve to the same nearest addressable ancestor-or-self or all null.

A chunk may not mix two independently addressable branches.

### 19.7 Deterministic representation identity

Deduplicate on the design representation key and assign deterministic `chunk_id` and dense per-document canonical order.

Release validation recomputes both.

## 20. Work package 2.15: Atomic/source-contained chunk coverage

Even though runtime context traversal is Phase 4, Phase 2 must build chunks that make later deterministic traversal possible.

For every source-bearing node eligible as an atomic future context target:

- emit one or more source-contained chunks whose memberships cover that node completely;
- do not include another node's bytes in those atomic chunks;
- allow token-limit splits while preserving exact cover;
- keep broader preferred multi-node retrieval chunks separately.

A broad requirement-plus-exception chunk cannot be the only representation of an atomic requirement or exception.

This is chunk construction, not Phase 4 traversal.

## 21. Work package 2.16: Table chunks

Create at least:

1. whole-table searchable representation;
2. row-level representations.

Row-level `search_text` repeats deterministic table context such as:

- table title;
- headers;
- units;
- parent clause context.

`original_text` remains source-faithful and does not turn repeated enrichment into source evidence.

Preserve table extraction/parser confidence for later diagnostic projection.

## 22. Work package 2.17: Source rows

Create exactly one `sources` row per persisted chunk.

Each source row binds:

- stable `source_id`;
- `document_id`;
- `chunk_id`;
- derived page start/end.

The source page range is recomputed from intersecting `node_page_spans`, not trusted from a chunk writer.

Every chunk must have one source and every source must name the owning chunk/document.

## 23. Work package 2.18: Basic cross-reference extraction and resolution

Phase 2 should create the deterministic cross-reference/catalog substrate required by the detailed design, but **not** runtime traversal.

### 23.1 Inputs

Extract from:

- source text/reference markers;
- approved manifest `relations`;
- approved `reference_edition_overrides`.

### 23.2 Exact resolution

Resolution uses exact document/edition/clause identities and approved deterministic rules.

Never resolve by:

- embedding similarity;
- LLM inference;
- “latest edition” guess;
- nearest clause number;
- text similarity fallback.

### 23.3 Unresolved references

Persist an explicit unresolved occurrence with no navigable target IDs.

For Phase 2:

- unresolved standard-document references are visible in build/review diagnostics;
- unresolved critical-document references block release where the design requires it.

Runtime following of these records remains Phase 4.

### 23.4 Phase 4 boundary

Do not implement `docs/design.md` Section 19 traversal queues, context classes, path retention, conflict closure, or runtime relationship expansion in this phase.

## 24. Work package 2.19: SQLite catalog schema

### 24.1 Connection factory

Every builder/runtime SQLite connection is created through one factory.

Immediately after open and before any transaction/statement:

```sql
PRAGMA foreign_keys = ON;
```

Read back and require `1`.

Runtime read-only connections additionally set and verify:

```sql
PRAGMA query_only = ON;
```

Application code may not toggle these pragmas later.

### 24.2 Phase 2 tables

Implement at minimum the design tables needed for Phase 2 data:

- `documents`;
- `document_jurisdictions`;
- `document_disciplines`;
- `nodes`;
- `node_classifications`;
- `chunks`;
- `chunk_nodes`;
- `node_page_spans`;
- `sources`;
- `cross_references`;
- build/release-admission metadata allowed before catalog freeze;
- lexical-engine/catalog metadata as appropriate.

Conflict tables may be created as versioned empty schema structures if required for forward schema compatibility, but Phase 2 must not fabricate conflict records or implement Phase 4 conflict semantics merely to populate them.

### 24.3 Database constraints

Encode invariants using:

- primary keys;
- foreign keys;
- `NOT NULL`;
- unique constraints;
- `CHECK` constraints;
- composite ownership foreign keys.

Do not rely exclusively on Python validation.

## 25. Work package 2.20: Identifier contracts

### 25.1 Opaque public IDs

Apply the design grammar to persisted public opaque IDs:

```text
^[a-z0-9][a-z0-9._:-]{0,127}$
```

Length 1-128.

### 25.2 Human-readable exact keys

Keep document code, edition, clause number, jurisdiction, and discipline as their own canonical normalized Unicode keys.

Do not force them into the opaque ASCII-ID grammar.

### 25.3 Deterministic derived IDs

Derived node/chunk/source/reference IDs must be:

- content/input-derived;
- stable across byte-identical rebuilds;
- validated before insert;
- independently recomputed during release validation.

## 26. Work package 2.21: Required catalog indexes

Create indexes supporting:

- exact `(document_id, clause_number)` lookup;
- unique document code + edition;
- `(status, document_type, document_id)` filtering;
- jurisdiction link-table filtering;
- discipline link-table filtering;
- source ID lookup;
- chunk-to-node and node-to-chunk membership;
- cross-reference source/target keys.

Query-plan regression tests must prove index usage for the design-required exact/filter plans.

## 27. Work package 2.22: Catalog freeze and blocking gate

After all Phase 2 catalog rows are materialized:

1. run `PRAGMA foreign_key_check` and require zero rows;
2. close mutation of `knowledge.sqlite` for the current build;
3. run independent validation queries;
4. never reopen the candidate catalog for mutation after the catalog gate.

### 27.1 Validate vocabulary/classifications

Reject:

- unsupported/changed vocabulary;
- legacy aliases;
- missing/duplicate classification rows;
- stored-versus-provenance mismatch;
- illegal inheritance;
- illegal critical unresolved classification.

### 27.2 Validate tree structure

Independently prove:

- one rooted tree per document;
- complete reachability;
- no parent cycles;
- canonical order;
- reciprocal previous/next links.

### 27.3 Validate chunks/sources

Prove:

- one source per chunk;
- one chunk per source;
- chunk text byte reconstruction;
- membership UTF-8 boundaries;
- deterministic chunk order;
- citation-node derivation;
- addressable-ancestor consistency.

### 27.4 Validate page provenance

Recompute:

- exact node byte partitions;
- page bounds;
- source page ranges;
- box validity;
- page count domain.

### 27.5 Validate exact clause coverage

For every addressable clause:

- resolve one exact canonical subtree;
- compute the exact-lookup chunk set;
- exclude any chunk containing retrievable text outside the subtree;
- require non-empty lookup set;
- merge member intervals per retrievable node;
- require byte-complete coverage of every retrievable node in the subtree;
- reject contentless addressable subtrees.

This gate is central to Phase 2 correctness.

### 27.6 Failure ordering

If the catalog gate fails:

- do not build the lexical index;
- do not assemble a release;
- retain diagnostic reports;
- leave active release unchanged.

Phase 3 embedding/vector builders do not exist yet and therefore cannot be invoked.

## 28. Work package 2.23: Lexical-engine benchmark

### 28.1 Candidate engines

Benchmark the design candidates that remain practical in the supported package environment:

- SQLite FTS5;
- BM25S;
- Tantivy bindings.

Do not select an engine solely from prior preference.

### 28.2 Evaluation corpus

Use Phase 0 cases covering:

- English engineering terms;
- Chinese queries;
- cross-language cases where lexical matching is expected to contribute;
- document codes;
- exact clause identifiers;
- table numbers;
- model numbers;
- abbreviations;
- exact phrases;
- numbers;
- units;
- punctuation-heavy identifiers.

### 28.3 Measurements

Compare:

- Recall@5/10/20;
- MRR/nDCG where applicable;
- exact-token preservation;
- Chinese tokenization behavior;
- punctuation/unit tokenization;
- field weighting;
- index byte size;
- build time;
- load/startup time;
- query latency;
- deterministic rebuild bytes or deterministic logical output;
- packaging complexity.

### 28.4 Accuracy-first selection

Select the engine/configuration only after quality comparison.

The selected lexical configuration must also satisfy the Phase 2 blocking retrieval gates in Section 50.2: the one-sided 95% Wilson lower bound for expected evidence at Recall@20 is at least 98%, and the corresponding lower bound for expected evidence in the Top 5 is at least 95%, using independently labelled applicable cases and the Phase 0 sample-size rules. A candidate that is correctly benchmarked but misses either bound cannot be selected for an activatable Phase 2 release.

Packaging convenience cannot justify materially worse retrieval.

### 28.5 Chinese tokenization decision

Document the selected Phase 2 tokenization strategy as an evidence-backed decision.

Keep lexical-engine-specific details behind a stable retrieval interface.

## 29. Work package 2.24: Lexical index builder

### 29.1 Inputs

The lexical cache/build identity includes:

- ordered chunk `search_text` hashes;
- metadata/filter hashes;
- lexical engine identity/version;
- tokenizer/configuration;
- schema/index version.

### 29.2 Deterministic row/source mapping

Lexical hits must map deterministically back to catalog `chunk_id`/`source_id`.

Do not depend on transient insertion order unless that order is itself a validated versioned contract.

### 29.3 No second authority

The lexical index stores/references derived search material only.

It does not become authority for:

- source text;
- edition;
- clause number;
- page mapping;
- classifications.

Those values are rejoined from the catalog.

### 29.4 Safe query compiler

Raw user query text is never accepted directly as an FTS expression or SQL fragment.

A dedicated query compiler:

- validates length/encoding;
- tokenizes/escapes according to selected mode;
- uses bound SQL parameters;
- prevents FTS operator injection;
- preserves literal engineering identifiers as appropriate.

## 30. Work package 2.25: Exact clause lookup service

### 30.1 Input semantics

Accept exact:

- opaque `document_id`;
- normalized exact `clause_number`.

No fuzzy lookup, edition substitution, or “latest” behavior.

### 30.2 Lookup algorithm

1. validate input grammar/bounds;
2. resolve exactly one addressable node through indexed catalog query;
3. identify its validated retrievable subtree;
4. select the catalog-gated exact-lookup chunk set;
5. join each chunk to its sole source row;
6. reconstruct/project source-faithful direct evidence;
7. order by chunk canonical order/source ID as defined;
8. generate deterministic citation fields from canonical/page provenance.

### 30.3 Missing clause

A missing document or clause is an explicit not-found result/error in the calling adapter; never return the nearest clause.

### 30.4 Direct-result semantics

The Phase 2 primitive returns the exact direct lookup set only.

It does not claim Phase 4 required context closure.

## 31. Work package 2.26: Lexical direct-search service

### 31.1 Filter semantics

Support design-aligned filters such as:

- document IDs/codes/editions as appropriate;
- status;
- document type;
- jurisdiction;
- discipline;
- exact clause or other deterministic query-analysis hints where implemented.

OR values within one filter class and AND across classes where the final design requires that behavior.

### 31.2 Status default

Default ordinary lexical search to `active` documents.

An explicit null/no-status filter removes that default so historical superseded/withdrawn documents remain searchable when requested.

### 31.3 Candidate result

A hit contains stable catalog identities and scores sufficient to order direct candidates, then joins to catalog source/citation data.

Search score is retrieval metadata, never source authority.

### 31.4 Empty search result

The direct Phase 2 service returns an empty candidate set rather than inventing an answer.

Final `evidence_insufficient` warning/refusal behavior belongs to the Phase 4 final evidence assembly surface.

## 32. Work package 2.27: Deterministic direct evidence projection

Define a Phase 2 internal/Python result object for direct candidates containing enough data for debugging, evaluation, and future Phase 4 assembly:

- release identity;
- document ID/code/edition;
- source ID;
- chunk ID;
- citation node ID;
- exact clause projection or null;
- source `original_text`;
- canonical node/member identities;
- page start/end;
- ordered intersecting page/box mappings;
- document type/status/normative metadata projections;
- exact node classification records/provenance needed to verify Phase 2 classification tests;
- parser/OCR uncertainty records available from the build;
- direct retrieval channel/rank/score;
- deterministic citation string/fields.

This is not named or advertised as the final `docs/design.md` Section 21 Evidence Package unless it fully satisfies that contract later.

## 33. Work package 2.28: Deterministic citations

### 33.1 Citation inputs

Generate citation fields only from validated catalog data:

- document code;
- edition;
- exact clause projection;
- page/page label;
- source ID;
- source hash/release identity as required internally.

### 33.2 No AI citation generation

No LLM/client-generated citation correction is allowed.

### 33.3 Page projection

Page bounds come from exact `chunk_nodes`/`node_page_spans` intersections and the validated source row.

Do not trust stale stored display fields.

### 33.4 Missing boxes

A missing optional bounding box does not change the page/citation identity. Preserve page-only provenance for later warning projection.

### 33.5 Citation tests

Use the complete Phase 0 deterministic citation suite and require zero document/edition/clause/page failures for Phase 2-supported cases.

## 34. Work package 2.29: Read-only runtime catalog

### 34.1 Startup order

The runtime:

1. resolves `active.json` or explicitly selected release;
2. validates pointer syntax/identity;
3. validates release manifest/checksums;
4. validates supported schema/vocabulary versions;
5. opens `knowledge.sqlite` read-only;
6. enables/verifies foreign keys;
7. enables/verifies `query_only`;
8. runs `foreign_key_check`;
9. loads/validates lexical index metadata;
10. exposes services only after all required checks pass.

### 34.2 No release mutation

Normal runtime operation must not modify:

- release files;
- SQLite catalog;
- indexes;
- release manifest;
- build reports.

Runtime logs/telemetry use a separate configured state directory.

### 34.3 Integrity failure

A checksum/schema/catalog-integrity failure is `release_integrity_failed` and prevents the runtime/MCP session from starting.

Do not attempt automatic repair of immutable release bytes.

## 35. Work package 2.30: Safe source-file access

For page/resource operations:

- resolve catalog source locator beneath the approved originals root;
- reject absolute/empty/`..` escape;
- resolve symlinks/junctions/reparse points;
- require regular file;
- verify identity/size/hash according to the design before emitting source bytes;
- never construct paths from client input directly.

Client IDs are catalog keys, not filesystem paths.

## 36. Work package 2.31: CLI surface

### 36.1 Phase 2 builder commands

Implement or scaffold with complete Phase 2 behavior:

```text
clausesift init <workspace>
clausesift ingest <path>
clausesift build
clausesift validate
clausesift release
```

### 36.2 Phase 2 runtime commands

Implement:

```text
clausesift list-documents
clausesift search <query>
clausesift get-clause <document-id> <clause>
clausesift mcp
```

### 36.3 Direct retrieval disclosure

`search` and `get-clause` in the exact-retrieval milestone must clearly state in machine-readable/help semantics that they return **direct Phase 2 evidence** without Phase 4 context expansion.

Do not label their structured output as a complete `docs/design.md` Section 21 Evidence Package.

### 36.4 Shared service layer

CLI does not issue its own SQL or lexical queries. It calls the same runtime catalog/direct-retrieval services used by Python and later MCP evidence assembly.

## 37. Work package 2.32: Basic MCP server

### 37.1 Transport/protocol baseline

Implement the MCP stdio server baseline required by the design for supported Phase 2 surfaces:

- stdout reserved exclusively for MCP frames;
- operator logs/tracebacks to stderr or configured log sink;
- bounded input frame handling;
- duplicate-key/I-JSON validation;
- strict schemas with `additionalProperties: false`;
- safe centralized serializer;
- protocol/application error separation;
- supported design protocol-revision compatibility for the surfaces actually advertised.

### 37.2 Advertised tools

Advertise Phase 2-complete tools such as:

- `get_document_metadata`;
- `list_documents`;
- `get_page_reference`.

### 37.3 Advertised resources

Advertise only resources Phase 2 can satisfy exactly:

- document metadata resource;
- page resource;
- active release resource.

### 37.4 Evidence tools remain gated

Do not advertise a successful final `search_evidence`, `get_clause`, `get_context`, or clause/evidence resource until Phase 4 implements required context and final Evidence Package serialization.

### 37.5 Error safety

Phase 2 MCP errors use the design's strict safe error routing for implemented surfaces.

No exception text, path, credential, or arbitrary client-controlled diagnostic body leaks into results.

## 38. Work package 2.33: MCP document metadata

Implement `get_document_metadata` exactly enough to project safe manifest/catalog data:

- release;
- immutable document ID;
- code/title/edition;
- vocabulary version;
- document type;
- normative status;
- lifecycle status;
- authority;
- jurisdiction/discipline sets;
- source hash;
- review/admission status;
- release identity.

Do not expose absolute source paths or infer legal force.

## 39. Work package 2.34: MCP document listing

Implement the final `docs/design.md` `list_documents` contract now because this tool is advertised as a completed Phase 2 surface.

### 39.1 Stable order and page size

- sort every result page by stable `(document_code, edition, document_id)` order;
- constrain `limit` to 1-100 with default 50;
- always return `items` and `next_cursor`;
- return `next_cursor: null` on the final page.

### 39.2 Mandatory opaque authenticated cursor

The cursor is a versioned opaque authenticated encoding of exactly:

```text
{
  release_id,
  cursor_version,
  order_version,
  normalized_filters,
  last_key
}
```

where:

- `normalized_filters` contains canonical `document_type`, `status`, and `discipline`, including null values;
- `last_key` is the last emitted `(document_code, edition, document_id)` tuple;
- the compact encoded cursor, including authentication tag, must never exceed the design's 4,096-scalar input/output bound.

### 39.3 Strict keyset resumption

Resume with a strict lexicographic keyset predicate over `(document_code, edition, document_id)`. Offset pagination is forbidden.

Cursor/filter/release handling is exact:

- invalid authentication -> `identifier_invalid`;
- unsupported cursor/order version -> `identifier_invalid`;
- filter mismatch -> `identifier_invalid`;
- valid cursor bound to another active release -> `resource_not_found`.

### 39.4 Cursor regression tests

Cover:

- maximum multibyte payload still within 4,096 scalars;
- one-over/invalid cursor input;
- tampering;
- filter mutation;
- release change;
- duplicate code/edition prefixes distinguished by `document_id`;
- empty page;
- final page;
- repeated pagination through an immutable release with zero gaps/duplicates.

No lexical engine query is needed for document listing.

## 40. Work package 2.35: MCP page reference/resource

### 40.1 `get_page_reference`

Use exact document ID and one-based page number within manifested count.

Return only the safe catalog-bound URI/hash metadata required by the design.

### 40.2 Page resource

Implement the design's full verified-PDF page-resource semantics only if the complete frame/source-size budgets can be enforced exactly.

Release admission must precompute the worst-case frame bound before making a document available through this resource.

### 40.3 Integrity races

Tests must cover pathname replacement/mutation and ensure only verified buffered bytes are emitted; otherwise return the design's complete integrity error with no partial contents.

This belongs to Phase 2 because it is deterministic source/citation access, not context retrieval.

## 41. Work package 2.36: Static build/review report

Generate an offline static report for Phase 2 review containing:

- registered document/manifests summary;
- source hashes/status;
- parser-validation report links/content;
- canonical tree inspection;
- classification/provenance inspection;
- node/page mapping coverage;
- chunk inspection;
- table chunk inspection;
- direct cross-reference resolution status;
- catalog validation results;
- lexical benchmark/index summary;
- exact lookup/citation evaluation results;
- current Phase 2 quality-gate status;
- release candidate/checksum status;
- known deferred Phase 3/4 capabilities.

Do not fabricate conflict/context/dense-retrieval report sections as if those later phases were implemented.

### 41.1 Static-report safety

Treat every source/manifest/parser/report string as untrusted data.

Use context-aware escaping and the restrictive offline CSP required by the design.

No report makes external network requests.

## 42. Work package 2.37: Phase 2 content-addressed cache

Implement cache nodes only for Phase 2 artefacts:

- parser-neutral output;
- passing parser-validation report;
- canonical model;
- page-provenance map;
- chunks/source rows;
- basic cross-reference artefact;
- lexical index;
- Phase 2 catalog/release assembly artefacts where applicable.

Do not create embedding/vector/reranker caches in this phase.

### 42.1 Cache identity

Use the design's declared direct inputs and upstream artefact hashes, including:

- source hash/size;
- approved manifest-content hash;
- parser/role/configuration/asset identities;
- parser report hash;
- vocabulary hash;
- normalizer/classification versions;
- page mapper;
- chunker;
- cross-reference resolver;
- lexical engine/configuration;
- schema versions;
- dependency lock;
- build-toolchain fingerprint.

### 42.2 Cache hits do not skip validation

Reused bytes still pass all applicable downstream catalog/release validation.

### 42.3 Failed parser report

Only passing deterministic parser-validation reports enter the content cache. Failed reports remain diagnostics outside the admitted cache.

## 43. Work package 2.38: Build content identity

Define deterministic Phase 2 build identity from the artefacts actually implemented/admitted in this milestone.

It must include:

- canonical manifest-content hashes;
- source hashes/sizes;
- evidence-vocabulary hash;
- parser/provenance artefact hashes;
- canonical model/page/chunk/catalog hashes;
- cross-reference and lexical artefact hashes;
- Phase 2 evaluation corpus/gate versions;
- dependency lock;
- toolchain fingerprint;
- reproducible build epoch;
- release/schema configuration.

It must exclude:

- wall-clock timestamps;
- random run IDs;
- credentials;
- absolute paths.

Phase 3/4 artefact hashes cannot appear until those artefacts exist.

## 44. Work package 2.39: Immutable milestone release assembly

### 44.1 Release principle

Every published Phase 2 milestone release is immutable/read-only.

A rebuild creates a new release identity when admitted semantic/artefact inputs change.

### 44.2 Phase 2 release contents

The exact-retrieval release includes the subset of the design release layout that is actually implemented, such as:

```text
releases/<release_id>/
├── manifest.json
├── build-info.json
├── evidence-vocabulary.json
├── knowledge.sqlite
├── chunks.jsonl              # optional audit projection
├── lexical-index/
├── reports/
├── build-ledger.jsonl
└── evaluation-results.json
```

It must not contain dummy embeddings/vector indexes/models merely to resemble the final layout.

### 44.3 Capability declaration

The release/runtime capability record must truthfully state that this milestone supports direct exact/lexical retrieval and implemented metadata/page surfaces, while dense/hybrid/rerank/context-complete evidence capabilities are unavailable.

Use the design's existing capability/version model; do not invent a misleading “success” for absent features.

### 44.4 Release identity

Derive release ID using the design's versioned release-assembly identity over exactly the admitted Phase 2 artefacts/configuration.

No self-reference through `manifest.json`.

## 45. Work package 2.40: Release manifest and checksums

The release manifest records every admitted file with:

- relative path;
- byte size;
- SHA-256;
- artefact/schema role/version;
- relevant capability metadata.

Reject:

- missing file;
- extra unmanifested runtime artefact where the schema forbids it;
- checksum mismatch;
- size mismatch;
- unsafe path;
- unsupported version.

Runtime verifies before opening mutable-format parsers/loaders.

## 46. Work package 2.41: Candidate read-only smoke validation

Before publication/activation:

1. reopen the candidate through the normal read-only runtime path;
2. verify manifest/checksums;
3. open/query-only SQLite;
4. rerun foreign-key check;
5. load lexical index;
6. run exact clause direct-lookup fixtures;
7. run lexical direct-search fixtures;
8. verify deterministic direct citation/page results;
9. run metadata/list/page MCP smoke calls, including multi-page `list_documents` cursor resumption;
10. prove base runtime does not import build-only dependencies;
11. prove no release bytes are modified.

Do not run Phase 3/4 smoke assertions for features not yet implemented.

## 47. Work package 2.42: Atomic active pointer

### 47.1 Pointer record

Use the design's `active.json` model rather than an unsafe in-place mutable release directory.

The record identifies one complete immutable release.

### 47.2 Atomic replacement

Update through:

1. build/validate new pointer bytes in same filesystem/directory context;
2. write temporary file;
3. flush temporary file;
4. atomic replace/rename;
5. flush parent directory as required by supported platform durability policy.

### 47.3 Reader behavior

Concurrent readers see either:

- complete old pointer; or
- complete new pointer.

Never missing/torn/combined JSON.

### 47.4 Crash injection

Test crashes:

- before temp flush;
- immediately before replace;
- immediately after replace before directory flush;
- after directory flush.

Recovery follows the design's old-or-new guarantees.

## 48. Work package 2.43: Rollback

`clausesift release`/validation tooling must support explicit rollback to a previously validated immutable release.

Rollback:

- validates target release/checksums first;
- uses the same atomic pointer replacement path;
- never mutates old/new release contents;
- records operator lifecycle event outside the immutable release;
- passes the same crash/reader tests as forward activation.

## 49. Work package 2.44: Build and operator ledgers

### 49.1 Deterministic embedded build ledger

Record deterministic build events through the declared Phase 2 seal cutoff using:

- sequence numbers;
- hash chaining;
- deterministic input/output hashes;
- reproducible build epoch;
- no random run ID/wall clock.

### 49.2 External operator lifecycle ledger

Record operational events outside releases:

- actual start/finish/failure times;
- operational run ID;
- candidate validation;
- publication;
- active-pointer switch;
- rollback/recovery.

Operational history never mutates sealed release bytes.

## 50. Work package 2.45: Phase 2 evaluation

Run the applicable Phase 0 evaluation slices after candidate catalog/index generation and before release admission.

### 50.1 Exact deterministic gates

Require zero failures for Phase 2-supported deterministic suites such as:

- exact clause identity/lookup set;
- correct document/edition/clause/page citation;
- vocabulary/schema round trip;
- classification provenance/inheritance deterministic fixtures;
- legacy-alias rejection;
- unsupported vocabulary-version rejection;
- wrong-edition exact-lookup negatives;
- source-hash/path integrity fixtures.

### 50.2 Lexical probabilistic blocking gates

For the exact-retrieval milestone, lexical retrieval is an implemented release capability, so the design's retrieval thresholds are blocking now rather than deferred.

Require:

- expected evidence present in Recall@20: **one-sided 95% Wilson lower confidence bound at least 98%**;
- expected evidence present in Top 5: **one-sided 95% Wilson lower confidence bound at least 95%**.

The gate report must include, for each metric:

- numerator/successes;
- denominator/applicable independently labelled cases;
- point estimate;
- one-sided 95% Wilson lower bound;
- target;
- pass/fail;
- corpus/question/label-set versions;
- excluded/not-applicable cases with reasons.

Phase 0 sample-size rules apply independently: at least 150 applicable independently labelled cases for the 98% Recall@20 gate and at least 60 for the 95% Top-5 gate, increased when required strata would otherwise be underrepresented. A small exploratory seed cannot be used to claim either release gate.

Also report, without replacing the two mandatory thresholds:

- Recall@5/10;
- MRR;
- nDCG;
- correct-document rate;
- correct-edition rate;
- correct-clause/page hit where direct candidates permit it;
- table-evidence hit rate;
- multilingual strata.

A lexical configuration that misses either mandatory Wilson lower bound blocks Phase 2 release activation.

### 50.3 Deferred gates

Do **not** claim pass/fail for Phase 3/4-only metrics such as:

- dense retrieval quality;
- fusion;
- reranker quality;
- context-path fidelity;
- optional-context precision;
- conflict all-side runtime preservation;
- final refusal/evidence-support behavior.

Reports label them `not_implemented_in_phase_2`, not zero and not passed.

## 51. Work package 2.46: Phase 2 quality gate

A Phase 2 milestone release may be activated only when:

- all manifests/source hashes pass;
- parser gates pass;
- canonical/classification gates pass;
- page-provenance gates pass;
- chunk/source/catalog gates pass;
- exact clause coverage gate passes;
- lexical index validates;
- Recall@20 one-sided 95% Wilson lower bound is at least 98% on the required independently labelled sample;
- Top-5 evidence-presence one-sided 95% Wilson lower bound is at least 95% on the required independently labelled sample;
- all other applicable Phase 2 evaluation gates pass;
- static report is durable;
- no Phase 2 release-blocking finding remains;
- candidate checksums pass;
- read-only smoke tests pass.

It must be clearly identified operationally as the exact-retrieval milestone rather than the final high-accuracy release if Phase 3/4 capabilities are absent.

## 52. Work package 2.47: Runtime security and query safety

### 52.1 SQL

All SQL uses bound parameters.

No client identifier becomes an SQL fragment.

### 52.2 FTS

All lexical queries pass through the safe query compiler.

### 52.3 Paths

Client document/source/page identifiers resolve through catalog rows first, then safe root-contained paths.

### 52.4 Output serializer

Use explicit allowlists and closed schemas for public MCP/CLI structured outputs.

Unknown internal fields fail closed rather than leaking.

### 52.5 Logging

Runtime query/evidence text logging defaults off.

Credentials/absolute paths are never loggable.

## 53. Work package 2.48: Unit tests

### 53.1 Manifest tests

Cover:

- safe YAML;
- custom tags;
- duplicate keys;
- unknown fields;
- every enum;
- legacy aliases;
- hash format;
- exact-key bounds;
- path normalization;
- approval mismatch;
- raw-only formatting changes;
- relation canonicalization/duplicates.

### 53.2 Canonical-model tests

Cover:

- stable IDs;
- one root;
- parent cycles;
- disconnected nodes;
- dense order;
- exact clause uniqueness;
- classification origin/provenance;
- narrow inheritance;
- `unclassified`/`unknown` tier policy.

### 53.3 Page-provenance tests

Cover:

- exact partition;
- UTF-8 boundaries;
- multi-page nodes;
- missing optional boxes;
- invalid boxes;
- out-of-range page;
- gaps/overlap/order.

### 53.4 Chunker tests

Cover:

- clause/subclause boundaries;
- requirement/exception representations;
- tables and rows;
- token splitting;
- deterministic IDs/order;
- membership reconstruction;
- citation-node DCA;
- addressable-ancestor consistency;
- atomic target source-contained cover.

### 53.5 Catalog tests

Cover every schema constraint, foreign-key initialization, `query_only`, and independent validation query.

### 53.6 Lexical tests

Cover:

- literal identifiers;
- FTS operator injection;
- punctuation;
- units;
- Chinese tokenization;
- filters;
- default status;
- deterministic mapping/order;
- Recall@20/Top-5 Wilson-gate exact pass/fail boundary calculations.

### 53.7 Citation tests

Cover exact source/page reconstruction and no client/AI repair.

### 53.8 `list_documents` cursor tests

Cover the complete Section 39 cursor contract, including authentication, filter/release binding, ordering-version checks, strict keyset resumption, worst-case size, tampering, and no duplicates/gaps.

## 54. Work package 2.49: Integration tests

Implement end-to-end tests for:

- workspace initialization;
- manifest registration/approval;
- Phase 1 parser route invocation;
- canonical tree build;
- page provenance;
- chunk/source creation;
- cross-reference resolution;
- fresh SQLite catalog creation;
- catalog freeze/gate;
- lexical index build;
- exact lookup;
- lexical direct search;
- citation projection;
- static report generation;
- candidate release assembly;
- read-only runtime load;
- basic CLI;
- basic MCP metadata/list/page surfaces, including cursor pagination;
- active pointer publication;
- rollback.

## 55. Work package 2.50: Failure-injection tests

At minimum inject:

- manifest schema failure;
- approval mismatch;
- source hash mismatch;
- parser failure;
- parser comparison failure;
- canonical classification failure;
- invalid tree;
- page-provenance gap;
- chunk reconstruction mismatch;
- orphan chunk/source;
- exact clause coverage gap;
- foreign-key violation;
- lexical builder failure;
- lexical Recall@20 gate failure;
- lexical Top-5 gate failure;
- invalid/tampered/stale-release document-list cursor;
- evaluation execution failure;
- quality-gate failure;
- candidate checksum failure;
- read-only smoke failure;
- pointer-write/replace crash.

Every failure must prove:

- applicable diagnostics remain available;
- downstream Phase 2 builders do not run after their gate;
- active release remains unchanged until the defined atomic replacement boundary;
- no partial mutable release is served.

## 56. Work package 2.51: Regression tests

Use Phase 0 fixtures to pin:

- manifested document metadata;
- canonical tree snapshots/hashes;
- classification/provenance snapshots;
- page mappings;
- chunk/source identities;
- exact clause lookup sets;
- table representations;
- lexical search expected IDs/ranks;
- deterministic citations;
- cross-reference resolved/unresolved records;
- SQLite query plans;
- document-list pagination/cursor behavior;
- release checksums/identity;
- rollback behavior.

A source/manifest/parser/configuration change may intentionally update snapshots only through reviewed versioned changes.

## 57. Work package 2.52: Packaging tests

Test:

- wheel build;
- sdist build;
- clean base install;
- build-extra install;
- OCR-extra install where supported;
- CLI entry point;
- basic MCP start;
- base runtime without build-only imports;
- release portability across supported local runtime environments where the design/toolchain permits it.

## 58. Work package 2.53: Documentation/configuration deliverables

Phase 2 should produce implementation-facing docs/configuration for:

- workspace format;
- manifest authoring/approval;
- package extras;
- canonical schema versions;
- lexical engine/tokenizer decision;
- release layout;
- runtime startup/rollback;
- direct retrieval versus final Phase 4 evidence-tool boundary;
- `list_documents` stable order/cursor contract;
- lexical release-gate thresholds;
- known unsupported/deferred capabilities.

Do not duplicate the design document; link to normative sections and document implementation-specific decisions only.

## 59. Phase 3 handoff

Phase 2 hands Phase 3:

- immutable catalog/chunk/source identities;
- deterministic `embedding_text` projection inputs;
- chunk canonical row order;
- stable direct lexical retrieval interface;
- Phase 0 retrieval benchmark splits;
- release/cache architecture into which chunk embeddings/vector artefacts can be added;
- runtime capability gating for unavailable dense/hybrid mode.

Phase 2 must not select or generate embeddings on Phase 3's behalf.

## 60. Phase 4 handoff

Phase 2 hands Phase 4:

- canonical node tree;
- node classifications/provenance;
- page provenance;
- source-contained atomic chunks;
- broader retrieval chunks;
- sources;
- basic resolved/unresolved cross-reference records;
- exact direct lookup primitive;
- lexical direct candidates;
- deterministic citation/source projections;
- read-only catalog/runtime service;
- basic MCP protocol infrastructure.

Phase 4 owns:

- deterministic Evidence Graph traversal;
- required/supporting/diagnostic closure;
- final context completeness;
- final Evidence Package assembly;
- final evidence-returning MCP tools/resources;
- high-accuracy reranking integration;
- conflict runtime closure/serialization;
- final typed warning/refusal behavior.

## 61. Acceptance criteria

Phase 2 is complete only when all of the following are true.

1. `clausesift` builds as a Python distribution and installs with separated runtime/build dependencies.
2. `clausesift init` creates a safe idempotent local workspace.
3. Manifest schema v2 is closed, safe-loaded, normalized, hashed, and human-approval-bound exactly as designed.
4. Source hashes/sizes/page counts are validated before ingestion.
5. Phase 1 parser routes are bound to manifests; critical documents use independent comparison.
6. Blocking parser failures produce no canonical artefact.
7. The exact ClauseSift Engineering Evidence Vocabulary is materialized and hash-bound.
8. Canonical nodes and classifications/provenance are deterministic and validated.
9. Every document has one validated rooted node tree with deterministic sequence links.
10. Every non-empty node has exact page-provenance byte coverage.
11. Standards-aware chunks preserve source-faithful text and deterministic memberships.
12. Atomic future context targets have source-contained chunk coverage without implementing Phase 4 traversal.
13. Whole-table and row-level searchable representations exist.
14. Every chunk has exactly one source row and derived page range.
15. Basic cross-reference records are exact and unresolved references remain explicit/non-guessed.
16. SQLite enforces foreign keys/constraints and becomes byte-stable at the catalog gate.
17. Every addressable clause has a unique, non-empty, byte-complete exact-lookup set with no out-of-subtree leakage.
18. Required exact/filter catalog indexes exist and query-plan regression tests use them.
19. A lexical engine/tokenizer is selected from Phase 0 benchmark evidence and meets the blocking Recall@20 and Top-5 Wilson lower-bound thresholds.
20. Lexical query compilation prevents SQL/FTS expression injection.
21. Exact clause direct lookup returns deterministic source candidates with no edition substitution.
22. Lexical direct retrieval supports design-aligned metadata filters and active-status default.
23. Deterministic document/edition/clause/page citations pass the complete applicable Phase 0 deterministic suite.
24. Read-only runtime verifies release checksums/schema/vocabulary/catalog before serving.
25. CLI builder/runtime commands use shared services and identify direct Phase 2 retrieval honestly.
26. Basic MCP metadata/list/page/release surfaces satisfy their final schemas and protocol safety requirements.
27. `list_documents` uses mandatory stable `(document_code, edition, document_id)` keyset pagination with authenticated filter/order/release-bound cursors and no gaps/duplicates.
28. Final context-complete evidence MCP tools are not falsely advertised before Phase 4.
29. Static Phase 2 reports are offline, escaped, deterministic where required, and show deferred capabilities explicitly.
30. Phase 2 caches include complete declared identities and never bypass validation.
31. Exact-retrieval milestone releases are immutable and contain no dummy Phase 3/4 artefacts.
32. Candidate releases reopen successfully through the normal read-only runtime before activation.
33. `active.json` publication and rollback are atomic and crash-tested.
34. Phase 2 evaluation gates pass with sample counts/confidence intervals where applicable; Recall@20 lower bound is at least 98% and Top-5 lower bound at least 95% on their independently labelled samples.
35. Failures before activation do not modify the active release.
36. Runtime operation does not modify release bytes.
37. Base runtime does not import build/OCR dependencies.
38. Phase 3 embeddings/fusion and Phase 4 traversal/reranking/refusal remain out of scope.
39. Repository quality checks pass.

## 62. Risks and mitigations

### 62.1 Phase 2 accidentally becomes the full product

**Risk:** Detailed final-design contracts tempt implementation of dense retrieval/context/reranking early.

**Mitigation:** Capability boundary in Sections 2-3 and explicit Phase 3/4 handoffs; no dummy or partial final evidence tools.

### 62.2 Exact lookup leaks another clause

**Risk:** A broad chunk spanning multiple addressable branches appears in an exact clause result.

**Mitigation:** Catalog-gated subtree membership and byte-complete exact-lookup validation.

### 62.3 Normalized text becomes evidence

**Risk:** Search repair changes quoted engineering text.

**Mitigation:** `original_text` is source-faithful; search enrichment is derived/non-authoritative.

### 62.4 SQLite application checks drift

**Risk:** Invalid relationships enter catalog when Python validation misses one path.

**Mitigation:** SQL constraints plus independent catalog validation queries and `foreign_key_check`.

### 62.5 Lexical engine becomes public API

**Risk:** Later engine replacement breaks callers.

**Mitigation:** Stable direct retrieval interface; engine-specific tokens/scores remain internal retrieval metadata.

### 62.6 Chinese retrieval is under-tested

**Risk:** English BM25 quality masks Chinese tokenization failure.

**Mitigation:** mandatory multilingual benchmark strata before lexical selection.

### 62.7 Milestone release is mistaken for final evidence completeness

**Risk:** Direct source hits are interpreted as context-complete engineering answers.

**Mitigation:** do not advertise final evidence MCP tools; CLI/direct APIs declare direct-retrieval semantics; unavailable capabilities fail visibly.

### 62.8 Release mutation

**Risk:** evaluation/logging/pointer state contaminates immutable release bytes.

**Mitigation:** catalog freeze, immutable directories, external operator state, checksum verification, read-only runtime tests.

### 62.9 Copyright leakage through reports

**Risk:** static reports or `chunks.jsonl` expose proprietary standards in a public repository.

**Mitigation:** apply Phase 0 rights policy to generated artefacts; releases remain local; repository fixtures use rights-cleared samples only.

## 63. Recommended implementation sequence

Execute Phase 2 in this order.

1. Bootstrap Python package/dependency boundaries.
2. Implement safe workspace initialization.
3. Implement manifest schema/loader/hash/approval.
4. Implement source registration/change detection.
5. Bind Phase 1 parser routing and parser-validation gate.
6. Materialize/validate evidence vocabulary.
7. Build canonical model and classification provenance.
8. Validate canonical trees.
9. Build/validate node page provenance.
10. Build standards-aware chunks/source rows.
11. Build basic exact cross-reference records.
12. Materialize SQLite catalog with constraints/indexes.
13. Freeze catalog and run every Phase 2 blocking validation query.
14. Benchmark lexical candidates/tokenizers on Phase 0 corpus and enforce the mandatory Recall@20/Top-5 Wilson gates before selection.
15. Select and implement lexical index builder/loader only from a passing configuration.
16. Implement exact clause direct lookup.
17. Implement lexical direct retrieval/filtering.
18. Implement deterministic direct evidence/citations.
19. Implement read-only runtime startup/integrity checks.
20. Implement CLI surfaces.
21. Implement basic MCP metadata/list/page/release surfaces, including mandatory authenticated keyset pagination for `list_documents`.
22. Generate static Phase 2 review report.
23. Implement Phase 2 cache identities.
24. Run applicable Phase 0 regression evaluation.
25. Persist evaluation/report results and enforce Phase 2 gates.
26. Assemble immutable milestone release.
27. Validate checksums and reopen read-only candidate.
28. Run candidate smoke tests.
29. Publish and atomically update `active.json`.
30. Prove rollback/crash behavior.
31. Run packaging/import-boundary tests.
32. Freeze Phase 2 handoff artefacts for Phase 3 and Phase 4.

No step may use a later-phase capability as a shortcut for an earlier deterministic requirement.

## 64. Definition of done

Phase 2 is done when another implementation agent can reproduce, from repository documentation and fixtures alone:

- how source documents are registered and approved;
- how Phase 1 parser output becomes one canonical model;
- how evidence classifications are derived and provenanced;
- how every source byte maps to pages;
- how chunks/source IDs are constructed and validated;
- how exact clause lookup is made byte-complete and edition-safe;
- how lexical retrieval is indexed, queried, filtered, evaluated, and blocked when its mandatory Wilson bounds are missed;
- how source-faithful direct evidence and citations are projected;
- how SQLite invariants prevent cross-document or malformed evidence;
- how the runtime opens an immutable release safely;
- which CLI/MCP surfaces are valid at this milestone;
- how `list_documents` paginates deterministically with authenticated release-bound keyset cursors;
- why final evidence-returning MCP tools remain gated until Phase 4;
- how build caches invalidate;
- how candidate releases are validated, activated, and rolled back;
- which Phase 2 gates must pass;
- which capabilities remain explicitly deferred.

The central Phase 2 deliverable is a **deterministic, immutable exact/lexical evidence-retrieval foundation**, not semantic or high-accuracy retrieval.
