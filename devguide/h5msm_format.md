# H5MSM Format Contract

**Status:** normative for writers and readers implemented by MolSysMT.

H5MSM is the versioned native persistence format for complete or partial
molecular systems. New writers emit version 0.4. Readers support versions 0.3
and 0.4 and reject missing, malformed, or unknown versions explicitly.

## Root contract

Every file carries at least:

- `type = "h5msm"`;
- `version`;
- integer and floating-point precision declarations;
- canonical unit declarations;
- creation and modification timestamps.

The root contains `topology` and `structures` groups. Absence of an optional
dataset is different from a present nullable dataset and from a dataset filled
with zero or `False`.

## Version 0.4 topology

`/topology` stores stable atom identity and semantic hierarchy:

- `atoms`: `atom_id`, `atom_name`, `atom_type`, nullable `isotope`, `group_index`, `chain_index`;
- `groups`, `molecules`, `entities`, and `chains` with their stable columns;
- `chemical_states` as an ordered group keyed by contiguous integer strings.

`/topology/chemical_states` declares `n_chemical_states` and a nullable
`reference_chemical_state_index`, encoded as `-1` when absent. Each state owns:

- optional `state_id`;
- connectivity and component completeness;
- component evidence and an optional provenance index;
- atom-aligned `component_indices`;
- a state-local `components` table;
- optional nullable `atom_attributes` columns;
- the full normalized nullable `bonds` table.

Nullable datasets use a sibling `<name>__is_null` Boolean mask only when at
least one value is missing. This preserves a materialized all-null column as
distinct from an absent column. Canonical Pandas extension dtypes are restored
by the reader.

When a reference state exists, `/topology/components`,
`/topology/atoms/component_index`, and endpoint datasets under
`/topology/bonds` are compatibility hard links or projections. They do not
constitute a second physical authority. Version-aware readers must use
`chemical_states` for nullable and rich chemical semantics.

## Structure-to-state association

Version 0.4 stores `/structures/chemical_state_index` as an atom-independent
integer vector aligned with stored structures. MolSysMT writers populate it
from the authoritative `MolSys` association, use implicit zero for a topology
with exactly one state, and encode missing multi-state associations as `-1`.
The global reference state is never repeated as if it were per-structure
evidence. Readers restore the vector on `MolSys`, not on `Structures`; the
public `structure_chemical_state_index` attribute exposes resolved values.

## Version 0.3 migration

Version 0.3 remains read-only compatibility input for new scientific output.
Its legacy bonds, components, and atom component indices become one reference
chemical state. Connectivity is marked complete, component completeness is
derived from missing membership, and component evidence is `unknown` because
0.3 did not preserve source evidence. This is an explicit migration assumption,
not a claim that the source format recorded that evidence.

Legacy 0.3 extraction may retain a 0.3 output layout so large trajectories can
be subset without materializing all coordinates. Any normal new conversion or
write emits 0.4.

## Required validation

Changes to H5MSM require tests for:

- 0.3 migration and unknown-version rejection;
- empty, single-state, and multi-state topology;
- missing reference states;
- absent, partially null, all-null, zero, and `False` values;
- rich bond metadata and non-unique string IDs;
- atom extraction with state-local endpoint and component remapping;
- structural round trips and structure-to-state alignment;
- direct file getters that expose a compatibility projection.

Current bundled demos use H5MSM 0.4 and are validated against
`molsysmt/data/demo_manifest.json`. One immutable 0.3 alanine-dipeptide fixture
is isolated under `tests/form/file_h5msm/data/` for read-compatibility tests.
Regenerating a file is not itself validation.
