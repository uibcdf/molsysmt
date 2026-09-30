(user-foundations-native-world-classes-molsysmt-molsys)=
# MolSys

`molsysmt.MolSys` is the primary native molecular system container in MolSysMT. It can combine topology, chemical states, a 3D structures sequence or ensemble, named interaction results, and molecular mechanics data.

---

## Overview and Role

As a user, `molsysmt.MolSys` is the central object returned when loading, converting, or processing molecular systems. By composing dedicated sub-containers, `MolSys` ensures strict separation of concerns while providing a unified gateway for selections, spatial queries, and form transformations.

Some native operations edit a `MolSys` in place; `extract` returns an independent subset. A partial `MolSys` retains only the information domains that were available in its source.

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
Each analysis's `software` dictionary records its producer versions; saving
or loading the system preserves those versions rather than substituting
the version installed by the reader. An empty dictionary means unknown.
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

---

## Invariants and Performance

- **String Identifier Invariant**: All element IDs (`atom_id`, `group_id`, `chain_id`) inside `topology` are normalized to string representations.
- **Fast Digestion Bypass**: Compatible with `skip_digestion=True` for high-frequency internal algorithm passes.

---

## API Documentation

Detailed methods, converters, and getters for `molsysmt.MolSys` are documented in the [{doc}`molsysmt.MolSys API Reference </api/form/molsysmt_MolSys/api_molsysmt_MolSys>`].
