---
summary: Sequence identity counts non-sequence groups and returns shifted group indices.
issue: uibcdf/molsysmt#439
status: open
opened: 2026-10-23
closed:
severity: medium
verification: reproduced
area: [topology, sequence, indexing]
guard:
normative:
blocked_by: []
supersedes: []
---

# Sequence identity counts non-sequence groups

**Reported:** 2026-10-23, native-source inspection while receiving the tools
addon under uibcdf/molsysviewer#264 and uibcdf/molsysmt#421; filing authorized
by the principal maintainer.
**Status:** open; no scientific fix is included in the addon wrappers.

## What

Bundled pentalanine contains ACE, five ALA groups and NME. Native alignment
against itself returns two identical AAAAA strings, but identity returns
71.42857142857143 percent and source group lists [0, 1, 2, 3, 4]. Those lists
include ACE and omit the last ALA. Both the percentage and correspondence are
wrong for the aligned amino-acid sequence.

```python
import molsysmt as msm

molsys = msm.convert(
    msm.systems['pentalanine']['traj_pentalanine.h5msm'],
    to_form='molsysmt.MolSys', structure_indices=[0],
)
msm.topology.get_sequence_alignment(molsys, reference_molecular_system=molsys)
# ('AAAAA', 'AAAAA')
msm.topology.get_sequence_identity(molsys, reference_molecular_system=molsys)
# (71.42857142857143, [0, 1, 2, 3, 4], [0, 1, 2, 3, 4])
msm.topology.get_sequence_identity(
    molsys, selection="group_type=='amino acid'",
    reference_molecular_system=molsys,
    reference_selection="group_type=='amino acid'",
)
# (100.0, [1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
```

## How

[topology/get_sequence_identity.py](../../molsysmt/topology/get_sequence_identity.py)
selects all source groups before requesting a converted amino-acid alignment.
Its counter indexes that unfiltered group list for each non-gap sequence letter,
and its final denominator is len(group_indices). Sequence conversion excludes
terminal caps, so these domains differ. The alignment helper alone returns the
correct five-letter strings. A correction needs the converter's actual
sequence-to-source-group mapping, rather than assuming every group is a letter.

## Why

Capped or mixed molecular systems can report a wrong identity and highlight
unrelated source groups. This is a native scientific result issue, independent
of Viewer binding, coordinates, rendering or synchronization.

## What is measured and what is assumed

Measured: default self-comparison and explicit amino-acid selection results above,
including indices. Other polymers, mixed populations, gapped and reordered
selections need native regression coverage; they were not exhaustively tested.

## What was refuted

No addon is imported in the reproduction. Explicit amino-acid selections repair
this case without changing aligner settings. Closed uibcdf/molsysmt#360 concerns
copy/identity-format conversion of Biopython values, a different mechanism.

## Scope and exclusions

The addon preserves native results and documents this limitation. No wrapper
formula override, hidden atom preparation or new alignment engine is proposed.
Existing frozen package candidates and publication pauses remain unchanged.

## Acceptance criteria

Native identity uses groups that actually contribute sequence letters, returns
correct source indices in both systems, and self-comparison of capped pentalanine
is 100 percent. Guard capped/uncapped, mixed-group and independently selected
reference inputs without silently changing selection semantics. Record the
chosen empty-sequence policy and cover gaps where source indices shift.

## Provenance

Observed 2026-10-23 on Linux in molsyssuite@uibcdf_3.14, Python 3.14.7,
Biopython 1.88. Provider HEAD 3c43a9554858f015b33a5a2940926f5ec56bab32 with
concurrent unrelated source work; the reviewed sequence files are unchanged.
The installed development version reports 0.23.0+160.gb35a29326.dirty and is
not a clean installed artifact qualification. The demo's H5MSM 0.4 legacy warning
is retained; it does not explain the sequence/group-axis mismatch.
