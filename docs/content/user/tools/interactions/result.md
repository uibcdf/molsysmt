(user-tools-interactions-result)=
# Querying interaction results

Build an experimental `molsysmt.Interactions` result from observations that
have local atom and structure indices. By default these equal the source
system's indices; explicit source maps support a selected or reordered domain.
This class stores the
observations; it does not detect interactions or declare covalent bonds.

```python
import molsysmt as msm

records = [
    {
        "structure_index": 0,
        "interaction_type": "hbond",
        "participants": [
            {"role": "donor", "atom_indices": [0]},
            {"role": "hydrogen", "atom_indices": [1]},
            {"role": "acceptor", "atom_indices": [2]},
        ],
        "measurements": {"distance": 0.20},
    },
]
interactions = msm.Interactions.from_records(
    records, n_atoms=3, n_structures=3,
    evaluated_structure_indices=[0, 2],
    method="example", measure_units={"distance": "nm"},
)
```

The distance is in nanometers. Structure 2 was evaluated and has no observed
interactions; structure 1 was not evaluated. The result keeps that difference.
By default, the declared atom search scope is `internal` over all local atoms.
The caller must declare the actual search scope; the class cannot infer from
observed records whether a detector examined all possible participants.

For a search involving one selection and its surroundings, declare the
selection and the complete atom universe examined:

```python
scoped = msm.Interactions.from_records(
    records, n_atoms=4, n_structures=3,
    evaluated_structure_indices=[0, 2], method="example",
    measure_units={"distance": "nm"},
    evaluation_mode="incident", evaluation_atom_indices=[0],
    evaluation_universe_indices=[0, 1, 2],
)
assert scoped.evaluation_scope["universe_indices"].tolist() == [0, 1, 2]
```

`internal(A)` covers relations whose participant atoms all belong to `A`;
`incident(A)` covers relations with at least one participant atom in `A`;
`between(A, B)` covers relations touching each of two disjoint sets. In every
mode, all participants must belong to the declared universe. The declaration
applies uniformly to the listed evaluated structures. Analyses with distinct
scopes belong in separate named results. A structure marked evaluated and
empty is empty only within this declared search scope.

```python
interactions.query(structure_indices=[2, 0, 2]).to_dict()
interactions.query(atom_indices=[0], mode="incident")
interactions.query(atom_indices=[0, 1, 2], mode="internal")
interactions.query(atom_indices=[0], mode="cross")
interactions.between([0, 1], [2], exclusive=True)
```

`incident` means at least one participating atom belongs to the selection;
`internal` requires all participating atoms; `cross` means incident but not
internal. For a ring, every constituent atom participates in these tests.
`between(A, B)` requires at least one atom from each disjoint set. With
`exclusive=True`, every participant atom must belong to `A` or `B`.

Each query returns a lightweight view. `to_dict()` provides typed occurrence
columns, explicit evaluated-structure indices, measurement units, and optional
periodic-image vectors. Use `relation(index)` to inspect the type and roles
referenced by a result's `relation_indices` column.
The aligned `occurrence_indices` column identifies each observation within
this named analysis, even when two observations share a structure and relation.
Filtering and an H5MSM round trip preserve these indices. Extracting or editing
the analysis creates a new set of indices; rebuild saved selections against
the new result. The current API does not expose a persistent revision token.
If any input observation supplies periodic-image vectors, every observation
in that result must supply them; missing vectors are not interpreted as zero
images.
Each vector applies to one participant in relation order. With the three box
vectors as rows in nanometers, add `image_vector @ box` to each constituent
atom's stored coordinate. A positive `[1, 0, 0]` adds the first box vector;
relative geometry uses the first participant as reference. All atoms in a
compound participant receive the same shift. These vectors do not unwrap a
ring split across a periodic boundary.

To transfer the **complete** result through MolSysMT's conversion system,
convert it to `molsysmt.InteractionsDict`:

```python
columns = msm.convert(interactions, to_form="molsysmt.InteractionsDict")
assert msm.get_form(columns) == "molsysmt.InteractionsDict"
restored = msm.convert(columns, to_form="molsysmt.Interactions")
assert restored.query(structure_indices=[2]).n_interactions == 0
```

`InteractionsDict.data` contains versioned NumPy columns for relations,
participants, occurrences, evaluated coverage, evidence, and measurements.
It avoids one Python dictionary per occurrence. It is a typed Python payload,
not JSON data. A query view's `to_dict()` has a different purpose: it reports
selected occurrences and cannot reconstruct the full result.

```python
interactions.save("observations.h5i")
restored = msm.Interactions.load("observations.h5i")
```

The standalone HDF5 file is versioned and separate from H5MSM. `load` reads
the complete result into memory. The current version has no streaming writer,
lazy file-backed queries, incremental add/remove editor, or automatic detector
adapters.

Use `remap()` to extract a complete result into new index spaces. A relation
survives only if all atoms in its participants survive. Repeated structure
indices make distinct output structures, and evaluated structures with no
occurrences stay marked as evaluated.

If a structure changes and its prior observations are stale, use
`invalidate_structures()` to remove its occurrences and mark it unevaluated
while keeping its positional structure index:

```python
invalidated = interactions.invalidate_structures([0])
assert invalidated.query(structure_indices=[0]).to_dict()[
    "evaluated_structure_indices"
].size == 0
```

This returns an independent result and leaves existing query views unchanged.
It copies the packed occurrence arrays, so repeated local edits still need
the planned incremental editor. Re-evaluate the affected structures before
claiming that they have no interactions.

```python
subset = interactions.remap(atom_indices=[0, 1, 2], structure_indices=[2, 0])
assert subset.n_structures == 2
assert subset.query(structure_indices=[0]).n_interactions == 0
assert subset.structure_source_indices.tolist() == [2, 0]
```

`atom_source_indices` and `structure_source_indices` map each local positional
index to its original source index; `source_n_atoms` and
`source_n_structures` define the original index spaces. These are indices, not
element IDs. `remap()` composes the maps and preserves `source_id`. An
appended structure or atom with no counterpart in the original source has map
value `-1`. Query projections do not copy the complete maps on every call; read
them from the result when needed. The typed dictionary and standalone HDF5
file omit identity-map vectors; their readers reconstruct those maps from
the declared axis sizes.

A native `MolSys` can hold several named, full interaction analyses. Their
atom and structure counts must match the system. Its `copy()`, `extract()`,
and `remove()` methods preserve or remap the analyses.

```python
import numpy as np
from molsysmt.native import MolSys

molsys = MolSys(n_atoms=3)
molsys.structures.append(coordinates=np.zeros((3, 3, 3)))
molsys.interactions = {"example": interactions}
selected = molsys.extract(atom_indices=[0, 1, 2], structure_indices=[2, 0])
assert selected.interactions["example"].n_structures == 2
```

Appended structures remain unevaluated by existing analyses, including a
coordinate-only source passed to `msm.append_structures`. Adding atoms to a
system with analyses keeps their previous search universe fixed; the added
atoms are outside it and are not claimed as evaluated. Adding atoms from a
source `MolSys` that already has analyses, or appending structures from such a
source, requires an explicit analysis merge policy and currently raises an
error. H5MSM 0.4 and MolSysDict 0.1
cannot store attached analyses and reject that export; use standalone
`Interactions.save()` until H5MSM 0.5 supports the interaction layer.
