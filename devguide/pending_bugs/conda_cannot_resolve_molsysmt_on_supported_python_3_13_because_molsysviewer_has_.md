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
**Status:** active. The source-side staging path is implemented; publication and the
installed-pair matrix remain pending.

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
5. The release-event path produces build 1 and does not use `--no-test`; it resolves the
   staged Viewer and runs the recipe test before any package reaches the `main` label.
   Distinct build numbers prevent overwriting the validated bootstrap coordinates.

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
to the build environment's interpreter. Windows staging publication and the
installed-pair gate remain pending.

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

**Settled after the original measurement:** the coordinated release pair is MolSysMT
0.22.0 and MolSysViewer 0.21.0. The Viewer candidate identity and its remaining blocked
checks are recorded in the implementation checkpoint above.

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

1. The MolSysViewer 0.21.0 `noarch: python` package is available from the staging channel
   and declares Python 3.11--3.13 support.
2. The MolSysMT runtime dependency set resolves in dry-run mode for Python 3.11, 3.12
   and 3.13.
3. The staging evidence installs exact MolSysMT 0.22.0 and MolSysViewer 0.21.0 packages
   on all five native platforms with Python 3.11, 3.12 and 3.13, and fails on a version,
   provenance, native-extension or packaged-resource mismatch.

## Dependencies and risks

Resolution depends on the separately owned MolSysViewer staging step. The agreed
bootstrap publishes MolSysMT only from this repository and validates the exact staged
pair after the Viewer team publishes its own artefact; neither repository publishes on
behalf of the other.

## Provenance

Measured 2026-09-01 on Linux x86_64 with Conda 26.5.3 and the libmamba solver against
`uibcdf`, `conda-forge` and `ambermd`. MolSysMT worktree based on `6eea33df9`.
