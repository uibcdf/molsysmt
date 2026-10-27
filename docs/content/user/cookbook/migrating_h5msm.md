(cookbook-migrating-h5msm)=
# Migrating an H5MSM file

*Moving a legacy molecular system into the modular H5MSM 0.5 schema.*

This recipe keeps a 0.3 or 0.4 source file and writes a separate 0.5 file. The
helper validates that the native system reconstructed from the source can be encoded
without dropping an unsupported field.

## Translating the file

```python
import molsysmt as msm

msm.h5msm.migrate_to_05("trajectory_04.h5msm", "trajectory_05.h5msm")
molsys = msm.h5msm.read("trajectory_05.h5msm")
print(molsys.structures.n_structures)
```

You can also load the new file with `msm.convert("trajectory_05.h5msm")`.
One file converted to one `MolSys` gives you a fresh independent resident object
without a second eager snapshot by default. Editing it does not modify the
saved file; use an explicit write to persist your changes. Loading a subset
through this conversion can still require materializing the file first. See
{ref}`user-tools-form-h5msm-05` for layer selection and copy boundaries.

After migration, use these 0.5 readers rather than `H5MSMFileHandler`.
That handler supports only 0.3 and 0.4; requesting it for the migrated file
raises `FormatError` with resident-load and selected-layer alternatives.

## Resolving unit errors

Legacy H5MSM 0.3/0.4 readers require explicit units. Dataset units are checked against any duplicated group/root declarations; equivalent spellings are accepted, but different scales or dimensions raise `FormatError`. A missing dataset unit may use a coherent explicit group/root declaration. Velocity units may be derived from explicit length/time declarations. B factors require their own unit because legacy writers negotiated it independently of coordinates; missing metadata never implies nm or ps. Public queries and iteration convert the resulting quantities to your active PyUnitWizard policy. Migration to 0.5 validates these units before writing.

If migration rejects a file, recover the correct declarations from the original
writer or its documented unit contract. Recreate the file with those units;
MolSysMT cannot infer a missing unit from the numerical values.

## Preserving state associations

Chemical states and structures are independent populations. One structure may
refer to one of several stored states; writing and reloading the system retains
the whole state inventory, its reference and the declared association. A map
`[0]` into two states remains explicit, while a full index-for-index map between
equal populations can use compact identity storage. Unknown associations remain
unknown. See {ref}`user-tools-form-h5msm-05` for an executable round trip.

An invalid identity marker across unequal populations is rejected. If an older
writer produced such a file, regenerate it from the original native source with
the corrected writer; the reader does not guess missing correspondence.

## Inspecting independent layers

Read only the domains needed for the next step:

```python
payload = msm.h5msm.read_layers(
    "trajectory_05.h5msm", layers=["chemical_states", "interactions"]
)
states = payload["chemical_states"]
analyses = payload["interactions"]
```

An absent layer has value `None`. An interaction layer can also contain an
analysis whose evaluated structures have zero observed interactions.

If a 0.5 file contains topology and chemical states without structures, load it
as a native `MolSys` before selecting atoms:

```python
molsys = msm.h5msm.read("topology_chemistry_05.h5msm")
subset = msm.extract(molsys, selection=[0])
assert subset.structures is None
msm.convert(subset, to_form="file:h5msm", output_filename="selected_05.h5msm")
```

The output retains the selected chemistry without fabricating coordinates.
Do not select structure indices unless a present domain declares that axis.

## Consolidating complementary files

If your matching topology/chemistry and Structures domains are stored separately,
declare their positional correspondence by supplying a list. For example, for
files containing at least two atoms and three corresponding structures:

```python
molsys = msm.convert(
    ["matching_topology_chemistry.h5msm", "matching_structures.h5msm"],
    selection=[0, 1], structure_indices=[2, 0],
)
assert msm.get(molsys, n_atoms=True, n_structures=True) == [2, 2]
msm.convert(molsys, to_form="file:h5msm", output_filename="consolidated_05.h5msm")
```

Compose full domains first: selecting each partial file independently can ask
the topology-only input for a nonexistent structure axis. Counts are checked
before selection, and each domain must have one provider. You remain responsible
for the declared index correspondence. This example assumes the selected atoms
are not coupled to stored assembly metadata requiring additional chain remapping.

(cookbook-h5msm-assembly-operations)=
## Saving assembly operations

Constructing assembly metadata normally produces operation arrays that can be
saved directly. This self-contained example stores one identity operation with
a translation of 1 nm along x; no topology is needed to preserve the metadata:

```python
import numpy as np
import molsysmt as msm
from molsysmt.native import Structures

puw = msm.pyunitwizard
structures = Structures(bioassembly={
    "1": {
        "chain_indices": [0],
        "rotations": [np.eye(3)],
        "translations": puw.quantity([[10.0, 0.0, 0.0]], "angstrom"),
    },
})
msm.h5msm.write_layers("assembly_05.h5msm", structures=structures)
molsys = msm.convert("assembly_05.h5msm")
operation = molsys.structures.bioassembly["1"]
assert operation["rotations"].shape == (1, 3, 3)
np.testing.assert_allclose(
    puw.get_value(operation["translations"], to_unit="nm"), [[1.0, 0.0, 0.0]]
)
```

`chain_indices=[0]` declares one chain set shared by the operations. A nested
sequence supplies one set per operation. Reconstructing with
`Structures(bioassembly=structures.bioassembly)` keeps the operation shapes
and does not modify the input. Building coordinates with
{func}`molsysmt.build.make_bioassembly` additionally requires a system with
compatible topology and coordinates. That builder accepts a common chain set
or identical sets repeated per operation; heterogeneous sets remain unsupported.

For a complete ensemble with topology, coordinates, at least three structures
and an assembly named `"1"`, use
`msm.build.make_bioassembly(molsys, bioassembly="1", structure_indices=[2, 0, 2])`
to build those three structures in that order. Every operation acts on each
selected structure; operation copies are combined along the atom axis. Structure
labels and times follow the selected source structures. Omitting
`structure_indices` selects structure 0; `"all"` selects the complete axis.

You can supply the complete H5MSM path directly instead of `molsys`; the builder
loads a native in-memory system and leaves the source file unchanged. Its default
result for a file input is a `MolSys`. This resident load may materialize the
file before selecting structures; it is not a bounded disk-query interface.

## Keeping analyses without coordinates

Named analyses can declare a structure-index domain even when coordinates are
absent. For example, starting from the topology-and-chemistry-only system above:

```python
analysis = msm.Interactions.from_records(
    [], n_atoms=msm.get(molsys, n_atoms=True), n_structures=3,
    evaluated_structure_indices=[0, 2], method="imported_example",
)
molsys.interactions = {**molsys.interactions, "example": analysis}
msm.convert(
    molsys, to_form="file:h5msm", output_filename="analyses_without_coordinates.h5msm"
)
restored = msm.h5msm.read("analyses_without_coordinates.h5msm")
assert restored.structures is None
columns = restored.interactions["example"].query(
    structure_indices=[2, 1, 0]
).to_dict()
assert columns["evaluated_structure_indices"].tolist() == [2, 0]
assert columns["occurrence_indices"].size == 0
```

Structures 0 and 2 were evaluated without observations; structure 1 was not
evaluated. Attaching an independently loaded analysis declares its correspondence
to the current atom indices. Confirm that correspondence before attachment.
The native writer records the declared axis links and retains original producer
versions. Displaying these observations still requires compatible coordinates.

:::{seealso}
See {doc}`H5MSM 0.5 <../tools/form/file/h5msm_05>` for the schema API and
{ref}`the molecular system model <user-foundations-molecular-system-definition>`
for domain ownership.
:::

When preparing a downstream descriptor table after loading a molecular system,
`get_surface_area(definition='collantes')` returns an area quantity using the
provisional Å² convention, then PyUnitWizard standardization. Extract explicit
Å² values to retain the historical model input scale. Original-paper verification
is still pending under #473; unit typing does not certify conformational SASA.
See {ref}`Tutorial_Get_surface_area`.
