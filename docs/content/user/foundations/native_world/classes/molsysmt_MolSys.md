(user-foundations-native-world-classes-molsysmt-molsys)=
# MolSys

`molsysmt.MolSys` is the primary native unified molecular system container in MolSysMT. It composes the topological graph, 3D structures sequence or ensemble, and molecular mechanics parameter contracts into a single immutable state object.

---

## Overview and Role

As a user, `molsysmt.MolSys` is the central object returned when loading, converting, or processing molecular systems. By composing dedicated sub-containers, `MolSys` ensures strict separation of concerns while providing a unified gateway for selections, spatial queries, and form transformations.

`molsysmt.MolSys` instances are treated as immutable state objects. Modifying system composition or atom inventories is handled via `molsysmt.MolSysBuilder` before compiling back to a fresh `MolSys`.

---

## Internal Attributes

Inside a `molsysmt.MolSys` instance, three primary core component objects are composed:

| Attribute | Internal Object Class | Description |
| :--- | :--- | :--- |
| **`topology`** | `molsysmt.Topology` | Topological graph containing atom, residue, group, component, molecule, and chain inventories. |
| **`structures`** | `molsysmt.Structures` | Structural container holding 3D coordinates `(n_structures, n_atoms, 3)`, periodic box matrices `(n_structures, 3, 3)`, and frame timestamps. |
| **`molecular_mechanics`** | `molsysmt.MolecularMechanics` | Forcefield parameters, partial charges, atom masses, and non-bonded interaction rules. |

---

## Invariants and Performance

- **String Identifier Invariant**: All element IDs (`atom_id`, `group_id`, `chain_id`) inside `topology` are normalized to string representations.
- **Fast Digestion Bypass**: Compatible with `skip_digestion=True` for high-frequency internal algorithm passes.

---

## API Documentation

Detailed methods, converters, and getters for `molsysmt.MolSys` are documented in the [{doc}`molsysmt.MolSys API Reference </api/form/molsysmt_MolSys/api_molsysmt_MolSys>`].
