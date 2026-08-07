(user-foundations-native-world-classes-molsysmt-molsysdict)=
# MolSysDict

`molsysmt.MolSysDict` is the native declarative dictionary representation of a complete molecular system in MolSysMT.

---

## Overview and Role

`molsysmt.MolSysDict` provides a pure Python dictionary schema capable of representing an entire molecular system without instantiating complex class structures. It is wrapped by the `MolSysDict` dataclass, making it ideal for JSON serialization, network transport, configuration files, and inter-process message passing.

---

## Declarative Schema

The underlying `data` dictionary of `MolSysDict` contains standard header envelope fields and nested core aspect dictionaries:

| Top-Level Key | Value Type | Description |
| :--- | :--- | :--- |
| **`"format"`** | String (`"molsysmt"`) | Framework format identifier tag. |
| **`"kind"`** | String (`"molsys"`) | System object category classifier. |
| **`"version"`** | String (`"0.1"`) | Schema specification version string. |
| **`"metadata"`** | Dictionary | User-defined or system provenance metadata dictionary. |
| **`"topology"`** | Dictionary (`TopologyDict`) | Declarative dictionary defining `atoms`, `groups`, `bonds`, `chains`, `molecules`, and `entities`. |
| **`"structures"`** | Dictionary (`StructuresDict`) | Declarative dictionary holding `structure_id`, `time`, `box`, `coordinates`, and observable trajectory fields. |

---

## Usage and Workflow

```python
import molsysmt as msm
import json

# 1. Convert a native system to a MolSysDict object
sys_dict = msm.convert(system, to_form='molsysmt.MolSysDict')

# 2. Extract underlying dictionary data and serialize to JSON string
json_str = json.dumps(sys_dict.to_dict())

# 3. Reconstruct native MolSys from MolSysDict
reconstructed_system = msm.convert(sys_dict, to_form='molsysmt.MolSys')
```

---

## Invariants and Performance

- **Pure JSON Compatibility**: Primitive Python types (`dict`, `list`, `str`, `int`, `float`, `None`) suitable for lossless JSON serialization.
- **Deep Copy Safety**: `sys_dict.to_dict(copy=True)` and `sys_dict.copy()` ensure deep copy isolation during message passing.

---

## API Documentation

Methods and form conversions for `molsysmt.MolSysDict` are documented in the [{doc}`molsysmt.MolSysDict API Reference </api/form/molsysmt_MolSys/api_molsysmt_MolSys>`].
