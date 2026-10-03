# H5MSM Format Contract

**Status:** normative for writers and readers implemented by MolSysMT.

H5MSM is the versioned native persistence format for complete or partial
molecular systems. Public conversion and h5msm writers emit version 0.5. Readers support versions
0.3, 0.4 and 0.5, with deprecation warnings for legacy input. Unknown versions
are rejected explicitly. The legacy codec details below describe 0.3/0.4; the
public modular layout is documented in
[H5MSM 0.5](../docs/content/user/tools/form/file/h5msm_05.md).

## Root contract

Every file carries at least:

- `type = "h5msm"`;
- `version`;
- integer and floating-point precision declarations;
- canonical unit declarations;
- creation and modification timestamps.

Legacy roots contain `topology` and `structures` groups. Modular 0.5 layers
`topology`, `chemical_states`, `structures` and named `interactions` are optional,
with explicit associations; MolecularMechanics is outside 0.5. Absence of an optional
dataset is different from a present nullable dataset and from a dataset filled
with zero or `False`.

## Version 0.5 interaction metadata

Named analyses are optional and may accompany structures, chemistry, topology,
or stand alone with declared atom and structure index domains. Public conversion
preserves typed sparse relations, occurrence order, evaluated-empty coverage,
search scope, source maps, units, evidence and periodic images. The full contract
is [Interaction Analysis API](interactions_api.md); the existing interaction
codec schema is independent of the H5MSM root version.

Each analysis stores producer `software` versions once in metadata. Interaction
codec 2 also stores frame-scoped execution records separately from scientific
parameters; codec-1 input is migrated on reading. The H5MSM root remains 0.5. Scientific
selectors, profiles, definition labels and detached bibliography are ordinary
versioned analysis parameters. The optional `parameters["attribution"]` payload
uses `molsysmt.scientific_attribution@1`; it adds no per-occurrence columns and
requires no new H5MSM root version. A loader preserves original producer
versions and references without reporting a new calculation. Missing historical
attribution stays absent, and missing producer versions stay unknown.
Guards are `tests/interactions/test_scientific_attribution.py` and
`tests/interactions/test_software_provenance.py`.

Recorded covalent bonds are owned by the sibling `chemical_states` layer.
Disulfide and metal-coordination observations must not replace that authority.
`Topology.bonds` is a native compatibility facade, not a second file-layer store.
H5MSM 0.5 excludes `MolecularMechanics`; nonempty mechanics data are rejected
rather than silently lost. Mechanics persistence belongs to 0.6 after 1.0.

### Native composition without Structures

A native system containing topology, chemical states and named analyses can be
serialized without a Structures layer. It requires a declared identity atom link
from chemical states to topology and from each analysis to topology. When multiple
analyses are present, identity structure links must connect all their named axes.
The writer emits a star rooted at the first sorted analysis name; the reader
accepts any connected identity graph. One analysis needs no inter-analysis link.
Equal cardinalities or matching source labels do not replace these declarations.

The reader rejects missing, nonidentity or unrepresentable associations rather
than composing ambiguous axes. Independent layer reading still preserves such
domains. No coordinates, periodic boxes or structure-to-state association are
created. Analyses retain their declared search scope, coverage (including evaluated
empty frames), sparse observations, periodic images and original producer versions.
Complete-axis scope may be normalized to its compact implicit representation by
native remapping; the public `evaluation_scope` remains equivalent. A named empty
analysis is supported, including a zero-length structure axis. A present-empty
interaction layer remains distinguishable through `read_layers` and is rejected
by native composition. Guard:
`tests/form/file_h5msm/test_topology_chemistry_interactions_v05.py`.

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
be subset without materializing all coordinates. Public new conversion and writes emit 0.5. The explicit legacy codec retains
its 0.4 layout for legacy operations.

## Extraction safety

Extracting an atom or structure subset from a `file:h5msm` input requires an
explicit output filename that identifies a different file. Omitting the
destination or naming the input through an equivalent path or hard link raises
`ArgumentError` before any HDF5 file is opened for writing. An unrestricted
extraction without a destination returns the original path unchanged. Callers
that want an in-memory subset may request `to_form='molsysmt.MolSys'`.

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

## Declared hydrogen annotations

The registered optional atom-state field `n_explicit_hydrogens` uses nullable UInt8
semantics and the ordinary sibling null mask. It stores atom-level declarations
such as RDKit `[NH2+]`, not indexed bonded H atoms or implicit hydrogens. The current
chemical codec preserves it in 0.4/0.5; absent historical fields remain unknown.
Readers predating the column may reject files containing it. Source atom/structure
axes never grow merely to preserve this annotation. Guard:
`tests/form/rdkit_Mol/test_declared_hydrogen_round_trip.py`.
