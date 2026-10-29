(user-foundations-native-world-classes)=
# Classes

Welcome to **Classes**, the native object module detailing MolSysMT's core Python data containers and declarative dictionary schemas.

Native objects have brief metadata representations for interactive inspection.
They distinguish unavailable axes from empty ones and avoid rendering arrays,
validating chemistry or reading file contents. See {ref}`user-foundations-native-world-classes-molsysmt-molsys`
and the executed example in {ref}`Tutorial_Info`. Plain Python dictionaries keep
their ordinary representation.

Resident `MolSys`, `Topology`, `Structures`, `ChemicalStates`, `Interactions`
and `MolSysBuilder` objects also share validated `get()`/`info()` methods.
The typed `ChemicalStatesDict` wrapper provides these methods directly over its
stored columns. Plain dictionary forms retain ordinary Python key lookup.
They follow the basic-tool arguments and outputs for each available domain;
use named options to preserve the legacy MolSys positional convention.
See {ref}`Tutorial_Get` and {ref}`Tutorial_Info` for executed examples.

---

## **Contents**

- **{doc}`molsysmt_MolSys`**  
  The native unified molecular system composing topology, chemical states, structures, named interactions and optional molecular mechanics.

- **{doc}`molsysmt_MolSysBuilder`**  
  The editable native container for incrementally constructing and modifying molecular models.

- **{doc}`molsysmt_MolSysDict`**  
  The declarative, serializable dictionary representation of a complete molecular system.

- **{doc}`molsysmt_Topology`**  
  The stable atom, group, molecule, entity and chain inventory, with transitional chemical compatibility access.

- **{doc}`molsysmt_TopologyDict`**  
  The declarative, serializable dictionary representation of molecular topology.

- **{doc}`molsysmt_ChemicalStates`**
  The ordered chemical-state collection with selected-state graph editing and state-local components.

- **{doc}`molsysmt_ChemicalStatesDict`**
  Typed chemical columns with direct selected-state queries and explicit null masks.

- **{doc}`molsysmt_Structures`**  
  The native structures container storing 3D coordinates, periodic boxes and structure-aligned series.

- **{doc}`molsysmt_StructuresDict`**  
  The declarative, serializable dictionary representation of coordinate and other structure-aligned data.

- **{doc}`molsysmt_MolecularMechanics`**  
  The native molecular mechanics object managing force field terms, partial charges, masses, and energy parameters.

- **{doc}`molsysmt_MolecularMechanicsDict`**  
  The declarative, serializable dictionary representation of molecular mechanics parameters.

- **{doc}`molsysmt_ViewerJSON`**  
  The lightweight, JSON-serializable graphics representation for 3D visualization and web renderers.

```{eval-rst}
.. toctree::
   :maxdepth: 1
   :hidden:

   molsysmt_MolSys
   molsysmt_MolSysBuilder
   molsysmt_MolSysDict
   molsysmt_Topology
   molsysmt_TopologyDict
   molsysmt_ChemicalStates
   molsysmt_ChemicalStatesDict
   molsysmt_Structures
   molsysmt_StructuresDict
   molsysmt_MolecularMechanics
   molsysmt_MolecularMechanicsDict
   molsysmt_ViewerJSON
```
