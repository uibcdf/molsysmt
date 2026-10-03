(user-tools-form-h5msm-05)=
# H5MSM 0.5

*Storing modular molecular systems in a versioned HDF5 file.*

H5MSM 0.5 stores `Topology`, `ChemicalStates`, `Structures`, and named
`Interactions` analyses in independent, optional layers. An absent layer stays
absent when the file is read. Associations record when two layers share atom or
structure indices; equal axis lengths alone do not imply that they correspond.

`msm.convert(..., to_form="file:h5msm")` writes 0.5 by default, including
selected atoms and structures. It accepts complete or partial native `MolSys`,
`Structures`, and `ChemicalStates` objects. Attached named `Interactions`
analyses are stored with a `MolSys`. `msm.convert` and `msm.h5msm.read` read 0.5;
`msm.h5msm.read` also accepts 0.3 and 0.4 and warns with a migration
instruction. The older file-form adapters remain available for legacy 0.3/0.4
operations. General 0.5 file queries currently materialize a native `MolSys`;
use `msm.h5msm.read_layers` to load only selected layers.
Native `MolSys` round trips also support structures and attached interactions
without topology or chemical states, provided their atom and structure axes
are explicitly linked in the file.

Each analysis's `software` dictionary retains the versions that produced its
observations. For example, a Buch result records the MolSysMT version used
for calculation. A different writer or reader version does not replace that
value. The optional metadata is stored once per named analysis; older analyses
without it expose an empty dictionary, meaning unknown producer versions.
Frame-scoped `execution_records` preserve how retained and recalculated observations
were produced, including structures evaluated without occurrences. New files use
interaction codec 2 inside H5MSM 0.5. Current MolSysMT also reads codec 1 and
migrates its recorded runtime fields; older builds supporting only codec 1 need
updating to read new analyses. Full-axis native writes traverse resident active
interaction blocks in bounded numeric windows, without packing edited analyses.
This bound covers observation-column writes, not total RAM or other domains;
selection/remapping before writing can still materialize data.
See {ref}`user-tools-interactions-result`.

## Reading legacy units

Legacy H5MSM 0.3/0.4 readers require explicit units. Dataset units are checked against any duplicated group/root declarations; equivalent spellings are accepted, but different scales or dimensions raise `FormatError`. A missing dataset unit may use a coherent explicit group/root declaration. Velocity units may be derived from explicit length/time declarations. B factors require their own unit because legacy writers negotiated it independently of coordinates; missing metadata never implies nm or ps. Public queries and iteration convert the resulting quantities to your active PyUnitWizard policy. Migration to 0.5 validates these units before writing.

## Writing and reading a molecular system

```python
import numpy as np
import molsysmt as msm
from molsysmt.native import MolSys, Structures

molsys = MolSys(n_atoms=2)
molsys.structures = Structures(
    coordinates=msm.pyunitwizard.quantity(np.zeros((2, 2, 3)), "nm")
)
msm.h5msm.write(molsys, "example.h5msm")
restored = msm.h5msm.read("example.h5msm")
assert restored.structures.n_structures == 2
```

The general conversion route writes the same schema:

```python
msm.convert(molsys, to_form="file:h5msm", output_filename="converted.h5msm")
assert msm.convert("converted.h5msm").structures.n_structures == 2
```

`msm.h5msm.write` creates a new file and rejects domain data that the current
0.5 codec cannot encode. Coordinates are stored in nanometers and time in
picoseconds. `msm.h5msm.read` reconstructs a native `MolSys` when the file's
declared index links are representable by that object.
Biological assemblies use typed chain-index and rotation arrays with translations
stored in nanometers. Alternate atom locations use sparse frame and site offsets,
typed values, and explicit nanometer and square-nanometer units. Structure IDs
retain either their integer or string type. H5MSM 0.5 has no
`MolecularMechanics` layer. Writing a system with nonempty mechanics data
raises an error before creating the file. Mechanics persistence is planned
for H5MSM 0.6 after MolSysMT 1.0, once its native parameter model is defined.
The structures-only reader rejects atom subsets when a stored biological
assembly is present, because its chain indices cannot be remapped without a
topology. `msm.convert` likewise rejects writing an atom subset that retains
bioassembly metadata until chain indices can be remapped safely.

Chemical-state atom tables also preserve nullable `n_explicit_hydrogens` (UInt8),
separately from implicit hydrogen counts and indexed H atoms. A missing old field
stays unknown; it is not reconstructed. Readers predating this optional column may
reject files containing it. Current readers accept older files lacking it. Named
cation–π analyses preserve the original method reference as well as producer versions;
ProLIF's SMARTS membership order remains available to reconstruct its ring normal.

## Reading optional layers

`msm.h5msm.read_layers` returns a dictionary. Each requested layer is present
under its schema name; an absent layer has value `None`. For example:

```python
layers = msm.h5msm.read_layers(
    "example.h5msm", layers=["chemical_states", "interactions"]
)
assert layers["chemical_states"] is not None
assert layers["interactions"] is None
```

A file containing only `Structures` is also readable as a partial `MolSys`.
The reader leaves topology and chemical states absent:

```python
msm.h5msm.write_layers("structures_only.h5msm", structures=molsys.structures)
molsys = msm.h5msm.read("structures_only.h5msm")
assert molsys.topology is None
assert molsys.chemical_states is None
assert molsys.structures.n_structures == 2
subset = molsys.extract(atom_indices=[1, 0], structure_indices=[1, 0])
assert subset.structures.coordinates.shape == (2, 2, 3)
```

A frame-only `Structures` layer with time but no atom-aligned arrays likewise
loads without inventing an atom count.

A topology-and-chemistry-only file likewise loads with `molsys.structures is None`.
Use `msm.extract(molsys, selection=[...])` or
`msm.convert(filename, to_form='molsysmt.MolSys', selection=[...])` to retain
selected atoms and remap the present chemistry. With topology, selected atoms
follow sorted source indices. An explicit `structure_indices` selection requires
a declared structure-index domain; topology and chemical states alone do not
declare one. Save the selected native system through the public 0.5 conversion;
its absent Structures layer stays absent.

Topology, chemical states and named interactions can round-trip together while
`molsys.structures is None`. Analyses supply the structure-index domain, including
evaluated structures with zero occurrences. Atom and nonconsecutive structure
selections remap the analyses without fabricating coordinates or a periodic box.
Chemical states are not automatically assigned to those structures.

The native writer declares chemistry-to-topology and analysis-to-topology identity
atom links. When several analyses share the structure axis, it also declares
identity links connecting them. The native reader accepts any connected graph of
these identity structure links; matching counts alone are insufficient. Independent
`write_layers` callers must supply these associations to compose the layers as
one native system. Missing or nonidentity links raise an error; `read_layers`
remains available for independent domains. Source labels and maps are provenance,
not proof of correspondence. A named empty analysis retains its axes and coverage;
a present-empty interaction layer requires `read_layers`.

`msm.h5msm.write_layers` accepts independent native domains and explicit
associations. It can also store an interaction analysis without a topology or
coordinate layer. This is useful when an analysis refers to source atom and
structure index spaces maintained elsewhere. Load such an interaction-only
file as a partial `MolSys`, or use `read_layers` to preserve the absent versus
present-empty layer distinction:

```python
analysis = msm.Interactions.from_records(
    [], n_atoms=2, n_structures=3,
    evaluated_structure_indices=[0], method="example",
)
msm.h5msm.write_layers(
    "interactions_only.h5msm", interactions={"example": analysis}
)
loaded = msm.h5msm.read_layers(
    "interactions_only.h5msm", layers="interactions",
    analysis_names="example",
)["interactions"]["example"]
assert loaded.query(structure_indices=[0]).to_dict()[
    "evaluated_structure_indices"
].tolist() == [0]
```

`msm.h5msm.read("interactions_only.h5msm")` returns a partial `MolSys`
whose atom and structure index domains come from the named analysis. Its
`topology`, `chemical_states`, and `structures` are absent. `extract` accepts
explicit atom and structure indices, including nonconsecutive and repeated
structure indices. A present-empty interaction layer has no index domains;
read that layer with `read_layers`.

## Migrating a 0.3 or 0.4 file

```python
msm.h5msm.migrate_to_05("legacy.h5msm", "modular.h5msm")
```

The helper reads a complete 0.3 or 0.4 molecular system, writes a separate
0.5 file, and records the source version in `migrated_from_version`. It leaves
the source unchanged. Reading a legacy file raises a visible
`LegacyH5MSMWarning` that names this helper; legacy reading remains supported.
The narrower `msm.h5msm.migrate_04_to_05` accepts only 0.4 input.
Migration rejects a zero-atom legacy scaffold because that scaffold
does not establish which optional 0.5 layers were semantically present. It
also rejects fields that the 0.5 writer cannot yet represent without loss.

## Appending structures

`msm.h5msm.append_structures` can add complete rows to a 0.5 file without
topology or interactions. If the file declares a structure-to-state mapping,
pass one chemical-state index for each new structure with
`structure_state_indices`; use `-1` for an unknown state. The append path
validates axes, fields, and associations before resizing datasets. A write
interrupted by a crash is not yet transactional.
Stored biological assemblies are preserved; incoming assembly metadata, if
supplied, must match the stored assembly after unit conversion.
Sparse alternate-location data can grow with the structural series when both
the stored file and incoming block provide that field. A one-sided field is
rejected before any dataset is resized.

:::{seealso}
The {ref}`molecular system model <user-foundations-molecular-system-definition>`
explains the native domains. See {doc}`file_h5msm` for legacy file operations.
:::
