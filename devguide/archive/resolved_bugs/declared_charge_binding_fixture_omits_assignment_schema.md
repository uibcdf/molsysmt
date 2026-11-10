---
summary: Declare the supported schema in the atom-name projection charge fixture.
issue: uibcdf/molsysmt#670
status: resolved
opened: 2026-11-09
closed: 2026-11-09
severity: medium
verification: reproduced
area: [tests, ci]
guard: tests/build/test_project_atom_names.py::test_template_sensitive_charge_binding_is_not_recertified_after_rename
normative:
blocked_by: []
supersedes: [uibcdf/molsysmt#672]
---

# Declared charge fixture fails before testing name invalidation

## What

The original full-CI Linux/Python 3.14 JUnit records 32,901 cases, one failure,
zero errors and 169 skips. The sole failing test is the guard below. It creates
a declared force-field-sensitive binding without its supported schema, so native
validation correctly refuses before the test reaches the independent rename.
The report is a fixture, not an executed force-field calculation.

## How

The two-field input to bind_assignment omits
schema=molsysmt.partial_charge_assignment@1. The helper adds fingerprints but
never upgrades unrecognized evidence to a supported scientific report.
_require_assignment_report rejects this incomplete declaration. Add the schema
to this intentionally declared fixture, preserve source validation before/after
projection, and retain the renamed-output bound-chemistry refusal unchanged.
Production schema validation is unchanged.

## Why

The intended regression guard no longer reaches the stale-name mechanism. This
blocks the required full suite without demonstrating an incorrect projection or
an actual scientific calculation failure. Do not relax source-report integrity,
skip this case or accept malformed bindings to make the fixture pass.

## Measured evidence and exclusions

Original run 42689572908, Linux/Python 3.14 artifact 13710862374: independently
downloaded ZIP SHA-256
75da1eff153420ea884131a22cfaaa2037840b2acdab327f11bb7d999967eb25
matches GitHub's digest. JUnit is parsed without executing downloaded content.
On clean receiving merge 3dfe27ab6 / Viewer 346c3319 / published PyUnitWizard
0.28.1, the 66-case bounded source selection reproduces exactly this failure,
with 65 passes and five existing legacy-format warnings. Original input hashes,
JUnit/events/logs and resource receipts remain in the private campaign.

#669's artifact placement and #671's macOS download failure are independent.
No claim is made that the original full CI passed, that the failed source is a
release candidate or that this fixture certifies force-field execution. The
concurrently discovered duplicate #672 is superseded by the earlier #670.

## Acceptance

The original guard must validate the well-formed source before and after
independent projection, and refuse the renamed output specifically for changed
bound chemistry. Receive the full projection/native unknown-report controls,
including future/empty/missing-index evidence refusals, without changing their
expected outcomes or production schema validation.


## Resolution — 2026-11-09

Clean source c37e42510 / immutable Viewer 346c3319 passes all 5,711 addon and
selected preflight cases, 251 affected mechanics/projection/force controls and
all 107 registered scientific cases (68 nodes, no skips). The strict clean
scientific certificate records source correspondence; it is not release
authorization. Fourteen fast gates pass. Original native refusal/assertion
semantics are preserved, including malformed report rejection and deliberate
inside-checkout artifact refusal.

Actual Jupyter receives all ten Chemistry and twenty Analysis checks on the
new host. Missing local Playwright/harness preparation attempts are retained;
the existing tools and generated harness resolve those setup failures without
source/assertion/deadline changes. Original hosted failures stay failed. #671
provisioning and the required exact-candidate full matrix remain pending.

See the [bounded receiving record](../../../devtools/data/pre1_ci_and_mechanics_receiving_669_670_582_20261109.json)
for exact source/backend identities, input hashes, failed originals, execution
scopes, resource limits, notebook preservation and limitations. The front-matter
guard protects the actual original mechanism rather than a weaker output shape.
