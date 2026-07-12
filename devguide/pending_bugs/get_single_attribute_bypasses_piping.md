# Bug: a single-attribute `get()` bypasses the attribute pipes

**Status:** pending (diagnosed 2026-07-12, reproduced; fix not started)
**Severity:** high — affects Tier 1 forms through the public `get()` facade
**Location:** `molsysmt/basic/get.py:375`

## Symptom

Asking `get()` for **one** attribute fails, while asking for that same attribute
**plus another one** succeeds. Requesting less makes the call break.

```python
import molsysmt as msm
pdb = msm.systems['T4 lysozyme L99A']['181l.pdb']   # file:pdb, Tier 1

msm.get(pdb, element='atom', atom_type=True)
# AttributeError: module 'molsysmt.form.file_pdb' has no attribute 'get_atom_type_from_atom'

msm.get(pdb, element='atom', atom_type=True, atom_name=True)
# works: (['N', 'C', 'C', ...], ['N', 'CA', 'C', ...])
```

The same pattern holds for `group_type`, and for every attribute a piped form does
not serve with a getter of its own. Reproduced on `file:pdb`, `file:xtc` and
`file:trjpk`.

`file:inpcrd` used to reproduce it too, and no longer does — but only because every
one of its getters was implemented directly. That is the expensive way out: it makes
the pipe redundant instead of making it work. It should not be taken as the template
for the other forms.

## Root cause

File forms are designed to implement a handful of cheap direct getters and to
delegate everything else through their pipes. `file:pdb`, for instance, implements
8 getters but declares 65 attributes, routing the rest via
`piped_topological_attribute = 'molsysmt.Topology'` and
`piped_structural_attribute = 'molsysmt.Structures'`. That design is sound.

The problem is that `get()` only ever consults the pipes when more than one
attribute is requested:

```python
# molsysmt/basic/get.py:375, inside _piped_molecular_system
if not_piped or len(in_attributes)==1:
    return None, None
```

When a single attribute is requested, `_piped_molecular_system` returns
`(None, None)`, `get()` falls through to the direct-getter branch at
`molsysmt/basic/get.py:249`, and

```python
aux_get = getattr(_dict_modules[aux_form], f'get_{in_attribute}_from_{element}')
```

raises a raw `AttributeError` — an internal error leaking straight to the user,
not even a MolSysMT exception.

## The clause is a deliberate optimisation, and it is a sound one

`len(in_attributes)==1` is not an oversight. Going through a pipe means converting
the form, and that conversion can be expensive: asking only for `n_atoms` must not
parse a whole PDB file into a `Topology` when the header already holds the number.
The clause exists so that a single cheap attribute is served directly.

The intent is right. The defect is that **the number of attributes is a proxy for
cost, not a guarantee that the direct getter exists**, and the code uses it as if
it were the latter. It takes the cheap path without ever checking that there is a
cheap path to take.

## Proposed fix

Keep the optimisation and give it the missing floor: take the direct path only when
the getter is actually there.

```python
if not_piped:
    return None, None
if len(in_attributes) == 1:
    attribute = in_attributes[0]
    _, aux_form = where_is_attribute(molecular_system, attribute, skip_digestion=True)
    if hasattr(_dict_modules[aux_form], f'get_{attribute}_from_{element}'):
        return None, None      # cheap direct read, exactly as designed
    # no direct getter: fall through to the pipe instead of raising AttributeError
```

`get(pdb, n_atoms=True)` still converts nothing. `get(pdb, element='atom', atom_type=True)`
stops crashing.

Where neither a direct getter nor a pipe can serve the attribute, `get()` must raise
a MolSysMT exception naming the form and the attribute, never a bare `AttributeError`
from `getattr`.

## The cost model behind the clause is worth making explicit

The reverse case also happens, and it is the reason the clause reads `== 1` rather
than `<= 3`: on a file form, each direct getter may open and close the file, so N
direct getters cost N file opens, whereas the pipe costs one conversion plus N cheap
reads from the converted object. Past some N the pipe is cheaper *even when the direct
getters exist*.

So the real rule the code is approximating is:

- if any requested attribute has no direct getter, pipe everything (one conversion,
  one open);
- if all of them have one, choose by cost: a single attribute goes direct, several
  go through the pipe.

That is what `get.py` already does, minus the existence check. What it cannot do is
know *where* the crossover sits, because the cost is a property of the form, not of
`get()`: a small `file:pdb` and a 10 GB `file:xtc` do not have the same crossover.
A fixed constant in `get.py` is guessing on behalf of every form.

Whether forms should declare their own crossover (a threshold, or a list of attributes
that are cheap to read directly) is an open design question. It should be settled
before the constant is tuned, but it does **not** block the correctness fix above,
which is orthogonal: whatever the heuristic decides, it must never route to a getter
that does not exist.

## Related, still undiagnosed

While reproducing this, a second wrinkle appeared and needs its own diagnosis
before the fix is finalised: `element` is a single value applied to the whole
`get()` call, so mixing attributes that live at different elements in one piped
call can still fail. On `file:xtc`:

```python
msm.get(xtc, element='atom', coordinates=True, structure_id=True)
# AttributeError inside mdtraj.XTCTrajectoryFile
```

Here the pipe does engage (the error names the pipe target, not `file:xtc`), but
`structure_id` is only served `from_system` while `element='atom'` was requested
for the whole call. Whether `get()` should resolve `element` per attribute is a
design question, not just a bug fix.

## Verification

A fix should make these pass, for every Tier 1 form, for **each** declared
attribute requested **on its own**:

```python
msm.get(item, element=<element from the attribute catalog>, **{attribute: True})
```

See [`form_attributes_declared_without_getters.md`](form_attributes_declared_without_getters.md)
for the forms where the attribute is unreachable even with the pipes working —
those are a separate defect and will still fail after this one is fixed.
