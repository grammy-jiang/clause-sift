# Phase 4 Supporting-Source Required-Incompleteness Clarification

**Phase:** 4 — High-Accuracy Retrieval  
**Status:** Normative Phase 4 clarification  
**Authority:** `docs/design.md` Section 19 and Section 31

This file supersedes the Phase 4 supporting-context sentence that requires every admitted supporting source to produce a `complete` required closure before it may remain in the Evidence Package.

A supporting source is not discarded merely because that source itself introduces an admitted unresolved required occurrence.

For a standard-tier source whose required traversal encounters an unresolved required occurrence that the governing lower-phase policy permits to remain source-faithful:

1. retain the supporting source and every already validated required/conflict consequence;
2. do not invent a target or silently remove the source;
3. emit the design-defined `context_incomplete` and/or `cross_reference_unresolved` warning as applicable;
4. set/retain result-level `context_completeness` as `incomplete_required` under the normal precedence rule;
5. continue deterministic processing of other admitted obligations/optional candidates while respecting all existing bounds and warning rules.

## Optional-candidate bound semantics

A supporting source and every required/conflict consequence that would be induced by admitting it are evaluated prospectively as one optional candidate before that candidate is committed to the result.

If that prospective optional candidate would exceed a depth/object/path/step/conflict/reason/output bound:

- do **not** admit the supporting source or any consequence introduced only by that candidate;
- stop optional traversal before that candidate under the deterministic optional ordering;
- preserve the already completed required fixed point and every earlier admitted optional object;
- emit `context_truncated`;
- use `context_completeness: "truncated_optional"` unless an already-existing `incomplete_required` condition has precedence, in which case the top-level value remains `incomplete_required` while the truncation warning is still retained.

`context_limit_exceeded` with no partial Evidence Package remains reserved for a required closure that is already mandatory independently of optional supporting admission, such as required closure originating from direct retrieval seeds or another already-admitted required object.

Release-tier rules remain authoritative: unresolved required relationships that are forbidden for a critical-tier release remain release blockers and therefore cannot appear as admitted runtime evidence.

Add fixtures for a supporting source that introduces an unresolved standard-tier required reference; a supporting source whose prospective induced closure is exactly at the bound; one whose prospective closure is one over and is therefore not admitted while optional traversal truncates; a direct-seed required closure that exceeds the same bound and fails with `context_limit_exceeded`; and critical-tier release-blocking cases.
