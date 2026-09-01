---
summary: Conda cannot resolve MolSysMT on supported Python 3.13 because MolSysViewer has no compatible build
issue: uibcdf/molsysmt#195
status: open
opened: 2026-09-01
closed:
severity: high
verification: reproduced
area: [build, deps]
guard:
normative:
blocked_by: []
supersedes: []
---

# Conda cannot resolve MolSysMT on supported Python 3.13

**Reported:** 2026-09-01, while verifying the corrected dependency contract for
uibcdf/molsysmt#193 against the live Conda channels.
**Status:** open. MolSysMT resolves on Python 3.12 but not on its supported Python 3.13.

## What

MolSysMT declares Python 3.11--3.13 support in `pyproject.toml`. Its Conda recipe has an
unversioned runtime dependency on `molsysviewer`. A dry-run resolution of that recipe's
runtime dependencies for Python 3.13 fails:

```text
LibMambaUnsatisfiableError: Encountered problems while solving:
  - package molsysviewer-0.5.3-py310_1 requires python >=3.10,<3.11.0a0,
    but none of the providers can be installed
```

The solver lists MolSysViewer builds only for Python 3.10, 3.11 and 3.12. Repeating the
same command with `python=3.12` succeeds and selects `molsysviewer-0.7.0-py312_1`.

## How

The live `uibcdf` channel contains MolSysViewer 0.5.3, 0.6.0, 0.6.1 and 0.7.0, each
built for Python 3.10--3.12. It has no Python 3.13 artifact. The current MolSysViewer
source declares `requires-python = ">=3.11"`, and its Conda publication workflow already
contains a Python 3.11--3.13 matrix, so the source contract and intended build matrix
include 3.13 while the published channel does not.

MolSysMT's recipe therefore becomes unsatisfiable when its own supported Python 3.13 is
selected, before MolSysMT itself can be built or installed.

## Why

Python 3.13 is part of MolSysMT's declared 1.0 support matrix. A distribution path that
cannot install the package on that interpreter cannot support the declared matrix, even
when the source and wheel gates are green. This blocks an honest Python 3.13 Conda claim
for MolSysMT 1.0.

Severity is high because the failure affects a supported installation path and release
matrix cell. It is explicit rather than silent: the solver names MolSysViewer.

## What is measured and what is assumed

**Measured:** a live-channel dry run on Python 3.13 fails; the otherwise identical
Python 3.12 dry run succeeds; `conda search -c uibcdf --override-channels --json
molsysviewer` reports no Python 3.13 build; MolSysViewer source and workflow declare
Python 3.13.

**Assumed:** the MolSysViewer stabilization work will produce the next publishable
release. This report does not assume its version or publication date.

## What was refuted

**The new ArgDigest and SMonitor floors make the environment unsatisfiable.** Refuted.
The channel now contains ArgDigest 0.12.1 and SMonitor 0.13.0 for Python 3.11--3.13, and
the complete dependency set resolves on Python 3.12.

**MolSysViewer does not support Python 3.13.** Refuted at source level. Its package
metadata and CI matrix include 3.13; only the channel artifact is absent.

## Scope and exclusions

In scope: making the MolSysMT Conda dependency graph resolvable on every Python version
MolSysMT claims for 1.0, and guarding that resolution in the release evidence.

Out of scope: changing MolSysViewer while its stabilization is owned by the parallel
team; changing MolSysMT's source-level Python support; and the manifest-divergence fix
tracked separately as uibcdf/molsysmt#193.

## Acceptance criteria

1. A MolSysViewer Conda artifact compatible with Python 3.13 is available from the
   channel used by MolSysMT's recipe.
2. The MolSysMT runtime dependency set resolves in dry-run mode for Python 3.11, 3.12
   and 3.13.
3. The release evidence includes a guard or matrix job that fails if any supported
   Python version loses a resolvable MolSysViewer dependency.

## Dependencies and risks

Resolution depends on the separately owned MolSysViewer stabilization and publication
work. Publishing an interim artifact from this repository would cross that ownership
boundary and is deliberately excluded.

## Provenance

Measured 2026-09-01 on Linux x86_64 with Conda 26.5.3 and the libmamba solver against
`uibcdf`, `conda-forge` and `ambermd`. MolSysMT worktree based on `6eea33df9`.
