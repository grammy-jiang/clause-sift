# Phase 4 Automatic Supporting-Context Plan

**Project:** ClauseSift  
**Phase:** 4 — High-Accuracy Retrieval  
**Status:** Normative Phase 4 implementation-plan appendix  
**Primary design authority:** `docs/design.md` Sections 17, 19-22, 29, and 31  
**Companion:** `docs/implementation/phase-4-high-accuracy-retrieval.md`

## 1. Purpose

Phase 2 already implements:

- required Evidence Graph closure for ordinary evidence;
- material-conflict fixed-point closure;
- explicit Python/MCP `get_context(required|supporting|diagnostic)` inspection.

Phase 4 adds a different capability: **automatic supporting-context expansion as part of ordinary `high_accuracy` search**.

This appendix defines that boundary so Phase 4 neither reimplements Phase 2 required context nor accidentally makes diagnostic context automatic.

## 2. Runtime ordering

High-accuracy context processing follows this order:

```text
final reranked direct seeds
  -> Phase 2 required graph closure
  -> Phase 2 material-conflict closure
  -> repeat to required fixed point
  -> Phase 4 supporting traversal
  -> for each candidate optional source, prove its required consequences can remain complete
  -> retain optional source only if admission is safe/in-bound
  -> continue supporting queue until complete or deterministic truncation
  -> strict Evidence Package serialization
```

Supporting traversal never runs before the current required fixed point is complete.

## 3. Context-level boundary

Automatic Phase 4 high-accuracy search uses:

- `required` context, inherited from Phase 2;
- `supporting` context, added automatically by Phase 4.

It does **not** automatically include `diagnostic` context.

Diagnostic adjacency/version inspection remains available only through explicit Python/MCP `get_context(context_level="diagnostic")` or another future design-defined inspection surface.

## 4. Supporting rule authority

Use only the current Section 19 supporting rules and their exact direction/intent/stop semantics.

Supporting eligibility may include the design-defined forms such as:

- uniquely resolved direct `references` targets under the supporting rule;
- non-empty structural ancestors through the admitted scope under the current rule;
- direct supporting note/footnote/table children under current endpoint rules;
- version/amendment endpoints when the query has the required deterministic version-comparison intent.

The detailed design remains authority for every endpoint class/direction/recursion/stop condition.

Do not create supporting context from:

- similarity alone;
- unresolved/ambiguous occurrences;
- sibling proximity;
- guessed edition/clause mapping;
- second-hop generic references not admitted by the supporting rule;
- diagnostic `precedes` adjacency in ordinary high-accuracy search.

## 5. Supporting candidate ordering

Use the current deterministic context queue/order from Section 19.

Phase 4 must not introduce a second optional-context ordering algorithm merely because a reranker exists.

Supporting order remains explainable through:

- context class;
- originating seed final rank;
- source identity;
- path length;
- relation-type ranks;
- target canonical identity/order;
- edge IDs.

No model score may change graph edge authority or traversal direction.

## 6. Required consequences of an optional source

Accepting a supporting source cannot create a context-incomplete final package.

Before an optional source becomes final evidence:

1. identify the exact canonical source/target;
2. account for its complete source bytes and object/path/reason cost;
3. run or prospectively validate every Phase 2 required graph obligation induced by that source;
4. preserve every material conflict side reached by that source;
5. ensure newly required sources can also close to the required fixed point;
6. accept the optional source only when the resulting required closure remains valid and in-bound.

A supporting source is never admitted first and then left with missing required applicability/exception/conflict context.

## 7. Optional truncation semantics

If the next supporting candidate or any required consequence of admitting it would exceed an optional/request/output bound:

- do not admit that optional candidate;
- stop optional traversal before it in deterministic priority order;
- keep the complete required fixed point already produced;
- set `context_completeness: "truncated_optional"`;
- emit the current typed `context_truncated` warning with safe configured/observed details;
- return no partial form of that rejected optional candidate or its required consequences.

Optional truncation cannot remove/replace direct seeds, required context, or material conflict sides.

## 8. Current bounds

Phase 4 reuses the existing Section 19 request bounds; it does not silently increase them to make supporting context fit.

Important shared bounds include:

- supporting semantic depth 1;
- diagnostic depth 2 (not automatic in high-accuracy search);
- 128 expanded context objects excluding direct seeds;
- 32 unique paths per context object;
- 1,024 accepted path steps;
- existing conflict/position/span/reason limits;
- complete Section 22/MCP output/frame limits.

Any design-approved future bound change is behavior-bearing release identity and must be reevaluated.

## 9. Supporting-source materialization

Use the same source-faithful Phase 2 materialization rules.

- Source-bearing target -> canonical source/chunk/node coverage with original text/citation/lineage.
- Empty structural target -> metadata-only `context_targets` record, never fabricated source text.
- Already returned source -> merge roles/paths rather than duplicate by text similarity.
- Different edition/status -> preserve actual identity/status and emit the current boundary warning where required.

Supporting status never promotes informative/recommended material to normative/required authority.

## 10. Version and amendment context

Supporting traversal of `supersedes`/`amends` follows the current deterministic version-intent contract.

Phase 4 must not:

- automatically add newer/older editions for every query;
- replace a requested historical edition with an active edition;
- match same-number clauses across editions without a validated edge;
- turn version context into controlling legal precedence.

When admitted, every version-context item preserves its real edition/status/source authority and the current typed status-boundary warning behavior.

## 11. Table supporting context

Phase 4 high-accuracy table improvements should improve retrieval/reranking/supporting materialization without changing the lower-phase source model.

Cover:

- table title/header/unit preservation;
- exact row identity;
- nearest addressable clause context;
- multi-page table provenance;
- natural-language query alignment to row/header/unit meaning;
- similar numeric hard negatives from other tables/editions;
- no invented header/unit/row repair.

If table title/header/unit is required for a direct/accepted source's correctness, it remains required context and cannot be treated as optional to avoid a failure.

## 12. Cross-reference supporting context

Only uniquely resolved, release-authorized supporting references are navigable.

Phase 4 improves the usefulness of resolved cross-reference context but does not:

- follow unresolved/ambiguous rows;
- use similarity to repair missing targets;
- convert generic reference into a required dependency;
- follow unbounded reference chains;
- merge document editions.

A target required to complete meaning should already be represented by the lower-phase `depends_on`/required context contract rather than a Phase 4 optional reference.

## 13. Interaction with reranking

Reranking orders direct source candidates. Supporting context does not get to retroactively change source authority or rerank already selected direct evidence by an undocumented second model.

If the design permits ranking among optional supporting candidates, it must remain deterministic/versioned and cannot bypass Section 19 traversal order/authority. The initial implementation should reuse the current graph queue rather than introduce another learned optional-context ranker.

## 14. Assembly lineage

For supporting items retain the existing closed assembly fields:

- `selection_roles` including expanded context as applicable;
- originating `seed_source_ids`;
- complete accepted context paths;
- every path step's validated edge/origin groups/rule ID;
- completeness state;
- typed warnings;
- material conflict reasons where the optional source induces required conflict closure.

Do not write query-specific supporting paths into immutable `lineage.json`.

## 15. Warning behavior

Supporting traversal can surface current warnings including:

- `context_truncated`;
- `context_cycle_detected`;
- `context_status_boundary`;
- `cross_reference_unresolved` when the requested/encountered relation semantics require it;
- parser/OCR/classification/source-coordinate diagnostics on attached evidence;
- material conflict warnings induced by accepted supporting evidence.

Never suppress a lower-phase warning because the item is "only supporting".

## 16. Evaluation corpus

Create independently reviewed supporting-context labels that distinguish:

- required evidence;
- useful supporting evidence;
- irrelevant but topically similar evidence;
- diagnostic-only material;
- wrong-edition/wrong-document context;
- false sibling/adjacency context;
- resolved vs unresolved cross-reference targets;
- relevant vs irrelevant tables/notes/version context.

Labels must be granular enough to measure optional-context precision by relation/context family and expose false expansion hidden by a global average.

## 17. Supporting-context precision gate

Use the **exact optional-context precision gate defined by current `docs/design.md` Section 29.4**, including its current one-sided Wilson confidence-bound target, minimum applicable sample size, and stratification expansion rules.

The implementation plan must not substitute a different locally invented threshold if the detailed design changes.

Report at minimum:

- correct optional attachments;
- incorrect optional attachments;
- applicable total;
- point estimate;
- one-sided Wilson lower bound;
- target;
- context/relation family;
- corpus/split/reviewer versions;
- frozen Phase 4 supporting/routing configuration identity.

The gate evaluates automatic high-accuracy supporting context, not Phase 2 required closure.

## 18. Deterministic conformance

In addition to the probabilistic precision gate, require zero failures across deterministic suites for:

- required-before-supporting ordering;
- only validated supporting edges followed;
- no diagnostic auto-expansion;
- no wrong-edition substitution;
- complete required consequences for accepted optional sources;
- material conflict preservation;
- exact optional truncation behavior;
- context path/order/provenance;
- no optional item after truncation boundary;
- no source authority promotion.

## 19. Negative tests

Reject/prove absence of:

- unresolved reference traversal;
- generic second-hop reference auto-expansion;
- sibling exception guessing;
- diagnostic adjacency added to high-accuracy answer;
- optional source admitted without required applicability/conflict side;
- optional source admitted partially across an overflow;
- supporting context replacing a direct seed;
- wrong-edition same-clause substitution;
- generated table header/unit repair;
- hidden suppression of `context_truncated`.

## 20. Suggested implementation sequence

1. freeze the Phase 4 automatic supporting-context configuration/version;
2. reuse Phase 2 traversal/materialization interfaces rather than fork them;
3. add high-accuracy post-required supporting traversal entry point;
4. implement prospective optional admission including required consequences;
5. implement deterministic optional truncation;
6. add version/table/cross-reference high-accuracy fixtures;
7. integrate supporting paths/warnings through closed serializer;
8. build reviewed supporting-context evaluation labels;
9. tune only on development/model-selection evidence;
10. freeze Phase 4 supporting configuration;
11. run deterministic conformance/negative suites;
12. run the current Section 29.4 optional-context precision gate on decisive data;
13. run performance/output-size/cancellation tests;
14. validate release/activation/rollback integration.

## 21. Acceptance criteria

Automatic supporting context is complete only when:

1. it starts only after complete required graph/conflict closure;
2. only current supporting rules are automatic;
3. diagnostic context is never silently included;
4. every accepted supporting source preserves its own required context/conflicts;
5. optional truncation is deterministic and never removes required evidence;
6. source/edition/status identity and authority are preserved;
7. table/cross-reference behavior is source-grounded and does not guess missing structure/targets;
8. assembly provenance uses existing closed schemas;
9. deterministic supporting/truncation/negative suites pass;
10. the exact current Section 29.4 optional-context precision gate passes under leakage-safe decisive evidence;
11. optional context performance/output growth is measured after correctness;
12. Phase 2 explicit `get_context` and Phase 4 automatic high-accuracy supporting expansion remain distinct, non-duplicated implementations.
