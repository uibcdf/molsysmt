---
summary: form/molsysviewer_MolSysView/extract.py has the public signature, not the form-level one, so msm.extract(view) always raises
issue: uibcdf/molsysmt#204
status: resolved
opened: 2026-09-06
closed: 2026-09-06
severity: medium
verification: reproduced
area: [form, basic]
guard: tests/test_form_plugin_conventions.py::test_every_form_extract_accepts_the_dispatch_contract
normative:
blocked_by: []
supersedes: []
---

# A form that cannot be called the way every form is called

**Reported:** 2026-09-06 from `uibcdf/molsysviewer`, while re-measuring which of the
viewer's MolSysMT-facing methods are redundant. Not blocking anything there:
`view.extract(...)` does not go through this path.
**Status:** resolved.

## What

`msm.extract` raised `TypeError` for every call on a `molsysviewer.MolSysView`, including
the default one.

```python
>>> msm.extract(msv.demo["1TCD"])
TypeError: extract() got an unexpected keyword argument 'atom_indices'
```

The rest of the form is fine: `get`, `contains`, `is_composed_of`, `convert` and `copy`
all work on a `MolSysView`. `extract` was the only one.

## How

`molsysmt/basic/extract.py:139` resolves the selection once and then calls every form the
same way, with the form-level contract:

```python
_dict_modules[form_in].extract(item, atom_indices=atom_indices,
                               structure_indices=structure_indices,
                               copy_if_all=copy_if_all, skip_digestion=True)
```

`molsysmt/form/molsysviewer_MolSysView/extract.py` declared the **public** signature
instead — `selection`, `syntax`, no `atom_indices`, no `copy_if_all` — so the dispatch
never matched. Its body then re-did selection work the caller had already done: it
converted to `molsysmt.MolSys`, called `basic.extract` again with `selection`, and
converted back. That repetition is the tell that it was written against the wrong contract
rather than for a viewer-specific reason.

It now follows `nglview_NGLWidget/extract.py`, the form of the same kind that had it
right: honour `copy_if_all` when nothing is selected, and otherwise convert out with the
indices, convert back.

## Why

`extract` is one of the public operations a supported form is expected to answer, and the
failure was total rather than partial — no argument combination worked. The error also
named an internal keyword the user never wrote, so it reads as a MolSysMT defect rather
than as an unsupported operation, which is exactly what it was.

## What is measured and what is assumed

**Measured:** the reproduction above, and the same three assertions passing afterwards on
a builder system: default extraction returns an equivalent, distinct view; a selection
returns the subset; `copy_if_all=False` returns the same object.

**Measured:** scanning all 84 `form/*/extract.py` signatures against the four keywords the
dispatcher passes, five forms did not accept them. One is the reported form. A second,
**`molsysmt.StructuresDict`, is Tier 1** and failed for the same reason with a smaller
cause: no `skip_digestion` parameter.

```
molsysmt_StructuresDict:         missing ['skip_digestion']
molsysviewer_MolSysView:         missing ['atom_indices', 'copy_if_all']
molsysmt_MolecularMechanics:     missing ['atom_indices', 'structure_indices']
molsysmt_MolecularMechanicsDict: missing ['atom_indices', 'structure_indices']
string_amino_acids_3:            missing ['atom_indices', 'structure_indices']
```

Both unambiguous ones are fixed here. `molsysmt.StructuresDict` now returns a copy for a
whole-system extraction and raises the `NotImplementedMethodError` its body always
intended for a subset, instead of `TypeError` for both.

**Measured:** the remaining three raise `TypeError` through `msm.extract` today. The
report suspected they might be deliberate; they are reachable, so the failure is real,
but the fix is not mechanical.

## What was refuted

**That the three remaining forms are the same defect.** They are the same symptom and a
different question. `molsysmt.MolecularMechanics` and its dict form have no element axis
at all — the first already answers `NotWithThisFormError`, which is the right answer once
it can be reached. `string_amino_acids_3` indexes by group, not by atom, throughout its
module: `add`, `merge` and all four converters take `group_indices`, so renaming one
parameter would break its own callers and mean nothing for a sequence with no atoms. Each
needs a decision about what extraction means for a form without atoms, which is more than
this entry.

They are named in `EXTRACT_CONTRACT_DEBT` in the guard rather than skipped, so the debt is
visible in the test that would otherwise appear to cover them.

## Scope and exclusions

Covered: `molsysviewer.MolSysView` and `molsysmt.StructuresDict`, and a gate over every
form's `extract` signature.

Not covered: that `molsysmt.StructuresDict` cannot extract a subset at all. Its body
raises `NotImplementedMethodError` for any non-`all` index, which is a capability gap and
not this defect; the signature fix only lets that intended error be reached.

## Acceptance criteria

- `msm.extract(view)` and `msm.extract(view, selection=...)` return a `MolSysView`.
- A form whose `extract` does not accept the dispatcher's four keywords fails the suite,
  outside the three declared exceptions. Confirmed to report both fixed forms against the
  previous signatures.

## Provenance

Linux, Python 3.13.14, MolSysViewer 0.23.0 from a source checkout, `molsysmt` at working
tree `4eab2f6c1`, 2026-09-06.
