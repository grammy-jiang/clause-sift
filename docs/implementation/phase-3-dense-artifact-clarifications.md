# Phase 3 Dense Artifact Clarifications

**Project:** ClauseSift  
**Phase:** 3 — Hybrid Retrieval  
**Status:** Normative Phase 3 implementation-plan clarification  
**Primary design authority:** `docs/design.md` Section 16 and runtime release-integrity contract  
**Companion plan:** `docs/implementation/phase-3-hybrid-retrieval.md`

## 1. Purpose and precedence

This clarification closes two Phase 3 dense-artifact requirements that are already normative in `docs/design.md`.

Where the companion Phase 3 plan is less specific, this document is authoritative for these two requirements. It does not add Phase 4 behavior.

## 2. Fixed v0.1 release dtype

ClauseSift v0.1 stores the chunk embedding matrix as:

```text
embeddings.f16.npy
```

The release representation is **unconditionally `float16`** for the current v0.1 design.

An implementation must not treat another release dtype as Phase 3-compliant merely because the embedding provider emits another dtype or because another dtype benchmarks well. Supporting a different release representation requires an explicit design/release-schema change outside this implementation plan.

Provider output may use higher precision internally, but the builder performs the versioned canonical conversion to `float16` before the release artifact is sealed and evaluated.

Release validation requires all of the following to agree exactly:

- filename/declared artifact kind;
- manifest `dtype`;
- NumPy matrix dtype;
- shape-derived byte expectations;
- embedding-artifact schema version;
- lineage transformation identity.

A matrix whose actual dtype is not `float16`, or whose manifest does not declare `float16`, is `release_validation_failed` and cannot be activated.

## 3. Bounded safe NumPy header loading

Every builder-side independent validation and runtime open of the dense matrix uses the safe NumPy loading contract equivalent to:

```python
numpy.load(
    path,
    mmap_mode="r",
    allow_pickle=False,
    max_header_size=10000,
)
```

The exact API call may be wrapped by ClauseSift's loader abstraction, but the semantics are mandatory:

- read-only memory mapping;
- pickle disabled;
- NumPy header size bounded to **10,000 bytes**;
- no fallback retry with a larger/unbounded header;
- no object or structured dtype;
- malformed or oversized headers fail closed before the artifact can serve a query.

The runtime must not first parse an unbounded header merely to discover whether the file would pass the bounded loader.

## 4. Boundary tests

Phase 3 adds fixtures proving:

1. a valid `float16` matrix with a header within 10,000 bytes loads read-only;
2. a non-`float16` matrix is rejected even when shape and values are otherwise valid;
3. a manifest claiming `float16` for another actual dtype is rejected;
4. a header at the admitted maximum is accepted when NumPy's format permits it;
5. a header exceeding 10,000 bytes is rejected without an unbounded retry;
6. `allow_pickle=True` is never used by the release loader;
7. object/structured dtypes remain rejected;
8. the same checks run in independent release validation and runtime startup/open paths.

## 5. Acceptance criteria

These two requirements are blocking Phase 3 acceptance criteria:

- the v0.1 release matrix is always `embeddings.f16.npy` with actual and declared dtype `float16`;
- every release/runtime NumPy open enforces read-only mmap, `allow_pickle=False`, and `max_header_size=10000` before the matrix is admitted for retrieval.
