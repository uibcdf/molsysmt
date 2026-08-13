---
summary: Audit PyUnitWizard fast-path adoption at quantity boundaries.
issue: uibcdf/molsysmt#155
status: open
opened: 2026-08-13
closed:
verification: inspected
area: [argdigest, performance, units]
guard:
normative:
blocked_by: []
supersedes: []
---

# Audit PyUnitWizard fast-path adoption at quantity boundaries

**Reported:** 2026-08-13, after implementing and validating the first canonical-unit
fast paths for coordinates, box vectors, and box lengths.
**Status:** Open. The first measured hot paths are migrated; the remaining quantity
boundaries have not been classified.

## What

Audit MolSysMT's quantity digesters and hot normalization boundaries against the
canonical `PYUNITWIZARD_GUIDE.md`. Adopt `ensure_quantity()`, `has_unit()`, registered
fast tracks, or the general introspection API according to the contract each boundary
actually owns.

This is not a request to replace every `check()` or `standardize()` call. It is a
request to find legacy combinations that repeat unit discovery, dimensionality checks,
and standardization at frequently exercised argument boundaries.

## How

Build an inventory of production call sites using `check()`, `get_unit()`,
`standardize()`, `ensure_quantity()`, `has_unit()`, and `fast_track`. Classify each as:

1. public or adapter validation;
2. private normalization after a validated boundary;
3. numerical-kernel preparation;
4. form conversion or output standardization; or
5. cold-path introspection where clarity matters more than specialization.

For public magnitude arguments, prefer `ensure_quantity()` when it captures the whole
contract. Add an explicit `has_unit()` branch only to a measured hot path that also
performs local shape or dtype normalization. Use registered fast tracks only where the
caller owns validation or the helper preserves MolSysMT's exception contract.

Migrate one coherent family at a time. Add a canonical-input regression test and an
incompatible-unit regression test before changing each family.

## Why

PyUnitWizard now answers exact-unit canonicity cheaply and avoids repeated work inside
its general normalization routes. MolSysMT already uses that mechanism for coordinates,
box vectors, and box lengths, where the canonical path became materially cheaper while
the complete suite remained green.

Source inspection still finds older digesters that compose `check()` and
`standardize()` manually, as well as paths that obtain a unit only to determine whether
conversion is necessary. Some are legitimate specialized contracts; others may be
historical duplication. Without classification, a mechanical migration could weaken
validation just as easily as it could remove overhead.

## What is measured and what is assumed

Measured in the initiating optimization: the canonical coordinate and box-family paths
can avoid the general dimensionality route without changing incompatible-unit behavior.
The focused ArgDigest tests, Ruff, and the complete MolSysMT suite passed after that
change.

Assumed: additional worthwhile hot paths exist among the remaining legacy patterns.
Every candidate must be benchmarked before specialization; source similarity alone is
not performance evidence.

## What was refuted

- A generic identity passport is unnecessary. PyUnitWizard exposes the missing cheap
  predicate, and MolSysMT already has explicit trusted delegation through
  `skip_digestion=True`.
- Replacing every `standardize()` call is not justified. Output construction and form
  adapters often need unconditional standardization and are outside the argument-hot-
  path problem.
- `has_unit() is False` does not prove dimensional compatibility. Both `False` and
  `None` require the general validation route at an untrusted boundary.

## Scope and exclusions

In scope are production quantity digesters, kernel-input helpers, and frequently used
adapter boundaries. Tests are used as evidence but are not migration targets merely
because they call the general API.

Out of scope are changes to PyUnitWizard itself, global unit-configuration authority,
new value-certification containers, and unrelated form-conversion refactors.

## Acceptance criteria

- Production unit call sites are inventoried and classified by boundary type.
- Every migrated family has tests for canonical input, compatible non-canonical input,
  incompatible units, shape, dtype, and local exception behavior where applicable.
- Specialization is backed by a reproducible before/after benchmark with telemetry
  settings recorded.
- Unmeasured or cold paths retain the clearest general implementation.
- Ruff, focused tests, and the normal full-suite gate pass.
- Durable MolSysMT-specific rules are absorbed into
  `devguide/digestion_and_dependencies.md`; the canonical API rules remain in
  `PYUNITWIZARD_GUIDE.md`.

## Dependencies and risks

The audit depends on the PyUnitWizard version that provides the documented tri-state
`has_unit()` contract and optimized `ensure_quantity()`. The primary risk is confusing
exact-unit equality with dimensional compatibility and thereby changing which error a
public caller receives.

