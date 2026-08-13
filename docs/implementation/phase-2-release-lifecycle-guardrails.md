# Phase 2 Release Lifecycle Guardrails

**Project:** ClauseSift  
**Phase:** 2 — Exact Retrieval MVP  
**Status:** Normative Phase 2 implementation-plan appendix  
**Primary design authority:** `docs/design.md`  
**Companion plans:** `phase-2-exact-retrieval-mvp.md`, `phase-2-release-gates.md`, `phase-2-held-out-retry-policy.md`

## 1. Purpose and precedence

This appendix closes two Phase 2 release-lifecycle edge cases:

1. repeated fresh held-out attempts must not become an unbounded stop-on-pass procedure;
2. a newly initialized workspace has no active release and therefore must not contain a placeholder `active.json`.

It is strictly limited to Phase 2 evaluation governance and immutable-release activation. It does not add Phase 3 or Phase 4 behavior.

Where another Phase 2 document permits multiple decisive reserve attempts or implies that `clausesift init` creates `active.json`, this appendix is authoritative and narrows that behavior.

## 2. One release campaign, one non-retried confirmation decision

A Phase 2 **release campaign** is the preregistered attempt to qualify one Exact Retrieval MVP release objective under a fixed design/gate version and evaluation methodology.

Before any held-out result is observed, the campaign records:

- campaign ID and schema version;
- design/gate versions;
- Phase 0 corpus/split/rubric versions;
- Phase 2 canonical-ID migration version;
- candidate-selection benchmark split;
- optional screening-reserve allocation;
- exactly one final confirmation split or a deterministic blinded procedure that allocates it without exposing labels;
- required sample counts and strata for every applicable gate;
- the rule that final confirmation is not retried within the campaign.

Changing a candidate does not reset the campaign or create a new statistical error budget.

## 3. Screening reserves are non-decisional

The project may preregister at most **two** fresh screening-reserve evaluations before final confirmation when additional evidence is operationally justified.

A screening reserve:

- uses an unseen independent split;
- follows the same label/migration integrity rules;
- is marked `screening_only`;
- may block advancement to final confirmation;
- cannot itself authorize activation;
- becomes observed and retired immediately after use;
- cannot be reused for a changed candidate;
- cannot be selected or skipped based on unseen performance.

The finite screening limit prevents indefinite sequential probing. A campaign cannot create a third screening reserve after observing two screening results.

Screening results are retained in the campaign report and cannot be hidden because a later candidate performs better.

## 4. Final confirmation is decisive and non-retried

Only the **single preregistered final confirmation split** produces the release-authoritative probabilistic pass/fail decision.

The final candidate is frozen before the confirmation labels/results are exposed. The confirmation run evaluates all applicable Phase 2 probabilistic gates using the design-required one-sided 95% Wilson lower bounds and the applicable Phase 0 minimum/stratified sample rules.

Because there is exactly one decisive confirmation run per campaign, the nominal one-sided 5% error budget is not multiplied by repeated stop-on-pass decisive attempts.

If final confirmation fails any applicable gate:

- the campaign fails;
- activation is blocked;
- the confirmation split becomes observed and retired;
- no materially changed candidate may receive another decisive confirmation in the same campaign;
- the prior active release remains unchanged;
- all screening and confirmation results remain visible in the campaign history.

A deterministic replay of the exact same candidate and exact same confirmation split is allowed only as `reproduction_only`; it cannot alter the campaign's original pass/fail decision.

## 5. Starting a later campaign after confirmation failure

A failed campaign cannot be relabelled or restarted merely to obtain another draw from the same statistical procedure.

A later campaign requires all of the following before any new held-out evidence is exposed:

- a new preregistered campaign identity;
- a materially documented remediation hypothesis derived from development/benchmark evidence rather than hidden labels from unused confirmation data;
- a new independently constructed and reviewed final confirmation split with no forbidden overlap with prior development, benchmark, screening, or confirmation cases;
- Phase 0 change-control compliance for any corpus/rubric/split changes;
- a fresh reviewed Phase 2 canonical-ID migration for the new cases;
- explicit retention of the prior failed campaign in aggregate release history.

The governance record must explain why the later campaign is a new engineering validation cycle rather than a continuation of stop-on-pass retries. Repeated campaign creation without materially new evidence or remediation is invalid.

## 6. Error-budget reporting

Every campaign report includes:

- zero, one, or two screening results;
- exactly one final confirmation result when the campaign reaches confirmation;
- the candidate identity used for each run;
- split identities and observation/retirement state;
- all five applicable Phase 2 probabilistic gate results;
- sample counts and Wilson bounds;
- the reviewed canonical-ID migration hash;
- campaign outcome;
- prior related failed-campaign references.

A release report must never present a screening result as the decisive 95% gate or omit a failed earlier screening/confirmation result from the same campaign.

## 7. Retry-policy correction

`phase-2-held-out-retry-policy.md` remains authoritative for split retirement, candidate identity, reproduction-only replay, and leakage rules, with this correction:

- reserve splits after candidate changes are **screening-only**, not successive decisive gates;
- no more than two screening reserves may be consumed in one campaign;
- exactly one unseen confirmation split is decisive;
- confirmation failure ends the campaign;
- a new campaign requires new independent confirmation data plus documented remediation and cannot be opened solely to keep trying until a pass appears.

This structure provides the finite attempt budget and separate non-retried confirmation gate required to prevent sequential stop-on-pass inflation.

## 8. Workspace initialization before the first release

`clausesift init <workspace>` creates the workspace structure needed for corpus, cache, release, and operator state, but **does not create `active.json`** when no validated release exists.

A newly initialized workspace therefore has:

- an empty or absent `releases/` content set as appropriate;
- no active-release pointer file;
- no null/empty/placeholder release ID;
- no fabricated manifest digest;
- no pointer record outside the atomic activation path.

The absence of `active.json` before first activation is a valid pre-release workspace state, not a torn/corrupt pointer.

Builder/registration commands that do not require an active release remain usable in this state.

Runtime entry points that require an active release must detect the pre-release state before opening a catalog or serving an MCP session and fail cleanly without inventing a release. They must distinguish **pointer absent because no release has ever been activated** from **pointer expected but corrupt/torn after activation** in operator diagnostics, while preserving the design's fail-closed runtime behavior and not emitting non-protocol data on MCP stdout.

## 9. First activation creates `active.json`

The first validated release follows the same candidate validation and durability gates as every later release.

Only after the first candidate passes all Phase 2 gates does activation:

1. verify the immutable candidate release and manifest digest;
2. prepare the complete active-pointer record in the same directory/filesystem context required by the atomic-replacement design;
3. flush the temporary pointer record as required;
4. atomically install the complete `active.json`;
5. flush the containing directory where required by the platform contract;
6. verify the referenced release before serving it;
7. record the activation in the external operator lifecycle ledger.

There is no earlier placeholder file to replace.

## 10. Subsequent activation and rollback

After one release has been successfully activated, the ordinary old-or-new atomic replacement and rollback contract applies.

A crash or failure must never expose:

- an empty pointer;
- a partial JSON record;
- a null release ID;
- a placeholder digest;
- a pointer to an unvalidated candidate.

Rollback likewise targets an existing validated release and atomically installs a complete pointer record.

## 11. Initialization and activation tests

Phase 2 must test:

- fresh `clausesift init` creates no `active.json`;
- build/manifest preparation remains usable with no active release;
- search/runtime/MCP startup with no active release fails cleanly before serving requests and does not fabricate a pointer;
- a manually created empty/null/placeholder `active.json` is rejected as invalid rather than treated as the normal pre-release state;
- first valid activation creates the complete pointer only after candidate validation;
- crash injection before first pointer installation leaves the workspace with no pointer and no active release;
- crash injection after atomic installation follows the design's old-or-new/recovery contract, with "old" meaning no active release only for the first activation window where the pointer had not yet been durably installed;
- subsequent activation/rollback never returns to a placeholder state;
- concurrent readers never observe a missing/torn pointer after a release has been durably activated except where the platform's explicitly tested first-activation recovery contract says no active release remains the valid old state.

## 12. Statistical-attempt tests

Phase 2 must test:

- zero screening attempts + one final confirmation;
- one or two screening attempts + one final confirmation;
- attempted third screening reserve is rejected;
- screening result cannot authorize activation;
- final confirmation pass can authorize activation only if every non-statistical Phase 2 gate also passes;
- final confirmation failure ends the campaign;
- materially changed candidate cannot receive another decisive split in the same campaign;
- exact-candidate confirmation replay is reproduction-only;
- a later campaign without documented remediation is rejected;
- a later campaign that reuses old confirmation cases is rejected;
- a later valid campaign uses new independent reviewed confirmation data and retains the previous failed campaign in history.

## 13. Acceptance criteria

Phase 2 is not complete unless:

1. each release campaign has a finite preregistered attempt structure;
2. at most two screening reserves are allowed and none is release-decisional;
3. exactly one unseen final confirmation gate is decisive per campaign;
4. confirmation is never retried for a materially changed candidate within the campaign;
5. a failed campaign remains visible and cannot be reset solely to keep sampling until pass;
6. `clausesift init` omits `active.json` before any valid release exists;
7. the first `active.json` is created only by successful atomic activation of a validated release;
8. pre-release pointer absence is distinguished from post-activation corruption without weakening fail-closed runtime behavior;
9. first activation, later activation, rollback, crash recovery, and concurrent-reader tests all preserve complete valid pointer states.

These guardrails remain strictly Phase 2 because they govern Phase 2 release qualification and activation semantics.
