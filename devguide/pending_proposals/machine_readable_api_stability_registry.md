# Machine-Readable Public API Stability Registry

**Status:** Proposed

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
