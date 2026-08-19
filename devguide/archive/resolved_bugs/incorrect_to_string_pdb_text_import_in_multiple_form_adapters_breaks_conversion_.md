---
summary: Incorrect to_string_pdb_text import in multiple form adapters breaks conversion with skip_digestion
issue: uibcdf/molsysmt#180
status: resolved
opened: 2026-08-19
closed: 2026-08-19
severity: high
verification: reproduced
area: [form, convert]
guard: tests/form/test_piped_pdb_text_conversion_routes.py
normative:
blocked_by: []
supersedes: []
---

# Bug: incorrect to_string_pdb_text import in multiple form adapters

**Reported:** 2026-08-19, during documentation and static view generator audit.
**Status:** resolved. The seven imports are corrected, and two further defects on the same routes were found and fixed while verifying them.

## What

Multiple form conversion modules in `molsysmt/form/` import `to_string_pdb_text` from `molsysmt.form.string_pdb_text.to_string_pdb_text` (the converter for converting `string:pdb_text` to `string:pdb_text`) instead of their local `from .to_string_pdb_text import to_string_pdb_text`.

When `msm.convert(...)` invokes one of these two-step piped conversion adapters, it calls the imported `to_string_pdb_text(item, ..., skip_digestion=True)` passing the source object (`nglview.NGLWidget`, `openmm.Topology`, or `string:alphafold_id`). Because `skip_digestion=True` is supplied, `string_pdb_text.to_string_pdb_text` bypasses form checking and calls `extract(item) -> copy(item)` on the non-string object, causing immediate execution failures:

```python
import molsysmt as msm

molsys = msm.convert(msm.systems['Met-enkephalin']['met_enkephalin.h5msm'])
v = msm.view(molsys, viewer='nglview')
top = msm.convert(v, to_form='openmm.Topology')
```

Output:
```
Traceback (most recent call last):
  ...
  File "molsysmt/form/nglview_NGLWidget/to_openmm_Topology.py", line 32, in to_openmm_Topology
    tmp_item = to_string_pdb_text(item, atom_indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)
  File "molsysmt/form/string_pdb_text/to_string_pdb_text.py", line 33, in to_string_pdb_text
    return extract(item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=copy_if_all, skip_digestion=True)
  File "molsysmt/form/string_pdb_text/extract.py", line 37, in extract
    tmp_item = copy(item)
  File "copy.py", line 80, in copy
    return copier(x)
  File "ipywidgets/widgets/widget.py", line 509, in __copy__
    raise NotImplementedError("Widgets cannot be copied; custom implementation required")
NotImplementedError: Widgets cannot be copied; custom implementation required
```

## How

In the affected adapters, the import path was mistakenly hardcoded to the target form package rather than relative to the source adapter module:

- [`molsysmt/form/nglview_NGLWidget/to_openmm_Topology.py:29`](../../molsysmt/form/nglview_NGLWidget/to_openmm_Topology.py#L29)
  ```python
  # Wrong:
  from molsysmt.form.string_pdb_text.to_string_pdb_text import to_string_pdb_text
  # Correct:
  from .to_string_pdb_text import to_string_pdb_text
  ```

- [`molsysmt/form/openmm_Topology/to_file_pdb.py:31`](../../molsysmt/form/openmm_Topology/to_file_pdb.py#L31)
  ```python
  # Wrong:
  from molsysmt.form.string_pdb_text.to_string_pdb_text import to_string_pdb_text
  # Correct:
  from .to_string_pdb_text import to_string_pdb_text
  ```

- [`molsysmt/form/openmm_Topology/to_nglview_NGLWidget.py:29`](../../molsysmt/form/openmm_Topology/to_nglview_NGLWidget.py#L29)
  ```python
  # Wrong:
  from molsysmt.form.string_pdb_text.to_string_pdb_text import to_string_pdb_text as to_string_pdb_text
  # Correct:
  from .to_string_pdb_text import to_string_pdb_text
  ```

- [`molsysmt/form/openmm_Topology/to_openmm_PDBFile.py:29`](../../molsysmt/form/openmm_Topology/to_openmm_PDBFile.py#L29)
  ```python
  # Wrong:
  from molsysmt.form.string_pdb_text.to_string_pdb_text import to_string_pdb_text
  # Correct:
  from .to_string_pdb_text import to_string_pdb_text
  ```

- [`molsysmt/form/openmm_Topology/to_pdbfixer_PDBFixer.py:29`](../../molsysmt/form/openmm_Topology/to_pdbfixer_PDBFixer.py#L29)
  ```python
  # Wrong:
  from molsysmt.form.string_pdb_text.to_string_pdb_text import to_string_pdb_text as to_string_pdb_text
  # Correct:
  from .to_string_pdb_text import to_string_pdb_text
  ```

- [`molsysmt/form/string_alphafold_id/to_openmm_PDBFile.py:29`](../../molsysmt/form/string_alphafold_id/to_openmm_PDBFile.py#L29)
  ```python
  # Wrong:
  from molsysmt.form.string_pdb_text.to_string_pdb_text import to_string_pdb_text
  # Correct:
  from .to_string_pdb_text import to_string_pdb_text
  ```

- [`molsysmt/form/string_alphafold_id/to_openmm_Topology.py:29`](../../molsysmt/form/string_alphafold_id/to_openmm_Topology.py#L29)
  ```python
  # Wrong:
  from molsysmt.form.string_pdb_text.to_string_pdb_text import to_string_pdb_text
  # Correct:
  from .to_string_pdb_text import to_string_pdb_text
  ```

## Why

This breaks public conversion routes declared in the capability matrix:
- `nglview.NGLWidget -> openmm.Topology`
- `openmm.Topology -> file:pdb`
- `openmm.Topology -> nglview.NGLWidget`
- `openmm.Topology -> openmm.PDBFile`
- `openmm.Topology -> pdbfixer.PDBFixer`
- `string:alphafold_id -> openmm.PDBFile`
- `string:alphafold_id -> openmm.Topology`

Users relying on `msm.convert()` to move between viewer widgets, topology objects, and downstream preparation tools (such as PDBFixer or OpenMM PDB writers) encounter crashes even when all dependencies are installed.

## What is measured and what is assumed

- Measured: Exactly 7 files in `molsysmt/form/` contain the faulty import statement `from molsysmt.form.string_pdb_text.to_string_pdb_text import to_string_pdb_text`.
- Measured: Direct conversion `nglview_NGLWidget -> openmm.Topology` succeeds when `from .to_string_pdb_text import to_string_pdb_text` is used.
- Measured: `openmm.Topology -> string:pdb_text` currently requires `coordinates` to be provided or default dummy coordinates synthesized when coordinates are `None`.

## What was refuted

- Refuted hypothesis: That the failure was caused by missing attributes in `NGLWidget`. The widget has full state extraction in `nglview_NGLWidget/to_string_pdb_text.py`, which works properly when invoked.

## Scope and exclusions

- **In scope**: Correcting the import statement in all 7 identified adapter files and adding unit tests under `tests/form/` verifying conversion through each route.
- **Out of scope**: Architectural redesign of intermediate string:pdb_text pipelines.

## Acceptance criteria

1. All 7 adapters import `to_string_pdb_text` relatively from their own directory (`from .to_string_pdb_text import to_string_pdb_text`).
2. Unit tests verify end-to-end conversion for each of the 7 routes without throwing exceptions.
3. Release gate script `validate_form_adapters.py` and `pytest tests/form/` pass cleanly.

## Resolution

Reproduced independently before changing anything: `NGLWidget -> openmm.Topology` fails
with `NotImplementedError: Widgets cannot be copied`, and the faulty import is in
exactly the seven files this report lists. All three affected packages do have a local
`to_string_pdb_text.py`, so the proposed correction applies.

**Where it came from.** `git log -S` places all seven in `e6b20c77c` (2026-08-08),
*"refactor(form): make a plugin's converters lazy, and unambiguous to import"* — 214
files, 1 939 insertions, 2 467 deletions. Seven imports landed on the target form's
package rather than the local module during a mass rewrite whose stated goal was
unambiguous imports.

**Why it stayed hidden for eleven days.** The import resolves cleanly, because
`string_pdb_text.to_string_pdb_text` exists — it is that form's identity converter. The
adapters call it with `skip_digestion=True`, legitimately, since this is an internal
two-step conversion; and `skip_digestion=True` switches off the form check. So the
identity converter accepted a widget and passed it to `extract() -> copy()`. The
mechanism that made the failure silent is the same one that made it fatal.

### Two further defects on the same routes

Correcting the imports fixed `NGLWidget -> openmm.Topology` and left the three
`openmm.Topology -> X` routes failing differently, which is how these surfaced:

- `AttributeError: 'NoneType' object has no attribute 'shape'`. An `openmm.Topology`
  carries no coordinates, and `openmm_Topology/to_string_pdb_text.py:44` reaches
  `coordinates.shape[0]` unguarded. With `coordinates=` supplied the routes work, so
  this is the contract rather than a defect in the route — but the diagnostic is the
  same class as `uibcdf/molsysmt#179` and is **not fixed here**.
- `openmm_Topology/to_openmm_PDBFile.py` called `StringIO().read(text)`, which reads
  *from* an empty buffer and takes a size argument, so it raised
  `TypeError: argument should be integer or None, not 'str'`. Fixed to
  `PDBFile(StringIO(text))`, matching what `string_pdb_text/to_openmm_PDBFile.py`
  already did.

### A guard at the mechanism, not only at the seven sites

`string_pdb_text.to_string_pdb_text` now checks that its item is a string **even when
digestion is skipped**. An identity converter is the one place where a wrong item cannot
be inferred from what the function is asked to do, so it is worth the one `isinstance`.
The failure now names the likely import mistake instead of surfacing from inside
`copy()`.

## What was refuted

**A static check in `validate_form_adapters.py`, proposed as the third part of this
fix.** It does not work and was withdrawn rather than shipped.

The first rule — flag an absolute import of a converter that shadows a local module —
produced 52 hits, most of them legitimate: `MDAnalysis_AtomGroup/to_molsysmt_MolSys.py`
delegating to `MDAnalysis_Universe.to_molsysmt_MolSys` is how that adapter is designed.

Narrowing it to *identity* converters looked sharper and was not. It flagged
`file_h5msm` and `file_pdb` importing `molsysmt_H5MSMFileHandler.to_molsysmt_H5MSMFileHandler`
and `molsysmt_PDBFileHandler.to_molsysmt_PDBFileHandler`, and those are correct:
unlike `string_pdb_text`'s, those converters explicitly accept `str`/`PathLike` and build
the handler from a path. Verified by running the routes — `file:h5msm -> molsysmt.MolSys`,
`file:h5msm -> molsysmt.Topology` and `file:pdb -> molsysmt.MolSys` all succeed.

What separates the defect from the legitimate cases is **behavioural** — whether the
imported converter tolerates a foreign item — and that is not visible to a static rule.
Shipping it would have meant either a spuriously failing gate or 52 unverified waivers.

The runtime guard above covers the same ground soundly, and
`test_no_adapter_imports_the_identity_converter` pins this specific import at test time.
