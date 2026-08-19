---
summary: Getters build numpy scalars only to have them converted away
issue: uibcdf/molsysmt#172
status: open
opened: 2026-08-19
verification: measured
area: [api, performance, form]
guard:
normative:
blocked_by: []
supersedes: []
closed:
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
