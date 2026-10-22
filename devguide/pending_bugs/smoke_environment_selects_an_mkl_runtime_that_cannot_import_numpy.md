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

The first recovery tried the documented
[conda-forge OpenBLAS selection](https://conda-forge.org/docs/maintainer/knowledge_base/#switching-blas-implementation).
[Run 39821410897](https://github.com/uibcdf/molsysmt/actions/runs/39821410897),
source `453458a5a4cd34905e3f4ac56b82e49d6d241767`, instead failed solving
its full dependency set. The solver reports a MDTraj/PyTables/NumExpr path
whose available alternatives require either MKL BLAS or a `nomkl` constraint
incompatible with the rest of this solve. The cleanup `ENOENT` is secondary,
not the solver's root cause. The OpenBLAS dependency entry is removed.

The known-green baseline [run 39711713560](https://github.com/uibcdf/molsysmt/actions/runs/39711713560)
uses MKL 2026.1.0 `hd2095e1_245` with the same NumPy, libblas and NumExpr
builds named above. The next recovery applies a temporary `mkl<2026.2`
constraint through the four maintained source-test workflow `condarc` blocks.
Unlike an environment dependency, a pinned-package constraint must not require
MKL on platforms/routes that do not install it. Keep runtime package floors,
optional test dependencies and user-selected backends unchanged. Remove this
fence only after a replacement MKL runtime passes hosted numerical qualification.

## Why

The failed runtime prevents exact-source smoke qualification despite passing
local numerical regressions. Retrying without a declared backend can select the
same unusable runtime and gives no durable recovery route.

## What is measured and what is assumed

**Reproduced remotely:** Ubuntu/Python 3.14, job 119969751412 in the run above.
The job log identifies the solved packages and fatal error. The previous local
843 integrated tests and 481 parser tests pass in the existing development
environment; those results do not substitute for the failed hosted import.
A local Linux/Python 3.14 dry solve of the complete unchanged dependency list,
using the same strict channels and `pinned_packages: [mkl<2026.2]`, succeeds.
It selects MKL 2026.1.0 `hd2095e1_245`, NumPy 2.5.4 `py314hd3a7d6b_0`,
libblas 3.11.0 `11_h5875eb1_mkl`, NumExpr 2.14.2 `mkl_py314h85e79cc_1`,
MDTraj 1.11.2 and AmberTools 26.0. Only solver metadata is downloaded into
isolated temporary paths; no new environment or packages are installed.
This qualifies solvability, not import or numerical execution. No independent
upstream MKL package reproduction, other-platform solve or successful recovery
CI is claimed yet. The historical baseline and failed recoveries remain distinct.

## What was refuted

- The numerical regression suite failed: it never executed in this hosted job.
- OpenBLAS is a drop-in full-stack recovery: the attempted solve fails on the
  optional dependency graph, so that route is withdrawn.
- The hosted import checks passed because the package installed: installation
  and controlled-version validation finish, then the native runtime fails.
- Local green results qualify the hosted environment: the dependency solves differ.

## Scope and exclusions

Constrain only the source-test workflow runtime. Do not raise runtime floors,
replace NumPy, suppress import errors or weaken mandatory CI gates. This is not
a cross-platform/installed-candidate or MKL scientific-accuracy qualification.

## Acceptance criteria

- The solved exact-source CI environment excludes the observed failing MKL release
  and does not force MKL onto platforms that otherwise omit it.
- The existing import checks and smoke test suite actually execute and pass.
- Dependency-contract and governance checks accept the environment change.
- Retain the failed run and successful recovery run as distinct evidence.

## Provenance

2026-10-22, GitHub-hosted Ubuntu, Python 3.14; exact commit and native package
versions above. GH Run Receptor identified the failed import job; the native
job-log endpoint supplied the MKL diagnostic while workflow logs were pending.
