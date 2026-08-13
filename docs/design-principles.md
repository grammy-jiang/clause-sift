# ClauseSift Design Principles

- **Document version:** 0.2
- **Status:** Design rulebook
- **Product intent:** [ClauseSift Design Brief](design-brief.md)
- **Detailed realization:** [ClauseSift Design Document](design.md)

## 1. Role

This document contains durable rules for turning the design brief into a detailed
design. It does not restate the product, architecture, workflow, release scope,
schemas, algorithms, or tests.

Every technical decision must be consistent with these principles and with the
detailed design. The detailed design owns exact contracts and may choose among
implementations that satisfy the rules. A deliberate exception must be explicit,
justified, bounded, and recorded in the detailed design.

## 2. Decision order

When goals compete, preserve them in this order:

1. source and citation correctness;
2. contextual completeness and applicability correctness;
3. interactive query speed;
4. traceability and reproducibility;
5. operational simplicity;
6. build speed.

A lower priority cannot silently weaken a higher one.

## 3. Evidence and meaning

### DP-01 — Keep original sources authoritative

Structured data, indexes, and model outputs may improve retrieval, but they must
remain traceable to approved source text and pages and must never replace source
authority. See detailed design Sections 5, 14, 20, and 31.

### DP-02 — Preserve semantic dimensions

Keep identity, edition, lifecycle status, evidence role, source modality,
jurisdiction, applicability, and relationships distinct. Do not compress them
into a convenient but ambiguous label. See Sections 6, 10, 12, and 13.

### DP-03 — Make identity and provenance deterministic

Stable identity, ordering, citation, and lineage must come from versioned rules
and reviewed inputs, not database insertion order or model judgment. See Sections
7, 19, 20, and 21.

### DP-04 — Treat required context as correctness

Evidence is incomplete when required scope, applicability, definitions,
dependencies, exceptions, table context, or material conflict sides are absent.
Context closure must therefore be deterministic and bounded. See Sections 17-19.

### DP-05 — Preserve disagreement and uncertainty

Represent every material position and every unresolved condition. Select a
controlling position only through encoded, source-grounded precedence; never use
rank, recency, or model confidence as authority. See Sections 13, 18, and 21.

## 4. Architecture and lifecycle

### DP-06 — Compile offline and serve read-only

Perform document-dependent work in the build path and publish its result as an
immutable release. Normal retrieval must not alter sources, indexes, or release
state. See Sections 7-9 and 24-27.

### DP-07 — Separate canonical evidence from acceleration

Canonical structure and provenance define meaning; indexes, embeddings, caches,
and models are derived and rebuildable. Replacing an accelerator must not change
the public evidence contract. See Sections 7, 15, 16, and 25.

### DP-08 — Publish only complete verified releases

Build failures must leave the active release unchanged. Activation must be
atomic, and recovery must select a complete previously verified release rather
than combine partial states. See Sections 24-26 and 31.

### DP-09 — Keep components replaceable behind contracts

Parsers, OCR, tokenizers, models, and index engines may change only behind
versioned canonical and public boundaries, with downstream effects revalidated.
See Sections 8, 9, 15, 16, and 25.

## 5. Trust and operation

### DP-10 — Validate before use and fail closed

Treat sources, manifests, parser outputs, releases, paths, databases, models,
indexes, and protocol inputs as untrusted until verified. Integrity loss must
stop unsafe success rather than trigger silent degradation. See Sections 11, 22,
27, and 31-33.

### DP-11 — Bound work and make outcomes terminal

Inputs, queues, traversals, responses, workers, model loads, deadlines, and
shutdown paths must have explicit limits and exactly one terminal outcome. See
Sections 22, 27, 30, and 31.

### DP-12 — Keep data local and disclose minimally

Document and query content remains local by default. External transmission
requires explicit configuration, and every response, diagnostic, report, and log
must expose only necessary safe information. See Sections 11, 22, and 33.

## 6. Retrieval and interfaces

### DP-13 — Keep exact and lexical retrieval first-class

Exact identifiers, metadata, numbers, and lexical terms must work independently.
Semantic retrieval and reranking may improve recall but cannot repair or replace
an identity contract. See Sections 15-18.

### DP-14 — Use models as bounded assistants

Models may propose or rank candidates, but they must not create source facts,
citations, relationships, precedence, or release authority. Their behavior must
remain attributable, replaceable, and evaluated. See Sections 8, 16, 17, and 29.

### DP-15 — Expose one strict evidence contract

Python, CLI, and MCP must share validation, evidence semantics, ordering,
pagination, typed failures, and safe serialization through one runtime service
layer. See Sections 21-23 and 31.

### DP-16 — Version behavior and make output deterministic

Version every behavior-bearing vocabulary, rule set, schema, identity algorithm,
cache, release, and compatibility path. Equivalent inputs must produce stable
results wherever the contract claims determinism. See Sections 10, 21, 25, 30,
and 31.

## 7. Quality and change

### DP-17 — Let representative evidence choose components

Select parsers, models, indexes, thresholds, and retrieval settings through the
project's representative corpus and real question classes rather than popularity
or unrelated benchmarks. See Sections 28 and 29.

### DP-18 — Match proof to the claim

Use complete conformance checks for deterministic invariants and preregistered
statistical methods for sampled quality claims. Report failures and uncertainty
instead of converting them into unsupported certainty. See Sections 29, 34, and
36.

### DP-19 — Test failures and recovery as behavior

Verification must cover boundaries, invalid states, adverse ordering, races,
crashes, rollback, and forbidden side effects as well as successful examples.
See Sections 31, 32, 34, and 36.

### DP-20 — Optimize only after quality gates pass

Measure before optimizing, and preserve every validated correctness, context,
integrity, and privacy gate. Performance alone cannot justify weaker evidence.
See Sections 28, 29, and 36.

## 8. Applying the rulebook

When generating or revising the detailed design:

1. start from the product intent in the design brief;
2. identify the principles that constrain each decision;
3. put the exact contract, implementation choice, and verification method only
   in the detailed design;
4. keep the distinction between source authority, canonical evidence, and
   derived acceleration explicit;
5. record any exception and its consequences;
6. update this document only when a cross-cutting rule changes.

If a statement describes what ClauseSift is or which major workflow it provides,
it belongs in the brief. If it describes an exact schema, algorithm, protocol,
limit, gate, or test, it belongs in the detailed design. This document contains
only the durable rules between those two levels.
