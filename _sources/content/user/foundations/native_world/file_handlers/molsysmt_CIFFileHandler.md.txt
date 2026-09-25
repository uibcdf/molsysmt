(user-foundations-native-world-file-handlers-molsysmt-ciffilehandler)=
# CIFFileHandler

`molsysmt.native.CIFFileHandler` is the native low-level file handler class in MolSysMT for reading and parsing Macromolecular Crystallographic Information File (`.cif` / `.mmcif`) formats.

---

## Overview and Handler Role

`CIFFileHandler` provides dictionary-based category parsing for mmCIF files. It processes loop blocks, category key-value pairs (`_atom_site.*`, `_struct_conf.*`), and large macromolecular structures where standard PDB column limits (99,999 atoms) are exceeded.

---

## Class Attributes and Parsed Records

Inside `CIFFileHandler`, mmCIF syntax categories are stored in parsed dictionaries:

| Attribute / Property | Data Type | Description |
| :--- | :--- | :--- |
| **`file`** | File Handle / Stream | Active file handle pointing to mmCIF file or text buffer. |
| **`categories`** | Dictionary | Dictionary mapping mmCIF category headers (`_atom_site`, `_cell`, `_entity`) to value tables. |
| **`content`** | Dictionary | Standardized content dictionary prepared for conversion to `molsysmt.Topology` and `molsysmt.Structures`. |

---

## Practical Usage and Streaming Workflow

```python
import molsysmt as msm
from molsysmt.native import CIFFileHandler

# 1. Instantiate CIFFileHandler
handler = CIFFileHandler("complex.cif", io_mode="r")

# 2. Inspect mmCIF categories
categories = handler.categories

# 3. Close stream
handler.close()
```

---

## Performance and I/O Invariants

- **Arbitrary Size Scaling**: Handles large macromolecular assemblies without atom serial number truncation.
- **Robust Category Lexer**: Parses standard STAR/mmCIF token syntax and looped tables.
