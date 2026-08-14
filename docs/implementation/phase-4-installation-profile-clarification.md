# Phase 4 Reranker Installation-Profile Clarification

**Phase:** 4 — High-Accuracy Retrieval  
**Status:** Normative Phase 4 clarification  
**Authority:** `docs/design.md` Sections 8.2–8.3 and 34.4

Phase 4 must make the local cross-encoder runtime installable through the design-defined optional dependency profile without contaminating the base runtime.

## Required packaging contract

- `pip install clausesift` installs the base runtime without reranker-only dependencies.
- `pip install "clausesift[rerank]"` installs the base runtime plus every officially supported dependency required to execute the selected local cross-encoder reranker.
- `pip install "clausesift[all]"` includes the officially supported reranker profile together with the other supported optional components.
- the base runtime remains able to start, use exact/lexical/vector paths, run the CLI/MCP surfaces that do not require reranking, and report the explicit unavailable-capability contract without importing reranker-only packages;
- reranker modules and heavy model-runtime dependencies are imported only when the high-accuracy/rerank capability is selected or otherwise explicitly needed.

A Phase 4 candidate is not release-ready if its selected reranker requires an undeclared manual dependency, if the `rerank` extra cannot reproduce the supported runtime, or if adding Phase 4 makes ordinary base-runtime startup import/install the reranker stack.

## Required clean-install tests

Run isolated clean-environment packaging tests for:

1. base wheel/sdist install: import `clausesift`, start the base runtime/MCP path, and prove reranker-only dependencies are not imported or required;
2. `clausesift[rerank]`: load the checksum-verified selected local reranker through the normal lazy-loader path and execute representative high-accuracy inference;
3. `clausesift[all]`: prove the same reranker path remains functional alongside all supported optional components;
4. base installation + explicit `high_accuracy`: use the exact design-defined unavailable-capability error/fallback behavior rather than an import traceback or implicit package install;
5. dependency-boundary regression: importing the base package or running model-free operations does not import parser/OCR/reranker-only modules.

The distribution metadata and lock/release identity must bind the supported reranker dependency/profile version used by the candidate.

These packaging gates are Phase 4 blockers for a release that advertises local high-accuracy reranking.
