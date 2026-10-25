---
summary: Sequence-based structural alignment treats atom-index selections as group indices.
issue: uibcdf/molsysmt#453
status: resolved
opened: 2026-10-24
closed: 2026-10-24
severity: medium
verification: reproduced
area: [structure, alignment, selection]
guard: tests/structure/align/test_sequence_alignment_contract.py
normative:
blocked_by: []
supersedes: []
---

# Sequence-based structural alignment treats atom-index selections as group indices

**Reported:** 2026-10-24, independent native reproduction after a real multi-component
addon receiving test exposed the mismatch; filing explicitly authorized.
**Status:** resolved; atomic selection and paired-group correspondence are corrected.

## What

`molsysmt.structure.least_rmsd_align` mixes atom-index and group-index semantics for its `selection`. The documented expression selecting Cα atoms works; the equivalent integer list produced by `msm.select` fails because it is interpreted as group indices inside sequence identity. This also makes the reference selection's numeric scope suspect; its exact matrix should be reviewed by the scientific owner.

Reproduced without MolSysViewer at source `fd2b28a1d4f299466964fd0bf69f5358973b7af4` in `molsyssuite@uibcdf_3.14`, Python 3.14.7. Alignment and sequence source files match that commit; unrelated center/get_center work is not involved.

## How

```python
import molsysmt as msm

molsys = msm.convert(
    msm.systems['pentalanine']['traj_pentalanine.h5msm'],
    structure_indices=[0],
)
selection = msm.select(molsys, selection="atom_name=='CA'")
print(selection)  # [8, 18, 28, 38, 48]

# Returns a MolSys.
msm.structure.least_rmsd_align(
    molsys, selection="atom_name=='CA'",
    reference_molecular_system=molsys,
    reference_selection="atom_name=='CA'", use_gpu=False,
)

# ArgumentError: out-of-range group indices, despite valid atom indices.
msm.structure.least_rmsd_align(
    molsys, selection=selection,
    reference_molecular_system=molsys,
    reference_selection="atom_name=='CA'", use_gpu=False,
)
```

Actual error: `'selection' contains out-of-range group indices [8, 18, 28, 38, 48]; valid indices are in [0, 7).`

The alignment function forwards `selection` directly to `topology.get_sequence_identity`; its `_sequence.sequence_with_groups` helper asks `basic.get(element='group', selection=selection, ...)`, which interprets numeric indices in the group domain. The alignment later uses its selection in `basic.select(element='atom', ...)` and as a component-selection anchor. The same integers therefore address incompatible domains within one operation.

## Why

Define and enforce one unambiguous public selection contract for structural alignment. Its documented atomic-anchor use and supported numeric/boolean selection types must agree, without silently interpreting atom indices as groups. Preserve the sequence helper's own group-domain contract; resolve the owning structural operation's atom-to-group correspondence explicitly instead of changing its consumer in the addon.

Please protect both query and reference sides with independent pytest cases spanning expression/list/tuple/ndarray/boolean selections, different index spaces and atom/group numbering, capped peptide source-group maps, nonconsecutive/repeated structures, mismatched and insufficient anchors, multiple components, whole-component motion versus anchor populations, independent/in-place returns and rejection before unwanted coordinate writes. Include physical coordinate/RMSD and reference-preservation assertions, not just parity of two native calls.

Related: `uibcdf/molsysmt#421`, `uibcdf/molsysviewer#264`, and the distinct None-reference defect `uibcdf/molsysmt#452`. Current addon receiving qualifies expression selections and passes native arguments unchanged; it must not convert integer lists to strings or invent correspondence rules. No package/publication qualification is claimed.


## What is measured and what is assumed

The query-side mismatch is independently reproduced with one native pentalanine
structure. The expression returns MolSys and its equivalent CA atom indices
raise ArgumentError in the group domain. A larger two-component real-view test
encounters the same failure. Reference-side permutations and other numeric types
are acceptance scope, not claims of executed reproductions.

## What was refuted

The selected atom indices are valid in the same molecule, and the explicit
reference avoids uibcdf/molsysmt#452. The identical expression selection works.
The failure occurs in native sequence handling before coordinate publication;
no Viewer synchronization, GPU or periodic transform participates.

## Scope and exclusions

Define the owning structural alignment's input selection domain without changing
sequence identity's independent group-domain API. The addon qualifies expression
selections and must not convert integer selections into strings or perform its
own correspondence calculation.

## Acceptance criteria

Add addressable native pytest guards for the scientific and selection contracts
above. Retain actual atom/group correspondence, proper whole-component motion,
reference/source ownership and clear invalid-input behavior. Closure requires
native evidence, a guard and archive/index reconciliation.

## Provenance

Python 3.14.7, Linux, molsyssuite@uibcdf_3.14. Native scientific source matches
fd2b28a1d4f299466964fd0bf69f5358973b7af4; unrelated center/get_center work remains
separate. Legacy H5MSM and best-effort Biopython form warnings are retained.
This is local source evidence, not installed-package qualification.


## Correction and working evidence — 2026-10-24

Resolve both selections once as atom populations on their respective source
axes, including full-axis Boolean masks through the existing index/mask owner.
Project per-atom group_index values to unique original groups in topology
sequence order and call get_sequence_identity with those group positions.
Its group-domain public API, source-group mapping, scoring, identity criterion
and optional attribution are unchanged. Only identically aligned amino-acid
groups supply anchors; caps remain excluded without compacting their positions
into a misleading molecular index space.

Retain the returned group pairs while constructing the atomic correspondence.
Selected atom names must be unique and agree within each aligned group pair;
otherwise reject before writes. Numeric order and repetition describe an atom
population, not an arbitrary atom-pair ordering. Reference atom permutations
therefore remain meaningful. Explicit arbitrary correspondences belong to
least_rmsd_fit. Group membership is indexed in a linear pass before iterating
matched groups; no full selected-atom scan is repeated for every group.

All atoms of components touched by the original query population move under the
common fit. Source groups without identity matches can contribute moving
components but no anchors. Unselected components and structures stay fixed.
No new public callable, chemical store, sequence provider or compiled formula
is introduced; generic get/select, group-sequence identity and the existing
compiled Kabsch fit remain the owning tools.

The original 99cb83107 function was executed on the new fixture and rejects
valid CA atom positions [8,18,28,38,48] as out-of-range group positions. Working
checks include all expression/list/tuple/array/Boolean combinations on both
axes, different cap/water offsets, atom permutations, sequence gaps, ambiguous
or missing names, insufficient/collinear anchors and source/reference ownership.
They also protect invalidation and immutable earlier analysis views. A readable
H5MSM and an MDTraj reference are exercised without writing either. MDTraj's
float32 input is compared with an independent float64 SVD fit to the actual
quantized reference, rather than incorrectly expecting its pre-conversion pose.
The first SVD test draft also averaged the reference in float32; correcting that
oracle did not change production code. Native/source tests and real-view masks
pass; final broad and documentation evidence follows before publication.

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
