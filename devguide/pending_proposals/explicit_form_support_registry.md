# Explicit Form Support Registry

**Status:** explicit tier registry implemented 2026-07-13; capability evidence pending

## Why

The original registry listed only Tier 2 and Tier 3 forms and silently treated
absence as Tier 1. The registry now contains all 92 discovered forms, and tests
plus the adapter validator require exact agreement. Unknown forms fail instead
of receiving contractual support.

## Proposal

Register every known form explicitly with tier, capability scope, owner, and
evidence. Unknown forms should be unclassified and fail validation rather than
defaulting to Tier 1.

## How

1. Discover all registered adapter `form_name` values. **Implemented.**
2. Define an explicit entry for each form, including Tier 1 forms. **Implemented.**
3. Separate recognition, conversion, topology, structure, iterator, and heavy
   capabilities where a single tier is too coarse.
4. Link entries to public delivery/parity tests.
5. Make CI fail for adapters missing from the registry or stale registry names.
   **Implemented in the adapter validator and focused tests.**
6. Generate the support report/notebook from the registry. **Implemented.**

## Acceptance criteria

- Adding an adapter requires an explicit support decision.
- Typos cannot become silently contractual.
- Tier 1 claims point to passing delivery and conversion tests.
- Viewer and optional-backend forms have accurately scoped guarantees.
