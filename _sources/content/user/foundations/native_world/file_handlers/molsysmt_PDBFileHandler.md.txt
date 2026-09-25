(user-foundations-native-world-file-handlers-molsysmt-pdbfilehandler)=
# PDBFileHandler

`molsysmt.native.PDBFileHandler` is the native low-level parser and I/O handler class in MolSysMT for reading, writing, and parsing Protein Data Bank (`.pdb`) files.

---

## Overview and Handler Role

`PDBFileHandler` provides low-level file stream management and record-level parsing for PDB files (compliant with wwPDB format version 3.3). It acts as the internal I/O engine when converting `.pdb` files to native containers (`molsysmt.Topology`, `molsysmt.Structures`) or streaming multi-model structures via `msm.Iterator`.

---

## Class Attributes and Parsed Records

Inside `PDBFileHandler`, file content is parsed into structured record containers and string buffers:

| Attribute / Property | Data Type | Description |
| :--- | :--- | :--- |
| **`file`** | `io.StringIO` or File Handle | Active stream handle pointing to memory string buffer or disk file. |
| **`format_version`** | String (`"3.3"`) | Format specification version string determined during file loading. |
| **`entry`** | Parsed Record Object | Structured representation of PDB header records (TITLE, HELIX, SHEET, SSBOND). |
| **`content`** | Dictionary / Record Array | Normalized record arrays containing atomic coordinates, element names, residue IDs, and occupancy. |

---

## Practical Usage and Streaming Workflow

```python
import molsysmt as msm
from molsysmt.native import PDBFileHandler

# 1. Initialize PDBFileHandler directly with a PDB file path
handler = PDBFileHandler("protein.pdb", io_mode="r")

# 2. Inspect parsed content dictionary
parsed_records = handler.content

# 3. Always close the file handler stream when finished
handler.close()
```

---

## Performance and I/O Invariants

- **Serial Number Overflow Support**: Supports standard decimal atom serial numbers (1–99,999), uppercase hex overflow (OpenMM/VMD), and Hybrid-36 encoding (Chimera/CCTBX).
- **Resource Management**: Ensures underlying stream buffers are closed cleanly via `.close()` or garbage collection (`__del__`).
