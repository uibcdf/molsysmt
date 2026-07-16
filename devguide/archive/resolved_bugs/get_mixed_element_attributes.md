# Resolved Bug: mixed-element attribute requests failed inside pipe targets

**Status:** resolved and contract-tested 2026-07-13
**Originally isolated:** 2026-07-13
**Severity:** medium — public `get()` facade and trajectory forms
**Location:** `molsysmt/basic/get.py`

## Symptom

`element` was applied to every attribute in a `get()` call even when the
attribute catalog allowed some requested attributes only at another element
level. This mixed request therefore attempted to find
`get_structure_id_from_atom` inside the XTC pipe target:

```python
msm.get(xtc, element='atom', coordinates=True, structure_id=True)
```

The public boundary raised `NotWithThisFormError`, although the request was
unambiguous: coordinates are available from atoms and `structure_id` is
available only from the system.

## Resolution

`get()` now groups requested attributes by a catalog-compatible element before
selection and pipe resolution. It follows two conservative rules:

- retain the requested element whenever the attribute supports it;
- redirect an incompatible attribute only when its catalog entry declares one
  unique supported element.

Each group is evaluated independently and the results are reassembled in the
original keyword order. Element selections and masks apply only to the group
evaluated at that element; redirected system-level metadata uses all system
elements. The existing special meaning of an atom selection passed with
`element='system'` is preserved.

Regression tests use the bundled XTC trajectory and cover values, dictionary
ordering, atom selection, structure selection, and system-level metadata.
The public docstring, User Guide, trajectory Cookbook, and Common Core course
now state the mixed-element contract.
