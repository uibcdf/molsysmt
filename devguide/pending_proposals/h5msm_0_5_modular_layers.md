# H5MSM 0.5 Modular Layer Contract

**Status:** accepted pre-1.0 design target; explicit 0.5 API and public
`convert` writing implemented, full form integration and final schema gates pending

**Target:** before MolSysMT 1.0 candidate freeze

**Related contract:** [Native Structures Contract](../native_structures_contract.md)

**Interaction-layer boundary:** H5MSM 0.5 is now the pre-1.0 target for
`molsysmt.Interactions` persistence under `uibcdf/molsysmt#251` and
`uibcdf/molsysmt#252`. The 0.4.1 extension candidate is withdrawn. Version
0.5 must also separate chemical states from topology at the file root, as
proposed below. The native decision is now tracked by
`uibcdf/molsysmt#254`: `ChemicalStates` owns the state records, and
`Topology` retains compatibility access to the selected state. The native
migration is underway. Public `molsysmt.convert` now writes 0.5 and reads it
through the native 0.5 codec. The legacy file-form adapters still serve 0.3/0.4;
the explicit `molsysmt.h5msm` API also writes and reads versioned 0.5 layers.

**Attachment responsibility, 2026-09-29:** The accepted pre-1.0
[interaction attachment policy](../interactions_api.md#associating-analyses-with-a-system)
uses declared correspondence. The writer owns the scientific correspondence
of layers; the reader validates their explicit associations. Attaching an
analysis from another file is a caller declaration after any necessary axis
alignment. Optional provenance labels and source maps are not authenticated
cross-file identity. Automatic origin verification is future work rather
than a requirement for the 0.5 format or MolSysViewer 1.0 integration.

**Producer provenance, 2026-09-29:** Named analyses now store optional
`software` metadata mapping software names to calculation-time versions.
Buch and disulfide adapters capture the MolSysMT version; public conversion
and layer reading preserve it regardless of the installed writer/reader.
Old analysis payloads without the field remain unknown (`{}`). The guard
`tests/interactions/test_software_provenance.py` covers historical versions,
empty evaluated frames, dictionaries, views, remapping, invalidation, and
standalone as well as H5MSM persistence. MolSysViewer accepts the declared
correspondence policy after reviewing `2e79b5f29`; canvas and saved-session
integration tests remain pending on the client side.

## Motivation

MolSysMT deliberately accepts molecular-system forms with partial information.
A sequence may have no coordinates, a trajectory may have no topology, and a
chemical-state representation need not carry a complete stable topology.
H5MSM must preserve that philosophy instead of requiring artificial empty
objects merely to satisfy one fixed hierarchy.

The current H5MSM 0.4 organization couples chemical states too closely to
topology and can make an absent layer indistinguishable from an automatically
created empty scaffold. Extending that organization incrementally would make
readers infer semantics from storage accidents.

## Required Capability

The format must support every non-empty combination of the three principal
native information layers. Interactions are a fourth optional domain, with
explicit atom and structure index spaces even when another layer is absent:

| Topology | Chemical states | Structures | Valid use |
| --- | --- | --- | --- |
| present | absent | absent | stable inventory and hierarchy only |
| absent | present | absent | chemical-state information only |
| absent | absent | present | topology-free trajectory or observations |
| present | present | absent | stable inventory plus chemical states |
| present | absent | present | classical fixed-topology trajectory |
| absent | present | present | chemical-state trajectory without a full stable topology |
| present | present | present | complete molecular-system representation |

An entirely empty container may be technically readable for tooling, but it is
not a meaningful molecular-system payload and need not be a normal write
target.

## Proposed Root Layout

H5MSM 0.5 should store four optional domain groups and one optional metadata
group for declared associations:

```text
/
├── topology/          # optional
├── chemical_states/   # optional
├── structures/        # optional
├── interactions/      # optional; versioned sparse analyses
└── associations/      # optional; explicit cross-layer index links
```

No layer is a prerequisite for another. An interaction analysis must declare
its atom and structure index spaces even when topology or structures are
absent. Cross-layer associations are explicit datasets or references, not
implied by nesting.

Examples include:

- a structure-to-chemical-state association when both layers exist;
- a chemical-state atom-domain reference when topology exists;
- an explicit local atom domain when a chemical state exists without topology.

The exact reference encoding remains undecided until append, slicing, and
partial-read behavior have been tested. This proposal fixes the semantic
contract, not the complete low-level HDF5 encoding.

The experimental `Interactions` result has a private, versioned HDF5 group
codec that preserves one complete analysis. A private collection codec stores
named analyses under numeric group keys, preserving arbitrary names in
attributes. These are candidate building blocks for `/interactions`, but do
not settle independent layer presence, selective reading, or the root 0.5
schema.

An isolated interaction-only 0.5 probe now writes `/interactions` under a
root with `type=h5msm` and `version=0.5`. `None` leaves the layer absent;
an empty mapping creates a present-empty layer. Tests cover multiple fields,
unknown collection schema, and the current 0.3/0.4 handler's explicit
rejection of 0.5. This private probe is not registered as a MolSysMT file
form and does not claim that H5MSM 0.5 is implemented. It supplies a concrete
file fixture for deciding the remaining four-layer schema and migration.

A second private probe now writes `/chemical_states` independently of
`/topology`. It reuses the record encoding of H5MSM 0.4, adds a layer schema
version and explicit local `n_atoms`, and preserves absent, present-empty,
and present-with-data cases. Tests cover multiple states, nullable columns,
and absent reference state. The H5MSM 0.4 writer still creates its historical
compatibility links inside `/topology`, and its regression tests pass. This
probe does not settle cross-layer atom mapping, associations with structures,
selective reads, or public 0.5 file conversion.

A third private probe writes numeric `/structures` series without a topology
group. It records frame cardinality and either a known atom cardinality or
`-1` for a frame-only series whose atom domain is unknown. It writes by frame
blocks and reads explicit, nonconsecutive frame selections without scanning
unselected rows; repeated requested frame indices preserve their requested
order. Atom selections read only requested atom columns and preserve their
order. It distinguishes an
absent group from a present-empty group and initially rejected unsupported
`alternate_location` and `bioassembly` before writing. The 0.4 reader still
requires coordinates, so this probe must not be confused with public 0.5
support. A private topology-free file probe now appends complete frame rows
to resizable datasets in blocks, with or without a chemical-state layer. It
preserves atom-axis associations and extends one declared
structure-to-chemical-state link when the caller supplies a state index for
each new frame. The link accepts `-1` for unknown state, and an existing
identity mapping becomes explicit when later frames reuse a state. It validates
the atom axis, series inventory,
stored shapes, dtypes, units, and resizability before resizing, preserves
constant-step metadata only when the joined values support it, and reads
nonconsecutive selections after append. Tests cover an initially empty series,
a frame-only series with unknown atom cardinality, and rejected appends that
leave the stored frame count unchanged. Append involving topology, interactions,
or other structure-axis associations, remapping bioassemblies during atom
subset extraction,
and large-trajectory performance measurements remain acceptance work. A write
failure during a multi-dataset append is not yet transactional; this private
probe does not claim crash-safe append.

A fourth private probe writes the stable `/topology` tables as typed columns
with explicit null masks. It stores atoms, groups, molecules, entities, and
chains, without components or covalent bonds. A topology-only round trip
therefore restores zero chemical states; a sibling `/chemical_states` group
can carry bonds once, independently. This is still a schema probe: it does
not yet implement cross-layer associations, atom selections, or a public
0.5 `MolSys` round trip. The table layout and HDF5 metadata overhead need
measurement before stabilization.

One combined fixture now writes all four sibling layers in one 0.5 file and
reads them independently. It confirms that the stable topology contains no
second bond record, the chemical-state layer owns the covalent bond, and an
interaction result retains evaluated-empty and observed frames. The fixture
does not yet declare or validate cross-layer index associations, so it is
evidence for layer separation only, not a complete `MolSys` round trip.

A private modular-file probe now accepts explicit axis links in the optional
`/associations` metadata group. Each link names its source and target layer
(and analysis name for an interaction endpoint), its axis kind, and a
source-to-target index mapping. Atom and structure axes use their own link
kinds; a separate structure-to-chemical-state link records per-frame state
assignment. Equal cardinalities never create an implicit link. Identity
links require equal axis lengths and use only a scalar encoding; reordered,
partial, and unresolved mappings use an integer vector with `-1` for an
unknown counterpart. Validation rejects absent axes, out-of-range targets,
duplicate atom targets, duplicate link endpoints, and contradictions between
direct and two-step paths before creating a file. The reader revalidates the
stored links. This is a candidate encoding, not a stabilized public schema;
selection remapping, append semantics, and native `MolSys` ownership remain
open.

The modular reader and writer round-trip each of the seven non-empty
combinations of topology, chemical states, and structures. Public `read`,
`write`, and registered H5MSM 0.5 conversion routes reconstruct supported
partial native `MolSys` objects. A named interaction-only payload also
reconstructs as a partial `MolSys`; its analyses declare the atom and
structure index domains. A state-only payload preserves absent topology and
structures through copy and pickle, including zero versus one empty chemical
state. Further optional-layer combinations and file-backed selective reads
remain separate work.

A second private native probe round-trips chemical states, structures, and
named interaction analyses with no topology. It requires explicit identity
links for every shared atom or structure axis and preserves a nullable
structure-to-state map. Files with reordered or undeclared links remain
readable as modular domain payloads, but are rejected as one native `MolSys`
until remapping is implemented. A present-empty interaction layer is also
rejected by this native reader because its current mapping cannot retain the
distinction from an absent layer. A frame-only structural series has no atom
axis to link, even when chemical states declare their own atom cardinality.

Private native probes now also round-trip topology only, structures only,
topology plus structures, and topology plus chemical states. Together with
the state-only, topology-free chemistry-and-structures, and complete-system
probes, all seven primary layer-presence combinations have a native
round-trip test. Absent chemistry remains `MolSys.chemical_states is None`
through copy and pickle; it is not replaced with an empty collection. A
frame-only structures payload retains an unknown atom count instead of
reporting zero atoms. These are still constrained probes: the combined
reader requires declared identity links, and the public file form has not
been switched to 0.5.

A strict private complete-`MolSys` probe now writes all three principal
domains plus attached interaction analyses and reconstructs their single
chemical-state authority. It declares identity links for the shared atom
axes and for each interaction analysis's structure axis, and writes an
explicit nullable structure-to-state mapping when one exists. The reader
requires those links and rejects reordered axes until a lossless native
remapping route exists. The initial writer rejected nonempty molecular-mechanics
data, alternate locations, and bioassembly before file creation. This round trip was an integration fixture,
not a public `file:h5msm` conversion or evidence that all MolSys information
domains are serializable in 0.5.

The modular reader also accepts a set of requested layers and leaves
omitted payloads unloaded. Association validation obtains axis sizes from
group metadata, so a request for interactions and associations does not load
the topology or coordinates. Named interaction analyses can also be selected
without deserializing the other analyses in the collection. A private
file-backed reader now selects explicit frames through a per-frame offset
index and filters their relations by atom and interaction type. The reader
preserves evaluated-empty coverage and supports nonconsecutive frame lists.
It still scans requested frames' occurrences for atom queries; an on-disk
inverse atom index and bounded-memory large-trajectory evidence remain open.
The [H5MSM benchmark guide](../benchmarking/h5msm.md) records this probe and
its limits. The explicit `molsysmt.h5msm` API now exposes versioned read,
write, layer selection, and topology-free append paths, while the registered
legacy `file:h5msm` adapter operations still handle only the 0.3/0.4 layout.
Public `convert(..., to_form="file:h5msm")` writes 0.5 and can read a 0.5 file
through the native 0.5 codec. A separate
`migrate_to_05` helper reads a nonempty 0.3 or 0.4 system through the existing
native converter, writes 0.5, and records its source version. Legacy reads
emit `LegacyH5MSMWarning` with the migration function named in the message.
The structures layer now encodes biological assemblies as typed chain-index,
rotation, and translation datasets. A unit-bearing translation is converted to
nanometers; reading rejects a missing or inconsistent unit. The public
`convert` path round-trips the bundled TcTIM BinaryCIF system with its
bioassembly and B factors. Sparse alternate-location records now preserve
per-frame atom keys, multiple sites, optional fields, and physical units;
the bundled PDB with alternate locations round-trips through public 0.5
conversion. String and integer structure IDs retain their types. Sparse
alternate-location columns now append with structural rows when both blocks
declare them; incompatible presence or stored units reject before resizing.
Nonempty molecular mechanics still rejects before output creation.
Appending structures preserves a stored biological assembly and accepts
incoming assembly metadata only when it matches the stored operations after
unit normalization. A structures-only atom subset with an assembly now raises
instead of returning chain indices from the original atom domain. Public
`convert` also rejects writing a selected atom subset that still carries an
unremapped assembly, before creating the output file.
The helper rejects a zero-atom legacy scaffold because its optional-layer presence is
ambiguous. Remaining 0.5 form operations, complete field fidelity, and
large-trajectory validation remain open.
The public native route also round-trips a partial `MolSys` with structures
and named interactions but no chemical states, both with and without topology.
It requires explicit identity associations for every shared interaction axis.
An interaction-only file with named analyses is readable through `read` as a
partial native `MolSys` and through `read_layers` as independent results.
Native extraction uses the analyses' declared atom and structure index axes.
A present-empty interaction layer remains available through `read_layers`.

## Molecular-Mechanics Version Boundary

H5MSM 0.5 does not define a `molecular_mechanics` layer. The current native
`MolecularMechanics` object is minimal and experimental before MolSysMT 1.0;
its parameterization contract is not mature enough to freeze in this schema.
Persisting that domain is deferred to H5MSM 0.6, after MolSysMT 1.0. It is
not an acceptance condition for the 0.5 release or the 1.0 candidate.
The later design is tracked separately in the
[H5MSM 0.6 mechanics proposal](h5msm_0_6_molecular_mechanics_persistence.md)
(`uibcdf/molsysmt#256`).

The 0.5 writer must reject nonempty mechanics data before creating a file,
including through public `convert` and migration routes. An empty native
mechanics default does not imply that the file contains a mechanics layer.
The 0.6 design must first settle the parameter model, physical units,
atom-axis associations, and how absent versus present mechanics data are
represented; 0.5 makes no promise about their eventual encoding.

## Presence Semantics

Readers and writers must distinguish three states for every principal layer:

1. **Absent:** the root group does not exist and the file makes no claim about
   that information domain.
2. **Present but empty:** the group exists intentionally, carries its schema
   metadata, and contains a valid zero-length representation.
3. **Present with data:** the group exists and contains one or more domain
   records.

An absent layer must not be materialized as an empty native object merely for
convenience. Conversely, a deliberately empty layer must not be reported as
absent.

`has_attribute()` and conversion-fidelity reports should answer from semantic
payload presence, not from the existence of scaffolding created by a reader.

## Minimal Independent Domains

### Topology

Topology owns stable atom inventory, grouping and hierarchy. It must not need
coordinates or chemical-state payloads.

### Chemical states

A chemical-state-only file needs enough information to define the domain to
which its state data apply. This may be a minimal local atom domain such as an
atom count and stable local indices. It must not require inventing atom names,
groups, molecules, or other topology.

When topology is also present, the state layer should reference its atom
domain explicitly and validate compatible cardinality.

### Structures

A structures-only file may contain any valid complete-axis combination of
coordinates, velocities, box, time, thermodynamic series, B factors,
occupancies, alternate locations, and structure identifiers. It must not
require topology.

Atom-aligned structural arrays define their own atom-axis cardinality. Files
with only non-atom-aligned structural series are valid and may have unknown
atom cardinality.

### Interactions

The optional interaction layer contains named analyses with typed sparse
relations, participants, structure-specific occurrences, explicit evaluated
coverage, source-index maps, method parameters, evidence, measures and units,
and periodic images when relevant. It must not materialize dense atom-pair
matrices or one Python object per occurrence. Its payload schema is versioned
within H5MSM 0.5 so later interaction codecs can evolve without silently
changing the root format's meaning.

Each analysis declares its own source atom and structure axes. When topology
or structures are also present, their correspondence is explicit and
validated. An interaction-only file is valid if those local axes and method
provenance are sufficient to interpret its results. Absent interaction data
means no analysis is claimed; a present analysis with evaluated frames and
zero occurrences means the analysis ran and found none.

## Association Rules

- With one chemical state and no explicit per-structure association, all
  structures are associated with that state.
- With multiple chemical states, an association dataset is required whenever
  structures are claimed to have resolved states.
- Missing association information means unavailable information; it must not
  be replaced by a fabricated state.
- Topology and structures may coexist without a chemical-state layer. This is
  the normal compact representation for many classical trajectories.
- Layer cardinalities are validated only where a semantic relationship is
  declared. The mere coexistence of layers must not create an undocumented
  inference.

## H5MSM 0.4 Compatibility and Migration

The 0.4 reader remains valid for legacy files. The modular layout is
introduced as a versioned 0.5 schema before MolSysMT 1.0, not as an ambiguous
reinterpretation of existing 0.4 files. Older readers reject 0.5 explicitly;
new readers support both versions.

A 0.4-to-0.5 migrator should:

1. detect which 0.4 groups contain semantic payload rather than scaffolding;
2. promote topology, chemical states, and structures into sibling 0.5 groups;
3. reconstruct only associations demonstrated by 0.4 data;
4. preserve absence instead of manufacturing empty layers;
5. report any ambiguous inference through the conversion-fidelity machinery.

The 0.5 reader may expose a common MolSysMT object model for both versions, but
must retain the source schema version in provenance.

## Acceptance Criteria

The design is ready for implementation only when the H5MSM and MolSysMT sides
agree on:

- the schema and ownership of all four optional root layers;
- the interaction layer's relation to
  each available atom and structure axis;
- the encoding of cross-layer references and local atom domains;
- absent versus present-empty semantics;
- append behavior for files that do not contain all layers;
- selection and partial-read behavior;
- conversion-fidelity and strict-mode reporting;
- 0.4 migration and compatibility policy.

Implementation evidence must include:

1. one round trip for each of the seven valid layer combinations;
2. explicit absent/present-empty/present-data tests for every layer;
3. topology-free structural append and slicing;
4. chemical-state-only storage with a minimal atom domain;
5. single-state implicit and multi-state explicit structure associations;
6. cross-layer cardinality rejection without partial file mutation;
7. 0.4-to-0.5 migration fixtures;
8. lazy or selective reads proving that omitted layers are not loaded or
   synthesized.
9. interaction-only, interaction-plus-structures, and complete-system round
   trips, including evaluated-empty coverage, multiple analyses, source
   remapping, and periodic images;
10. bounded-memory write, read, and subset extraction for a large trajectory
    carrying interactions.

The MolSysViewer consultation for `uibcdf/molsysviewer#114` must review the
interaction result and the public H5MSM 0.5 route together. Present the same
named analyses and queries in memory and after H5MSM loading, including
absent/present-empty layers, source-index maps, and invalidated structures.
Ask whether `read_layers` meets the viewer's memory and latency needs or a
public file-backed query is required, and obtain representative trajectory
sizes and access patterns. The detailed questions and review packet are in
[the Interactions design proposal](design_a_sparse_public_interactions_result_and_serialization_contract.md#molsysviewer-review-gate-before-client-implementation).
The viewer's feedback is consumer acceptance for its pre-1.0 integration;
MolSysMT remains responsible for the H5MSM schema and its other acceptance
criteria.

## Non-Goals

- persisting `MolecularMechanics` in H5MSM 0.5; that domain is reserved for a
  separately designed H5MSM 0.6 after MolSysMT 1.0;
- implementing per-structure missing-value masks for partially sampled
  observables; that is a related but independent decision;
- forcing every MolSysMT form to expose all three layers;
- inferring a chemically rich topology from coordinates alone;
- silently changing the meaning of an existing H5MSM 0.4 file.

## Recommended Scheduling

Deliver the H5MSM 0.5 modular layout, including chemical states and the
interaction layer, before the MolSysMT 1.0 candidate freeze. Preserve 0.3/0.4
read compatibility and establish selective 0.5 reads and writes before
claiming the large-trajectory gate. Complete the native `ChemicalStates`
ownership migration before treating the four-layer file round trips as
complete.
