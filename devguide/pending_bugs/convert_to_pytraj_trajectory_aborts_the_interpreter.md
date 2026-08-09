---
summary: Converting into pytraj.Trajectory kills the process with SIGABRT, uncatchable from Python.
issue: uibcdf/molsysmt#138
status: open
opened: 2026-08-08
closed:
severity: high
verification: reproduced
area: [form, convert]
guard:
normative:
blocked_by: []
supersedes: []
---

# Converting into `pytraj.Trajectory` aborts the interpreter

**Reported:** 2026-08-08, found while mapping how an item of every declared form can be
obtained, for a `get_form` test battery. Not found by the test suite, which never performs
this conversion.

**Status:** open. Reproducible.

**Severity:** high in kind, low in reach. The process dies with `SIGABRT`; no Python
exception is raised, so no caller can catch it, no `pytest.raises` can contain it, and a
test session that hits it loses every result gathered so far. It also means a declared,
publicly listed form can take down a user's session. Reach is low because nothing in the
suite or the documented workflows converts into `pytraj.Trajectory` today.

## Symptom

```
$ python -c "
import molsysmt as msm
from molsysmt import systems
pdb = systems['chicken villin HP35']['1vii.pdb']
msm.convert(pdb, to_form='pytraj.Trajectory')"

double free or corruption (!prev)
Aborted (core dumped)          # exit 134
```

A different origin fails earlier and more politely, which is why the crash went unnoticed:

```
msm.convert(molsys, to_form='pytraj.Trajectory')   # from molsysmt.MolSys
AttributeError: 'MolSys' object has no attribute 'is_empty'
```

## What is known

- The abort is raised by native code, so the fault is in pytraj/cpptraj or in how the
  converter hands memory to it -- not in Python-level MolSysMT logic.
- `pytraj.Topology` converts and is detected correctly, so the dependency itself works.
- The `AttributeError` from the `molsysmt.MolSys` origin is a separate, plain defect: the
  converter calls `is_empty` on an object that has no such attribute.

## Why it matters beyond this form

Any harness that enumerates forms -- the planned `get_form` battery, a conversion-coverage
matrix, a benchmark sweep -- has to run each form in its own process, or one native abort
destroys the whole run. That is a constraint on how those tools are written, so it is
worth recording even before the bug is fixed.

## Next steps

1. Reduce it: find which converter call aborts, and whether it survives outside MolSysMT
   with the same inputs. If plain pytraj aborts too, the issue is upstream and the right
   answer here is to gate the edge.
2. Fix the `is_empty` `AttributeError` on the `molsysmt.MolSys` origin regardless; it is
   independent and cheap.
3. Decide whether `pytraj.Trajectory` should stay a declared conversion target while it
   can abort the interpreter.
