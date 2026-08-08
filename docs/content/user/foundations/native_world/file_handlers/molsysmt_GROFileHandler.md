(user-foundations-native-world-file-handlers-molsysmt-grofilehandler)=
# GROFileHandler

`molsysmt.native.GROFileHandler` is the native low-level file handler class in MolSysMT for reading and writing Gromacs GRO (`.gro`) coordinate files.

---

## Overview and Handler Role

`GROFileHandler` manages file stream reading and line parsing for Gromacs `.gro` files. It handles fixed-column coordinate fields, residue numbering, atom labels, velocity vectors, and triclinic box vectors in nanometers.

---

## Class Attributes and Parsed Records

Inside `GROFileHandler`, parsed lines are exposed as structured field dictionaries:

| Attribute / Property | Data Type | Description |
| :--- | :--- | :--- |
| **`file`** | `io.StringIO` or File Handle | Active stream handle pointing to string memory buffer or disk file. |
| **`title`** | String | Header title line read from the first line of the GRO file. |
| **`n_atoms`** | Integer | Total number of atoms declared on line 2 of the GRO file. |
| **`content`** | Dictionary | Structured dictionary holding parsed atom names, residue IDs, coordinates (nm), and velocities. |

---

## Practical Usage and Streaming Workflow

```python
import molsysmt as msm
from molsysmt.native import GROFileHandler

# 1. Instantiate GROFileHandler
handler = GROFileHandler("system.gro", io_mode="r")

# 2. Access parsed title and atom counts
print(handler.title, handler.n_atoms)

# 3. Close handle
handler.close()
```

---

## Performance and I/O Invariants

- **Nanometer Unit Invariant**: Automatically parses coordinates directly in nanometers (`nm`) and velocities in `nm/ps`.
- **Fixed-Column Line Parser**: High-speed fixed-width string slicer for fast GRO file loading.
