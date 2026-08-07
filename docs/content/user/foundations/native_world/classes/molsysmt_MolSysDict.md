(user-foundations-native-world-classes-molsysmt-molsysdict)=
# MolSysDict

`molsysmt.MolSysDict` is the native declarative dictionary representation of a complete molecular system in MolSysMT.

---

## Overview and Role

`molsysmt.MolSysDict` provides a pure Python dictionary schema capable of representing an entire molecular system without instantiating complex class structures. It is ideal for JSON serialization, network transport, configuration files, and inter-process message passing.

---

## Declarative Schema

A `molsysmt.MolSysDict` object is structured around three main dictionary keys corresponding to the core aspect containers:

| Top-Level Key | Value Type | Description |
| :--- | :--- | :--- |
| **`"topology"`** | `molsysmt.TopologyDict` | Declarative dictionary defining atoms, groups, components, molecules, chains, and bonds. |
| **`"structures"`** | `molsysmt.StructuresDict` | Declarative dictionary holding coordinate arrays, box vectors, and frame timestamps. |
| **`"molecular_mechanics"`** | `molsysmt.MolecularMechanicsDict` | Declarative dictionary storing forcefield names, partial charges, and atom masses. |

---

## Usage and Workflow

```python
import molsysmt as msm
import json

# 1. Convert native system to MolSysDict
sys_dict = msm.convert(system, to_form='molsysmt.MolSysDict')

# 2. Serialize to JSON string
json_str = json.dumps(sys_dict)

# 3. Reconstruct native MolSys from MolSysDict
reconstructed_system = msm.convert(sys_dict, to_form='molsysmt.MolSys')
```

---

## Invariants and Performance

- **Pure JSON Compatibility**: Arrays are stored as nested list structures or base64 binary strings when serialized.

---

## API Documentation

Methods and form conversions for `molsysmt.MolSysDict` are documented in the [{doc}`molsysmt.MolSysDict API Reference </api/form/molsysmt_MolSys/api_molsysmt_MolSys>`].
