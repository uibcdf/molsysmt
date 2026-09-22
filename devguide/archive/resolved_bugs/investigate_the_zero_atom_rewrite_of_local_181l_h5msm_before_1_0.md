---
summary: Investigate the zero-atom rewrite of local 181l.h5msm before 1.0
issue: uibcdf/molsysmt#216
status: resolved
opened: 2026-09-22
closed: 2026-09-22
severity: medium
verification: reproduced
area: [tests, form]
guard: tests/form/molsysmt_H5MSMFileHandler/test_get_structural_attributes_comprehensive.py::TestGetBFactorFromAtomNonEmpty::test_all_structures_all_atoms
normative:
blocked_by: []
supersedes: []
---

# Investigate the zero-atom rewrite of local 181l.h5msm before 1.0

**Reported:** 2026-09-22, during inspection of a pre-existing working-tree modification.
**Status:** Resolved for the local fixture incident. The tracked artifact is
restored locally and the unsafe extraction path is tracked separately in
uibcdf/molsysmt#235. The historical caller remains unknown.

## What

At discovery, the working copy of molsysmt/data/h5msm/181l.h5msm was an H5MSM
file with zero atoms and bonds and one empty coordinate frame. The manifest expects 1441
atoms, 1322 bonds, and one frame. The existing asset validator reproduces the
failure:

    $ python devtools/scripts/validate_demo_assets.py
    AssertionError: ('181l.h5msm', [0, 0, 0, 0, 0, 0, 0, 1])

The file was already modified before the PDBQT and SDF proposal reports were
written. This report records a local defect and a pre-1.0 review obligation;
it does not claim that main contains a broken 181l artifact.

## How

The tracked HEAD version contains the manifest's expected hierarchy, whereas
the working copy contains empty topology datasets and coordinates of shape
(1, 0, 3). The working file has H5MSM creation metadata dated
2026-09-21T17:48:52. Its structure resembles a newly initialized H5MSM file
followed by writing one empty structure. The H5MSMFileHandler writer initializes
zero-sized datasets when opened in write mode, but the available evidence does
not identify the command, notebook, or process that targeted this path.

The existing [demo asset validator](../../../devtools/scripts/validate_demo_assets.py)
checks actual hierarchy sizes against
[demo_manifest.json](../../../molsysmt/data/demo_manifest.json). It catches this
exact failure; the immediate question is how the local copy was overwritten
and whether a normal workflow can repeat it.

## Why

181l.h5msm is a bundled demo used by tests and examples. Before restoration,
the demo-asset gate failed and tests expecting a nonempty lysozyme system
could not provide valid evidence. The
[1.0 execution plan](../../pending_proposals/release_1_0_execution_plan.md)
requires a clean exact-commit candidate with passing release gates, so this
review and a correct fixture are pre-1.0 work.

Severity is medium because the bad artifact was an uncommitted local change,
the versioned artifact is intact, and the existing manifest validator detects
it. The reproducible in-place overwrite remains a risk until constrained.

## What is measured and what is assumed

**Measured:** The validator command above fails with eight observed counts
[0, 0, 0, 0, 0, 0, 0, 1], against manifest counts
[1441, 302, 141, 141, 5, 6, 1322, 1]. Direct HDF5 inspection gives
0 atoms, 0 bonds, and coordinate shape (1, 0, 3) for the working file.
The working file is 42,128 bytes; the tracked HEAD artifact is 293,219 bytes
and contains 1441 atoms and 1322 bonds. Its HDF5 creation timestamp is above.

**Assumed:** The exact historical command or process is unknown. The
reproductions below establish a viable mechanism, not the identity of the
historical caller.

## What was refuted

**Main already contains the empty fixture:** false. The tracked HEAD artifact
has the expected atom and bond counts.

**No integrity check exists:** false. validate_demo_assets.py fails on this
file, and the release gate includes that validator. The earlier resolved
[truncated-artifact report](truncated_demo_artifact_reached_main_no_push_path_gate_checks_bundled_data.md)
describes the broader guard history.

**The PDBQT/SDF issue filing caused the empty data:** false as a chronology
claim. The file was already modified when that work began. The later rebase
restored the pre-existing modification and updated its filesystem mtime, but
did not create the zero-atom HDF5 content.

## 2026-09-22 investigation and local restoration

The empty local file was preserved outside the repository before restoring
`181l.h5msm` byte for byte from `origin/main`. The restored file matches its
tracked Git blob and is no longer modified. Running
`python devtools/scripts/validate_demo_assets.py` passed for all 17 H5MSM
0.4 demos and the legacy fixture. The targeted
`tests/form/file_structures_yaml/test_roundtrip.py::test_structures_yaml_roundtrip`
also passed using the restored 181L asset. These checks establish local
restoration, not release-candidate certification.

The empty file's internal creation time is
`2026-09-21T17:48:52.130842`. Its topology has zero atoms and bonds, and its
single coordinate frame has shape `(1, 0, 3)`. On a separate temporary copy
of the intact artifact, the following public call returned the input path
and replaced that copy with the same counts and coordinate shape:

```python
msm.extract(temporary_181l_h5msm, selection='atom_index<0')
```

The reproduction had the same file size (42,128 bytes) and all 51 HDF5
objects matched the preserved empty file in paths, shapes, data, and
attributes other than creation and modification times. Serializing an
explicitly empty native `MolSys` produced the same HDF5 contents. These
observations identify empty-MolSys serialization as a reproducible mechanism;
they do not distinguish the historical caller.

The `file:h5msm` extract adapter defaults `output_filename` to the input path
when none is supplied. For H5MSM 0.4, it materializes the selected `MolSys`,
closes the input, and passes the same path to the writer, which opens it with
`h5py.File(filename, 'w')`. The source at commit `284038cfc`, the last
MolSysMT commit before the file's internal creation time, already had this
behavior. An empty selection therefore silently replaces the original file;
other subset selections can also replace it in place. The normal 181L demo
generator is unlikely to explain this isolated rewrite because its other
outputs retain older filesystem timestamps. No available command log
identifies the precise caller at 17:48.

The remaining adapter fix is tracked in uibcdf/molsysmt#235: extraction
without an explicit output path must preserve its input, with a test for empty
and nonempty selections. This fixture incident can close without treating that
separate product defect as fixed.

## Scope and exclusions

Review the local 181l overwrite, decide whether it is reproducible through a
normal generation, conversion, or documentation workflow, and return the
fixture to a verified state before the 1.0 candidate is certified. Do not
replace the tracked artifact merely because the working copy differs; inspect
the intended source and output first. This report does not reopen the
general bundled-data gate work resolved in #182 or the broader push-trigger
policy still tracked in #185.

## Acceptance criteria

1. Record the outcome of the writer investigation. If exact attribution is
   unavailable, state that explicitly and document which normal write paths
   were checked.
2. Restore the local 181l fixture from a verified source or regenerate it
   through the documented recipe, with manifest counts and supported data
   preserved. Do not commit the zero-atom copy.
3. The demo-asset validator and a relevant 181L fixture test pass locally.
   The exact release-candidate commit still requires its full release gate
   under the 1.0 execution plan.
4. If a repeatable in-repository write path is found, transfer its correction
   and source-preservation guard to a distinct tracked defect before closing
   this fixture incident.

## Dependencies and risks

This can be resolved independently of #185 because the existing offline
validator already detects the bad copy. Restoring the binary before
understanding a reproducible writer could leave the same overwrite path
active; the investigation must separate evidence from inference.

## Provenance

Initially measured 2026-09-22 on host nauta, Python 3.13.14, h5py 3.16.0,
with HEAD 1e18f239e. The tracked artifact was read through git show into a
temporary file; the working artifact was opened read-only with h5py. A later
step restored the local fixture after preserving its empty contents outside
the repository.

## Resolution

The local `181l.h5msm` was restored from the intact `origin/main` artifact;
Git no longer reports it as modified. Its expected 1,441 atoms, 1,322 bonds
and one structure passed the demo-asset validator. The selected pytest guard
reads the bundled H5MSM and requires a `(1, 1441)` b-factor array, so it fails
if the fixture is replaced again by the observed zero-atom file. The targeted
guard and a separate 181L structures round-trip test passed locally.

The empty file was reproduced through a normal public subset extraction on
a temporary copy. The exact historical caller could not be recovered from
available logs; direct empty-MolSys serialization can produce the same file.
The general implicit overwrite defect and its future fix are tracked in
uibcdf/molsysmt#235. The full 1.0 release gate remains a separate candidate
requirement under the execution plan.
