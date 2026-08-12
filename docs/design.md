# ClauseSift Design Document

**Document version:** 0.1  
**Status:** Initial design baseline  
**Project:** ClauseSift  
**Repository:** `grammy-jiang/clause-sift`  
**Primary implementation language:** Python  

## 1. Executive summary

ClauseSift is an accuracy-first evidence retrieval engine for engineering standards, codes, design guidelines, technical manuals, and product specifications.

The initial use case is local retrieval across HVAC, ventilation, smoke-control, fire-safety, and manufacturer documentation. The system is intended for a single technical user and a relatively stable document corpus, with most documents changing no more than once per year.

ClauseSift is deliberately not designed as a general-purpose chat platform. Its primary output is a structured evidence package containing the correct document, edition, clause, context, page location, and original text. An AI client such as Claude Desktop or Claude Code may then interpret that evidence through an MCP interface.

The system adopts the following priority order:

1. Accuracy.
2. Query speed.
3. Traceability and reproducibility.
4. Operational simplicity.
5. Build speed.

The central architectural decision is to separate the system into two parts:

- an offline knowledge-base compiler that performs expensive parsing, OCR, structural analysis, chunking, embedding, indexing, validation, and release generation;
- a lightweight, read-only runtime that loads a compiled knowledge-base release and serves evidence through a Python API, CLI, and MCP server.

The compiler materializes a canonical **Evidence Graph**—the storage-neutral logical model formed by canonical evidence nodes and their typed structural and semantic relationships—together with rebuildable retrieval indexes. The graph organizes source-grounded evidence; it never replaces the original documents as authority.

This design allows ClauseSift to use slow, high-quality processing during infrequent document builds while keeping normal query operations fast and operationally simple.

---

## 2. Problem statement

Engineering design work frequently requires repeated consultation of several document classes:

- mandatory or referenced standards;
- codes and regulations;
- recommended design guidelines;
- technical manuals;
- manufacturer product specifications;
- superseded editions retained for historical projects;
- tables, appendices, figures, notes, exceptions, and cross-references.

General RAG platforms can ingest these documents, but they usually introduce infrastructure and abstractions that are unnecessary for this use case, including multi-user management, persistent task queues, object storage services, chat interfaces, agent orchestration, and online document synchronization.

More importantly, generic RAG systems often treat documents as unstructured text. Engineering standards require stronger guarantees:

- clause numbers must be preserved;
- document editions must not be mixed;
- mandatory requirements must be distinguished from guidance and notes;
- exceptions and parent scope conditions must accompany isolated requirements;
- table headers, units, and row context must survive extraction;
- citations must resolve to an original page and, where possible, a bounding box;
- retrieval must work for exact identifiers, technical terms, numbers, and natural-language questions;
- the system must explicitly report insufficient or conflicting evidence.

ClauseSift addresses this problem as an evidence-retrieval system rather than a PDF-chat application.

---

## 3. Goals

ClauseSift shall:

1. Ingest local engineering standards, codes, guidelines, manuals, and product specifications.
2. Preserve document identity, edition, status, jurisdiction, type, and source hash.
3. Preserve document structure down to clause, subclause, note, exception, table, and appendix level where possible.
4. Support exact identifier lookup, lexical retrieval, semantic retrieval, and reranking.
5. Return original source text with deterministic citations.
6. Expand retrieved evidence with relevant parent scope, exceptions, notes, tables, and cross-references.
7. Support immutable, versioned knowledge-base releases.
8. Allow release validation and rollback.
9. Expose retrieval through a Python library, command-line interface, and MCP server.
10. Operate locally without requiring MySQL, Redis, MinIO, Elasticsearch, or a permanently running vector database.
11. Be distributable as a standard Python installation package.
12. Permit parser, embedding, lexical-index, vector-index, and reranker components to be replaced through stable interfaces.
13. Include a regression-evaluation framework based on real engineering questions and expected evidence.

---

## 4. Non-goals

The first major version will not attempt to provide:

- multi-user authentication or authorization;
- a general-purpose web chat interface;
- enterprise document connectors;
- real-time document synchronization;
- collaborative annotation;
- a generic agent workflow engine;
- long-term conversational memory;
- automatic legal determination of whether a document is enforceable;
- complete HVAC or fire-engineering calculations;
- autonomous approval of engineering designs;
- a universal knowledge graph;
- automatic redistribution of copyrighted standards or specifications.

ClauseSift retrieves and organizes evidence. It does not replace professional engineering judgement or statutory review.

---

## 5. Core design principles

### 5.1 Accuracy before speed

ClauseSift shall not improve latency by silently removing retrieval channels, shrinking candidate pools below validated thresholds, dropping contextual clauses, or replacing original evidence with generated summaries.

Performance optimization begins only after retrieval and citation quality meet defined quality gates.

### 5.2 Original documents remain authoritative

The evidence hierarchy is:

1. original source page;
2. deterministic structured representation;
3. normalized text;
4. generated metadata, summaries, keywords, or query expansions.

Generated content may improve retrieval but must not become the final authority for an engineering conclusion.

### 5.3 Offline compilation, read-only runtime

All document-dependent computation that can be performed once shall be performed during a build:

- parsing and OCR;
- layout analysis;
- clause-tree construction;
- text normalization;
- chunk construction;
- table expansion;
- cross-reference extraction;
- chunk embeddings;
- lexical indexing;
- vector indexing;
- page rendering and coordinate mapping;
- validation and regression tests.

At query time, the runtime should only:

- analyse the query;
- apply metadata filters;
- compute query embeddings when needed;
- search prebuilt indexes;
- fuse and rerank candidates;
- expand evidence context;
- return structured evidence.

### 5.4 Deterministic rules before LLM inference

The following should be supplied by manifests, parsers, rules, or human review rather than inferred freely by an LLM:

- document identifier;
- edition;
- authority;
- status;
- jurisdiction;
- document type;
- clause number;
- page number;
- file hash;
- supersession relationship;
- citation string.

### 5.5 Immutable knowledge-base releases

A published knowledge-base release is read-only. Updates produce a new release, which is validated before an atomic switch of the active release pointer.

This model supports reproducibility, rollback, and auditability.

### 5.6 Replaceable components

Parsers, embedding models, rerankers, and index engines are implementation choices, not permanent parts of the public data model.

The canonical document model and evidence API must remain stable when individual components change.

### 5.7 Fail visibly

Parser anomalies, unresolved references, low-confidence OCR, conflicting editions, and incomplete applicability conditions must be surfaced as warnings or build failures. They must not be hidden behind a plausible answer.

---

## 6. System context

```mermaid
flowchart LR
    U[Engineer] --> C[Claude Desktop / Claude Code]
    C <-->|MCP stdio| R[ClauseSift Runtime]
    R --> K[Compiled KB Release: Evidence Graph and indexes]
    B[ClauseSift Builder] --> K
    S[Local source documents] --> B
    M[Human-maintained manifests] --> B
    E[Evaluation corpus] --> B
```

ClauseSift does not require the AI client to be bundled with the package. The MCP server is an adapter between the client and the evidence-retrieval runtime.

---

## 7. High-level architecture

```mermaid
flowchart TB
    subgraph Build[Offline build environment]
        A[Source documents] --> B[Document registration]
        B --> C[Parser router]
        C --> PN[Parser-neutral artifacts]
        PN --> PV[Parser validation and comparison gate]
        PV --> D[Canonical document model]
        D --> I[Cross-reference resolver]
        D --> J[Page and bounding-box mapper]
        D --> E[Standards-aware chunker]
        J --> E
        E --> CG[Catalog validation gate]
        I --> CG
        CG --> F[Lexical index builder]
        CG --> G[Embedding builder]
        G --> H[Vector index builder]
        F --> EV[Regression evaluation, reports, and quality gates]
        H --> EV
        CG --> EV
        EV --> K[Candidate release assembler]
        K --> L[Checksum and read-only smoke validation]
        L --> AP[Atomic active-pointer switch]
        AP --> M[Immutable active KB release]
    end

    subgraph Runtime[Read-only runtime]
        Q[Query] --> QA[Query analyser]
        QA --> X[Exact lookup]
        QA --> Y[Lexical retrieval]
        QA --> Z[Dense retrieval]
        X --> FU[Fusion and deduplication]
        Y --> FU
        Z --> FU
        FU --> RR[Cross-encoder reranker]
        RR --> CE[Context expansion]
        CE --> EP[Evidence package]
    end

    M --> Runtime
    EP --> MCP[MCP / Python / CLI]
```

### 7.1 Evidence Graph architecture

The **Evidence Graph** is ClauseSift's versioned, deterministic, source-grounded logical graph of canonical engineering-evidence nodes and typed relationships. Its nodes are the canonical document-model nodes in Section 12; its edges are the validated structural relationships and typed semantic or cross-document relationships described by the catalog and Section 20. The name describes a logical contract, not a storage product: v0.1 persists the graph relationally in `knowledge.sqlite` and requires no Neo4j, RDF, SPARQL service, generic graph database, or universal knowledge graph.

The architecture has five distinct layers:

```mermaid
flowchart LR
    A[Authoritative sources: files, pages, manifests] --> G[Canonical Evidence Graph in SQLite]
    G --> I[Derived retrieval artifacts]
    Q[Runtime query] --> I
    I --> S[Bounded runtime evidence subgraph]
    G --> S
    S --> P[Evidence Package]
    P --> C[MCP, Python, and CLI clients]
```

1. **Authoritative source layer:** original files and pages plus human-reviewed manifests. These remain authoritative for text, identity, edition, status, and other manifest-owned facts.
2. **Canonical Evidence Graph:** immutable canonical nodes and validated relationships compiled for one release. It preserves document structure, source identity, applicability, dependencies, cross-references, and the information required to reconstruct provenance.
3. **Derived retrieval artifacts:** lexical indexes, embeddings, vector indexes, and caches. They accelerate candidate selection and are rebuildable from release inputs; they are never graph or source authority.
4. **Runtime evidence subgraph:** a bounded, deterministic selection consisting of retrieval seeds and context attached under declared relationship and traversal rules. It is a per-request view, not a mutable persisted graph.
5. **Evidence Package:** the client-facing serialization of that selected subgraph, including original evidence, citations, provenance, retrieval metadata, and visible warnings.

Every published graph is bound to the release ID, graph-schema version, vocabulary version, source hashes, and deterministic build inputs. Node identity is independent of a database engine. Every authoritative graph edge has declared semantics and either source provenance or an explicitly identified deterministic derivation; the word “graph” does not permit arbitrary LLM-generated facts. A future probabilistic relationship class would require a separate typed contract, provenance, confidence and review policy, and cannot be silently promoted to an authoritative edge.

Unresolved references remain explicit non-navigable records. Cycles in structural ownership are invalid; cycles among otherwise valid semantic references may exist but do not authorize unbounded traversal. Superseded editions and duplicate-looking requirements remain distinct through release-scoped document and node identity. Missing optional coordinates do not erase a node when its source text and document/clause identity are valid, but the absence remains visible in provenance and warnings. Table rows retain inherited headers, units, and parent context through declared relationships rather than retrieval-time guessing. New node or relationship types require versioned vocabulary/schema changes and must fail visibly in an older runtime.

Sections 12–14 define graph nodes and relational persistence, Sections 19–20 define context and semantic relationships, and Section 21 defines serialization. Later sections may refine relationship, provenance, traversal, and conflict contracts, but they must reuse this layered model rather than introduce a parallel graph or entity system.

### 7.2 Evidence Lineage

**Evidence Lineage** is the mandatory, deterministic derivation record for every Evidence Package item. It answers three separate questions without changing source authority: where the quoted evidence came from, which build transformations produced its canonical representation, and why the runtime selected or attached it. The complete lineage is:

```text
approved manifest + exact source bytes
    -> parser-neutral output(s) + parser-validation report
    -> canonical node(s) + page-provenance mappings
    -> chunk + source record
    -> checksummed lexical/vector/model artifacts
    -> retrieval candidate + fusion/rerank decision
    -> zero or more typed context edges
    -> Evidence Package item
```

The contract has three non-interchangeable dimensions:

| Dimension | Required meaning | Authority boundary |
| --- | --- | --- |
| **Source provenance** | Approved manifest-content hash, exact source-file hash and size, stable document/source identities, contributing canonical-node byte spans, and their ordered page/box mappings. | Original source bytes and the approved manifest remain authoritative. Missing optional boxes are represented explicitly; they are never reconstructed by a model. |
| **Build provenance** | Ordered parser roles and content hashes, passing validation-report hash, canonical/page/chunk transformation hashes and versions, stable node/chunk identities, diagnostic state, catalog hash, `build_content_id`, and lineage-schema version. | Parsers and deterministic transforms describe derivation, not new source facts. A comparator validates the selected primary output but never silently merges into it. |
| **Retrieval and assembly provenance** | Every contributing retrieval channel and release-artifact hash, candidate rank/score where meaningful, rerank decision, selection role, originating seed source, and each accepted context path as ordered typed edge steps with rule IDs. | Indexes, scores, ranking models, and traversal choices are non-authoritative selection metadata. They cannot create source text, applicability, or graph relationships. |

The builder materializes the first two dimensions plus release-artifact references as RFC 8785 canonical `lineage.json` after the retrieval artifacts are complete and before `build_content_id` is derived. It contains exactly one record for every manifested document and, beneath it, exactly one source-lineage record for each of that document's catalog `sources` rows. It identifies every selected parser route and ordered transformation by kind, role, producer/version/configuration hash, and content hash, and identifies the canonical catalog and retrieval artifacts. It contains no source locator, source text, credential, wall-clock timestamp, random run ID, `build_content_id`, `release_id`, or self-hash. The internal catalog retains the normalized source locator needed for authorized page access, but that path is never a public lineage field. The later release manifest binds the lineage-file hash, `build_content_id`, and `release_id` without a recursive identity dependency. The runtime joins that verified record to the catalog's node, chunk, source, membership, and page-span rows and adds the per-request assembly dimension; no parallel entity store is introduced.

Lineage is release-scoped and immutable. Stable document, node, chunk, source, relationship-occurrence, and edge identities survive a byte-identical rebuild. A changed source hash, approved manifest content, selected parser/configuration, canonical transformation, retrieval artifact, lineage schema, or admitted traversal/ranking configuration changes the corresponding artifact hash and therefore the build/release identity. A different runtime query changes only its per-request assembly lineage and never mutates the release. Reusing a filename for different bytes cannot preserve lineage, rollback restores the earlier release and its lineage together, and regenerated indexes are distinguishable unless their admitted bytes and all declared inputs are identical.

For source-bearing evidence, ordered lineage spans are the exact intersections of `chunk_nodes` membership with `node_page_spans`. They support a chunk assembled from several blocks or pages without inventing one scalar origin. `coordinate_status` is `page_and_box` only when every contributing page mapping has validated boxes and `page_only` otherwise; a missing box is accompanied by `source_coordinate_incomplete`. Because Section 14.1 requires complete page mapping for non-empty source text, `unavailable` is reserved for non-source structural records and is invalid on an Evidence Package evidence item. OCR use, minimum admitted OCR confidence, and parser-comparison status remain build uncertainty rather than source facts. A below-threshold comparison difference may ship only with `parser_comparison_difference`; a blocking disagreement produces no release and therefore no evidence lineage.

Runtime assembly records use the closed selection roles `retrieval_seed`, `expanded_context`, and `conflict_context`; several may appear when an item was selected in several ways. A direct result has its own `source_id` as a seed and an empty context-path array. An expanded item names every contributing seed and at least one accepted path. A conflict-attached item names every matching conflict/position and triggering source in its conflict reasons; it needs a context path only when graph traversal also reached it. Each path binds one originating seed to ordered steps; every step records the stable edge ID, canonical relation type and origin, traversal direction, source and target node IDs, ordered occurrence IDs when present, and the versioned context-rule ID. Exact duplicate `(seed source, edge-ID sequence)` paths are collapsed; independent paths and conflict reasons are retained in deterministic order. An unresolved or ambiguous relationship has no navigable edge or path: it remains a warning-bearing occurrence and can never explain inclusion of an absent target.

Every public evidence item must carry the strict Section 21 lineage object. The central serializer constructs it only from the checksum-verified active release and typed runtime decisions, rejects missing or unknown fields, and never accepts client-supplied lineage. Absolute paths, raw parser internals, configuration bodies, exception text, and secrets are excluded; hashes and safe producer identifiers are sufficient for reproducibility. Generated summaries, model scores, and future inferred metadata remain explicitly non-authoritative and cannot be cited as source provenance.

---

## 8. Package and distribution design

### 8.1 Distribution names

- PyPI distribution: `clausesift`
- Python import package: `clausesift`
- CLI command: `clausesift`
- Repository: `clause-sift`

### 8.2 Installation profiles

The package should use optional dependency groups so that the query runtime does not require heavy parsing and OCR dependencies.

Proposed usage:

```bash
pip install clausesift
pip install "clausesift[build]"
pip install "clausesift[ocr]"
pip install "clausesift[rerank]"
pip install "clausesift[all]"
```

Proposed semantic meaning:

- base: runtime, SQLite catalog, lexical search, exact vector search, CLI, and MCP;
- `build`: standard document parsing and release building;
- `ocr`: heavyweight OCR and difficult-document fallbacks;
- `rerank`: local cross-encoder models;
- `all`: all officially supported optional components.

### 8.3 Runtime/build dependency separation

The runtime package must not import parser or OCR modules during normal startup. Builder-specific code should be loaded only when build commands are invoked.

This prevents a simple MCP runtime from inheriting the memory footprint and installation complexity of the offline pipeline.

---

## 9. Proposed repository layout

```text
clause-sift/
├── docs/
│   ├── design.md
│   ├── canonical-model.md
│   ├── retrieval.md
│   ├── mcp-api.md
│   └── evaluation.md
├── src/
│   └── clausesift/
│       ├── __init__.py
│       ├── cli.py
│       ├── config/
│       ├── model/
│       ├── builder/
│       │   ├── parsers/
│       │   ├── normalisation/
│       │   ├── chunking/
│       │   ├── references/
│       │   ├── lexical/
│       │   ├── embeddings/
│       │   ├── vector/
│       │   ├── reports/
│       │   └── release/
│       ├── runtime/
│       │   ├── catalog/
│       │   ├── query/
│       │   ├── retrieval/
│       │   ├── reranking/
│       │   ├── context/
│       │   └── evidence/
│       ├── mcp/
│       └── evaluation/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── regression/
├── examples/
├── pyproject.toml
├── README.md
├── LICENSE
└── CHANGELOG.md
```

The first implementation may use fewer modules, but public boundaries between builder, runtime, evidence model, and MCP should be preserved.

---

## 10. Source corpus and manifests

### 10.1 Source files

Source documents are stored outside the Python package and are never included in the published wheel or source distribution.

A typical user workspace may contain:

```text
workspace/
├── corpus/
│   ├── inbox/
│   ├── originals/
│   └── manifests/
├── cache/
├── releases/
└── current
```

### 10.2 Copyright boundary

ClauseSift distributes software only. It must not bundle proprietary standards, manufacturer documents, or user corpora.

Users are responsible for possessing and using source documents lawfully.

### 10.3 Document manifest

Each document should have a human-reviewed manifest.

Example:

```yaml
manifest_schema_version: "1"
document_id: as-1668-1-2015
title: AS 1668.1:2015
document_code: AS 1668.1
edition: "2015"
authority: Standards Australia
document_type: mandatory_standard
release_tier: critical
jurisdictions:
  - Australia
disciplines:
  - hvac
  - smoke_control
  - fire_safety
status: active
effective_from: null
supersedes: null
superseded_by: null
reference_edition_overrides: {}
language: en
source_file: corpus/originals/AS1668.1-2015.pdf
sha256: "sha256:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
```

Registration computes a raw `manifest_bytes_hash` for provenance before decoding, then loads the YAML with a safe loader that rejects custom tags and validates it against a versioned schema with unknown fields rejected. It separately computes `manifest_content_hash` over the schema-normalized canonical representation. SHA-256 values use the canonical string form `sha256:` followed by exactly 64 lowercase hexadecimal characters; bare digests, uppercase characters, and surrounding whitespace are invalid. The non-zero value above is illustrative and registration must replace it with the digest calculated from the selected source bytes before human approval. `sha256` is mandatory and non-null for any manifest admitted to a build. Registration also records the selected source's positive byte size.

Every manifest value that becomes a public exact lookup key or filter—`document_code`, `edition`, and each jurisdiction and discipline—must contain 1-128 Unicode scalar values after its field-specific canonical normalization. Registration applies the same bound both before and after normalization and rejects rather than truncates, hashes, or aliases an over-limit value. Closed enums retain their narrower enumerated contracts. Source inspection also rejects a document whose page count is outside `1..2,147,483,647`, the public page-number domain, before page mapping or cache promotion.

The immutable approval binds the schema-normalized `manifest_content_hash` and selected source hash. Before ingestion, the builder safe-loads and canonicalizes the current manifest and requires exact equality with the approved content hash, then verifies the source hash and size. A semantic manifest or source change invalidates approval and affected caches. A raw-byte-only change—such as comments, whitespace, encoding, or key order that leaves canonical content unchanged—does not require human reapproval or invalidate semantic artifacts; the builder records the current `manifest_bytes_hash` and the change only in the external operator lifecycle ledger for forensic provenance. Raw manifest bytes and their hash are not release or runtime catalog authority.

`release_tier` is either `critical` or `standard`. A critical document is one whose omission or structurally incorrect parsing can invalidate a release; it is subject to the dual-parser and release-blocking rules in Section 11.3.

The initial closed document `status` enum is `active`, `superseded`, and `withdrawn`. Values are exact lowercase ASCII tokens: aliases, case folding, and unrecognized values are rejected at registration with `document_status_unknown`, rather than normalized into one of the enum members. Status is independent of `document_type` and effective-date metadata. `search_evidence.status` and `list_documents.status` use this same enum when non-null; `active` is the search default, while an explicit null removes the default status filter so superseded and withdrawn documents can remain available for historical work.

### 10.4 Initial document types

- `mandatory_standard`
- `referenced_standard`
- `code_or_regulation`
- `design_guideline`
- `technical_manual`
- `manufacturer_specification`
- `research_reference`
- `superseded_document`

Document type is part of evidence and affects how an AI client should describe the source.

---

## 11. Parser architecture

### 11.1 Parser router

No parser is assumed to be best for every document.

The parser router chooses a path according to document characteristics and user configuration.

Initial candidate paths:

- Docling for structured standards and ordinary technical PDFs;
- PyMuPDF-based extraction for deterministic page text and coordinate comparison;
- MinerU or another OCR pipeline for scanned or difficult documents;
- dual-parser comparison for critical documents.

No parser selection becomes permanent until it is measured against the project evaluation corpus.

Source documents and parser outputs are untrusted. Parser adapters must run in isolated subprocesses with no network access, a dedicated temporary directory, explicit CPU, memory, wall-time, file-size, and page-count limits, and read-only access only to the selected source file plus the pinned parser executable, runtime libraries, and declared local model assets required for that adapter. They receive no read access to the remaining corpus, workspace, credentials, or operator state. Failure to establish or verify any isolation control is a blocking `parser_failed`; the builder never falls back to an unisolated execution. The builder validates the adapter's parser-neutral output before importing it; a timeout, limit violation, crash, or malformed output fails that document rather than weakening isolation.

### 11.2 Parser contract

Every parser adapter must produce a parser-neutral intermediate representation containing, where available:

- pages and page dimensions;
- blocks and reading order;
- headings and hierarchy;
- paragraphs and lists;
- tables and cells;
- figures and captions;
- footnotes;
- source page numbers;
- bounding boxes;
- original extracted text;
- OCR status and confidence;
- parser warnings.

### 11.3 Parser validation

The builder must test:

- source and parsed page counts;
- missing-text ratios;
- abnormal-character ratios;
- heading-tree consistency;
- clause-number continuity;
- duplicated header/footer text;
- cross-page paragraph continuity;
- table shape consistency;
- unresolved page coordinates;
- differences between two parser outputs when comparison mode is enabled.

Comparison mode is mandatory for every `critical` document and optional for a `standard` document. The enabled state is part of the versioned, approved parser-routing configuration and cache identity; changing it requires review before rebuilding, so a failed standard comparison cannot be bypassed by silently disabling the mode. Whenever comparison mode is enabled, the document must be parsed independently by two configured adapters backed by distinct parser implementations; running one implementation twice or changing only its options does not satisfy this rule. Neither adapter's output becomes canonical until the comparison gate passes. Enabling comparison mode is therefore a gating build-policy choice, not an advisory shadow run.

For every comparison-mode document, any of the following is a blocking disagreement: either adapter fails; parsed page counts differ from the source or each other; a normative clause, exception, table, or page mapping appears in only one output; clause identities or ordering differ; a table's dimensions, headers, units, or cell values differ; or any versioned comparison metric exceeds the configuration selected for that document's release tier. Step 7 writes a durable parser-validation report before evaluating the blocking gate. The report identifies both adapters and includes both parser-neutral outputs when produced, an explicit sanitized failure record in place of any missing output, every single-parser result, every comparison metric, and every disagreement. The gate is not considered evaluated until that report is successfully finalized in the build's diagnostic-report area, which remains available after failure and is never itself canonical authority. A passing report is additionally promoted byte-for-byte into the content-addressed parser-validation cache and its hash becomes a canonical-model input; a failed report is retained only as a diagnostic and never enters canonical or downstream artifact caches. A passing comparison with any non-zero below-threshold difference records `parser_comparison_difference` in that promoted report so Section 7.2 can preserve the uncertainty on affected evidence. A blocked document may proceed only after correcting the parser, source, manifest, or comparison-mode routing configuration and rerunning the build; v0.1 has no waiver that selects one output while a blocking disagreement remains.

The versioned parser-routing configuration must name exactly one `canonical_primary` for every document. It additionally names exactly one ordered `independent_comparator` for every comparison-mode document, either directly or through a deterministic rule over manifested fields; a standard document outside comparison mode has only the primary route. Every selected adapter's identity, version, configuration, and assigned role is a build input. After the primary's single-parser gate and, when applicable, the comparator's single-parser gate and comparison gate pass, the builder selects the `canonical_primary` parser-neutral artifact byte-for-byte as the sole input to deterministic canonical-model construction; the comparator is validation-only. Below-threshold wording or OCR differences therefore resolve to the primary output, never to field-by-field merging, majority selection, or build-order choice. Changing an adapter or role invalidates the parse and all downstream cache entries and requires a complete rebuild and review. With unchanged source bytes, ordered roles, adapters, and configurations, both the selected parser artifact and resulting canonical model must be byte-identical across rebuilds.

A document that fails any applicable single-parser or comparison gate must not enter a production release; critical documents cannot disable comparison mode.

---

## 12. Canonical document model

The canonical document model isolates the rest of ClauseSift from parser-specific output formats. Its canonical nodes are the node set of the Evidence Graph; parser-native objects and retrieval chunks are not a parallel entity graph.

### 12.1 Core node fields

```text
node_id
document_id
node_type
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

A non-null `clause_number` declares that the node is independently addressable by exact clause lookup. It must contain the canonical normalized, non-empty identifier for that document; descendants that are not independently addressable keep it null rather than copying an ancestor's number for display. The catalog constraints in Section 14.1 make every non-null `(document_id, clause_number)` unique, so exact lookup cannot select between two canonical subtrees. Page bounds and bounding boxes are logical read-only projections of the authoritative ordered `node_page_spans` rows in Section 14.1, not independently writable node columns.

### 12.2 Initial node types

- `document`
- `part`
- `chapter`
- `section`
- `clause`
- `subclause`
- `paragraph`
- `requirement`
- `definition`
- `exception`
- `note`
- `table`
- `table_row`
- `figure`
- `caption`
- `appendix`
- `footnote`

### 12.3 Text variants

Each searchable unit may include:

- `original_text`: source-faithful text returned as evidence;
- `normalized_text`: repaired line breaks, hyphenation, and whitespace;
- `search_text`: normalized text plus deterministic document and hierarchy context;
- `embedding_text`: text formatted for the selected embedding model.

Search-enriched text must not replace original evidence text.

---

## 13. Standards-aware chunking

### 13.1 Chunk boundaries

Preferred boundaries are:

1. complete clause or subclause;
2. complete requirement plus its directly attached exception or note metadata;
3. complete table or logically independent table row;
4. semantically complete paragraph;
5. token-limit split as a last resort.

Fixed-size character chunking is not the primary strategy.

### 13.2 Chunk fields

```text
chunk_id
document_id
node_ids
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

`document_id` is the immutable identity of one manifested edition. `edition` remains the human-readable version label in the document record; chunks do not introduce a second `document_version` concept. The list above is logical: ordered `node_ids` are persisted through `chunk_nodes`. Clause number, heading path, node type, and page bounds are not independently writable scalar chunk fields. The builder derives `citation_node_id` as the deepest common ancestor of every member node in the validated canonical tree; release validation recomputes it. Heading path and node type project from that anchor, while page bounds and boxes project from the sole source row and intersecting page-span mappings.

For each retrievable member, the builder computes its nearest ancestor-or-self with a non-null `clause_number`, or null when none exists; every value in one chunk must be identical. A shared non-null node supplies the evidence `clause`, while an all-null chunk emits `clause: null`. A candidate mixing addressed and unaddressed content or spanning two independently addressable branches is split before persistence, so a scalar clause and generated citation are never ambiguous even when `citation_node_id` itself is a non-addressable paragraph or structural ancestor.

Every persisted chunk has non-empty source-faithful `original_text`. Chunk membership records the ordered, half-open UTF-8 byte span contributed by each member node; offsets must fall on code-point boundaries. Full-node membership uses the entire encoded `nodes.original_text`. The versioned chunk projection joins those spans with its declared source-faithful separator, while hierarchy and retrieval enrichment appear only in `search_text` or `embedding_text`.

`chunk_kind` is a closed, versioned enum covering every representation emitted by the chunker, and the chunker configuration assigns every kind a unique rank. The builder deduplicates the exact representation key `(chunk_kind, ordered (node_id, node_text_start, node_text_end) memberships)`, sorts each document's remaining chunks by `(first member node canonical order, first member byte start, chunk-kind rank, last member node canonical order, last member byte end, SHA-256 of the ordered membership tuples, chunk_id)`, and persists a dense zero-based `canonical_order`. The final `chunk_id` tie-breaker is itself deterministically derived from the unchanged chunk inputs. Release validation recomputes the representation keys and ordering and rejects a duplicate representation, gap, duplicate position, unknown kind, or mismatch; runtimes order evidence by persisted `canonical_order` ascending.

### 13.3 Context integrity

The chunker must preserve or link:

- scope conditions inherited from parent clauses;
- exceptions;
- notes and their informative status;
- table titles, headers, and units;
- normative versus informative appendices;
- source pages and bounding boxes;
- previous and next logical units.

### 13.4 Tables

Tables should create at least two searchable representations:

1. a whole-table representation;
2. row-level representations that repeat table title, headers, units, and parent clause context.

Table extraction confidence should be carried into evidence warnings.

---

## 14. Catalog and storage

### 14.1 SQLite as the authoritative catalog

SQLite should store:

- document manifests;
- versions and status;
- canonical nodes;
- chunks and text variants;
- page and bounding-box mappings;
- cross-references;
- classified conflict records and exact position spans;
- build metadata;
- parser warnings;
- release-admission metadata known at the catalog gate.

SQLite is the authoritative persisted representation of the compiled Evidence Graph and other structured knowledge-base metadata. This authority is about the deterministic compiled representation; original documents and human-reviewed manifests retain the evidence authority defined in Section 5.2.

The current run's evaluation results are not written back into `knowledge.sqlite`: the candidate catalog is fully materialized and becomes byte-stable at step 13, before evaluation runs. Step 18 writes the authoritative, versioned `evaluation-results.json`; the static report and release manifest refer to that artifact by hash and carry only its derived summary. Post-gate evaluation, candidate-validation, activation, and rollback records likewise live outside the immutable catalog. No later build step reopens `knowledge.sqlite` for mutation.

Every builder, validator, CLI, and MCP runtime SQLite connection executes `PRAGMA foreign_keys = ON` immediately after open and before starting a transaction, preparing a statement, creating schema, or reading/writing catalog data; the connection factory reads back `PRAGMA foreign_keys` and aborts unless it is `1`. Read-only runtime connections additionally enable and verify `PRAGMA query_only = ON`. Connection pooling may expose only connections initialized by this factory, and application queries cannot change either pragma. After the candidate catalog is fully materialized at step 13, the builder runs `PRAGMA foreign_key_check` and requires zero result rows before any derived builder runs; a disabled pragma or reported violation is a blocking `release_validation_failed`. The read-only runtime repeats `foreign_key_check` after opening the checksum-verified database and before starting the MCP session or serving a CLI/Python query; a disabled pragma or violation there follows the existing `release_integrity_failed` startup route. Neither condition is advisory.

Primary keys, foreign keys, `NOT NULL` constraints, and uniqueness constraints must encode the canonical invariants rather than relying only on application code. The initial schema requires at least:

`node_id`, `chunk_id`, `source_id`, `cross_reference_id`, `conflict_id`, and `conflict_position_id` are globally unique within a catalog release and remain stable across deterministic rebuilds of unchanged inputs. Every persisted public catalog identifier—`document_id`, `node_id`, `chunk_id`, `source_id`, `cross_reference_id`, `conflict_id`, and `conflict_position_id`—uses the same ASCII grammar as opaque tool identifiers: length 1-128 and pattern `^[a-z0-9][a-z0-9._:-]{0,127}$`. Registration validates manifested document IDs; deterministic generators validate every derived ID; the schema carries equivalent length/character checks; and release validation independently rechecks all seven identifier columns so a cache import cannot bypass the rule. The apparently redundant unique pairs `(document_id, node_id)` and `(document_id, chunk_id)` are ownership candidate keys: dependent tables and self-relations reference those pairs so SQLite proves that an otherwise global node or chunk ID belongs to the accompanying document.

Public human-readable lookup and filter keys use a different shared constraint: `documents.document_code`, `documents.edition`, every non-null `nodes.clause_number`, `document_jurisdictions.jurisdiction`, and `document_disciplines.discipline` contain 1-128 Unicode scalar values in their field-specific canonical normalized form. Manifest registration enforces the manifest-owned values, parser/canonical-model validation enforces generated clause keys, SQLite carries equivalent non-empty and length checks, and the step 13 release gate independently rechecks every stored value, including values imported from caches. These keys are never truncated or forced into the opaque-ID ASCII grammar. The manifest, canonical-model, and catalog schema versions change when this key contract changes so an older cache entry cannot bypass it.

| Table | Required constraints |
| --- | --- |
| `documents` | `document_id` primary key; 1-128-scalar canonical `document_code` and `edition`, `document_type`, `release_tier`, `status`, normalized relative `source_file`, positive `source_file_size`, `manifest_content_hash`, `source_file_hash`, and `source_page_count` in `1..2,147,483,647` `NOT NULL`; unique `(document_code, edition)`; checks reject an absolute/empty source locator and `.` or `..` segments, and enforce the Section 10.4 document-type enum, `release_tier IN ('critical', 'standard')`, and `status IN ('active', 'superseded', 'withdrawn')`. The runtime resolves the locator beneath the configured originals root and applies the containment and link checks in Section 22.1. |
| `nodes` | Globally unique `node_id` primary key; `document_id`, `node_type`, `original_text`, and canonical order `NOT NULL`; `document_id` foreign key to `documents`; unique ownership key `(document_id, node_id)` and unique `(document_id, canonical_order)`. `clause_number` is either null or a 1-128-scalar canonical normalized exact-lookup key, with a unique partial key `(document_id, clause_number) WHERE clause_number IS NOT NULL`. `parent_node_id`, `previous_node_id`, and `next_node_id` are nullable only for the sole document root or sequence boundaries, may not equal `node_id`, and each non-null relation uses composite foreign key `(document_id, related_node_id)` to `nodes(document_id, node_id)` with `ON DELETE RESTRICT`. |
| `chunks` | Globally unique `chunk_id` primary key; `document_id`, `citation_node_id`, closed-enum `chunk_kind`, dense zero-based `canonical_order`, non-empty `original_text`, `search_text`, and `embedding_text` `NOT NULL`; `document_id` foreign key to `documents`; unique ownership key `(document_id, chunk_id)`, unique `(document_id, canonical_order)`, and composite foreign key `(document_id, citation_node_id)` to `nodes(document_id, node_id)`. Validation requires the citation node to equal the deepest common ancestor of all member nodes and the nearest addressable-ancestor-or-null value to be identical for every retrievable member. `parent_chunk_id`, `previous_chunk_id`, and `next_chunk_id` are nullable only where the structural relation or sequence neighbor does not exist; each non-null relation uses composite foreign key `(document_id, related_chunk_id)` to `chunks(document_id, chunk_id)` with `ON DELETE RESTRICT`. |
| `chunk_nodes` | `document_id`, `chunk_id`, `node_id`, `member_order`, `node_text_start`, and `node_text_end` `NOT NULL`; composite primary key `(chunk_id, node_id)` and unique `(chunk_id, member_order)`; checks require zero-based `member_order`, `node_text_start >= 0`, and `node_text_end > node_text_start`; composite foreign keys `(document_id, chunk_id)` to `chunks(document_id, chunk_id)` and `(document_id, node_id)` to `nodes(document_id, node_id)` with `ON DELETE RESTRICT`. |
| `node_page_spans` | `document_id`, `node_id`, half-open UTF-8 byte `node_text_start`, `node_text_end`, `page_number`, and `mapping_order` `NOT NULL`; primary key `(node_id, node_text_start, node_text_end, page_number)` and unique `(node_id, mapping_order)`; composite foreign key `(document_id, node_id)` to `nodes(document_id, node_id)` with `ON DELETE RESTRICT`; checks require valid non-empty byte spans, non-negative mapping order, page numbers in `1..2,147,483,647`, and schema-valid optional bounding boxes. Release validation requires every non-empty node's rows, in dense `mapping_order`, to form an exact non-overlapping partition of `[0, byte_length(nodes.original_text))`; adjacent rows meet at one boundary, while any overlap, duplicate coverage, gap, or out-of-order interval blocks release. An empty-text structural node has no span row. |
| `document_jurisdictions` and `document_disciplines` | Both value columns are 1-128-scalar canonical normalized strings and `NOT NULL`; `document_id` foreign key to `documents`; composite primary key `(document_id, jurisdiction)` or `(document_id, discipline)`. |
| `sources` | Globally unique `source_id` primary key; `document_id`, `chunk_id`, and page span `NOT NULL`; `document_id` foreign key to `documents`; composite foreign key `(document_id, chunk_id)` to `chunks(document_id, chunk_id)` with `ON DELETE RESTRICT`; unique `(document_id, chunk_id)`; page span check enforces ordered endpoints in `1..2,147,483,647`. |
| `cross_references` | Globally unique `cross_reference_id` primary key; source node and document IDs, closed-enum relation type and relation origin, raw text, normalized parsed target fields, and resolution status `NOT NULL` where the reference grammar supplies them; composite foreign key `(source_document_id, source_node_id)` to `nodes(document_id, node_id)`. A `resolved` row requires both target IDs and composite foreign key `(target_document_id, target_node_id)` to `nodes(document_id, node_id)`; every unresolved row requires both target IDs to be null. Endpoint-type checks and relation-specific cycle rules follow Section 20. All ownership foreign keys use `ON DELETE RESTRICT`. Source and resolved-target document code, edition, and clause are read-only join projections rather than independently writable base columns. |
| `conflicts` | Globally unique `conflict_id` primary key; release state, comparison-key hash, detector/rule identity and version, configuration hash, decision origin, precedence status, decision-schema version, and decision-artifact hash `NOT NULL`; nullable explanation code, precedence-rule ID, and controlling position. State is only `confirmed`, `explained`, or `unresolved`—a `potential` row is release-invalid. Decision origin is `deterministic_rule` or `human_reviewed`; precedence is `not_applicable`, `encoded`, or `undetermined`. `encoded` requires a non-null controlling position and approved precedence-rule ID; other precedence states require both null. A deferred composite foreign key `(conflict_id, controlling_position_id)` references `conflict_positions(conflict_id, conflict_position_id)` when non-null. |
| `conflict_dimensions` | `conflict_id` and closed-enum dimension `NOT NULL`; composite primary key `(conflict_id, dimension)` and foreign key to `conflicts` with `ON DELETE RESTRICT`. Every conflict must have at least one row. |
| `conflict_positions` | Globally unique `conflict_position_id` primary key; `conflict_id`, dense zero-based `position_order`, strict canonical comparison projection, and projection SHA-256 `NOT NULL`; unique `(conflict_id, conflict_position_id)` and `(conflict_id, position_order)`; foreign key to `conflicts` with `ON DELETE RESTRICT`. The projection schema is selected by the dimension/rule and contains no generated summary. Every conflict must have at least two positions. |
| `conflict_position_spans` | `conflict_id`, `conflict_position_id`, dense zero-based `span_order`, `document_id`, `node_id`, and non-empty half-open UTF-8 `node_text_start`/`node_text_end` `NOT NULL`; primary key `(conflict_position_id, span_order)`; unique exact span per position; composite foreign keys `(conflict_id, conflict_position_id)` to `conflict_positions` and `(document_id, node_id)` to `nodes` with `ON DELETE RESTRICT`. Every position must have at least one span. |

Release validation rebuilds every conflict candidate ID and comparison projection from source spans, manifests, required context, typed relations, detector/rule configuration, and review input; reruns every deterministic explanation/confirmation rule; and requires exact equality with the stored state, dimensions, explanation, precedence, positions, projections, and ordering. It proves two or more dense positions, one or more dense valid spans per position, UTF-8 boundaries and ownership, complete deterministic source coverage for every position, and an exact review candidate/hash match. A stale review, `potential` state, one-sided record, duplicate position/span, missing source cover, controlling position outside the record, model-only confirmation, or stored-versus-recomputed difference is `release_validation_failed`. It additionally computes each conflict's touched release tiers: an `unresolved` record touching any `critical` document is blocking; a complete `confirmed`, `explained`, or standard-only `unresolved` record follows Section 20.3.

Before any subtree or context query runs, release validation proves that every document's node parent relation is one rooted tree. Each document has exactly one null-parent node of type `document`; every other node has exactly one parent in that document whose canonical order is lower than the child's. A recursive traversal seeded at that root must visit every document node exactly once, and explicit path tracking must report a self-edge, repeated node, disconnected component, or parent cycle. The same gate requires previous/next node links to be reciprocal and to name the immediate canonical-order neighbor or null at the corresponding boundary. A violation blocks index assembly and activation, so runtime traversal never relies on a recursion-depth limit to contain malformed structure. Chunk parent edges must likewise point to a lower chunk `canonical_order`; chunk previous/next links must be reciprocal immediate-order neighbors, which makes the optional chunk hierarchy acyclic and its sequence deterministic.

Release validation enforces a total one-to-one mapping between chunks and sources: every chunk admitted to the release has exactly one source row, and every source row names that chunk's document. The unique key rejects duplicate mappings and the ownership foreign key rejects orphan or cross-document sources; an anti-join for chunks without a source is a blocking catalog invariant before index assembly or activation. The runtime opens only a catalog that passed this check.

Release validation reconstructs each chunk's `original_text` by sorting its `chunk_nodes` rows by the gap-free `member_order`, checking that every half-open byte span is within the referenced non-null `nodes.original_text` and starts and ends on UTF-8 code-point boundaries, extracting those spans, and joining them with the versioned projection separator. Null or empty chunk text, an invalid membership span, missing or duplicate order positions, and any byte mismatch between the reconstruction and stored `chunks.original_text` block index assembly and activation.

Release validation also derives source provenance rather than trusting stored page numbers. It independently requires every document page count and stored or derived page number to lie in `1..2,147,483,647`, then recomputes each non-empty node's exact non-overlapping page-span partition before using it; every mapping page must also be within `1..documents.source_page_count`. For each chunk, the validator computes the minimum and maximum mappings intersecting its `chunk_nodes` member spans and requires its sole `sources` row to store exactly those page values. Evidence bounding boxes are projected only from those intersecting mappings, in page and mapping order, and must lie on pages within that derived span. A missing, overlapping, duplicate, gapped, or out-of-order mapping; an out-of-range page or box; or any stored-versus-derived source span mismatch blocks index assembly and activation.

Release validation also enforces exact-key determinism and byte-complete subtree coverage. Every non-null clause number must already be in canonical normalized form, and the partial unique key rejects two addressable nodes with the same `(document_id, clause_number)`. For this check, a retrievable node has non-empty source-faithful `original_text`, including any serialized table-cell text; an empty structural anchor is contextual rather than a retrievable chunk member and derives any displayed page context from covered descendants rather than owning a zero-length page-span row. For each addressable clause, its covering set is every distinct chunk that has at least one membership in that clause's retrievable subtree and whose every retrievable member belongs to that subtree; a chunk that also contains text from outside the requested subtree cannot satisfy or appear in exact lookup for that clause. The covering set must be non-empty. For every retrievable subtree node, the validator sorts and merges all member intervals contributed by that covering set and requires their union to equal exactly the full half-open UTF-8 byte interval `[0, byte_length(nodes.original_text))`; overlaps from whole-table and row representations are allowed, but a missing prefix, interior gap, or missing suffix blocks release. An addressable structural root whose own `original_text` is empty needs no zero-length direct membership; byte-complete descendant coverage satisfies the clause and supplies its contextual page range. An addressable subtree with no retrievable self or descendant content remains invalid. A recursive coverage query reports the clause, node, every uncovered byte interval, and every otherwise selected chunk with an out-of-subtree member; any duplicate normalized key, empty covering set, contentless addressable subtree, byte-incomplete retrievable descendant, or exact-lookup chunk leaking outside the subtree is a blocking catalog invariant before index assembly or activation. Together with chunk-to-source totality and chunk-text reconstruction, this guarantees that an existing clause resolves one subtree and can always produce the non-empty, complete, source-faithful `get_clause` result required by Section 22.

Jurisdictions, disciplines, chunk-node membership, and other multivalued query fields use normalized link tables, not delimiter-encoded strings.

All runtime SQL, including FTS5 predicates, must use bound parameters. A dedicated query compiler escapes or rejects FTS5 operators according to the selected search mode; raw client text is never accepted as an FTS expression. Identifiers from MCP or CLI input are catalog keys, never SQL fragments or path components.

### 14.2 Rebuildable indexes

Lexical and vector indexes are derived artifacts. They must be reconstructable from the canonical model and catalog.

The catalog must provide indexes for exact `(document_id, clause_number)` lookup; unique document code plus edition; `(status, document_type, document_id)` filtering; `(jurisdiction, document_id)` and `(discipline, document_id)` link-table filtering; source IDs; chunk-node membership in both directions; and cross-reference source and target keys. Query-plan regression tests must demonstrate index use for exact clause lookup and jurisdiction, discipline, status, and document-type filters. `chunks.jsonl`, when emitted, is a checksummed audit/export projection derived from SQLite; the runtime does not treat it as a second source of truth.

### 14.3 Original files

Original files remain in the user workspace. The catalog stores paths and hashes but does not replace the original source.

Runtime telemetry is not part of the immutable catalog. If enabled, it is written to a separately configured state directory outside the active release, with query text disabled by default as specified in Section 33.

---

## 15. Lexical retrieval

Lexical retrieval is mandatory because engineering queries frequently contain exact tokens that dense models can blur:

- document codes;
- clause identifiers;
- table numbers;
- product model numbers;
- numbers and units;
- abbreviations;
- exact phrases.

Candidate engines include:

- Tantivy bindings;
- BM25S;
- SQLite FTS5.

The initial implementation will select an engine after benchmarking:

- English and Chinese retrieval;
- punctuation and unit tokenisation;
- field weighting;
- index size;
- load time;
- reproducibility;
- Python packaging complexity.

The public retrieval interface must not depend on a specific lexical engine.

---

## 16. Dense retrieval

### 16.1 Offline chunk embeddings

ClauseSift v0.1 generates exactly one embedding for every persisted chunk during the build and stores those vectors in the release. Document-level vectors are outside the v0.1 artifact and retrieval contracts: no unused document rows are mixed into the chunk matrix, and a future document-level retrieval feature must introduce its own typed matrix, deterministic row mapping, cache identity, retrieval/fusion semantics, and evaluation gates before admission.

The chunk-vector row order is the total order `(document_id, chunks.canonical_order, chunk_id)` using the catalog's canonical string ordering and dense per-document chunk order. The release manifest records `embedding_scope: "chunk"`, `row_count`, `vector_dimensions`, `dtype`, `normalized`, and a versioned row-order identifier. Release validation requires a total one-to-one mapping between matrix rows and catalog chunks in that order; SQLite insertion order is never an input.

Changing the embedding model or revision invalidates the affected vector artifacts.

### 16.2 Runtime query embeddings

Only the current query is embedded at runtime.

The query model may be loaded lazily when semantic retrieval is first requested.

### 16.3 Exact search first

For small and medium local corpora, ClauseSift should prefer exact cosine or dot-product search over approximate nearest-neighbour search.

A normalized vector matrix may be memory-mapped and searched as:

```python
scores = embeddings @ query_vector
```

Approximate indexing should be introduced only when measured latency justifies it and recall loss has been quantified.

### 16.4 Candidate scale guidance

These are starting hypotheses, not hard limits:

- under approximately 50,000 chunks: NumPy memory-mapped exact search;
- approximately 50,000 to 300,000 chunks: NumPy or FAISS exact search;
- larger corpora or validated latency constraints: evaluate ANN indexes.

Actual thresholds must be determined on target hardware.

### 16.5 Embedding model selection

Embedding models must be benchmarked on the project corpus, including:

- English standards;
- Chinese standards;
- cross-language queries;
- HVAC and fire-safety terminology;
- identifiers and product models;
- numbers and units;
- synonyms;
- negation and exception queries.

No embedding model is considered permanent without evaluation evidence.

---

## 17. Query analysis and retrieval modes

### 17.1 Query analysis

Deterministic analysis should detect:

- document codes;
- clause numbers;
- editions;
- product model numbers;
- numbers and units;
- document types;
- jurisdiction and discipline filters;
- version-comparison intent;
- source-page requests.

### 17.2 Retrieval modes

#### Exact mode

For explicit document, clause, model, or numeric queries:

```text
metadata filtering
+ exact identifier lookup
+ lexical retrieval
```

No embedding or reranker is required unless exact retrieval is ambiguous.

#### Hybrid mode

For natural-language questions:

```text
lexical retrieval
+ dense retrieval
+ rank fusion
```

#### High-accuracy mode

For complex, cross-document, or applicability-sensitive questions:

```text
exact lookup
+ lexical retrieval
+ dense retrieval
+ fusion
+ cross-encoder reranking
+ context expansion
```

The public mode enum is `auto`, `exact`, `hybrid`, and `high_accuracy`. The runtime may select a mode automatically, but the API must allow an explicit mode override. `auto` selects only among capabilities present in both the installed runtime and the active release. If dense retrieval or reranking is unavailable, `auto` returns the best available result with a typed `retrieval_capability_unavailable` warning; an explicit unavailable mode fails with `feature_unavailable` rather than silently degrading.

Context correctness is independent of the candidate-selection accelerator. After seeds are selected, `exact`, `hybrid`, and `high_accuracy` all run the required-context closure in Section 19; an implementation cannot omit an applicability condition or exception merely because a faster mode was requested. `high_accuracy` additionally enables supporting context. Diagnostic context is returned only by an explicit diagnostic `get_context` request and never enters an ordinary answer silently. `auto` inherits the context profile of the concrete mode it resolves to, and the resolved mode is recorded in assembly lineage.

---

## 18. Candidate fusion and reranking

A starting high-accuracy pipeline is:

```text
exact identifier matches
lexical top 30-50
dense top 30-50
        ↓
deduplication and reciprocal-rank fusion
        ↓
cross-encoder reranking of top 20-30
        ↓
final evidence candidates: top 8-12
```

These numbers are initial parameters. They must be adjusted through Recall@K and end-to-end evaluation rather than latency preference alone.

The reranker may be loaded lazily. High-value engineering queries should retain the option to invoke it even when it increases latency. Lazy-load timeout and cold-versus-warm behavior are defined once in Section 27; Section 30 defines how those states are measured.

---

## 19. Context expansion

A relevant sentence is not necessarily sufficient evidence.

After retrieval, ClauseSift should inspect document structure and attach required context, including:

- parent scope clauses;
- definitions;
- exceptions;
- notes;
- referenced tables;
- linked clauses;
- normative appendices;
- immediate previous or next logical units for explicit diagnostic inspection.

Context expansion is structure-driven rather than a fixed previous/next chunk window. It is one deterministic traversal over the release-validated Evidence Graph, not arbitrary neighborhood expansion or LLM reasoning:

```text
ranked source/chunk candidates
    -> every ordered canonical member node becomes a seed
    -> apply versioned node/relation traversal rules
    -> close required context, then consider optional context
    -> materialize target nodes as source-backed evidence
    -> deduplicate and order the bounded evidence subgraph
    -> attach every accepted path, uncertainty, and warning
    -> serialize one Evidence Package
```

### 19.1 Context classes and profiles

Every rule has one context class:

1. **required** — omission can change scope, applicability, normative meaning, a value, or the subject of an exception;
2. **supporting** — useful corroboration or navigation that is not required to interpret the seed correctly;
3. **diagnostic** — adjacency, version history, or other inspection material that is useful for review but must not be mistaken for answer evidence.

Required closure runs for every ordinary evidence-returning search or exact-clause operation. Hybrid and exact search stop after required closure. High-accuracy search runs required and supporting rules. `get_context` accepts the closed `context_level` enum `required`, `supporting`, or `diagnostic`; each value includes all preceding levels and defaults to `supporting`. Its relation-class include flags may intentionally narrow this explicit inspection request, but they do not alter automatic required closure on the original search or clause result. Diagnostic context is never enabled merely by an installation option or latency heuristic.

Every admitted release records `context_rule_set_version`, a canonical configuration hash, node/relation vocabulary versions, the relation-type rank, and the limits below. Changing any value changes `build_content_id` and `release_id`. The rule set is executable configuration owned by ClauseSift and validated against the evaluation corpus; callers cannot upload rules or a graph query. A model may rank the already retrieved candidates, but it cannot add a traversal edge, change a context class, or decide that required context is unnecessary.

### 19.2 Initial traversal rules

The v0.1 rule set is closed. “Forward” and “reverse” use the canonical directions in Section 20, never query-relative naming.

| Seed or accepted node | Edge and direction | Class | Target and stop semantics |
| --- | --- | --- | --- |
| `requirement`, `clause`, `subclause`, `paragraph`, or `table_row` | `applies_subject_to` forward | required | Include every uniquely resolved condition. Apply required rules recursively to the target. |
| Same families | `depends_on` forward | required | Include every uniquely resolved definition, requirement, clause, table, or document dependency. Apply required rules recursively. A definition required by actual term use must be compiled as this edge; runtime reverse-scanning of all `defines` scopes is forbidden. |
| `requirement`, `clause`, `subclause`, `paragraph`, or `table_row` | `exception_to` reverse | required | Include every exception that explicitly limits the node. Apply the exception rule below; sibling position alone never creates an exception. |
| `exception` | `exception_to` forward | required | Include the exact affected source-bearing node and stop this rule after that target; cycles are release-invalid. |
| `definition` | `defines` forward | required | Include the exact governing scope so the definition is not presented as globally applicable. Stop this rule after that target. |
| `table_row` | `contains` reverse | required | Include the containing table and nearest addressable clause. The table projection must preserve title, headers, and units. Stop at that clause; do not attach unrelated rows. |
| `note` or `footnote` | `contains` reverse | required | Include the nearest source-bearing parent that the informative material qualifies. Preserve the note/footnote's informative status; attachment never makes it normative. |
| Any source-bearing seed or required node | `references` forward | supporting | Include each uniquely resolved direct target once. Do not recursively follow another `references` edge in an ordinary profile. Use `depends_on` when the target is required to complete meaning. |
| Any source-bearing seed or required node | `contains` reverse | supporting | Include non-empty structural ancestors through the nearest addressable clause and retain the complete heading path as metadata. Applicability text needed for correctness must also have `applies_subject_to`; hierarchy alone is not enough. |
| Any source-bearing seed or required node | directly contained `note`, `footnote`, or table reached by `contains` forward | supporting | Include only direct children whose type matches the rule. Exceptions require `exception_to`; a child relation alone cannot classify them as applicable. |
| Document root, or the exact document root projected from a seed with version-comparison intent | `supersedes` or `amends` forward from the newer/amending source or reverse from the exact older/amended target | supporting with version-comparison intent; otherwise diagnostic | Include only the exact resolved edition/document metadata target and stop. Never replace the seed or copy a same-number clause from another edition. |
| Any node | `precedes` forward or validated inverse | diagnostic | At most one immediate neighbor in each requested direction; adjacency never supplies required scope or an exception. |
| A definition-scope seed with no compiled term dependency | `defines` reverse | diagnostic | Show scoped definitions for inspection only. Ordinary search cannot infer that every definition in scope is required. |

A normative appendix follows the same typed rules as any other scope: a `depends_on` or `applies_subject_to` edge can make it required, a direct `references` edge makes it supporting, and containment or physical adjacency alone does not. An informative appendix, note, or footnote retains its source status in every attached item and citation.

Only release-validated structural edges and resolved semantic edges are navigable. A non-resolved occurrence is never followed or matched by document code, edition label, clause number, text similarity, or “latest” status. If that occurrence belongs to a rule that would be required, the result remains source-faithful but marks `context_completeness: "incomplete_required"` and emits `context_incomplete` plus `cross_reference_unresolved`; a critical document would already have failed release admission. A non-resolved optional occurrence emits `cross_reference_unresolved` only when its relation class was requested. A table-row seed whose validated structure cannot supply its table title, headers, units, and affected clause similarly remains visible but is `incomplete_required` and propagates `table_structure_anomaly`; no header or unit is inferred. v0.1 has no probabilistic navigable relation. Parser/OCR uncertainty on the nodes or occurrences used by a validated edge propagates through Section 7.2 warnings; a future low-confidence edge type requires a versioned policy and is non-navigable until then.

### 19.3 Traversal algorithm, materialization, and bounds

The runtime creates one seed record for every member node of every directly returned source chunk, preserving final candidate rank, source ID, and `chunk_nodes.member_order`. It processes a priority queue in this total order:

```text
(context-class rank,
 seed final rank,
 seed source_id,
 path length,
 ordered relation-type ranks,
 target document_id,
 target node canonical_order,
 ordered edge IDs)
```

Required candidates are therefore exhausted before supporting or diagnostic candidates. Path-local edge/node tracking prevents recursion; the global visited key `(seed_source_id, target_document_id, target_node_id, rule_id, direction, context_class)` prevents repeated expansion while still allowing independent paths to the same target. Encountering an allowed `references` or `depends_on` cycle records the finite path up to the first repeated node, does not enqueue that step, and emits one deterministically keyed `context_cycle_detected` warning. A structural, governing, amendment, or supersession cycle never reaches runtime because release validation rejects it.

“Required closure” is the least fixed point of required typed traversal and Section 20.3 material-conflict closure. After the required graph queue drains, conflicts sort by `conflict_id`; positions sort by `position_order`; their uncovered sources sort by the ordinary materialization key. Each new conflict source enters the required graph queue with a deterministic key after the source that triggered it. The runtime repeats until neither phase adds a source or record, deduplicating by release-scoped source/conflict ID. Only then may supporting traversal begin. Conflict records are not graph edges and do not consume semantic path depth, but their added sources, reasons, positions, and bytes consume the explicit bounds below. This fixed point ensures that a conflict side cannot arrive without its own applicability/exception context and that a newly attached side cannot hide another admitted material conflict.

An accepted target is materialized as source-backed Evidence Package items rather than generated text. The versioned rule declares its evidence scope: semantic references to an addressable clause/subclause use the byte-complete retrievable subtree defined in Section 14.1; atomic requirements, definitions, exceptions, notes, footnotes, and rows use their exact node interval; table context uses its validated whole-table representation; structural ancestors use only their own non-empty source interval; and a document root used for version context contributes safe document metadata and a path but never expands the whole document. If the required bytes are already covered by a selected source, no duplicate item is added and the new inclusion path is attached to that item. Otherwise, at the first uncovered byte, the runtime considers memberships satisfying `node_text_start <= uncovered < node_text_end`, selects the one with greatest `node_text_end`, breaks ties by `(chunk-kind rank, chunk canonical_order, chunk_id)`, and repeats until the declared scope is covered. A structural node with no source text contributes its typed path and metadata but no invented evidence item. Release validation executes this algorithm for every node eligible under a required rule and blocks a release with an incomplete cover; table-kind ranking prefers the whole-table representation needed to preserve headers and units. Sources selected for several seeds or paths appear once, retain every unique lineage path, and use the smallest queue tuple as their output-order key. Direct seeds precede expanded items; expanded items then sort by that retained key and finally `source_id`.

The schema-validated v0.1 defaults are:

| Bound | Default and enforcement |
| --- | --- |
| Structural path depth | 64 edges. Release validation rejects any tree or required materialization path that would exceed it. |
| Required semantic path depth | 8 edges per seed. Exceeding it is `context_limit_exceeded`; required evidence is never truncated. |
| Optional semantic path depth | 1 for supporting and 2 for diagnostic traversal. A second ordinary `references` hop is diagnostic only. |
| Expanded evidence items | 128 unique source items per request, in addition to direct seeds. |
| Paths per evidence item | 32 unique paths. |
| Total accepted path steps | 1,024 per request. |
| Material conflict records | 64 per request, with at most 16 positions per record and 256 positions total. |
| Conflict position spans and inclusion reasons | 1,024 of each per request. |

The complete output must also satisfy the Section 22 frame-size bound. Before traversal, release validation proves that the largest single required graph-and-conflict closure addressable by `get_clause` fits every depth/item/path/step/conflict/position/reason/byte bound. At runtime, if required closure from several search seeds would exceed any bound, the server returns `context_limit_exceeded` as one tool error and publishes no partial Evidence Package. Optional traversal stops immediately before the first over-limit candidate in priority order, keeps the complete required closure, sets `context_completeness: "truncated_optional"`, and emits `context_truncated` with safe configured/observed counts. Thus resource pressure can remove optional context visibly but can never silently remove required or material conflict context.

Every source and target remains bound to its exact `document_id`, edition, and status. Traversal never joins on a human clause label. An explicit cross-document edge may attach a superseded or withdrawn target, but the item preserves that status and emits `context_status_boundary` unless the query has explicit version-comparison intent. A candidate already from a non-active document likewise remains visible with that warning; the runtime never substitutes an active edition. Multiple seeds whose closures overlap deduplicate only the identical release-scoped source ID, not similar text or clause numbers.

### 19.4 Worked traversal examples

**Scope and exception.** A retrieved requirement `R` has `R --applies_subject_to--> S`, while exception `E --exception_to--> R`. Required closure returns `R` as `retrieval_seed`, then `S` and `E` as `expanded_context`. Their lineage paths record the forward applicability step and reverse exception step respectively. An unresolved `applies_subject_to` occurrence produces no guessed `S`; the package is explicitly `incomplete_required`.

**Table row.** A row node `TR` is retrieved. Reverse `contains` reaches its table `T` and nearest addressable clause `C`. The deterministic context cover selects the whole-table representation containing the title, header cells, units, and row, and attaches `C` when it has source text. Other table rows are not individually expanded merely because they are siblings. The row remains the direct seed and table/clause sources retain required traversal paths.

**Cross-reference.** Requirement `A` is incomplete without clause `B`, so the builder emits `A --depends_on--> B`, not an ordinary citation. Required closure includes exact target `B` in its manifested edition and evaluates `B`'s required applicability/dependency rules up to the semantic-depth bound. A plain `A --references--> B` is supporting, follows one hop only in high-accuracy mode, and never follows `B --references--> C` unless an explicit diagnostic request enables the second hop. If another edition also has clause `B`, it is irrelevant unless the stored edge targets that exact document ID.

---

## 20. Evidence Graph relationship model

### 20.1 Canonical relationship contract

Evidence Graph relationships are either **structural** edges derived from the validated canonical document model or **semantic** edges whose meaning is source-grounded and relation-specific. Each canonical name has one direction and one meaning across parsers, storage adapters, traversal code, reports, and public evidence. Storage may use foreign keys, relation rows, or derived views; those representations must expose the same logical edges.

The canonical structural relations are:

| Relation | Canonical direction and cardinality | Origin, traversal, and cycle policy |
| --- | --- | --- |
| `contains` | Immediate parent node → immediate child node. Every non-root canonical node has exactly one incoming `contains`; a parent may have zero or more ordered children. | Derived from `child.parent_node_id`. Ancestor and child traversal is eligible when a tool requests that context. The relation must form the one rooted tree validated in Section 14.1. |
| `precedes` | Canonical node → its immediate next canonical node in the same document. A node has at most one incoming and one outgoing edge; `previous_node_id` is the validated inverse lookup, not a second relation type. | Derived from reciprocal previous/next fields and canonical order. Optional bounded adjacency traversal may use it. Edges always increase canonical order, so cycles are invalid. |

Chunk parent/sequence links and chunk-to-node membership remain retrieval/projection structure rather than additional canonical Evidence Graph node relations. Notes, exceptions, tables, and appendices obtain their ordinary attachment from `contains`; a semantic edge is added only when its distinct meaning changes validation or traversal behavior.

The initial semantic relations are deliberately limited to the existing vocabulary:

| Relation | Canonical source → target | Cross-document and resolution rule | Origin, context eligibility, and cycle policy |
| --- | --- | --- | --- |
| `references` | Any source-bearing node → an addressable node or document root explicitly cited by the source. | Allowed. A navigable edge exists only after unique resolution. An absent or ambiguous target remains an unresolved occurrence with no edge. | `source_text`; eligible only for requested direct-reference context. Cycles are allowed because source documents may cite each other, but traversal is bounded and uses a visited set. |
| `depends_on` | A requirement, clause, subclause, or table row → the requirement, clause, subclause, definition, table, or document on which its interpretation or satisfaction explicitly depends. | Allowed only for an explicit, uniquely resolved dependency. | `source_text` or `manifest`; eligible for dependency/applicability context. Source-grounded cycles may be retained with a warning, but never authorize recursive unbounded traversal. |
| `exception_to` | An `exception` node → the requirement, clause, subclause, or table row whose effect it limits. | Same-document by default; cross-document only when an explicit citation resolves uniquely. | `source_text`; runtime finds exceptions from the target by reverse traversal when requested. Self-edges and `exception_to` cycles are invalid. |
| `defines` | A `definition` node → the document, part, chapter, section, clause, subclause, or appendix scope whose terminology it governs. | Same-document by default; an external definition uses `references` or `depends_on` unless the source explicitly declares cross-document scope and resolves uniquely. | `source_text`; eligible by reverse lookup from a seed within the governed scope. Self-edges and `defines` cycles are invalid. |
| `supersedes` | A newer document root → each older document root it replaces. | Cross-document by definition. Both editions remain distinct release nodes; an unavailable or ambiguous older edition creates no navigable edge. | Human-reviewed `manifest` authority. Extracted text is only a proposed occurrence until reconciled. Not default answer context; eligible for explicit version work. Self-edges and cycles are invalid. |
| `amends` | An amending document root or explicit amendment clause → the document root or addressable node it changes. | Cross-document allowed and requires unique target resolution. | Human-reviewed `manifest` authority or reconciled `source_text`; eligible for explicit version work. Self-edges and cycles in the amendment/supersession subgraph are invalid. |
| `applies_subject_to` | A governed requirement, clause, subclause, or table row → the condition, exception, clause, requirement, or table that qualifies its applicability. | Cross-document only for an explicit, uniquely resolved condition. | `source_text` or `manifest`; eligible for applicability context. Self-edges and same-relation cycles are invalid. |

For example, direction never changes with the query:

```text
exception node --exception_to--> affected requirement
governed requirement --applies_subject_to--> applicability condition
citing clause --references--> cited clause
new document root --supersedes--> old document root
```

`relation_origin` is the closed v0.1 enum `structural`, `source_text`, or `manifest`. Structural relations are derived rather than stored as cross-reference occurrences. v0.1 admits no generated/probabilistic semantic edge. A future generated candidate requires a schema/vocabulary version change, explicit generator identity and confidence, review policy, and a non-authoritative state; it cannot become navigable merely because a model emitted it.

Every source occurrence is retained with its own stable occurrence ID and source evidence. For resolved semantic relations, the logical edge identity is `(source_document_id, source_node_id, relation_type, target_document_id, target_node_id)`. Repeated citations with that identity normalize to one runtime edge whose ordered provenance list contains every occurrence; evidence is never discarded. If source text explicitly enumerates several targets, the builder emits one occurrence and edge per explicit target. A phrase with several candidate interpretations is `ambiguous_edition` or otherwise unresolved, not a multi-target guess.

Release validation enforces the endpoint matrix, origin policy, target ownership, semantic identity, and cycle rules above. A semantic self-edge is rejected except where `references` or `depends_on` faithfully records an explicit source statement; those allowed cycles remain bounded at traversal. Structural hierarchy cycles always block release. Relation vocabulary additions require a schema and vocabulary version change; unknown relation names fail visibly rather than being mapped to the nearest known type.

Section 19 is the sole authority for automatic traversal class, direction, recursion, and materialization. Relation type constrains meaning but does not by itself authorize arbitrary expansion: in particular, ordinary `references` is supporting, semantic incompleteness is represented by `depends_on`, an applicable exception is found by reverse `exception_to`, and `supersedes`/`amends` require deterministic version intent for supporting traversal. The release validator executes that exact rule set against these canonical directions.

### 20.2 Cross-reference extraction and resolution

The build pipeline should detect deterministic references such as:

- `refer to Clause 4.2`;
- `subject to Section 5`;
- `except as permitted by Table 3.1`;
- `in accordance with AS/NZS 1668.2`.

Persisted fields:

```text
cross_reference_id
source_node_id
source_document_id
parsed_target_document_code
parsed_target_edition
parsed_target_clause
target_document_id
target_node_id
relation_type
relation_origin
resolution_status
raw_reference_text
```

The parsed target fields are null only when the reference grammar omits that component and otherwise contain its canonical normalized value. `source_edition` and the `target_document_code`, `target_edition`, and `target_clause` values exposed to reports or runtime clients are derived by joining the stored source and target IDs to `documents` and `nodes`; callers and builders cannot write those projections independently.

The base row stores `source_document_id` and `source_node_id`, with ownership enforced by their composite foreign key. A resolved reference stores only the release-scoped `target_document_id` and `target_node_id`; document code, edition, and clause projections alone are not stable join keys. Resolution is deterministic:

1. a same-document reference uses the source `document_id`;
2. an external reference naming a document code and edition requires exactly one catalogue match for that pair;
3. an unqualified external document code uses the source manifest's human-reviewed `reference_edition_overrides` mapping when present, and the mapped `document_id` must exist in the release and match that code;
4. without an override, an unqualified external code resolves only when exactly one release document has that code.

Multiple eligible documents produce `ambiguous_edition`; no eligible document produces `unresolved_document`; and an eligible document without the referenced clause produces `unresolved_clause`. None of these conditions may silently select the newest or active edition. The manifest schema defines `reference_edition_overrides` as a mapping from normalized external document code to an immutable target `document_id`; it is covered by manifest approval and release validation.

The initial `resolution_status` enum is `resolved`, `unresolved_document`, `ambiguous_edition`, and `unresolved_clause`. Same-document references inherit the source `document_id`. `resolved` requires both target IDs. When `parsed_target_clause` is present, the target must be the unique addressable node in the resolved document whose normalized `clause_number` equals it; when the grammar names only a document, the target node must be that document's sole root. Release validation reruns the deterministic four-step resolver from the immutable parsed fields, approved overrides, and candidate release catalog and requires the stored `resolution_status`, `target_document_id`, and `target_node_id` to equal its result exactly. For a `resolved` result only, every non-null parsed document code and edition must equal the selected joined document values. Every non-resolved result instead requires both target IDs and all joined target projections to be null; its non-null parsed fields remain normalized extraction evidence and are not compared with nonexistent joined values. An existing but different node, a writable code/edition projection, joined target data on an unresolved result, or target IDs attached to an unresolved result blocks index assembly and activation.

Release policy is tier-specific and has no count threshold in v0.1:

- for a `critical` document, every extracted cross-reference row must be `resolved`; any `unresolved_document`, `ambiguous_edition`, or `unresolved_clause` status emits a blocking `cross_reference_unresolved`, fails release validation, and requires a manifest correction, parser/resolver correction, or re-approved change of release tier before rebuilding;
- for a `standard` document, a non-resolved status emits an advisory `cross_reference_unresolved` and may ship only when the static review report enumerates it and the unresolved row exposes no navigable target IDs.

The release summary records unresolved counts by document, tier, status, and relation type. Runtime context expansion never follows an unresolved row.

Human-reviewed manifest fields are authoritative for `supersedes` and `superseded_by`. An extracted supersession statement is stored as a `source_text` occurrence and proposed metadata, but it does not overwrite or become equivalent to the `manifest` edge. Any disagreement emits `edition_conflict` and blocks a critical document until reviewed.

These records are typed semantic edges in the logical Evidence Graph. Structural edges may remain encoded by validated node/chunk foreign keys rather than duplicated into one generic edge table. The first release will use relational graph data, not a generic graph database.

### 20.3 Conflict detection and handling

A disagreement is itself evidence, but an apparent difference is not automatically a conflict. ClauseSift represents conflict assessment as a separate, versioned, n-ary record over exact source spans. It is not a symmetric `conflicts_with` graph edge: a conflict may have three or more positions, several dimensions, an explanation or precedence decision, and a lifecycle state. The record is derived release metadata, never a generated replacement for its source nodes.

The conflict lifecycle is:

| State | Meaning | Release behavior |
| --- | --- | --- |
| `potential` | A versioned deterministic detector, human submission, or future model-assisted detector identified comparable positions that may be incompatible, but context has not classified them. | Build-diagnostic state only. It must transition before catalog admission and can never appear in a runtime release. |
| `confirmed` | At least two source positions have incompatible compliance sets or normative effects under the same known subject and applicability context. Confirmation comes from an exact deterministic rule or immutable human review, never solely from a model score. | May ship when every position and decision is complete. It always remains visible when material and emits `evidence_conflict`; a genuine source conflict is not itself a corrupt build. |
| `explained` | A deterministic typed relation or trusted metadata proves why the positions are not jointly incompatible: for example unit equivalence, exception, amendment, supersession, disjoint applicability, or compatible modalities. | Retained for audit and false-positive evaluation. Ordinary answers omit it; explicit comparison or diagnostic requests may return it without a conflict warning. |
| `unresolved` | The known evidence is insufficient to prove either incompatibility or a valid explanation, including missing applicability or precedence facts. | A standard-tier record may ship with `conflict_unresolved`; a record touching a critical document blocks release pending corrected metadata, source/parser data, or immutable review. |

Each candidate has one stable ID derived from its versioned detector/rule, canonical comparison key, dimensions, and sorted exact position-span tuples. A source, manifest, normalized-value, detector, or context change therefore produces a new candidate ID; an old review cannot attach to changed evidence. Before catalog admission, the classifier computes required Section 19 context for every position and applies explanation rules before confirmation rules. It then converts every `potential` candidate to exactly one release state. Natural-language incompatibility that no exact rule proves is `unresolved` unless an immutable human conflict-review input confirms or explains it.

The closed initial dimensions are `edition_version`, `source_authority`, `jurisdiction`, `numeric_threshold`, `normative_statement`, `parser_extraction`, and `applicability`. A record may have several dimensions in canonical enum order. Its comparison projection is a strict, versioned, non-authoritative object containing only source-derived structured values needed to rerun the named rule—such as normalized subject key, modality, exact decimal/rational quantity and canonical unit, scope IDs, jurisdiction IDs, effective interval, product/equipment class, and source-span hash. Original text and Evidence Lineage remain the authority.

Conflict classification uses these rules in order:

1. **Extraction before source comparison.** Independent parser outputs for the same source region are not two source positions. Section 11.3 owns this `parser_extraction` disagreement: a blocking difference produces no canonical node or conflict record; an admitted below-threshold difference remains `parser_comparison_difference` in build lineage. The chosen primary parser never “wins” a blocking table value silently.
2. **Normalize only declared comparable values.** Numeric comparison uses exact decimal or rational conversion through the versioned unit registry, with any tolerance named in the rule configuration. Equal convertible quantities are `explained`. Modalities map to allowed-value sets: two stricter compatible minima or maxima are differences, not conflicts; an empty intersection under the same subject/applicability is a deterministic `confirmed` conflict.
3. **Apply typed explanations.** `exception_to`, `applies_subject_to`, `supersedes`, and `amends` are evaluated in their Section 20 directions. An exception qualifying its target, an amendment changing its base, a historical edition replaced by a newer edition, or positions with provably disjoint jurisdiction, effective interval, product/equipment class, or other manifested scope are `explained`, not conflicts.
4. **Do not invent applicability or precedence.** Similar clause labels, textual proximity, document type, authority name, stricter wording, active status, or ranking score cannot prove shared applicability or choose a controlling source. A mandatory minimum and a stricter compatible guideline may coexist; incompatible mandatory and manufacturer positions are `confirmed` only when shared applicability is known, and neither wins without a trusted rule.
5. **Resolve only through admitted decisions.** A deterministic rule may confirm numeric/set incompatibility or explain typed metadata. A schema-validated, content-addressed human review may confirm or explain normative wording and may name a controlling position only with an approved `precedence_rule_id`. A model may propose `potential` candidates for later review but cannot set `confirmed`, `explained`, a controlling position, or release-gate severity.

Every final state is bound to one immutable decision artifact. Its strict payload names the exact candidate ID, chosen state, explanation code or null, precedence status, optional controlling position, approved precedence-rule ID or null, decision origin, and decision-schema version; its content hash is stored separately as `decision_artifact_sha256`. A deterministic artifact also names the exact classifier rule and configuration that produced the decision. A human-reviewed artifact instead names the approved review-policy version and reviewer identity under the repository's review policy. Neither form contains generated summary text or rewrites a source claim. `precedence_status` is `not_applicable`, `encoded`, or `undetermined`; `controlling_position_id` is non-null exactly for `encoded` and must belong to that conflict. `authority`, `document_type`, or status metadata alone never implies `encoded` precedence. Changing a decision artifact, review policy, precedence rule, or rule configuration invalidates conflict analysis and every downstream artifact.

#### Build and runtime responsibilities

At build time ClauseSift generates deterministic numeric/structured candidates, imports exact human-reviewed candidates, attaches complete required context, classifies every candidate, materializes release records, and writes all potential-to-final transitions and detector false-positive explanations to the static report. A future replaceable semantic detector may add candidates only in `potential`. Release validation reruns deterministic comparison/explanation rules, verifies every span and review hash, and enforces the tier policy above.

At runtime, seed filtering and ranking happen first, but they cannot erase a material admitted conflict. After each required graph closure, the runtime finds every `confirmed` or `unresolved` conflict whose position intersects a selected source span, adds source-faithful coverage for every position as `conflict_context`, runs required Section 19 context for newly added positions, and repeats to a fixed point. Conflict context is required: the ordinary item/path/byte bounds apply, and an overflow returns `context_limit_exceeded` rather than a one-sided package. Metadata filters constrain retrieval seeds, not these exact conflict/context attachments; every attached item retains its actual edition, jurisdiction, document type, and status.

The response-level `conflicts` array is required and sorted by `conflict_id`. It contains each material record once with `state`, ordered `dimensions`, `explanation_code` or null, `precedence_status`, `controlling_position_id` or null, and every position in stable `position_order`. Each position contains its stable ID and the exact returned `source_ids`, `document_ids`, node IDs and byte spans that support it. It copies no detector-generated prose. Evidence added only for this closure carries `selection_roles: ["conflict_context"]` and a conflict inclusion reason naming the triggering source and position; an independently retrieved item may carry both roles. Confirmed records emit `evidence_conflict`; unresolved records emit `conflict_unresolved`. Explained records appear only for explicit version/comparison or diagnostic intent and cannot be presented as unexplained conflict.

Downstream clients must preserve every returned material position and warning. They may state an encoded precedence decision only with its rule ID and citations to all positions; otherwise they must describe the disagreement or uncertainty and cannot silently select the highest-ranked, newest, strictest, mandatory-looking, or model-preferred side. ClauseSift does not make legal, professional, or engineering-control judgments that are absent from approved deterministic metadata/rules.

#### Worked conflict examples

**Confirmed numeric conflict.** Two active mandatory requirements for the same manifested equipment class and jurisdiction require `x >= 50 L/s` and `x <= 40 L/s`. Exact unit normalization yields disjoint allowed sets, so the record is `confirmed`. A hit on either position forces both source-backed positions into the package; no winner is named unless an approved precedence rule does so.

**Valid exception.** Requirement `R` prohibits an action and exception `E --exception_to--> R` permits it under condition `C`. Required traversal returns `R`, `E`, and `C`; the candidate is `explained` by `exception`, not a confirmed contradiction. Retrieving `R` without the exception would instead be a context-completeness failure.

**Version/amendment difference.** A 2026 amendment changes a 2024 clause and has a validated `amends` edge; a newer edition has a manifested `supersedes` edge to the old edition. The differences are `explained` and remain edition-separated. An explicit historical/version query may return both records and the explanation; an ordinary current query never substitutes or blends clause numbers across editions.

**Jurisdiction/applicability difference.** One requirement applies only in jurisdiction A and another only in jurisdiction B, so trusted disjoint applicability makes the candidate `explained`. If one side lacks jurisdiction or equipment-class metadata, ClauseSift cannot assume overlap or disjointness: the candidate becomes `unresolved`, ships only under the standard-tier policy, and returns all known sides with `conflict_unresolved`.

---

## 21. Evidence package

ClauseSift returns structured evidence, not only prose. An Evidence Package is the serialized client-facing projection of one bounded runtime evidence subgraph; it does not transfer graph authority to the client or collapse distinct source nodes into a generated claim.

Example:

```json
{
  "query": "When may mechanical smoke exhaust be omitted?",
  "retrieval_mode": "high_accuracy",
  "release": "rel-sha256-0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
  "context_completeness": "complete",
  "evidence": [
    {
      "source_id": "src-001",
      "document_id": "as-1668-1-2015",
      "document_code": "AS 1668.1",
      "edition": "2015",
      "document_type": "mandatory_standard",
      "status": "active",
      "clause": "4.6.2",
      "heading_path": [
        "Smoke-control systems",
        "Fan operation"
      ],
      "node_type": "requirement",
      "content_trust": "untrusted_source",
      "page_start": 47,
      "page_end": 47,
      "original_text": "...",
      "citation": "[AS 1668.1:2015, cl. 4.6.2, p.47]",
      "bounding_boxes": [],
      "lineage": {
        "lineage_schema_version": "0.1.0",
        "source": {
          "manifest_content_hash": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
          "source_file_hash": "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
          "source_file_size": 4821936,
          "coordinate_status": "page_only",
          "spans": [
            {
              "node_id": "node-requirement-001",
              "node_text_start": 0,
              "node_text_end": 128,
              "page_spans": [
                {
                  "page_number": 47,
                  "node_text_start": 0,
                  "node_text_end": 128,
                  "bounding_boxes": []
                }
              ]
            }
          ]
        },
        "build": {
          "build_content_id": "build-sha256-cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
          "lineage_artifact_sha256": "sha256:dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",
          "catalog_artifact_sha256": "sha256:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
          "context_rule_set_version": "context.v1",
          "context_configuration_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000011",
          "chunk_id": "chunk-001",
          "canonical_node_ids": [
            "node-requirement-001"
          ],
          "transform_artifacts": [
            {
              "kind": "parser_neutral",
              "role": "canonical_primary",
              "producer_id": "docling",
              "producer_version": "2.4.0",
              "configuration_sha256": "sha256:1111111111111111111111111111111111111111111111111111111111111111",
              "artifact_sha256": "sha256:2222222222222222222222222222222222222222222222222222222222222222"
            },
            {
              "kind": "parser_validation_report",
              "role": "validation",
              "producer_id": "clausesift-parser-validator",
              "producer_version": "0.1.0",
              "configuration_sha256": "sha256:3333333333333333333333333333333333333333333333333333333333333333",
              "artifact_sha256": "sha256:4444444444444444444444444444444444444444444444444444444444444444"
            },
            {
              "kind": "canonical_model",
              "role": "transform",
              "producer_id": "clausesift-canonicalizer",
              "producer_version": "0.1.0",
              "configuration_sha256": "sha256:5555555555555555555555555555555555555555555555555555555555555555",
              "artifact_sha256": "sha256:6666666666666666666666666666666666666666666666666666666666666666"
            },
            {
              "kind": "page_provenance",
              "role": "transform",
              "producer_id": "clausesift-page-mapper",
              "producer_version": "0.1.0",
              "configuration_sha256": "sha256:7777777777777777777777777777777777777777777777777777777777777777",
              "artifact_sha256": "sha256:8888888888888888888888888888888888888888888888888888888888888888"
            },
            {
              "kind": "chunk_projection",
              "role": "transform",
              "producer_id": "clausesift-chunker",
              "producer_version": "0.1.0",
              "configuration_sha256": "sha256:9999999999999999999999999999999999999999999999999999999999999999",
              "artifact_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000001"
            },
            {
              "kind": "relationship_resolution",
              "role": "transform",
              "producer_id": "clausesift-relationship-resolver",
              "producer_version": "0.1.0",
              "configuration_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000005",
              "artifact_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000006"
            },
            {
              "kind": "conflict_analysis",
              "role": "transform",
              "producer_id": "clausesift-conflict-analyzer",
              "producer_version": "0.1.0",
              "configuration_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000012",
              "artifact_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000013"
            }
          ],
          "uncertainty": {
            "ocr_status": "not_used",
            "minimum_ocr_confidence": null,
            "parser_comparison_status": "not_required"
          }
        },
        "assembly": {
          "selection_roles": [
            "retrieval_seed"
          ],
          "seed_source_ids": [
            "src-001"
          ],
          "context_completeness": "complete",
          "retrievals": [
            {
              "channel": "lexical",
              "channel_version": "fts5.v1",
              "configuration_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000009",
              "artifact_set_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000002",
              "candidate_rank": 2,
              "score": 12.4
            },
            {
              "channel": "dense",
              "channel_version": "exact-cosine.v1",
              "configuration_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000010",
              "artifact_set_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000003",
              "candidate_rank": 4,
              "score": 0.78
            }
          ],
          "fusion": {
            "algorithm_id": "rrf.v1",
            "configuration_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000007",
            "rank": 1,
            "score": 0.0325
          },
          "rerank": {
            "model_id": "example-cross-encoder",
            "model_revision": "rev-1",
            "configuration_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000008",
            "artifact_set_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000004",
            "rank": 1,
            "score": 0.91
          },
          "context_paths": [],
          "conflict_reasons": []
        }
      },
      "warnings": [
        {
          "code": "source_coordinate_incomplete",
          "phase": "runtime",
          "severity": "advisory",
          "message": "Source page is known but bounding-box coverage is incomplete.",
          "source_id": "src-001",
          "details": {
            "lineage_stage": "source"
          }
        }
      ]
    }
  ],
  "conflicts": [],
  "warnings": [
    {
      "code": "applicability_incomplete",
      "phase": "runtime",
      "severity": "advisory",
      "message": "Applicability depends on building classification.",
      "source_id": "src-001",
      "details": {
        "lineage_stage": "assembly"
      }
    },
    {
      "code": "source_coordinate_incomplete",
      "phase": "runtime",
      "severity": "advisory",
      "message": "Source page is known but bounding-box coverage is incomplete.",
      "source_id": "src-001",
      "details": {
        "lineage_stage": "source"
      }
    }
  ]
}
```

The item above is a direct retrieval seed: both retrieval channels and the reranker are identified, its own source is the seed, and `context_paths` is empty. The result-level `context_completeness` is the deterministic worst state across every direct seed and optional traversal: `incomplete_required` takes precedence over `truncated_optional`, which takes precedence over `complete`; warnings preserve both conditions if they coexist. An expanded exception attached to that seed instead has this assembly lineage excerpt; its required source and build objects have the same complete shape as above:

```json
{
  "source_id": "src-exception-001",
  "lineage": {
    "assembly": {
      "selection_roles": [
        "expanded_context"
      ],
      "seed_source_ids": [
        "src-001"
      ],
      "context_completeness": "complete",
      "retrievals": [],
      "fusion": null,
      "rerank": null,
      "context_paths": [
        {
          "seed_source_id": "src-001",
          "context_class": "required",
          "steps": [
            {
              "edge_id": "edge-exception-001",
              "relation_type": "exception_to",
              "relation_origin": "source_text",
              "direction": "reverse",
              "from_node_id": "node-requirement-001",
              "to_node_id": "node-exception-001",
              "occurrence_ids": [
                "xref-exception-001"
              ],
              "context_rule_id": "context.exception.v1"
            }
          ]
        }
      ],
      "conflict_reasons": []
    }
  }
}
```

`lineage`, `source`, `build`, `uncertainty`, `assembly`, every artifact reference, retrieval record, path, path step, and conflict reason are closed objects with `additionalProperties: false`; all fields shown in the complete direct-item example are required, with only the explicitly nullable values allowed to be null. The enclosing item's `document_id` and `source_id` select the document/source lineage record and must match it exactly. Source spans are sorted by `(node member_order, node_text_start, node_text_end)`, and their page spans repeat the exact intersecting node-byte start/end in validated `mapping_order`; those intervals must form the same complete non-overlapping partition as the corresponding catalog mapping. The public `page_start`, `page_end`, and `bounding_boxes` fields are convenient projections only: the serializer recomputes them from `lineage.source.spans` and fails closed unless they match exactly. `canonical_node_ids` is the ordered membership projection for `chunk_id`; an ID not owned by the item's document or chunk is a release-integrity failure.

`transform_artifacts` follows the stage order in Section 7.2 and contains all selected parser-neutral routes before the validation report and selected canonical transformations, including relationship resolution and conflict analysis. `role` is a closed value appropriate to the artifact kind. `producer_id`, `producer_version`, configuration hash, and artifact hash must equal the verified `lineage.json` record. The context and conflict rule-set versions and configuration hashes must equal the active manifest and bind traversal, comparison, review, ordering, limits, and rule IDs. `parser_comparison_status` is `not_required`, `passed_exact`, or `passed_with_differences`; the last value requires an evidence-bound `parser_comparison_difference` warning. `ocr_status` is `not_used` or `used`; when used, `minimum_ocr_confidence` is the minimum confidence of the contributing spans and a below-policy value requires `ocr_low_confidence`.

`selection_roles` uses the closed canonical order `retrieval_seed`, `expanded_context`, `conflict_context`; `seed_source_ids` are non-empty, unique, and canonically sorted. `context_completeness` is the closed value `complete`, `incomplete_required`, or `truncated_optional` and agrees with the required Section 19 warnings. Retrieval records use the closed channels `exact`, `lexical`, and `dense`, are ordered by the versioned channel rank, and identify the exact checksummed release artifact set that produced the candidate; an item that is only context has an empty array, while a retrieval seed has at least one record. `candidate_rank` is one-based, and `score` is a finite number or null only for an exact lookup with no numeric scorer. An artifact-set hash is the SHA-256 of the versioned canonical ordered `(relative_path, byte_size, sha256)` tuples for its manifest-admitted files, so a multi-file index or model is named without exposing paths in the public object. `fusion` and `rerank` identify their versioned algorithm/model inputs and decision rank/score and are null when that stage did not run. Every context-path object binds one `seed_source_id` and `context_class` to a non-empty ordered `steps` array. Paths are unique by `(seed_source_id, context_class, ordered edge-ID sequence)` and sort by the Section 19 queue order. Every item carrying `expanded_context` has at least one path, and every step must match one release-validated structural or semantic edge. `conflict_reasons` is empty unless the item carries `conflict_context`; each reason is `{conflict_id, conflict_position_id, triggering_source_ids}` and must match one returned conflict position and its canonical triggering sources. An item reached several ways retains every role, path, and reason.

`conflicts` is a required array on every evidence-bearing success and is empty when no material record applies. Each strict conflict object has exactly:

```text
conflict_id
state
dimensions[]
decision_origin
decision_artifact_sha256
comparison_rule_id
comparison_rule_version
configuration_sha256
explanation_code
precedence_status
precedence_rule_id
controlling_position_id
positions[]
```

`potential` is invalid publicly. Dimensions use the Section 20.3 enum and order. `explanation_code` is null unless state is `explained`, when it is one of `unit_equivalent`, `compatible_modality`, `exception`, `amendment`, `supersession`, `disjoint_jurisdiction`, `disjoint_effective_interval`, `disjoint_product_or_equipment_class`, or `human_reviewed_nonconflict`. Precedence fields follow Section 20.3 and do not imply that ClauseSift independently chose a winner. Each strict position object is `{conflict_position_id, position_order, source_ids, spans}`. `source_ids` is the non-empty canonically ordered set of returned evidence sources that completely covers the position; each strict span is `{document_id, node_id, node_text_start, node_text_end}` and exactly matches the release record. Positions are dense and ordered; every source ID exists once in `evidence`, and every `conflict_context` reason points back to one of these objects. Missing sides, extra sides, stale IDs, generated summaries, or a position not completely covered by the returned evidence make serialization fail closed.

Citation fields are generated programmatically. The AI client must not invent or repair missing citations.

Every warning is an object with a Section 31 `code`, `phase`, `severity`, a human-readable `message`, and optional `source_id` and structured `details`; bare warning strings are invalid. Evidence-bound source or build uncertainty is deterministically projected from the admitted diagnostic record into the corresponding Section 31 runtime warning, names the affected `source_id`, and includes the closed `lineage_stage` value `source`, `build`, or `assembly` plus a diagnostic-artifact hash when that code's details contract permits it. Top-level warnings are the union of item warnings and request-level assembly warnings, deduplicated by complete canonical warning bytes and sorted by `(code, phase, source_id-or-empty, canonical details bytes, message)`; warning absence never erases `coordinate_status` or the build uncertainty object. `original_text` and other document-derived fields are untrusted quoted evidence, not instructions to the MCP host or model. Evidence items carry `content_trust: "untrusted_source"`, and tool descriptions instruct clients to preserve that boundary.

---

## 22. MCP interface

The first runtime uses the official Python MCP SDK and local `stdio` transport. ClauseSift v0.1 targets MCP revision `2026-07-28` through the SDK's dual-era server support and must also pass compatibility tests with `2025-11-25` clients. The exact SDK version is pinned and recorded in `build-info.json`; upgrading either protocol behavior or the SDK requires conformance and client-compatibility tests.

On the `2026-07-28` wire path, every non-JSON-RPC-error result carries `resultType: "complete"`. `tools/list`, `resources/list`, `resources/templates/list`, and `resources/read` additionally carry `ttlMs: 0` and `cacheScope: "private"`: the process-lifetime catalogue is stable, but local document metadata and content are not declared shareable across callers, and immediate staleness is the conservative v0.1 policy. The `2025-11-25` path omits all three revision-owned fields. Raw-frame conformance tests verify their required presence, exact values, and legacy absence even when the SDK supplies them below application code.

The v0.1 server advertises only the tools and resources it implements. Its tool and resource lists are stable for the lifetime of the process, so it does not advertise list-change notifications or resource subscriptions. A release-pointer change becomes visible after a server restart, not through an in-session mutable resource catalogue.

### 22.1 Initial tools

#### `search_evidence`

Search the active release and return ranked, citation-ready evidence with applicability context and typed warnings.

```python
search_evidence(
    query: str,
    document_codes: list[str] | None = None,
    document_types: list[str] | None = None,
    editions: list[str] | None = None,
    jurisdictions: list[str] | None = None,
    disciplines: list[str] | None = None,
    status: str | None = "active",
    mode: str = "auto",
    limit: int = 10,
)
```

The input schema constrains `mode` to the Section 17 enum and `limit` to the inclusive range 1-100.

#### `get_clause`

Resolve one cataloged document edition and clause number exactly; do not substitute another edition.

```python
get_clause(
    document_id: str,
    clause_number: str,
)
```

The lookup resolves one canonical clause node, then selects every distinct persisted chunk whose `chunk_nodes` membership is required to cover that clause's retrievable canonical subtree. It creates one direct evidence item only when one chunk provides the complete coverage; otherwise it creates one direct item per covering chunk in ascending canonical chunk order, regardless of whether the boundaries came from independently chunked subclauses, whole-table and row representations, semantic paragraphs, or a token-limit split. Each retains its own `source_id`, page span, bounding boxes, and source-faithful `original_text`; the handler must not aggregate several chunks under one source ID or omit any covering chunk. It then performs Section 19 required closure from all direct items. Expanded items follow the direct covering set, remain distinguishable in lineage, and do not change which chunks count toward exact subtree coverage.

#### `get_context`

Expand a previously returned source ID with its parent conditions, exceptions, notes, tables, and direct references.

```python
get_context(
    source_id: str,
    context_level: str = "supporting",
    include_parent: bool = True,
    include_applicability: bool = True,
    include_dependencies: bool = True,
    include_definitions: bool = True,
    include_exceptions: bool = True,
    include_notes: bool = True,
    include_tables: bool = True,
    include_references: bool = True,
    include_versions: bool = False,
    include_adjacent: bool = False,
)
```

`context_level` is the Section 19 closed enum and its schema description states the inclusive class behavior. The success object always contains top-level `context_completeness`, `evidence`, `conflicts`, and all ten context arrays: `parents`, `applicability`, `dependencies`, `definitions`, `exceptions`, `notes`, `tables`, `references`, `versions`, and `adjacent`. `evidence` is the canonical source-ID-deduplicated union of the requested source, every evidence object projected into a context array, and every conflict-only attachment required by Section 20.3. A complete evidence object repeated in a context array is byte-for-byte identical to its top-level Section 21 object; a relation-only record may refer only to source IDs present in the top-level array. Thus every conflict-position source ID resolves against `evidence`, even when that position is not a member of an enabled relation family. Serialized duplicate objects still count against the response-frame bound. A false include flag performs no traversal for that relation family and requires its corresponding array to be empty; a true flag may also produce an empty array when no matching relation exists. Version and adjacency traversal are opt-in even at diagnostic level. The strict output schema requires the completeness field, evidence/conflict arrays, and all ten context arrays and does not vary its shape with the flags.

The exact `source_id` identifies one chunk, not one arbitrary anchor node. Expansion starts from every node in that chunk's `chunk_nodes`, in persisted `member_order`; it never selects only the first member. The common Section 19 engine applies only enabled relation families through the requested level, uses its numeric bounds and queue ordering, projects results into the ten arrays without changing their Evidence Lineage, and preserves every independent accepted path after source-ID deduplication. Arrays correspond to reverse `contains`, `applies_subject_to`, `depends_on`, definition targets or governing `defines` scope, reverse/forward `exception_to`, note/footnote targets, table targets, ordinary `references`, `supersedes`/`amends`, and `precedes` respectively. A result qualifying for several arrays appears in each relevant array with the same `source_id` and lineage rather than acquiring several identities. A disabled family is not treated as incomplete in this explicit inspection call; unresolved required context in an enabled family is `incomplete_required`.

#### `get_document_metadata`

Return the human-reviewed manifest and release identity for one cataloged document edition.

```python
get_document_metadata(document_id: str)
```

#### `list_documents`

List document metadata in stable `(document_code, edition, document_id)` order with opaque cursor pagination.

```python
list_documents(
    document_type: str | None = None,
    status: str | None = None,
    discipline: str | None = None,
    cursor: str | None = None,
    limit: int = 50,
)
```

The input schema constrains `limit` to 1-100. The result contains `items` and `next_cursor`; `next_cursor` is null on the final page. A cursor is an opaque authenticated encoding of `{release_id, cursor_version, order_version, normalized_filters, last_key}`, where `normalized_filters` contains the exact canonical `document_type`, `status`, and `discipline` values (including nulls) and `last_key` is the last emitted `(document_code, edition, document_id)` tuple. The versioned compact codec is specified so every payload assembled from maximum-length valid fields plus its authentication tag is at most 4,096 Unicode scalar values; the serializer checks that bound and can never publish a cursor rejected by the input schema. Resumption uses a strict lexicographic keyset predicate, never an offset. Invalid authentication, unsupported cursor/order versions, or any filter mismatch is `identifier_invalid`; a valid cursor naming another release is `resource_not_found`. Tests cover the worst-case multibyte payload, tampering, filter mutation, release change, duplicate code/edition prefixes distinguished by `document_id`, empty and final pages, and no duplicates or gaps within one immutable release.

#### `get_page_reference`

Return deterministic page metadata and an authorized reference to the original page for one cataloged document.

```python
get_page_reference(
    document_id: str,
    page_number: int,
)
```

Every tool declares a human-readable description, JSON Schema input and output contracts, and a read-only annotation. Every input-schema property has a non-empty description covering its identifier domain or units, normalization, default and null behavior, list-combination behavior where applicable, and bounds. Each advertised output schema describes that tool's success object only and uses `additionalProperties: false`. A success returns that object in `structuredContent`, conforming to the advertised output schema, with the same JSON serialized into one text content block for legacy clients.

Tool execution errors use the other MCP result branch: they set `isError: true`, omit `structuredContent`, and place exactly one JSON serialization of the strict shared error object `{code, phase, severity, message, details?}` in a text content block. The central serializer validates this object against a separate internal error schema with `additionalProperties: false` and per-code `details` allowlists before emitting it. Because an error has no `structuredContent`, it cannot violate or masquerade as the advertised success output schema. Dual-era conformance tests require every tool's success to validate against its advertised schema and every routed tool error to have `isError: true`, absent `structuredContent`, and text that parses to the validated shared error object.

The stdio decoder caps each complete inbound JSON-RPC frame at 1,048,576 bytes before parsing or allocation beyond that bound. It drains an oversized frame to the transport boundary, emits JSON-RPC `-32600` with a null ID, and invokes no protocol or application handler. All tool input schemas also use `additionalProperties: false` and the following shared, normative bounds. JSON Schema `maxLength` counts Unicode scalar values. Request decoding rejects duplicate object keys and first validates the complete arguments value as I-JSON: strings contain only Unicode scalar values with no lone surrogate, numbers are finite, and every integer lies in the interoperable range `[-9007199254740991, 9007199254740991]`. After schema validation, the server serializes the parsed `params.arguments` with RFC 8785 JSON Canonicalization Scheme and rejects canonical UTF-8 longer than 65,536 bytes before normalization, query planning, model loading, or catalog access. I-JSON/JCS rejection or a bound violation is `identifier_invalid` on the sole runtime tool-input surface, never an exception leak, truncation, or partial processing. The same RFC 8785 bytes define every aggregate-size boundary fixture. The encoder likewise rejects any non-page response whose complete JSON-RPC frame would exceed 1,048,576 bytes before serialization begins; release validation proves every catalog-derived success is bounded accordingly. Page resources use their separately declared 33,554,432-byte complete-frame bound.

| Input class | Bounds |
| --- | --- |
| Search query | Trimmed `minLength: 1`, `maxLength: 4096`; encoded query value at most 16,384 UTF-8 bytes. |
| Opaque `document_id` or `source_id` | `minLength: 1`, `maxLength: 128`, pattern `^[a-z0-9][a-z0-9._:-]{0,127}$`. |
| Clause number, document code, edition, jurisdiction, discipline, status, document type, mode, or context-level string | `minLength: 1`, `maxLength: 128`; enum fields remain closed enums. |
| Cursor | `minLength: 1`, `maxLength: 4096`, plus authenticated-cursor syntax and release binding; the same maximum applies to every emitted `next_cursor`. |
| Any filter array | `maxItems: 64` and `uniqueItems: true`; `search_evidence` accepts at most 256 total values across all filter arrays. |
| Result limit | Integer in the inclusive range 1-100. |
| Page number | Integer in the inclusive range 1-2,147,483,647 and no greater than the selected document's manifested page count. |

The same limits apply before and after the field's specified normalization: a client cannot use trimming, Unicode normalization, or duplicate removal to turn an over-limit input into an accepted one. Registration, parser/canonical-model validation, schema checks, and release validation guarantee that every persisted `document_id`, `source_id`, document code, edition, non-null clause number, jurisdiction, and discipline exposed to a client satisfies the identical applicable input row, so the server never publishes a lookup or filter value that its own tools or resource templates reject. Boundary-value tests cover the exact maximum and one-over values for every string/list class, aggregate bytes, total filter values, and inbound frames, and assert that the retrieval service and model loader are not invoked after rejection.

Every handler returns an internal typed result to one central outbound serializer; that serializer constructs each public result from an explicit per-type field allowlist and fails closed on an unknown field. Diagnostics use code-owned message templates and per-code allowlists for detail keys and value types; raw exception strings, `repr` output, and arbitrary caller-supplied diagnostic messages are never serialized. The legacy text block is generated only from the already validated public object, not through a second formatting path. Raw source paths and internal workspace layout are not allowlisted and therefore cannot appear in either representation. Security regression tests inject an internal path as an extra field and inside otherwise allowed `message` and `details` values, and require both structured and legacy serialization to reject or safely redact it without emitting the sentinel.

The following semantic contract is normative. Each tool's input and advertised success-output schemas encode its selection and success columns directly rather than using unconstrained objects; the separate strict error schema plus Section 31 routing encode the domain-error column.

| Tool | Selection semantics | Success result | Domain-error cases |
| --- | --- | --- | --- |
| `search_evidence` | Bounded trimmed query; values are ORed within each supplied bounded filter list and filter categories are ANDed; `status: null` removes the default active-status filter; `mode` resolves under Sections 17 and 19. Filters constrain direct seeds; every seed runs required graph-and-conflict closure, and high accuracy also requests supporting context. | `{query, retrieval_mode, release, context_completeness, evidence, conflicts, warnings}` where `evidence` contains ordered direct, expanded, and conflict-context Section 21 items; `conflicts` contains the material Section 20.3 records; and `warnings` is typed. | `identifier_invalid` for malformed or over-limit query, filters, or aggregate arguments; `feature_unavailable` for an explicit unsupported mode or bounded load failure; `context_limit_exceeded` when complete required graph/conflict closure cannot fit a declared bound; `release_integrity_failed` when a lazy model asset fails its pre-load integrity check. No matches is a `complete` success with empty evidence/conflicts, not an error. |
| `get_clause` | Exact opaque `document_id` plus normalized exact `clause_number`; no fuzzy clause or edition substitution. Resolve the canonical clause node and select every distinct persisted chunk needed to cover its retrievable subtree, then run required graph-and-conflict closure from every direct covering source. | `{release, context_completeness, evidence, conflicts, warnings}` with a non-empty, canonically ordered array of Section 21 items. Exactly the covering chunks are `retrieval_seed`; later items are distinguishable `expanded_context` or `conflict_context`. Every item retains its own `source_id` and source span. | `identifier_invalid` for malformed input; `resource_not_found` when the document or clause is absent; `context_limit_exceeded` when complete required graph/conflict closure cannot fit a declared bound. |
| `get_context` | Exact `source_id`; `context_level` includes all context classes through the named level; each boolean independently controls one relation family and false yields an empty array for that family. Conflict closure still preserves every material side reached by an enabled family. | `{release, source_id, context_completeness, evidence, context, conflicts, warnings}` where `evidence` is the canonical union defined above and `context` always has required arrays `parents`, `applicability`, `dependencies`, `definitions`, `exceptions`, `notes`, `tables`, `references`, `versions`, and `adjacent`, each containing catalog-bound evidence or relation records when requested and found. | `identifier_invalid` for malformed input or context level; `resource_not_found` for an unknown source; `context_limit_exceeded` when complete required graph/conflict closure for the enabled families cannot fit a declared bound. |
| `get_document_metadata` | Exact opaque `document_id`; no active-edition fallback. | `{release, document}` where `document` contains the safe manifest projection, source hash, review status, and release identity, but no absolute path. | `identifier_invalid` for malformed input; `resource_not_found` for an unknown document. |
| `list_documents` | Non-null filters are ANDed; each filter value is an exact normalized enum or discipline key; ordering and cursor rules are those stated above. | `{release, items, next_cursor}` where every item is the same safe document-metadata summary and `next_cursor` is string or null. | `identifier_invalid` for a malformed filter, limit, or cursor; `resource_not_found` for a cursor bound to another release. |
| `get_page_reference` | Exact opaque `document_id` and one-based integer page number within the manifested source. | `{release, document_id, page_number, page_label, page_uri, content_hash}` where `page_uri` is an authorized `standards://page/...` resource URI, never a filesystem path. | `identifier_invalid` for malformed or out-of-range input; `resource_not_found` for an unknown document or unavailable page. |

Client-supplied `document_id`, `source_id`, cursor, and page or clause identifiers are opaque catalog keys. A handler first resolves them through a parameterized catalog query. It must never interpolate them into SQL, concatenate them into a filesystem path, or decode a cursor into a path. Any catalog-derived path is resolved against an allowlisted release or originals root, then rejected unless it is a regular file beneath that root after normalization and symlink, junction, or reparse-point resolution.

### 22.2 Future tools

- `compare_document_versions`
- `resolve_cross_reference`
- `search_tables`
- `search_product_specifications`
- `get_product_parameter`
- `validate_citation`

### 22.3 MCP resources

Proposed resource URIs:

```text
standards://document/{document_id}
standards://clause/{document_id}/{clause_number}
standards://source/{source_id}
standards://page/{document_id}/{page_number}
standards://release/current
```

Resource URI variables follow the same catalog-first resolution rule as tool inputs. Templates use RFC 6570 simple-string expansion over each normalized semantic value: encode it as UTF-8, leave only RFC 3986 unreserved bytes literal, and percent-encode every other byte with uppercase hexadecimal. The server decodes each route segment exactly once with strict UTF-8, rejects malformed escapes and any segment whose decoded-then-re-encoded form is not byte-identical, then applies field normalization and catalog lookup. Raw or non-canonical `/`, `%`, `?`, `#`, spaces, and non-ASCII forms never reach path or SQL construction. URI tests cover each of those characters, lower-case escapes, invalid UTF-8, and a literal percent-encoded-looking clause identifier without double decoding.

| URI | MCP kind | v0.1 capability |
| --- | --- | --- |
| `standards://document/{document_id}` | Resource template | Read-only; no subscribe; no list-change notification. |
| `standards://clause/{document_id}/{clause_number}` | Resource template | Read-only; no subscribe; no list-change notification. |
| `standards://source/{source_id}` | Resource template | Read-only; no subscribe; no list-change notification. |
| `standards://page/{document_id}/{page_number}` | Resource template | Read-only; no subscribe; no list-change notification. |
| `standards://release/current` | Static resource | Read-only snapshot for the process lifetime; no subscribe; no list-change notification. |

The v0.1 resource catalogue is immutable for one server process. The server does not advertise resource subscription or list-change capabilities.

Every successful `resources/read` result contains exactly one content item whose `uri` is the exact canonical requested URI. No handler returns an empty or multi-item success:

| URI | Content item and exact emitted bytes |
| --- | --- |
| `standards://document/{document_id}` | `TextResourceContents`, `mimeType: application/json`; UTF-8 RFC 8785 serialization of the same safe `{release, document}` success object as `get_document_metadata`. |
| `standards://clause/{document_id}/{clause_number}` | `TextResourceContents`, `mimeType: application/json`; UTF-8 RFC 8785 serialization of the same `{release, context_completeness, evidence, conflicts, warnings}` success object as `get_clause`. |
| `standards://source/{source_id}` | `TextResourceContents`, `mimeType: text/plain;charset=utf-8`; its `text` is exactly the source chunk's validated `original_text`, with no wrapper or normalization, so UTF-8 encoding reproduces the source-faithful bytes. |
| `standards://page/{document_id}/{page_number}` | `BlobResourceContents`, `mimeType: application/pdf`; its `blob` is the base64 encoding of the complete bounded and verified original PDF, and decoding it yields those exact bytes. The URI and companion tool result select the one-based page for client navigation; `get_page_reference.content_hash` equals the SHA-256 of the decoded PDF bytes (`documents.source_file_hash`), not a rendered-page hash. |
| `standards://release/current` | `TextResourceContents`, `mimeType: application/json`; UTF-8 RFC 8785 serialization of the safe immutable release summary and manifest digest. |

The full-PDF page contract avoids pretending that a renderer-created image is an original page, but it is admitted only within explicit v0.1 resource budgets. A complete JSON-RPC resource response, including the echoed request ID, canonical URI, JSON syntax, and base64 text, may be at most 33,554,432 bytes. Registration computes the worst-case page-response size for each PDF using its recorded source size, base64 expansion `4 * ceil(size / 3)`, the canonical longest page URI, and the worst-case serialized request ID allowed by the 1,048,576-byte inbound-frame bound; a document that could exceed the response bound fails the release gate with `release_validation_failed`. The runtime recomputes the exact frame size before allocating or reading source bytes and never truncates a response. A future single-page representation requires its own media type, deterministic renderer configuration, artifact checksum, and URI version.

### 22.4 Errors and protocol behavior

- Unknown methods or tools, malformed JSON-RPC, and requests that do not satisfy the MCP request schema are protocol-level JSON-RPC errors.
- A well-formed tool call that fails semantic validation or execution returns a tool result with `isError: true` and a typed error code, for example `identifier_invalid`, `resource_not_found`, or `feature_unavailable`.
- A valid search with no matching evidence is a successful result with an empty `evidence` array and an `evidence_insufficient` warning. It is not a protocol error.
- A resource URI with a malformed route shape, malformed percent escape, invalid UTF-8, or non-canonical encoding returns JSON-RPC `-32602` (`Invalid params`) on both protocol paths, with no `contents`. No catalog lookup occurs.
- An unknown, well-formed `standards://` resource is never represented as a tool result or an empty `contents` success. `resources/read` returns JSON-RPC `-32602` on the per-request `2026-07-28` path and `-32002` on a `2025-11-25` session. This protocol error is distinct from the ClauseSift `resource_not_found` diagnostic used by tool calls.
- When a known page resource's external original fails the handle-bound containment, identity, stability, size, or hash check below, `resources/read` returns JSON-RPC internal error `-32603` on both protocol paths with the code-owned message `Source integrity check failed` and safe data `{code: "source_hash_mismatch", phase: "runtime", severity: "blocking"}`. It returns no `contents`, absolute path, raw exception text, or partial frame; this denies that resource read without invalidating the immutable release catalogue.
- When a canonical clause resource's complete required closure would exceed a Section 19 bound, `resources/read` returns JSON-RPC internal error `-32603` on both protocol paths with the code-owned message `Required context exceeds limit` and safe data restricted to `{code: "context_limit_exceeded", phase: "runtime", severity: "blocking", bound_name, configured, observed}`. It returns no `contents` or partial Evidence Package.
- Cancellation of an in-progress request follows the per-request revision on the `2026-07-28` path or the initialized session revision on the `2025-11-25` path. Retrieval stops promptly, releases temporary resources, records a non-response cancellation event, and does not publish a partial success or a second tool response. Each request owns an atomic terminal state initially `pending`; success, tool error, cancellation, and server deadline each attempt one compare-and-set transition. The first successful transition is authoritative, including when events carry equal monotonic timestamps, and every losing completion is discarded before serialization.
- Progress notifications are emitted only when the client supplied a progress token and the applicable per-request or session revision supports them.

### 22.5 Worked tool sequence

For “When may mechanical smoke exhaust be omitted?” the client performs this sequence:

1. Call `search_evidence(query=..., mode="high_accuracy")` and verify that the result is successful, has evidence, reports `context_completeness`, and does not contain a blocking diagnostic. Its required and supporting applicability/exception context is already included and distinguished by lineage.
2. If an operator explicitly needs inspection material beyond the answer package, take `evidence[0].source_id` and call `get_context(source_id=..., context_level="diagnostic", include_parent=true, include_exceptions=true, include_adjacent=true)`; do not use diagnostic adjacency as normative answer evidence.
3. Take `document_id` and `page_start` from the same evidence item and call `get_page_reference(document_id=..., page_number=...)` to obtain the catalog-bound page resource.
4. Present `original_text` as untrusted quoted evidence, link the returned page resource, and display every typed warning. Do not claim an answer when either call reports `evidence_insufficient` or `applicability_incomplete`.

---

## 23. CLI design

Initial command surface:

```bash
clausesift init <workspace>
clausesift ingest <path>
clausesift build
clausesift validate
clausesift release
clausesift list-documents
clausesift search <query>
clausesift get-clause <document-id> <clause>
clausesift mcp
```

The CLI and MCP server must call the same runtime service layer rather than implementing separate retrieval logic.

`clausesift mcp` reserves stdout exclusively for MCP frames. Diagnostics, logs, progress intended for operators, and tracebacks go to stderr or the configured log sink; startup failure exits non-zero without writing non-protocol text to stdout.

---

## 24. Build pipeline

The intended build sequence is:

1. Scan the inbox and registered source files.
2. Calculate source hashes.
3. Record current raw manifest-byte hashes for provenance, then safe-load, canonicalize, and verify approved manifest-content and source hashes and source sizes.
4. Detect added, changed, and removed documents.
5. Select parser routes.
6. Produce parser-neutral artifacts for every selected route.
7. Run each adapter's parsing validation and every required dual-parser comparison, finalize the Section 11.3 parser-validation report for both pass and failure paths, and then evaluate the blocking gate; only after the report is durable and all applicable gates pass, select the configured `canonical_primary` artifact and produce canonical documents deterministically from it.
8. Construct clause and node trees.
9. Build the versioned node-level page-provenance artifact and validate its page counts and non-overlapping byte partitions against the source.
10. Generate standards-aware chunks and their source rows from the canonical model plus that page-provenance artifact.
11. Extract and resolve cross-references, generate deterministic conflict candidates, attach every position's complete required context, and classify each candidate under Section 20.3; retain pre-admission `potential` transitions in diagnostics but admit only validated final conflict records.
12. Generate lexical and embedding text.
13. Materialize the candidate SQLite catalog through a connection that verified foreign-key enforcement, require zero rows from `PRAGMA foreign_key_check`, and run every Section 14.1 blocking validation query, including chunk/source totality, source-text and page-span reconstruction, exact-key uniqueness, clause coverage, cross-reference integrity, and conflict position/state/review/source-cover integrity.
14. Generate exactly one chunk embedding per persisted chunk in the declared deterministic row order, only after the catalog gate passes.
15. Build lexical indexes.
16. Build vector artifacts.
17. Validate the complete Section 19 traversal rule set and deterministic materialization cover against the candidate catalog, then materialize the versioned `lineage.json` described in Section 7.2 from the exact source, parser, canonical, page, chunk, catalog, relationship/conflict, review, retrieval-artifact, and traversal-configuration records.
18. Derive `build_content_id` from the canonical manifest hashes, candidate catalog and admitted derived-artifact hashes including `lineage.json`, context and conflict rule-set/vocabulary/configuration/review inputs, evaluation corpus and gate versions, dependency lock, toolchain fingerprint, and reproducible build epoch; run the regression evaluation and durably persist versioned raw results bound to that deterministic ID. An execution failure produces a sanitized failure record rather than skipping report generation.
19. Complete and finalize the static review reports with canonical-tree, chunk, cross-reference, conflict-candidate/state/position, provenance, and current-run evaluation sections; incorporate the already finalized parser-validation report rather than generating it for the first time here.
20. Only after the current evaluation results and report are durable, enforce the documented quality gates.
21. Confirm that no release-blocking parser, catalog, security, integrity, evaluation, or document-review finding remains open.
22. Assemble a candidate release.
23. Validate the release manifest and every required artifact checksum.
24. Reopen the candidate through the read-only runtime and run exact-lookup, search, citation, lineage, all-side conflict, and rollback smoke tests.
25. Publish the release and atomically update the active pointer.

A failure through candidate validation at step 24 must leave `active.json` unchanged. Once step 25 begins its atomic replacement, a crash before the post-replacement directory flush may recover either the complete old or complete new record; recovery verifies the referenced release and records that observed outcome before serving. It never guesses, combines records, or exposes a missing/torn pointer, and a recovered valid new record completes the activation rather than reporting that the active release stayed old.

The publish step is unreachable unless every preceding gate succeeds. The step 13 catalog gate runs before any embedding or index builder is invoked and before any such derived artifact is written to the build cache; a failure may retain parser, chunk, conflict, and catalog diagnostics but produces no embedding, lexical-index, vector-index, or lineage artifact. Evaluation gate enforcement is likewise unreachable until step 19 has finalized a report bound to the same deterministic `build_content_id` and exact raw-result hash; a metric failure or evaluation-execution failure blocks at step 20 while retaining that diagnostic report. A wall-clock or random operational run ID exists only in the external operator lifecycle ledger and never enters a release-admitted report or evaluation artifact. Tests must inject failures at conflict classification/review, the catalog gate, lineage finalization, evaluation execution and quality gate, and before and during candidate validation, proving that required diagnostics remain available, downstream builders were not called where applicable, and neither the active pointer nor the previous release changes.

---

## 25. Build cache and invalidation

A source file hash alone is not sufficient for build caching.

The cache identity should include:

```text
source_file_hash
manifest_content_hash
parser_name
parser_version
parser_configuration
parser_role_assignment
parser_neutral_artifact_sha256
parser_validation_report_sha256
comparison_gate_version
comparison_gate_configuration
ocr_configuration
normalizer_version
page_mapper_version
page_provenance_artifact_sha256
chunker_version
cross_reference_resolver_version
embedding_model
embedding_model_revision
embedding_model_artifact_sha256
lexical_index_version
schema_version
reproducible_build_epoch
dependency_lock_hash
build_toolchain_fingerprint
lineage_schema_version
context_rule_set_version
context_rule_configuration_sha256
conflict_detector_version
conflict_rule_set_version
conflict_rule_configuration_sha256
unit_registry_version
conflict_review_artifact_sha256
```

The list above is the dependency vocabulary, not one flat cache key. Each artifact hashes only its declared inputs below, including the hashes of upstream artifacts rather than their paths.

| Cached artifact | Required cache-identity inputs |
| --- | --- |
| Parser-neutral output | Source-file hash and size; approved manifest-content hash; assigned role; adapter name, version, and configuration; parser-neutral schema version; OCR configuration and declared local asset digests; dependency-lock hash; build-toolchain fingerprint. The output hash is a result, never an input to locating this cache entry. |
| Parser-validation report | Approved manifest-content hash; source-file hash and size; ordered tuples `(role, adapter identity, adapter version, adapter configuration, declared local-asset digests, parser-neutral artifact SHA-256)` for every selected route; every single-parser validator version/configuration; comparison-gate implementation version and configuration when enabled; report schema version. Only a passing deterministic report is promoted into this cache; all attempts retain their diagnostic copy outside it. |
| Canonical model | Approved manifest-content hash; selected `canonical_primary` artifact SHA-256; hash of the passing parser-validation report; normalizer version and configuration; canonical schema version; dependency-lock hash; build-toolchain fingerprint. The manifest hash preserves document identity and metadata even when two manifests select identical source/parser bytes. No canonical entry is written for a failed report. |
| Page-provenance map | Canonical-model artifact hash; selected primary parser-neutral artifact SHA-256; source-file hash and size; page-mapper version, configuration, and schema version; dependency-lock hash; build-toolchain fingerprint. Its content-addressed output contains the authoritative ordered node byte spans, page numbers, and optional boxes imported at step 13. |
| Chunks and source rows | Canonical-model artifact hash; page-provenance artifact hash; chunker version and configuration; chunk, membership, and source-projection schema versions. |
| Cross-references | Canonical-model artifact hash; approved `reference_edition_overrides`; cross-reference resolver version and configuration; digest of only the resolver-relevant target subset. That sorted subset contains the source document, every candidate whose document code appears in a parsed external reference (all editions for an unqualified code and the named edition for a qualified code), and every document ID named by an approved override, each represented as `(document_id, document_code, edition, canonical_node_tree_hash)`. It is deterministically empty beyond the source document when no external reference or override exists. |
| Conflict analysis | Canonical-model, page-provenance, chunk/source, cross-reference, and document applicability/status/type artifact hashes; context rule-set/configuration and deterministic required-context source-cover projection hashes; sorted canonical comparison projections grouped by comparison key; detector, conflict-rule-set, unit-registry, modality, tolerance, comparison-projection, and conflict schema versions/configurations; ordered immutable conflict-review and precedence-rule artifact hashes. Potential candidates and final state transitions are deterministic outputs, not cache-locator inputs. |
| Chunk embeddings | Ordered tuples `(document_id, canonical_order, chunk_id, embedding_text_hash)` from the chunk artifact in the declared row order; `embedding_scope: "chunk"`; row-order version; embedding model identifier and revision; local model-artifact SHA-256 or external-provider request parameters; embedding configuration; dependency-lock hash; build-toolchain fingerprint. |
| Lexical index | Ordered search-text and metadata hashes from the chunk artifact; lexical-index engine, version, configuration, and schema version. |
| Vector index | Embedding artifact hash; vector-index engine, version, distance metric, configuration, dependency-lock hash, and build-toolchain fingerprint. |
| Evidence lineage | Approved manifest-content and exact source hashes/sizes; ordered selected parser-route provenance-envelope hashes; passing parser-validation-report hash; canonical-model, page-provenance, chunk/source, catalog, cross-reference, conflict-analysis, embedding, lexical-index, and vector-index artifact hashes; lineage schema version; context/conflict rule-set, relation/node/dimension vocabulary, review, ordering and configuration hashes. The output excludes its own hash, `build_content_id`, `release_id`, operational IDs, and timestamps. |
| Release assembly | Hashes of the canonical catalogue and every admitted derived artifact; approved manifest-content hashes; release schema and configuration; evaluation-corpus and gate-result hashes; explicit reproducible build epoch; dependency-lock hash; build-toolchain fingerprint. |

Adding, removing, or changing a resolver-relevant target edition therefore invalidates affected cross-reference artifacts even when the source PDF and its own canonical tree are unchanged; an unrelated document does not invalidate them. Downstream release assembly is invalidated by the changed cross-reference artifact hash. A raw-byte-only manifest formatting change is recorded only in the external operator lifecycle ledger and does not alter semantic cache keys or release bytes.

`build_toolchain_fingerprint` includes the Python implementation and version, operating system and architecture, resolved package set, and native parser/index library versions. Local model artifacts are identified by the digest of the bytes actually used, not only a mutable model name or revision string. External providers record provider, model identifier, documented revision, and request parameters; credentials are never part of the cache key or build record.

---

## 26. Release format

A compiled release may use the following layout:

```text
releases/
└── <release_id>/
    ├── manifest.json
    ├── build-info.json
    ├── knowledge.sqlite
    ├── lineage.json
    ├── chunks.jsonl
    ├── embeddings.f16.npy
    ├── lexical-index/
    ├── vector-index/
    ├── models/                 # optional query-embedding and reranker assets
    ├── documents/
    ├── pages/
    ├── reports/
    ├── build-ledger.jsonl
    └── evaluation-results.json
```

`release_id` is the filesystem-safe token `rel-sha256-` plus 64 lowercase hexadecimal characters: the SHA-256 of a versioned RFC 8785 release-assembly identity record containing `build_content_id`, sorted `(relative_path, byte_size, sha256)` tuples for every release artifact except `manifest.json`, the complete assembly configuration, and `reproducible_build_epoch`; it excludes `release_id`, final manifest bytes, `active.json`, and all operational timestamps to avoid recursion. Any different admitted byte, declared assembly input, or epoch therefore produces a different ID. An optional human `release_label`, such as `2026.08`, is display metadata included in that identity record and is never used for equality, cursor binding, directory selection, or activation.

The release manifest records:

- release identifier;
- optional human release label;
- deterministic build-content identifier;
- reproducible build epoch;
- document and chunk counts;
- schema version;
- lineage-schema version and `lineage.json` artifact hash;
- context rule-set, relation/node vocabulary, ordering, limit values, and canonical configuration hash;
- conflict detector/rule/schema, dimension/explanation/modality vocabulary, unit registry, tolerances, ordered review/precedence artifact hashes, and counts by state/dimension/touched tier;
- parser and chunker versions;
- embedding and reranker model identifiers, revisions, formats, and complete asset hashes;
- chunk-embedding scope, row count, row-order version, vector dimensions, dtype, and normalization state;
- index engine versions;
- source and artifact checksums;
- terminal hash of the sealed `build-ledger.jsonl`;
- evaluation summary.

The artifact table is exhaustive for release-relative files the runtime may open and records relative path, byte size, media type, and SHA-256. `manifest.json` is not recursively listed in its own table; its complete-byte digest is stored in `active.json`. Original source PDFs remain external workspace inputs rather than release artifacts: the document record stores their approved hash and size, registration enforces the Section 22.3 response-size admission bound, and `get_page_reference` performs an availability check before issuing a URI. That preliminary check is not authority for a later read. The page-resource handler opens one stable source handle and verifies the exact buffered bytes it will return under the runtime contract below. `chunks.jsonl` is an optional audit/export projection of SQLite and is never runtime authority. `build-info.json` records the build-toolchain fingerprint and dependency-lock hash.

The immutable `reproducible_build_epoch` is an explicit integer input using `SOURCE_DATE_EPOCH` semantics and is part of the release-assembly identity; a production release fails closed when it is absent. Serializers derive any embedded UTC date from that value and never read the wall clock. Actual build start, finish, validation, and activation times are operational events recorded only in the external operator lifecycle ledger, so identical release inputs produce byte-identical artifacts rather than stale or cache-dependent timestamps.

ClauseSift v0.1 represents the active release with a canonical JSON regular file named `active.json`, containing exactly the release ID and complete manifest digest; a symlink is not an activation pointer. Activation writes a complete sibling temporary file on the same filesystem, flushes that file, atomically replaces `active.json`, and then flushes the parent directory with the platform's documented durability primitive. Activation is successful only after the post-replacement directory flush completes; an orphaned temporary file is never authority and is discarded during recovery. A reader opens and parses one `active.json` snapshot and then verifies that exact manifest digest; it never combines fields from separate reads. Rollback uses the identical protocol. A platform without proven atomic-replacement and post-replacement-directory-flush primitives for this file form is unsupported.

Before activation, the builder verifies every required artifact, validates `lineage.json` against the declared lineage-schema version, proves that every catalog source has exactly one matching lineage record and every lineage reference names an admitted artifact, verifies the complete Section 19 traversal rules, bounds, ranks, required-node covers, and vocabulary/configuration hashes, and reruns the Section 20.3 conflict candidate, state, side, review, precedence, source-cover, tier-policy, and manifest-summary checks. It then writes the manifest digest into the temporary `active.json` described above. Checksums protect against accidental corruption and partial replacement. The local single-user v0.1 threat model does not claim authenticity against an attacker who can rewrite both a release and `active.json`; signed release manifests and an external trust root are required before releases are distributed across trust boundaries.

---

## 27. Runtime loading strategy

ClauseSift should use memory mapping and operating-system page caching instead of eagerly copying the complete knowledge base into process memory.

Recommended strategy:

- compact document metadata: load at startup or rely on SQLite page cache;
- chunk text: read from SQLite on demand;
- dense vectors: NumPy memory map;
- lexical index: open as a disk-backed index;
- query embedding model: lazy load;
- reranker: lazy load only for high-accuracy queries;
- original PDF pages: open only when source inspection is requested.

This design retains fast warm queries without creating unnecessary startup memory pressure.

At process startup, the runtime reads `active.json` once, verifies its manifest digest, then verifies the checksum, byte size, and expected type of every release artifact it may open. It validates the complete `lineage.json`, its declared schema version, referenced artifact hashes, one-to-one source coverage, exact Section 19 rule-set/vocabulary/configuration hashes, and every Section 20.3 conflict record/review/position/source-cover plus manifest count before accepting a query; evidence serialization, traversal, and conflict closure read only those validated immutable representations. It performs these checks before opening SQLite, indexes, release page files, or arrays. External originals follow the on-demand hash, size, containment, and symlink checks in Sections 22.1 and 26. A mismatch fails startup with `release_integrity_failed`; the runtime never falls back to an older or partially readable artifact without an explicit operator rollback.

Page-resource reads share a fixed 67,108,864-byte process working-set budget in v0.1, in addition to the request-count limit below. Before opening a source, the handler computes and atomically reserves `catalog_source_size + 1 + exact_serialized_response_size`; the extra byte is the bounded oversize probe used below. If the release-time response bound would be exceeded, catalog metadata is inconsistent and the read follows `source_hash_mismatch`, while temporary budget exhaustion returns the same both-revision `-32000` `Server busy` admission error defined below with safe reason `response_byte_budget`. No source buffer, probe, base64 value, or outbound frame is allocated before reservation, and the reservation is released on every terminal path.

After reservation, the handler opens the catalog-derived locator relative to a trusted originals-root directory handle using platform-specific component-by-component no-follow/reparse-point protections; it never verifies one pathname and later reopens it. It requires the opened handle to identify a regular file beneath that root, snapshots handle metadata, reads at most the approved size plus one byte into the bounded response buffer, and snapshots the same handle again. The two snapshots must identify the same file and approved size. The handler hashes exactly the buffered bytes, requires the approved digest and size, and base64-encodes that same immutable buffer into the already bounded response. A pathname replacement after open therefore cannot change the returned file, and an in-place mutation yields either the approved bytes or an integrity error—never unverified output. The Windows implementation uses the equivalent handle-relative open, final-handle-path, file-ID, and reparse checks. All failures occur before any response bytes are emitted.

Dense vectors are one numeric, chunk-only `embeddings.f16.npy` matrix opened with `numpy.load(..., mmap_mode="r", allow_pickle=False, max_header_size=10000)`. Object and structured dtypes, pickle-enabled fallback, and `.npz` runtime artifacts are forbidden in v0.1. The runtime requires manifest-declared `embedding_scope: "chunk"`, `float16`, rank two, shape `(chunk_count, vector_dimensions)`, normalization state, row count, row-order version, read-only mapping, and expected file size before serving a query. It reconstructs the total `(document_id, canonical_order, chunk_id)` row map from the validated catalog and requires one and only one row for every chunk; result indices are resolved only through that map and can never denote a document row or depend on SQLite insertion order. Other serialized model or index formats require an explicit safe-loading review before admission to the release format.

Lazy embedding and reranker model assets are part of the exhaustive release artifact table even though they are opened after startup. Before invoking a model loader, the runtime rechecks every file that loader may open against its manifest SHA-256 and byte size. ClauseSift v0.1 allowlists non-executable weight formats such as Safetensors or ONNX plus schema-validated JSON/tokenizer assets; pickle-backed PyTorch `.pt`, `.pth`, or `.bin`, joblib, and loaders with arbitrary-code hooks are rejected. The model format, loader name and version, and complete ordered asset digest are recorded in `build-info.json`; a missing, extra, or changed model file fails with `release_integrity_failed` before deserialization.

Normal work admission is atomic with respect to release state and is capped by schema-validated integer `max_in_flight_requests` in `1..1024`. The transport decoder remains live under saturation so cancellation and other protocol control frames are processed promptly, but it never places work in an unbounded decoded queue. A work request encountered while the admitted set is full is not admitted and receives JSON-RPC server error `-32000` on both protocol paths, with code-owned message `Server busy` and safe data `{code: "feature_unavailable", phase: "runtime", severity: "blocking", reason: "max_in_flight"}`; page-response budget exhaustion uses the identical error with reason `response_byte_budget`. No source open, response allocation, or model loader runs after either admission failure. The first lazy-asset integrity failure atomically changes process release state from `active` to `quarantined`, closes work admission, stops the decoder at a declared input-frame boundary, and snapshots the bounded admitted set before any loader runs. A complete work request is therefore either already in that snapshot, already rejected for saturation, or outside the shutdown input boundary; there is no decoded-but-unowned work request.

The triggering search and each snapshotted tool call whose Section 22 terminal state is still `pending` race once to commit `isError: true`, code `release_integrity_failed`, and safe reason `release_quarantined`; a pending `resources/read` races to commit JSON-RPC `-32603` with the same code, phase, and severity. A cancellation, deadline, success, or other error that already won retains its outcome, including cancellation's non-response rule. No new work request is admitted and no success may commit after quarantine. The server terminates and reaps model-loader and other runtime request workers, enqueues at most one terminal frame for each winning transition, and attempts to flush the bounded output set until `quarantine_shutdown_ms`. Cooperative transports acknowledge all frames before non-zero exit. If output remains blocked at the deadline, the server records only the bounded undelivered count and server-generated correlation IDs through the redacted runtime diagnostic sink, never client-controlled JSON-RPC IDs or the operator lifecycle ledger, and forces non-zero exit; bounded shutdown does not claim guaranteed delivery to a non-reading client. A restart must fail startup until the operator restores the exact release bytes or rolls back the active pointer. Tests control state-transition barriers, transport backpressure, and flush acknowledgement rather than relying on timing.

MCP tool calls that trigger lazy loading of the query embedding model or the reranker should emit progress notifications guarded by a client-supplied progress token, so the client can display loading state instead of assuming a stalled call. A call is `cold` when it loads at least one required lazy model, `warm` when every model it uses was already resident, and `model_free` when its selected path uses no model. Section 18 refers to this contract rather than defining a second timeout policy.

Runtime configuration declares a per-caller overall tool-call deadline and a per-attempt model-load deadline. A cold caller waits no longer than the earlier of its own overall deadline and the shared attempt's load deadline. The attempt deadline starts from a monotonic clock when its worker is spawned; every later caller joining that attempt observes the same absolute deadline rather than extending it. Lazy models load and run inference in supervised, terminable worker subprocesses, so timeout enforcement never depends on cancelling an in-process thread. A model handle becomes visible only when the supervisor atomically transitions the attempt from `loading` to `ready`.

If the attempt-level model-load deadline wins that transition, the supervisor marks the attempt `timed_out`, terminates and reaps its worker, discards any late completion, clears the single-flight state, and completes each still-live waiter exactly once. An explicit `hybrid` or `high_accuracy` waiter fails with `feature_unavailable` and safe detail `reason: model_load_timeout`; an `auto` waiter may continue through an already available path within its own overall deadline and emits `retrieval_capability_unavailable`.

If the overall deadline expires first for any cold, warm, or model-free tool call and wins the Section 22 atomic terminal transition, request-specific work stops promptly, temporary resources are released, and no partial success is published. The server returns exactly one `isError: true` tool result with `code: request_deadline_exceeded`, `phase: runtime`, `severity: blocking`, the code-owned message `Request deadline exceeded`, and safe details limited to `operation` and configured `deadline_ms`; it emits no success or second response. Expiry detaches only that caller from a shared model-load attempt and does not abort an attempt with another live waiter. Cancellation that wins the transition follows the non-response rule; success or another tool error that commits first remains the sole response even if cancellation or deadline observation follows. If cancellation or overall expiry removes the attempt's final live waiter, the supervisor terminates and reaps the worker, clears the attempt without publishing a handle, and does not count that no-waiter abort as a model failure or open the failure cooldown. Tests use an injectable monotonic clock plus synchronization barriers to force cancellation-first, deadline-first, completion-first, and equal-timestamp transition attempts without wall-clock sleeps. Configured values, winning outcome, and latency are recorded in performance results.

Lazy initialization is single-flight per model and globally load-serialized: at most one attempt for any model runs across the process. Concurrent callers needing that same model join its bounded attempt; a request for a different unloaded model enters a FIFO load queue and remains subject to its own overall deadline. The per-attempt load deadline begins only when that queue entry spawns its worker, never while it is waiting behind another model, and an entry with no live callers is removed without a load or cooldown penalty. Waiting callers remain independently cancellable. A genuine loader failure or attempt-level timeout clears the single-flight state and opens a per-model negative-cache cooldown: 30 seconds after the first failure, doubling after consecutive failures to a 10-minute cap. Calls during cooldown do not trigger a loader; explicit modes fail with `feature_unavailable` and safe detail `reason: model_load_backoff`, while `auto` may use an available model-free path with `retrieval_capability_unavailable`. A successful load resets that model's failure count. Tests use a controllable monotonic clock and a fake supervised worker to cover two joined callers with different overall deadlines, FIFO requests for different models, final-waiter detachment, the load-completion/deadline race, forced worker termination and reaping, late-result rejection, exactly-once caller completion, and per-model cooldown accounting. The configured deadlines, queue/cooldown state, and attempt count are observable without exposing model paths.

---

## 28. Static review reports

Each imported document should produce a static HTML report, without requiring a web application.

The report should expose:

- document metadata;
- heading and clause tree;
- parser output;
- chunk boundaries;
- original and normalized text;
- rendered source page;
- bounding boxes;
- table structure;
- OCR status;
- parser and validation warnings;
- extracted cross-references;
- every conflict candidate transition, final state/dimension, exact source position, explanation/precedence rule, review hash, and touched-tier gate result.

This provides the most valuable document-inspection capability of a large RAG platform without its operational infrastructure.

All manifest values, parser output, source text, warnings, SVG/XML-like text, and filenames are untrusted report data. The report generator inserts them only through context-aware HTML attribute/text escaping or inert JSON data blocks that escape `<`, `>`, `&`, U+2028, and U+2029; it never concatenates them into markup, URLs, CSS, or script. It rejects or strips active content from derived page assets and emits an offline Content Security Policy at least as strict as `default-src 'none'; img-src 'self' data:; style-src 'self'; script-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'`. Reports make no network request and use only checksummed local assets.

---

## 29. Evaluation strategy

### 29.1 Golden question set

The evaluation corpus should contain real questions covering:

- exact document identifiers;
- exact clause identifiers;
- definitions;
- scope and applicability;
- mandatory requirements;
- exceptions;
- informative notes;
- table values and units;
- product model numbers and parameters;
- cross-clause references;
- cross-document references;
- scope-plus-exception, table-row, definition, dependency-chain, cycle, unresolved-target, and cross-edition context traversals with versioned expected source IDs and edge paths;
- confirmed numeric/normative conflicts, compatible stricter requirements, unit-equivalent values, valid exceptions, amendment/supersession changes, disjoint jurisdictions/effective intervals/equipment classes, missing applicability, parser extraction disagreement, three-way conflicts, trusted precedence, and no-precedence cases with versioned expected candidates/states/positions;
- version differences;
- unanswerable questions;
- ambiguous questions;
- malformed, overlong, and out-of-range tool inputs;
- questions likely to trigger unsupported inference;
- English, Chinese, and cross-language queries.

### 29.2 Retrieval metrics

- Recall@5
- Recall@10
- Recall@20
- Mean Reciprocal Rank
- nDCG
- correct-document rate
- correct-edition rate
- correct-clause rate
- correct-page rate
- table-evidence hit rate
- required-context recall by source ID
- context-path fidelity by ordered edge-ID sequence
- optional-context precision
- over-expansion rate and evidence expansion factor
- prohibited-edge and cross-edition-contamination count
- byte-identical context ordering rate
- conflict-candidate recall
- confirmed/unresolved conflict precision
- explained-difference precision by explanation code
- conflict state/dimension/position accuracy
- all-material-side preservation rate
- false precedence-selection and model-only-confirmation count

### 29.3 End-to-end metrics

- citation accuracy;
- evidence support rate;
- unsupported assertion rate;
- refusal accuracy;
- version-selection accuracy;
- document-type interpretation accuracy;
- context completeness;
- context over-inclusion and status preservation;
- conflict recognition, explanation, uncertainty, and no-winner compliance.

Metric ownership is explicit:

| Metric family | Authoritative grader |
| --- | --- |
| Recall, rank, document, edition, clause, page, table-hit, context-source, context-path, ordering, prohibited-edge, and cross-edition metrics | Executable comparison of returned catalog IDs, ranks, context classes, ordered edge paths, statuses, and complete canonical output against versioned expected values. |
| Citation accuracy and version-selection accuracy | Executable validation of citation fields, source hashes, and selected edition against the catalog and golden label. |
| Refusal accuracy | Executable confusion matrix against independently human-labeled answerability. |
| Evidence support and unsupported assertion rates | Blinded human claim-to-evidence rubric with claim-level labels. |
| Document-type interpretation accuracy | Blinded human rubric against the manifested document role and the claim made. |
| Context completeness and over-inclusion | Executable expected-set/path comparison is authoritative where the golden case names exact catalog IDs; blinded human review covers whether the versioned expected set itself correctly classifies required, supporting, and irrelevant engineering context. |
| Conflict candidate/state/dimension/position, all-side preservation, and precedence-policy metrics | Executable comparison against versioned exact conflict records is authoritative for deterministic numeric/unit/relation/metadata cases. Blinded human review establishes the golden label for normative-language incompatibility, explanation, shared applicability, and whether a precedence conclusion is supported. |

The human rubric and label set are versioned. Two blinded reviewers independently label every initial release-gate item; after the first release, the second reviewer covers a preregistered stratified sample of at least 20%, every gate failure, and every item the primary reviewer marks uncertain. Each release cycle also intermixes a versioned blinded calibration set, excluded from product metrics, containing at least 10 independently adjudicated examples of every rubric category. Both reviewers label every calibration item without seeing its reference label.

Agreement is reported before adjudication. Nominal labels use unweighted Cohen's kappa and ordinal labels use the rubric's preregistered fixed weight matrix; a computable coefficient must be at least 0.80 on both the release sample and calibration set. If the release sample is degenerate because both reviewers assign its every item to the same single category, its kappa is recorded as `not_estimable`, never as zero or one. That sample passes the reliability gate only when raw agreement is exactly 100%, the independently labeled release sample otherwise meets its coverage rule, and the same reviewers achieve a computable calibration-set kappa of at least 0.80 using at least two observed categories. A degenerate calibration result, any release-sample disagreement in this fallback case, or any coefficient below 0.80 blocks release; affected semantic metrics remain exploratory while the rubric is clarified and the samples are relabeled. Disagreements are adjudicated by a third reviewer, and raw labels, category counts, agreement, coefficient computability, adjudication, and final scores are retained. An LLM grader may assist analysis but cannot be the sole release-gate authority.

### 29.4 Initial quality gates

These are internal targets, not external industry standards:

- exact clause lookup success: zero failures across the complete versioned deterministic lookup suite;
- expected evidence present in Recall@20: one-sided 95% Wilson lower confidence bound at least 98%;
- expected evidence present in Top 5: one-sided 95% Wilson lower confidence bound at least 95%;
- document, edition, clause, and page citation accuracy: zero failures across the complete versioned deterministic citation suite;
- unsupported deterministic conclusions in the golden set: zero observed failures;
- required context, lineage paths, source status, and deterministic ordering: zero failures across the complete versioned traversal conformance suite;
- prohibited, unresolved, guessed, or wrong-edition traversal: zero accepted edges across the complete versioned negative suite;
- optional-context precision: one-sided 95% Wilson lower confidence bound at least 95%, with the expansion factor reported by mode and node/relation family;
- conflict-candidate recall: one-sided 95% Wilson lower confidence bound at least 95%;
- confirmed/unresolved conflict precision and explained-difference precision: one-sided 95% Wilson lower confidence bound at least 98% for each reported state/code family;
- conflict position/source/lineage completeness, all-side runtime preservation, state/dimension ordering, and trusted-precedence serialization: zero failures across the complete deterministic conflict conformance suite;
- explained exception/version/jurisdiction/scope/unit/modality cases misreported as confirmed conflict, unresolved or model-only candidates promoted without admissible review, and winner selection without encoded precedence: zero occurrences across the complete negative suite.

Quality gates may be revised only through documented evidence.

Phase 0's 30-50 questions are an exploratory seed, not a statistically precise release gate. For the probabilistic retrieval, optional-context, and conflict gates, the evaluation plan uses independent labeled cases and a one-sided 95% Wilson interval; at least 150 applicable cases are required for each 98% gate and at least 60 for each 95% gate, with larger stratified samples required when a critical query, context-rule, conflict dimension/state, or hard non-conflict explanation would otherwise be underrepresented. A percentage is never reported without its numerator and denominator, and a release does not pass when the lower bound misses the target. The 100% and zero-failure criteria are deterministic conformance count gates rather than claims that a finite confidence interval proves population perfection; they report the complete suite size and every failure.

---

## 30. Performance strategy

Performance is optimized only after quality gates are met.

The runtime should measure separately:

- exact lookup latency;
- lexical retrieval latency;
- dense retrieval latency;
- fusion latency;
- reranking latency;
- context expansion latency;
- total MCP tool latency.

For every executed stage and total tool latency, report p50, p95, p99, maximum, sample count, and error/cancellation rate, segmented by tool, resolved retrieval mode, and the Section 27 load state. Cold, warm, and model-free calls are separate series; aggregate averages must not hide model-load latency.

Preferred optimization order:

1. cache query analysis;
2. cache query embeddings;
3. cache frequent query results;
4. memory-map vectors;
5. parallelize lexical and dense retrieval;
6. lazy-load models;
7. batch reranker inference;
8. use hardware acceleration where justified;
9. evaluate ANN only after exact search becomes a measured bottleneck.

ClauseSift must not silently degrade retrieval quality to meet a latency target.

---

## 31. Error and warning model

Warnings and failures should be typed and machine-readable.

Initial categories:

- `identifier_invalid`
- `resource_not_found`
- `feature_unavailable`
- `retrieval_capability_unavailable`
- `manifest_invalid`
- `source_hash_mismatch`
- `release_integrity_failed`
- `parser_failed`
- `ocr_low_confidence`
- `parser_comparison_difference`
- `source_coordinate_incomplete`
- `context_incomplete`
- `context_truncated`
- `context_cycle_detected`
- `context_status_boundary`
- `context_limit_exceeded`
- `evidence_conflict`
- `conflict_unresolved`
- `conflict_review_required`
- `clause_sequence_anomaly`
- `table_structure_anomaly`
- `cross_reference_unresolved`
- `edition_conflict`
- `document_status_unknown`
- `applicability_incomplete`
- `evidence_insufficient`
- `release_validation_failed`
- `request_cancelled`
- `request_deadline_exceeded`

MCP responses should carry relevant warnings alongside evidence.

Every emitted diagnostic includes `phase` (`manifest`, `parse`, `build`, `release`, or `runtime`) and `severity` (`blocking` or `advisory`). The tuple `(code, phase, operation or condition)` has exactly one surface in the normative routing table:

| Code | Phase and operation or condition | Severity | Sole surface |
| --- | --- | --- | --- |
| `identifier_invalid` | Runtime tool input | blocking | `isError: true` tool result |
| `resource_not_found` | Runtime tool lookup after valid input | blocking | `isError: true` tool result |
| `feature_unavailable` | Runtime explicit retrieval mode or model-load timeout | blocking | `isError: true` tool result |
| `retrieval_capability_unavailable` | Runtime `auto` fallback | advisory | In-band warning on a successful tool result |
| `manifest_invalid` | Manifest schema or approval validation | blocking | Build/review report |
| `source_hash_mismatch` | Manifested source admitted to a build | blocking | Build/review report |
| `source_hash_mismatch` | Runtime `resources/read` of a changed or unsafe external original | blocking | JSON-RPC `-32603` with safe diagnostic data and no contents |
| `release_integrity_failed` | Runtime startup artifact verification | blocking | Process startup failure and operator diagnostic; no MCP session starts |
| `release_integrity_failed` | Runtime lazy-model pre-load failure causes quarantine; triggering or other snapshotted admitted tool call still `pending` | blocking | Exactly one `isError: true` tool result is attempted; the failed loader is not invoked and no new work or success starts after quarantine |
| `release_integrity_failed` | Runtime quarantine transition for a snapshotted admitted `resources/read` still `pending` | blocking | JSON-RPC `-32603` with safe diagnostic data and no contents is attempted |
| `parser_failed` | Parse subprocess failure or invalid parser-neutral output | blocking | Build/review report |
| `ocr_low_confidence` | Parse OCR quality review | advisory | Build/review report |
| `ocr_low_confidence` | Runtime lineage assembly for admitted OCR evidence below the advisory threshold | advisory | In-band warning on the affected evidence item and successful tool result |
| `parser_comparison_difference` | Parse comparison passes with a non-zero below-threshold difference | advisory | Build/review report |
| `parser_comparison_difference` | Runtime lineage assembly for evidence from an admitted document with a below-threshold parser difference | advisory | In-band warning on the affected evidence item and successful tool result |
| `source_coordinate_incomplete` | Runtime lineage assembly for source text whose validated page mapping has no complete bounding-box coverage | advisory | In-band warning on the affected evidence item and successful tool result |
| `context_incomplete` | Runtime required traversal encounters a non-resolved required occurrence with no target | advisory | In-band warning with `context_completeness: "incomplete_required"` on the affected item and successful tool result |
| `context_truncated` | Runtime supporting or diagnostic traversal reaches an item, path, step, or response-byte bound | advisory | In-band warning with `context_completeness: "truncated_optional"` on the affected result and successful tool result |
| `context_cycle_detected` | Runtime reaches the first repeated node on an allowed `references` or `depends_on` path | advisory | In-band warning on the affected evidence item and successful tool result; the repeated step is not followed |
| `context_status_boundary` | Runtime seed or explicit traversal target is superseded/withdrawn, or crosses editions of one document code without version-comparison intent | advisory | In-band warning on the affected evidence item and successful tool result; no edition substitution occurs |
| `context_limit_exceeded` | Runtime evidence-returning tool's complete required traversal would exceed a semantic-depth, item, path, step, or serialized-byte bound | blocking | Exactly one `isError: true` tool result; no partial Evidence Package is emitted |
| `context_limit_exceeded` | Runtime `resources/read` of a canonical clause whose complete required traversal would exceed a declared bound | blocking | JSON-RPC `-32603` with the safe diagnostic data in Section 22.4 and no contents |
| `evidence_conflict` | Runtime graph/conflict closure selects any position of a `confirmed` conflict | advisory | In-band warning on every returned material position and successful result; the complete conflict object is present |
| `conflict_unresolved` | Build classification of a complete standard-only conflict whose applicability or incompatibility remains unresolved | advisory | Build/review report and immutable conflict record |
| `conflict_unresolved` | Runtime graph/conflict closure selects any position of an admitted `unresolved` conflict | advisory | In-band warning on every returned known position and successful result; the complete conflict object is present |
| `conflict_review_required` | Build/release classification leaves an unresolved conflict touching a critical document | blocking | Build/release report and non-zero builder exit; no release is assembled |
| `clause_sequence_anomaly` | Parse structural validation | advisory | Build/review report |
| `table_structure_anomaly` | Parse structural validation | advisory | Build/review report |
| `table_structure_anomaly` | Runtime required traversal from an admitted table/row cannot supply validated title, header, unit, or parent structure | advisory | In-band warning with `context_completeness: "incomplete_required"` on the affected item and successful tool result; no structure is inferred |
| `cross_reference_unresolved` | Build reference resolution for a `standard` document | advisory | Build/review report; the unresolved row has no navigable target |
| `cross_reference_unresolved` | Runtime requested traversal observes a non-resolved occurrence in a shipped `standard` document | advisory | In-band warning on the affected seed and successful tool result; no target or path is invented |
| `cross_reference_unresolved` | Release validation for any non-resolved row in a `critical` document | blocking | Release report and non-zero builder exit |
| `edition_conflict` | Build extracted-versus-manifest reconciliation | blocking | Build/review report |
| `document_status_unknown` | Manifest registration | blocking | Build/review report |
| `applicability_incomplete` | Runtime evidence assembly | advisory | In-band warning on a successful tool result |
| `evidence_insufficient` | Runtime valid search with no adequate support | advisory | In-band warning on a successful tool result |
| `release_validation_failed` | Release candidate gate | blocking | Release report and non-zero builder exit |
| `request_cancelled` | Runtime honored MCP cancellation | blocking | Non-response runtime event and cancellation metric; no tool result is emitted |
| `request_deadline_exceeded` | Runtime server-enforced overall tool-call deadline | blocking | Exactly one `isError: true` tool result; no partial or later response |

Context and conflict diagnostics use code-owned messages and closed safe details. `context_incomplete` and runtime `cross_reference_unresolved` allow only `relation_type`, stable occurrence ID, and `lineage_stage`; runtime `table_structure_anomaly` allows only stable table/row node IDs, a closed missing-component enum, and `lineage_stage`; `context_truncated` and `context_limit_exceeded` allow only `bound_name`, positive configured/observed counts, operation, and `lineage_stage`; `context_cycle_detected` allows only stable seed, node, and edge IDs plus relation type; `context_status_boundary` allows only stable seed/target document IDs, source/target status, and `lineage_stage`; and `evidence_conflict`, `conflict_unresolved`, and `conflict_review_required` allow only conflict/position/source IDs, ordered dimensions, state, precedence status, and `lineage_stage`. They never include raw reference text, comparison projections, review notes, query text, document text, paths, parser output, or exception strings.

The JSON-RPC errors for malformed requests, unknown methods, malformed/non-canonical resource URIs, and canonical `resources/read` misses are protocol-owned errors, not ClauseSift diagnostic codes. Warnings use the object contract from Section 21. Tool errors use the same stable code vocabulary plus a human-readable message and optional safe details. In addition to each tool's row-specific domain errors in Section 22, any tool call may return `request_deadline_exceeded` under the universal deadline contract above. Tests must exercise every routing-table row, distinguish the both-revision `-32602` malformed-URI route from the revision-specific canonical-miss wire codes, assert absence of an empty-content fallback, verify that honored cancellation emits no tool response, and deterministically exercise cancellation/deadline/quarantine races without a duplicate response.

The both-revision `-32000` saturation errors in Section 27 are likewise protocol-level admission results rather than tool execution results; request-count saturation is emitted before a work request acquires a Section 22 terminal state, while page-response-byte saturation wins that admitted request's terminal transition before source open or response allocation. Control frames remain processable while either budget is saturated.

---

## 32. Security and privacy

The initial deployment is local and single-user, but the following rules still apply:

- source files remain local unless the user explicitly configures an external model API;
- no document content is sent to an external service by default;
- external embedding or reranking providers must be opt-in and clearly identified;
- original document text is untrusted data and must be framed as quoted evidence, never interpreted by the server or client as instructions;
- SQL and FTS5 queries use bound parameters, and catalog identifiers never become SQL or path fragments;
- catalog-derived file paths must resolve beneath an explicit allowlist of release and originals roots after symlink resolution;
- MCP responses expose no absolute source path, workspace root, username, or temporary path; page access uses catalog-bound resource identifiers;
- parser subprocesses use the resource and network isolation defined in Section 11.1;
- release files should be treated as sensitive if they contain copyrighted or project-specific information;
- the MCP server should initially use local `stdio`, not an unauthenticated network listener.

Credentials for opt-in external providers come from environment variables, an OS credential store, or an explicitly configured secret provider. They must not appear in manifests, releases, cache keys, CLI arguments, reports, or logs. Missing credentials fail the requested external capability without falling back to a different provider.

Interactive consent for MCP tool invocation is owned and enforced by the MCP host, not by ClauseSift. The server advertises accurate read-only tool annotations, assumes that a received invocation has passed the host's consent policy, and never attempts to bypass or simulate host confirmation. Separate explicit workspace configuration is still required before any external provider may receive document or query content; host approval of a read-only tool call does not itself enable external transmission.

A future HTTP transport will require explicit authentication and authorization design.

---

## 33. Observability and reproducibility

Every build should record:

- source hashes;
- configuration;
- dependency versions;
- parser and model revisions;
- code version or Git commit;
- wall-clock build timestamps in the external operator lifecycle ledger;
- warnings and failures;
- evaluation results;
- release checksums.

Runtime logs should support debugging retrieval without storing sensitive queries by default. `log_queries` and `log_evidence_text` are separate explicit options and both default to false; enabling query logging never enables evidence logging. Runtime logs and optional query telemetry are written to an operator-selected state directory outside immutable releases and outside `knowledge.sqlite`; release directories remain read-only. Logs use structured event types, redact paths and credentials before dispatch to any sink, and normally record only release ID, retrieval mode, stage timings, warning codes, and request correlation ID. Credentials and absolute/internal paths are never loggable even when either content option is enabled.

Audit history has two explicitly bounded chains so an immutable release never claims to contain events that occur after it is sealed. The embedded build ledger is append-only, sequence-numbered, and hash-chained through completion of step 21, but contains only deterministic event data, `build_content_id`, phase sequence numbers, artifact hashes, and the explicit reproducible build epoch—never a random run ID or wall-clock observation. It is then sealed as `build-ledger.jsonl`, and its terminal hash is recorded in the release manifest. A separate operator lifecycle ledger outside the release directory records an operational run ID, actual build start/finish and failures, candidate assembly, manifest/checksum validation, smoke-test outcome, publication, active-pointer switch, rollback, and recovery with wall-clock times. That external chain begins with the operational run ID; when available it anchors `build_content_id`, after step 21 it anchors the terminal build-ledger hash, and after assembly it anchors `release_id` and the complete manifest digest. Every later entry links to its predecessor. Build, assembly, or activation failure can therefore be recorded without mutating candidate bytes, and “terminal” always names a declared chain cutoff rather than future events. Runtime diagnostic and optional query logs are not presented as either audit chain and need not share their retention policy.

---

## 34. Testing strategy

### 34.1 Unit tests

- manifest validation, including canonical `sha256:<64-lowercase-hex>` form, rejection of placeholders that do not match the selected source, semantic approval invalidation on canonical-content or source change, acceptance plus provenance logging of raw comment, whitespace, encoding, or key-order-only changes, and exact acceptance of the closed `active`, `superseded`, and `withdrawn` status enum with `document_status_unknown` for every other token;
- canonical model validation;
- text normalization;
- clause-number parsing, normalization, nullable non-addressable semantics, and rejection of duplicate exact-addressable `(document_id, clause_number)` keys;
- every parser-validation heuristic listed in Section 11.3, including deterministic primary selection for a passing below-threshold disagreement, a standard document with enabled comparison mode using the same ordered-role and blocking-gate contract, and cache invalidation when parser roles change;
- citation generation;
- query token detection;
- rank fusion;
- every Section 19 context profile and rule-table row, including inclusive context levels; required-first queue ordering; required recursion versus direct supporting/diagnostic stops; required empty arrays for false `get_context` flags and true flags with no matching relation; a multi-node seed whose every member contributes; deterministic target-cover materialization; duplicate-source/multiple-path preservation; exact path, item, step, and depth boundaries; allowed-cycle suppression; optional truncation; required-limit error; unresolved-required incompleteness; and status/edition isolation;
- Evidence Lineage schema closure and canonical ordering: exact source/manifest hashes and sizes, ordered multi-node and multi-page byte spans, coordinate-status derivation, selected parser roles and transformation hashes, chunk/source ownership, retrieval-artifact references, direct versus expanded selection roles, and unique independent context paths; reject missing or unknown fields, wrong ownership, a nonexistent artifact/edge/occurrence, unresolved-target traversal, duplicate paths, a direct-only item with a path, or a context-only item without one;
- exact clause lookup returning every covering chunk by the recomputed dense persisted order across independently chunked subclauses, overlapping whole-table and row representations, semantic boundaries, and token-limit splits without aggregating source IDs, including an empty structural clause root covered solely by descendant chunks and rejection of a candidate chunk containing any retrievable out-of-subtree member or members from two independently addressable branches;
- rejection of duplicate source mappings, release-admitted chunks with no source, invalid/escaping source locators or mismatched source sizes, null or empty chunk `original_text`, incorrect deepest-common-ancestor citation nodes, invalid member spans or ordering, reconstructed-text mismatches, missing, overlapping, duplicate, gapped, out-of-order, or out-of-range node-page mappings, stored source spans or bounding boxes that differ from the authoritative mapping projection, exact-lookup clauses with no chunk, and retrievable clause-subtree nodes with missing-prefix, interior-gap, or missing-suffix byte coverage;
- cross-reference resolution for same-document, exact-edition, manifest-override, unqualified-unique, and two-edition-ambiguous cases, including rejection of an existing but semantically wrong target node, code, edition, or document-root target; resolved rows compare parsed code and edition with joined targets, while unresolved rows retain parsed evidence with null target IDs/projections and perform no joined-field equality check;
- every Section 20 relationship direction, endpoint category, origin, cross-document rule, semantic identity, and cycle policy; fixtures cover duplicate occurrences preserved behind one runtime edge, explicit multi-target citations split into individual edges, ambiguous candidates producing no edge, allowed bounded reference/dependency cycles, forbidden structural/governing cycles, and unknown relation types failing release validation;
- every Section 20.3 candidate/state/dimension/explanation/precedence rule using exact unit conversions and modality-set intersections; fixtures cover compatible stricter minima/maxima, empty intersections, unit equivalence, exception, amendment, supersession, disjoint and missing jurisdiction/effective interval/equipment class, mandatory-versus-guidance/manufacturer types, two- and three-position records, and natural-language candidates that remain unresolved without immutable review;
- conflict catalog invariants and independent release recomputation: stable candidate/position IDs, dense dimensions/positions/spans, UTF-8 ownership, complete source cover, exact comparison projections, potential-state rejection, decision/review hash binding, controlling-position membership, model-only-confirmation rejection, standard-only unresolved admission, critical unresolved blocking, and changed source/rule/review invalidation;
- global identifier scope, ownership-preserving composite foreign keys, rejection of cross-document source/chunk and source-node/document pairs, and registration/generation/schema/release rejection of every public catalog ID outside the exact 1-128-character opaque-ID grammar;
- exact-maximum and one-over 128-Unicode-scalar values, including multibyte values, for persisted document codes, editions, non-null clause numbers, jurisdictions, and disciplines at registration or parser validation, schema insertion, cache import, and the independent release gate; null clause numbers remain valid, maximum values round-trip through search, exact lookup, clause-resource parsing, output validation, and cursor resume, while over-limit values publish no derived artifact or active release;
- connection-factory enforcement and readback of `PRAGMA foreign_keys = ON`, runtime `query_only`, zero-row builder/runtime `foreign_key_check`, and rejection of a deliberately injected ownership violation created through an external enforcement-disabled fixture connection;
- one-root node-tree reachability and acyclicity, parent-before-child ordering, reciprocal immediate previous/next links, and rejection of self-parent, multi-node parent-cycle, disconnected-node, and cyclic chunk-parent fixtures;
- target-node/document consistency and every `resolution_status` constraint;
- tier-specific cross-reference severity and release-gate selection;
- per-artifact cache-key dependency selection, semantic manifest invalidation without raw-format over-invalidation, parser-neutral/report/canonical/page-provenance/chunk cache layering, adapter-provenance invalidation even when output bytes match, same-source manifests with different document identity never colliding, page-mapper invalidation, parser-role and comparison-configuration invalidation, and resolver-relevant target-catalogue invalidation without unrelated-document churn;
- release checksum verification;
- lineage release validation, including one record per catalog source; complete admitted-artifact references; deterministic invalidation for a changed source, manifest, parser route, transformation, index, schema, or assembly input; byte-identical reuse for unchanged inputs; and rejection of a missing, extra, truncated, unknown-version, checksum-invalid, or catalog-inconsistent `lineage.json`;
- identifier and path-containment validation;
- central response-field and diagnostic-detail allowlists, including path injection as an extra field and inside allowed structured and legacy string fields;
- every Section 31 routing-table row and cancellation outcome;
- exact-maximum and one-over query, identifier, cursor, filter-list, total-filter, source-page-count, page-number, inbound-frame, I-JSON safe-integer, and RFC 8785 aggregate-argument bounds, including escaped lone-surrogate, worst-case multibyte cursor payload, emitted-cursor round trip, and out-of-interoperable-range integer fixtures, with every rejection routed before retrieval or model loading;
- human-grader reliability for ordinary label distributions, a unanimous single-category release sample that passes only through exact agreement plus a non-degenerate passing calibration set, and blocking degenerate-calibration or below-threshold cases;

### 34.2 Integration tests

- parser adapter to canonical model;
- adversarial parser-isolation fixtures that attempt network access; reads outside the selected source/runtime/assets allowlist; writes outside the dedicated temporary directory; and CPU, memory, wall-time, output-file-size, and page-count overruns, with isolation-setup failure blocking before adapter execution;
- mandatory independent dual-parser execution for a critical document, including injected parser failure and clause, table, and page-mapping disagreements that finalize and retain the complete diagnostic parser-validation report before blocking, promote no failed report and construct or cache no canonical artifact, and leave the active release unchanged, plus a passing below-threshold difference that byte-for-byte promotes its report, selects the configured primary parser artifact, and produces byte-identical canonical output on rebuild;
- end-to-end build of a public sample document;
- end-to-end Evidence Lineage for one multi-channel direct result and one context-only result, including OCR and no-OCR documents, complete and page-only coordinates, an admitted below-threshold parser comparison, a chunk spanning several node/page mappings, several independent paths to one target, and an unresolved or absent target that emits a warning but never a navigable path;
- deterministic traversal fixtures for scope plus multiple exceptions, definition dependency and governing scope, table row plus title/headers/units/clause, informative note plus affected parent, a required dependency chain, a cyclic reference, ordinary versus required cross-reference, superseded seed, explicit version comparison, same clause number in two editions, overlapping closures from several seeds, and each exact-at/one-over traversal bound; identical release/query/mode must produce byte-identical source order, classes, paths, completeness, and warnings;
- end-to-end conflict fixed-point closure where only the lowest-ranked side of a confirmed three-position conflict is a direct hit: all positions and each position's required context must appear once with exact spans/lineage/reasons, filters must affect only seeds, warnings and conflict ordering must be byte-identical, no winner may appear without encoded precedence, and exact-at/one-over conflict/position/span/reason/byte bounds must return a complete success or one `context_limit_exceeded` error without a one-sided package;
- parser comparison disagreements in numeric tables that block before canonicalization and never become competing source positions, plus an admitted below-threshold difference that remains parser uncertainty rather than a confirmed source conflict;
- a deliberately invalid catalog that fails at step 13 and invokes or caches no embedding, lexical-index, or vector-index builder while leaving the active release unchanged;
- an evaluation metric failure and an evaluation-execution failure that each finalize a report bound to the deterministic `build_content_id` and raw-result hash or failure record before step 20 blocks, while any operational run ID remains external and the active release remains unchanged;
- byte-stable `knowledge.sqlite` after the step 13 gate, with current-run results written only to the checksummed evaluation artifact and no later catalog mutation;
- SQLite catalog creation in a fresh temporary workspace and database per test;
- lexical and vector artifact loading;
- startup loading and validation of `lineage.json`, followed by strict Evidence Package serialization that cannot expose a source locator, parser temporary path, configuration body, credential, exception text, random run ID, or wall-clock timestamp;
- deterministic chunk-vector row mapping across multiple documents independent of SQLite insertion order; known scores must resolve to the intended chunk, source, and evidence under filters, while missing, duplicate, extra, shuffled, wrong-scope, wrong-row-order-version, wrong-shape, wrong-dtype, truncated, or checksum-invalid matrices are rejected and chunk identity/order/text, model/configuration, or row-order-version changes invalidate the embedding cache;
- rejection of a lazy model with a changed, missing, extra, or pickle-backed weight artifact before loader invocation; a bounded controlled admitted set must prove pending tool/resource calls race to their quarantine surfaces, a cancellation that already won keeps its non-response outcome, no work request is admitted and no success commits after the transition, workers are reaped, cooperative writers flush all committed frames, a blocked writer forces exit at the shutdown bound with redacted undelivered-frame accounting, and restart fails until rollback or repair;
- CLI search;
- MCP tool invocation;
- MCP compatibility for `2026-07-28` and `2025-11-25`, including success-schema validation versus error results with absent `structuredContent`; `resultType: "complete"` and the fixed cache hints on only the new wire path; authenticated filter/order/release-bound keyset cursors; canonical percent-encoded resource identifiers; both-revision `-32602` for malformed/non-canonical resource URIs versus revision-specific `-32602`/`-32002` canonical misses; both-revision `-32000` request-count or response-byte-budget saturation without source open/response allocation while cancellation/control frames still progress; every resource's exact one-item text/blob/MIME/hash success contract; `-32603` external-original integrity failures with required `code`, `phase`, and `severity`; no empty-content fallback; and barrier-controlled completion-first, deadline-first, cancellation-first, quarantine-first, and equal-timestamp races without duplicate responses or wall-clock sleeps;
- page-resource boundary tests covering exact-max and one-byte-over release admission; concurrent `source_size + 1 + response_size` reservations that cannot exceed the process byte budget; pathname replacement between availability check and open; pathname replacement after open; in-place truncate, append, and same-size mutation during read; handle identity/metadata changes; and proof that only the exact buffered bytes are hashed, encoded, and emitted or else a complete `-32603` error is returned;
- indexed query plans for exact clause, jurisdiction, discipline, status, and document-type filters;
- a target-edition catalogue change that invalidates cross-references and release assembly while an unrelated parse cache remains valid;
- a standard document with an unresolved reference that ships only with an advisory and no target IDs, contrasted with a critical document whose same unresolved status blocks publication;
- candidate-release smoke tests before the active-pointer switch;
- crash injection before temporary-file flush, immediately before replacement, after replacement but before the parent-directory flush, and after that flush; recovery must yield the complete old or new `active.json` before the final flush, must yield the new record after it, and must never expose a missing or torn record. Concurrent readers prove the same old-or-new property, and rollback passes the identical suite;
- injected build and validation failures proving the active release is unchanged;
- build-ledger sealing at the step 21 cutoff and external operator-lifecycle-ledger chaining for candidate validation, publication, pointer-switch failure, and rollback without modifying sealed release bytes;
- byte-identical release artifacts, deterministic `build_content_id`, and identical `release_id` across separate operational runs with the same explicit reproducible build epoch; a changed admitted artifact, assembly input, display label, or epoch must change `release_id`, while random run IDs and wall-clock timestamps appear only in external ledger events;
- lineage continuity when an identical source filename is replaced with different bytes, indexes are regenerated with changed or byte-identical inputs, and the active pointer rolls forward and back; every Evidence Package must use only the source, lineage, catalog, and retrieval artifacts from its single active release;
- adversarial static-report rendering with HTML, SVG, URL, CSS, and script sentinels in every untrusted field, verifying inert display, the restrictive offline CSP, and zero external requests;
- OS-read-only release operation and query logging that leaves every release byte unchanged;
- log-sink tests injecting credential, absolute-path, query, evidence-text, and client-controlled JSON-RPC-ID sentinels through successes, failures, saturation, and blocked quarantine flushes, proving credentials, paths, and client IDs never appear in any sink; query/evidence text is absent by default, explicit opt-in affects only its documented fields, undelivered frames use only server-generated correlation IDs, and redaction occurs before every configured sink;

### 34.3 Regression tests

- golden question retrieval;
- parser snapshots for representative documents;
- expected clause trees;
- expected table structures;
- citation, Evidence Lineage, uncertainty, and warning outputs, including `source_coordinate_incomplete`, `ocr_low_confidence`, and `parser_comparison_difference` propagation and deterministic top-level deduplication;
- confirmed, explained, unresolved, three-position, encoded-precedence, and no-precedence conflict outputs; hard negatives cover exceptions, compatible modalities, equal convertible units, amendments, supersession, and disjoint applicability, while all runtime material sides and exact lineage must survive adverse retrieval ranks;
- protocol error, tool execution error, empty-evidence success, and path-redaction outputs;

### 34.4 Packaging tests

- build wheel and source distribution;
- install base package in a clean environment;
- install optional dependency groups;
- execute CLI entry point;
- start MCP server;
- confirm the base runtime does not import build-only dependencies.

---

## 35. Initial implementation phases

### Phase 0: Evaluation corpus

- select 5-10 representative documents;
- include text PDFs, scans, complex tables, guidelines, specifications, and two editions of one standard;
- create an exploratory seed of 30-50 real questions with expected evidence, then expand it according to the release-gate sampling plan in Section 29.4.

### Phase 1: Parser benchmark

- implement parser adapters;
- compare structure, page mapping, tables, OCR, build time, and review cost;
- select default and fallback parser paths.

### Phase 2: Exact retrieval MVP

- implement manifests;
- canonical model;
- standards-aware chunker;
- SQLite catalog;
- clause lookup;
- lexical retrieval;
- deterministic citations;
- basic CLI and MCP tools;
- static review report;
- immutable release;
- candidate-release validation, atomic activation, and rollback tests.

### Phase 3: Hybrid retrieval

- benchmark embedding models;
- build memory-mapped exact vector search;
- add reciprocal-rank fusion;
- add query classification;
- expand regression evaluation.

### Phase 4: High-accuracy retrieval

- add cross-encoder reranking;
- add deterministic Evidence Graph context traversal;
- improve tables and cross-references;
- add typed warnings and refusal support.

### Phase 5: Version and product intelligence

- edition comparison;
- clause mapping across editions;
- structured product parameters;
- comparison of standard requirements and manufacturer specifications.

---

## 36. First release acceptance criteria

The first usable MVP must:

- install as a Python package;
- initialise a local workspace;
- ingest selected PDFs;
- validate manifests and source hashes;
- reject unsafe YAML tags, unapproved manifest changes, invalid catalog relationships, and path escapes;
- preserve document, edition, clause, page, and source identity;
- perform exact clause lookup;
- perform lexical search with metadata filters;
- return original evidence text and deterministic citations;
- retrieve relevant parent and adjacent context;
- expose core functionality through CLI and MCP;
- pass protocol compatibility, structured-output, typed-error, pagination, and cancellation tests;
- generate static parser/chunk review reports;
- build an immutable release;
- verify every runtime artifact before opening it and reject unsafe NumPy arrays;
- retain and roll back to a previous release;
- pass the golden retrieval test suite and all configured release gates with sample counts and confidence intervals reported.

Semantic retrieval is not required for the earliest exact-retrieval milestone, but the architecture must support it without changing the canonical evidence model.

---

## 37. Open decisions

### 37.1 Benchmark- or prototype-dependent technical decisions

1. Default parser and parser-routing rules.
2. OCR fallback behavior.
3. Lexical search engine.
4. Chinese tokenisation strategy.
5. Embedding model and vector dimensions.
6. Reranker model.
7. Exact vector implementation: NumPy versus FAISS.
8. Release-pointer implementation across operating systems.
9. Bounding-box representation and page-image format.
10. Evidence-based thresholds for parser quarantine and release failure.

These choices should be evaluated in the following order:

1. Does it improve or preserve accuracy?
2. Does it improve speed after accuracy is acceptable?
3. Is its packaging and maintenance burden justified?

### 37.2 Governance, legal, and support-policy decisions

1. Licensing constraints for OCR, parser, model, and index dependencies.
2. Rights-cleared public sample documents suitable for automated tests.
3. Minimum supported Python version and support window.
4. Project software licence and distribution obligations.

Each item in this group requires an identified owner, a decision record, and the appropriate legal, governance, or maintenance review; benchmark results may inform but cannot decide it alone.

---

## 38. Architectural decision summary

ClauseSift v0.1 is based on the following decisions:

- build a specialised engineering evidence-retrieval engine, not a general chat platform;
- prioritise accuracy first and speed second;
- compile stable document corpora offline;
- keep runtime read-only and lightweight;
- use SQLite as the authoritative structured catalog;
- retain lexical retrieval as a mandatory first-class channel;
- use exact dense retrieval before approximate indexing;
- use reranking for high-accuracy queries;
- preserve parent scope, exceptions, notes, tables, and references;
- generate deterministic citations and page mappings;
- expose a shared runtime through Python, CLI, and MCP;
- target MCP `2026-07-28` with tested dual-era compatibility for `2025-11-25` clients;
- publish immutable and reproducible knowledge-base releases;
- verify catalog-bound inputs and every runtime artifact before use;
- validate all major component choices against a project-specific golden corpus.

The defining product output is not a fluent answer. It is a defensible evidence package containing the correct source, correct edition, correct clause, complete applicability context, and a path back to the original page.
