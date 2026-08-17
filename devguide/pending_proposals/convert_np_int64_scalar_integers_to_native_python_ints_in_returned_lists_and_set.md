---
summary: convert np.int64 scalar integers to native python ints in returned lists and sets
issue: uibcdf/molsysmt#165
status: open
opened: 2026-08-17
closed:
verification: asserted
area: [docs]
guard:
normative:
blocked_by: []
supersedes: []
---

# Convert `np.int64` scalar integers to native Python `int`s in returned lists and sets

**Reported:** 2026-08-17 during User Guide audit of `docs/content/user/tools/topology/get_covalent_blocks.ipynb` and `get_dihedral_quartets.ipynb`.
**Status:** Open proposal under review.

## What

In several tutorial outputs across the User Guide (e.g. `get_covalent_blocks.ipynb` and `get_dihedral_quartets.ipynb`), returned lists, sets, or tuples of atom/group indices render NumPy scalar integers explicitly as `np.int64(...)` (e.g. `[{np.int64(0), np.int64(1), ...}]`).

Printing `np.int64(...)` wrapper representations in Python lists/sets bloats notebook cell outputs, increases vertical page length, and makes documentation outputs noticeably less readable.

## How

Evaluate whether public API functions returning nested Python structures (lists, sets, tuples, or dicts of indices) should convert internal `np.int64` scalar values to native Python `int` objects prior to returning:
1. Identify functions returning nested collections of indices (e.g., `get_covalent_blocks`, `get_dihedral_quartets`, `get_covalent_paths`).
2. Apply `int(x)` conversion or recursively cast nested integer elements when constructing return values.
3. Compare performance and memory impact vs rendering clarity.

## Why

Native Python integers render cleanly as plain numbers (e.g. `{0, 1, 2}`) rather than verbose type-wrapped strings (`{np.int64(0), np.int64(1), np.int64(2)}`), dramatically improving documentation output aesthetic quality and readability without breaking numeric equality or indexing behavior.
