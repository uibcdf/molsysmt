(user-tools-form-h5msm-10)=
# H5MSM 1.0

*Saving native molecular domains with explicit axes, units and provenance.*

H5MSM 1.0 is the default output of `msm.convert`, `msm.h5msm.write` and
`msm.h5msm.write_layers` in the current development source. It stores optional
Topology, ChemicalStates, Structures, named Interactions and MolecularMechanics
domains. A file can contain a complete system or independent layers with their
declared index associations. The first stable publication is coordinated with
MolSysMT 1.0.

## Writing a system

```python
from pathlib import Path
from tempfile import TemporaryDirectory
import h5py
import numpy as np
import molsysmt as msm
from molsysmt.native import MolSys, Structures

molsys = MolSys(n_atoms=2)
molsys.structures = Structures(
    coordinates=msm.pyunitwizard.quantity(np.zeros((1, 2, 3)), "nm")
)
molsys.molecular_mechanics.forcefield = "unresolved_model_request"
molsys.molecular_mechanics.partial_charge = [0.25, -0.25]

with TemporaryDirectory() as directory:
    path = Path(directory) / "system.h5msm"
    msm.convert(molsys, to_form=path)
    with h5py.File(path, "r") as stored:
        assert stored.attrs["version"] == "1.0"
    restored = msm.h5msm.read(path)
    np.testing.assert_array_equal(
        restored.molecular_mechanics.partial_charge, [0.25, -0.25]
    )
```

Choose a new destination. Publication of a new file is atomic and refuses an
existing destination. Mechanical model requests, parameter values and original
assignment reports are persisted as supplied. Reading them preserves their
assessment status.

## Reading layers and index associations

`msm.h5msm.read_layers(path, layers=["structures", "interactions"])` reads
the requested domains. An absent layer returns `None`; a present-empty
interaction collection returns `{}`. Independent layers can have different
atom axes. Equal counts establish correspondence only when declared in the
file's associations. `read` assembles a MolSys when those declarations support
one native system.

The root stores the file writer's version and creation time. Named analyses
retain their original scientific method, parameters, units, software versions,
coverage, occurrence indices and periodic images. Query and geometry
invalidation behavior is the native Interactions contract.

The domain codecs extend {ref}`H5MSM 0.5 <user-tools-form-h5msm-05>` with
the mechanics layer described under {ref}`user-tools-form-h5msm-06`.
Structural coordinates and boxes are stored in nm, time in ps, velocities in
nm/ps, temperature in K and energies in kJ/mol. Typed chemistry and mechanics
columns retain their declared encodings. Scalar mechanical quantities retain
their recorded units. Public queries follow your PyUnitWizard policy.

## Migrating and choosing older schemas

For a complete modular source, `msm.convert(source, to_form=destination)`
re-encodes its independent layers and axis maps into 1.0. Source 0.5 and 0.6 root
metadata are retained under `migration_source`. Conversion loads the stored
layers into memory. See {ref}`cookbook-migrating-h5msm-10`.

Explicit `format_version="0.5"` writes the mechanics-free schema.
`format_version="0.6"` writes the experimental intermediate schema. The named
helpers `migrate_to_05` and `migrate_04_to_05` still produce 0.5.
Legacy 0.3 and 0.4 files remain readable with a deprecation warning.
The legacy H5MSMFileHandler retains its 0.3/0.4 contract.

`msm.copy(path)` preserves the existing file bytes. File extraction preserves
the source's modular version while remapping the selected indices. Use
`convert` when the output should use the current default schema.
