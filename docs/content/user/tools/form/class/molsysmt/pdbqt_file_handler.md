(Tutorial_Form_PDBQTFileHandler)=
# PDBQTFileHandler

*Reusing a validated PDBQT document and reading selected structure blocks.*

- **Technical Form Name:** `molsysmt.PDBQTFileHandler`
- **Form Type:** `class`
- **Class:** {class}`molsysmt.native.PDBQTFileHandler`

:::{versionadded} 1.0.0
:::

The experimental handler owns a read-only **resident text snapshot**. It validates
all model bodies on opening, retains compact structure ranges and one reference
record, and builds coordinate arrays only for the requested structures. File
changes after opening do not change that snapshot. Copies share immutable text
and indexes but have independent lifetimes and mutable projection caches.

This initial handler still loads a file's text into RAM. Disk-backed indexing,
first-block latency and large-file memory benchmarks remain
[uibcdf/molsysmt#434](https://github.com/uibcdf/molsysmt/issues/434). A structure
iterator avoids a complete coordinate trajectory; it does not make resident
source text disappear.

## Opening and querying a document

This one-atom literal carries explicit PDBQT data, not a complete chemical graph.
The two MODEL labels below are string IDs; their structure indices are 0 and 1.

```python
import molsysmt as msm
import numpy as np
from molsysmt.native import PDBQTFileHandler

body = ('ATOM     17   C1 LIG A   7       1.000   2.000   3.000'
        '  0.50 12.00     0.125 C\nEND\n')
text = ('pdbqt_text:REMARK opaque source evidence\n'
        'MODEL 17\n' + body + 'ENDMDL\n'
        'MODEL 5\n' + body.replace('   1.000', '  11.000', 1) + 'ENDMDL\n')
with PDBQTFileHandler(text) as handler:
    assert msm.get_form(handler) == 'molsysmt.PDBQTFileHandler'
    assert handler.n_atoms == 1 and handler.n_structures == 2
    selected = handler.get(element='atom', coordinates=True,
                           structure_indices=[1, 0, 1])
    assert selected.shape == (3, 1, 3)
    np.testing.assert_allclose(msm.pyunitwizard.get_value(selected, to_unit='nm')[:, 0, 0], [1.1, 0.1, 1.1])
    clone = handler.copy()
assert handler.closed and not clone.closed
clone.close()
```

`get()` and `info()` use the normal public query conventions. Source atom IDs
remain strings. Coordinates cross the explicit angstrom boundary through
PyUnitWizard; default output lengths are nm and configured length units are
honored. B factors carry area units. Partial charges are stored values in
units of elementary charge; AutoDock labels remain `atom_ff_type`, separate
from chemical element symbols in `atom_type`.

## Iterating through the form classes

The three adapters expose `StructuresIterator` in their own `iterators.py`:
`msm.form.molsysmt_PDBQTFileHandler`, `msm.form.file_pdbqt` and
`msm.form.string_pdbqt_text`. They share a structural kernel and require no
change to the principal `msm.Iterator`.

```python
with PDBQTFileHandler(text) as handler:
    iterator = msm.form.molsysmt_PDBQTFileHandler.StructuresIterator(
        handler, structure_indices=[1, 0, 1], chunk=2,
        coordinates=True, structure_index=True, output_type='dictionary')
    blocks = list(iterator)
    assert [block['coordinates'].shape for block in blocks] == [(2, 1, 3), (1, 1, 3)]
    assert [block['structure_index'].tolist() for block in blocks] == [[1, 0], [1]]
    assert not handler.closed
    assert [chunk.shape for chunk in msm.Iterator(handler, coordinates=True, chunk=1)] == [(1, 1, 3), (1, 1, 3)]
```

Each coordinate block retains the shape `(n_structures, n_atoms, 3)`, including
single-structure blocks. Start/stop/step apply to the requested index sequence;
order and repetitions are preserved. An empty structure sequence yields no
blocks. Explicit atom selections are supported. Multiple requested structural
attributes share one model read per block.

A handler iterator borrows its input and never closes the caller's handler.
File/text iterators create an owned handler, released on exhaustion, failure,
explicit `close()` or their own context exit. For early termination through
`msm.Iterator`, keep an explicit handler context as above: that owner releases
the snapshot when the enclosing context ends.

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as directory:
    path = Path(directory) / 'poses.pdbqt'
    path.write_text(text[len('pdbqt_text:'):])
    with msm.form.file_pdbqt.StructuresIterator(
            path, chunk=1, coordinates=True) as iterator:
        assert next(iterator).shape == (1, 1, 3)
    assert iterator.closed
```

## Preserving document evidence

The handler retains ROOT/BRANCH/TORSDOF, opaque remarks, MODEL labels and source
text. `get_torsion_tree(structure_index=0)` returns detached declared evidence;
no complete connectivity, aromaticity or formal charges are inferred.

Full identity conversions to `file:pdbqt` or `string:pdbqt_text` preserve the
original text. Serialization of selected structures requires nonempty unique
indices because duplicate MODEL labels would be invalid; getters and iterators
can still repeat structures. Atom subsets of a ligand tree require an explicitly
remapped tree through the existing native writer.

Converting a ligand into MolSys requires `discard_torsion_tree=True`, since
MolSys does not store that format-specific tree. Reduced Topology, Structures
and MolecularMechanics projections preserve their own supported data and omit
the tree. For structure-only molecular-system iteration, choose
`output_form='molsysmt.Structures'`. A default MolSys conversion retains its
explicit tree-loss boundary.

To reconstruct returned poses on a known prepared graph, use
`msm.form.file_pdbqt.read_poses()`, `msm.form.string_pdbqt_text.read_poses()` or
`handler.read_poses()` with the known source and completed export map. Ordinary
PDBQT conversion preserves a partial graph; mapped reading supplies the known
chemistry and still validates every pose before returning a selection.

:::{seealso}
:class: dropdown

- {ref}`Tutorial_Read_PDBQT_Poses`
- {ref}`cookbook-native-pdbqt`
- {ref}`Tutorial_Iterator`
:::
