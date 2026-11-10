---
summary: MolSysMT requests Pint registry caching after the registry is already loaded.
issue: uibcdf/molsysmt#674
status: active
opened: 2026-11-09
closed:
severity: low
verification: reproduced
area: [units, deps]
guard: tests/test_unit_policy_bootstrap.py
normative:
blocked_by: []
supersedes: []
---

# Respecting prior unit-backend use during import

## What

An application can construct a Pint quantity through PyUnitWizard without
installing a standard-unit policy. MolSysMT then sees no active policy and calls
set_pint_registry_cache(True) after the registry exists. PyUnitWizard correctly
warns that the request cannot affect that registry.

## How

The fresh-interpreter `used_without_policy` guard constructs a real quantity,
then imports MolSysMT. Before repair it fails on that exact RuntimeWarning;
cold import and an explicit application policy already pass. Receiving uses the
published minimum PyUnitWizard 0.28.1, not a private provider modification.
Earlier fixture/launcher errors are retained separately from this reproduction.

## Why and correction

Absence of a policy is not absence of a loaded backend. Read the public
configure.report()['loaded_libraries'] before the cache setter and opt in only
while Pint is unloaded. Continue adopting the shared standards only when no
policy exists; keep an application policy and existing registry intact. No
warning filter, registry reconstruction, dependency-floor change or competing
unit policy is introduced. Fast-track registration remains unconditional.

## Acceptance

All three import orders must pass with unchanged existing registry identity,
requested cache setting, application policy/provenance and numeric conversion.
The shared policy is still established on cold and previously used/no-policy
imports. Broader composition and active-unit tests remain required.

## Provider guide follow-up

The copied consumer-guide example has the same absent-policy assumption.
Canonical guidance correction is tracked in uibcdf/pyunitwizard#144; MolSysMT
changes no synchronized guide copy or provider source. This follow-up does not
block the bounded consumer fix supported by the published minimum.
