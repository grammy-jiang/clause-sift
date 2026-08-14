# Phase 4 Final Review Clarifications

**Phase:** 4 — High-Accuracy Retrieval  
**Status:** Normative Phase 4 clarification  
**Authority:** `docs/design.md`

Where an earlier Phase 4 plan conflicts with this file on the contracts below, this file is authoritative. These corrections remain strictly within Phase 4 scope.

## Required incompleteness and optional truncation may coexist

The prerequisite for Phase 4 automatic supporting traversal is that the lower-phase **required traversal/fixed-point computation has finished**, not that its resulting `context_completeness` value must be `complete`.

If an admitted unresolved required occurrence leaves the result in `incomplete_required` without a blocking required-limit failure, Phase 4 may continue the configured supporting traversal. Optional processing must not repair, hide, or remove the required-incompleteness warning.

If supporting traversal then reaches an optional bound:

- stop before the first over-bound optional candidate under the deterministic optional-order contract;
- preserve all already admitted required evidence and optional evidence;
- preserve the required-incompleteness warning(s);
- also emit the design-defined `context_truncated` warning;
- compute result-level `context_completeness` using the design precedence: `incomplete_required` takes precedence over `truncated_optional`, which takes precedence over `complete`.

Therefore both conditions and both warning families may coexist while the top-level state remains `incomplete_required`.

A blocking required failure such as `context_limit_exceeded` remains different: it returns the design-defined error with no partial Evidence Package, so optional traversal never starts on that failed result.

Add fixtures for complete-required + optional truncation, incomplete-required without optional truncation, and incomplete-required + optional truncation with both warnings and the correct top-level precedence.

## Refusal-accuracy confusion matrix is mandatory reporting

Phase 4 expanded refusal evaluation must report the design's end-to-end **refusal accuracy** metric from independently human-labelled answerability cases.

For every evaluated case, retain the versioned expected answerability label and the evaluated system outcome used by the refusal evaluator. Report the complete answerability/refusal confusion matrix, including the raw count in every cell, total applicable count, and resulting refusal-accuracy value.

The matrix must make false-answer and false-refusal decisions separately visible; they cannot be hidden inside one aggregate percentage. Preserve the label-set, split, reviewer/adjudication/calibration, candidate, and evaluation-rule identities needed to reproduce the matrix.

This is a mandatory reported end-to-end metric even when the current design does not assign it a separate Wilson release threshold. Do not invent a new threshold merely to turn reporting into a different gate. Existing human-review reliability and any separately defined release blockers still apply.

The evaluator measures the answer/refuse decision; this requirement does not introduce generated answer prose or make an LLM the release-gate authority.

## Reranker licensing approval is a blocking eligibility condition

A third-party reranker model, tokenizer, processor, weight set, runtime, or other required asset cannot become the frozen winning Phase 4 candidate merely because its benchmark quality is good.

Before a candidate is eligible for final selection/freeze and release packaging, record:

- an identified licensing/governance owner;
- the exact model/runtime/asset identity and applicable licence or usage terms;
- a versioned decision record stating whether the intended ClauseSift use, local execution, packaging/distribution, deployment, and any relevant redistribution are permitted;
- the required legal/governance review or approval when the terms or project policy require it;
- the decision status and evidence/reference needed for audit.

An unknown, unresolved, incompatible, expired, or unapproved licensing decision makes the candidate ineligible for final selection and blocks release activation. Do not silently substitute another model after decisive evaluation; selecting another model creates the appropriate new frozen candidate/evaluation identity.

Benchmark reports may retain an ineligible model's technical measurements only when collecting them was itself permitted, but must mark that candidate non-selectable and must not treat its scores as release authorization.

Add release-validation fixtures for approved, unresolved, incompatible, and changed-licence/model-revision cases.
