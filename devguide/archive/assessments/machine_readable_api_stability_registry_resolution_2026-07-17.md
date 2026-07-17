# Machine-Readable Public API Stability Registry — Resolution

> Archived implementation record dated 2026-07-17. The current contract lives
> in `devtools/data/public_api_stability.json` and `devguide/api_surface.md`.

**Status:** Implemented on 2026-07-17

## Why

MolSysMT exposes a large lazy root surface and multiple public namespaces. A
manual table assigning Stable, Experimental, or Outside-contract status drifts
as symbols are added, renamed, deprecated, or moved. Discoverability, form tier,
test coverage, and `versionadded` metadata are not substitutes for release
stability.

## Proposal

Add a small machine-readable registry keyed by fully qualified public symbol,
with at least:

- stability level;
- version introduced;
- deprecation/removal metadata when applicable;
- owning namespace;
- optional dependency and feature flags;
- link to the normative documentation or contract test.

Generate the human API stability table from this registry and validate it
against `molsysmt._LAZY_ATTRIBUTES` plus public namespace exports.

## How

1. Define the schema and allowed transitions.
2. Inventory the root registry and namespace `__init__.py` files.
3. Require an explicit review decision for unclassified symbols; do not infer
   Stable from age or test presence.
4. Add a validator that fails on missing, stale, or nonexistent symbols.
5. Integrate the validator into the API/doc CI job.
6. Generate release-note input and the public stability page from the same data.

## Acceptance criteria

- Every intentionally public symbol is classified exactly once.
- Internal symbols cannot enter the registry.
- Deprecated symbols identify replacement and timeline.
- Documentation is generated or checked from the registry.
- CI detects both newly exported and removed symbols.

## Resolution

The normative registry now lives in
`devtools/data/public_api_stability.json`. It explicitly classifies the root
surface and all members of the first release-contract namespaces. Namespace
trees not yet promoted into exact member tracking inherit an explicit
Experimental or Outside-contract policy from their registered root namespace;
discoverability is therefore never interpreted as Stable by default.

`devtools/scripts/validate_api_stability.py` discovers exports through the AST,
validates metadata and documentation/test paths, rejects missing and stale
entries, and generates `devguide/api_stability_registry.md`. Its optional
baseline comparison forbids Stable demotion/removal and silent reversal of a
deprecated lifecycle. Focused validator tests and the developer-guide CI job
enforce the contract.

The `pre-1.0` introduction marker is deliberately supported for symbols whose
fine-grained development history predates a trustworthy public release record.
New symbols must use an actual semantic version.
