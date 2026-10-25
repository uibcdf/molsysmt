---
summary: Sequence-based alignment fails with its documented self-reference default.
issue: uibcdf/molsysmt#452
status: open
opened: 2026-10-24
closed:
severity: medium
verification: reproduced
area: [structure, alignment]
guard:
normative:
blocked_by: []
supersedes: []
---

# Sequence-based alignment fails with its documented self-reference default

**Reported:** 2026-10-24, native reproduction during bound-addon receiving under
uibcdf/molsysmt#421 / uibcdf/molsysviewer#264; filing explicitly authorized.
**Status:** open; scientific correction belongs to the native owner.

## What

`molsysmt.structure.least_rmsd_align(molsys)` fails with its declared `reference_molecular_system=None` default, although its public parameter contract says None uses the input system. Supplying `reference_molecular_system=molsys` explicitly works on the same bundled peptide and CPU route.

Reproduced independently of MolSysViewer in `molsyssuite@uibcdf_3.14` (Python 3.14.7), at provider commit `fd2b28a1d4f299466964fd0bf69f5358973b7af4`. The in-progress local center/get_center repair is separate; least_rmsd_align and get_sequence_identity match that commit.

## How

```python
import molsysmt as msm

molsys = msm.convert(
    msm.systems['pentalanine']['traj_pentalanine.h5msm'],
    structure_indices=[0, 8, 3],
)

# ArgumentError: molecular_system has value None.
msm.structure.least_rmsd_align(molsys, use_gpu=False)

# On the same system this returns a fitted MolSys.
msm.structure.least_rmsd_align(
    molsys, reference_molecular_system=molsys, use_gpu=False,
)
```

Run the two calls separately after observing the exception. The sequence-identity helper resolves its local None reference to the query, but least_rmsd_align subsequently calls `select(reference_molecular_system, ...)` on its still-None variable while constructing the reference anchors. The public native error is `ArgumentError` for `molecular_system=None`.

## Why

The omitted and explicit-None references should have the documented self-reference behavior, with the same scientific output and state effects as explicitly passing the input system. Resolve it in MolSysMT; the addon must preserve native defaults rather than silently substituting a reference.

Please add independent pytest guards covering omitted/None/explicit-self/external references, selected reference structures, nonconsecutive/repeated query structures, sequence-derived fit anchors versus whole-component movement, independent/in-place returns and source ownership, length units/precision where supported, invalid references or insufficient anchors without unintended coordinate writes, and edited-structure interaction invalidation. Verify physical coordinates/RMSD and source/reference preservation; parity alone does not prove the geometric result.

Related consumer work: `uibcdf/molsysmt#421` and `uibcdf/molsysviewer#264`. The bound tools integration will qualify explicit-reference calls and disclose this limitation until the scientific owner resolves it. No scientific workaround or package/release qualification is requested.


## What is measured and what is assumed

Both native CPU calls above were executed on the same bundled three-structure
peptide. The implicit reference raises ArgumentError, whereas the explicit
reference returns MolSys. The failure does not require a Viewer, GPU or periodic
handling. Broader numerical and optional-engine behavior is not certified by
this reproduction.

## What was refuted

The peptide and explicit native self-reference are accepted; sequence conversion
and Biopython are available. No addon binding, reference replacement or scene
synchronization participates in the failure.

## Scope and exclusions

The declared None-reference behavior is the defect. Explicit-reference calls
remain available for separate scientific receiving. The addon must not inject a
replacement, choose fit populations or compute an alternate rigid transform.

## Acceptance criteria

Protect omitted/None/self/external references and their physical results with
an addressable native pytest guard. Preserve independent and in-place returns,
selected structures, reference ownership and whole-component movement, and reject
invalid fits before unwanted writes. Native ownership chooses implementation;
closing requires the guard, final evidence and archive/index reconciliation.

## Provenance

Python 3.14.7 on Linux in molsyssuite@uibcdf_3.14; source
fd2b28a1d4f299466964fd0bf69f5358973b7af4. Legacy H5MSM and best-effort Biopython
form warnings were retained. This is source evidence, not artifact qualification.
