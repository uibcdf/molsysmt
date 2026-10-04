(user-foundations-native-world-classes-molsysmt-molsys)=
# MolSys

`molsysmt.MolSys` is the primary native molecular system container in MolSysMT. It can combine topology, chemical states, a 3D structures sequence or ensemble, named interaction results, and molecular mechanics data.

---

## Overview and Role

As a user, `molsysmt.MolSys` is the central object returned when loading, converting, or processing molecular systems. By composing dedicated sub-containers, `MolSys` ensures strict separation of concerns while providing a unified gateway for selections, spatial queries, and form transformations.

Some native operations edit a `MolSys` in place; `extract` returns an independent subset. A partial `MolSys` retains only the information domains that were available in its source.

If you hold chemical states and structures separately, use
`msm.convert([chemical_states, structures], to_form='molsysmt.MolSys')`.
The chemistry may also be a `ChemicalStatesDict`. The pair declares matching
atom-index correspondence and produces a topology-free system; index selections
remap both domains together. The reference state is preserved, but several
states are not automatically assigned to structures. See {ref}`Tutorial_Convert`.

---

## Internal Attributes

The native container exposes these domains:

| Attribute | Internal Object Class | Description |
| :--- | :--- | :--- |
| **`topology`** | `molsysmt.Topology` | Topological graph containing atom, residue, group, component, molecule, and chain inventories. |
| **`structures`** | `molsysmt.Structures` | Structural container holding 3D coordinates `(n_structures, n_atoms, 3)`, periodic box matrices `(n_structures, 3, 3)`, and structure timestamps. |
| **`chemical_states`** | `molsysmt.ChemicalStates` | State-dependent covalent bonds and atom-level chemical assignments. |
| **`interactions`** | Named `molsysmt.Interactions` results | Sparse observations with declared atom and structure index domains. |
| **`molecular_mechanics`** | `molsysmt.MolecularMechanics` | Forcefield parameters, partial charges, atom masses, and non-bonded interaction rules. |

An H5MSM 0.5 file may load as a partial `MolSys` without topology. If it
contains only named interactions, those results supply the atom and structure
index domains. `extract(atom_indices=[...], structure_indices=[...])` remaps
the present domains and keeps the selected structure order. An axis with no
declared domain cannot be selected explicitly.

A system with topology and chemical states can also select atoms while
`structures is None`; extraction keeps the coordinates absent and remaps the
available chemistry. With topology, atom subsets use sorted source indices.
Without a Structures domain, named analyses may still declare a structure-index
domain; otherwise an explicit structure selection raises `ValueError`.
Public H5MSM 0.5 reads and writes preserve this combination, including several
named analyses and evaluated structures without observations. The stored axis
associations declare correspondence; they do not supply missing coordinates,
periodic boxes or per-structure chemical-state assignments. See
{ref}`H5MSM 0.5 <user-tools-form-h5msm-05>`.
Complementary partial systems or matching H5MSM 0.5 files can be consolidated
with `msm.convert([molsys_A, molsys_B])` before selecting atoms/structures.
The list declares positional correspondence; each native domain has one provider
and analysis names are distinct. Full-axis conflicts fail before extraction.
Topology is copied to preserve its input owner's binding, while full-axis
`copy_if_all=False` can share structural arrays. See {ref}`Tutorial_Convert`.

Both hydrogen-bond detectors and the disulfide candidate detector can return an
independent `molsysmt.Interactions` analysis with
`output_type="molsysmt.Interactions"`. Attach it under a name by assigning
`molsys.interactions = {**molsys.interactions, "analysis_name": analysis}`.
This retains previous named results and checks that all analyses match the
system's atom and structure axes.

An analysis owns sparse relations and occurrences. A query retains selected row
indices and shares the analysis's numeric storage. Its experimental `to_page()`
projection copies a bounded set of observations and their referenced participant
definitions; it preserves complete-analysis occurrence indices. Coverage and
source maps remain shared read-only data. Query indexes, structure metadata and page
copies have distinct memory costs. See
{ref}`Inspecting bounded pages <user-tools-interactions-pages>`.

This assignment declares that the analysis's local atom and structure indices
correspond to the system. MolSysMT checks compatible axes and valid results;
you are responsible for the correspondence of independently loaded data.
Source labels and maps retain provenance without authenticating that origin.
Chemical recognition and geometric criteria are separate parts of an analysis.
Named hydrogen-bond, π–π, cation–π, halogen and hydrophobic profiles carry
their pinned method references;
a geometric profile on declared participants need not reproduce the reference
package's feature discovery. Different definitions remain separate named analyses.
The method reference describes the reproduced definition, while the producer
describes the software that actually generated these observations.
Each analysis's `software` dictionary records its producer versions; saving
or loading the system preserves those versions rather than substituting
the version installed by the reader. An empty dictionary means unknown.
Detector-produced analyses also keep bibliographic records and contextual
roles in `analysis.parameters["attribution"]`, once per named analysis.
These records accompany the system through H5MSM and extraction. Optional
Ackredit sessions collect references from completed calculations; opening a
saved system does not claim those calculations were performed again.
Optional attribution failures preserve completed science under strict warning
filters. Failed diagnostic delivery uses a fallback log with its code, operation
and both error reasons; it does not change the scientific exception policy.
Method names identify authors or criteria, and profiles identify the reproduced
recognition/geometry conventions. See
{ref}`Methods and attribution <user-tools-interactions-attribution>`.
See
{doc}`the interaction result guide <../../../tools/interactions/result>`
for participant roles, evaluated coverage, and experimental detector limits.

---

## Charge Interpretation

Formal charges describe a selected chemical state. Force-field partial charges
are molecular mechanics parameters. Residue descriptors or protonation assumptions
are named interpretations and do not replace either stored source automatically.

The experimental {func}`molsysmt.physchem.get_partial_charges` calculates an
explicit Gasteiger-Marsili or named force-field model on the full chemical graph.
{func}`molsysmt.build.assign_partial_charges` attaches one validated single-state
assignment to a detached MolSys, preserving source atoms, IDs, coordinates and
analyses. Native mechanical values use elementary charge; provenance records
original producer versions and projected source indices. PDBQT checks stored
assignment consistency and records a bounded summary before export rounding.
These mechanical values and reports are excluded from H5MSM 0.5. See
{ref}`Tutorial_Partial_Charge_Assignment` and {ref}`cookbook-assigning-partial-charges`.
Manual native writes through `msm.set(..., partial_charge=...)` accept finite
vectors or charge quantities, preserve formal charges and retain missing values
for unassigned atoms. Setter values follow an explicit index selection's order.

The experimental {func}`molsysmt.physchem.get_charge_centers` tool produces
sparse chemical features for one state, with whole-center atom membership,
distance-reference atoms, unitful charges, original input indices and evidence.
A molecule of zero net charge can contain separate local charged centers.
Those features precede geometric detection and are distinct from the occurrence
analyses stored in `interactions`.

The experimental `msm.interactions.ionic.get_ionic_interactions()` calculation
uses those features and an explicit geometric cutoff to produce an analysis.
You attach it under a chosen name by assigning
`molsys.interactions = {**molsys.interactions, 'ionic': analysis}`. It records
geometric proximity between opposite formal-charge centers, not an interaction
energy or a recorded bond. See {ref}`Tutorial_Get_ionic_interactions`.

The experimental `msm.interactions.pi_pi.get_pi_pi_interactions()` calculation
uses declared aromatic ring chemistry and least-squares planes. Explicit cutoffs
define parallel or edge-to-face observations; planarity alone does not establish
aromaticity. It returns another independently named analysis, with the same
source-index, coverage, producer-version and persistence contracts. Store both
families in `molsys.interactions` under different names. See
{ref}`Tutorial_Get_pi_pi_interactions` and {ref}`Cookbook_Saving_pi_pi_interactions`.

---

The cation–π detector defaults to the attributed ProLIF 2.2.2 definition and returns
another named analysis. Its original method reference is separate from the producing
MolSysMT/RDKit versions. The custom centroid/angle/offset proposal has a different
participant and geometric definition; no scientific superiority is established.
See {ref}`Tutorial_Get_cation_pi_interactions` and
{ref}`Cookbook_Saving_cation_pi_interactions`.

The experimental halogen detector adds an independent named analysis with four
roles: donor, halogen, acceptor and acceptor reference. Every eligible reference
neighbor remains identifiable. Chemical recognition can be inspected separately
through the general site tool. See {ref}`Tutorial_Get_halogen_bond_sites`,
{ref}`Tutorial_Get_halogen_bonds` and {ref}`Cookbook_Saving_halogen_bonds`.

Hydrophobic observations use a separately named atomic chemical interpretation
and a distance criterion. Their two roles identify canonical source-index order,
not ligand and protein sides. They are distinct from residue hydrophobicity
values or interaction energies. You can calculate a disjoint interface, attach
under a name and preserve its original scope and references in H5MSM 0.5. See
{ref}`Tutorial_Get_hydrophobic_sites`, {ref}`Tutorial_Get_hydrophobic_interactions`
and {ref}`Cookbook_Saving_hydrophobic_interactions`.

ChemicalStates distinguishes implicit hydrogen counts, bracket-declared atom-level
explicit hydrogen counts (`n_explicit_hydrogens`), and real indexed H atoms. Native
and H5MSM round trips preserve the annotations without adding coordinate rows.

{ref}`Explicit template preparation <Tutorial_Chemical_Templates>` can fill missing
assignments in a selected state. With explicit `complete_from_template` policy,
it can also add missing declared covalent edges to an incomplete graph. Components
are then rebuilt in that state, with new indices/IDs and unknown names/types;
stable atom order, group/molecule inventory, other states and structures stay
intact. This returns an independent MolSys, invalidates its named interaction
observations when chemistry changes, and supplies a detached bond-index map.
The original system remains unchanged. Template transfer does not select
protonation, create missing atoms or supply hydrogen coordinates.

The {ref}`peptide-template factory <Tutorial_Get_Peptide_Chemical_Template>` builds
a separate reference MolSys with explicit residue/terminal/link chemistry and
stored H counts. Its synthetic indices/IDs do not identify atoms in an observed
system. A caller-declared map establishes that correspondence before template
transfer. The reference has no coordinates or specified stereochemistry; it is
not a modeled pose or an independently certified biological chain.

The {ref}`aromatic normalization tool <Tutorial_Normalize_Aromatic_Bond_Orders>`
can canonicalize already declared aromatic bond orders on a copy, preserving
connectivity completeness and all atom assignments. It does not perceive
aromaticity. Retain its original-order report separately from H5MSM chemical
values; changing the representation invalidates named interactions on the copy.

The explicit {ref}`fixed-state H operation <Tutorial_Fixed_State_Hydrogens>`
can materialize those counts on a prepared isolated component. Declared aromatic bonds may
use fractional order 1.5 without an integer order; nonaromatic bonds still need
supported integer orders. The operation preserves the original atom indices,
pose and aromatic state on its returned copy.

## Evidence Updates

Editing coordinates or periodic boxes with `msm.set(molsys, ...)` removes
observations and evaluated coverage for the selected structures in every named
analysis. Even a previously evaluated structure with zero observations becomes
unevaluated after its geometry changes. Other structures and previously held
result/query snapshots remain intact. Recalculate the changed structures before
claiming new observations or evaluated-empty coverage.

Empty atom/structure selections and identifier/time changes do not
invalidate analyses. With attached results, full geometry assignment preserves
the structure axis; use extraction or append operations to change that axis.
Invalidation shares read-only observation columns and changes structure validity
without duplicating the surviving observations. Complete-column access,
remapping or export may materialize active columns later. After recalculating
selected structures on the original axes and scope, use
`current.replace_structures(fresh)` and attach its result under the same name.
Compatible recalculations may use different coordinate block sizes or execution
policies. Each analysis keeps their structure membership and details in
`execution_records`, including evaluated-empty structures; scientific parameters,
producer versions and atom scope must still agree. Saving the full system in
H5MSM writes these analyses from their active blocks without packing all their
observations. Remapping or typed dictionary conversion can still materialize them.
To release retired observation blocks after repeated edits, explicitly attach
`current.compact()` under the same name and release old analyses and query views.
Compaction preserves the indices and coverage; it needs memory for new columns
and keeps unused relation definitions. See
{ref}`Reclaiming retired observations <user-tools-interactions-compaction>`.

This preserves other structures and checks calculation compatibility; attaching
`fresh` directly would replace the whole named analysis. Geometry delegation failures conservatively retain
unevaluated coverage because a partial write may have occurred.

This automatic boundary is the native MolSys form. If you edit a separately
accessed `molsys.structures` directly, explicitly replace each affected named
result with `analysis.invalidate_structures(structure_indices)`. Geometry
setters do not infer changes made through independent objects or aliased data.

Invalidation applies even when the moved atom did not participate in a previous
interaction: moving it can create a new one. No detector runs automatically.
Use structure coverage, not a zero occurrence count alone, to distinguish a pending
calculation from a calculated absence. See
{ref}`Changing coordinates <user-tools-interactions-coordinate-edits>` for a
copyable example and the complete edit policy.

Changing chemical-state atom or scientific bond assignments through
`msm.set(molsys, ...)`, or replacing `molsys.chemical_states`, marks every
named analysis unevaluated. Charge centers, aromatic participants and
hydrogen-bond roles can change at fixed coordinates. MolSysMT conservatively
invalidates all covered structures because it does not infer each method's
chemical dependencies. Empty atom/bond selections and bond ID changes preserve
analyses. Assigning or clearing `structure_chemical_state_index` invalidates
only the selected structures. Earlier result/query snapshots remain available.

Separately accessed Topology/ChemicalStates collections, direct topology
replacement, mechanics changes and raw table/array edits require explicit
owner invalidation. Recalculate and attach new results before claiming that
these changed data have been evaluated.

## Invariants and Performance

Structural iteration reads the existing `structures` domain without copying
the complete ensemble first. Coordinate getters copy only the requested
atom and structure selection. The original system stays in memory, and
collecting every returned block still stores the complete selected result.
Use structure **indices** to choose rows; `structure_id` contains labels
that need not be consecutive numbers or match those indices.

- **String Identifier Invariant**: All element IDs (`atom_id`, `group_id`, `chain_id`) inside `topology` are normalized to string representations.
- **Fast Digestion Bypass**: Compatible with `skip_digestion=True` for high-frequency internal algorithm passes.

---

## API Documentation

Detailed methods, converters, and getters for `molsysmt.MolSys` are documented in the [{doc}`molsysmt.MolSys API Reference </api/form/molsysmt_MolSys/api_molsysmt_MolSys>`].

Metal coordination candidates and one- or two-water hydrogen-bond paths can be named
independent analyses in `molsys.interactions`. Their observed geometry does not
change declared chemical-state bonds. See {ref}`Getting metal coordination
<Tutorial_Get_metal_coordination>` and {ref}`Getting water bridges
<Tutorial_Get_water_bridges>` for exact chemical requirements and atom scopes.

### Detached aromaticity

ChemicalStates owns declared aromatic flags. Optional
{func}`molsysmt.physchem.get_aromaticity` returns detached model-dependent flags
on a complete selected graph; it does not fill missing stored assignments.
See {ref}`Tutorial_Get_Aromaticity` for prerequisites and source-axis evidence.


### Named chemical types

Chemical element symbols remain in `atom_type`. Mechanical `atom_ff_type`
labels are separate parameter assignments. A named chemical-environment profile
can attach labels with an `atom_type_assignment` report in MolecularMechanics.
It records the original rule/provider versions and binds labels to chemistry.
Extraction projects parent labels; manual replacement clears their attribution.
The PDBQT writer rejects stale named reports before writing. Charges and typing
are independent operations; neither establishes full parameterization. Both
mechanical reports are excluded from H5MSM 0.5. See
{ref}`Tutorial_AutoDock_Typing` and {ref}`Tutorial_Assign_AutoDock_Types`.

Native heavy-atom repair and terminal insertion retain the selected state's
known atom assignments and provenance while leaving new chemical fields unknown
and marking connectivity partial. They require one chemical state for expansion.
Atom IDs survive; group sorting or inserted groups can change indices. Named
interaction definitions and source-axis maps are retained and remapped, while
occurrences and evaluated coverage are cleared for recalculation. Atom-aligned
structural observables and force-field parameters without new values are reported
as dropped. The heavy-atom tool offers strict rejection of that loss. See
{ref}`Tutorial_Add_missing_heavy_atoms` for repair limits and attribute policy.
