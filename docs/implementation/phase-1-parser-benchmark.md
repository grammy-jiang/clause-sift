# Phase 1 Implementation Plan: Parser Benchmark

**Project:** ClauseSift  
**Phase:** 1 of the design-defined implementation sequence  
**Status:** Implementation plan  
**Primary design authority:** `docs/design.md`  
**Phase objective:** Implement isolated parser adapters and a reproducible benchmark harness, compare parser quality across the Phase 0 corpus, and select evidence-backed primary, comparator, OCR, and fallback routing choices without implementing the Phase 2 canonical model or retrieval stack.

## 1. Purpose

Phase 1 determines how ClauseSift should extract engineering evidence from difficult technical PDFs before the project commits to a production parser route.

The design explicitly assumes that no parser is best for every document. ClauseSift therefore needs measured evidence for parser selection across native-text standards, scans, complex tables, guidelines, manufacturer documentation, and multiple editions. This phase creates that evidence.

The output of Phase 1 is not a production knowledge-base release. It is a versioned parser benchmark and routing decision package that Phase 2 can adopt when it implements production manifests, the canonical document model, chunking, catalog persistence, exact retrieval, citations, and immutable releases.

Phase 1 must answer the following questions with reproducible measurements:

1. Which parser implementation should be the default `canonical_primary` path for each supported document class or deterministic routing rule?
2. Which independent parser implementation should act as the comparator when comparison mode is required?
3. Which parser/OCR path is appropriate for scanned or difficult documents?
4. Which alternative parser paths are useful as **configured routing alternatives** for other document classes, without creating a silent fail-open fallback after a parser failure?
5. Which parser disagreements must block later canonicalization?
6. Which below-threshold differences may be admitted while remaining visible as parser uncertainty?
7. What review burden does each parser path impose on an engineer?
8. Are the selected outputs deterministic enough to become stable inputs to Phase 2?

## 2. Phase boundary

Phase 1 is deliberately narrow.

### 2.1 In scope

This phase implements and validates:

- parser adapter interfaces;
- parser-neutral intermediate-output schemas;
- isolated parser subprocess execution;
- candidate parser integrations used only for benchmarking;
- OCR-path benchmarking;
- deterministic source-characterisation for benchmark grouping;
- single-parser validation heuristics required by the design;
- independent dual-parser comparison;
- parser comparison reports;
- structural, page, coordinate, table, OCR, text, and reading-order evaluation;
- parser runtime/build-time measurements;
- human review-cost measurement;
- deterministic/reproducibility checks;
- benchmark-only parser routing configurations;
- evidence-backed parser selection and decision records;
- the Phase 1 handoff contract for Phase 2.

### 2.2 Out of scope

Phase 1 must **not** implement:

- the production manifest schema or approval workflow;
- canonical document-model construction;
- production classification/inheritance admission into canonical nodes;
- production Evidence Graph nodes or edges;
- standards-aware chunking;
- SQLite `knowledge.sqlite` catalog construction;
- lexical or semantic retrieval;
- deterministic public citations;
- Python/CLI/MCP retrieval APIs;
- production static parser/chunk review reports defined for the later builder;
- immutable release assembly, activation, or rollback;
- embeddings, vector indexes, rank fusion, or reranking;
- runtime context traversal or conflict closure.

When Phase 1 needs metadata that is not yet represented by a production manifest, it uses Phase 0 corpus identity and **benchmark-only configuration**. It must not quietly create a second production manifest model.

## 3. Governing design constraints

The implementation must preserve these design decisions.

1. Accuracy is the first priority. Build time and operational cost are secondary.
2. No parser is assumed to be universally best before measurement.
3. Original source bytes remain authoritative.
4. Parser output is untrusted derived data.
5. Parser adapters produce a parser-neutral intermediate representation rather than parser-native objects leaking into later modules.
6. Parser adapters run in isolated subprocesses with no network access.
7. Isolation failure is blocking; ClauseSift never falls back to unisolated execution.
8. Parser failures, timeouts, malformed output, and resource-limit violations fail visibly.
9. Comparison mode uses two **distinct parser implementations**, not the same implementation with different options.
10. Every comparison-mode route has one ordered `canonical_primary` and one ordered `independent_comparator`.
11. The comparator is validation-only. Its fields are never merged into the primary output.
12. A blocking comparison disagreement cannot be waived by choosing the more convenient output.
13. A `release_tier: critical` production document will require comparison mode; Phase 1 must benchmark and prove a usable independent pair for this later requirement.
14. A parser route, adapter version, adapter configuration, role assignment, or comparison configuration is a deterministic build input and later cache identity component.
15. With unchanged source bytes, parser roles, adapter versions, and configurations, admitted parser-neutral output must be byte-identical across rebuilds.
16. Parser-selected classifications may preserve source labels/markers and spans, but Phase 1 does not promote parser guesses into authoritative document facts or legal conclusions.
17. A parser disagreement is parser uncertainty, not an engineering-source conflict.
18. Credentials, absolute temporary paths, raw exceptions, and unrelated corpus data must not leak into benchmark artefacts.

## 4. Prerequisite: Phase 0 handoff

Phase 1 begins only from the merged Phase 0 baseline.

The benchmark harness consumes the Phase 0 parser-benchmark pack for each selected representative document:

- `corpus_document_id`;
- immutable source SHA-256;
- source byte size;
- rights/use classification;
- verified or expected page count where available;
- source type and layout characteristics;
- representative structural landmarks;
- representative table pages;
- representative OCR-sensitive pages;
- representative page/coordinate anchors;
- known layout anomalies;
- source-grounded expected snippets/labels;
- review worksheet conventions.

Phase 1 may add parser-specific benchmark labels when required, but must not rewrite Phase 0 ground truth to make a parser pass.

If a benchmark exposes a Phase 0 label error, the correction follows Phase 0 change control and receives a new reviewed label/corpus revision before it is used as accepted ground truth.

## 5. Recommended repository layout

A practical implementation layout is:

```text
src/
└── clausesift/
    └── parsing/
        ├── __init__.py
        ├── adapter.py
        ├── model.py
        ├── isolation.py
        ├── runner.py
        ├── validation.py
        ├── comparison.py
        ├── routing.py
        └── adapters/
            ├── docling.py
            ├── pymupdf.py
            └── ocr.py

benchmark/
└── parsing/
    ├── README.md
    ├── schema/
    ├── config/
    ├── fixtures/
    ├── expected/
    ├── runs/
    ├── reports/
    └── scripts/

tests/
├── unit/
│   └── parsing/
├── integration/
│   └── parsing/
└── regression/
    └── parsing/
```

The exact package path may be aligned with the Phase 2 package bootstrap when implementation starts. The architectural separation is more important than the literal names:

- reusable parser/adaptation/isolation code belongs in the package;
- benchmark-only configuration and expected labels stay outside production runtime code;
- raw private corpus sources remain outside Git unless rights-cleared;
- parser-native temporary output is never treated as a canonical project artefact.

## 6. Work package 1.1: Define the parser-neutral contract

### 6.1 Contract purpose

The parser-neutral representation is the only output shape that benchmarked parser adapters expose to the comparison and validation harness.

It must be rich enough to test the design requirements without prematurely implementing the Phase 2 canonical model.

### 6.2 Required top-level fields

Define a closed, versioned parser-neutral envelope containing at least:

- parser-neutral schema version;
- benchmark source identity;
- exact source SHA-256 and byte size;
- parser adapter identity;
- parser implementation identity and version;
- adapter version;
- configuration digest;
- execution role (`canonical_primary_candidate`, `independent_comparator_candidate`, or standalone benchmark role);
- page count;
- ordered page records;
- ordered block/element records;
- parser warnings;
- OCR summary;
- extraction statistics;
- deterministic content hash of the parser-neutral payload.

Operational run IDs and wall-clock observations must be kept outside deterministic parser-neutral content identity.

### 6.3 Page records

A page record should expose, where the parser can provide it:

- one-based source page number;
- source page label if separately available;
- page width and height;
- declared coordinate system and units;
- rotation/orientation;
- ordered block IDs;
- page text reconstructed from the adapter output;
- OCR-used flag;
- page-level OCR confidence summary;
- adapter warnings.

Page records do not invent bounding boxes when the parser does not supply them.

### 6.4 Block/element records

The neutral model must be able to represent, where available:

- heading;
- paragraph;
- list/list item;
- table;
- table row;
- table cell;
- figure;
- caption;
- footnote;
- generic/unclassified block.

Each source-bearing element records:

- stable deterministic benchmark element ID derived from parser-neutral inputs;
- page number;
- reading-order position;
- original extracted text;
- optional bounding box;
- optional parent parser-neutral element;
- parser-native type preserved only as non-authoritative diagnostic metadata;
- exact source labels/markers and spans relevant to structural type, normative status, or modality when the parser exposes them;
- OCR status/confidence where applicable;
- warnings.

The neutral model must not translate parser-native categories directly into Phase 2 canonical vocabulary values unless a deterministic benchmark adapter rule is explicitly under test. Parser-native aliases remain parser evidence, not canonical authority.

### 6.5 Heading and hierarchy representation

Represent detected hierarchy without assuming it is correct:

- heading text;
- source marker/number where parsed;
- claimed level/depth;
- parent heading/block reference;
- source page;
- coordinate;
- reading order.

The validation harness compares this structure with Phase 0 expected landmarks and parser-to-parser output.

### 6.6 Table representation

The parser-neutral table structure must preserve:

- table page(s);
- title/caption when detected;
- row count;
- column count;
- cell coordinates;
- row/column spans;
- cell text;
- header designation;
- units when explicitly captured;
- footnotes when linked;
- continuation/merged-table metadata when the adapter can provide it;
- bounding boxes;
- confidence/warnings.

Do not silently flatten a table into prose and still report table extraction as successful.

### 6.7 OCR representation

OCR output must expose:

- whether OCR was invoked;
- OCR engine identity/version;
- model/language-pack/configuration digest;
- page/block confidence where supported;
- original OCR text;
- coordinate output where supported;
- warnings;
- explicit `confidence_unavailable` rather than invented confidence when the engine does not provide one.

### 6.8 Serialization

Use a deterministic, schema-validated serialization suitable for byte-for-byte comparison and hashing.

Requirements:

- UTF-8;
- closed schema;
- deterministic ordering;
- no absolute paths;
- no credentials;
- no parser temporary filenames unless reduced to safe, deterministic role identifiers;
- no raw exception object serialization;
- finite numeric values only;
- explicit nulls when a field is defined but unavailable;
- stable representation of bounding boxes and dimensions.

## 7. Work package 1.2: Define the parser adapter interface

### 7.1 Adapter responsibilities

Each adapter must:

1. accept exactly one selected source plus declared configuration/assets;
2. run through the common isolated execution boundary;
3. invoke one parser implementation;
4. translate parser-native output into the parser-neutral schema;
5. emit sanitized warnings/failure records;
6. publish no canonical model or retrieval artefact;
7. expose exact adapter/parser/configuration identity for reproducibility.

### 7.2 Adapter protocol

Define a small internal adapter protocol such as:

```text
prepare(config, assets) -> PreparedAdapter
parse(source_handle, limits) -> ParserNeutralResult
identity() -> AdapterIdentity
```

The exact Python API may differ, but the contract must separate:

- adapter identity;
- parser implementation identity;
- parser configuration;
- external model assets;
- execution limits;
- parser-neutral output.

### 7.3 No parser-native leakage

Comparison, validation, reporting, and routing-selection code must consume the parser-neutral contract, not `DoclingDocument`, PyMuPDF page objects, MinerU-specific structures, or another parser's private classes.

Parser-native objects may exist only inside the adapter subprocess and temporary adapter translation layer.

### 7.4 Failure contract

All adapter failures become typed, sanitized benchmark failures such as:

- isolation setup failed;
- parser process failed;
- timeout;
- memory limit;
- CPU limit;
- output-size limit;
- page-count limit;
- malformed parser-native output;
- parser-neutral schema validation failed;
- missing declared local asset;
- unexpected network attempt;
- forbidden filesystem access.

Do not preserve arbitrary exception text in durable reports when it may contain paths or credentials.

## 8. Work package 1.3: Implement parser-process isolation

### 8.1 Isolation requirements

Every parser adapter execution must run in a dedicated subprocess or stronger isolation boundary with:

- no network access;
- a dedicated temporary directory;
- read-only access only to the selected source;
- read-only access to the pinned parser executable/runtime libraries required by that adapter;
- read-only access to explicitly declared local parser/OCR model assets;
- no read access to the remaining corpus;
- no read access to repository credentials or operator state;
- no write access outside the dedicated temporary directory;
- explicit CPU limit;
- explicit memory limit;
- explicit wall-time limit;
- explicit output-file-size limit;
- explicit source/page-count limit.

### 8.2 Fail closed

If any requested isolation mechanism cannot be established or verified on the current platform, the adapter execution returns a blocking `parser_failed` benchmark result and does not launch the parser unisolated.

### 8.3 Cross-platform isolation abstraction

Define the isolation interface independently of one operating system. The initial implementation may support the project's primary development/CI platform first, but the benchmark report must state exactly which controls are enforced and which platforms are unsupported.

Do not claim equivalent security on a platform whose controls have not been tested.

### 8.4 Adversarial isolation fixtures

Implement test adapters/fixtures that deliberately attempt:

- outbound network access;
- DNS/network socket creation;
- reading another corpus file;
- reading the repository root;
- reading environment/credential files;
- following a symlink outside the source/asset allowlist;
- writing outside the temporary directory;
- creating excessive output;
- consuming excessive memory;
- consuming excessive CPU;
- exceeding wall time;
- reporting more pages than allowed.

Each attempt must be blocked or terminate the adapter before its output is admitted.

## 9. Work package 1.4: Candidate adapter implementations

### 9.1 Candidate set from the design

The initial benchmark must include distinct implementations representing the design's candidate paths:

- a Docling adapter for structured technical PDFs;
- a PyMuPDF-based adapter for deterministic page text and coordinate extraction/comparison;
- an OCR-oriented adapter using MinerU or another explicitly selected OCR implementation for scanned/difficult documents.

Candidate products are benchmark subjects, not permanent architecture commitments.

### 9.2 Version pinning

For each benchmark run record:

- exact package/application version;
- exact adapter version;
- Python/runtime version;
- platform/architecture;
- relevant parser configuration;
- local model/language-pack asset digests;
- optional acceleration/backend configuration.

Never report only a product name such as “Docling” without the tested version/configuration.

### 9.3 Distinct implementation rule

Two adapters backed by the same parser implementation do not satisfy the independent dual-parser comparison rule, even if their options differ.

The benchmark metadata must identify `implementation_family` so the harness can reject an invalid primary/comparator pair.

### 9.4 Optional additional candidates

An implementation agent may benchmark an additional parser when there is a documented Phase 1 reason, for example a demonstrated failure on a Phase 0 document class.

Adding a candidate is in scope only as a parser benchmark. It must not expand Phase 1 into a general document-processing platform selection exercise.

## 10. Work package 1.5: Source characterisation for benchmark grouping

### 10.1 Purpose

Parser selection may depend on source characteristics. Phase 1 needs deterministic benchmark grouping without inventing the future production manifest or an opaque ML classifier.

### 10.2 Benchmark characteristics

Record source characteristics such as:

- native-text availability;
- extractable-character density;
- image-only page ratio;
- mixed text/image pages;
- page count;
- dominant page dimensions;
- multi-column layout;
- table density;
- complex/merged table presence;
- repeated header/footer prevalence;
- scanned/rotated pages;
- OCR requirement;
- known language(s);
- known difficult fonts/encodings;
- known forms/diagrams.

### 10.3 Source of truth

Characteristics may come from:

- Phase 0 reviewed corpus labels;
- deterministic file/page inspection;
- benchmark reviewer annotation.

They must not be silently inferred by a parser under evaluation and then used to justify that same parser's routing decision.

### 10.4 Future production routing

Phase 1 produces recommended deterministic routing predicates in terms that Phase 2 can later bind to approved manifest fields and safe source inspection.

Phase 1 does not implement the production router against production manifests.

## 11. Work package 1.6: Build the benchmark runner

### 11.1 Run identity

Separate deterministic benchmark content identity from operational run metadata.

Deterministic benchmark identity should depend on:

- source hash;
- Phase 0 label-set version;
- parser-neutral schema version;
- adapter implementation/version;
- parser implementation/version;
- parser configuration digest;
- declared model assets;
- execution role;
- validation/comparison configuration version.

Wall-clock timestamps and random operational run IDs are report metadata only.

### 11.2 Execution matrix

For every representative document:

1. execute every applicable standalone candidate;
2. validate each parser-neutral result independently;
3. execute each eligible primary/comparator pair required by the benchmark matrix;
4. compare outputs through the common comparison engine;
5. collect resource/runtime measurements;
6. collect reviewer annotations/cost;
7. generate per-document and aggregate reports.

### 11.3 Fresh-process requirement

Each parser run starts in a fresh isolated subprocess. Parser state from one document must not leak into another benchmark document.

### 11.4 Warm/cold measurements

When parser initialization/model loading materially affects build time, report separately:

- cold execution;
- warm asset-cache execution where the cache itself is an admitted local parser asset/cache;
- pure parse/translation time where measurable.

Do not hide parser/model startup behind one aggregate average.

### 11.5 Repeat runs

Execute enough repeated runs to establish:

- deterministic output stability;
- timing variability;
- absence of order-dependent output.

At minimum, every selected final candidate/configuration must be parsed multiple times from fresh processes, with source order permuted, before it can be recommended.

## 12. Work package 1.7: Single-parser validation heuristics

Implement the Section 11.3 validation checks as independent, versioned benchmark rules.

### 12.1 Page count

Compare:

- source page count;
- parser-neutral page count;
- highest emitted source page number;
- missing/duplicated page identities.

A page-count mismatch is a blocking defect for a candidate route.

### 12.2 Missing-text ratio

Define a reproducible text-coverage metric using Phase 0 reviewed expected spans/landmarks and deterministic baseline page-text extraction where appropriate.

Report:

- expected source-bearing pages;
- pages with no extracted text;
- expected labelled spans missed;
- character/token coverage statistics;
- OCR-specific coverage separately.

Do not use one parser under evaluation as the sole ground truth for another parser's missing-text metric.

### 12.3 Abnormal-character ratio

Measure extraction artefacts such as:

- replacement characters;
- impossible control characters;
- repeated encoding garbage;
- suspicious ligature/font-decoding failures;
- implausible character runs.

Keep the heuristic versioned and language-aware enough not to penalize valid Chinese or technical symbols.

### 12.4 Heading-tree consistency

Validate:

- ordering;
- impossible level jumps where source rules support that check;
- orphaned headings;
- duplicate heading identity where inappropriate;
- Phase 0 expected hierarchy landmarks;
- parser-to-parser structural differences.

### 12.5 Clause-number continuity

Measure extraction of source clause markers without assuming every document uses one numeric pattern.

The benchmark includes:

- expected exact clause identifiers from Phase 0;
- missing clause markers;
- duplicated clause markers;
- order anomalies;
- parser-generated markers not present in source evidence.

Production clause normalization remains Phase 2 scope.

### 12.6 Header/footer duplication

Detect repeated page furniture that contaminates body text or hierarchy.

Report both:

- missed removal where the parser claims body text;
- over-removal where real evidence matching repeated text is lost.

### 12.7 Cross-page paragraph continuity

Use reviewed fixtures for paragraphs/requirements split over page boundaries.

Measure whether the parser:

- preserves correct order;
- duplicates text;
- drops boundary text;
- incorrectly joins unrelated header/footer material;
- splits one logical unit in a way that loses source continuity.

Do not require Phase 1 to construct the final canonical paragraph node.

### 12.8 Table-shape consistency

Validate:

- dimensions;
- headers;
- units;
- row/column spans;
- cell text;
- continuation tables;
- ordering;
- table title/caption;
- footnotes where applicable.

### 12.9 Page-coordinate completeness

Measure:

- percentage of expected source-bearing elements with page mapping;
- percentage with bounding boxes;
- invalid/out-of-page boxes;
- coordinate-system inconsistencies;
- wrong-page mappings;
- box-to-source anchor mismatch on reviewed fixtures.

A parser that has excellent text but unreliable page mapping cannot be treated as equally suitable for deterministic citation provenance.

## 13. Work package 1.8: Structural benchmark

### 13.1 Structural metrics

For every candidate, measure:

- document-order fidelity;
- heading recall/precision against reviewed landmarks;
- hierarchy fidelity;
- clause-marker recall/precision;
- paragraph/list segmentation quality;
- exception/note marker preservation;
- footnote preservation;
- figure/caption association where relevant;
- table detection recall/precision;
- page association accuracy.

### 13.2 Accuracy grading

Prefer exact source-grounded/evaluation comparisons where Phase 0 labels exist.

Use blinded human review for genuinely semantic layout questions not covered by deterministic labels.

### 13.3 No generated repair

The benchmark must score the parser output as produced. An LLM or downstream heuristic may not silently repair hierarchy before the parser is scored.

A separate deterministic adapter-normalization rule may be benchmarked only when it is declared as part of the adapter configuration and included in its identity.

## 14. Work package 1.9: Page and coordinate benchmark

### 14.1 Coordinate fixtures

Use Phase 0 reviewed page/coordinate anchors spanning:

- ordinary paragraphs;
- clause headings;
- multi-column text;
- table cells;
- footnotes;
- page boundary text;
- scanned/OCR pages;
- rotated pages where available.

### 14.2 Coordinate normalization

The parser-neutral adapter must convert parser-specific coordinates into one declared benchmark coordinate convention without changing source location semantics.

Record the original parser coordinate convention in adapter metadata.

### 14.3 Accuracy measurements

Measure:

- correct page;
- box presence;
- box containment/overlap with reviewed anchors;
- coordinate bounds validity;
- reading-order consistency with coordinates;
- multi-page element handling.

### 14.4 Missing coordinates

Missing optional boxes are recorded as missing. Do not generate estimated boxes to improve the benchmark score.

## 15. Work package 1.10: Table benchmark

### 15.1 Table corpus

Create a table subset from the Phase 0 representative documents containing:

- simple rectangular tables;
- merged cells;
- multi-row headers;
- units in headers;
- units in cells;
- footnotes;
- multi-page tables;
- repeated continuation headers;
- blank cells;
- numeric thresholds;
- symbols and technical abbreviations.

### 15.2 Required measurements

For each table compare:

- table detection;
- row/column count;
- cell grid;
- row/column spans;
- header assignment;
- title/caption;
- units;
- cell text;
- numeric value integrity;
- page mapping;
- bounding boxes;
- continuation handling;
- footnote association.

### 15.3 Blocking table disagreement for comparison mode

The comparison engine must be able to mark as blocking when the two selected parser implementations disagree materially on:

- dimensions;
- headers;
- units;
- cell values;
- table presence;
- relevant page mapping.

### 15.4 Numeric integrity

Numerical table cells deserve explicit checks for:

- lost decimal points;
- sign changes;
- digit substitutions;
- merged adjacent values;
- dropped superscripts;
- unit separation;
- OCR digit/letter confusion.

A parser with a visually plausible table but altered engineering values fails the accuracy-first requirement.

## 16. Work package 1.11: OCR benchmark

### 16.1 OCR subset

Use the Phase 0 scanned/difficult source subset and deliberately include:

- clean scans;
- low-resolution pages if available;
- skew/rotation;
- technical symbols;
- tables;
- small footnotes;
- page furniture;
- mixed scan/native-text pages where available.

### 16.2 OCR measurements

Report:

- text coverage;
- character/word error on reviewed spans where practical;
- exact identifier preservation;
- clause-number preservation;
- numeric/unit integrity;
- table integrity;
- reading order;
- page mapping;
- bounding-box coverage;
- confidence availability;
- confidence calibration observations;
- manual review burden.

### 16.3 OCR fallback meaning

A selected OCR path is a **routing path for documents identified as requiring OCR**, not a fail-open action invoked after an unrelated primary parser crashes.

The later production router must select the OCR path deterministically before parsing based on approved configuration/source characteristics.

### 16.4 Low confidence

Phase 1 determines evidence-based candidate thresholds or review bands for OCR confidence where the selected engine exposes a meaningful confidence value.

It does not invent a universal confidence threshold without benchmark evidence.

## 17. Work package 1.12: Independent dual-parser comparison engine

### 17.1 Preconditions

The comparison engine rejects a pair unless:

- both parser-neutral outputs bind to identical source hash/size;
- implementations are from distinct implementation families;
- roles are explicitly ordered;
- schemas are supported;
- both standalone validations have completed;
- comparison configuration is versioned.

### 17.2 Blocking conditions

For a comparison-mode benchmark document, treat the following as blocking exactly as required by the design:

- either adapter fails;
- source/parser page-count mismatch;
- parser-to-parser page-count mismatch;
- normative clause present in only one output;
- exception present in only one output;
- table present in only one output;
- source role/modality marker present in only one output where benchmark ground truth requires comparison;
- page mapping present/correct in only one output for material evidence;
- clause identity mismatch;
- clause ordering mismatch;
- material evidence-vocabulary classification disagreement where Phase 1 is explicitly testing preserved source markers/provisional deterministic adapter projection;
- table dimension mismatch;
- header mismatch;
- unit mismatch;
- cell-value mismatch;
- any versioned comparison metric over its admitted threshold.

### 17.3 Below-threshold differences

A comparison may pass with a non-zero difference only when:

- the difference is below a versioned admitted threshold;
- it is not one of the unconditional blocking categories above;
- the exact difference is retained in the report;
- the report marks `parser_comparison_difference`;
- the primary output remains unchanged;
- no field-level merge occurs.

### 17.4 Primary selection

After both standalone gates and the comparison gate pass, the selected `canonical_primary` candidate parser-neutral artefact is the sole downstream candidate.

The comparator never contributes replacement text, missing cells, corrected coordinates, or majority-vote fields.

### 17.5 No waiver

A failed comparison produces no “pick primary anyway” option in Phase 1 decision logic.

The benchmark may test another **predeclared candidate pair** in a separate run, but cannot reinterpret a failed pair as passing.

## 18. Work package 1.13: Parser-validation report

### 18.1 Report purpose

Create a durable Phase 1 benchmark report format that exercises the information required by the future builder's parser-validation report without implementing Phase 2 release assembly.

### 18.2 Required contents

For each run/pair include:

- safe source/corpus identity;
- source hash/size;
- parser-neutral schema version;
- primary adapter identity/version/configuration;
- comparator identity/version/configuration when present;
- roles;
- isolation configuration/results;
- standalone validation results;
- parser-neutral output hashes;
- comparison configuration;
- every comparison metric;
- every disagreement;
- OCR status/confidence summary;
- resource/time measurements;
- deterministic pass/fail decision;
- advisory differences;
- review-cost data;
- benchmark label-set version.

### 18.3 Failure reports

When an adapter fails, finalize the diagnostic report with a sanitized failure record in place of its missing output.

The report must remain available for review even though no output is admitted.

### 18.4 Safe report content

Reports must not expose:

- credentials;
- unrestricted environment variables;
- absolute private source paths;
- parser temporary paths;
- raw exception traces containing sensitive paths;
- unrelated document text.

Source excerpts used for private local review remain governed by Phase 0 rights handling and are not automatically committed.

## 19. Work package 1.14: Benchmark accuracy metrics

### 19.1 Metric families

Report parser quality separately by:

- page integrity;
- text integrity;
- structural integrity;
- clause/identifier integrity;
- table integrity;
- OCR integrity;
- coordinate/page-mapping integrity;
- source-marker/modality-marker preservation;
- warning/error rate;
- reproducibility.

Do not collapse these into one opaque parser score as the sole decision criterion.

### 19.2 Critical-error counts

Track zero-tolerance defects separately, including:

- wrong page count;
- missing labelled normative clause;
- changed numeric engineering value;
- wrong edition/source mix;
- wrong page mapping for labelled evidence;
- lost exception;
- materially wrong table header/unit;
- nondeterministic output bytes for an unchanged admitted route;
- unsafe isolation behaviour.

### 19.3 Reviewable weighted summaries

A weighted summary score may assist ranking after hard gates, but:

- weights are documented;
- accuracy-related hard failures dominate;
- weighting cannot turn a blocking defect into a passing route;
- raw metrics remain visible.

## 20. Work package 1.15: Build-time and resource benchmark

### 20.1 Measurements

For each adapter/configuration collect:

- wall time;
- CPU time where available;
- peak resident memory;
- temporary disk usage;
- output bytes;
- model/asset initialization time;
- OCR-specific time;
- pages per second as a descriptive metric;
- failure/timeout rate.

### 20.2 Reporting

Report at least:

- per-document values;
- p50/p95 where sample size supports them;
- maximum;
- cold versus warm state where relevant;
- document-class segmentation.

### 20.3 Decision priority

Performance is considered **only after** the candidate satisfies the required extraction/citation-quality gates.

A faster parser that loses exceptions, units, clauses, page mappings, or source text is not preferred.

## 21. Work package 1.16: Human review-cost benchmark

### 21.1 Why review cost matters

Phase 1 explicitly needs to compare review cost because a parser that requires extensive manual correction undermines the offline compiler's operational simplicity even if raw runtime is acceptable.

### 21.2 Review protocol

Use a fixed review worksheet over blinded parser outputs.

Record:

- time to inspect one document or selected page set;
- number of structural corrections identified;
- number of text corrections identified;
- number of table corrections identified;
- number of page/coordinate corrections identified;
- number of OCR corrections identified;
- number of uncertain issues requiring source re-check;
- reviewer confidence;
- reviewer identity and worksheet version.

### 21.3 Review sampling

Ensure the review set covers:

- ordinary pages;
- difficult pages;
- tables;
- exceptions/notes;
- scanned pages;
- versioned documents;
- cross-page content.

### 21.4 Avoid false precision

Human review cost is an operational measurement, not a universal constant. Report sample size and distribution rather than one unsupported single-minute target.

## 22. Work package 1.17: Determinism and reproducibility

### 22.1 Byte-identical output test

For every parser/configuration considered for selection:

- run the same source multiple times in fresh processes;
- randomize benchmark document execution order;
- compare parser-neutral canonical bytes;
- compare output hashes;
- compare deterministic warnings/metrics.

### 22.2 Sources of nondeterminism

Investigate and either pin/remove or explicitly reject candidate routes that depend on uncontrolled:

- random seeds;
- thread scheduling that changes reading order;
- nondeterministic OCR/model decoding;
- current time;
- temporary filenames embedded in output;
- filesystem enumeration order;
- network-fetched model/data revisions;
- mutable remote APIs.

### 22.3 External assets

All parser/OCR assets needed for a selected local route must have declared identities/digests. A benchmark using unpinned remotely changing assets cannot support a reproducible production recommendation.

### 22.4 Same output, changed provenance

If an adapter/configuration/version changes but happens to emit identical parser-neutral bytes, the benchmark still records the changed provenance as a distinct route identity. Phase 2 cache logic must later include adapter provenance, not only output hash.

## 23. Work package 1.18: Benchmark routing configuration

### 23.1 Purpose

Create a **benchmark routing configuration**, not the production manifest/router implementation.

It records which candidate route/pair is being evaluated for each corpus document or deterministic source-characteristic class.

### 23.2 Required fields

Each benchmark route records:

- route/configuration version;
- Phase 0 corpus IDs or a deterministic benchmark predicate;
- primary candidate adapter;
- comparison enabled/disabled for the benchmark case;
- comparator candidate when enabled;
- OCR path selection when applicable;
- resource-limit profile;
- validation profile;
- comparison profile;
- rationale/decision status.

### 23.3 Critical-document simulation

For Phase 0 documents marked as critical-comparison candidates, comparison is always enabled in the Phase 1 benchmark route.

This proves the independent pair before Phase 2 introduces actual production `release_tier` manifests.

### 23.4 Standard-document comparison experiments

Benchmark some ordinary documents both with and without comparison to measure whether optional production comparison would materially improve detection/review quality.

A failed comparison experiment cannot be “fixed” by silently reclassifying that same run as non-comparison.

## 24. Work package 1.19: Default, comparator, OCR, and fallback selection

### 24.1 Selection hierarchy

Evaluate candidate routes in this order:

1. blocking accuracy/integrity defects;
2. structural and source-text accuracy;
3. table and numeric integrity;
4. page/coordinate accuracy;
5. OCR quality where applicable;
6. deterministic output stability;
7. review burden;
8. build time/resource cost;
9. packaging/maintenance burden as a documented operational consideration.

### 24.2 Default path

Select a default primary parser only if the benchmark evidence shows it is appropriate for the relevant document class.

Do not make “default” mean “use it for every PDF regardless of source characteristics.”

### 24.3 Comparator path

The recommended independent comparator must:

- be a genuinely distinct parser implementation;
- provide enough independent structural/page/table evidence to detect primary errors;
- pass isolation/reproducibility tests;
- be practical enough for critical-document compilation.

It does not need to be the second-highest overall parser score if another implementation provides more useful independent disagreement detection.

### 24.4 OCR path

Select an OCR-oriented route based on scan-specific evidence. The output must still satisfy the same parser-neutral and isolation contracts.

### 24.5 Fallback path semantics

A “fallback” recommendation means a **configured alternative route selected for a known source class or operator-reviewed routing change**.

It does **not** mean:

```text
try primary
if it crashes or disagrees:
    silently try another parser and ship that output
```

Production parser failure remains visible and blocking under the design.

### 24.6 No permanent choice without evidence

When two candidates remain materially tied or the corpus does not cover a needed source class, record the decision as unresolved and define the additional benchmark needed. Do not force a permanent parser choice to make Phase 1 look complete.

## 25. Work package 1.20: Parser routing decision record

Produce a versioned decision record containing:

- benchmark corpus/label versions;
- candidate implementations/versions;
- benchmark configuration version;
- per-document metrics;
- blocking defect summary;
- isolation status;
- reproducibility status;
- manual review-cost summary;
- performance/resource summary;
- selected primary route(s);
- selected independent comparator route(s);
- selected OCR route(s);
- configured alternative/fallback route(s);
- known unsupported source classes;
- rejected candidates and reasons;
- unresolved decisions;
- evidence needed to revisit the decision.

The decision record does not modify `docs/design.md` silently. If benchmark evidence requires a design change, propose that change separately.

## 26. Work package 1.21: Unit tests

Add focused tests for Phase 1 components.

### 26.1 Parser-neutral schema

Test:

- required fields;
- unknown-field rejection;
- deterministic ordering;
- invalid page numbers;
- invalid/non-finite coordinates;
- invalid box geometry;
- duplicate element IDs;
- duplicate reading-order positions where forbidden;
- malformed table grid/spans;
- invalid OCR confidence;
- absolute-path rejection;
- secret/path sentinel rejection.

### 26.2 Adapter identity

Test that identity changes when:

- parser version changes;
- adapter version changes;
- parser configuration changes;
- local model asset digest changes;
- implementation family changes;
- role changes.

### 26.3 Validation heuristics

Create deterministic fixtures for every Section 11.3 heuristic:

- page count;
- missing text;
- abnormal characters;
- heading tree;
- clause continuity;
- header/footer duplication;
- cross-page continuity;
- table consistency;
- page/coordinate completeness;
- parser comparison.

### 26.4 Comparison rules

Test:

- invalid same-implementation pair rejected;
- primary/comparator ordering;
- each unconditional blocking disagreement;
- threshold exact-at and one-over boundaries;
- below-threshold advisory difference;
- no field-level merge;
- deterministic primary selection after pass;
- failed comparison never promotes output.

### 26.5 Routing

Test benchmark routing configuration for:

- deterministic matching;
- no ambiguous two-route result;
- critical-comparison candidate always compared;
- OCR route chosen only by declared criteria;
- no crash-triggered fail-open fallback.

## 27. Work package 1.22: Integration tests

### 27.1 Adapter isolation

Run adversarial fixtures proving:

- network denied;
- unrelated source denied;
- credential/operator-state read denied;
- write escape denied;
- symlink escape denied;
- CPU limit enforced;
- memory limit enforced;
- wall-time limit enforced;
- output-size limit enforced;
- page-count limit enforced;
- isolation setup failure stops before adapter execution.

### 27.2 Real public/rights-cleared sample

Execute each supported adapter end-to-end on at least one rights-cleared representative sample and validate its parser-neutral output.

### 27.3 Critical dual-parser simulation

Use a Phase 0 critical-comparison candidate and inject:

- primary failure;
- comparator failure;
- clause disagreement;
- table disagreement;
- page-mapping disagreement;
- OCR/text disagreement;
- passing below-threshold difference.

For failures, the benchmark must finalize the complete diagnostic comparison report and promote no selected downstream parser output.

For a passing below-threshold difference, the report retains the difference and the selected primary artefact remains byte-identical to the standalone primary output.

### 27.4 Numeric table disagreement

Inject a numeric table disagreement and prove it is reported as parser disagreement, not an engineering evidence conflict.

## 28. Work package 1.23: Regression tests

Create versioned parser snapshots/expectations for the selected benchmark corpus where rights handling permits storage of the derived artefacts.

Regression coverage includes:

- expected page counts;
- expected structural landmarks;
- expected clause-marker sets;
- expected table shapes;
- selected expected text hashes/snippets;
- coordinate-anchor results;
- OCR-quality fixtures;
- comparison decisions;
- deterministic output hashes for selected routes;
- parser warning codes.

Private source-derived snapshots must follow Phase 0 rights rules and may need to remain local rather than in the public repository.

## 29. Benchmark reports

### 29.1 Per-document report

For every source/candidate route include:

- source identity;
- source characteristics;
- parser identity/configuration;
- isolation status;
- standalone validation results;
- structure metrics;
- text metrics;
- table metrics;
- OCR metrics;
- coordinate metrics;
- critical errors;
- performance/resources;
- reproducibility;
- reviewer findings/cost;
- final route assessment.

### 29.2 Pairwise comparison report

For every primary/comparator candidate pair include:

- role order;
- independent implementation proof;
- output hashes;
- comparison metrics;
- blocking disagreements;
- advisory differences;
- gate result;
- primary artefact hash when passed.

### 29.3 Aggregate matrix

Produce a matrix by document/source class showing:

- candidate pass/fail;
- blocking defect count;
- structural quality;
- table quality;
- OCR quality;
- coordinate quality;
- reproducibility;
- review cost;
- build time;
- recommendation.

Do not rank a failed candidate above a passing candidate merely because of speed.

## 30. Quality gates for Phase 1

The exact quantitative benchmark thresholds for parser quarantine/failure remain evidence-dependent open decisions, but Phase 1 itself has non-negotiable gates.

### 30.1 Hard gates

A recommended parser route must have:

- zero unresolved isolation failures;
- zero source-page-count mismatches on its admitted benchmark class;
- zero known changed numeric/table values in reviewed critical fixtures;
- zero known missing labelled critical clauses/exceptions on its admitted benchmark class;
- deterministic parser-neutral output under repeat testing;
- valid page association for required source-grounded anchors;
- no parser-native object dependency outside its adapter;
- a complete version/configuration/asset identity.

### 30.2 Comparator hard gates

A recommended comparator must additionally:

- be a distinct implementation family;
- detect injected material disagreements;
- never merge into primary output;
- preserve a complete diagnostic report on failure;
- support deterministic comparison decisions.

### 30.3 Threshold decision rule

For heuristic thresholds not already fixed by the design:

1. derive candidate values from benchmark distributions and labelled errors;
2. test exact-at/one-over boundaries;
3. document false-positive/false-negative consequences;
4. prefer blocking uncertainty for critical evidence when evidence is insufficient;
5. record unresolved threshold decisions rather than inventing a convenient number.

## 31. Handoff to Phase 2

Phase 1 hands Phase 2 the following **inputs**, not Phase 2 implementations:

- parser-neutral schema and serializer;
- adapter interface;
- isolated execution runner;
- selected and rejected parser adapter evidence;
- selected primary-route recommendations;
- selected independent comparator recommendations;
- selected OCR routing recommendation;
- configured alternative/fallback recommendations;
- versioned parser validation/comparison rules;
- benchmark routing predicates;
- benchmark report schema;
- benchmark decision record;
- deterministic output fixtures/hashes where rights permit;
- known unsupported document classes;
- unresolved threshold decisions;
- packaging dependencies required only by the build/parser extras.

Phase 2 is responsible for binding these to:

- production manifests and `release_tier`;
- production parser routing configuration;
- canonical-model construction;
- production caches;
- static build review reports;
- catalog/release admission.

Phase 1 must not implement those Phase 2 responsibilities in advance.

## 32. Acceptance criteria

Phase 1 is complete only when all of the following are true.

1. A versioned parser-neutral intermediate schema exists and covers every Section 11.2 field class.
2. At least the design's initial parser-path classes are represented by benchmark adapters: structured PDF, deterministic page/coordinate extraction, and OCR/difficult-document extraction.
3. Every adapter runs only through the common isolation boundary.
4. Isolation adversarial tests pass and failure to establish isolation is blocking.
5. Every Section 11.3 single-parser validation heuristic is implemented and tested.
6. The comparison engine rejects same-implementation “dual” parsing.
7. Primary/comparator roles are explicit and ordered.
8. All unconditional blocking comparison conditions are implemented and tested.
9. Below-threshold differences remain visible as `parser_comparison_difference` and never cause field-level merging.
10. Phase 0 critical-comparison candidates have been benchmarked with two independent parser implementations.
11. Structural, page, coordinate, table, OCR, text, build-time, resource, and review-cost metrics are reported separately.
12. Complex table and numeric-integrity fixtures are included.
13. OCR-sensitive fixtures are included.
14. Selected route outputs are reproducible/byte-identical under repeat runs with unchanged inputs.
15. Parser identity includes implementation, version, adapter, configuration, assets, and role.
16. A default primary route or deterministic set of primary routing recommendations is selected from evidence.
17. An independent comparator recommendation exists for the critical-document path.
18. An OCR route recommendation exists or is explicitly unresolved with a documented benchmark gap.
19. Any fallback recommendation is defined as a configured alternative route, never a silent fail-open retry.
20. Rejected candidates and unresolved decisions are documented.
21. The Phase 1 decision record is sufficient for Phase 2 to implement production routing without relying on private chat history.
22. No production canonical model, catalog, retrieval, MCP/CLI, or immutable release functionality has been pulled into the Phase 1 implementation plan.
23. Repository documentation checks pass.

## 33. Risks and mitigations

### 33.1 Benchmark overfits to clean PDFs

**Risk:** A parser wins because most samples are native text.

**Mitigation:** Report native-text, OCR, table-heavy, and layout-heavy strata separately and require the Phase 0 representative coverage matrix.

### 33.2 Parser-native schema leaks downstream

**Risk:** Later code becomes coupled to one parser.

**Mitigation:** Enforce the closed parser-neutral adapter boundary and prohibit parser-native objects in comparison/validation code.

### 33.3 Comparator is not independent

**Risk:** Two configurations of one parser share the same systematic errors.

**Mitigation:** Explicit implementation-family identity and pair validation.

### 33.4 Silent fail-open fallback

**Risk:** A parser crash or disagreement causes another parser to be used without review.

**Mitigation:** Define fallback as preconfigured routing only; failures remain blocking and diagnostic.

### 33.5 OCR confidence is misleading

**Risk:** Engine confidence is treated as universal correctness probability.

**Mitigation:** Calibrate against reviewed fixtures and retain `confidence_unavailable`/engine-specific semantics.

### 33.6 Tables look correct but values change

**Risk:** Visual structure masks decimal/sign/unit errors.

**Mitigation:** Dedicated numeric-cell integrity metrics and blocking disagreement fixtures.

### 33.7 Performance drives selection too early

**Risk:** Fast parser chosen despite evidence loss.

**Mitigation:** Hard accuracy gates precede runtime/review-cost comparison.

### 33.8 Benchmark artefacts leak copyrighted content

**Risk:** Parser snapshots include licensed source text in Git.

**Mitigation:** Apply Phase 0 rights classification to derived snapshots/reports; store hashes/metadata or local-only artefacts when redistribution is not allowed.

### 33.9 Unpinned external assets break reproducibility

**Risk:** OCR/model assets change remotely.

**Mitigation:** Local, declared, digested assets for selected routes; no network during parse.

## 34. Recommended implementation sequence

Implement Phase 1 in this order.

1. Load the frozen Phase 0 parser-benchmark pack.
2. Define parser-neutral schema and deterministic serialization.
3. Define adapter identity and failure contracts.
4. Implement/verify parser subprocess isolation.
5. Add adversarial isolation fixtures.
6. Implement the Docling adapter candidate.
7. Implement the PyMuPDF adapter candidate.
8. Implement the OCR-oriented adapter candidate.
9. Implement single-parser validation heuristics.
10. Build table, OCR, page/coordinate, and structural benchmark subsets.
11. Implement the independent comparison engine.
12. Implement benchmark-only routing configuration.
13. Execute standalone candidate matrix.
14. Execute primary/comparator pair matrix.
15. Run repeat/determinism tests.
16. Conduct blinded review-cost sampling.
17. Generate per-document and aggregate reports.
18. Apply accuracy-first hard gates.
19. Select primary/comparator/OCR/configured-alternative recommendations.
20. Record unresolved thresholds/gaps.
21. Freeze the Phase 1 parser-routing decision package for Phase 2.

Any material benchmark-ground-truth correction returns through Phase 0's versioned label-change process rather than being edited silently inside Phase 1.

## 35. Definition of done

Phase 1 is done when a Phase 2 implementation agent can determine, from repository artefacts alone:

- how to invoke every selected parser safely;
- exactly what parser-neutral output means;
- how parser identity and configuration are hashed/versioned;
- how to validate a standalone parser result;
- when comparison mode blocks;
- how independent parser pairs are proved;
- which primary/comparator/OCR routes were selected and why;
- which alternative route applies to which source class;
- which choices remain unresolved;
- what structural/table/OCR/page-mapping failures were observed;
- how review cost and build time compare after accuracy gates;
- how to reproduce the benchmark;
- which artefacts are safe to commit or must remain local;
- and which responsibilities remain explicitly deferred to Phase 2.

The central Phase 1 deliverable is **measured parser-routing evidence**, not a prematurely complete ClauseSift builder.