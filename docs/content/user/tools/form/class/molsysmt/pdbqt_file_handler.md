(Tutorial_Form_PDBQTFileHandler)=
# PDBQTFileHandler

*Reusing a validated PDBQT document and reading selected structure blocks.*

- **Technical Form Name:** `molsysmt.PDBQTFileHandler`
- **Form Type:** `class`
- **Class:** {class}`molsysmt.native.PDBQTFileHandler`

:::{versionadded} 1.0.0
:::

The experimental handler supports two storage modes:

- `storage_mode='resident'` (default) keeps a read-only text snapshot. Later
  file changes do not change that snapshot.
- `storage_mode='indexed'` keeps an uncompressed UTF-8 file open and reads model
  bodies through byte offsets. Changes, replacement or removal of its source
  cause a clear error; reopen the handler to validate a new source.

Both validate every model on opening, keep one parsed reference model, and
create coordinate arrays for requested structures. Copies close independently;
indexed copies share a guarded descriptor until the final owner releases it.
Use context managers for deterministic cleanup. Explicit text remains resident.

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
the owned source when the enclosing context ends.

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

    with PDBQTFileHandler(path, storage_mode='indexed') as handler:
        assert handler.storage_mode == 'indexed'
        chunks = list(msm.Iterator(handler, coordinates=True,
                                  structure_indices=[1, 0, 1], chunk=2))
        assert [value.shape for value in chunks] == [(2, 1, 3), (1, 1, 3)]
        output = Path(directory) / 'copy.pdbqt'
        msm.convert(handler, to_form=output)
        assert output.read_bytes() == path.read_bytes()
```

File-form iterators use indexed storage automatically. Reusing an explicitly
opened indexed handler avoids repeated validation in separate file queries.
Source identity, size and timestamps are checked around reads. This is a source
consistency check, not cryptographic authentication or a filesystem snapshot.
Reading through copied handlers is serialized at their shared descriptor;
closing one copy does not close another. An interrupted owned iterator closes
its source; an iterator borrowing your handler leaves it open.

## Choosing storage for a large ensemble

On 2026-10-23, the synthetic 8,192-structure × 64-atom comparison used a 39.7 MiB
file. Additional measured process peak above a warmed runtime was 79.4 MiB in
resident mode and 5.4 MiB indexed. Opening and full validation took approximately
8.5 s and 9.0 s respectively. Indexed storage saves source-text memory; opening
still examines every model. See the
[benchmark procedure and complete measurements](https://github.com/uibcdf/molsysmt/blob/main/devguide/benchmarking/pdbqt.md)
for fixtures, versions and measurement limits.

The working set also includes indexes, model IDs, the reference model and
preamble metadata; a very large individual model or preamble can dominate it.
Queries and iterators preserve ordered/repeated indices. A request for all
coordinates, a complete text string or a selected native system materializes
that requested result. Selected handler extraction currently produces a resident
document; use block queries or file output for large subsets. The mapped
known-source `read_poses` remains eager in its source metadata.

Full-atom file output streams source ranges; rigid atom subsets are written
one selected model at a time. Temporary destination files are committed only
after successful completion, preserving an existing destination on failure.
Uncompressed files are the supported indexed profile. Compressed random access
and reusable index sidecars require separate designs; no sidecar is created.

## Preserving document evidence

The handler preserves access to ROOT/BRANCH/TORSDOF, opaque remarks, MODEL
labels and source text. `get_torsion_tree(structure_index=0)` returns detached declared evidence;
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
