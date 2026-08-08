(user-foundations-native-world-files-file-h5msm)=
# h5msm

`h5msm` is MolSysMT's native binary HDF5 storage format (`.h5msm`) engineered for rapid I/O, trajectory chunking, compressed persistence, and complete metadata preservation.

---

## Overview and Format Purpose

The `h5msm` file format provides an efficient, portable, and versioned binary persistence format built on top of HDF5 (`h5py`). It is designed to store complex molecular topologies, chemical states, multi-frame 3D coordinate trajectories, and forcefield parameters in a single file without losing precision or unit definitions.

New files written by MolSysMT use **Schema 0.4**, while maintaining full backward compatibility for reading legacy **Schema 0.3** files.

---

## HDF5 Layout and Dataset Schema

An `.h5msm` file organizes data into hierarchical HDF5 groups and dataset arrays:

| Group / Dataset Path | Data Type | Physical Units | Description |
| :--- | :--- | :--- | :--- |
| **`/`** (Root Attributes) | String / Attributes | N/A | File header attributes: `version` (`"0.4"`), `creator` (`"MolSysMT"`), `date`, and default unit definitions. |
| **`/topology/atoms`** | HDF5 Dataset / Compound | N/A | Atom inventory table containing `atom_id`, `atom_name`, `atom_type`, `isotope`, `group_index`, `chain_index`. |
| **`/topology/groups`** | HDF5 Dataset / Compound | N/A | Residue and group table containing `group_id`, `group_name`, `group_type`, `molecule_index`. |
| **`/topology/bonds`** | HDF5 Dataset / Compound | N/A | Bond table containing `atom1_index`, `atom2_index`, `bond_order`, `bond_type`, `is_aromatic`. |
| **`/topology/chemical_states`** | HDF5 Group | N/A | Chemical state subgroups containing state-local components, formal charges, and atom chemistry. |
| **`/structures/coordinates`** | HDF5 3D Dataset | `nanometer` (`nm`) | 3D Cartesian atomic coordinates array with shape `(n_structures, n_atoms, 3)`. |
| **`/structures/box`** | HDF5 3D Dataset | `nanometer` (`nm`) | Unit cell box vectors array with shape `(n_structures, 3, 3)`. |
| **`/structures/time`** | HDF5 1D Dataset | `picosecond` (`ps`) | Simulation timestamps vector with shape `(n_structures,)`. |

---

## Read, Write, and Streaming Operations

MolSysMT provides seamless conversion and streaming handlers for `.h5msm` files:

```python
import molsysmt as msm
from pathlib import Path
from tempfile import TemporaryDirectory

# 1. Save a native molecular system to an h5msm file
with TemporaryDirectory() as tmpdir:
    h5_file = Path(tmpdir) / "trajectory.h5msm"
    msm.convert(system, to_form="file:h5msm", output_filename=h5_file)

    # 2. Read topology or structures back from disk
    restored_sys = msm.convert(h5_file, to_form="molsysmt.MolSys")

    # 3. Stream trajectory frames in chunks without loading full file into RAM
    for chunk in msm.Iterator(h5_file, chunk_size=100, structure_indices="all"):
        coords = msm.get(chunk, element="system", coordinates=True)
```

---

## Performance and Storage Invariants

- **Gzip & LZF Chunk Compression**: Trajectory coordinate datasets are chunked along the structure axis and compressed using Gzip (level 4) or LZF.
- **Selective I/O**: `msm.get()` reads specific frame ranges or atom selections directly from disk without reading the whole trajectory.
- **Schema 0.4 Invariants**: Stable atom inventories and isotopes are isolated from chemical state definitions.
