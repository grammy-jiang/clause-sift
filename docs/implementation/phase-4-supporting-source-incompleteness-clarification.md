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

This is different from a blocking required-bound failure. If admitting the supporting source would cause required closure to exceed a declared required depth/object/path/step/conflict/byte bound, return `context_limit_exceeded` with no partial Evidence Package according to the existing contract.

Release-tier rules remain authoritative: unresolved required relationships that are forbidden for a critical-tier release remain release blockers and therefore cannot appear as admitted runtime evidence.

Add fixtures in which a supporting source introduces an unresolved standard-tier required reference and remains returned with the typed incomplete state, contrasted with required-bound overflow and critical-tier release-blocking cases.
