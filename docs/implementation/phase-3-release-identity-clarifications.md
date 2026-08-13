# Phase 3 Release Identity Clarifications

**Project:** ClauseSift  
**Phase:** 3 — Hybrid Retrieval  
**Status:** Normative Phase 3 implementation-plan clarification  
**Primary design authority:** `docs/design.md` Sections 7.2, 25, 26, and 27  
**Companion plan:** `docs/implementation/phase-3-hybrid-retrieval.md`

## 1. Purpose and precedence

This clarification closes three Phase 3 release-identity requirements identified during review.

Where the companion Phase 3 plan is less specific or cites the wrong design section for these requirements, this document is authoritative. It remains entirely within Phase 3.

## 2. Byte-identical canonical embedding artifact

For the same **complete build identity**, ClauseSift must produce a **byte-identical canonical `embeddings.f16.npy` release artifact**.

A tolerance-governed difference in release artifact bytes is not acceptable. Numerical tolerance may be used only for validation predicates such as checking whether vectors satisfy the declared normalization invariant; it does not permit equivalent builds to emit different canonical matrix bytes.

Therefore:

- identical source/chunk inputs;
- identical `embedding_text` bytes;
- identical model/provider implementation;
- identical model assets and revisions;
- identical embedding configuration;
- identical dependency lock/toolchain identity;
- identical canonical float16 conversion rule;
- identical row-order/schema identity

must produce the same exact `.npy` bytes and SHA-256.

If an embedding model/provider cannot satisfy this release reproducibility contract under the admitted build environment, it is not eligible for selection, regardless of retrieval quality.

### 2.1 Reproducibility tests

Phase 3 must build the same embedding artifact in fresh build processes/environments covered by the admitted reproducibility contract and assert:

- byte-for-byte file equality;
- identical SHA-256;
- identical shape/header bytes;
- identical `build_content_id` inputs;
- identical downstream release identity inputs.

A normalization check may use a documented numerical tolerance, but a matrix-byte comparison may not.

## 3. Complete local query-model asset binding

A local model identifier and revision are insufficient when tokenizer/model files can change underneath those identifiers.

The Phase 3 release manifest and `build-info.json` must bind the **complete ordered asset set** required by the query-embedding model loader.

For every local model asset the release records at minimum:

- canonical release-relative asset path or stable safe asset name;
- asset role/kind;
- model format where applicable;
- exact byte size;
- SHA-256;
- loader-relevant ordering where the loader consumes an ordered set.

The release also records:

- model ID;
- exact model revision;
- model format family;
- loader name;
- loader version;
- tokenizer/processor implementation and version where applicable;
- complete ordered aggregate asset digest;
- provider/model configuration hash.

The aggregate digest is derived deterministically from the complete ordered asset table and is part of release/build identity.

No local model file that the loader may open may be omitted from the exhaustive release artifact table.

### 3.1 Safe formats

The existing design safe-loading policy remains authoritative:

- allowlisted non-executable weight formats such as Safetensors or ONNX plus validated JSON/tokenizer assets may be admitted;
- pickle-backed `.pt`, `.pth`, `.bin`, joblib, or loaders with arbitrary-code hooks remain forbidden for v0.1 unless the design is explicitly changed.

### 3.2 Runtime recheck

Before invoking the query-model loader, runtime rechecks every file the loader may open against the manifest size/hash table.

A missing, extra, reordered where order is meaningful, size-mismatched, hash-mismatched, unsupported-format, or loader-version-incompatible asset fails before deserialization and follows the existing release-integrity/quarantine contract.

This ensures the chunk embeddings built offline and the current-query embedding produced at runtime always use the exact same bound model asset identity.

## 4. Correct build-cache authority

The authoritative per-artifact cache dependency contract is:

```text
docs/design.md Section 25 — Build cache and invalidation
```

Any reference in the companion Phase 3 plan that points to Section 32 for embedding/vector cache dependencies is superseded by this clarification and must be implemented against **Section 25**.

Phase 3 inherits the complete Section 25 dependency entries for:

- chunk embeddings;
- vector index;
- evidence lineage;
- release assembly;
- every upstream artifact named by those entries.

The abbreviated dependency lists in the Phase 3 plan are implementation reading aids only. They do not remove or replace any Section 25 dependency.

## 5. Blocking validation

Phase 3 release validation must fail when:

- an equivalent complete build identity produces different canonical embedding artifact bytes;
- a selected local query model lacks a complete manifest-bound asset set;
- the runtime's asset set differs from the build-bound set;
- model format/loader identity is missing or unsupported;
- any Section 25 embedding/vector cache dependency is omitted from the cache identity;
- a stale embedding/vector cache entry is reused after any behavior-bearing dependency changes.

## 6. Acceptance criteria

These requirements are blocking Phase 3 acceptance criteria:

1. same complete build identity produces byte-identical `embeddings.f16.npy` bytes and SHA-256;
2. numerical tolerance is used only for numerical invariants, never as a substitute for release byte reproducibility;
3. local query-model format, loader identity, tokenizer/weight assets, sizes, hashes, and complete ordered aggregate digest are bound into the release/build identity;
4. runtime rechecks the complete model asset set before loading;
5. embedding/vector cache keys inherit the full authoritative `docs/design.md` Section 25 dependency contract.
