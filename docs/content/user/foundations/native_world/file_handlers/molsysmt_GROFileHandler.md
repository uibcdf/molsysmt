(user-foundations-native-world-file-handlers-molsysmt-grofilehandler)=
# GROFileHandler

`molsysmt.native.GROFileHandler` is the native low-level reader for a GROMACS
GRO coordinate entry. Its current writer is not implemented.

## Overview and Handler Role

The handler loads the source text into a resident buffer and parses the **first
entry**. It is a single-entry reader, not a streaming trajectory reader. It
retains atom/group labels, fixed-width coordinates, optional velocities and
three- or nine-value periodic boxes. GRO positions are in nm and velocities
in nm/ps; the nine-value box is represented by three row vectors.
The [GROMACS format reference](https://manual.gromacs.org/current/reference-manual/file-formats.html#gro)
describes the external record layout.

## Class Attributes and Parsed Records

Parsed fields live under `handler.entry`, not directly on the handler:

| Attribute / Property | Data Type | Description |
| :--- | :--- | :--- |
| **`file`** | `io.StringIO` | Resident source stream; its owner closes it. |
| **`entry.header`** | str | First entry's title line. |
| **`entry.n_atoms`** | int | Atom count declared by the entry. |
| **`entry.atom_names`, `entry.atom_ids`** | arrays | Deposited atom labels; native conversion normalizes IDs to strings. |
| **`entry.group_names`, `entry.group_ids`** | arrays | Group labels, distinct from zero-based indices. |
| **`entry.coordinates`** | quantity | Parsed atom positions in nm. |
| **`entry.velocities`** | quantity or None | Optional velocities in nm/ps. |
| **`entry.box`** | quantity | Three row vectors in nm. |

There is no public `handler.content`, `handler.title` or `handler.n_atoms`
attribute. Request higher-level quantities and selections through
{func}`molsysmt.basic.get` or convert to a native molecular system.

## Practical Usage and Streaming Workflow

```python
import molsysmt as msm
from molsysmt.native import GROFileHandler

handler = GROFileHandler(msm.systems['nglview']['md_1u19.gro'])
copied = msm.copy(handler)
try:
    print(handler.entry.header, handler.entry.n_atoms)
    assert copied is not handler
finally:
    copied.close()
    handler.close()
```

Default identity conversion, `copy` and whole-handler `extract` create an
independent resident buffer and parsed entry. Closing or editing the copy does
not close or change the original. Explicit `copy_if_all=False` permits aliasing.
Handler subset extraction and handler writing remain unsupported; convert to
`MolSys` or `Structures` to work with native selections.

## Performance and I/O Invariants

The resident buffer and parsed entry are loaded eagerly; no large-file or
streaming performance claim follows from the class name. Native GRO conversion
reads one entry, including the optional velocities. For concatenated coordinate
structures, use the existing MDTraj/OpenMM provider routes and inspect their
supported attributes rather than assuming every GRO form retains every field.

### Connectivity and conversions

GRO declares labels and coordinates, but no covalent bonds. The native conversion
uses {func}`molsysmt.build.get_missing_bonds` unless `get_missing_bonds=False`.
Inference occurs on the complete first entry before atom extraction. Consecutive
groups with equal IDs remain distinct when their names differ. Inferred bonds
do not certify arbitrary chemistry or assign force-field parameters.

The file-to-OpenMM Topology and Modeller bridges reuse native conversion and
extraction. Selected atom labels, inferred bonds and coordinates use the same
native source order, and the periodic box is retained. These native-backed file
bridges have the same first-entry scope; Modeller represents one structure.

The file-to-MDTraj Topology/Trajectory bridges use the existing native connectivity
policy. MDTraj reads the coordinate series, available times and boxes. Nonconsecutive
structure lists retain requested geometry; MDTraj's own lengths use nm and time
uses ps. Its output does not retain native chemical-state evidence.

Reading attributes or converting a caller-owned `mdtraj.GroTrajectoryFile` uses
independent read cursors and leaves the original iteration position unchanged.
Its public copy opens a new cursor at the **beginning of the same backing file**
with independent mutable topology; it does not duplicate file bytes or the
original cursor position. Closing a copied cursor leaves the original open.
This coordinate-oriented form does not declare the native handler's full set
of topological attributes or velocity data. When converting an
`openmm.GromacsGroFile` to MolSys, atom extraction is applied once to topology
and coordinates together, preserving their correspondence.
