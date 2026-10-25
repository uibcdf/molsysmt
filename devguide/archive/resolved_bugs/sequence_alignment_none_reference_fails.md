---
summary: Sequence-based alignment fails with its documented self-reference default.
issue: uibcdf/molsysmt#452
status: resolved
opened: 2026-10-24
closed: 2026-10-24
severity: medium
verification: reproduced
area: [structure, alignment]
guard: tests/structure/align/test_sequence_alignment_contract.py::test_self_reference_uses_original_selected_reference_structure
normative:
blocked_by: []
supersedes: []
---

# Sequence-based alignment fails with its documented self-reference default

**Reported:** 2026-10-24, native reproduction during bound-addon receiving under
uibcdf/molsysmt#421 / uibcdf/molsysviewer#264; filing explicitly authorized.
**Status:** resolved; native correction, guards and maintained documentation are complete.

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


## Correction and working evidence — 2026-10-24

Resolve None to the query before every sequence or selection operation. Keep
reference_selection's established default, preserve the selected original
reference structure, and delegate fit/units/precision/publication to the existing
least_rmsd_fit owner. No full reference snapshot or additional molecular copy is
introduced by this wrapper. Both engines and query/reference structure scopes
are validated before coordinate publication. Empty scopes reject explicitly.

The original source from 99cb83107 was executed separately on the new local
multi-component fixture: implicit reference still raises ArgumentError for
molecular_system=None. The repaired path is checked against independently
constructed rigid poses, not only parity with explicit self reference. Tests
cover omitted/None/self/external inputs, reference structure 1, repeated and
nonconsecutive query structures, units and both native ownership modes.

Working source checks pass: 184 native/sequence tests in 24.43 seconds, the
public doctest in 8.28 seconds, and 61 real-view fitting checks in 17.44 seconds.
The addon continues forwarding defaults unchanged. Its successful in-place
sequence-fit admission now relies on the native nonempty-anchor guarantee,
rather than misinterpreting the native Boolean population through generic select.
The invalid-input rejection token still distinguishes failed validation from a
partial scientific write. Broader regression and executed documentation are
being completed before publication. CPU evidence does not qualify GPU execution
or any installed package.

## Final local verification — 2026-10-24

The broad structural/PBC/sequence/argument matrix passes **1,950 tests in
51.66 seconds** with pytest-receptor and 12 workers. Network-marked tests are
excluded explicitly; the existing unmarked RCSB-neighbor case was allowed its
required network access. No failures or skips occurred. Legacy H5MSM,
intentional GPU-unavailability and deliberately tiny-memory-budget warnings are
retained; GPU fallback checks do not establish GPU execution.

The final focused native, argument, recipe/course and real-view fitting matrix
passes **633 tests in 28.87 seconds**, after adding malformed ragged-selection
rejection. The one public alignment doctest passes. Six actual notebooks execute
successfully, and all 14 fast repository gates, signature stability and full Ruff
lint/format checks pass. Sphinx HTML builds with the accepted existing warning
population under uibcdf/molsysmt#144. No public signature, dependency floor,
installed artifact, release or optional GPU qualification is changed or claimed.
Publication and applicable CI are verified separately after the source commit.
