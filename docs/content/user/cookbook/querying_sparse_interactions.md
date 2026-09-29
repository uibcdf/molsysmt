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

```python
view = interactions.query(structure_indices=[3, 1, 0, 3])
columns = view.to_dict()
assert columns["structure_indices"].tolist() == [3, 0]
assert columns["occurrence_indices"].tolist() == [1, 0]
assert columns["evaluated_structure_indices"].tolist() == [3, 1, 0]

ring_between = interactions.between([3, 4, 5], [6, 7, 8], exclusive=True)
assert ring_between.n_interactions == 1
assert interactions.query(atom_indices=[3], mode="cross").n_interactions == 1

columns = msm.convert(interactions, to_form="molsysmt.InteractionsDict")
reconstructed = msm.convert(columns, to_form="molsysmt.Interactions")
assert reconstructed.query(structure_indices=[1]).n_interactions == 0
```

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

The synthetic records above show the container without requiring a detector.
For a molecular system with eligible cysteine sulfur atoms, the disulfide
candidate detector can instead return an `Interactions` result with
`output_type="molsysmt.Interactions"`. Attach that result under a name in
`molsys.interactions` before writing H5MSM 0.5. Its geometric S–S candidates
do not assert that a covalent bond exists in the chemical state.

Use {doc}`the interaction result guide <../tools/interactions/result>` for
role, unit, and evaluated atom-scope conventions. The example uses the default
`internal` scope over all nine atoms. For a detector restricted to one selection,
pass its actual `evaluation_mode`, selected atoms, and searched atom universe
to `from_records`. A complete result can be attached to `MolSys`
under an analysis name; extraction remaps its atom and structure indices.
After changing coordinates in one structure, call
`interactions.invalidate_structures([structure_index])` and replace the named
result before re-evaluating that structure. The invalidated frame is no longer
marked as evaluated; an evaluated frame with zero observations has a different
meaning.

An observed proximity is separate from the chemical state's covalent graph.
For example, explicitly adding a covalent bond changes the `ChemicalStates`
domain and the compatible `Topology.bonds` view together:

```python
from molsysmt.native import MolSys

molsys = MolSys(n_atoms=2)
molsys.topology.add_bonds([[0, 1]])
assert molsys.chemical_states.get_bonds() is molsys.topology.bonds
```
