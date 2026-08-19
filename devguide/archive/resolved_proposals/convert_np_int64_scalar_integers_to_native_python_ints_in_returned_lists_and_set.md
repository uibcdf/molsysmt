---
summary: Public returns deliver numpy scalars where the rest of the API delivers native ones
issue: uibcdf/molsysmt#165
status: resolved
opened: 2026-08-17
closed: 2026-08-19
verification: measured
area: [api, basic, topology]
guard: tests/basic/get/test_native_scalar_delivery.py
normative: devguide/INTERFACES.md
blocked_by: []
supersedes: []
---

# Public returns deliver NumPy scalars where the rest of the API delivers native ones

**Reported:** 2026-08-17 during a User Guide audit, as a rendering complaint about
`np.int64(...)` in notebook output. **Rewritten 2026-08-18** after an audit that
found the original scope wrong in both directions and the cause elsewhere.
**Status:** resolved 2026-08-19 in `375d4347c`. The rule is written in
[INTERFACES.md](../INTERFACES.md), *Scalar types in returned values*, and the code
now follows it.

## What

`molsysmt.basic.get` returns **native Python `int`** for some attributes and
**`np.int64`** for others. Same library, same kind of datum, two types:

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

And the surface is not in `topology` at all. Sweeping the 118-attribute catalogue
over 9 element levels, 2 selections and 4 molecular systems finds **45
attribute/element combinations across 23 attributes**, in two distinct families.

**Containers holding NumPy scalars** — 11 attributes:

```
bonded_atom_pairs        atom, bond, system     chain_index      component, entity, group, molecule
bonded_atoms             atom, system           component_index  chain, entity, molecule
inner_bonded_atoms       atom, system           entity_index     component
inner_bonded_atom_pairs  atom, system           group_index      component
chain_name               molecule               molecule_index   component
chain_type               molecule
```

`chain_name` and `chain_type` deliver `numpy.str_`, so this is not a problem about
integers. It is a problem about NumPy scalars.

**Bare NumPy scalars, with no container at all** — the 12 counters:

```
n_amino_acids  n_dnas   n_ions          n_lipids   n_nucleotides      n_peptides
n_proteins     n_rnas   n_saccharides   n_waters   n_polysaccharides  n_small_molecules
```

This family is the starkest statement of the inconsistency:

```python
>>> msm.get(ms, element='atom', n_atoms=True)     # int,   json.dumps OK
1441
>>> msm.get(ms, element='atom', n_waters=True)    # int64, json.dumps raises
136
```

Counting atoms and counting waters are the same question, and they answer with
different types. There is no container here and no `dtype` to preserve — it is one
number.

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

- 45 attribute/element combinations across 23 attributes, from sweeping the whole
  118-attribute catalogue over 9 element levels and 2 selections on four systems:
  `181l.pdb` (protein, water, ions), the POPC membrane (lipids), the pentalanine
  trajectory, and `4v4z.bcif.gz` (ribosome, RNA). It appears in all four, so it does
  not depend on chemical content.
- Scalar types found: `int64` and `str_`.
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

- Building a flat list of 500 000 integers: 35.1 ms by iterating the array against
  15.3 ms through `tolist()`. Building then converting afterwards costs 80.0 ms and
  peaks at 36.3 MB, against 13.4 ms and 20.0 MB for `tolist()` at the source.
- A recursive normaliser at the return boundary costs **86.0 ms on already-clean
  data**, five times what `tolist()` costs doing the whole job from scratch.

Assumed:

- That 45 is not the whole surface. The count went 9 → 30 → 45 as the sweep widened,
  and it still covers only `get()`: functions in `topology`, `structure` and `build`
  that assemble their own structures, `set()`, and the inter-form conversion paths
  are not included. The real figure is a lower bound.

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
the larger change and a worse one. Most attributes return native `int` today;
converting them would break `json.dumps` on the most-used outputs, raise memory and
slow traversal, for a consistency visible only when printing.

*Rectangular returns should become arrays.* No — and this report asserted it in an
earlier revision. Shape is not the criterion; the nature of the datum is.
`bonded_atom_pairs` is rectangular, *n* rows of two, and is correctly a `list`,
because it is a relation between atoms and not a magnitude anyone computes on.
Reasoning from shape also fails on its own terms: `component_index` per molecule is
rectangular in every system where each molecule has one component and ragged the
moment one does not, and an attribute cannot change container between systems.
Because no container migration is needed, no return type changes, and
`deprecation_policy.md` section 3 does not apply — this report carries no deadline
of any kind.

*The `dtype` would be lost.* There is no `dtype` in a container holding one Python
object per element, and `np.array` recovers `int64` on the way back.

## Scope and exclusions

Covers scalars delivered inside Python containers, and bare scalars, from the public
API.

Excludes `ndarray` and `Quantity` returns, which are correct as they are and must not
be converted. They carry the numeric magnitudes, they are the hot paths, and the
measured cost stays confined to containers that are already Python-level.

Excludes which container each attribute should use. That question is settled by
[INTERFACES.md](../INTERFACES.md) and nothing here proposes moving an attribute from
one container to another.

Excludes the wider question of what the public API returns, now settled in
[INTERFACES.md](../INTERFACES.md) and explained in
`docs/content/developer/core_architecture/return_types.md`. This report is the first
consumer of that rule, not its owner.

## Acceptance criteria

- Every scalar delivered inside a Python container, and every bare scalar returned
  by the public API, is a native Python type. A sweep equivalent to the one above
  reports zero NumPy scalars outside `ndarray` and `Quantity`.
- `get_covalent_blocks` returns sets of `int`, without a second change of its own —
  fixing the `get()` delivery is expected to be sufficient, and if it is not, that is
  a finding worth recording.
- `json.dumps` succeeds on every return listed in *What*.
- A test that sweeps the attribute catalogue over every element level and fails if a
  NumPy scalar reappears outside `ndarray` and `Quantity`. Names the `guard` field.

## Dependencies and risks

**Normalise at the source, not at the return boundary.** The boundary is the
tempting choice — one place, and `_coerce_ids_to_string` in `molsysmt/basic/get.py`
is an existing precedent for recursive, shape-preserving normalisation. It is the
wrong choice here, and measurement says so: a recursive normaliser costs 86.0 ms
walking 500 000 already-clean integers, five times what `tolist()` costs doing the
entire conversion from scratch. A universal net taxes every call, including the
majority that need nothing.

`ndarray.tolist()` where the structures are built, and `.item()` for the bare
counters, does the conversion in C in one pass and never materialises the boxed
scalars. It is roughly six times cheaper than building and converting, and it is
what the already-correct attributes do today.

The cost of that choice is that the fix lands in several places and a new attribute
can forget the rule. That is what the guard is for, and detecting it in CI is free
where preventing it at run time is not.

The observable behaviour change is `isinstance(x, int)` going from `False` to `True`
for these elements. It moves toward what the docstrings already claim, but it is a
change and belongs in the release notes.

## Provenance

Host: this development checkout, molsysmt at `2a77a8cb0`. Python 3.13.14,
NumPy 2.4.6. Systems: `181l.pdb` (1441 atoms) and `traj_pentalanine.h5msm`.
2026-08-18.

## Resolution — 2026-08-19

`375d4347c` normalises the 23 affected attributes at the delivery boundary in
`molsysmt/basic/get.py`, and `tests/basic/get/test_native_scalar_delivery.py` sweeps
the whole 118-attribute catalogue over every element level to keep it that way.

The normalisation is applied to a named set rather than to every return. A blanket
pass must walk a value to discover whether it needs anything, and on a 78 974-atom
system that costs 12.4 ms on the already-clean `atom_index` against a 6.1 ms call —
tripling the most used attribute in the library to achieve nothing. Membership is
O(1); the 23 pay 17-34 % of their own call.

`get_covalent_blocks` was fixed by this without a change of its own, confirming the
diagnosis recorded above: its mixed sets came from NetworkX using the delivered
bond-pair objects as adjacency keys.

Full suite on the resolved tree: 10 100 passed, 11 skipped.

**What this does not do.** The getters still build the NumPy scalars that are then
converted away, and building them is itself the slow part —
`itertuples` over the bond table costs 91.2 ms where `to_numpy().tolist()` costs
11.0 ms for the same result. That is tracked as
[uibcdf/molsysmt#172](https://github.com/uibcdf/molsysmt/issues/172), which does not
supersede this one: the delivery net stays whatever happens to the producers,
because 89 adapters carry hand-written getters and this guard certifies the ones
that exist today, not the next one.
