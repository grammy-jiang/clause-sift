# Phase 0 Implementation Plan: Evaluation Corpus

**Project:** ClauseSift  
**Phase:** 0 of the design-defined implementation sequence  
**Status:** Implementation plan  
**Primary design authority:** `docs/design.md`  
**Phase objective:** Establish the representative source corpus, evaluation taxonomy, source-grounded labels, reviewer protocol, and statistical expansion plan that will be used to evaluate every later parser, retrieval, context, conflict, citation, and refusal decision.

## 1. Purpose

Phase 0 creates the evidence and evaluation baseline for ClauseSift before parser or retrieval implementation begins.

ClauseSift is accuracy-first. The project therefore cannot choose parsers, tokenisation, chunking, lexical search, embedding models, rerankers, context rules, or performance optimisations using informal spot checks. Later implementation phases must be evaluated against a stable, versioned, source-grounded corpus that represents the engineering-document problems ClauseSift is explicitly designed to solve.

This phase implements the preparation work required by the design's evaluation strategy and the first implementation phase. It must produce enough representative material to drive the Phase 1 parser benchmark immediately, while also establishing the process by which the corpus expands to the statistically meaningful release-gate sample sizes required later.

Phase 0 does **not** implement the production manifest format, parser pipeline, canonical Evidence Graph, retrieval indexes, runtime API, CLI, MCP server, or release builder. Those are later phases. It may define evaluation-only schemas and fixture conventions, but they must not become a competing production data model or source of engineering authority.

## 2. Design constraints that govern this phase

The implementation of this phase must preserve the following design decisions.

1. Accuracy has priority over speed, convenience, or implementation effort.
2. Original source documents remain authoritative. Evaluation labels may point to and describe source evidence, but may not replace or rewrite it as authority.
3. Document identity and edition must remain explicit. Different editions must never be silently merged.
4. Clause numbers, pages, tables, units, exceptions, notes, applicability, cross-references, and source modality must be represented in the evaluation material where applicable.
5. Source modality such as `required`, `prohibited`, `recommended`, or `permitted` must not be promoted into a project-specific legal-force conclusion.
6. Unknown, ambiguous, conflicting, unresolved, or insufficient evidence must be represented explicitly rather than coerced into a plausible answer.
7. Generated summaries or LLM labels may assist corpus preparation, but they cannot be the sole release-gate authority.
8. The evaluation corpus must include English, Chinese, and cross-language queries.
9. Phase 0 begins with an exploratory seed of 30-50 real questions. That seed is not statistically sufficient for the final release gates.
10. Probabilistic gates must later use independent labelled cases and one-sided 95% Wilson confidence intervals, with at least 150 applicable cases for each 98% gate and at least 60 applicable cases for each 95% gate, increased when stratification would otherwise underrepresent critical cases.
11. Deterministic 100% and zero-failure gates must report the complete suite size and every failure; they are conformance gates rather than population estimates.
12. Rights-cleared public sample documents suitable for automated tests are a governance decision and must not be assumed to exist merely because a document is accessible to the developer.

Whenever this plan appears to conflict with `docs/design.md`, the design document is authoritative and this plan must be amended before implementation continues.

## 3. Phase outcomes

Phase 0 is complete when the project has all of the following.

### 3.1 Representative engineering corpus

A curated set of 5-10 representative documents is selected and recorded. Collectively the set must include:

- native-text PDF material;
- at least one scanned or OCR-dependent PDF;
- complex tables with headers, units, merged cells, footnotes, or multi-page continuation where available;
- at least one design guideline or similar mixed normative/informative document;
- at least one manufacturer specification or technical manual;
- two editions of the same standard or code family;
- definitions and scope provisions;
- exceptions and notes;
- cross-clause or cross-document references;
- material suitable for version-difference questions;
- source text containing numbers, units, identifiers, and technical terminology.

The corpus should favour HVAC, ventilation, smoke-control, fire-safety, and manufacturer documentation because these are the initial ClauseSift use cases.

### 3.2 Exploratory golden-question seed

A versioned seed of 30-50 real engineering questions exists, with expected source-grounded evidence and explicit answerability labels.

The seed is deliberately broad rather than statistically representative. It is the first working benchmark for Phase 1 and the basis for later expansion.

### 3.3 Evaluation taxonomy and schemas

The repository contains a precise, versioned specification for:

- query records;
- expected evidence records;
- answerability labels;
- classification labels;
- context-path labels;
- conflict labels;
- reviewer labels and adjudication;
- corpus-version metadata;
- calibration items;
- metric result records.

These are evaluation artefacts only. They must reference source-grounded identity and later canonical IDs when those IDs become available, rather than inventing a second production evidence model.

### 3.4 Human-review protocol

A repeatable labelling and adjudication process exists for semantic cases. It must support:

- blinded independent review;
- disagreement recording;
- third-reviewer adjudication;
- raw agreement reporting;
- Cohen's kappa where defined;
- the design's degenerate-sample fallback rules;
- calibration-set handling;
- provenance from the final label back to the reviewed source evidence.

### 3.5 Release-gate expansion plan

The Phase 0 deliverables identify exactly how the exploratory seed will be expanded into independently labelled samples large enough for the Section 29.4 quality gates, including stratification, minimum sample sizes, data-splitting rules, leakage controls, and ownership.

The later implementation phases may start using the exploratory seed once its baseline is approved, but the first release cannot claim a probabilistic gate until the applicable expanded sample meets the design's minimum sample-size and confidence-interval requirements.

## 4. Repository and data-handling layout

Phase 0 implementation should establish a layout that separates version-controlled evaluation metadata from source documents whose redistribution may not be permitted.

Recommended layout:

```text
evaluation/
├── README.md
├── schema/
│   ├── corpus.schema.json
│   ├── question.schema.json
│   ├── evidence-label.schema.json
│   ├── classification-label.schema.json
│   ├── context-label.schema.json
│   ├── conflict-label.schema.json
│   └── review-label.schema.json
├── corpus/
│   ├── corpus-v0001.json
│   └── documents/
├── questions/
│   ├── seed-v0001.jsonl
│   ├── calibration-v0001.jsonl
│   └── README.md
├── labels/
│   ├── evidence/
│   ├── classification/
│   ├── context/
│   ├── conflict/
│   └── reviews/
├── splits/
├── reports/
└── scripts/

tests/
└── fixtures/
    └── public-evaluation/
```

The exact directory names may be adjusted during implementation if repository conventions require it, but the following separation is mandatory.

- Copyright-restricted original standards and manuals are **not** committed merely to make evaluation convenient.
- Version-controlled records may contain safe metadata, hashes, stable corpus IDs, labels, and citations required to reproduce the evaluation.
- Rights-cleared public samples used in automated tests live separately from the private/local engineering corpus.
- Local source paths are never treated as stable public identity.
- Source-file hashes are used to detect accidental substitution of a file with different bytes.
- Evaluation records must not contain credentials or private absolute filesystem paths.

## 5. Work package 0.1: Establish corpus governance

### 5.1 Define corpus classes

Create two explicit corpus classes.

#### Private/local engineering corpus

This is the high-value representative corpus used by the technical user for realistic evaluation. It may contain licensed standards and commercial manufacturer documents that ClauseSift is permitted to process locally but not redistribute.

The repository stores only the safe metadata and hashes needed to identify the expected local inputs. The source bytes remain outside Git history unless their licence explicitly permits redistribution.

#### Public automated-test corpus

This contains rights-cleared material that can safely be included in the repository or downloaded deterministically by CI under documented terms.

Its purpose is deterministic automated testing of parser, citation, traversal, schema, release, and runtime behaviour. It does not need to match the commercial engineering corpus in subject importance, but it must exercise representative structures.

### 5.2 Record rights status

For every selected document, record at minimum:

- corpus document key;
- human-readable title;
- document code or identifier where available;
- edition or revision;
- document class;
- expected discipline and jurisdiction metadata where known from authoritative metadata;
- source-file SHA-256;
- source byte size;
- page count if independently available;
- source acquisition category;
- redistribution status;
- automated-test eligibility;
- licence or rights-review status;
- reviewer responsible for the rights decision;
- decision-record reference when required;
- notes limited to governance facts, not inferred legal enforceability.

Use a closed rights-status enumeration such as `private_local`, `redistributable`, `public_domain`, `external_fixture`, and `review_required`. The exact enum must be documented and schema-validated.

A document with `review_required` must not be committed as source bytes and must not become a CI dependency until its status is resolved.

### 5.3 Prevent accidental source publication

Add safeguards during Phase 0 implementation so future contributors do not accidentally commit restricted files.

At minimum:

- document the permitted source locations;
- extend `.gitignore` for local/private corpus directories if needed;
- add a validation script that detects forbidden PDF/source files under version-controlled evaluation paths unless explicitly allowlisted as rights-cleared fixtures;
- make the validation script deterministic and CI-friendly;
- ensure hashes and safe metadata remain reviewable without revealing private paths.

## 6. Work package 0.2: Select the representative 5-10 documents

### 6.1 Selection method

Build a candidate inventory larger than the final corpus, score it against the structural and semantic coverage matrix below, then select the smallest set that covers the required dimensions without creating unnecessary labelling cost.

Selection should not be based on prestige or document popularity alone. A document is valuable when it exercises a ClauseSift failure mode.

### 6.2 Required coverage matrix

The selected set must collectively cover these dimensions.

| Dimension | Required coverage |
| --- | --- |
| PDF type | Native text and scanned/OCR-dependent |
| Structure | Flat sections and deeply nested clauses |
| Tables | Simple and complex tables; units and footnotes where available |
| Normative structure | Requirements/prohibitions plus informative notes or commentary |
| Applicability | Scope conditions and at least one meaningful exception |
| References | Internal clause references and preferably cross-document references |
| Editions | Two editions of one document family |
| Document class | Standard/code/guideline plus manufacturer manual/specification |
| Technical tokens | Exact identifiers, model numbers, units, symbols, and numeric thresholds |
| Language challenge | Material that can support English, Chinese, and cross-language queries |
| Layout challenge | Multi-column, headers/footers, page labels, repeated table headers, or similar complexity where available |

### 6.3 Preferred corpus shape

A practical target is 7-9 documents, for example:

- two editions of one representative standard;
- one code or regulation-style document;
- one mixed normative/informative design guideline;
- one scanned legacy document;
- one manufacturer technical manual;
- one manufacturer product specification with dense tables;
- optionally one document chosen specifically for complex references, appendices, or page-layout challenges.

This is a coverage pattern, not a fixed product list. Actual documents must be chosen from material the user is entitled to process.

### 6.4 Selection review

Before freezing corpus version `v0001`, produce a corpus-selection report showing:

- candidate documents considered;
- coverage matrix for each candidate;
- reasons for selection or rejection;
- known gaps;
- licence/redistribution constraints;
- expected use in later phases;
- which documents are `release_tier: critical` candidates for later dual-parser testing, without prematurely creating production manifests.

Do not select a document solely because it makes a parser look good.

## 7. Work package 0.3: Define stable evaluation identity

Phase 0 needs stable references before the production canonical model exists, but it must avoid creating a parallel authority model.

### 7.1 Corpus document identity

Assign each evaluation document a stable `corpus_document_id` that is opaque and independent of local filenames. Bind it to the expected source SHA-256 and edition metadata.

When Phase 2 introduces the production manifest and canonical `document_id`, add a versioned mapping from `corpus_document_id` to the canonical identity. Do not silently replace historical labels.

### 7.2 Evidence locator identity before Phase 2

Initial expected evidence may be located using source-grounded fields such as:

- corpus document ID;
- document code and edition;
- printed clause number or table identifier;
- one-based PDF page number;
- printed page label where different;
- a short deterministic hash of the exact expected source span;
- reviewer-entered locator notes where structure is ambiguous.

The source span itself remains authoritative. The locator is a bridge until Phase 2 can replace or supplement it with canonical node/source IDs.

### 7.3 Canonical-ID migration

Phase 2 must provide a one-time migration tool or script that resolves Phase 0 locators to canonical IDs and produces a diff for human review.

The migration must fail visibly when:

- more than one canonical node matches a supposedly exact locator;
- no canonical node matches;
- the source hash differs;
- the edition differs;
- the expected text hash differs;
- page or clause identity cannot be reconciled.

No fuzzy migration result becomes accepted ground truth automatically.

## 8. Work package 0.4: Define the golden-question record

Each golden question must be a versioned record with enough information to evaluate retrieval without reconstructing intent from prose comments.

### 8.1 Required fields

A question record should include at least:

- `question_id`;
- corpus version;
- question-set version;
- question text;
- query language;
- expected response language if constrained;
- query category labels;
- answerability label;
- expected document and edition identities;
- expected evidence-label IDs;
- required-context label IDs where applicable;
- conflict-label IDs where applicable;
- expected refusal or insufficiency behaviour where applicable;
- allowed retrieval intent such as exact lookup, lexical/hybrid search, or general query;
- criticality/priority tag for stratification;
- provenance showing who authored and who independently reviewed the item;
- change reason when an accepted record is modified.

### 8.2 Answerability enum

Use a closed answerability classification such as:

- `answerable`;
- `answerable_with_conflict`;
- `answerable_with_incomplete_context`;
- `insufficient_evidence`;
- `ambiguous_query`;
- `unsupported_inference`;
- `invalid_input`.

The exact enum may be refined during schema review, but it must remain closed and must distinguish a valid no-match/insufficient-evidence result from malformed input and from unsupported engineering inference.

### 8.3 Query-language enum

At minimum support:

- `en`;
- `zh`;
- `cross_language`.

For cross-language items, record which language appears in the source and which language appears in the query.

### 8.4 Versioning rule

Changing question wording in a way that can change retrieval behaviour creates a new question revision. Historical evaluation results remain bound to the exact question revision used.

Typographic corrections that are proven not to alter canonical query bytes may be handled according to a documented narrow rule; do not rewrite historical records casually.

## 9. Work package 0.5: Build the 30-50 question exploratory seed

### 9.1 Seed size

Target 40 questions initially, with an acceptable Phase 0 range of 30-50 as required by the design.

The seed must not be presented as statistically proving the release gates.

### 9.2 Coverage allocation

A practical initial allocation is:

| Category | Target seed items |
| --- | ---: |
| Exact document/clause identifiers | 4-6 |
| Definitions | 2-4 |
| Scope and applicability | 3-5 |
| Requirements/prohibitions/recommendations/permissions | 4-6 |
| Exceptions and informative notes | 3-5 |
| Tables, values, and units | 4-6 |
| Product models/parameters | 2-4 |
| Cross-clause/cross-document references | 3-5 |
| Edition/version differences | 2-4 |
| Conflict and no-precedence cases | 2-4 |
| Unanswerable/ambiguous/unsupported inference | 4-6 |
| Malformed or boundary-oriented logical cases | 2-4 |
| Chinese/cross-language subset | at least 8 total across categories |

These targets overlap. One question may cover several categories, but each category must have independently reviewable coverage.

### 9.3 Real engineering wording

Questions should resemble how an engineer actually searches, including:

- terse identifier lookups;
- natural-language design questions;
- incomplete but realistic wording;
- unit-bearing questions;
- product model queries;
- questions that imply a tempting but unsupported conclusion;
- questions whose answer changes between editions.

Avoid creating a seed consisting only of queries that mirror exact source wording.

### 9.4 Leakage control

Question authors may inspect source documents to create realistic questions, but later benchmark tuning must not repeatedly rewrite the golden set around known parser/retrieval failures.

Create three categories from the start:

- development diagnostics;
- benchmark validation;
- held-out release evaluation.

The 30-50 exploratory seed may initially be mostly development/benchmark material. Before release-gate evaluation, held-out independently labelled cases must be added and kept out of implementation tuning.

## 10. Work package 0.6: Evidence labels

### 10.1 Source-backed expected evidence

Every answerable golden question must identify the minimum expected source evidence required to support the intended result.

An evidence label must record:

- exact document and edition;
- clause/table/appendix/definition identity where available;
- page identity;
- exact expected source span or deterministic hash of that span;
- whether the evidence is direct or contextual;
- whether the evidence is required for a correct answer or merely acceptable supporting context;
- expected source modality when independently labelable;
- known coordinate limitations;
- reviewer provenance.

Do not store a generated paraphrase as the expected evidence when the original source span is available.

### 10.2 Multiple valid evidence items

Some questions legitimately require several source items. Represent them as explicit expected sets with required/optional roles rather than accepting any one chunk that happens to contain overlapping words.

Examples include:

- a requirement plus its parent scope;
- a requirement plus an exception;
- a table row plus title/header/unit context;
- a definition plus the clause that depends on it;
- both sides of a material conflict;
- two editions used in an explicit version comparison.

### 10.3 Forbidden evidence

For hard-negative cases, record source items or relationship classes that must **not** appear as accepted required context.

Examples:

- a clause from the wrong edition;
- an unresolved reference target guessed from similar text;
- an informative note promoted to a normative requirement;
- a semantically similar requirement from a different jurisdiction when the query is explicitly scoped;
- a broader chunk used to claim precise atomic context when the design requires a scope-contained source.

These labels support the design's zero-accepted-edge and contamination gates.

## 11. Work package 0.7: Context and traversal labels

Phase 0 must prepare cases that later validate deterministic Evidence Graph traversal.

### 11.1 Required context cases

Include cases for:

- parent scope;
- multiple exceptions;
- definitions;
- applicability;
- table title/header/unit/parent context;
- notes affecting a parent;
- required dependencies;
- ordinary and required references;
- unresolved targets;
- cyclic references;
- superseded seeds;
- explicit version comparison;
- same clause number in two editions;
- overlapping closures from multiple seeds.

### 11.2 Expected path representation

Before graph edge IDs exist, record the expected semantic path in source terms. After Phase 2/4 generates canonical relationships, migrate each applicable record to an exact ordered edge-ID sequence.

The final release-gate label must be capable of exact comparison of:

- seed source ID;
- target source or metadata-only target ID;
- relation type sequence;
- edge-ID sequence;
- inclusion class;
- required/supporting role;
- expected warning where traversal is incomplete, cyclic, status-bounded, or unresolved.

### 11.3 Deterministic negative traversal suite

Identify a closed set of cases where traversal is prohibited, unresolved, guessed, or wrong-edition. These become deterministic conformance fixtures with zero accepted bad edges.

## 12. Work package 0.8: Evidence-vocabulary and classification labels

The corpus must support later evaluation of the design's versioned engineering evidence vocabulary.

### 12.1 Coverage goals

Prepare examples for every applicable core value and edge case in the design, including:

- document types;
- node types;
- normative statuses;
- source modalities;
- classification origins;
- inheritance branches;
- normative and informative appendices;
- nested notes;
- manufacturer instructions;
- multiple or unknown jurisdictions;
- multiple or unknown disciplines;
- `unclassified` and `unknown` cases;
- forbidden composite aliases;
- unsupported vocabulary/core/extension versions where synthetic fixtures are appropriate.

### 12.2 Labelling rule

A semantic classification label is accepted only when a reviewer can point to source-grounded evidence or an explicitly deterministic rule defined by the design.

When the source does not support a stronger value, use the conservative `unknown`/`unclassified` outcome expected by the design. Do not force complete labels to make the metric easier to calculate.

### 12.3 Independence from retrieval rank

Classification labels must describe the source/canonical evidence, not the ranking result. Later tests must prove that adverse retrieval ranks do not change classification values.

## 13. Work package 0.9: Conflict corpus

Prepare a compact but deliberately difficult set of conflict cases for later Phase 4 implementation.

### 13.1 Positive cases

Include where sources permit:

- confirmed numeric conflict;
- confirmed normative-language incompatibility;
- three-position conflict;
- conflict with encoded trusted precedence;
- unresolved conflict with insufficient applicability information.

### 13.2 Explained non-conflict or difference cases

Include hard negatives for:

- unit-equivalent values;
- compatible modalities;
- valid exception;
- amendment;
- supersession;
- disjoint jurisdiction;
- disjoint effective interval;
- disjoint product/equipment class;
- compatible stricter requirements where the design's conflict model treats them as non-conflicting;
- parser disagreement that must remain parser uncertainty rather than be promoted to a source conflict.

### 13.3 No implicit winner

Every conflict item must state whether trusted precedence is explicitly encoded. A label with no encoded precedence must never contain a selected winner.

### 13.4 Later canonicalisation

Phase 4 will replace preliminary source-level conflict locators with exact versioned conflict IDs, positions, source IDs, and spans. Migration is reviewed rather than inferred silently.

## 14. Work package 0.10: Invalid, ambiguous, and unsupported questions

At least 15-20% of the exploratory seed should exercise behaviour where returning a confident engineering answer would be wrong.

Include:

- a valid question with no supporting evidence in the corpus;
- a question whose scope is ambiguous;
- a question that asks ClauseSift to infer legal applicability not contained in the source metadata;
- a question that asks for an engineering calculation outside ClauseSift's retrieval scope;
- a query that attempts to mix editions without explicit comparison intent;
- a query that assumes an unresolved reference has a known target;
- malformed identifiers;
- overlong logical fixtures and out-of-range values represented in synthetic protocol tests rather than requiring absurd human question text.

For each case, label the expected behaviour separately from the expected prose. The important ground truth is whether evidence should be returned, whether a warning/refusal is required, and which diagnostic category applies after the corresponding runtime functionality exists.

## 15. Work package 0.11: Multilingual evaluation

### 15.1 Minimum seed coverage

At least eight seed questions should exercise Chinese or cross-language retrieval, distributed across several engineering categories rather than isolated into one translation-only group.

Include:

- Chinese question against English source text;
- English question using a Chinese synonym or mixed-language technical identifier where realistic;
- Chinese paraphrase of an exact engineering concept;
- queries containing unchanged standard identifiers, clause numbers, model numbers, and units inside Chinese prose.

### 15.2 Translation authority

A translated question is a query variant, not a translated source authority. Expected evidence continues to point to the original source document and original source text.

### 15.3 Later tokenisation benchmark

Tag multilingual records so Phase 2 lexical-search and Phase 3 embedding benchmarks can report their performance separately. This is necessary because Chinese tokenisation remains an explicit implementation decision in the design.

## 16. Work package 0.12: Human labelling and adjudication

### 16.1 Reviewer roles

Define three logical roles:

- primary reviewer;
- independent secondary reviewer;
- adjudicator.

A person may perform more than one role across different items, but the same individual must not act as both initial independent reviewers for one semantic release-gate item.

### 16.2 Initial release-gate labelling

For the initial release-gate corpus, two blinded reviewers independently label every item that requires human semantic judgement.

Each reviewer must record:

- raw label;
- evidence locator(s);
- uncertainty flag;
- rubric category;
- optional bounded rationale;
- reviewer identifier;
- rubric version;
- timestamp in the review record where operational history requires it, without using wall-clock data as deterministic corpus identity.

### 16.3 Subsequent release cycles

After the first release, the second reviewer covers:

- a preregistered stratified sample of at least 20%;
- every gate failure;
- every item marked uncertain by the primary reviewer;
- the full blinded calibration set.

### 16.4 Calibration set

Create a versioned blinded calibration set excluded from product metrics. It must contain at least ten independently adjudicated examples of every human-rubric category used in the applicable release evaluation.

Reference labels must be hidden from active reviewers during labelling.

### 16.5 Agreement calculation

Report agreement before adjudication.

- Nominal labels use unweighted Cohen's kappa.
- Ordinal labels use the rubric's preregistered fixed weight matrix.
- A computable coefficient must be at least 0.80 on the release sample and calibration set.
- If the release sample is degenerate because both reviewers assign every item to the same category, report kappa as `not_estimable`.
- The degenerate release sample passes reliability only with exactly 100% raw agreement and a computable calibration kappa of at least 0.80 using at least two observed categories.
- A degenerate calibration result blocks the gate.
- Any release-sample disagreement in the degenerate fallback case blocks the gate.
- Disagreements are adjudicated by a third reviewer.

The evaluation tooling must retain raw labels, category counts, agreement, coefficient computability, adjudication, and final labels.

## 17. Work package 0.13: Statistical expansion plan

### 17.1 Separate deterministic and probabilistic suites

Maintain separate suites for:

- deterministic conformance;
- probabilistic retrieval/classification/context/conflict quality;
- human semantic judgement.

Do not combine them into one headline accuracy percentage.

### 17.2 98% probabilistic gates

For every 98% gate, create an independently labelled applicable sample of at least 150 cases.

This minimum applies independently to applicable metric families such as:

- Recall@20 lower-bound target;
- node-type accuracy;
- normative-status accuracy;
- source-modality accuracy;
- confirmed/unresolved conflict precision where that gate is evaluated;
- explained-difference precision where that gate is evaluated.

If a metric family has subclasses that would be critically underrepresented, increase the sample rather than relying on the bare minimum.

### 17.3 95% probabilistic gates

For every 95% gate, create an independently labelled applicable sample of at least 60 cases.

Examples include:

- Top-5 evidence presence;
- optional-context precision;
- conflict-candidate recall.

Again, increase the sample when stratification would otherwise omit important query, relation, conflict, or hard-negative categories.

### 17.4 Wilson interval implementation

Evaluation tooling must calculate the one-sided 95% Wilson lower confidence bound from the exact numerator and denominator.

Every metric report includes:

- successes;
- failures;
- total applicable cases;
- point estimate;
- one-sided 95% Wilson lower bound where applicable;
- target;
- pass/fail;
- corpus version;
- question/label-set version;
- excluded/not-applicable count with reasons.

A percentage without numerator and denominator is invalid for a release-gate report.

### 17.5 Stratification

Preregister strata before running a release gate. At minimum consider:

- exact versus natural-language query;
- English, Chinese, cross-language;
- document type;
- native text versus OCR;
- table versus prose;
- current versus superseded edition;
- exact identifiers and numeric/unit queries;
- required context family;
- optional context family;
- classification field and origin;
- conflict dimension and state;
- answerable versus hard negative;
- critical versus standard source tier once production manifests exist.

Strata are for coverage and reporting, not for quietly dropping poor-performing classes.

## 18. Work package 0.14: Evaluation splits and leakage controls

### 18.1 Stable splits

Create versioned split manifests for:

- development;
- parser benchmark;
- retrieval benchmark;
- held-out release gate;
- calibration.

An item may belong to only the explicitly allowed roles. Release-gate labels must not be exposed to implementation-time tuning scripts.

### 18.2 Document-level leakage

Where possible, reserve at least some held-out questions from documents or structural patterns not repeatedly used during component tuning.

For edition comparison, ensure both editions do not leak through duplicated near-identical questions across development and held-out sets.

### 18.3 Model benchmark leakage

Phase 3 embedding and reranker model selection must not optimise directly on the final held-out release gate. Provide a benchmark split specifically for model selection and preserve a separate held-out set.

### 18.4 Change control

Any change to a held-out label after a model or retrieval system has been evaluated against it requires:

- recorded reason;
- reviewer identity;
- whether the change was discovered because of system output;
- adjudication if semantic;
- corpus-version increment when the meaning changes.

## 19. Work package 0.15: Evaluation tooling

Phase 0 should implement only tooling needed to validate and manage the corpus itself. Retrieval scoring that depends on later runtime outputs may initially be stubbed behind stable input formats.

### 19.1 Required Phase 0 utilities

Implement deterministic utilities for:

- JSON/JSONL schema validation;
- duplicate question-ID detection;
- duplicate or conflicting source-hash detection;
- corpus-document coverage reporting;
- taxonomy/stratum coverage reporting;
- split-overlap detection;
- rights-status validation;
- forbidden source-file detection;
- reviewer-role validation;
- calibration-set completeness checks;
- Wilson lower-bound calculation with unit tests;
- Cohen's kappa calculation or a pinned, reviewed dependency with deterministic wrapper tests;
- corpus/version consistency checks;
- safe generation of static summary reports without embedding untrusted data as active content.

### 19.2 Future-facing result adapter

Define a simple evaluation-result input contract that later phases can populate with:

- query ID;
- release/build identity;
- returned document/source IDs;
- ranks;
- retrieval channel;
- context paths;
- warnings;
- conflict records;
- citations;
- latency metadata where relevant.

Do not implement fake runtime output merely to complete Phase 0. The purpose is to prevent every later phase from inventing a different evaluator interface.

### 19.3 Determinism

Given identical corpus bytes, label bytes, and tool version, Phase 0 validation reports should be byte-stable except for explicitly separated operational metadata.

## 20. Work package 0.16: Phase 0 tests

### 20.1 Unit tests

Add tests for:

- every evaluation schema;
- exact enum validation;
- unknown-field rejection where schemas are intended to be closed;
- duplicate IDs;
- bad SHA-256 values;
- changed source hash;
- invalid page/clause locators;
- invalid split overlap;
- invalid reviewer combinations;
- missing calibration categories;
- rights-review blocking cases;
- Wilson interval boundary cases;
- kappa computable and non-computable cases;
- degenerate-sample fallback rules;
- malformed multilingual metadata;
- illegal stronger classification where a fixture is explicitly `unknown`/`unclassified`.

### 20.2 Golden self-tests

The corpus validator should include intentionally invalid fixture records proving that it rejects:

- a question referring to a non-existent evidence label;
- an evidence label referring to the wrong document edition;
- a conflict label that declares a winner without encoded precedence;
- a classification label using a forbidden composite alias;
- an item simultaneously placed in held-out and development splits when the split policy forbids it;
- a redistributable flag without the required rights decision;
- a semantic label with no source/reviewer provenance.

### 20.3 Repository checks

All new Markdown must pass the repository's Markdown linting. Any Mermaid added later must pass the existing Mermaid validation hook. Evaluation JSON/YAML validation should be integrated into pre-commit and GitHub Actions only after its schema and runtime cost are stable.

## 21. Work package 0.17: Phase 0 reports

Produce the following machine-readable and human-readable reports.

### 21.1 Corpus inventory report

Includes:

- document count;
- document classes;
- editions;
- PDF types;
- table coverage;
- OCR coverage;
- rights status;
- public/private fixture status;
- known gaps.

### 21.2 Question coverage report

Includes:

- total questions;
- counts by query category;
- counts by language;
- answerability distribution;
- document coverage;
- table/context/conflict/vocabulary coverage;
- development/benchmark/held-out/calibration split counts.

### 21.3 Reviewer-quality report

Includes:

- reviewer coverage;
- uncertain-item count;
- disagreements;
- raw agreement;
- kappa or `not_estimable` status;
- adjudication count;
- calibration results.

### 21.4 Statistical-readiness report

For each Section 29.4 probabilistic gate, report:

- current applicable sample count;
- required minimum count;
- identified missing strata;
- whether the corpus is exploratory, benchmark-ready, or release-gate-ready.

Phase 0's initial 30-50 question seed must be labelled `exploratory` until the relevant expansion thresholds are actually met.

## 22. Work package 0.18: Review gates before Phase 1

Phase 1 parser benchmarking may begin only after the following Phase 0 baseline gate passes.

- 5-10 representative documents have been selected.
- Every selected document has a stable corpus ID and source hash.
- Rights/redistribution status is recorded.
- The selected set covers native text, scan/OCR, complex table, guideline/specification, and two-edition requirements.
- 30-50 exploratory golden questions exist.
- Every answerable question has reviewed source-grounded evidence labels.
- Unanswerable/ambiguous/unsupported-inference cases exist.
- English, Chinese, and cross-language cases exist.
- Evaluation schemas validate with no errors.
- Split leakage checks pass.
- Corpus validation and statistical helper unit tests pass.
- Known coverage gaps are written down rather than silently ignored.

The full release-gate sample-size targets do **not** have to be complete before the first parser benchmark. However, the expansion plan, ownership, and schemas must already be approved, and the later first-release acceptance criteria cannot be declared satisfied until the applicable expanded corpus meets them.

## 23. Handoff to Phase 1: Parser benchmark

Phase 0 must hand Phase 1 a parser-benchmark pack containing, for each representative document where licensing permits local use:

- immutable source hash and size;
- source acquisition/rights classification;
- expected page count where verified;
- expected high-level clause/section landmarks;
- representative table pages;
- representative OCR-sensitive pages;
- representative page/coordinate anchors;
- known layout anomalies;
- expected text snippets used only as source-grounded parser checks;
- review-cost worksheet template;
- corpus IDs shared with the golden-question set.

Phase 1 should benchmark parsers on this pack and write parser outputs/results separately. It must not modify Phase 0 ground truth to make a parser appear correct.

## 24. Handoff to later phases

### 24.1 Phase 2

Phase 2 will bind Phase 0 document/evidence locators to production manifest, canonical node, chunk, source, citation, and release identities. Phase 0 records must be migrated through an explicit reviewed mapping.

### 24.2 Phase 3

Phase 3 will use the benchmark and held-out query splits to compare embedding models and hybrid retrieval without tuning on the final release gate. Multilingual tags and retrieval categories must permit segmented reporting.

### 24.3 Phase 4

Phase 4 will resolve context and conflict labels to exact Evidence Graph edge paths, conflict IDs, positions, source IDs, and warnings. Phase 0's source-grounded cases must remain traceable after this migration.

## 25. Acceptance criteria

Phase 0 implementation is accepted only when all of the following are true.

1. The representative corpus contains 5-10 approved document records and meets every mandatory document-type/layout/edition coverage requirement.
2. No restricted source file is committed without an explicit rights-cleared decision.
3. Every selected source is bound to a SHA-256 and safe stable corpus identity.
4. The exploratory golden set contains 30-50 real questions.
5. The set includes exact identifiers, definitions, scope/applicability, source modalities, exceptions, notes, tables/units, products, references, version differences, conflicts, unanswerable/ambiguous inputs, unsupported inference, and multilingual cases.
6. Every answerable question has source-grounded expected evidence.
7. Wrong-edition, prohibited-edge, unsupported-inference, and other hard-negative fixtures are represented explicitly.
8. Context/traversal and conflict cases are defined in a form that can later migrate to exact canonical IDs and edge paths.
9. Evaluation schemas are versioned and closed enough to detect malformed or ambiguous records.
10. Reviewer, calibration, agreement, and adjudication procedures implement the design's rules.
11. Statistical tooling correctly implements one-sided 95% Wilson lower bounds and reports numerator/denominator.
12. The release-gate expansion plan identifies the minimum 150-case and 60-case requirements for the applicable probabilistic metrics and documents stratification.
13. Development, benchmark, held-out, and calibration splits have explicit leakage rules.
14. Corpus validation tests pass.
15. Markdown and repository documentation checks pass in CI.
16. A Phase 0 readiness report lists any remaining coverage gaps and does not claim release-gate readiness unless the sample requirements have actually been met.

## 26. Explicit non-goals

Phase 0 must not:

- choose the production parser;
- choose the lexical engine;
- choose the embedding model;
- choose the reranker;
- implement production chunking;
- implement the Evidence Graph;
- implement runtime context traversal;
- create final conflict records without source support;
- build a vector index;
- implement CLI/MCP behaviour;
- treat generated labels as source authority;
- infer legal enforceability;
- commit licensed standards merely to simplify CI;
- claim the 30-50 question exploratory seed satisfies the final probabilistic release gates.

## 27. Risks and mitigations

### 27.1 Corpus too easy

**Risk:** The selected documents are all clean native-text PDFs and parser/retrieval decisions overfit to simple material.

**Mitigation:** Enforce the coverage matrix before selection approval and require scan/OCR, complex table, version, reference, and mixed normative/informative cases.

### 27.2 Copyright leakage

**Risk:** Commercial standards are accidentally committed to the public repository.

**Mitigation:** Separate private/local and public corpora, default uncertain rights status to blocking review, add source-file detection, and commit hashes/metadata rather than restricted bytes.

### 27.3 Label leakage into implementation

**Risk:** Later parser/retrieval tuning repeatedly sees the held-out release labels.

**Mitigation:** Versioned splits, restricted held-out access in benchmark tooling, and separate development/benchmark data.

### 27.4 LLM-generated ground truth

**Risk:** An AI-generated summary or classification is accepted because it looks plausible.

**Mitigation:** Require source locators and human/deterministic provenance for accepted semantic labels. LLMs may propose labels but cannot be sole release-gate authority.

### 27.5 Edition contamination

**Risk:** Similar clauses from two editions are treated as interchangeable.

**Mitigation:** Bind every document/evidence label to edition and source hash; add wrong-edition negative fixtures and explicit version-comparison cases.

### 27.6 Statistical overclaiming

**Risk:** A high percentage on a small seed is presented as production accuracy.

**Mitigation:** Mark the seed exploratory, report sample counts, implement Wilson lower bounds, and block release-gate claims below the required sample sizes.

### 27.7 Evaluation schema becomes a second product model

**Risk:** Phase 0 creates identifiers or semantics that compete with the production canonical model.

**Mitigation:** Keep evaluation identity explicitly provisional/source-grounded where canonical IDs do not yet exist and require reviewed migration after Phase 2.

## 28. Recommended implementation sequence

Execute Phase 0 in this order.

1. Add corpus governance and rights-handling rules.
2. Add evaluation schemas and validators.
3. Inventory candidate documents.
4. Select and freeze representative corpus `v0001`.
5. Create preliminary source/evidence locators.
6. Author the 30-50 exploratory questions.
7. Independently review and adjudicate semantic labels.
8. Create context, vocabulary, classification, conflict, and hard-negative subsets.
9. Create multilingual variants and cross-language cases.
10. Define development/benchmark/held-out/calibration splits.
11. Implement statistical and reviewer-quality utilities.
12. Generate corpus/coverage/readiness reports.
13. Run repository and corpus validation.
14. Review known gaps.
15. Freeze the Phase 0 baseline used by Phase 1.

Each material change to accepted ground truth after step 15 must create an auditable new corpus or label-set version.

## 29. Definition of done

Phase 0 is done when another implementation agent can begin Phase 1 without needing private chat history or informal explanations to understand:

- which documents to benchmark;
- why those documents were selected;
- what evidence is expected from them;
- which questions must succeed or fail;
- how multilingual, table, edition, context, conflict, classification, and hard-negative behaviour is represented;
- how labels were reviewed;
- how later metrics will be calculated;
- which source files may or may not be redistributed;
- what constitutes a regression;
- what is still exploratory rather than release-gate evidence.

The Phase 0 corpus and labels become a controlled test asset. Later phases may extend them, but they must not weaken, silently rewrite, or bypass them in order to make an implementation pass.