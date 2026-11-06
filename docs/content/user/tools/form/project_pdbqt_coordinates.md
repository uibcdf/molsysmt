(Tutorial_Project_Prepared_PDBQT)=
# Projecting coordinates onto prepared PDBQT

*Replacing an explicitly mapped conformation while retaining prepared fields.*

Use this experimental operation when you already have a prepared PDBQT and
want to change its coordinates without retyping, protonating or renormalizing
charges. The source may declare only partial connectivity. You must supply a
complete atom correspondence and new coordinates for every prepared atom,
including hydrogen atoms. A count match never establishes correspondence.

:::{admonition} API documentation
:class: dropdown

- {meth}`molsysmt.native.PDBQTFileHandler.project_coordinates`
- {func}`molsysmt.form.file_pdbqt.project_coordinates`
- {func}`molsysmt.form.string_pdbqt_text.project_coordinates`
:::

:::{versionadded} 1.0.0
:::

## Replacing one conformation

The following two-atom literal is a format example, not a chemically complete
molecule. Its atom serial IDs are 17 and 45; its atom indices are 0 and 1.
The coordinate array below uses the opposite atom order.

```python
import numpy as np
import molsysmt as msm
from molsysmt.native import PDBQTFileHandler

molsys = (
    'pdbqt_text:REMARK VINA RESULT: -7.0 0.0 0.0\n'
    'ATOM     17   C1 LIG B   7       1.000   2.000   3.000  1.00 20.00     0.125 C\n'
    'ATOM     45   O1 LIG B   7       3.000   4.000   5.000  1.00 20.00    -0.250 OA\n'
    'END\n'
)
replacement = msm.pyunitwizard.quantity([[0.7, 0.8, 0.9], [0.4, 0.5, 0.6]], 'nm')
with PDBQTFileHandler(molsys) as handler:
    projection = handler.project_coordinates(
        replacement, atom_correspondence=[[0, 1], [1, 0]],
        discard_remarks=True,
        chemical_state_provenance={'state': 'caller:prepared-state-1'})
projected = projection['molecular_system']
assert projected.removeprefix('pdbqt_text:').splitlines()[0][30:54] == '   4.000   5.000   6.000'
assert 'REMARK' not in projected
assert projection['report']['output_to_coordinate_atom_indices'] == [1, 0]
```

Each map row is `(coordinate_atom_index, source_pdbqt_atom_index)`.
Rows may be reordered, but both columns must cover their entire atom axis
exactly once. Positional indices are plain nonnegative integers; boolean or
quantity-wrapped indices are invalid. Missing-H maps, duplicate atoms,
nonfinite coordinates, bare arrays and non-length units raise an error.
This operation never fills an omitted atom with an old source position.

Only coordinate columns 31--54 change. ATOM/HETATM kinds, serials, names,
group/chain labels, occupancy, B factors, charge precision and AutoDock labels
are retained. ROOT/BRANCH/TORSDOF records retain their meaning. Coordinates
are written as 8.3 angstrom fields; values that do not fit after rounding are
rejected. The report records the maximum absolute rounding error per structure,
with its unit. Application standard units are preserved.

## Choosing structures and metadata policy

`structure_indices=[10, 2]` selects source positions 10 and 2 in that order.
The coordinate array must then contain exactly two structures in the same
order, each with all prepared atoms. Source MODEL labels are preserved as
strings, including declared leading zeros; they are not positional indices.
The supported MODEL labels are ASCII positive-integer tokens.
Serialized selections must be nonempty and unique. An unwrapped source has no
declared structure ID. Getters and iterators retain their separate repeated-index
contract. Source validation always checks every model, including unselected ones.

The default `discard_remarks=False` refuses any source containing REMARK records.
Set `discard_remarks=True` to authorize removing **all** remarks, including old
scores, preparation annotations, inter-model and trailing comments. The report
retains the original input payload hash and optional caller-declared chemical
provenance. That declaration uses finite JSON-compatible values and string keys
at every object level; non-string or colliding keys are rejected. It does not
interpret a stale score as a newly evaluated result or
authenticate a declaration. MODEL wrapper whitespace is canonical; inter-model
blank lines and a terminal document END may be omitted for MODEL output.

## Writing bounded file output

The file adapter opens indexed storage. To avoid repeatedly validating the
same large source, open one indexed handler and reuse it for serial calls.
The source remains unchanged; an output may not alias it through a path,
symlink or hard link.

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as directory:
    source_path = Path(directory) / 'prepared.pdbqt'
    source_path.write_bytes(molsys.removeprefix('pdbqt_text:').encode('utf-8'))
    with PDBQTFileHandler(source_path, storage_mode='indexed') as handler:
        file_projection = handler.project_coordinates(
            replacement, [[0, 1], [1, 0]], discard_remarks=True,
            output_filename=Path(directory) / 'conformation.pdbqt')
        assert Path(file_projection['molecular_system']).is_file()
    assert source_path.read_bytes() == molsys.removeprefix('pdbqt_text:').encode('utf-8')
```

Writing stages one model at a time and replaces the destination only after
successful completion. A later-coordinate error or changed indexed source
leaves an existing destination intact. This uses the shared document writer,
not a complete output-text intermediary. Coordinate input, report maps,
reference/index metadata and one-model work buffers have distinct costs.
String output additionally materializes the full result. Buffer estimates are
checked against `configure.max_ram_usage`; they do not bound total process RSS.
Input coordinate arrays must not be concurrently edited.

## Reading the report

The JSON-compatible `molsysmt.pdbqt_coordinate_projection@1` report separates:

| Field | Meaning |
| --- | --- |
| `source_payload`, `output_payload` | Actual UTF-8 payload SHA-256 and byte count, excluding the `pdbqt_text:` prefix. |
| `coordinate_to_source_atom_indices` | Prepared source position for each coordinate-input atom. |
| `output_to_source_atom_indices` | Source position for each output atom; this operation retains prepared order. |
| `output_to_coordinate_atom_indices` | Input coordinate atom for each output atom. |
| `output_to_source_structure_indices`, `source_structure_ids` | Selected source positions and declared MODEL labels, separately. |
| `coordinate_input` | Digest of converted float64 little-endian angstrom values, in supplied atom/structure order; encoding is declared alongside it. |
| `coordinate_precision` | Field width, decimals, unit and measured maximum absolute error per output structure. |
| `metadata_disposition`, `chemical_state_provenance`, `software` | Explicit losses, caller declaration and producing MolSysMT version. |

Hashes identify bytes; they do not certify chemical identity or scientific
validity. The result is still the same limited prepared representation with
new geometry. Retain an earlier preparation/export map separately when you
need correspondence to atoms omitted or created before PDBQT preparation.

Native `copy`/`set` plus the native PDBQT writer remain useful when canonical
serialization is acceptable. That writer formats charges to three decimals
and does not preserve opaque source remarks. Use this projection when those
prepared fields must remain fixed. Neither route performs scoring.

:::{seealso}
:class: dropdown

- {ref}`Tutorial_Form_PDBQTFileHandler`
- {ref}`Tutorial_Read_PDBQT_Poses`
- {ref}`cookbook-native-pdbqt`
:::
