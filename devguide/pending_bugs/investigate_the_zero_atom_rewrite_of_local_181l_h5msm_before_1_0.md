---
summary: Investigate the zero-atom rewrite of local 181l.h5msm before 1.0
issue: uibcdf/molsysmt#216
status: open
opened: 2026-09-22
closed:
severity: medium
verification: reproduced
area: [tests, form]
guard:
normative:
blocked_by: []
supersedes: []
---

# Investigate the zero-atom rewrite of local 181l.h5msm before 1.0

**Reported:** 2026-09-22, during inspection of a pre-existing working-tree modification.
**Status:** Open, pre-1.0 review. The tracked artifact on main is intact; the local working copy is not.

## What

The working copy of molsysmt/data/h5msm/181l.h5msm is an H5MSM file with zero
atoms and bonds and one empty coordinate frame. The manifest expects 1441
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

The existing [demo asset validator](../../devtools/scripts/validate_demo_assets.py)
checks actual hierarchy sizes against
[demo_manifest.json](../../molsysmt/data/demo_manifest.json). It catches this
exact failure; the immediate question is how the local copy was overwritten
and whether a normal workflow can repeat it.

## Why

181l.h5msm is a bundled demo used by tests and examples. In the current
working tree, the demo-asset gate fails and tests expecting a nonempty
lysozyme system cannot provide valid evidence. The
[1.0 execution plan](../pending_proposals/release_1_0_execution_plan.md)
requires a clean exact-commit candidate with passing release gates, so this
review and a correct fixture are pre-1.0 work.

Severity is medium because the bad artifact is currently an uncommitted local
change, the versioned artifact is intact, and the existing manifest validator
detects it. Its risk would rise if an empty artifact were committed or used in
release validation.

## What is measured and what is assumed

**Measured:** The validator command above fails with eight observed counts
[0, 0, 0, 0, 0, 0, 0, 1], against manifest counts
[1441, 302, 141, 141, 5, 6, 1322, 1]. Direct HDF5 inspection gives
0 atoms, 0 bonds, and coordinate shape (1, 0, 3) for the working file.
The working file is 42,128 bytes; the tracked HEAD artifact is 293,219 bytes
and contains 1441 atoms and 1322 bonds. Its HDF5 creation timestamp is above.

**Assumed:** The precise writer is unknown. The HDF5 shape is consistent with
an empty or failed conversion being written to the fixture path, but that
mechanism has not been reproduced.

## What was refuted

**Main already contains the empty fixture:** false. The tracked HEAD artifact
has the expected atom and bond counts.

**No integrity check exists:** false. validate_demo_assets.py fails on this
file, and the release gate includes that validator. The earlier resolved
[truncated-artifact report](../archive/resolved_bugs/truncated_demo_artifact_reached_main_no_push_path_gate_checks_bundled_data.md)
describes the broader guard history.

**The PDBQT/SDF issue filing caused the empty data:** false as a chronology
claim. The file was already modified when that work began. The later rebase
restored the pre-existing modification and updated its filesystem mtime, but
did not create the zero-atom HDF5 content.

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
3. The demo-asset validator and relevant 181l fixture tests pass in the
   release-candidate working tree. The exact candidate commit passes the
   full release gate before a 1.0 tag.
4. If a repeatable in-repository write path caused the overwrite, remove or
   constrain that path and add an addressable pytest guard for it. At closure,
   name the relevant guard in front matter as required by the reporting
   protocol.

## Dependencies and risks

This can be resolved independently of #185 because the existing offline
validator already detects the bad copy. Restoring the binary before
understanding a reproducible writer could leave the same overwrite path
active; the investigation must separate evidence from inference.

## Provenance

Measured 2026-09-22 on host nauta, Python 3.13.14, h5py 3.16.0, with
HEAD 1e18f239e. The tracked artifact was read through git show into a
temporary file; the working artifact was opened read-only with h5py. No
H5MSM data was modified during this investigation.
