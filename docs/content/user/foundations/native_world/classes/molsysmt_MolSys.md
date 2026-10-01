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
| **`structures`** | `molsysmt.Structures` | Structural container holding 3D coordinates `(n_structures, n_atoms, 3)`, periodic box matrices `(n_structures, 3, 3)`, and frame timestamps. |
| **`chemical_states`** | `molsysmt.ChemicalStates` | State-dependent covalent bonds and atom-level chemical assignments. |
| **`interactions`** | Named `molsysmt.Interactions` results | Sparse observations with declared atom and structure index domains. |
| **`molecular_mechanics`** | `molsysmt.MolecularMechanics` | Forcefield parameters, partial charges, atom masses, and non-bonded interaction rules. |

An H5MSM 0.5 file may load as a partial `MolSys` without topology. If it
contains only named interactions, those results supply the atom and structure
index domains. `extract(atom_indices=[...], structure_indices=[...])` remaps
the present domains and keeps the selected structure order. An axis with no
declared domain cannot be selected explicitly.

Both hydrogen-bond detectors and the disulfide candidate detector can return an
independent `molsysmt.Interactions` analysis with
`output_type="molsysmt.Interactions"`. Attach it under a name by assigning
`molsys.interactions = {**molsys.interactions, "analysis_name": analysis}`.
This retains previous named results and checks that all analyses match the
system's atom and structure axes.

This assignment declares that the analysis's local atom and structure indices
correspond to the system. MolSysMT checks compatible axes and valid results;
you are responsible for the correspondence of independently loaded data.
Source labels and maps retain provenance without authenticating that origin.
Chemical recognition and geometric criteria are separate parts of an analysis.
Named hydrogen-bond, π–π, cation–π and halogen profiles carry their pinned method references;
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

ChemicalStates distinguishes implicit hydrogen counts, bracket-declared atom-level
explicit hydrogen counts (`n_explicit_hydrogens`), and real indexed H atoms. Native
and H5MSM round trips preserve the annotations without adding coordinate rows.

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
