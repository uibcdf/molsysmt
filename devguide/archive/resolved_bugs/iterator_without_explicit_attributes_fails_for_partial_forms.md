# Iterator Without Explicit Attributes Fails for Partial Forms

## Status

**RESOLVED (archived 2026-08-03).** Four defects fixed and guarded by
regressions. The fifth case was not a fault in `Iterator` at all and closed with
[`structural_attribute_resolution_ignores_the_structure_axis.md`](../archive/resolved_bugs/structural_attribute_resolution_ignores_the_structure_axis.md).

Discovered during the F2 notebook-execution audit on 2026-07-28.

## Public Contract

`molsysmt.Iterator` documents that, when no attributes are requested, each
iteration yields a molecular system whose structural data are updated for the
current chunk.

## What was fixed

### 1. `structure_indices=None` reached the reader

`basic/iterator.py` built its reusable output object with
`convert(..., structure_indices=None)`, and the H5MSM reader treated `None` as an
iterable of indices. The conversion now asks for a single structure: the yielded
system is a container whose structural series are overwritten on every iteration,
so converting the whole structure axis would materialize the trajectory that
chunked iteration exists to avoid.

### 2. An unguarded `append` — worse than the reported crash

`where_is_attribute` returns `(None, None)` for an attribute no item provides.
The loop building the per-item iterators guarded only the **assignment** of
`tmp_iterator`; the `self._iterators.append(tmp_iterator)` was outside the guard.
So the behaviour depended on the position of the missing attribute:

| request on a DCD (no `structure_id`, no `time`) | before | after |
|---|---|---|
| `coordinates=True` | 1 item ✔ | 1 item ✔ |
| `coordinates=True, box=True` | 1 item ✔ | 1 item ✔ |
| `coordinates=True, time=True` | **0 items, no error** | `NotWithThisFormError` |
| `time=True, coordinates=True` | `UnboundLocalError` | `NotWithThisFormError` |

The third row is the one the original report missed. The previous iterator was
appended a second time, so the loop body never ran and nothing was reported —
which also contradicts the original *Impact* note that explicit structural
iteration "works and is sufficient". It works only while every requested
attribute exists in the same item.

Unavailable attributes are now dropped when they come from the implicit default
list (`structure_id`, `time`, `coordinates`, `box` are defaults, not a request),
and rejected with `NotWithThisFormError` when the caller named them.

### 3. The placeholder pinned the structure axis

Converting a coordinate-only form yields a system with a *generated*
`structure_id` of length one. Left in place, it kept the structure axis pinned to
the placeholder while each chunk carried many structures, and `set` refused the
result. The series the iterator will not be feeding are now cleared on the
placeholder. Relatedly, `__next__` sets every structural series in a single call
with the element level inferred per attribute; setting them one level at a time
compared a fresh chunk against the series still holding the previous one.

### 4. `structures/id` stored as an empty dataset

Not in the original report, and in the form layer rather than in `Iterator`:
`molsysmt_H5MSMFileHandler/iterators.py` read `f['id'][indices]` even when the
dataset has shape `(0,)`, raising `IndexError: Fancy indexing out of range for
empty dimension`. This is what broke implicit iteration over an ordinary H5MSM
trajectory such as `traj_pentalanine.h5msm`, whose `structures/id` is empty while
`coordinates` and `time` are full. The `time` branch of the same reader already
treated an empty dataset as absent; `structure_id` now does the same.

This belongs to the family tracked in
[`form_attributes_declared_without_getters.md`](form_attributes_declared_without_getters.md):
the attribute is declared, so `where_is_attribute` reports it, but no value backs
it.

## Verification

| case | result |
|---|---|
| `Iterator(popc_membrane.dcd, chunk=2)` | 3 items sized `[2, 2, 1]`, last chunk partial |
| `Iterator(popc_membrane.dcd, selection='atom_index < 100', chunk=2)` | 100 atoms per yielded system |
| `Iterator(traj_pentalanine.h5msm, chunk=1000)` | 5 items of 1000 structures |
| `Iterator([villin.h5msm, villin.dcd], chunk=10, coordinates=True, box=True)` | 2 chunks of 10 |
| `Iterator([villin.h5msm, villin.dcd], chunk=10)` | 2 chunks of 10, in either item order |

Guarded by nine regressions in `tests/basic/iterator/test_iterator.py`, including
a parametrization over both keyword orders — the order-independence is the point
of the second fix — and one over both item orders of the composite. 7913 tests
across `tests/basic`, `tests/form` and `tests/_private` pass.

## The composite case was a symptom, not a bug here

The composite reproducer failed for a reason outside this module:

```
villin traj_chicken_villin_HP35_solvated.h5msm  ->  1 structure
villin traj_chicken_villin_HP35_solvated.dcd    -> 20 structures
```

`structure_id` and `time` resolved to the H5MSM item and `coordinates` and `box` to
the DCD, so one iterator was built per item and they were advanced in lockstep over
different structure axes. The molecular system had no structure axis of its own:
listing the same two files the other way round made `n_structures` 1 instead of 20,
and a conversion discarded nineteen structures without a word.

That is a defect of attribute resolution, reported and fixed separately in
[`structural_attribute_resolution_ignores_the_structure_axis.md`](../archive/resolved_bugs/structural_attribute_resolution_ignores_the_structure_axis.md).
`where_is_attribute` now delivers a structural attribute only from items spanning
the axis, so every iterator built here covers the same axis by construction.

`Iterator([h5msm, dcd], chunk=10)` yields two chunks of ten, in either item order,
iterating `coordinates` and `box`. A structure-axis check added to `iterator.py`
while this was being diagnosed was removed once the resolution layer was correct:
one policy, in one place.

## Remaining work

None. Structure order and units are asserted by
`test_iterator_preserves_structure_order_and_units`, which stacks the chunks back
together and compares them with the whole trajectory, units included.
