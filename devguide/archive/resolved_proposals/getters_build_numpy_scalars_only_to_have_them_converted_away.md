---
summary: Getters build numpy scalars only to have them converted away
issue: uibcdf/molsysmt#172
status: resolved
opened: 2026-08-19
verification: measured
area: [api, performance, form]
guard:
normative: devguide/form_adapter_implementation.md
blocked_by: []
supersedes: []
closed: 2026-08-19
---

# Getters build NumPy scalars only to have them converted away

**Reported:** 2026-08-19, while implementing
[uibcdf/molsysmt#165](https://github.com/uibcdf/molsysmt/issues/165). Fixing the
delivered types exposed that producing the wrong types is itself the slow part.
**Status:** open proposal.

## What

Attribute getters assemble Python containers by iterating NumPy arrays and pandas
frames one element at a time. Every element so produced is a boxed NumPy scalar,
which `get()` then converts back to a native one at the delivery boundary. The
conversion is a contract requirement and is not what this report questions — the
production is.

Doing it the other way round is not a trade-off. It is faster, and the result is
already native:

```python
# molsysmt/form/molsysmt_Topology/get_topological_attributes.py, get_bonded_atom_pairs_from_bond
output = [[bond.atom1_index, bond.atom2_index] for bond in bonds.itertuples(index=False)]
# 91.2 ms, leaves are np.int64

output = bonds[['atom1_index', 'atom2_index']].to_numpy().tolist()
# 11.0 ms, leaves are int, identical result
```

## How

Three patterns, each with a mechanical replacement:

| Pattern | Where it produces scalars | Replacement | Measured |
| --- | --- | --- | --- |
| `DataFrame.itertuples()` | one namedtuple and two NumPy scalars per row | `to_numpy().tolist()` | **8.3x faster** |
| `to_numpy()` then a Python loop | one NumPy scalar per element read | `.tolist()`, same loop | **1.4x faster** |
| `np.count_nonzero(...)` returned directly | one bare NumPy scalar | `int(...)` | free |

The reason is the same in all three: indexing or iterating an `ndarray` from Python
allocates an object per element. `tolist()` does the same work in C in a single
pass, and a Python loop over a `list` is faster than over an `ndarray` because
nothing is boxed on the way.

The bond family has a single root. `get_bonded_atoms_from_atom`,
`get_bonded_atom_pairs_from_atom` and the `inner_*` variants all consume
`get_bonded_atom_pairs_from_bond`; none produces scalars of its own. Fixing the root
cleans the family without touching it — the same relationship that made
`get_covalent_blocks` correct itself once `get()` delivered clean pairs.

## Why

Not correctness. [#165](https://github.com/uibcdf/molsysmt/issues/165) settled the
delivered types and its guard keeps them settled. This is about the work discarded
on the way there, and it is not marginal: on a 78 974-atom membrane, the bond-pair
root spends 91.2 ms building 130 884 objects that are then thrown away, where 11.0 ms
would have produced the final answer directly.

It also shrinks what the delivery net has to do. Every root repaired is an attribute
the net walks and finds nothing to change.

## What is measured and what is assumed

Measured on this checkout at `375d4347c`, Python 3.13.14, NumPy 2.4.6, on the POPC
membrane (78 974 atoms, 65 442 bonds):

- `itertuples` 91.2 ms against `to_numpy().tolist()` 11.0 ms, results identical.
- Python loop over `ndarray` 44.6 ms against the same loop over `list` 31.3 ms,
  on 79 000 elements.
- `itertuples(` appears 16 times in 6 adapter files.
- `np.count_nonzero` appears 48 times across `get_topological_attributes.py`.

Assumed, and deliberately not quantified:

- How many of the 402 `to_numpy()` calls in `get_topological_attributes.py` feed a
  Python loop rather than a vectorised operation. Most are correct as they stand and
  must not be touched: an array consumed by NumPy should remain an array. This one
  needs reading case by case, and no total is offered here.

During #165 the surface of that report was estimated at 9 combinations, measured at
30, then at 45; and the cost of a source-level fix was quoted as 820 definitions,
which counted consumers rather than producers. Counts in this area have been wrong
in both directions, so the two bounded patterns are stated with their measurements
and the third is stated as unmeasured.

## What was refuted

*Normalising at the source and normalising at delivery are alternatives.* They are
not, and #165 chose delivery for the contract because a blanket walk costs 12.4 ms on
an already-clean `atom_index` against a 6.1 ms call. This report is about the
producers; the net stays regardless, because 89 adapters carry hand-written getters
and a guard certifies the ones that exist today, not the next one.

*The whole surface is 820 definitions.* That figure counted every consumer of the
affected attributes. The bond family alone collapses to one root.

## Scope and exclusions

Covers getters that assemble Python containers or return bare counts.

Excludes `to_numpy()` calls feeding vectorised NumPy operations, which are correct.

Excludes the delivery net and its guard in `molsysmt/basic/get.py`, which stay.
Removing them is explicitly not an outcome of this work.

Excludes the Rust boundary, which is unaffected: it receives `f64` arrays and plain
integer scalars, never ragged containers, and PyO3 accepts native and NumPy integers
alike within measurement noise.

## Acceptance criteria

- The three patterns are replaced where they produce delivered values, and each
  replacement is shown to be at least as fast on a system of realistic size.
- The `#165` guard still passes, and the delivery net finds nothing to convert for
  the repaired attributes — verifiable by asserting the value is already native
  before normalisation.
- A benchmark that fails if the bond-pair root regresses to per-row iteration.
  Names the `guard` field.

## Dependencies and risks

The risk is the shape of the change rather than its content: a mechanical
substitution across adapter files is exactly the operation that produced the
regression repaired in `9f4fbd515` on 2026-08-18. It should be done in small,
measured batches with the full suite between them, not as one sweep.

`to_numpy().tolist()` on a column holding pandas nullable integers (`Int64`) yields
`None` for missing values where the current path yields something else. Attributes
whose columns are nullable need checking before substitution.

## Provenance

Host: this development checkout, molsysmt at `375d4347c`. Python 3.13.14,
NumPy 2.4.6. System: POPC membrane, 78 974 atoms and 65 442 bonds. 2026-08-19.

## Resolution — 2026-08-19

Two patterns done, the third measured and declined. The rule is written into
`form_adapter_implementation.md` so new getters are built the fast way without
anyone rewriting the ones that work.

### Done

**The bond-pair root**, in `57e2a2e25`. `itertuples` replaced by
`to_numpy().tolist()` in the three branches that build it: 98.5 ms to 15.0 ms over
65 442 bonds for an identical result. It is the root of a family, so
`bonded_atoms`, `bonded_atom_pairs` and both `inner_*` variants are clean with three
substitutions. Delivered cost on a 78 974-atom system: `bonded_atom_pairs` 260.8 ms
to 208.6 ms, `bonded_atoms` 589.6 ms to 533.1 ms.

**The counters.** All 48 `np.count_nonzero` results wrapped in `int()`, so the twelve
`n_*` attributes are native from the source as `n_atoms` already was.

### Declined, with the measurement

The third pattern is `to_numpy()` feeding a Python loop. Its surface is **13
getters**, not the 402 `to_numpy()` calls and not the 60 a first static pass
suggested. Found by executing all 488 getters of `molsysmt_Topology` and inspecting
their raw output, which is ground truth where the static classification was not:

```
get_chain_id_from_molecule          get_component_index_from_chain
get_chain_index_from_component      get_component_index_from_entity
get_chain_index_from_entity         get_component_index_from_molecule
get_chain_index_from_group          get_entity_index_from_component
get_chain_index_from_molecule       get_group_index_from_component
get_chain_name_from_molecule        get_molecule_index_from_component
get_chain_type_from_molecule
```

They are declined on two grounds.

**The gain is about 1 % where a caller can see it.** The loop itself improves 1.48x —
15.7 ms to 10.7 ms over 78 974 atoms — but it is a small part of a call that runs
around 533 ms. And there is no correctness gain at all: `uibcdf/molsysmt#165`
normalises the delivered values and its guard sweeps the whole catalogue, so what
these getters produce internally never reaches a caller as a NumPy scalar.

**The mechanical route does not work here.** Three attempts failed, each differently:
the first converted `aux_dict`, which is a dict; the second converted an array that
is *subscripted* by fancy indexing, which then raises `only integer scalar arrays can
be converted to a scalar index`; the third left three getters raising and four still
leaking. These functions mix iterating one array, indexing another element by
element, and using a third as an index, and the decision is per variable rather than
per function.

A baseline of all 488 getter outputs, captured before each attempt and compared
after, is what caught all three. Without it the second attempt would have been
committed with three broken getters.

### What was refuted

*The surface is the 402 `to_numpy()` calls.* Most feed vectorised operations and must
not be touched. A first classification put 60 in Python loops; of those, the ones
that actually leak are 13.

*`arr[indices].tolist()` is a candidate.* It is already correct — fancy indexing
followed by a single conversion — and accounts for most of what a syntactic pass
flags as scalar indexing.

*Iterating a list is enough faster to justify the change.* It is faster, and by less
than it looks: including the `tolist()` call the synthetic gain is 1.03x to 1.24x,
and 1.48x on the real function. Neither is 1 % of a call away from being invisible.
