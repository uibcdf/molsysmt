(Cookbook_Copying_Disk_Systems)=
# Copying a stored system

*Keeping file snapshots and editable native copies independent.*

Omit the destination for a session-owned temporary snapshot, or choose a filename
for persistent storage. Convert to a native object when you want to edit
coordinates in memory. These operations have different ownership and lifetimes.

:::{versionadded} 1.0.0
:::

## Copying the stored bytes

This example writes bundled particle coordinates as H5MSM 0.5, then creates
both automatic and persistent copies. Raw copying does not deserialize the
molecular data. A caller-owned Python context manages the demonstration source
and persistent destination; MolSysMT manages the separate automatic snapshot.

```python
import filecmp
import tempfile
from pathlib import Path
import numpy as np
import molsysmt as msm
from molsysmt.native import Structures
puw = msm.pyunitwizard

with tempfile.TemporaryDirectory() as directory:
    source = Path(directory) / 'source.h5msm'
    destination = Path(directory) / 'snapshot.h5msm'
    structures = Structures(coordinates=msm.get(
        msm.systems['particles 4']['traj_particles_4.xyznpy'], coordinates=True))
    msm.h5msm.write_layers(str(source), structures=structures)
    automatic = msm.copy(source)
    snapshot = msm.copy(source, output_filename=destination)
    assert filecmp.cmp(source, automatic, shallow=False)
    assert filecmp.cmp(source, snapshot, shallow=False)

    molsys = msm.convert(automatic, to_form='molsysmt.MolSys')
    molsys_working = msm.copy(molsys)
    original = msm.get(molsys, selection=[0], structure_indices=[0], coordinates=True)
    moved = original + puw.quantity(np.array([1., 0., 0.]), 'nm')
    msm.set(molsys_working, selection=[0], structure_indices=[0], coordinates=moved)
    np.testing.assert_array_equal(
        puw.get_value(msm.get(molsys, selection=[0], structure_indices=[0],
            coordinates=True), to_unit='nm'), puw.get_value(original, to_unit='nm'))
    np.testing.assert_allclose(
        puw.get_value(msm.get(molsys_working, selection=[0], structure_indices=[0],
            coordinates=True), to_unit='nm'), puw.get_value(moved, to_unit='nm'))
    assert filecmp.cmp(source, snapshot, shallow=False)
assert Path(automatic).is_file()  # session-owned, independent of the context above
```

## Copying a coordinate file and saving a selection

DCD/XTC byte copies have the same lifetime rules. Selected coordinate conversion
requires optional MDTraj; subset serialization back to DCD/XTC is unsupported.
Save selected structures as H5MSM instead. Here the source carries coordinates
without a topology; the H5MSM output keeps that structural scope.

```python
source = msm.systems['chicken villin HP35']['traj_chicken_villin_HP35_solvated.dcd']
with tempfile.TemporaryDirectory() as directory:
    snapshot = msm.convert(source, to_form='file:dcd',
        output_filename=Path(directory) / 'snapshot.dcd')
    assert filecmp.cmp(source, snapshot, shallow=False)
    selected = msm.convert(source, to_form='molsysmt.Structures',
        selection=[3, 1], structure_indices=[2, 0])
    assert selected.coordinates.shape == (2, 2, 3)
    destination = Path(directory) / 'selected.h5msm'
    msm.convert(source, to_form=destination,
        selection=[3, 1], structure_indices=[2, 0])
    restored = msm.convert(destination, to_form='molsysmt.Structures')
    np.testing.assert_allclose(puw.get_value(restored.coordinates, to_unit='nm'),
        puw.get_value(selected.coordinates, to_unit='nm'), atol=1e-6)
```

The input remains unchanged. Explicit source aliases are rejected even for a
whole-file output. `copy_if_all=False` returns the source only with all atoms,
all structures and no output filename. File-handler copying has separate
capabilities; it must not be inferred from a successful file-path copy.

## Respecting each boundary

Without `output_filename`, MolSysMT securely reserves a unique same-suffix path
in a private directory under the platform temporary directory. These ordinary
path strings remain valid for the current Python process, independently of string
copies or garbage collection. Normal interpreter exit attempts to remove only
registered automatic copies. Abrupt termination or locked files can leave
leftovers; no unconditional cleanup guarantee is made. Choose a persistent
destination for a saved session or another process that must outlive the creator.

An explicit destination is caller-owned and never automatically deleted, even
if it is placed in the temporary workspace. Existing distinct destinations may
be overwritten. Directories and source aliases, including symlinks and hard
links, raise `ArgumentError`. A composite source without a destination receives
individual member copies; one explicit filename cannot address multiple inputs.
Failed automatic copies are retired; an explicit destination remains caller-owned
if a filesystem write fails. Automatic copies are private and writable even when
the source is read-only. Native conversion materializes data in RAM; a byte copy
instead consumes additional temporary disk space.
The selected temporary filesystem can itself be RAM-backed; choose its location
to suit the size of your data.

A byte copy keeps the H5MSM version, compression and stored domains. It does not
migrate legacy data; use {func}`molsysmt.h5msm.migrate_to_05` for that operation.
SDF and PDBQT copies retain their adapter-specific validation. File copying does
not certify chemical validity, and live file handlers have separate resource
contracts. Native conversion materializes the selected molecular data in RAM;
choose selections and a suitable memory budget before loading a large ensemble.

:::{seealso}
:class: dropdown

- {ref}`Copy <Tutorial_Copy>`
- {ref}`Native copying <user-foundations-resident-copying>`
- {ref}`Migrating H5MSM <cookbook-migrating-h5msm>`
:::
