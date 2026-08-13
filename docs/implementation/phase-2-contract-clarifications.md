# Phase 2 Contract Clarifications

**Project:** ClauseSift  
**Phase:** 2 — Exact Retrieval MVP  
**Status:** Normative Phase 2 implementation-plan clarification  
**Primary design authority:** `docs/design.md` Sections 7.2 and 22.3  
**Companion plans:** `docs/implementation/phase-2-mcp-wire-resources.md`, `docs/implementation/phase-2-lineage-release-contract.md`

## 1. Purpose and precedence

This document closes two narrowly scoped Phase 2 canonicality requirements discovered during exact-head review:

1. every page resource has exactly one accepted URI spelling for its normalized integer page number;
2. every selected parser route and ordered build transformation in `lineage.json` carries the complete transformation identity tuple required by the design.

Where a companion Phase 2 document is less specific about either rule, this clarification is authoritative. It does not add any Phase 3 or Phase 4 capability.

## 2. Canonical page-number URI syntax

The `page_number` variable in:

```text
standards://page/{document_id}/{page_number}
```

is semantically a positive one-based integer, not an arbitrary string that is converted to an integer only after URI canonicality checks.

Its **only canonical decoded lexical representation** is base-10 ASCII matching:

```text
^[1-9][0-9]*$
```

followed by the existing semantic bounds:

- value >= 1;
- value <= 2,147,483,647;
- value <= the selected document's manifested page count.

Therefore the following are never alternative spellings of page 1:

- `01`;
- `001`;
- `+1`;
- `-1`;
- a leading-space form such as " 1";
- a trailing-space form such as "1 ";
- a percent-encoded sign or leading whitespace;
- any Unicode digit sequence other than ASCII `0`-`9` in the canonical decimal grammar.

`0` is lexically non-canonical for this one-based route and also semantically invalid.

## 3. Normalized-semantic re-expansion check

The Phase 2 resource parser applies **two** canonicality checks before catalog lookup:

1. **encoding canonicality:** decode each route segment exactly once with strict UTF-8, then re-encode that decoded text with the RFC 6570 / RFC 3986 uppercase-percent rule and require byte identity with the supplied segment;
2. **semantic canonicality:** validate and normalize the decoded value according to its field type, then expand the **normalized semantic value** back to the canonical route segment and again require byte identity with the supplied segment.

For `document_id`, normalization is identity-preserving under its strict opaque-ID grammar, so the two checks collapse to the same canonical bytes.

For `page_number`, normalization parses the canonical decimal text into the bounded integer and serializes that integer back using ordinary base-10 ASCII with no sign and no leading zeroes. The resulting segment must equal the client-supplied segment byte-for-byte.

Consequently:

```text
.../1     -> canonical candidate for page 1
.../01    -> rejected before catalog lookup
.../+1    -> rejected before catalog lookup
.../%2B1  -> rejected before catalog lookup
.../-1    -> rejected before catalog lookup
.../０１   -> rejected before catalog lookup
```

No URI spelling that normalizes to another accepted URI may reach catalog lookup.

## 4. Page URI error routing

A page resource with a malformed or non-canonical page-number spelling is a malformed/non-canonical resource URI, not a valid lookup miss.

It therefore returns on both supported protocol paths:

- JSON-RPC `-32602` (`Invalid params`);
- no `contents`;
- no catalog query;
- no source open;
- no page-response working-set reservation.

A canonical page-number spelling that is syntactically canonical but outside the selected document's manifested range follows the design's applicable invalid-parameter/resource routing, never a successful alias to another page.

## 5. Page URI generation

`get_page_reference` and every server-generated page URI use the same single formatter:

1. validate one-based integer range;
2. format the integer as base-10 ASCII with no sign and no leading zeroes;
3. RFC 6570-expand `document_id` and the formatted page-number segment;
4. emit uppercase percent escapes for any non-unreserved byte where applicable.

There is no independent URI formatter in the resource router.

For every successful page reference/resource pair:

```text
get_page_reference.page_uri == resources/read requested canonical URI
```

byte-for-byte.

## 6. Page-number canonicality tests

Phase 2 must cover at least:

- `/1` accepted for manifested page 1;
- `/9` and `/10` demonstrate ordinary decimal transition;
- `/01` rejected as non-canonical;
- `/001` rejected;
- `/+1` rejected;
- `/%2B1` rejected;
- `/-1` rejected;
- `/0` rejected;
- Unicode full-width or other Unicode digits rejected;
- upper range `2147483647` accepted only when the manifest permits it;
- `2147483648` rejected;
- a canonical integer one greater than the manifested page count rejected;
- generated `get_page_reference.page_uri` round-trips through the parser unchanged;
- every rejected spelling proves zero catalog/source/admission calls.

## 7. Complete lineage transformation identity tuple

`lineage.json` must identify **every selected parser route and every ordered build transformation** with the same complete, strict transformation identity tuple.

The required logical tuple is:

```text
{
  kind,
  role,
  producer,
  producer_version,
  configuration_sha256,
  content_sha256
}
```

The concrete schema may use equally explicit versioned field names, but it must preserve all six meanings with no implicit defaults.

### 7.1 `kind`

A closed, versioned transformation-kind token describing what the stage does, for example:

- parser-neutral extraction;
- canonical normalization/model construction;
- evidence-vocabulary classification;
- page-provenance mapping;
- standards-aware chunk/source projection;
- catalog materialization;
- lexical-index construction.

Future Phase 3/4 stages require new admitted kinds rather than being represented by a generic catch-all value.

### 7.2 `role`

The stage's exact role in the ordered build, for example:

- `canonical_primary`;
- `independent_comparator`;
- `normalizer`;
- `canonical_builder`;
- `classifier`;
- `page_mapper`;
- `chunker`;
- `catalog_builder`;
- `lexical_index_builder`.

Role is not inferred from array position alone.

### 7.3 `producer`

A stable safe identifier for the code component or external parser/index implementation that produced the transformation output. Mutable filesystem paths and executable locations are forbidden.

### 7.4 `producer_version`

The exact admitted producer version/revision. A version string alone is insufficient identity without the configuration and content hashes below.

### 7.5 `configuration_sha256`

SHA-256 of the versioned canonical configuration that materially controls the transformation. The configuration hash must change when a behavior-bearing setting changes even if the resulting output bytes happen to remain identical.

Secrets, credentials, absolute paths, and raw configuration bodies are not embedded in public lineage; only the approved safe identity/hash is retained.

### 7.6 `content_sha256`

SHA-256 of the exact transformation output artefact bytes, or of the explicitly versioned canonical projection bytes when the stage's output is persisted inside another canonical artefact rather than as a standalone file.

The preimage/projection rule is versioned and deterministic. A producer cannot choose an ad-hoc subset of its output for this hash.

## 8. Ordered transformation chain

Each source-lineage record retains the complete ordered transformation chain needed to derive that source from the approved input.

For Phase 2, the applicable chain includes every stage that actually transforms or validates bytes/structure used by the source, including as applicable:

1. each selected parser route, with explicit parser role;
2. canonical normalization / canonical-model construction;
3. evidence-vocabulary classification/provenance transformation;
4. page-provenance mapping;
5. standards-aware chunk/source projection;
6. catalog materialization/projection on which runtime identity depends;
7. lexical-index construction as the Phase 2 retrieval artefact.

The passing parser-validation report remains separately bound by its own report hash as required by the lineage contract; its existence does not remove the parser transformation tuples.

If a transformation is factored into several independently versioned behavior-bearing stages, each stage gets its own tuple rather than collapsing them under one convenient label.

## 9. No identity shortcuts

The following are invalid lineage shortcuts:

- recording only `version` without producer/configuration identity;
- recording only an output artefact hash without the producer/configuration identity;
- recording only configuration hash without exact output content hash;
- inferring `role` from tuple order;
- omitting a transformation because its output bytes are identical to a previous build;
- treating identical output bytes as proof that a changed behavior-bearing configuration is equivalent;
- replacing producer identity with a local executable path;
- using one generic transformation tuple for several independently controlled stages.

A changed producer, producer version, role, or behavior-bearing configuration invalidates the lineage/release identity according to the declared dependency graph even if the newly produced bytes are coincidentally identical.

## 10. Release validation of transformation identities

Release validation independently reconstructs the expected ordered transformation identity set from the release's admitted build inputs and artefacts.

It rejects `lineage.json` when any transformation tuple is:

- missing;
- extra;
- out of order;
- wrong `kind`;
- wrong `role`;
- wrong producer;
- wrong producer version;
- wrong configuration hash;
- wrong content hash;
- bound to the wrong document/source;
- from an unsupported transformation schema version.

Runtime startup repeats the checksum/schema/catalog consistency validation required by the Phase 2 lineage contract before accepting work.

## 11. Transformation identity regression tests

Tests must include:

- identical build inputs reproduce byte-identical ordered tuples;
- changed normalizer configuration with identical output bytes changes `configuration_sha256` and therefore lineage/release identity;
- changed classifier configuration with identical selected labels still changes the configuration identity;
- changed page-mapper configuration with byte-identical page projection remains distinguishable;
- changed producer version is visible even when output bytes match;
- changed content bytes with unchanged declared configuration changes `content_sha256`;
- missing producer/config/content field is rejected;
- swapped roles are rejected;
- reordered transformation tuples are rejected;
- one generic tuple standing in for two independently configured transformations is rejected;
- rollback restores the exact older ordered transformation identities together with the older release.

## 12. Acceptance criteria

Phase 2 is not complete unless:

1. page resource numbers have one canonical decoded decimal spelling;
2. normalized semantic page values are re-expanded and byte-compared before catalog lookup;
3. leading-zero, sign, Unicode-digit, range, and manifested-page fixtures pass the exact canonicality/error contract;
4. all server-generated page URIs use the same canonical formatter and round-trip byte-identically;
5. every selected parser route and ordered build transformation in `lineage.json` carries `kind`, `role`, `producer`, `producer_version`, `configuration_sha256`, and `content_sha256`;
6. the full ordered transformation chain covers every behavior-bearing Phase 2 stage actually used to derive a source/retrieval artefact;
7. release validation rejects incomplete, stale, reordered, or mismatched transformation identities;
8. configuration/producer changes remain provenance-visible even when output bytes happen to be identical.

These clarifications remain entirely inside Phase 2 because they tighten the canonical URI and immutable build-provenance contracts of resources/releases Phase 2 already ships.
