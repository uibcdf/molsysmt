---
summary: Smoke environment selects an MKL runtime that cannot import NumPy
issue: uibcdf/molsysmt#402
status: open
opened: 2026-10-22
closed:
severity: medium
verification: reproduced
area: [ci]
guard:
normative:
blocked_by: []
supersedes: []
---

# Smoke environment selects an MKL runtime that cannot import NumPy

**Reported:** 2026-10-22 during exact-head qualification after uibcdf/molsysmt#396.
**Status:** Open; a bounded test-environment backend selection is under qualification.

## What

[Smoke run 39820372523](https://github.com/uibcdf/molsysmt/actions/runs/39820372523),
source `9f04699273d89a800fa0977073d9a6d3033c372b`, fails at `Test import`
before executing its test suite. The job reports:

```text
INTEL oneMKL ERROR: .../libmkl_gf_lp64.so.3: cannot open shared object file
Intel oneMKL FATAL ERROR: Cannot load libmkl_gf_lp64.so.3.
Process completed with exit code 2.
```

The solved environment contains NumPy 2.5.4 `py314hd3a7d6b_0`, MKL 2026.2.0
`hd2095e1_881` and libblas 3.11.0 `11_h5875eb1_mkl`. Controlled source-version
validation and package installation finish before the failing import step.

## How

`devtools/conda-envs/test_env.yaml` leaves the BLAS implementation unconstrained.
The CI solve selects the MKL route, whose native runtime cannot load the library
named in the error. This establishes an unusable solved environment, not the
precise upstream packaging or loader cause. It does not establish a defect in
the biological assembly calculation.

Select `libblas=*=*openblas` in this source-test environment using the documented
[conda-forge backend mechanism](https://conda-forge.org/docs/maintainer/knowledge_base/#switching-blas-implementation).
Keep runtime package requirements and user-selected BLAS implementations unchanged.
The environment is shared by source-test workflows, so this deliberately selects
their backend; it does not claim coverage of every BLAS implementation.

## Why

The failed runtime prevents exact-source smoke qualification despite passing
local numerical regressions. Retrying without a declared backend can select the
same unusable runtime and gives no durable recovery route.

## What is measured and what is assumed

**Reproduced remotely:** Ubuntu/Python 3.14, job 119969751412 in the run above.
The job log identifies the solved packages and fatal error. The previous local
843 integrated tests and 481 parser tests pass in the existing development
environment; those results do not substitute for the failed hosted import.
No independent upstream MKL package reproduction or alternative-backend CI
success is claimed yet.

## What was refuted

- The numerical regression suite failed: it never executed in this hosted job.
- The hosted import checks passed because the package installed: installation
  and controlled-version validation finish, then the native runtime fails.
- Local green results qualify the hosted environment: the dependency solves differ.

## Scope and exclusions

Constrain only the source-test environment backend. Do not raise runtime floors,
replace NumPy, suppress import errors or weaken mandatory CI gates. This is not
a cross-platform/installed-candidate or MKL scientific-accuracy qualification.

## Acceptance criteria

- The solved exact-source CI environment uses the declared OpenBLAS route.
- The existing import checks and smoke test suite actually execute and pass.
- Dependency-contract and governance checks accept the environment change.
- Retain the failed run and successful recovery run as distinct evidence.

## Provenance

2026-10-22, GitHub-hosted Ubuntu, Python 3.14; exact commit and native package
versions above. GH Run Receptor identified the failed import job; the native
job-log endpoint supplied the MKL diagnostic while workflow logs were pending.
