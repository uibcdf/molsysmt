---
summary: Build one ABI3 Conda artifact per native platform
issue: uibcdf/molsysmt#202
status: resolved
opened: 2026-09-02
closed: 2026-09-04
verification: measured
area: [build, performance, ci]
guard: devtools/tests/test_conda_release_workflows.py
normative:
blocked_by: []
supersedes: []
---

# Build one ABI3 Conda artifact per native platform

**Reported:** 2026-09-02, while measuring the first native Conda staging builds.
**Status:** Resolved. The redundant post-build render was removed, the single-artifact
design passed on all five native platforms and all fifteen interpreter cells, and the
production staging/release workflow now uses it.

## What

Build MolSysMT once per native platform against CPython 3.11's stable ABI and declare a
runtime range of Python 3.11 through 3.13. Validate that exact Conda artifact in clean
Python 3.11, 3.12, and 3.13 environments before it can replace the current three-build
matrix. This would reduce the release build from fifteen Rust compilations to five
without reducing the fifteen-platform/runtime staging gate.

## How

The existing extension is already built with `py-limited-api = "cp311"`, and the wheel
gate builds one ABI3 wheel per platform and tests it across supported interpreters.
[Conda CEP 20](https://github.com/conda/ceps/blob/main/cep-0020.md) defines the matching
platform-package contract, so the recipe should use it directly:

1. set `build/python_version_independent: true` and build with both Python 3.11 and
   `python-abi3 3.11` in the host environment;
2. retain the platform subdirectory while emitting CEP 20's `noarch: python` relocation
   metadata;
3. declare `python >=3.11,<3.14` explicitly, require the `cpython` and
   `_python_abi3_support` exports, and ensure no exact `python_abi 3.11` dependency leaks
   into the final package metadata;
4. install the same artifact into clean Python 3.11, 3.12, and 3.13 environments and
   import the compiled extension in each;
5. retain the current three-variant recipe until the experiment passes on all five
   native release platforms.

Before this architectural change, the shared build action will stop invoking a second
`conda build --output` render after the real build. Its isolated output directory is a
complete and less ambiguous source of the package paths.

The ABI3 branch is conditional inside the shared recipe and has a separate one-entry
variant file. The production workflow now selects that branch and file explicitly. The
legacy three-variant rendering remains available as a rollback path, but it is no
longer the publication path.

## Why

The current workflow compiles the same ABI3 Rust extension three times on each of five
platforms. The Windows corrective staging job took 28 minutes 53 seconds; the three
builds themselves occupied 22 minutes 22 seconds. A second recipe render performed only
to rediscover output paths added approximately 2 minutes 3 seconds after compilation.
This latency makes iteration on packaging defects unnecessarily expensive.

## What is measured and what is assumed

**Measured:** GitHub Actions run `33682123937` completed the Windows job in 28 minutes
53 seconds. Its log timestamps delimit 22 minutes 22 seconds for the three-variant
`conda build` invocation and approximately 2 minutes 3 seconds for the following
`conda build --output` invocation.

```bash
gh run view 33682123937 --repo uibcdf/molsysmt --log
```

**Inspected:** `pyproject.toml` sets both setuptools-rust and wheel metadata to the
CPython 3.11 limited API. The wheel workflow already tests one platform artifact with
Python 3.11, 3.12, and 3.13.

**Measured:** action run `33687074611` passed installation and import of both fixture
variants on Linux and Windows after the second render was removed. Against run
`33668608034`, total Linux time fell from 3 minutes 44 seconds to 2 minutes 14 seconds,
and Windows fell from 5 minutes 45 seconds to 4 minutes 27 seconds.

```bash
gh run view 33687074611 --repo uibcdf/action-build-and-upload-conda-packages
gh run view 33668608034 --repo uibcdf/action-build-and-upload-conda-packages
```

**Measured:** local `conda build --output` with the ABI3 selector and exclusive config
resolved exactly one Linux package before the dedicated `pyabi3` build string was added:

```text
molsysmt-0.21.0-py311h03bb3b7_0.conda
```

**Measured:** the first five-platform experiment, run `33690618780`, passed the exact
artifact's metadata and Python 3.11--3.13 native execution on four platforms. Total job
times were Linux x86-64 5:18, Linux ARM64 4:43, macOS ARM64 5:47, and macOS x86-64
16:44. Windows built one correctly named `pyabi3` artifact in 8:41 instead of the prior
three-variant build's 22:22, then exposed an over-strict validator assumption: PyO3's
stable-ABI Windows extension is `_rust.pyd`, not `_rust.abi3.pyd`. The validator now
uses the platform's real filename convention, and the workflow accepts a target input so
only the failed platform needs to be repeated.

```bash
gh run view 33690618780 --repo uibcdf/molsysmt
```

**Measured:** targeted Windows run `33692126791` then passed metadata inspection and
executed the exact package under Python 3.11, 3.12, and 3.13 in 13:24. Its only failure
was the final evidence upload: the Node-based upload action could not interpret the
POSIX `/tmp` path emitted inside Git Bash. The workflow now copies the already validated
artifact to the runner's native temporary directory before upload; package behavior did
not fail.

**Measured:** final targeted Windows run `33693263538` passed the complete experiment,
including evidence upload, in 13:40. Its single build step took 9:25 and the metadata
plus Python 3.11, 3.12, and 3.13 runtime validation took 2:30. Together with the four
platforms that passed run `33690618780`, this proves five artifacts across fifteen
platform/interpreter cells. The design reduces Rust compilations from fifteen to five,
a 66.7% reduction, while retaining all fifteen runtime validations.

```bash
gh run view 33693263538 --repo uibcdf/molsysmt
```

**Measured:** production staging run `33849332945` built and uploaded the five
MolSysMT 0.22.0 build-2 artifacts successfully. The complete matrix took 19:56,
bounded by macOS x86-64; individual job times were Linux ARM64 4:12, Linux x86-64
4:34, macOS ARM64 8:05, Windows 10:49, and macOS x86-64 19:56. An independent query of
the `uibcdf/label/staging` channel found exactly one build-2 artifact in every native
subdirectory, each with the required ABI3 metadata and no `python_abi` dependency:

| Subdirectory | SHA-256 |
| --- | --- |
| `linux-64` | `6fa364cba5b22140c3205b3dc032d017250e05919a4092a5c02d5367a7ba8b2f` |
| `linux-aarch64` | `352fc567edd1d43442b84fd8d52ec52e2825b439ca5a15540947c1ed3d6445b0` |
| `osx-64` | `7e9cc6d8ded8f30da405784d672e82ad6a00dda55b8609dce9ed661ff84fbe25` |
| `osx-arm64` | `d7e660ab794b15e0e542f505444e2726a94633d35a4ac75ce78e3bd535c94d8b` |
| `win-64` | `7075929e7636126a68f9e85fd24b15a494158125406548d7cc72ce952579123b` |

```bash
gh run view 33849332945 --repo uibcdf/molsysmt
conda search --override-channels -c uibcdf/label/staging \
  --subdir <native-subdirectory> molsysmt=0.22.0 --json
```

## What was refuted

- Forcing four compilation jobs is not the primary design: Cargo already parallelizes
  compilation, while the dominant repetition is three independent ABI-identical builds.
- Sharing Cargo's target directory may help cold builds, but it retains three package
  builds and introduces cross-variant cache correctness concerns.
- Skipping Python 3.12 and 3.13 validation is rejected. The optimization applies only to
  compilation; runtime coverage remains a release requirement.
- The earlier statement that ABI3 is irrelevant inside Conda was a convention, not a
  Conda limitation. Approved CEP 20 explicitly exists to reduce a platform package's
  Python-minor build matrix while preserving platform-specific binaries.

## Scope and exclusions

This proposal covers MolSysMT native Conda artifacts and the shared action work needed
to measure them efficiently. It does not convert pure-Python sibling packages into
platform packages, reduce the supported platform set, weaken the staging installation
matrix, or publish experimental artifacts. General dependency-solver performance is
outside this scope.

## Acceptance criteria

- The shared action's Linux and Windows integration jobs build, install, and import both
  fixture variants after removal of the second render.
- One MolSysMT Conda artifact is built on each native platform.
- The package metadata contains `python >=3.11,<3.14` and no exact `python_abi`
  dependency, plus the CEP 20 `cpython` and `_python_abi3_support` requirements.
- The exact same artifact installs and its native extension imports under Python 3.11,
  3.12, and 3.13 on every supported native platform.
- The experiment reports per-platform timings against the three-build baseline.
- The production workflow changes only after those conditions pass, and the invariant
  is retained by an automated guard.

All criteria passed. Production uses staging build number 2 so the ABI3 artifacts
supersede the pre-existing builds 0 and 1; release publication uses the distinct later
build number 3.

## Dependencies and risks

Incorrect ABI3 metadata could create a package that the solver admits but whose
extension cannot load. Testing only installation would miss that failure, so the gate
must execute the compiled module's reviewed export and minimum-image contract. The
Windows CPython 3.12 debug run-export defect tracked in #201 is avoided by a Python 3.11
build host, but final metadata still requires direct inspection.

## Provenance

GitHub-hosted `windows-2025` runner, Conda recipe Python variants 3.11--3.13, Rust 1.97.1,
actions `uibcdf/action-build-and-upload-conda-packages@v2.0.2` and `v2.0.3`, Conda CEP
20, 2026-09-02. Runs `uibcdf/molsysmt/actions/runs/33682123937` and
`uibcdf/action-build-and-upload-conda-packages/actions/runs/33687074611`, plus MolSysMT
runs `33690618780`, `33692126791`, and `33693263538`.
