---
summary: Selected composite conversion applies trajectory positions to a reference-only provider.
issue: uibcdf/molsysmt#698
status: active
opened: 2026-11-10
closed:
severity: high
verification: reproduced
area: [convert, selection]
guard: tests/basic/convert/mult_to_one/test_convert_mult_to_molsysmt_MolSys.py::test_selected_trajectory_positions_never_index_the_reference_only_provider
normative:
blocked_by: []
supersedes: []
---

# Selecting a composed trajectory must not index its reference

## What / How / Why

During #695's native Iterator integration, both reference/trajectory input orders
fail with h5py IndexError: trajectory position one is used to read a reference
provider with only position zero. The protected 363-case intermediate receiving
has 361 passes and these two failures. The input is the bundled one-structure
villin H5MSM inventory plus its twenty-structure DCD; both components describe
one molecular system, rather than independent systems to concatenate.

The shared converter already prunes off-axis structural attributes, but still
passes the global structure selection into its chosen base converter. Filtering
attribute contributions alone does not protect that base read or remove the
reference's already materialized series. This is a general conversion defect,
not a Viewer-specific issue or a scientific ring/interaction calculation.

## Correction and exclusions

The existing axis resolver still rejects two different multi-structure lengths.
Its pruning helper now returns off-axis counts to the conversion owner. A chosen
reference base reads at most its one representative (or all of a zero-structure
provider), not selected trajectory positions. A native result discards that
reference structure payload together before receiving the on-axis observations.
Stable inventory and system-level assembly metadata remain available. Existing
association reconciliation and selected conversion continue to own chemistry,
other structural observations, named analyses and units.

No coordinate matching, implicit reference broadcasting, new data model, unit
policy or public argument is introduced. The existing off-axis warning remains.
The earlier archived structure-axis report explains provider choice; this record
tracks the additional selected-base read missed by that original correction.

## Receiving

The public direct regression selects positions [11, 2, 11] from both input orders
and compares exact trajectory coordinates, missing reference-only labels/time,
and the single-state association. Neighboring native Iterator tests verify
nonconsecutive/repeated positions, shorter final chunks, caller-owned native
outputs, other observations and evaluated-empty coverage/state maps.

After the correction, all 535 affected builder/iterator/PDBQT/composite-conversion
cases pass without omissions. The broader clean source, registered science,
documentation and receiving gates remain separate until their results are
recorded. Supplemental #698 adds no original milestone weight or release authority.
