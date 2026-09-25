(user-foundations-native-world-file-handlers-molsysmt-h5msmfilehandler)=
# H5MSMFileHandler

`molsysmt.native.H5MSMFileHandler` is the native binary HDF5 I/O handler class in MolSysMT responsible for reading, writing, and streaming `.h5msm` binary files.

---

## Overview and Handler Role

`H5MSMFileHandler` manages disk handles for MolSysMT's native `.h5msm` binary format. It encapsulates `h5py.File` handles, manages compression filters (Gzip/LZF), enforces schema versioning (Schema 0.4 and 0.3), and powers chunked trajectory iterators.

---

## Class Attributes and Parsed Records

Inside `H5MSMFileHandler`, state and binary datasets are exposed via property interfaces:

| Attribute / Property | Data Type | Description |
| :--- | :--- | :--- |
| **`file`** | `h5py.File` | Active HDF5 file handle opened in read (`"r"`) or write (`"w"`) mode. |
| **`format_version`** | String (`"0.4"`) | Schema specification version read from root file attributes. |
| **`topology`** | HDF5 Group (`/topology`) | HDF5 group containing `atoms`, `groups`, `bonds`, `chains`, and `chemical_states`. |
| **`structures`** | HDF5 Group (`/structures`) | HDF5 group containing coordinate matrices `(n_structures, n_atoms, 3)` and box vectors. |

---

## Practical Usage and Streaming Workflow

```python
import molsysmt as msm
from molsysmt.native import H5MSMFileHandler

# 1. Open an h5msm file handler in context manager mode
with H5MSMFileHandler("trajectory.h5msm", io_mode="r") as handler:
    # 2. Access raw HDF5 dataset shapes without loading to RAM
    coords_shape = handler.file["/structures/coordinates"].shape
    version = handler.format_version
```

---

## Performance and I/O Invariants

- **Context Manager Support**: Fully supports python context protocol (`with H5MSMFileHandler(...) as handler:`).
- **Zero-Copy Dataset Views**: Enables direct dataset slicing from HDF5 disk blocks without loading full trajectories into RAM.
