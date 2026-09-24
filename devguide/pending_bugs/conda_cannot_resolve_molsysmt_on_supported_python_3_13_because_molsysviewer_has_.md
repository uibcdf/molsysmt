---
summary: Conda cannot resolve MolSysMT on supported Python 3.13 because MolSysViewer has no compatible build
issue: uibcdf/molsysmt#195
status: active
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
**Status:** active. MolSysMT 0.22.0 build 4 and MolSysViewer 0.23.1 build 1
are staged. The first exact 15-cell hosted gate exposed a Windows import
defect and an environment-recording command unavailable on micromamba-only
runners; a corrected build 5 and second gate are pending.

## Coordination checkpoint — 2026-09-24

Hosted exact-pair run `35961600369` pinned MolSysMT ABI3 build 4 and
MolSysViewer noarch build 1 on all five platforms and Python 3.11--3.13.
All 15 package installation steps succeeded. All Linux, ARM and macOS
installed-pair validation steps succeeded (12 cells). Linux x86-64 then
recorded all three explicit environment artifacts. On Linux ARM and both
macOS architectures (nine cells), only the subsequent record step failed:
`conda: command not found`. The workflow used `conda list --explicit`
although `setup-micromamba` supplies micromamba, not Conda, on those runners.
The record step now uses the action-provided `MAMBA_EXE` to export the
named environment explicitly. The validator can now select one native
platform for a focused three-interpreter rerun before allocating the full
15-cell gate; the default remains all five platforms.
Focused ARM run `35963306739` then passed its preparation and all three
Python jobs. Its three environment artifacts were uploaded. A downloaded
Python 3.13 record contains `@EXPLICIT`, `# platform: linux-aarch64`,
Viewer `0.23.1-py_1` and MolSysMT `0.22.0-pyabi3*_4` URLs from the staging
label. GH Run Receptor currently reports that successful targeted run as
failed because the repository rule still expects all five platforms; this
tool limitation is tracked as uibcdf/gh-run-receptor#54. The GitHub run
conclusion and job conclusions are all successful. Keep the five-platform
expectation for the final full-matrix gate.

The three Windows cells reached validation but failed importing
`molsysmt.configure` because `os.sysconf` is unavailable. This source defect
is tracked separately as uibcdf/molsysmt#239 and has a local regression
covering both POSIX and Windows memory discovery. No Windows functional
success is claimed from run `35961600369`. The source fix requires an
additive ABI3 build 5; the public release path is reserved as build 6.
Neither the old build nor Viewer build 1 is to be overwritten.
Targeted producer run `35963198451` subsequently succeeded from exact
candidate `ec5cbd41bf121f595fbb88e16f9aa9f3728581ea`. An independent
Anaconda inventory found `win-64/molsysmt-0.22.0-pyabi3h2d2bc06_5.conda`
with the `staging` label. Windows installed-pair run `35964451004` passed
all three Python 3.11--3.13 jobs against Viewer build 1, including BCIF,
PDB-text, Viewer and explicit-environment checks. The Windows import defect
is resolved as uibcdf/molsysmt#239. The remaining task is to publish build
5 on the other four native platforms and repeat the full 15-cell gate.

## Coordination checkpoint — 2026-09-23

The 2026-09-20 plan below was overtaken by hosted work that day. MolSysMT run
`35498945251` completed all five native ABI3 jobs and published build 3 to
staging. MolSysViewer corrected its internal version mismatch in
`uibcdf/molsysviewer#91`; run `35502257553` published additive noarch build
`py_1`, and a clean Python 3.13 pair reported both Viewer version surfaces
as exactly `0.23.1`. Neither package is a public release.

The first 15-cell pair run, `35499866604`, failed in every cell. Its nine
Linux x86-64 and macOS cells reached validation and rejected Viewer build 0:
installed metadata reported `0.23.1+0.g736e8274.dirty`, not the requested
`0.23.1`. Three Linux ARM and three Windows cells failed earlier in the
Conda solver because support-library artifacts were unavailable; the
subsequent micromamba cleanup errors were secondary. Do not weaken the
version check or classify those six failures as action setup defects.

On 2026-09-23, live-channel dry runs for Linux ARM and Windows/Python 3.11
resolved MolSysMT build 3, Viewer build 1, and staged noarch SMonitor 0.16.0,
DepDigest 0.11.0, ArgDigest 0.13.0, and PyUnitWizard 0.26.0. This removes
the previously observed **solver** gap in those two cells; it does not yet
prove installed behavior, other Python minors, or every native platform.

Build 3 predates the PDB/Biopython fix below. MolSysMT run `35932403014`
completed all five native jobs from exact commit
`432e039ad7e9ee7c9a1f803ddbdc824d2a743435`. GH Run Receptor reported
five successful producer uploads; an independent Anaconda package inventory
found exactly one new build-4 ABI3 archive on each of the five native
platforms, all with the `staging` label. The release route is reserved as
build 5; neither channel was overwritten or promoted.

A fresh Linux/Python 3.13 environment installed staged MolSysMT build 4 and
Viewer build 1. Both Conda records name the staging channel; Biopython is
absent. The installed-pair validator passed version identity, native import,
BCIF conversion, four-atom PDB-text conversion and Viewer load, and Viewer
resources. This is **one local installed cell**, not the 15-cell hosted gate.
An initial solve using older repodata selected MolSysMT build 3 despite build
4 already being present; updating the local environment to build 4 exposed
the need to pin both exact build numbers in the workflow. A Conda dry run
confirmed that `pyabi3*_4` and `py_1` select the intended pair, and the
hosted validation workflow now requests those build identities explicitly.
Keep the staged and public labels separate.

## Clean-install PDB guard — 2026-09-23

A local Linux/Python 3.14 clean-pair probe found an additional packaging hazard
that is not specific to Python 3.14: an unprefixed amino-acid string detector
imported optional Biopython while sweeping form candidates. When Bio was
absent, `get_form(PDB_TEXT)` failed before reaching the PDB detector. The
resolution and exact local artifacts are recorded under
[`#238`](../archive/resolved_bugs/pdb_text_detection_imports_optional_biopython.md).

The main-line detector now counts canonical amino-acid letters without Bio;
its regression explicitly masks Bio and checks both an amino-acid sequence
and PDB text. The exact-pair validator now also classifies, converts, and
loads four-atom PDB text through Viewer. The focused source and validator
selection passed 36 tests, and this validator passed against the corrected
local Python 3.14 installed pair. The same validator fails against the
uncorrected local pair at the absent-Bio import, proving the new gate detects
this regression. These are **local** results, not evidence
that the older staged `0.22.0`/`0.23.1` pair has passed. MolSysMT build 4
contains this fix; it still must pass the full 15-cell staged-pair gate.

## Coordination checkpoint — 2026-09-20

The missing Viewer coordinate is no longer the immediate blocker:

- MolSysViewer run `35491679182`, exact commit
  `736e82740ad39072a5d055065e03b001bb4293c5`, published
  `uibcdf/label/staging/noarch::molsysviewer-0.23.1-py_0`. Its runtime contract is
  `molsysmt >=0.22.0` and `python >=3.11,<3.14`.
- The existing five-platform MolSysMT 0.22.0 build-2 ABI3 set predates the fix for
  uibcdf/molsysmt#200 and does not declare `py-mmcif`. It is historical evidence, not a
  releasable candidate.
- At this checkpoint, the next non-overwriting MolSysMT coordinate was build 3, and
  the eventual release path was reserved as build 4. The 2026-09-23 checkpoint
  above supersedes those numbers after the additional PDB fix.
- The exact-pair gate now rejects a MolSysMT Conda record without `py-mmcif` and performs
  an offline conversion of the bundled HP35 BCIF file, checking its 596 atoms. This
  turns the clean-install defect into behavior exercised in every one of the 15
  platform/interpreter cells.

At this checkpoint the remaining sequence was to publish MolSysMT 0.22.0 build 3 from an
exact commit to `staging`, audit its five channel records independently, and run the
exact 0.22.0/0.23.1 pair across five platforms and Python 3.11--3.13. Nothing from this
sequence is promoted to the main channel.

## Coordination checkpoint — 2026-09-19

The package cycle is now measured from both repositories rather than inferred from their
recipes:

- MolSysMT run `33849332945`, exact commit
  `e5820d4794f8ce31a1f64e345c5edf9073ade975`, published build-2 ABI3 artefacts to
  `uibcdf/label/staging` for `linux-64`, `linux-aarch64`, `osx-64`, `osx-arm64` and
  `win-64`. Live channel queries find all five.
- A Linux dry-run against staging resolves `molsysmt=0.22.0` on Python 3.12 but not
  Python 3.13. The failing solver tree reaches MolSysMT's hard MolSysViewer dependency
  and finds only the old interpreter-specific public packages. Publishing MolSysMT to
  `main` first would hide the cycle rather than validate it.
- MolSysViewer now has a manual exact-SHA staging path that builds its noarch package
  against staged MolSysMT and keeps its recipe test enabled. Its hosted `CI`, `CI_e2e`
  and notebook workflows can select staging only through an explicit manual input;
  ordinary runs keep using the public channel.
- The former MolSysViewer 0.21.0 candidate identity below is historical. MolSysViewer
  has since tagged 0.22.0 and 0.23.0, and both tags predate packaging and hosted-CI fixes
  made under uibcdf/molsysviewer#88 and #89. They must not be moved. A new candidate
  version and commit must be frozen and recorded before its staging dispatch.

For that reason, the exact-pair workflow no longer defaults the MolSysViewer version.
The operator must name the newly frozen version already present in staging; an old
default must not decide release identity by inertia.

The reusable release semantics exposed by this pilot are owned centrally by
`uibcdf/molsyssuite#27`. This repository retains its native ABI3 implementation and
evidence, and must converge on the accepted suite contract rather than letting the local
workflow become a separate policy.

## Implementation checkpoint — 2026-09-02

The maintainers settled the dependency and release decisions that were still assumed in
the original report:

- MolSysViewer remains a hard MolSysMT dependency.
- MolSysMT 0.22.0 will be staged before MolSysMT 1.0.0.
- MolSysViewer 0.21.0 is the coordinated counterpart. Its candidate is
  `b0888d9a78243b8d1829a2793f42b816e0b1643e`; its source release gate reports 9 passed,
  0 failed and 2 blocked. The Qt check is blocked by the absence of a display on the
  candidate machine, and the Conda check is blocked by the package cycle described below.
- MolSysViewer's platform-independent Python and JavaScript payload is prepared as one
  `noarch: python` package with the runtime floor `molsysmt >=0.22.0`. This replaces the
  old assumption that Python 3.13 needed a separate `py313` Viewer artefact.

The accompanying MolSysMT change implements Route A from
[`../pending_proposals/migration_off_the_in_house_publication_actions.md`](../pending_proposals/migration_off_the_in_house_publication_actions.md):

1. `devtools/conda-build/meta.yaml` builds with the native Rust compiler metapackage on
   every platform and the C compiler metapackage on Linux to capture the `libgcc` run
   export. It pins Rust 1.97.1, separates `build` and `host`, and imports both `molsysmt`
   and `molsysmt._rust` in the package test.
2. `.github/workflows/build_and_upload_conda_packages.yaml` runs one native job per
   platform. Each invocation of the UIBCDF publication action builds Python 3.11, 3.12
   and 3.13 without conversion, then uploads that platform only if all three variants
   succeeded. A failed platform can be rerun without rebuilding successful platforms.
3. A manual build of an exact SHA creates a temporary local `0.22.0` tag and publishes
   build 0 only to the `staging` label. It uses `--no-test` solely for this bootstrap
   package, because MolSysViewer 0.21.0 cannot yet be installed without MolSysMT 0.22.0.
4. After the Viewer team stages 0.21.0, `validate_conda_staging.yaml` installs the exact
   pair in all 15 native cells. It checks versions, non-editable provenance, the Rust
   extension, Viewer runtime resources and the explicit Conda environment.
5. The release-event path produces build 2 and does not use `--no-test`; it resolves the
   staged Viewer and runs the recipe test before any package reaches the `main` label.
   Build 1 is reserved for non-overwriting bootstrap repairs such as uibcdf/molsysmt#201;
   distinct build numbers prevent overwriting the validated bootstrap coordinates.

This is **Implemented** and locally contract-tested. Native workflow run `33637476601`
compiled all 15 platform/interpreter combinations, including three successful Windows
packages. Its common upload job failed before contacting Anaconda because it referenced
a nonexistent third-party action tag. Platform-atomic run `33645401415` subsequently
published all three variants for `linux-64`, `linux-aarch64`, `osx-64` and `osx-arm64`.
Windows built its three variants but retained a carriage return in each path reported by
`conda build --output`, so publication stopped when the action checked those paths.

`uibcdf/action-build-and-upload-conda-packages@v2.0.2` normalizes that Windows output.
Its integration run `33668608034` builds Python 3.11 and 3.12 variants on both Ubuntu
and Windows, installs each artifact in a clean matching environment, and imports it.
MolSysMT's manual publication dispatch also accepts one native `target`, allowing the
remaining Windows platform to be rebuilt without allocating the four successful
platform runners. Local `conda render` checks produce distinct `py311`, `py312` and
`py313` build-0 coordinates for both `linux-64` and `win-64`; the recipe's Python
requirements are governed by `conda_build_config.yaml` so the variants cannot collapse
to the build environment's interpreter. Targeted run `33671942326` then published
`py311h2d2bc06_0`, `py312h2d2bc06_0` and `py313h2d2bc06_0` for `win-64` from exact
candidate `0856e0c71c47e4d95adb54d2671062d7197423a4`. All 15 build-0 artifacts are staged,
but a direct metadata audit found that the Windows/Python 3.12 artifact inherited an
erroneous `*_debug_cpython` run export from conda-forge CPython 3.12.14 build 2. That
single cell was invalid. Targeted run `33682123937` published clean Windows build-1
artifacts from `d53268c449434be761b4762c48ee5e47538b8ec2`; the Python 3.12 record no longer
contains the debug constraint. The repair is resolved as uibcdf/molsysmt#201.
MolSysViewer staging and the installed-pair gate remain pending.

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
source declares Python 3.11--3.13 support. Its coordinated 0.21.0 recipe is now
`noarch: python`, so one staged artefact will cover that interpreter range while the
published channel still does not.

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

**Settled after the original measurement:** the first proposed coordinated pair was
MolSysMT 0.22.0 and MolSysViewer 0.21.0. That candidate is historical. The currently
frozen staged counterpart is MolSysViewer 0.23.1 at the commit recorded in the
2026-09-20 checkpoint.

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

1. A newly frozen MolSysViewer candidate is recorded here, available from the staging
   channel as `noarch: python`, and declares Python 3.11--3.13 support.
2. The MolSysMT runtime dependency set resolves in dry-run mode for Python 3.11, 3.12
   and 3.13.
3. The staging evidence installs exact MolSysMT 0.22.0 and the recorded MolSysViewer
   candidate on all five native platforms with Python 3.11, 3.12 and 3.13, and fails on
   a version, provenance, native-extension or packaged-resource mismatch.

## Dependencies and risks

MolSysViewer's separately owned staging step is complete for 0.23.1 build 1,
and MolSysMT build 4 contains the PDB fix. Windows additionally needs the
portable memory-budget correction in build 5 (uibcdf/molsysmt#239).
Resolution depends on exact-pair validation across all claimed
platform/interpreter cells.
Each repository continues to publish only its own artefact.

## Provenance

Measured 2026-09-01 on Linux x86_64 with Conda 26.5.3 and the libmamba solver against
`uibcdf`, `conda-forge` and `ambermd`. MolSysMT worktree based on `6eea33df9`.
