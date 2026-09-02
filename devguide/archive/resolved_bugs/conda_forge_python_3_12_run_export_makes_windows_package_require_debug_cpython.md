---
summary: Conda-forge Python 3.12 run export makes Windows package require debug CPython
issue: uibcdf/molsysmt#201
status: resolved
opened: 2026-09-02
closed: 2026-09-02
severity: high
verification: reproduced
area: [build, deps]
guard:
normative: devguide/release_gate.md
blocked_by: []
supersedes: []
---

# Conda-forge Python 3.12 run export makes Windows require debug CPython

**Reported:** 2026-09-02, while auditing the metadata uploaded by MolSysMT native
staging run `33671942326`.
**Status:** resolved and archived. A bounded recipe workaround produced a clean build 1,
and the release gate now requires inspection of actual published Conda constraints.

## What

MolSysMT 0.22.0 build 0 for Windows/Python 3.12 carries both a normal CPython constraint
and an incompatible debug-CPython constraint:

```bash
CONDA_PKGS_DIRS=/tmp/molsysmt-conda-search-pkgs conda search \
  -c uibcdf/label/staging --override-channels --platform win-64 \
  'molsysmt=0.22.0' --json
```

The `py312h2d2bc06_0` record includes:

```text
python >=3.12,<3.13.0a0
python >=3.12,<3.13.0a0 *_debug_cpython
python_abi 3.12.* *_cp312
```

The release build therefore cannot be installed with normal CPython 3.12 even though
the package compiled and uploaded successfully.

## How

The constraint originates in conda-forge's Windows package
`python-3.12.14-hb12b558_2_cpython.conda`, published on 2026-09-02. Although its filename,
index and binary identify it as release CPython, its embedded `info/run_exports.json`
contains:

```json
{"noarch": ["python"], "weak": ["python_abi 3.12.* *_cp312", "python 3.12.* *_debug_cpython"]}
```

Conda-build correctly propagates that weak host run export into MolSysMT. The immediately
preceding `python-3.12.14-hb12b558_1_cpython.conda` contains only the expected
`python_abi 3.12.* *_cp312` weak export.

`devtools/conda-build/meta.yaml` therefore pins only the affected Windows/Python 3.12
host variant to `3.12.14 *_1_cpython`. All other platform/interpreter variants retain
normal solver selection. The staging workflow accepts an explicit build number so a
corrected build 1 can supersede the defective build 0 without overwriting it; production
publication moves to build 2.

## Why

The defect invalidates one of MolSysMT's 15 declared native/Python Conda cells and would
make the coordinated installed-pair gate fail on Windows/Python 3.12. It is high severity
for release delivery because a green build/upload job otherwise presents the artifact as
usable.

## What is measured and what is assumed

**Measured:** the embedded run-export files of conda-forge Windows CPython 3.12.14 builds
1 and 2; the live staging metadata for all 15 MolSysMT 0.22.0 records; and workflow run
`33671942326`.

**Measured:** only `win-64`/Python 3.12 among the 15 MolSysMT records carries the debug
constraint. Linux, Linux ARM64 and both macOS architectures were built before the faulty
upstream package appeared and have clean metadata.

**Assumed:** conda-forge will replace or supersede the faulty Python build. The local
workaround does not depend on when that occurs.

## What was refuted

**The MolSysMT recipe requested debug Python.** Refuted. Its variant file contains only
Python 3.11, 3.12 and 3.13, and the selected Python artifact is named `_cpython`, not
`_debug_cpython`.

**The CRLF repair in publication action v2.0.2 altered package metadata.** Refuted. The
action only removes a carriage return from paths reported by `conda build --output`; the
bad constraint is present inside the upstream Python artifact and is propagated during
the earlier Conda build.

**All 15 newly staged packages require replacement.** Refuted by querying each platform.
Fourteen records have no debug constraint; only the Windows/Python 3.12 cell is bad.

## Scope and exclusions

In scope: producing a normal-CPython-compatible MolSysMT staging artifact for the affected
cell and preventing this exact metadata defect from passing unnoticed.

Out of scope: repairing or removing the conda-forge package, and changing MolSysMT's
declared Python support. Reporting the upstream defect is a separate external action.

## Acceptance criteria

1. A new Windows staging build for Python 3.12 contains no `*_debug_cpython` dependency
   and supersedes build 0 without overwriting it.
2. The Windows Python 3.11 and 3.13 variants remain buildable under the bounded pin.
3. A repository test checks both the conditional host pin and explicit staging build
   number, while the normative release gate requires the eventual installed-pair check
   with normal CPython 3.12.

## Resolution checkpoint — 2026-09-02

Targeted workflow run `33682123937` built and published Windows build 1 from exact
candidate `d53268c449434be761b4762c48ee5e47538b8ec2`. Live channel metadata confirms:

- `py311h2d2bc06_1` requires normal CPython 3.11 and `python_abi 3.11.* *_cp311`;
- `py312h2d2bc06_1` requires normal CPython 3.12 and `python_abi 3.12.* *_cp312`, with
  no `*_debug_cpython` constraint; and
- `py313h2d2bc06_1` requires normal CPython 3.13 and `python_abi 3.13.* *_cp313`.

Build 1 supersedes, but does not overwrite, the defective Python 3.12 build 0. The
repository contract test guards the bounded pin and build-number separation. The durable
release rule is in [`release_gate.md`](../release_gate.md): actual published Conda
constraints must be audited and the exact 15-cell pair must install before release.

## Dependencies and risks

The workaround deliberately pins an exact upstream build only for one cell. It must be
removed after conda-forge provides a corrected later build and before that older build is
no longer available from the channel.

## Provenance

Reproduced 2026-09-02 from Linux x86-64 with Conda 26.5.0 against the live
`uibcdf/label/staging` and `conda-forge` channels. Upstream package archives were
inspected with `cph`; the affected MolSysMT artifact was produced by GitHub-hosted
`windows-2025` using Conda-build 26.7.1.
