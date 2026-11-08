---
summary: Fresh-process test imports resolve a sibling tests package instead of MolSysMT
issue: uibcdf/molsysmt#650
status: active
opened: 2026-11-08
closed:
severity: medium
verification: reproduced
area: [tests]
guard: tests/conversion_truth/test_declared_docking_edges.py::test_docking_routes_do_not_attempt_optional_engine_imports
normative:
blocked_by: []
supersedes: []
---

# Fresh-process ownership of test imports

## What

The no-optional-engine docking conversion guard launches a fresh interpreter
and imports `tests.conversion_truth`. MolSysMT's test root is a namespace
without __init__.py. The received Viewer source contains a regular `tests`
package, so normal Python lookup selects that package instead. The subprocess
fails before any docking route is exercised.

## Evidence

The full-source attempt on `6205fcc78` records ModuleNotFoundError for
`tests.conversion_truth`. A separate standard-library find_spec observation
resolves tests to the received Viewer's tests/__init__.py even with MolSysMT
on PYTHONPATH. This is test-package ownership, not a missing molecular form or
optional-engine dependency. The failure is separate from the task-cap EAGAIN
failures and ParmEd fixture prerequisites in #649. Reproduce the original
guard serially before correction.

## Intended correction and acceptance

Give MolSysMT's test root a real package identity and explicitly prioritize its
known source root in the fresh child. Run the child from an unrelated temporary
working directory to protect that ownership instead of relying on the parent's
cwd. Execute every original declared docking edge under the unchanged blocked
optional-engine imports, keep output count and actual public conversions, and
retain the missing-import original control. Verify package discovery still
excludes tests from the shipped library. No sys.modules fake scientific
provider, downstream adapter, runtime dependency or public API is introduced.

Receive the changed and related conversion tests plus fast/source gates. #612
retains complete-suite acceptance and exact-source scope; package, platform and
independent scientific qualification remain separate.

## Directed receiving — 2026-11-08

The original thirteen-case serial diagnosis yields six failures (five explicit
ParmEd prerequisites and one test-namespace refusal) and seven passes after
controlling Rayon threads. Corrected complete form-census/resident-edge/docking
and strict ParmEd modules pass 518 cases, zero skips/failures/errors. Source
fixtures declare known single O–H bonds; runtime unknown-order refusals remain.
The fresh child executes all original docking cases from an unrelated temporary
working directory under the same blocked optional engines. This is source test
receiving; exact committed-source/fast and full-suite acceptance remain due.
