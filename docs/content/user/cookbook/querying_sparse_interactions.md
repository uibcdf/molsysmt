(cookbook-querying-sparse-interactions)=
# Comparing sparse interactions across structures

Use this recipe when a detector or another source has already produced
chemically classified observations. It compares selected structures and atom
sets without building a dense atom-pair matrix. The numbers below are synthetic
examples, not scientific detections.

```python
import molsysmt as msm

records = [
    {"structure_index": 0, "interaction_type": "hbond",
     "participants": [
         {"role": "donor", "atom_indices": [0]},
         {"role": "hydrogen", "atom_indices": [1]},
         {"role": "acceptor", "atom_indices": [2]},
     ], "measurements": {"distance": 0.20}},
    {"structure_index": 3, "interaction_type": "pi_pi",
     "participants": [
         {"role": "ring", "atom_indices": [3, 4, 5]},
         {"role": "ring", "atom_indices": [6, 7, 8]},
     ], "measurements": {"distance": 0.36}},
]
interactions = msm.Interactions.from_records(
    records, n_atoms=9, n_structures=5,
    evaluated_structure_indices=[0, 1, 3],
    method="example", measure_units={"distance": "nm"},
)
```

The selected structures may be nonconsecutive. Repeating structure 3 does not
duplicate its occurrence; structure 1 remains present in coverage with zero
occurrences. Structure 2 was never evaluated.

Keep these selections as integer indices. A fractional value such as `3.5`
raises instead of selecting structure 3. Leave `skip_digestion` at its default
`False` when accepting input from a user or a file; it is a trusted-delegation
option, not a way to repair malformed data. See
{ref}`Querying interaction results <user-tools-interactions-result>`.

```python
view = interactions.query(structure_indices=[3, 1, 0, 3])
columns = view.to_dict()
assert columns["structure_indices"].tolist() == [3, 0]
assert columns["occurrence_indices"].tolist() == [1, 0]
assert columns["evaluated_structure_indices"].tolist() == [3, 1, 0]

ring_between = interactions.between_selections([3, 4, 5], [6, 7, 8], exclusive=True)
assert ring_between.n_interactions == 1
assert interactions.query(atom_indices=[3], mode="across_selection_boundary").n_interactions == 1

columns = msm.convert(interactions, to_form="molsysmt.InteractionsDict")
reconstructed = msm.convert(columns, to_form="molsysmt.Interactions")
assert reconstructed.query(structure_indices=[1]).n_interactions == 0
```

For an inspector, keep `view` and materialize only the rows being displayed:

```python
page = view.to_page(limit=1)
assert page["occurrence_indices"].tolist() == [1]
assert page["participant_atoms"].tolist() == [3, 4, 5, 6, 7, 8]
assert page["measure_units"]["distance"] == "nm"
next_page = view.to_page(offset=page["next_offset"], limit=1)
assert next_page["occurrence_indices"].tolist() == [0]
assert next_page["next_offset"] is None
```

The page retains complete-analysis occurrence indices, while its offset counts
rows in the query's order. Count and evaluated coverage remain available even
for empty pages. A participant-atom budget guards large compound groups before
copying them. See {ref}`Inspecting bounded pages <user-tools-interactions-pages>`
for the compact relation catalog and the separate query/index memory costs.

Keep an independent analysis when exploring a different invalidation decision:

```python
from copy import copy

independent = copy(interactions)
independent.parameters["purpose"] = "alternative coverage"
alternative = independent.invalidate_structures([3])
assert alternative.evaluated_structure_indices.tolist() == [0, 1]
assert interactions.evaluated_structure_indices.tolist() == [0, 1, 3]
assert "purpose" not in interactions.parameters
```

The copies share immutable numeric bytes, with separate array headers and
mutable metadata. No detector runs and no sparse columns are packed just to
copy the result. For enclosing graphs, copied raw arrays and query-cache costs,
see {ref}`Copying analyses <user-tools-interactions-copying>`. For a complete
system, use the {ref}`MolSys copy contract <user-foundations-molsys-copying>`.

For interchange, copy the typed payload without decoding its columns:

```python
payload = msm.convert(interactions, to_form="molsysmt.InteractionsDict")
payload_copy = msm.copy(payload)
assert payload_copy is not payload
assert payload_copy.data is not payload.data
from_payload = msm.convert(payload_copy, to_form="molsysmt.Interactions")
assert from_payload.query(structure_indices=[3]).n_interactions == 1
```

`payload.copy()` and Python `copy.copy(payload)` also own independent mutable
payload data; a wrapper copy does not validate its schema. Direct Python copies
of plain dictionary forms retain Python's shallow semantics. See
{ref}`Native Copying <user-foundations-resident-copying>`.

Attach the complete result to a native molecular system to keep its atom and
structure index spaces together. H5MSM 0.5 stores the named analysis alongside
the structures. The same query works after loading it:

```python
import numpy as np
from pathlib import Path
from tempfile import TemporaryDirectory
from molsysmt.native import MolSys, Structures

molsys = MolSys(n_atoms=9)
molsys.structures = Structures(
    coordinates=msm.pyunitwizard.quantity(np.zeros((5, 9, 3)), "nm")
)
molsys.interactions = {"example": interactions}

with TemporaryDirectory() as directory:
    filename = str(Path(directory) / "observations.h5msm")
    msm.h5msm.write(molsys, filename)
    loaded = msm.h5msm.read(filename)
    stored = loaded.interactions["example"]
    assert stored.query(structure_indices=[3, 1, 0, 3]).to_dict()[
        "structure_indices"
    ].tolist() == [3, 0]
    assert stored.query(structure_indices=[1]).to_dict()[
        "evaluated_structure_indices"
    ].tolist() == [1]
    assert stored.query(structure_indices=[2]).to_dict()[
        "evaluated_structure_indices"
    ].size == 0

    analysis_file = str(Path(directory) / "analysis_only.h5msm")
    msm.h5msm.write_layers(
        analysis_file, interactions={"example": interactions}
    )
    partial = msm.h5msm.read(analysis_file)
    assert partial.topology is None
    assert partial.structures is None
    subset = partial.extract(
        atom_indices=[2, 0, 1], structure_indices=[3, 0]
    )
    assert subset.interactions["example"].query(
        structure_indices=[1]
    ).n_interactions == 1
```

`read_layers(filename, layers="interactions")` can load the interaction layer
without the other layers. Both `read` and `read_layers` currently materialize
the selected interaction result in memory; they are not file-backed query
objects.

## Editing a structure

An atom that had no previous interactions can acquire one after moving. Reset
the evaluated status of the affected frames before a new calculation. Native
`MolSys` coordinate and box setters do this for all attached named analyses,
even for a frame previously evaluated with no observations:

```python
molsys_edited = molsys.copy(deep=False)
previous_view = molsys_edited.interactions["example"].query(structure_indices=[3])
msm.set(molsys_edited, selection=[0], structure_indices=[1],
        coordinates=msm.pyunitwizard.quantity([[[0.1, 0.0, 0.0]]], "nm"))
current = molsys_edited.interactions["example"]
assert current.query(structure_indices=[1]).n_interactions == 0
assert current.query(structure_indices=[1]).to_dict()[
    "evaluated_structure_indices"
].size == 0  # It now needs a calculation.
assert current.query(structure_indices=[3]).n_interactions == 1
assert previous_view.n_interactions == 1

with TemporaryDirectory() as directory:
    filename = str(Path(directory) / "edited.h5msm")
    msm.h5msm.write(molsys_edited, filename)
    restored = msm.h5msm.read(filename).interactions["example"]
    assert restored.evaluated_structure_indices.tolist() == [0, 3]
    assert restored.query(structure_indices=[1]).to_dict()[
        "evaluated_structure_indices"
    ].size == 0
```

Now simulate a recalculation of frame 1 with one synthetic hydrogen bond:

```python
fresh_record = {**records[0], "structure_index": 1,
                "measurements": {"distance": 0.24}}
fresh = msm.Interactions.from_records(
    [fresh_record], n_atoms=9, n_structures=5,
    evaluated_structure_indices=[1], method="example",
    measure_units={"distance": "nm"},
)
updated = current.replace_structures(fresh)
molsys_edited.interactions = {"example": updated}
assert updated.query(structure_indices=[3, 1, 0]).to_dict()[
    "occurrence_indices"
].tolist() == [2, 1, 0]
assert updated.query(atom_indices=[2]).n_interactions == 2
assert previous_view.n_interactions == 1
compacted = updated.compact()
assert compacted.query(structure_indices=[3, 1, 0]).to_dict()[
    "occurrence_indices"
].tolist() == [2, 1, 0]
molsys_edited.interactions = {"example": compacted}
with TemporaryDirectory() as directory:
    filename = str(Path(directory) / "recalculated.h5msm")
    msm.convert(molsys_edited, to_form="file:h5msm", output_filename=filename)
    restored = msm.convert(filename, to_form="molsysmt.MolSys").interactions["example"]
    assert restored.query(structure_indices=[3, 1, 0]).to_dict()[
        "occurrence_indices"
    ].tolist() == [2, 1, 0]
```

`replace_structures` replaces every frame evaluated by the new result, including
frames recalculated with zero observations. It checks axes, source maps, method,
scientific parameters, producer versions, units and atom scope. Execution mode
and block counts may differ; `restored.execution_records` preserves the producing
calculation for each evaluated frame, including empty ones. Recalculation must retain
the original system axes and scope; an extracted frame has different local axes.
The unchanged observation blocks are shared. New occurrence handles belong to
the updated version; old views remain snapshots of the earlier result.
The recipe explicitly attaches `updated.compact()` to release references to
retired row blocks while preserving the updated handles. Release `updated`,
`current` and any older views too if you want their buffers reclaimed. Building
the compacted result requires memory for new columns; unused relation definitions
stay in its catalog. Compaction is optional before saving.

Frame invalidation shares read-only columns and does not recalculate anything.
Selected queries and HDF5 saving avoid packing the complete surviving analysis.
Saving traverses active blocks in numeric windows and preserves any existing
complete-column cache. Typed dictionary export, pickle and remapping may still
materialize all active rows temporarily. Earlier snapshots can keep shared storage alive.
For attached geometry setters, other direct writes, and recalculation/attachment
rules, see {ref}`Changing coordinates <user-tools-interactions-coordinate-edits>`.

Attaching a separately loaded analysis declares that its local atom and
structure indices correspond to the target system. You are responsible for
that correspondence; matching axis sizes and a `source_id` label do not prove
it. Align reordered axes before attachment using a supported remap or
extraction. The {ref}`association guide <user-tools-interactions-association>`
explains the current checks and limits. The writer is responsible for the
correspondence of system and analyses stored together in H5MSM.

Inspect `stored.software` or a query projection's `"software"` field to
recover the versions that produced the observations. MolSysMT's hydrogen-bond
and disulfide adapters capture their version during calculation; H5MSM preserves
it even when saved or loaded by another version. `{}` means the producer
version was not recorded, as in these manually constructed synthetic records.

Detector-produced analyses also retain a compact bibliography in
`analysis.parameters["attribution"]`. H5MSM preserves the original references
and producer versions independently of whether Ackredit is installed when
reading the file. Loading does not credit a new calculation. The synthetic
records in this recipe have no attribution because no scientific detector was
run. See {ref}`Methods and attribution <user-tools-interactions-attribution>`
for method/profile names and optional workflow reporting.
If optional tracking fails, the scientific result and detached bibliography remain
available, including under warnings-as-errors. A failed attribution diagnostic
uses a fallback log carrying its signal code and both error reasons. Inspect that
diagnostic rather than assuming session tracking succeeded. Scientific errors and
unrelated warnings retain their usual behavior.

The synthetic records above show the container without requiring a detector.
For a molecular system with eligible cysteine sulfur atoms, the disulfide
candidate detector can instead return an `Interactions` result with
`output_type="molsysmt.Interactions"`. Attach that result under a name in
`molsys.interactions` before writing H5MSM 0.5. Its geometric S–S candidates
do not assert that a covalent bond exists in the chemical state.

`msm.interactions.hbonds.get_buch_hbonds(...,
output_type="molsysmt.Interactions")` supplies the same workflow for Buch
hydrogen bonds, with donor, hydrogen, and acceptor roles and H-A distances in
nm. Coverage includes evaluated frames with no bonds. A covalently attached
donor hydrogen remains a participant even if the atom selection named only
its donor. The optional result supports automatic roles in one selection or
two disjoint participant universes; it does not yet stream large trajectories.

`msm.interactions.hbonds.get_luzard_chandler_hbonds(...,
output_type="molsysmt.Interactions")` returns the same sparse result contract,
with D-A distance in nm and H-D-A angle in rad. Both D-H and D-A periodic
images use the donor as reference and reproduce the angular calculation.
It preserves empty evaluated frames and the calculation-time software version.

Use {doc}`the interaction result guide <../tools/interactions/result>` for
role, unit, and evaluated atom-scope conventions. The example uses the default
`internal` scope over all nine atoms. For a detector restricted to one selection,
pass its actual `evaluation_mode`, selected atoms, and searched atom universe
to `from_records`. A complete result can be attached to `MolSys`
under an analysis name; extraction remaps its atom and structure indices.
Explore a standalone geometry variant with shared protected coordinate/box
storage, before deciding whether to calculate a new analysis:

```python
variant = molsys.structures.copy(deep=False)
variant.set_coordinates(indices=[3], structure_indices=[3],
    value=msm.pyunitwizard.quantity([[[1., 0., 0.]]], "nm"))
assert msm.pyunitwizard.get_value(
    molsys.structures.get_coordinates(indices=[3], structure_indices=[3]),
    to_unit="nm",
).tolist() == [[[0., 0., 0.]]]
assert msm.pyunitwizard.get_value(
    variant.get_coordinates(indices=[3], structure_indices=[3]),
    to_unit="nm",
).tolist() == [[[1., 0., 0.]]]
```

The variant owns its geometry edits and metadata. Selected getters return
editable output arrays; coordinate/box storage itself is protected. This
standalone `Structures` copy carries no named analyses or topology. Use a
matching molecular system and recalculate appropriate evidence before attaching
analyses to changed geometry. To carry the entire system instead, use
`molsys.copy(deep=False)` and edit through `msm.set` as above: only the copy's
affected structures become unevaluated. `msm.copy(molsys)` uses eager geometry
allocation. See {ref}`MolSys copies <user-foundations-molsys-copying>` and
{ref}`Structures copies <user-foundations-structures-copying>`.

Geometry edits through `msm.set(molsys, coordinates=..., structure_indices=[...])`,
`molsys.structures.set_coordinates(...)` or their box setters automatically
replace affected named results with snapshots
whose edited frames are unevaluated. They remove old observations and preserve
untouched frames and previous query views. This is conservative per-structure
invalidation, even when only one atom moved; it does not calculate new results.
Full `coordinates`/`box` assignments on the attached domain do the same.
For raw/private storage writes, whole-domain replacement or other unobserved
edits, explicitly call `analysis.invalidate_structures([structure_index])` and
replace each affected named result before re-evaluating. Use the owning system's
append/add tools when changing axes. An unevaluated structure differs from one
evaluated with zero observations. A standalone `Structures.copy()` has no owner;
a `MolSys` copy's structure setters invalidate only the copy's analyses.

The synthetic system above demonstrates the automatic boundary:

```python
old_view = molsys.interactions['example'].query(structure_indices=[0])
msm.set(molsys, selection=[2], structure_indices=[0],
        coordinates=msm.pyunitwizard.quantity([[[1, 0, 0]]], 'nm'))
updated = molsys.interactions['example']
assert updated.query(structure_indices=[0]).to_dict()[
    'evaluated_structure_indices'
].size == 0
assert updated.query(structure_indices=[1]).to_dict()[
    'evaluated_structure_indices'
].tolist() == [1]
assert updated.query(structure_indices=[3]).n_interactions == 1
assert old_view.n_interactions == 1
```

Chemical-state assignments have a wider scope. Changing a formal charge or
aromaticity through `msm.set(molsys, ...)` invalidates every covered structure
in every named analysis. Replacing `molsys.chemical_states` does the same.
The library does not infer which methods depend on the edited assignment.
Changing `structure_chemical_state_index` instead invalidates only the selected
structures. Bond identifiers and empty selections preserve analyses.

The records in this recipe remain synthetic; this charge edit illustrates
invalidation without assigning a scientific interpretation to those records:

```python
previous_ring_view = molsys.interactions['example'].query(structure_indices=[3])
msm.set(molsys, element='atom', selection=[0], formal_charge=0)
assert molsys.interactions['example'].evaluated_structure_indices.size == 0
assert molsys.interactions['example'].n_interactions == 0
assert previous_ring_view.n_interactions == 1
```

Chemical-state setters invoked on `molsys.topology` also notify the owner, as
do its native bond addition/removal and full `bonds` replacement. A standalone
topology copy is detached. If your client subclasses `MolSys`, `Topology` or
`ChemicalStates`, it can inherit the native constructor and use ordinary validated
count arguments. Copying preserves supported subclass attributes without calling
that constructor again; the subclass still needs its own form integration if it
introduces a distinct molecular-system form. Owner detachment also works when
the link is stored in a subclass slot. Slots declared by different classes
retain their separate values and aliases. Repeated references to canonical
tables follow the shared deepcopy memo; arbitrary mutable table-cell data and
pandas metadata retain pandas' own copy rules. Appending a state through
`molsys.chemical_states.append_state()` also makes every analysis unevaluated.
Explicit structure-to-state assignments stay unchanged; with multiple states,
structures without an explicit assignment resolve to unknown. Existing state
records and coordinates are not copied. Appending preparation history preserves
analyses because it only archives evidence. Other private collection changes,
whole topology replacement, mechanics changes and raw table/array writes need
explicit owner invalidation. Use
`analysis.invalidate_structures(...)` to replace each affected named result
before calculating new evidence.

An observed proximity is separate from the chemical state's covalent graph.
For example, explicitly adding a covalent bond changes the `ChemicalStates`
domain and the compatible `Topology.bonds` view together:

```python
from molsysmt.native import MolSys

molsys = MolSys(n_atoms=2)
molsys.topology.add_bonds([[0, 1]])
assert molsys.chemical_states.get_bonds() is molsys.topology.bonds
```

## Consuming results in MolSysViewer

MolSysViewer consumes named `Interactions` analyses through its native backend
and `view.interactions` API; no MolSysMT addon needs to be enabled. Keep an
analysis associated with the correct molecular system and its declared index
maps before displaying it. For persistence, use the documented public H5MSM 0.5
conversion paths. MolSysViewer owns canvas rendering and saved scene/session
state; these are separate from the scientific analysis stored by MolSysMT.
