# Forms and Conversions

## Form Adapters
Form adapters live under `molsysmt/form`. Each form module must define:
- `form_name`
- `form_type`
- `form_info`
- `_convert_to` dictionary where keys are form names and values are **strings** of the converter function names (e.g., `'to_molsysmt_MolSys'`).

## Lazy Discovery
Forms are discovered lazily. Mapping from form directory to dependency lives in
`molsysmt/_depdigest.py` (see `SPEC_DEPENDENCIES.md`).

### Conversion Path Resolution
1. When `msm.convert(A, to_form='B')` is called, the system calculates the shortest path in the conversion graph.
2. The values in `_convert_to` are strings to prevent loading submodule code until the edge in the graph is actually traversed.
3. The function `molsysmt.basic.convert._convert_one_to_one` handles the dynamic import of these string-named functions.

## Conversion Rules
- **Polymorphism in Handlers**: Native file handlers (`H5MSMFileHandler`, `PDBFileHandler`) must be able to instantiate themselves from a file path string during conversion to ensure long chains of `msm.convert` don't break.
- **Unit Standardization**: Every converter must use `PyUnitWizard` to ensure outputs are in MolSysMT standard units (nanometers, degrees, picoseconds).
- **ID Normalization**: All topological IDs (atom_id, group_id, etc.) must be converted to strings during ingestion to ensure uniform behavior across forms.

## Key 1.0.0 Additions
The following "Hardened" forms were added or finalized during the 1.0.0 sprint:
- **`rdkit.Mol`**: Full support for cheminformatics-grade molecules, including bond orders and conformers.
- **`biopython.PDBStructure`**: Support for BioPython's `Bio.PDB.Structure` objects.
- **`MDAnalysis.AtomGroup`**: Direct support for MDAnalysis selections without full Universe conversion.
- **`molsysviewer.MolSysView`**: The official viewer is now a first-class molecular system.

## Tier 3 cheminformatics forms (added March 2026)
- **`string:smiles`**: SMILES strings with optional `smiles:` prefix. `is_form` uses prefix detection, then rdkit, then structural-feature regex. Topology piped through `molsysmt.Topology` via rdkit.
- **`file:smi`**: SMILES text files (`.smi`). Multi-molecule files are merged into a single `molsysmt.Topology`. `to_string_smiles` works without rdkit; getters require rdkit.
- **`file:fasta`**: FASTA sequence files. Topology built directly from BioPython `SeqIO.parse`. Groups are amino acid residues; one chain per FASTA record.
- **`file:pir`**: PIR/NBRF sequence files. Same topology strategy as `file:fasta` using BioPython's PIR parser.
- **`openff.Molecule`**: OpenFF Toolkit `Molecule` object. Includes explicit hydrogens. Converters to/from `rdkit.Mol`, `string:smiles`, `openff.Topology`, `molsysmt.Topology`. Requires `openff-toolkit`.
- **`openff.Topology`**: OpenFF Toolkit `Topology` (one or more molecules). Multi-molecule topologies merged via `molsysmt.basic.merge`. Converters to `openmm.Topology` and `openff.Molecule` (single-molecule only). Requires `openff-toolkit`.

## Tier 2 forms recovered from attic (March 2026)

The following form adapters were absent from `molsysmt/form/` but referenced in `attic/`.
They were either implemented from scratch or recovered and corrected:

| Form | Status | Key notes |
|------|--------|-----------|
| `mdtraj.AmberRestartFile` | New | Always 1 frame. Coordinates in Å (convert with `puw.quantity(..., 'angstrom', standardized=True)`). Use `item._n_atoms` (not `item.n_atoms` — raises `OSError` because file handle is closed after mode='r' init). No topology. |
| `mdtraj.GroTrajectoryFile` | New | Coordinates already in nm. `getPeriodicBoxVectors()` returns `unitcell_vectors` shape `(n_frames, 3, 3)` in nm — use directly. `item.seek(0)` raises `NotImplementedError`; rewind with `item._file.seek(0)`. No topology. |
| `mdtraj.PDBTrajectoryFile` | New | Coordinates in Å. Exposes `item.topology` (an `mdtraj.Topology`). `to_mdtraj_Topology` returns it directly; `to_molsysmt_MolSys` builds a full topology via the mdtraj.Topology chain. |
| `parmed.GromacsTopologyFile` | New | Inherits from `parmed.Structure` — all Structure getters work. Key converter is `to_file_top` via `item.write(filename)`. Other converters delegate to `parmed_Structure` equivalents. Registered in `parmed_Structure._convert_to`. |
| `MDAnalysis.topology.PDBParser` | New | Constructed as `PDBParser(filename)`. Call `item.parse()` to get `MDAnalysis.core.topology.Topology`. No coordinates, no box. `to_molsysmt_Topology` and `to_molsysmt_MolSys` create a fresh `Universe(item.filename)` and delegate to `MDAnalysis_Universe` converters. |
| `openmm.GromacsGroFile` | Corrected | Pre-existing skeleton had multiple broken converters (see below). |

### `openmm.GromacsGroFile` — bugs found and fixed

The pre-existing skeleton in `molsysmt/form/openmm_GromacsGroFile/` had several critical errors:

| File | Bug | Fix |
|------|-----|-----|
| `to_openmm_Topology.py` | Used `item.topology` which does not exist in `openmm.app.gromacsgrofile.GromacsGroFile` | Replaced with `NotImplementedMethodError`; removed from `_convert_to` |
| `to_openmm_Modeller.py` | Used `item.topology` (same) and `structure_indices` undefined in function signature | Same fix |
| `to_molsysmt_Topology.py` | Used `item.topology` | Rewritten: builds `molsysmt.Topology` from `atomNames`, `residueIds`, `residueNames` using consecutive-group detection |
| `to_molsysmt_MolSys.py` | Imported `to_molsysmt_Topology` from `molsysmt.form.molsysmt_Topology` (converts a molsysmt.Topology to itself, wrong) | Fixed to use local `from .to_molsysmt_Topology import ...` |
| `get_structural_attributes.py` | Empty — no getter functions | Implemented all structural getters (see below) |
| `attributes.py` | Claimed bonds, molecules, chains as True (unavailable from this form) | Corrected to only True attributes with implemented getters |

**`openmm.app.gromacsgrofile.GromacsGroFile` actual API** (no `topology` property):
- `item.atomNames` — list of atom names
- `item.residueIds` — list of residue IDs (int, per atom)
- `item.residueNames` — list of residue names (per atom)
- `item.elements` — list of `Element` objects or `None` (per atom)
- `item.getPositions(asNumpy=True, frame=i)` — Quantity, nm, shape `(n_atoms, 3)`
- `item.getPeriodicBoxVectors(frame=i)` — Quantity wrapping tuple of 3 Vec3, nm
- `item.getNumFrames()` — int
- No time information stored

---

## `attributes.py` — contract and invariant

`attributes.py` describes what data the form **actually has**, not merely what has a getter
already implemented. The invariant is bidirectional:

> **If an attribute is `True` in `attributes.py`, a working getter function must exist.
> If a getter function exists, the corresponding attribute must be `True`.**

Do not set an attribute `True` because the form *could* provide it via an expensive
conversion — `attributes.py` is about what the form exposes **natively**. If data requires
calling `.parse()`, building a Universe, or full topology reconstruction, the attribute is
`False` and the data is only accessible via `msm.convert(item, to_form='molsysmt.Topology')`.

---

## `get_coordinates_from_atom` vs `get_coordinates_from_system`

The `coordinates` attribute is defined with `get_from=['atom', 'system']`. This means
the dispatch layer (`msm.get`) will call different getter functions depending on the
`element` argument:

- `element='atom'` (explicit) → `get_coordinates_from_atom(item, indices=..., structure_indices=...)`
- `element='system'` (default when no `selection` given) → `get_coordinates_from_system(item, structure_indices=...)`

**Both functions must be implemented** in `get_structural_attributes.py` for any form that
provides coordinates. `get_coordinates_from_system` returns all-atom coordinates (no
`indices` parameter). A form implementing only `get_coordinates_from_atom` will fail when
`msm.get(item, coordinates=True)` is called with the default `element='system'`.

Typical implementation pattern:

```python
def _get_positions_array(item, indices, structure_indices):
    # shared helper — build (n_frames, n_atoms, 3) numpy array
    ...

def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    output = _get_positions_array(item, indices, structure_indices) * puw.unit('nanometer')
    return output

def get_coordinates_from_system(item, structure_indices='all', skip_digestion=False):
    output = _get_positions_array(item, 'all', structure_indices) * puw.unit('nanometer')
    return output
```

---

## Converters that cannot be implemented — do not register in `_convert_to`

If a converter requires data that the form does not store and cannot recover (e.g., a full
topology when only partial atom info is available, or a file path when the object does not
store it), the converter file should exist but raise `NotImplementedMethodError`, and the
target form must be **absent from `_convert_to`**.

Do not add broken converters to `_convert_to` even as stubs — the conversion graph will
include them as valid paths, causing confusing runtime errors rather than clear "no path"
messages.

```python
# Correct pattern for an unimplementable converter:
from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='openmm.GromacsGroFile')
def to_openmm_Topology(item, atom_indices='all', skip_digestion=False):
    # openmm.GromacsGroFile does not expose a full Topology object and does not
    # store the file path, so conversion to openmm.Topology is not supported.
    raise NotImplementedMethodError()

# And in __init__.py — do NOT add 'openmm.Topology': to_openmm_Topology to _convert_to
```

---

## Consecutive-group detection from per-atom residue lists

Several forms (e.g., `openmm.GromacsGroFile`, `mdtraj.GroTrajectoryFile` minimal topology)
expose only per-atom `(residueId, residueName)` lists without a pre-built group index.
The standard pattern for building a group index from such lists is consecutive-change
detection (same as how GRO files work — residue numbering can repeat after 99999):

```python
group_index_per_atom = []
group_ids = []
group_names = []
prev = None
g_idx = -1
for resid, resname in zip(item.residueIds, item.residueNames):
    curr = (resid, resname)
    if curr != prev:
        g_idx += 1
        group_ids.append(str(resid))
        group_names.append(resname)
        prev = curr
    group_index_per_atom.append(g_idx)
```

This correctly handles residue number wrapping in large GRO files, unlike grouping by
unique `(resid, resname)` pairs which would merge non-consecutive residues with the same ID.
