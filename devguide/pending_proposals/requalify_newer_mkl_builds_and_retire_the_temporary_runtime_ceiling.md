---
summary: Requalify newer MKL builds and retire the temporary runtime ceiling
issue: uibcdf/molsysmt#403
status: open
opened: 2026-10-22
closed:
verification: upstream
area: [ci]
guard:
normative:
blocked_by: []
supersedes: []
---

# Requalify newer MKL builds and retire the temporary runtime ceiling

**Reported:** 2026-10-22, explicitly requested by the maintainer after the
source-test recovery in uibcdf/molsysmt#402.
**Status:** Open future qualification task; the working runtime ceiling remains.

## What

Track whether MKL 2026.2.0 replacement builds or later versions restore the
GNU-interface compatibility required by the conda-forge NumPy/BLAS stack. Qualify
a corrected concrete package combination before removing or revising the
source-test `mkl<2026.2` constraint.

#402 closed the immediate consumer CI recovery. This separate issue owns
retirement of its temporary workaround, not reopening the recovered incident.

## How

Follow these upstream records and the actual published package inventory:

- [Intel repack issue #145](https://github.com/conda-forge/intel_repack-feedstock/issues/145):
  missing GNU LP64/ILP64 shared interfaces in both the Intel original and its
  conda-forge Linux repack.
- [Admin request #2430](https://github.com/conda-forge/admin-requests/pull/2430):
  withdrawal of the broken Linux build. Withdrawal prevents a bad solve; it does
  not itself provide a corrected modern runtime.
- [Functional-test proposal #146](https://github.com/conda-forge/intel_repack-feedstock/pull/146):
  interface-layer and NumPy/SciPy ecosystem validation.
- [Published MKL inventory](https://api.anaconda.org/package/conda-forge/mkl):
  inspect version, build, platform and channel labels. A repair may retain the
  version `2026.2.0` while changing its build number.

When a candidate appears, use a clean hosted qualification route with the complete
optional source-test dependency set. That route must deliberately select the
candidate and override the old ceiling only for its qualification; a successful
solve falling back to MKL 2026.1.0 cannot satisfy this task. Record the actual
installed backend and versions, not just requested specifications.

Reuse upstream functional tests and existing MolSysMT import/numerical
regressions. Check NumPy/SciPy imports, matrix products, linear solves, SVD and
complex-valued operations with known answers so ABI/interface errors cannot
pass merely because shared-library filenames exist. Run the existing exact-source
smoke gate and relevant consumer regressions, retaining failure evidence and
using the repository receptor tools.

If qualified, revise the temporary ceiling coherently across the maintained
smoke/full/weekly/benchmark workflow routes and update the
[dependency contract guidance](../dependency_contract_audit.md). Cover affected
platform/Python routes; do not require MKL where the normal solve omits it.

## Why

An unowned temporary ceiling can silently become permanent or be removed on a
version-number assumption. This task provides an explicit owner for returning
to supported newer MKL packages with numerical evidence.

## What is measured and what is assumed

**Upstream-confirmed:** the original Linux `mkl 2026.2.0` build lacks the shared
GNU interfaces requested by conda-forge's activation configuration. The local
[incident record](../archive/resolved_bugs/smoke_environment_selects_an_mkl_runtime_that_cannot_import_numpy.md)
retains manifest evidence and the successful MKL 2026.1.0 consumer recovery.
At filing, upstream issue #145, admin request #2430 and functional-test PR #146
are open. Their future closure is not assumed to qualify a replacement package.

**Not qualified:** any corrected 2026.2.0 build or later MKL version, its availability,
or its compatibility with the full MolSysMT test stack. No new runtime has been
installed or tested by this follow-up report.

## What was refuted

- A greater version is necessary: a new build of the same version can repair
  missing files or dependencies.
- Marking the broken build unavailable proves a modern replacement works:
  the solver may simply return the already qualified 2026.1.0 line.
- A passing import alone proves the numerical ABI: complex and integer-interface
  conventions also need functional evidence.
- #402's source recovery permits removing the ceiling: that recovery deliberately
  excluded the failing release.

## Scope and exclusions

Track and qualify retirement of the source-test workaround. Keep public runtime
floors, optional dependency coverage and scientific behavior unchanged unless a
separate justified change is required. Do not install an unqualified runtime
into the maintainer's development environment. This is not a release-publication
authorization or an automatic block on an otherwise qualified existing runtime.
No recurring automation or scheduled monitoring is created by this issue.

## Acceptance criteria

- Identify the corrected candidate with version, build, channel, platform,
  package URL and SHA-256; record the actual complete solved environment.
- Demonstrate that qualification uses that candidate rather than silently falling
  back through the current ceiling.
- Retain passing interface-sensitive numerical, import and consumer smoke evidence
  for the affected platform/Python routes.
- Remove or revise the workaround together across its four maintained workflow
  routes and update current guidance, with applicable dependency/governance gates.
- Close with the exact tested source and artifact identities, retained regression
  guards and the maintained document that absorbs the resulting constraint policy.
