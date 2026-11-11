(user-foundations-native-world-files-file-h5msm)=
# h5msm

`h5msm` is MolSysMT's native binary HDF5 storage format (`.h5msm`) engineered for rapid I/O, trajectory chunking, compressed persistence, and complete metadata preservation.

---

## Overview and Format Purpose

The `h5msm` file format provides an efficient, portable, and versioned binary persistence format built on top of HDF5 (`h5py`). It is designed to store complex molecular topologies, chemical states, 3D coordinate structure series, and sparse interaction analyses in a single file with explicit precision and unit definitions. Nonempty molecular mechanics is outside schema 0.5.

Public conversion writes **Schema 0.5**. Legacy **Schema 0.3/0.4** files remain
readable with a deprecation warning. The layout below describes the legacy
format; see {doc}`the modular 0.5 schema <../../../tools/form/file/h5msm_05>`.

---

Experimental **Schema 0.6** is available by explicit `format_version="0.6"`
in conversion or `msm.h5msm.write`; it preserves the bounded mechanical domain
and original assignment reports. The default stays 0.5. Reading stored mechanics
does not calculate or certify assignments. See {ref}`user-tools-form-h5msm-06`
for public layer queries, metadata cardinalities, source-preserving extraction
and the limitations of resident assembly. The legacy handler does not support
modular roots.

Explicit `format_version="1.0"` is also available in development for writing a
new modular file and testing migration. It stores the same independent domains
as 0.6, including mechanics. To migrate a complete modular file while retaining
independent layers and axis links, see {ref}`cookbook-migrating-h5msm-10`.

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

    # 3. Load only the requested domain; this is still a resident layer load.
    structures = msm.h5msm.read_layers(h5_file, layers=["structures"])
```

---

Legacy H5MSM 0.3/0.4 readers require explicit units. Dataset units are checked against any duplicated group/root declarations; equivalent spellings are accepted, but different scales or dimensions raise `FormatError`. A missing dataset unit may use a coherent explicit group/root declaration. Velocity units may be derived from explicit length/time declarations. B factors require their own unit because legacy writers negotiated it independently of coordinates; missing metadata never implies nm or ps. Public queries and iteration convert the resulting quantities to your active PyUnitWizard policy. Migration to 0.5 validates these units before writing.

For legacy 0.3/0.4 files, `msm.get(molsys, structure_index=True,
structure_indices=[3, 0, 3])` returns `[3, 0, 3]` when those positions exist.
This index-only query reads metadata, with no coordinate or other dataset payload
load. It also works on an open `H5MSMFileHandler` and leaves that handler open.
Indices are dimensionless positions, independent of stored structure IDs. Empty
selections return `[]`; `structure_indices=None` returns `None`; invalid positions
raise `ArgumentError`. Existing unit checks and legacy warnings still apply.
H5MSM 0.5 also supports metadata-only axis queries and projected dense structural
queries. Resident conversion remains a separate operation; see
{ref}`user-tools-form-h5msm-05` for the query scope and limits.

The modular 0.5 format preserves structure and chemical-state populations
independently. Structure-to-state indices are stored explicitly when the two
populations differ, including a prefix map into a larger state inventory.
An identity link requires equal populations and the same index at every position.
Reference-state choice and unknown associations remain separate. See
{ref}`user-tools-form-h5msm-05` for the versioned association contract.

A complete default conversion to `molsysmt.Topology` from one 0.5 path loads
only the stable inventory. That resident object is independent of the file;
unrequested coordinate, chemical-state and interaction payloads stay unloaded.
This does not validate every layer or bound the size of the inventory. Selection,
reporting and other contextual conversion options keep their existing route.
See {ref}`user-tools-form-h5msm-05` for the supported boundary.

## Performance and Storage Invariants

Modular H5MSM 0.5, 0.6, and 1.0 use field-specific stored types. Structural floating
series use float64; chemistry, topology, maps and mechanical payloads follow
their declared encodings. The legacy global `float_precision` and `int_precision`
conversion options are unsupported, including explicit `'single'` or `'double'`.
Omit them: public conversion raises `ArgumentConflictError` before publishing
output instead of accepting an ineffective setting. This neither changes the
schema nor rounds stored scientific evidence. Legacy 0.3/0.4 handlers keep
their separate precision controls.


- **Gzip & LZF Chunk Compression**: Trajectory coordinate datasets are chunked along the structure axis and compressed using Gzip (level 4) or LZF.
- **Selective I/O**: Legacy 0.3/0.4 handlers support dataset slicing. H5MSM 0.5 `get()` projects requested dense fields and atom/structure positions; counts use metadata. Static queries load required inventory/chemistry without coordinate series. Full conversion and `read_layers()` remain resident operations. Results and downstream analyses need their own memory budget.
- **Schema 0.4 Invariants**: Stable atom inventories and isotopes are isolated from chemical state definitions.
