# Phase 4 Implementation Plan: High-Accuracy Retrieval

**Project:** ClauseSift  
**Phase:** 4 of the design-defined implementation sequence  
**Status:** Canonical implementation plan  
**Primary design authority:** `docs/design.md`  
**Product intent:** `docs/design-brief.md`  
**Design principles:** `docs/design-principles.md`

## 1. Objective

Phase 4 completes ClauseSift's first high-accuracy retrieval path without replacing the source-grounded evidence architecture established by earlier phases.

Phase 4 consumes:

- Phase 2 exact/lexical retrieval, canonical IDs, required Evidence Graph closure, material-conflict fixed point, strict Evidence Package service, lineage, interfaces, release lifecycle, and quality/security baseline;
- Phase 3 deterministic query preprocessing/classification, chunk embeddings, exact dense retrieval, lexical+dense fusion, hybrid provenance, and release-bound model/vector configuration.

Phase 4 adds:

1. a benchmark-selected local cross-encoder reranker;
2. a deterministic high-accuracy candidate/rerank path using exact, lexical, and dense evidence candidates;
3. automatic **supporting-context** expansion for `high_accuracy` search after complete required graph/conflict closure;
4. the current high-accuracy table/cross-reference improvements assigned by the design;
5. expanded warning/insufficiency/refusal-support evaluation;
6. high-accuracy release/capability/cache/lineage integration;
7. final quality, latency, memory, cancellation, integrity, activation, and rollback gates.

Phase 4 does not add generated answers or transfer source authority to a model.

## 2. Phase boundary

### 2.1 In scope

Phase 4 implements and validates:

- cross-encoder candidate-model benchmark/selection;
- deterministic model-specific query/candidate pair preprocessing for each reranker candidate;
- complete local reranker asset/loader identity and safe loading;
- bounded candidate-pool selection for high-accuracy mode;
- exact/lexical/dense candidate preservation and edition-safe deduplication;
- deterministic cross-encoder scoring and total ordering;
- high-accuracy final seed selection;
- runtime lazy reranker loading through the common supervised model lifecycle;
- release/runtime capability detection for high-accuracy mode;
- explicit `high_accuracy` mode and `auto` resolution when high-accuracy capability is available;
- required Phase 2 graph/conflict fixed point for the final ranked seeds;
- automatic Section 19 **supporting** traversal for high-accuracy search;
- required closure for every accepted supporting source before it can become final evidence;
- material-conflict preservation for supporting evidence;
- deterministic optional-context truncation after complete required closure;
- high-accuracy table/cross-reference behavior assigned by current design;
- typed warning/insufficiency behavior and refusal-support evaluation;
- high-accuracy retrieval/assembly provenance using the existing closed Evidence Package schema;
- release/cache/model-asset/configuration identity;
- cold/warm/model-free comparative performance measurement;
- high-accuracy quality gates and hard-negative evaluation;
- cancellation/deadline/resource-admission/quarantine/security tests;
- activation and rollback integration.

### 2.2 Out of scope

Phase 4 must not implement:

- generated engineering answers or summaries as source authority;
- LLM-based authoritative query rewriting;
- LLM-based applicability/conflict/precedence decisions;
- new probabilistic graph edges without an explicit future design change;
- automatic diagnostic-context expansion in ordinary search;
- silent removal of exact/lexical/dense channels to improve latency;
- ANN solely because it is conventional;
- an external vector/search/database service;
- document redistribution;
- autonomous design approval or legal conclusions;
- product/version intelligence beyond the current first-release design boundary.

## 3. Governing invariants

Phase 4 preserves all lower-phase correctness contracts.

1. Original source bytes and approved manifest facts remain authoritative.
2. Reranker scores are non-authoritative selection metadata only.
3. Reranking can reorder canonical candidates but cannot create/merge document, edition, chunk, source, or graph identity.
4. Exact anchors and exact metadata filters cannot be erased by semantic/reranker similarity.
5. Wrong-edition near-duplicates remain distinct candidates and hard negatives.
6. Every final high-accuracy seed enters the Phase 2 required graph/conflict fixed point.
7. Supporting context begins only after complete required closure for current seeds.
8. Every accepted supporting source must retain its own required applicability/exception/dependency context and material conflict sides.
9. Required evidence is never truncated to fit optional context.
10. Optional supporting context may be truncated only under the current deterministic `truncated_optional` contract.
11. Diagnostic context remains explicit inspection only and is never enabled automatically by high-accuracy mode.
12. Immutable `lineage.json` remains query-independent; rerank/context decisions are request-scoped assembly provenance.
13. Public Evidence Package objects remain the current closed schema; Phase 4 cannot add ad-hoc score/explanation fields without a versioned design change.
14. Explicit unavailable `high_accuracy` fails visibly; `auto` fallback is typed and never silent.
15. Model/load/integrity failures use the common runtime terminal-state/quarantine contract.
16. Quality gates precede latency optimization.

## 4. Canonical high-accuracy runtime path

The Phase 4 path is conceptually:

```text
validated request
  -> Phase 3 deterministic query preprocessing/analysis
  -> exact candidate channel
  -> lexical candidate channel
  -> dense candidate channel
  -> deterministic high-accuracy candidate fusion/assembly
  -> cross-encoder reranking
  -> final ranked direct source seeds
  -> Phase 2 required graph + material-conflict fixed point
  -> Phase 4 automatic supporting-context traversal
  -> required closure/conflict preservation for every accepted supporting source
  -> deterministic optional truncation if necessary
  -> strict Phase 2 Evidence Package serializer
  -> Python / CLI / MCP result
```

The exact/lexical/dense candidate pool and reranker do not bypass the Phase 2 evidence service.

## 5. High-accuracy candidate contract

Phase 4 consumes lower-phase typed candidates, not backend-native arrays/model objects.

A rerankable candidate retains:

- canonical `document_id`;
- `chunk_id`;
- `source_id`;
- exact edition/status metadata needed by the candidate/filter contract;
- lower-phase retrieval-channel provenance;
- lower-phase fused rank/score/configuration where applicable;
- exact/direct-anchor metadata where applicable;
- release identity;
- no generated source text or interpretation.

Candidate deduplication uses canonical source/chunk identity, never normalized-text equality.

## 6. Exact-channel preservation

The current design's high-accuracy path includes exact lookup alongside lexical/dense retrieval.

Phase 4 must preserve deterministic exact anchors by either:

- feeding exact candidates through the versioned high-accuracy fusion/assembly contract; or
- injecting exact candidates through an equivalently deterministic design-conformant candidate stage that guarantees they cannot be silently discarded before reranking.

The implementation must freeze one behavior and prove it through evaluation. It may not invent a hidden exact boost after seeing held-out failures.

Exact candidate handling is part of the frozen Phase 4 candidate identity.

## 7. Candidate-pool sizing

The design's initial candidate-count ranges are hypotheses, not permanent constants.

Benchmark bounded configurations around the current starting guidance, including:

- lexical/dense candidate pools in the design's initial range;
- reranker input pool around the initial top-20-to-30 guidance;
- final direct evidence seeds around the initial top-8-to-12 guidance;
- exact-channel inclusion policy;
- any high-accuracy fusion parameters that differ from Phase 3.

Select values using accuracy/hard-negative evidence first. A smaller pool cannot win solely because it is faster.

## 8. Query analysis and mode resolution

Phase 3 already provides deterministic query analysis/classification and a high-accuracy-intent signal. Phase 4 activates the real `high_accuracy` path without replacing deterministic routing with an LLM.

For explicit `high_accuracy`:

- require every capability the active release/runtime declares necessary for the high-accuracy path;
- if a required dense/reranker capability cannot execute, return `feature_unavailable` through the current contract rather than silently relabeling hybrid/exact output as high accuracy.

For `auto`:

- resolve only among installed + active-release capabilities;
- if high-accuracy/dense/reranker capability is unavailable and `auto` uses a lower path, include `retrieval_capability_unavailable` as required by current design;
- record the concrete resolved mode in the existing assembly/package contract.

Any Phase 4 routing-rule change is behavior-bearing candidate/release/evaluation identity.

## 9. Reranker input boundary

Cross-encoder input is deterministic retrieval input, never evidence authority.

For each candidate model, freeze the exact query/candidate preprocessing needed by that model before benchmarking, including as applicable:

- query prefix/template/role marker;
- candidate/document role marker;
- deterministic candidate text projection;
- heading/document-code context admitted by the design;
- tokenizer configuration;
- max length/truncation policy;
- pair ordering;
- Unicode/whitespace normalization;
- model/provider asset/configuration identity.

Candidate-specific preprocessing may differ across benchmarked reranker models. Selection chooses the **model + preprocessing projection** together. The winning projection is reused unchanged in later tuning, final confirmation, and production.

Reranker input never replaces `original_text` in returned evidence.

## 10. Reranker scoring and deterministic ordering

The reranker returns finite model scores for the admitted candidate pool.

Validate:

- exact model/revision/assets/configuration compatible with active release;
- finite scores;
- one result per input candidate;
- no duplicate/lost candidate identity;
- deterministic candidate batching/order;
- deterministic total final order.

Freeze a total tie-break chain ending in canonical document/chunk/source identity. Hash-map iteration, batch scheduling, or backend order cannot decide a tie.

## 11. Supporting-context automatic expansion

After final direct seeds complete the Phase 2 required graph/conflict fixed point, high-accuracy mode executes the current Section 19 **supporting** rule set automatically.

This is distinct from Phase 2 explicit `get_context(supporting|diagnostic)`: Phase 4 makes supporting traversal part of ordinary `high_accuracy` search.

Diagnostic traversal remains explicit inspection only.

## 12. Supporting-context correctness

For each optional supporting candidate:

1. follow only release-validated supporting-eligible edges/directions/intents;
2. preserve exact source/document/edition/status identity;
3. before accepting the optional source into final evidence, ensure all required context/conflict obligations induced by that source can be completed;
4. preserve every accepted supporting path/reason through the closed assembly schema;
5. never promote an informative note/reference to normative authority because it was attached;
6. never use optional traversal to bypass direct-seed metadata or applicability rules.

A supporting source that would require incomplete/over-bound required closure cannot be partially admitted.

## 13. Optional truncation

Optional supporting traversal follows the current deterministic queue/order/bounds from Section 19.

When the next optional candidate (including the required consequences of admitting it) would exceed a bound:

- stop before that optional candidate;
- retain the complete required fixed point already produced;
- set `context_completeness: truncated_optional`;
- emit `context_truncated` with the permitted safe configured/observed details;
- do not drop earlier required evidence or conflict sides.

## 14. Supporting relationship classes

Use only current design supporting rules. Examples include the design-defined direct references, non-empty structural ancestors, direct supporting note/footnote/table children, and version/amendment context under the exact required version-comparison intent rules.

Do not make `precedes` adjacency or generic second-hop references automatic high-accuracy evidence merely because they are available diagnostically.

Required relationships remain Phase 2 and run independently of supporting traversal.

## 15. Table and cross-reference high-accuracy work

Phase 4 owns the high-accuracy table/cross-reference improvements explicitly assigned by current design.

Implementation work should focus on improving candidate reranking and supporting materialization/selection while preserving lower-phase authority, including:

- table-title/header/unit/row context fidelity;
- ranking table representations against natural-language queries;
- resolved cross-reference supporting context;
- explicit version/amendment intent handling;
- hard negatives where cited/similar tables or clauses are wrong edition/document;
- no navigation of unresolved/ambiguous references;
- no generated repair of missing table/cross-reference structure.

If an issue is actually an ordinary required-context correctness defect, fix it in the lower-phase contract rather than redefining it as optional Phase 4 behavior.

## 16. Warning and insufficiency behavior

Phase 4 preserves all lower-phase warnings and expands high-accuracy evaluation coverage.

At minimum evaluate correct handling of:

- `retrieval_capability_unavailable` on `auto` fallback;
- `evidence_insufficient` when no adequate evidence is found;
- `applicability_incomplete` where applicability remains incomplete under the design rules;
- `context_incomplete`/unresolved reference diagnostics;
- `context_truncated` for optional truncation;
- `evidence_conflict`;
- `conflict_unresolved`;
- parser/OCR/classification/source-coordinate warnings;
- feature/load/integrity errors.

Phase 4 does not invent generated refusal prose as a new source of truth. Warning/refusal evaluation exists so downstream clients can deterministically avoid presenting unsupported high-confidence answers.

## 17. Evidence Lineage and closed schema

Phase 4 extends release identity with query-independent reranker model/configuration/assets and any Phase 4 behavior configuration.

At runtime, use only existing closed Section 21 fields:

- `assembly.retrievals[]` for contributing retrieval channels;
- existing `fusion` object for the fusion stage;
- existing `rerank` object for reranker model/revision/configuration/artifact-set/rank/score;
- package-level `retrieval_mode`;
- `selection_roles`, `seed_source_ids`, context paths, conflict reasons, warnings.

Do not add arbitrary model explanation strings, attention values, classifier IDs, or per-token rationale without a versioned design/schema change.

## 18. Release and cache identity

Bind every behavior-bearing Phase 4 input, including:

- reranker model ID/revision;
- complete local model/tokenizer/processor asset table/digest;
- safe model format and loader ID/version;
- model-specific query/candidate preprocessing identity;
- rerank candidate-pool configuration;
- final seed-count configuration;
- exact-channel handling/high-accuracy fusion configuration;
- deterministic tie-break/version;
- high-accuracy routing/classifier configuration if changed;
- supporting-context rule/configuration identity already present in the release;
- relevant dependency-lock/toolchain identity;
- evaluation/gate report identities required by release policy.

A behavior-bearing change invalidates stale Phase 4 decisive evidence and affected caches/release identity.

## 19. Runtime model lifecycle

Reuse the common supervised lazy-model loader and terminal-state machinery.

Reranker loading must:

- verify every allowlisted local asset size/hash before deserialization;
- use only safe admitted model formats/loaders;
- bind exact model/tokenizer/processor/loader configuration to active release;
- single-flight concurrent loads;
- obey per-attempt model-load and caller overall deadlines;
- remain cancelable under the common worker contract;
- expose a handle only after successful validation/load;
- quarantine/fail the release under current integrity rules if a lazy asset check fails;
- never write model-loader logs to protocol stdout.

## 20. Performance measurement

Measure separately:

- Phase 3 hybrid candidate latency before rerank;
- reranker cold load;
- warm rerank latency by candidate pool size;
- required closure latency;
- supporting traversal latency;
- complete high-accuracy cold/warm latency;
- peak/incremental RSS;
- model asset size;
- candidate-pool sensitivity;
- optional-context growth/output size;
- cancellation/deadline behavior under model load/rerank/context expansion.

Performance optimization is allowed only after quality gates pass.

## 21. Security and privacy

Preserve local-first behavior:

- no network access at runtime by default;
- no pickle/arbitrary-code model assets;
- checksum/allowlist every file a loader can open;
- no query/source text in unrestricted logs;
- no source/workspace paths in public results;
- no client-supplied model path/template/rule executable content;
- malformed requests rejected before model work;
- optional context and reranking remain bounded and cancelable.

## 22. Evaluation strategy

Keep these data roles separate:

1. development diagnostics;
2. reranker model/preprocessing selection;
3. candidate-pool/routing/supporting-context tuning;
4. final decisive confirmation.

Freeze the complete Phase 4 candidate identity before final confirmation. Do not repeatedly tune against observed decisive data.

The selected reranker must be evaluated on real ClauseSift engineering evidence, not generic leaderboard reputation.

## 23. Evaluation slices

Include at minimum:

- English/Chinese/cross-language natural-language queries;
- exact anchors embedded in natural-language questions;
- HVAC/fire-safety terminology;
- numbers/units;
- negation/exceptions;
- same wording across editions;
- near-duplicate wrong-document clauses;
- table rows with similar numeric patterns;
- resolved cross-references;
- applicability-sensitive questions;
- multi-document questions;
- material conflicts;
- no-answer/evidence-insufficient cases;
- capability-unavailable/fallback cases;
- optional-context precision cases;
- latency/resource stress cases.

Compare at least Phase 3 hybrid vs Phase 4 reranked high-accuracy results so improvements/regressions are visible by stratum.

## 24. Test plan

### Unit

- reranker pair preprocessing;
- model/asset identity;
- safe-loader metadata;
- score validation;
- deterministic tie-break;
- exact-channel preservation;
- candidate deduplication;
- mode/capability resolution;
- supporting-rule selection;
- optional truncation;
- rerank provenance serialization.

### Integration

- warm/cold explicit high-accuracy request;
- `auto` selects high accuracy when capable;
- `auto` typed fallback when capability unavailable;
- explicit high-accuracy unavailable error;
- exact anchor survives rerank;
- wrong-edition semantic hard negative;
- final seeds receive Phase 2 required graph/conflict fixed point;
- automatic supporting traversal only in high-accuracy search;
- supporting source receives its own required context/conflicts;
- optional truncation keeps complete required evidence;
- Python/CLI/MCP overlapping high-accuracy semantics;
- rollback to Phase 3/earlier release capability.

### Negative/boundary

- NaN/Inf reranker score;
- output/input count mismatch;
- wrong model/revision/assets;
- unsupported loader/format;
- corrupted lazy model asset/quarantine;
- model-load timeout;
- canceled rerank;
- deadline during supporting traversal;
- too-large candidate pool rejected/config-invalid;
- supporting source whose required consequences would exceed bounds;
- unresolved reference never followed;
- diagnostic adjacency never auto-added;
- false precedence/source-authority promotion prohibited.

## 25. Suggested implementation sequence

1. freeze Phase 4 candidate/reranker/supporting-context interfaces;
2. implement benchmark harness and candidate-specific pair preprocessing;
3. benchmark/select reranker model+preprocessing on non-decisive data;
4. bind safe local assets/loader identity;
5. implement lazy supervised reranker load;
6. implement high-accuracy candidate assembly including exact-channel preservation;
7. implement deterministic rerank scoring/order;
8. select/freeze candidate-pool/final-seed configuration;
9. activate deterministic high-accuracy mode/auto routing;
10. integrate final seeds with Phase 2 required graph/conflict service;
11. enable automatic supporting traversal after required completion;
12. implement high-accuracy table/cross-reference improvements;
13. validate optional truncation and supporting-source required consequences;
14. integrate rerank/supporting provenance through closed schema;
15. add release/cache/capability identity;
16. expand warning/insufficiency/refusal-support evaluation;
17. run quality/hard-negative/conformance tests;
18. run cold/warm/resource/cancellation/security tests;
19. freeze complete Phase 4 candidate identity;
20. run decisive held-out/confirmation gates under leakage-safe policy;
21. assemble/reopen/validate candidate release;
22. verify activation/rollback;
23. update final Phase 4 decision/evidence report.

## 26. Definition of Done

Phase 4 is complete only when:

1. the reranker model+preprocessing is selected by project-specific evidence;
2. complete local model assets/loader identity are release-bound and safe-loaded;
3. high-accuracy candidate assembly preserves exact/lexical/dense identity and exact anchors;
4. reranking is deterministic and provenance-complete;
5. explicit high-accuracy and `auto` capability behavior follows current typed warning/error contracts;
6. every final seed receives complete Phase 2 required graph/conflict closure;
7. automatic supporting context executes only after required completion and never admits partial required consequences;
8. optional truncation preserves complete required evidence and is visible;
9. table/cross-reference high-accuracy behavior is source-grounded and edition-safe;
10. strict existing Evidence Package schemas are preserved;
11. all applicable Phase 4 retrieval/optional-context/warning/refusal-support gates pass with correct decisive-data governance;
12. exact/lexical/hybrid lower-phase behavior has no unacceptable critical regression;
13. cold/warm memory/latency is measured after correctness;
14. cancellation/deadline/admission/integrity/quarantine/security tests pass;
15. immutable release activation and rollback pass;
16. no generated answer, graph fact, applicability fact, or precedence decision becomes source authority.

## 27. Final project handoff

Phase 4 is the last design-defined implementation-plan phase in the current sequence. After merge, the repository has a complete implementation plan from Phase 0 through Phase 4 aligned with current `docs/design.md`.

Any future phase or scope extension must begin from an explicit design change rather than silently expanding Phase 4.
