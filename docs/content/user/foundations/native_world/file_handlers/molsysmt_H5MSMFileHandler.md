(user-foundations-native-world-file-handlers-molsysmt-h5msmfilehandler)=
# H5MSMFileHandler

`molsysmt.native.H5MSMFileHandler` owns an open HDF5 handle for legacy H5MSM
0.3/0.4 files. Its registered form name is `molsysmt.H5MSMFileHandler`.

---

## Overview and Handler Role

The handler opens legacy files for supported queries and structure iteration,
or creates a legacy 0.4 file when explicitly requested with `io_mode="w"`.
Reading emits the legacy deprecation warning. Always close the handle, preferably
with a context manager.

The handler rejects modular **0.5, 0.6 and 1.0** roots with `FormatError`.
Public `msm.convert` and `msm.h5msm.write` default to 1.0; their output cannot be
opened with this legacy class. Use `msm.h5msm.read(path)` or
`msm.convert(path, to_form="molsysmt.MolSys")` for resident assembly, and
`msm.h5msm.read_layers(path, layers=["structures"])` for a resident selected layer.
These operations do not return a modular file-backed handler. See
{ref}`user-tools-form-h5msm-10` for the supported public interfaces and limits.

Unsupported creation versions reject before opening or truncating a destination.
A valid legacy `io_mode="w"` remains an explicit replacement operation; this is
not a general crash-transactional writer.

---

## Class Attributes and Parsed Records

The class exposes `file` and `format_version`. Topology and structural HDF5
groups are accessed through `file`; there are no `handler.topology` or
`handler.structures` properties.

| Attribute or expression | Data type | Meaning |
| :--- | :--- | :--- |
| `handler.file` | `h5py.File` | Owned legacy file handle; valid only while open. |
| `handler.format_version` | str | Decoded legacy root version, `"0.3"` or `"0.4"`. |
| `handler.file["topology"]` | `h5py.Group` | Legacy inventory and represented chemical-state data. |
| `handler.file["structures"]` | `h5py.Group` | Legacy coordinate, box, time and observable datasets. |
| `handler.file["structures/coordinates"].shape` | tuple | Stored `(n_structures, n_atoms, 3)` shape, read as metadata. |

---

## Practical Usage and Streaming Workflow

```python
import molsysmt as msm
from molsysmt.native import H5MSMFileHandler

legacy_path = msm.systems["pentalanine"]["traj_pentalanine.h5msm"]
with H5MSMFileHandler(legacy_path, io_mode="r") as handler:
    coords_shape = handler.file["structures/coordinates"].shape
    version = handler.format_version
    # Public queries apply the active PyUnitWizard output policy.
    coordinates = msm.get(
        handler, selection=[0, 1], structure_indices=[0], coordinates=True
    )
    assert coordinates.shape == (1, 2, 3)
    assert coords_shape[1:] == (62, 3)
```

The legacy adapter supports its declared coordinate/box iteration routes.
Iteration allocates each requested chunk; a small chunk does not bound every
HDF5 cache or downstream result. The
{ref}`form tutorial <Tutorial_Form_molsysmt_H5MSMFileHandler>` distinguishes
working access routes from exported but unimplemented operations.

---

## Performance and I/O Invariants

- **Resource lifetime:** closing the handler invalidates its HDF5 dataset/group
  handles. Context exit closes only the handle owned by that context.
- **Metadata and slices:** shape/dtype inspection does not load a coordinate
  series. Raw `dataset[...]` reads materialize NumPy arrays; they are not
  zero-copy views of on-disk data and do not apply PyUnitWizard conversion.
- **Copy boundary:** independent copying of a live handler is unavailable and
  raises `NotImplementedMethodError`. Finish a writer first, then use
  `msm.copy(filename)` for byte-preserving file copying, or convert to resident
  `MolSys` before copying. The supported file-path route retains the stored
  version and its documented process-owned or explicit destination lifetime.
