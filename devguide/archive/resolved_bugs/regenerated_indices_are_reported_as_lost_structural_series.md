---
summary: Complementary native composition reports regenerated positional indices as lost observations.
issue: uibcdf/molsysmt#675
status: resolved
opened: 2026-11-09
closed: 2026-11-09
severity: low
verification: reproduced
area: [basic, convert, diagnostics]
guard: tests/basic/convert/mult_to_one/test_regenerated_index_diagnostics.py
normative:
blocked_by: []
supersedes: []
---

# Distinguishing regenerated positions from lost structural observations

## What

Composing a coordinate-free native MolSys with one native Structures object
emits StructuralAttributeOffAxisWarning naming atom_index. Conversion later
excludes atom_index and structure_index from copied attributes unconditionally:
these are regenerated positions, not lost scientific observations.

## How

The public guard constructs smiles:CO using optional RDKit, supplies one real
two-atom structure, and composes in both item orders. Before repair both MolSys
cases emit the warning; the standalone Topology route is a negative control.
The private rule control also reproduces index noise beside a real off-axis time
series. No numerical loss is established by the incoming report.

## Why and correction

Exclude only the two regenerated positional attributes from off-axis series
pruning. Preserve the structure-axis/count compatibility rules and warnings for
real observations unavailable on any on-axis item. A real off-axis time remains
absent with a warning; available on-axis coordinates remain present. Do not
filter warning categories or suppress diagnostics in DockingMT.

## Acceptance

Verify both public item orders, stable atom names/counts/indices, exact coordinate
values/units and unchanged source objects. Keep the single-reference/trajectory
and incompatible-axis controls. An early fixture wrongly assumed a reorder for
the documented ascending native-pair extraction and queried atom_index at the
system level; those fixture failures are retained and are not provider defects.


## Resolution — 2026-11-09

Real complementary public composition in both input orders passes without
regenerated-index loss noise; names/counts/positions/coordinates remain exact.
The negative control still warns for genuinely missing off-axis time, and the
existing incompatible-trajectory refusal remains. Clean combined ecf05b066
receives all 187 selected composition/axis/unit cases and fourteen fast gates.
All 102 existing selected warnings remain: 99 legacy H5MSM and three genuine
off-axis diagnostics. No warning category is filtered and no scientific source
loss is claimed or repaired.

Receiving record: [import_and_composition_receiving_674_675_20261109.json](../../../devtools/data/import_and_composition_receiving_674_675_20261109.json).
