---
summary: Extend MolSysMT Python support to 3.14.
issue: uibcdf/molsysmt#237
status: active
opened: 2026-09-22
closed:
verification: measured
area: [packaging, ci, deps]
guard:
normative:
blocked_by: []
supersedes: []
---

# Extend MolSysMT Python support to 3.14

**Reported:** 2026-09-22, after the public Python 3.14 admission of the
SMonitor, DepDigest, ArgDigest, and PyUnitWizard dependency chain.
**Status:** Active feasibility work. A locally built MolSysMT wheel and its
native extension work on Linux/Python 3.14; the declared package and
MolSysViewer contracts still stop at 3.13.

## What

Extend the supported Python range from 3.11–3.13 to 3.11–3.14 under
`uibcdf/molsyssuite#29`. The target includes MolSysMT's Rust extension,
source and installed-package tests, Conda metadata, the hard MolSysViewer
dependency, and public documentation. The current 0.22.0 MolSysMT /
0.23.1 MolSysViewer staging campaign under `uibcdf/molsysmt#195` remains
the 3.11–3.13 release path; a Python 3.14 claim needs its own later exact
candidate and package evidence.

## How

1. Finish the existing coordinated 0.22.0/0.23.1 installed-pair gate without
   silently expanding either candidate's Python range.
2. Run the full MolSysMT source suite and scientific evidence on Python 3.14
   with representative optional backends. Keep Python 3.11–3.13 lanes.
3. Coordinate MolSysViewer's source, CI, noarch metadata, resources, and
   installed-pair tests on Python 3.14 under `uibcdf/molsysviewer#93`.
   Its interpreter ceiling is an actual dependency boundary, not a
   MolSysMT-only metadata edit.
4. Update MolSysMT classifiers, `requires-python`, the ABI3 Conda runtime
   bound, CI matrices, controlled sibling revisions, package validators,
   documentation, and release notes together. Keep Ruff's target at Python
   3.11 while that is the minimum supported interpreter.
5. Build an exact candidate and exercise the installed extension and BCIF
   conversion across every claimed platform and Python 3.11–3.14. Obtain
   central `authorized` and later `admitted` status according to the
   independent evidence required by the suite policy. Verify every claimed
   public channel after release before changing the public Python badge.

## Why

The public lower dependency chain resolves on Python 3.14. MolSysMT's
`pyproject.toml` still declares `>=3.11.0,<3.14.0`, its ABI3 Conda recipe
declares `>=3.11,<3.14`, and its required source and installed-package
matrices stop at 3.13. MolSysViewer is a hard dependency in both Python and
Conda metadata. Its staged 0.23.1 noarch package also declares
`python >=3.11,<3.14`, so the pair cannot resolve on 3.14 today.

## What is measured and what is assumed

- On commit `b82019dac`, `ruff check --no-cache .` and
  `ruff format --check .` passed; the latter selected 3,361 Python files.
  `python -m pytest --receptor=llm -n 12 --dist loadfile
  devtools/tests/test_ruff_clean.py` passed both selection and execution
  guards. The Ruff migration is complete under `uibcdf/molsysmt#212`.
- A Linux Conda dry run with Python 3.14, excluding MolSysViewer, resolved
  the declared runtime packages from `uibcdf` and `conda-forge`, including
  SMonitor 0.16.0, DepDigest 0.11.0, ArgDigest 0.13.0,
  PyUnitWizard 0.26.0, and py-mmcif 1.1.1. A temporary Python 3.14.7
  environment imported these packages and the `mmcif` module.
- From a sparse clone of the exact commit, `python -m pip wheel --no-deps
  --no-build-isolation --ignore-requires-python` built
  `molsysmt-0.21.0+689.gb82019dac-cp311-abi3-linux_x86_64.whl`.
  The development version is provenance, not a release candidate.
  The wheel was installed with `--no-deps --ignore-requires-python` into
  the temporary Python 3.14.7 environment. The installed extension validator
  passed all 99 expected Rust exports; importing the installed package
  reported the same version as its distribution metadata; converting the
  bundled `1vii.bcif.gz` produced a native `MolSys` with 596 atoms.
  The bypassed metadata makes this source feasibility evidence only.
- A Conda dry run of `python=3.14 molsysviewer=0.23.1` with
  `uibcdf/label/staging`, `uibcdf`, and `conda-forge` failed because
  the staged Viewer package requires `python >=3.11,<3.14`.
  Its own dependency is `molsysmt >=0.22.0`; the pair must be
  coordinated. The full MolSysMT suite and installed pair have not
  been tested on 3.14.
- A paired Linux/Python 3.14.7 source probe from MolSysMT `fe0be24b8`
  and MolSysViewer `251f7759` built both wheels. With the current Python
  bounds bypassed, both imported, the installed extension passed 99 exports,
  the BCIF conversion produced 596 atoms, and MolSysViewer loaded the native
  result. Its MolSysMT/runtime integration selection passed 19 tests.
  MolSysMT's BCIF, Rust-threading, and distribution-manifest selection passed
  18 tests with 12 workers. These tests were run against the installed wheel
  from outside the source tree with `--import-mode=importlib` so the source
  package did not shadow its installed `_rust.abi3.so`.
- The source probe revealed a pre-existing distribution guard mismatch:
  PyPI names the dependency `mmcif`, whereas Conda names the same provider
  `py-mmcif`. The `python-3.14-support` worktree now maps that one known
  name and tests that deleting the Conda dependency is still caught.
  This is part of the remaining `uibcdf/molsysmt#200` gate.
- Candidate wheels from the isolated worktrees now declare Python
  `>=3.11,<3.15` and install on 3.14 without bypassing their Python bound.
  They are not resolver-consistent: `pip check` rejects MolSysViewer's
  `molsysmt>=0.22.0` floor because the source tree still has a 0.21.x
  development identity. CI matrices, full suites, exact candidates, and
  public packages are still outstanding.
- MolSysViewer's candidate source suite on Linux/Python 3.14 executed 2,090
  tests in one 12-worker run: 2,069 passed, five failed, and 16 skipped.
  Its three affected test files passed 208 tests after adding missing
  `jinja2` and `mdtraj` to the probe environment and regenerating a stale
  capability audit. The next gate is a clean full run in the exact pinned
  source-pair workflow on Linux and macOS, not an inference from focused
  reruns. The optional UIBCDF Qt stack still resolves only through a
  Python 3.13 ABI dependency; see `uibcdf/molsysviewer#93`.
- A further installed-wheel test selection across MolSysMT's native objects,
  bundled BCIF adapters, and Rust boundaries passed 641 tests on Linux/
  Python 3.14.7 with 12 workers. The command ran from outside the source
  checkout so the installed ABI3 extension remained the import target.

## What was refuted

- The earlier 13,500-finding Ruff debt is not a current Python 3.14
  prerequisite. The repository-wide gate and its file-selection guard pass.
- PyO3 or the existing `cp311-abi3` extension is not an immediate
  Linux/Python 3.14 import blocker: the actual wheel build and installed
  extension check passed. This does not establish five-platform or
  free-threaded Python 3.14 support.
- Changing only MolSysMT's `requires-python` cannot yield a supported
  installation while the required MolSysViewer package excludes 3.14.

## Scope and exclusions

This proposal covers standard GIL-enabled CPython 3.14. It does not claim
free-threaded `3.14t`, and it does not repurpose the existing 0.22.0
staging artifacts as a 3.14 release. Issues `uibcdf/molsysmt#185`,
`uibcdf/molsysmt#195`, and `uibcdf/molsysmt#200` retain their own
CI and clean-install release gates.

## Acceptance criteria

- MolSysMT and its required MolSysViewer version both declare and test
  Python 3.11–3.14 without losing the older supported lanes.
- The full source suite, scientific evidence, Rust wheel checks, and
  installed Conda pair pass on the claimed interpreters and platforms.
- One exact ABI3 artifact per native platform declares the 3.14 range,
  installs on all four interpreter minors, and passes the installed
  extension and BCIF checks. Package provenance and version identity
  match the frozen candidate.
- A new immutable public release and every claimed package channel pass
  independent clean Python 3.14 installation. Only then does the central
  registry record `admitted` and the README badge claim 3.14.
- A durable pytest guard or normative document records the final contract
  before this proposal is archived and its issue closed.

## Dependencies and risks

MolSysViewer's interpreter contract is tracked in
`uibcdf/molsysviewer#93`; the coordinated Conda release under
`uibcdf/molsysviewer#82` and `uibcdf/molsysmt#195` determines
the publication order. Updating a source matrix before the package
channels are ready is useful feasibility evidence but not admission.
The current Conda package cycle requires an exact staged-pair test.

## Provenance

Linux x86_64; CPython 3.14.7 from conda-forge; MolSysMT commit
`b82019dac`; Rust 1.97.1; PyO3 0.29.0; NumPy, h5py, pandas, and
the named public UIBCDF support libraries from a clean Conda
environment; 2026-09-22. The temporary wheel was built only for
this local feasibility test and was not published.
