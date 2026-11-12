(user-foundations-native-world-file-handlers-molsysmt-pdbfilehandler)=
# PDBFileHandler

`molsysmt.native.PDBFileHandler` is the resident low-level reader behind native
Protein Data Bank (`.pdb`) conversion. Its registered form name is
`molsysmt.PDBFileHandler`.

## Overview and Handler Role

The handler reads the full source into a text buffer and builds parsed record
collections in memory. It accepts multiple MODEL records; it is not a streaming
trajectory reader. The parser uses the PDB 3.3 record profile. The reported
`format_version='3.3'` selects that parser; it does not certify complete wwPDB
conformance or infer the original author's format version.

Writing through this handler is unavailable: `io_mode='w'` and `dump()` do not
produce PDB records. Convert a supported native molecular system to `file:pdb`
when you need the public PDB writer. See {ref}`Tutorial_Convert` for conversion
and its source/target limits.

Unnumbered or nonnumeric `REMARK` records are retained as opaque comments.
In `handler.entry.title.remarks`, their `remarkNum` is `None` and `message`
contains the full trimmed payload, including text beyond column 80. Numbered
comments retain their PDB number and message field. Recognized structured
records, including `REMARK 350` assemblies, retain their independent validation.
Comment tolerance does not interpret provider-specific metadata or guarantee
its preservation after conversion to another form.

## Class Attributes and Parsed Records

| Attribute or expression | Data type | Meaning |
| :--- | :--- | :--- |
| `handler.file` | `io.StringIO` | Resident text buffer; close it explicitly. |
| `handler.format_version` | str | Selected parser profile, currently `"3.3"`. |
| `handler.entry` | parsed record object | Legacy PDB record collections such as title, coordinates and connectivity. |
| `handler.content` | normalized content object | Ordered `models`, `links`, `ssbonds`, `conect`, `bioassemblies` and `issues`, with optional `cryst1`. |
| `handler.content.models[0].atoms` | list | Normalized atom records in the first model. |

Raw atom records retain coordinate tuples in **angstroms** and B factors in
**angstrom squared**, without PyUnitWizard quantity wrappers. They are not
canonical native coordinate arrays. Use {func}`molsysmt.basic.get` or convert
to resident `Structures`/`MolSys` for quantities following your active unit
policy, selections and native `(n_structures, n_atoms, 3)` coordinate shape.
Normalization can record uninterpreted or malformed declarations in `issues`;
it does not certify arbitrary chemical assignments.

## Practical Usage and Streaming Workflow

```python
from contextlib import closing
import molsysmt as msm
from molsysmt.native import PDBFileHandler

path = msm.systems['Trp-Cage']['1l2y.pdb']
with closing(PDBFileHandler(path, io_mode='r')) as handler:
    parsed = handler.content
    assert parsed.models and parsed.models[0].atoms
    assert handler.format_version == '3.3'
    coordinates = msm.get(
        handler, selection=[0, 1], structure_indices=[0], coordinates=True
    )
    assert coordinates.shape == (1, 2, 3)
assert handler.file.closed
```

`contextlib.closing` supplies deterministic cleanup; the handler itself does
not implement the context-manager protocol. A handler built from your own
`StringIO` uses that same buffer, so closing the handler closes it too.

## Performance and I/O Invariants

- **Resident cost:** source text, normalized content and legacy parsed records
  occupy memory. A selected coordinate query may assemble resident structures
  before selecting its result; a small result does not imply a bounded input
  working set. No large-file or zero-copy claim follows from the class name.
- **Operation boundaries:** independent live-handler copy, editing and its
  form-specific structure/topology iterators are unavailable. The identity
  adapter may return the borrowed handler; it is not a snapshot. Convert to
  resident `MolSys` or `Structures` for independent copies and selections. See
  {ref}`Tutorial_Form_molsysmt_PDBFileHandler` for the registered routes.
- **Serial labels:** the parser accepts decimal serials and selected provider
  overflow spellings. It is not a complete validator for every serial-number
  dialect. Native indices remain positions, separate from deposited labels.
