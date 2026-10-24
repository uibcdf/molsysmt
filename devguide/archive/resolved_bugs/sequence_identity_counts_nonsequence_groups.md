---
summary: Sequence identity counts non-sequence groups and returns shifted group indices.
issue: uibcdf/molsysmt#439
status: resolved
opened: 2026-10-23
closed: 2026-10-24
severity: medium
verification: reproduced
area: [topology, sequence, indexing]
guard: tests/topology/get_sequence_identity/test_sequence_source_groups.py
normative:
blocked_by: []
supersedes: []
---

# Sequence identity counts non-sequence groups

**Reported:** 2026-10-23, native-source inspection while receiving the tools
addon under uibcdf/molsysviewer#264 and uibcdf/molsysmt#421; filing authorized
by the principal maintainer.
**Status:** resolved in the native scientific owner.

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

[topology/get_sequence_identity.py](../../../molsysmt/topology/get_sequence_identity.py)
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

## Implementation — 2026-10-24

Native one-letter conversion and identity now share a private letter/group
projection. Only contributing amino-acid groups enter the molecular sequence,
its denominator and source maps. Sequence-only inputs retain their supplied
letters and selected source positions without inventing an atom inventory.
The public identity tool aligns the projected letters with the existing
Biopython scoring and maps non-gap matches back through the paired source maps.
Order and repeated selections survive. None as reference uses the query system;
empty, undefined and pre-gapped sequences raise an explicit argument error.
The public tool also gains its standard skip_digestion boundary and a lazy
Biopython dependency guard.

The denominator remains query length, preserving established MolSysMT semantics.
Inspection of Ensembler's calculate_seq_identity at revision
264930d28d3d4987c4fc0c03caba6cf0066e12ca verifies that its denominator is the
shorter sequence instead. Documentation explicitly distinguishes our adaptation;
optional Ackredit credits that reference and the actually executed Biopython
version after success. No new alignment score or provider is introduced.

All six original source-map guards failed before correction. The expanded
initial selection passes 25 tests, including real Ackredit, independent query
normalization, gaps, mixed groups, native Topology/MolSys/H5MSM and sequence
objects. Final qualification adds a fresh-process absence guard and executes
the documentation. A distinct existing three-letter-to-Biopython codec refusal
is reproduced and tracked under uibcdf/molsysmt#443; it is not silently repaired
or treated as qualified by the source-map correction.

## Final source qualification — 2026-10-24

The combined length-observable, heavy-execution, sequence-mapping, sequence-form
and conversion-truth selection passed **511 tests** in 35.73 seconds with
`--receptor=llm -n 12`. Three public doctests are included. Network-marked
sequence tests were explicitly excluded; no installed/release matrix was run.
The 66 warnings are 63 expected legacy H5MSM notices and three intentional
memory-pressure observations from tiny test budgets. No test failed or skipped.

The two observable tutorials, unit-safety module 09, large-ensemble cookbook,
sequence-identity tutorial and topology module 13 executed successfully. All
250 selected public docstrings passed fidelity/content validation. The final
fast-gate and Sphinx results are retained in the qualification receipt:
[`native_observable_repairs_20261024.json`](../../../devtools/data/native_observable_repairs_20261024.json).

The primary guard asserts literal source maps and query-normalized percentages
for capped/mixed inventories, gaps, reordering, repeated selections, independently
selected references, sequence-only forms and empty/undefined input rejection.
A real Ackredit session verifies software/reference credit and reuse; an
import-blocked fresh process verifies genuine provider absence and lazy startup.
Provider failure preserves the completed scientific tuple.

## CI signature qualification follow-up — 2026-10-24

The first hosted smoke run for `1123eeb7d` failed its parent-signature guard:
adding the standard optional `skip_digestion=False` slot had not been registered
as an intentional additive change. The scientific correction and the retained
511-case source receipt are unchanged; that receipt is historical evidence for
its recorded hashes, not a claim that the first CI run passed.

A function-scoped registry declaration now names exactly this append-only change,
its owning #439 and its guard. The guard additionally executes the historical six
positional arguments and rejects a string bypass flag, preserving both ordinary
calls and explicit validation. Comparing the complete repaired source with
`bae6d0101` now reports zero unauthorized signature changes. The source-group and
two API-validator test modules pass **38 tests** in 11.72 seconds; their two
warnings are expected legacy H5MSM reads. No runtime scientific code or global
signature-checking rule was modified by this follow-up.
