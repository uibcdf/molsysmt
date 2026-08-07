(user-foundations-native-world-classes-molsysmt-molsys)=
# molsysmt.MolSys

`molsysmt.MolSys` is the primary native unified molecular system container in MolSysMT. It composes the topological graph, 3D structural trajectory, and molecular mechanics parameter contracts into a single immutable state object.

---

## Conceptual Overview & User Role

As a user, `molsysmt.MolSys` is the central object returned when loading, converting, or processing molecular systems. By composing dedicated sub-containers, `MolSys` ensures strict separation of concerns while providing a unified gateway for selections, spatial queries, and form transformations.

`molsysmt.MolSys` instances are treated as immutable state objects. Modifying system composition or atom inventories is handled via `molsysmt.MolSysBuilder` before compiling back to a fresh `MolSys`.

---

## Internal Architecture & Attributes (What's Inside)

Inside a `molsysmt.MolSys` instance, three primary core component objects are composed:

| Attribute | Internal Object Class | Physical Units | Description |
| :--- | :--- | :--- | :--- |
| **`topology`** | `molsysmt.Topology` | N/A | Topological graph containing atom, residue, group, component, molecule, and chain inventories. |
| **`structures`** | `molsysmt.Structures` | Length in `nm`, Time in `ps` | Structural trajectory container holding 3D coordinates `(n_structures, n_atoms, 3)`, periodic box matrices `(n_structures, 3, 3)`, and frame timestamps. |
| **`molecular_mechanics`** | `molsysmt.MolecularMechanics` | Charge in `e`, Mass in `Da` | Forcefield parameters, partial charges, atom masses, and non-bonded interaction rules. |

---

## Declarative Dictionary Serialization (`MolSysDict`)

`molsysmt.MolSys` can be losslessly serialized into a declarative Python dictionary (`molsysmt.MolSysDict`) or instantiated directly from a declarative system dictionary:

```python
import molsysmt as msm

# 1. Converting a MolSys instance to a serializable MolSysDict
molsys_dict = system.to_dict()

# 2. Instantiating a new MolSys from a MolSysDict
system = msm.convert(molsys_dict, to_form='molsysmt.MolSys')
```

---

## Invariants, Performance & API Reference

- **String Identifier Invariant**: All element IDs (`atom_id`, `group_id`, `chain_id`) inside `topology` are normalized to string representations.
- **Fast Digestion Bypass**: Compatible with `skip_digestion=True` for high-frequency internal algorithm passes.
- **API Reference**: Detailed methods, converters, and getters for the `molsysmt.MolSys` form are documented in the [{doc}`molsysmt.MolSys API Reference </api/form/molsysmt_MolSys/api_molsysmt_MolSys>`].
