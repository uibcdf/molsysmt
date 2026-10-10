---
summary: TRJPK subset exports fail on list selections
issue: uibcdf/molsysmt#365
status: open
opened: 2026-10-10
closed:
severity: medium
verification: reproduced
area: [form, convert]
guard:
normative:
blocked_by: []
supersedes: []
---

# TRJPK subset export fails on valid list selections

**Reported:** 2026-10-10, current pre-1.0 issue audit.
**Status:** Reproduced; no runtime repair implemented in this audit.

## What

A native StructuresDict with three structures and four atoms is recognized as
`molsysmt.StructuresDict`. Selecting two atoms and two structures for TRJPK export
raises `AttributeError: 'list' object has no attribute 'shape'`:

```python
from pathlib import Path
from tempfile import TemporaryDirectory
import numpy as np
import molsysmt as msm

molsys = {
    "coordinates": msm.pyunitwizard.quantity(np.arange(36.0).reshape(3, 4, 3), "nm"),
    "box": msm.pyunitwizard.quantity(np.repeat(np.eye(3)[None, :, :], 3, axis=0), "nm"),
    "time": msm.pyunitwizard.quantity([0.0, 1.0, 2.0], "ps"),
    "structure_id": np.array(["s0", "s1", "s2"]),
}
with TemporaryDirectory() as directory:
    msm.convert(molsys, to_form=str(Path(directory) / "subset.trjpk"),
                selection=[3, 1], structure_indices=[2, 0])
```

## How

`molsysmt/form/molsysmt_StructuresDict/to_file_trjpk.py` accesses
`atom_indices.shape[0]` and `structure_indices.shape[0]`, although the public
conversion boundary supplies lists. The same writer uses an `elif` between
coordinate structure selection and atom selection, so its source also indicates
that selecting both axes would omit the atom subset after fixing list counts.
That second failure mechanism is source-inspected, not yet reproduced by a
successful public export.

## Why

This existing public export route fails for valid selections. A repair must also
prevent a header reporting two atoms while retaining four atoms in its payload.
Restoring the four missing TRJPK structural getters is separately part of #139;
that does not repair the writer.

## What is measured and what is assumed

The public call above was executed on the named source and raises the list-shape
error. No successful selected round trip, performance measurement or fixed
behavior is claimed. The bundled TRJPK reader separately converts its local
20,000-structure, two-atom file to StructuresDict, showing that a reader already
exists. Its four advertised direct queries currently fail under #139.

## What was refuted

The failing input is recognized as StructuresDict and uses unit-bearing
coordinates, box and time. The failure occurs on selection counting, not format
detection or lack of a reader. No new storage format is needed.

## Scope and exclusions

Repair the existing selected export and its round trip. Preserve fixed nm/ps
storage and original structure ID labels. Do not add streaming, general append,
new backends or format migration. No runtime or dependency changes in this audit.

## Acceptance criteria

- Public list/array selections produce coherent header and payload dimensions.
- Simultaneous atom/structure selections apply both axes and retain their declared
  order, including nonconsecutive structure positions.
- Coordinates, boxes, time and structure IDs stay aligned after reading.
- Empty selections and optional absent fields retain explicit semantics.
- A nondefault unit-policy control verifies fixed nm/ps storage and correct
  physical values on reading.
- Add meaningful public round-trip guards and update the affected documentation.

## Provenance

Linux shared development environment, Python 3.14.7, NumPy 2.4.6,
2026-10-10. Audited source: `970fd28e374f3dda58eda0a5ab259bbdf7629402`.
The reproduction uses managed temporary storage removed after failure.
