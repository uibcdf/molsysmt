---
summary: Ragged returns carry numpy scalars where the rest of the API returns native ints
issue: uibcdf/molsysmt#165
status: open
opened: 2026-08-17
closed:
verification: measured
area: [api, basic, topology]
guard:
normative: devguide/INTERFACES.md
blocked_by: []
supersedes: []
---

# Ragged returns carry NumPy scalars where the rest of the API returns native ints

**Reported:** 2026-08-17 during a User Guide audit, as a rendering complaint about
`np.int64(...)` in notebook output. **Rewritten 2026-08-18** after an audit that
found the original scope wrong in both directions and the cause elsewhere.
**Status:** open. The rule this resolves to is written in
[INTERFACES.md](../INTERFACES.md), *Scalar types in returned values*; the code does
not yet follow it everywhere.

## What

`molsysmt.basic.get` returns **native Python `int`** for flat attributes and
**`np.int64`** for ragged ones. Same library, same kind of datum, two types:

```python
>>> msm.get(ms, element='atom', atom_index=True)[0]
0                                     # int
>>> msm.get(ms, element='atom', bonded_atoms=True)[1]
[np.int64(0), np.int64(2), np.int64(4)]
>>> msm.get(ms, element='system', bonded_atom_pairs=True)[0]
[np.int64(0), np.int64(1)]
```

`molsysmt.topology.get_covalent_blocks` returns something worse — a single
container holding both:

```python
>>> {type(x).__name__ for blk in msm.topology.get_covalent_blocks(ms) for x in blk}
{'int', 'int64'}
```

### The original report was wrong about the scope, in both directions

It names three functions. Two of them are already correct:

| Function named | Actual state |
| --- | --- |
| `get_dihedral_quartets` | native `int` leaves — already clean |
| `get_covalent_paths` | returns an `ndarray`, `dtype=int64` — correct under the rule, never a defect |
| `get_covalent_blocks` | `ndarray(dtype=object)` of `set`s mixing `int` and `int64` |

And the surface is not in `topology` at all. Sweeping 11 attributes across 4 element
levels on one system finds nine combinations delivering NumPy scalars:

```
bonded_atoms        (atom, system)      chain_index     (group, component)
inner_bonded_atoms  (atom, system)      entity_index    (component)
group_index         (component)         molecule_index  (component)
```

It reaches first-line documentation: `docs/content/user/tools/basic/get.ipynb` and
course Module 08, not only the `get_covalent_blocks` tutorial.

## How

Flat attributes pass through `ndarray.tolist()` in the form adapters — for example
`molsysmt/form/molsysmt_Topology/get_topological_attributes.py:465` — and `tolist()`
converts NumPy scalars to native types recursively. Ragged structures are assembled
by Python-level iteration over the same arrays and keep `np.int64`.

The library already normalises; it normalises half its outputs.

### Why `get_covalent_blocks` mixes the two

Worth recording, because the mixture looks arbitrary and is not. The graph's nodes
are **all** `int`:

```
tipos de nodo en el grafo:            {'int': 62}
tipos en el primer componente conexo: {'int', 'int64'}
```

`get_bondgraph` calls `G.add_nodes_from(atom_indices)` with the clean list, then
`G.add_edges_from(bonded_atoms)` with pairs of `np.int64`. Since `np.int64(1)` hashes
equal to `1`, NetworkX does not create a second node — but it does use the `np.int64`
object as the key inside the adjacency mapping. `connected_components` walks that
adjacency, so the seed node comes out `int` and its neighbours `np.int64`.

**This makes it one defect, not two.** If `get()` delivers
`inner_bonded_atom_pairs` with native ints, `get_bondgraph` builds clean edges and
`get_covalent_blocks` stops mixing.

## Why

Not for how it prints. That was the symptom that made it visible.

**A NumPy scalar inside a Python container is worse than a native one on both axes**,
and buys nothing. Measured over 200 000 integers:

| Container | Memory | `sum()` |
| --- | ---: | ---: |
| `list` of `np.int64` | 8.02 MB | 7.7 ms |
| `list` of `int` | 7.22 MB | 2.5 ms |
| `ndarray` of `int64` | 3.20 MB | 0.2 ms |

NumPy's advantages belong to the array, not to the scalar. Boxed into a list, the
scalar has left the typed buffer behind and carries only the overhead.

**It breaks serialisation for the caller.** `json.dumps` and `yaml.safe_dump` raise
on NumPy scalars:

```python
json.dumps(msm.get(ms, element='system', bonded_atom_pairs=True))
# TypeError: Object of type int64 is not JSON serializable
```

**It breaks type identity.** `isinstance(np.int64(1), int)` is `False` under NumPy
2.x, so downstream code validating with `isinstance` rejects values this project
documents as integers.

**And it is inconsistent with itself**, which is the part no user can predict: the
same datum arrives with a different type depending on which attribute asked for it.

## What is measured and what is assumed

Measured, on this checkout at `2a77a8cb0`, Python 3.13.14, NumPy 2.4.6:

- The nine attribute/element combinations above, on `181l.pdb` (1441 atoms).
- `get_covalent_blocks` leaves `{'int', 'int64'}`; graph nodes `{'int': 62}`.
- Memory and timing table, over 200 000 integers.
- `json.dumps` and `yaml.safe_dump` raise; pickle of one scalar is 117 bytes against
  5 for an `int`.
- Conversion cost on the ragged returns of a 1441-atom system: 0.94 ms for
  `bonded_atom_pairs` against a 5.10 ms call, 1.00 ms for `bonded_atoms` against
  7.58 ms — **13–18 % of the call itself**, and only on ragged returns.
- `np.array` over a list of Python `int` infers `int64`; `int` and `np.int64` index
  an array identically.
- MolSysMT's own serialisable forms are **already clean**: `MolSysDict.data` contains
  zero NumPy scalars and the emitted `file:molsys_yaml` carries no `!!python` tag.

Assumed:

- That the nine combinations are not the whole surface. Eleven attributes on four
  element levels were swept on one system; the sweep was not exhaustive.

## What was refuted

*It is a cosmetic problem about notebook output.* That is how it was filed and it is
not what it is. Rendering is the symptom; the cost is memory, speed, serialisability
and type identity.

*It is a return-type change requiring a deprecation cycle.* No. The container stays
`list` or `set`; only the type of the elements changes.
`deprecation_policy.md` section 3 covers the type of the returned value, which is
unchanged. This was asserted early in the investigation and is wrong.

*The three named functions are the scope.* Two of the three are already correct.

*Returning NumPy scalars everywhere would be the consistent alternative.* It would be
the larger change and a worse one. Flat attributes return native `int` today;
converting them would break `json.dumps` on the most-used outputs, raise memory and
slow traversal, for a consistency visible only when printing. The only coherent
"all NumPy" option is returning real `ndarray`s — which is right where the data is
rectangular, and impossible where it is ragged: `bonded_atoms` has a different
neighbour count per atom, and an `ndarray(dtype=object)` of lists is again the worst
of both worlds.

*The `dtype` would be lost.* There is no `dtype` in a container holding one Python
object per element, and `np.array` recovers `int64` on the way back.

## Scope and exclusions

Covers ragged, nested and `set` returns from the public API.

Excludes rectangular returns — `ndarray` and `Quantity` — which are correct as they
are and must not be converted. They are the hot paths and the reason the measured
cost stays confined to containers that are already slow.

Excludes the wider question of what the public API returns, now settled in
[INTERFACES.md](../INTERFACES.md) and explained in
`docs/content/developer/core_architecture/return_types.md`. This report is the first
consumer of that rule, not its owner.

## Acceptance criteria

- Ragged, nested and `set` returns from the public API carry native Python scalars.
  A sweep equivalent to the one above reports zero NumPy scalars outside `ndarray`
  and `Quantity`.
- `get_covalent_blocks` returns sets of `int`, without a second change of its own —
  fixing the `get()` delivery is expected to be sufficient, and if it is not, that is
  a finding worth recording.
- `json.dumps` succeeds on the ragged returns listed in *What*.
- A test that fails if a NumPy scalar reappears in a ragged return. Names the `guard`
  field.

## Dependencies and risks

The natural implementation point is the existing return boundary in
`molsysmt/basic/get.py`, where `_standardize` already normalises per attribute and
`_coerce_ids_to_string` already performs exactly this shape of recursive,
shape-preserving normalisation for `*_id` values. That precedent is worth following
rather than inventing a second pattern.

The risk of doing it per function instead is that the surface grows: nine
combinations were found by a non-exhaustive sweep, and each new ragged attribute
would have to remember the rule on its own.

The observable behaviour change is `isinstance(x, int)` going from `False` to `True`
for these elements. It moves toward what the docstrings already claim, but it is a
change and belongs in the release notes.

## Provenance

Host: this development checkout, molsysmt at `2a77a8cb0`. Python 3.13.14,
NumPy 2.4.6. Systems: `181l.pdb` (1441 atoms) and `traj_pentalanine.h5msm`.
2026-08-18.
