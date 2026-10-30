# Receiving the independent ChemicalStates model

**Role:** operational migration guide for the unreleased source cutover in
[MolSysMT #255](https://github.com/uibcdf/molsysmt/issues/255).
The [core specification](CORE_SPECIFICATION.md) owns the model; this page explains
how existing clients receive it. A source checkpoint is not a published dependency
floor or installed-package qualification.

## Moving chemical access

Topology supplies stable atom, group, molecule, entity and chain inventory.
ChemicalStates supplies state-local bonds, assignments and components, even when
both domains belong to the same MolSys. An attached Topology has no chemical
fallback through its owner.

| Previous access | Receiving route |
| --- | --- |
| `molsys.topology.bonds` | `molsys.chemical_states.get_bonds(chemical_state=...)` |
| Topology bond/component counters | Native `molsys.get(...)` or `molsys.chemical_states.get(...)`, with an explicit state when needed. |
| Topology component tables | ChemicalStates component queries through `get(element='component', ...)`. |
| Topology chemical mutation/reconstruction | ChemicalStates `add_bonds`, `remove_bonds`, `rebuild_components` and supported `set` attributes. |
| Nine `msm.topology` chemical-graph tools | The corresponding names under `msm.chemical_states`; see the [accepted migration inventory](pending_proposals/retire_topology_bonds_after_1_0_in_favor_of_chemicalstates.md). |
| Addon graph tools under `view.addons.molsysmt.topology` | `view.addons.molsysmt.chemical_states`; sequence alignment/identity remain under `.topology`. |

Sequence functions and chains remain in topology. Geometric dihedral calculations
remain in structure; chemical dihedral-quartet enumeration belongs to
chemical_states. Physicochemical interpretation, periodic reconstruction and
interaction detection retain their existing domain owners.

Use supported molecular-system extraction, removal and permutation to remap all
present domains together. Do not reorder only a topology table while retaining
unmapped chemistry or coordinates. Stable molecule membership does not follow
later connectivity edits; constructor-time inference is separate from editing an
existing chemical state. Supply stable Topology explicitly when reconstructing
chemical labels requires inventory context.

## Declaring the available domains

Pass a complete MolSys when the calculation needs inventory, chemistry and
coordinates. For independently held domains, an explicit list declares positional
atom correspondence, for example `[topology, chemical_states, structures]`.
ChemicalStatesDict can supply the chemical domain. One coordinate-only source,
such as a DCD file, can replace Structures in an explicit chemical composition;
reader-specific I/O limits still apply. Counts are validated but do not prove
common origin.

Projecting a richer source to pure Topology deliberately removes chemical data.
Converting that pure inventory back to MolSys cannot recover its previous bonds.
Keep the full source or supply ChemicalStates explicitly instead of restoring a
Topology compatibility facade. Read-only providers must borrow already compatible
native domains without rebinding their owners; public conversion retains its
independent-result and copy-policy contracts.

Chemical-only ring, torsion, aromaticity, molecular-descriptor, typing, charge
and CIP queries with numeric or `all` selections omit structural conversion at
the chemistry boundary for foreign molecular forms. Explicit structure indices are still
validated against the original source axis before chemistry is detached. Rich
string selections retain their coordinate-capable route. ChemicalStates, alone
or alongside Structures, also supports predicates over its supplied chemical
attributes without synthesizing stable inventory; unavailable attributes remain
explicit prerequisites.

Geometry consumers retain coordinates. CIP coordinate inference reads its
requested structure separately, and rich selections use the original geometric
context. RDKit conformer counting has a direct adapter route without coordinate
conversion; selected empty structural conversion preserves its atom axis.

An absent chemical domain, a present collection with zero states, an unknown graph
and a declared complete graph with zero bonds are different conditions. A standalone
ChemicalStates starts with no states. Ordinary MolSys/Builder construction retains
its documented unknown staging state. A consumer must check its prerequisite and
must not create a state merely to make a read succeed.

## Resolving state and scope

Use `chemical_state='reference'` only when the source has an unambiguous reference.
Use an integer to choose an existing state explicitly. `chemical_state='structure'`
resolves declared associations for selected structure indices; missing or mixed
associations fail rather than choosing state zero. A standalone list of states and
coordinates does not recover associations from weak owner links.

A component index belongs to one state. A component ID is a label, not a persistent
cross-state identity. Do not align states or components solely by their row numbers.
Current independent union supports one-state inputs; unsupported multi-state merge
policies reject rather than guessing a Cartesian product or correspondence.

Controlled edits preserve other domains and invalidate affected named analyses
according to the [query](native_queries.md), [copy](native_copy.md) and
[interaction](interactions_api.md) contracts. Raw pandas/array writes do not gain
controlled-edit notifications through this migration.

## Receiving serialized data

Latest TopologyDict and MolSysDict writers use schema 0.2. TopologyDict contains
stable inventory only. MolSysDict retains independently optional domains, explicit
associations and named analyses through typed transports. Legacy 0.1 interpretation
is separate; use complete MolSys decoding to retain chemistry actually written there.

The public H5MSM writer remains version 0.5, with independent layers and topology
layer version 3. Existing topology-layer versions remain readable. The legacy
H5MSMFileHandler supports 0.3/0.4, not 0.5: receive a current file as MolSys or use
the documented layer-reading tools. MolecularMechanics persistence remains outside
0.5. Do not claim a new public file-backed interaction/coordinate query API from
private codec benchmarks.

Old mixed-Topology pickles are refused by the new Topology restoration boundary.
Use the writing version to export a complete supported H5MSM representation, then
read/migrate that file with the maintained reader. Pure inventory restoration does
not silently resurrect a hidden chemical domain.

## Qualifying a client

Exercise real queries, geometry, extraction and controlled mutation, including
nonreference/missing states, unknown memberships and explicit empty axes. A text
search or successful import does not prove receiving. Keep original source/index
maps, physical units, provenance and analysis invalidation assertions.

Coordinate with the receiving issues: `uibcdf/molsyssuite#155`,
`uibcdf/molsysviewer#269`, `uibcdf/dockingmt#56`,
`uibcdf/pharmacophoremt#69` and `uibcdf/topomt#100`.
Record exact provider/consumer source identities and dirty state, then qualify
installed artifacts separately when immutable package coordinates exist. Visual
scene reconstruction and sessions remain owned by MolSysViewer.
