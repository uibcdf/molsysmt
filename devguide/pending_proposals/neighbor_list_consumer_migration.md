# Proposal: migrate remaining spatial consumers onto the shared neighbour-list primitive

**Status:** pending (post-1.0)
**Owner:** MolSysMT
**Related:** `sasa_methodologies_and_acceleration_post_1_0.md`

## Context

`molsysmt/lib/structure/neighbor_list.py` provides a reusable CPU cell-list
neighbour search returning CSR neighbour lists (`neighbor_list_csr`) and pair
arrays (`neighbor_pairs`), vacuum and periodic, with query/ref generality. It
already backs `physchem.get_sasa` (`use_cell_list`) and `structure.get_contacts`
(the former per-function `get_contacts_cell_list` was folded into it). Two more
consumers still run their own O(N²) neighbour search and should migrate onto the
shared primitive, each behind a numerical/scientific parity test.

## 1. `structure.get_neighbors` — threshold mode

Currently the threshold mode builds a **full pairwise distance matrix** via
`get_distances` and filters it with `np.argwhere(all_dists <= threshold)`. This is
O(N²) in memory and time. The cell-list primitive returns exactly the within-cutoff
candidates in ~O(N).

Not a drop-in: `get_neighbors` also **returns the neighbour distances** and supports
several output modes (`pairs`, `unique_pairs`, `mutual_only`, `sorted`,
`output_type='numpy.ndarray'`). The migration must:
- use `neighbor_list_csr(cutoff=threshold)` to obtain candidates;
- compute distances **only for the candidates** (not the full matrix) to preserve
  the distance return and `sorted`/nearest ordering;
- preserve `unique_pairs` / `mutual_only` semantics;
- keep parity tests across every output mode.

The **fixed-count mode** (`n_neighbors`, k-nearest) does **not** benefit from a
fixed-cutoff cell-list and stays on the distance-based path.

## 2. `hbonds` candidate-pair generation

The h-bond engines (`get_buch_hbonds`, `get_luzard_chandler_hbonds`) enumerate
donor–acceptor candidate pairs within a distance cutoff — a natural query≠ref use
of `neighbor_pairs` (query = donors, ref = acceptors). Each engine has its own
candidate logic and scientific acceptance criteria, so migration requires
per-engine scientific parity tests.

## Sequencing and risk

Both touch tested public/scientific functions, so they are deliberately deferred
past the 1.0 freeze: the primitive is already in place and proven, and these are
incremental, parity-gated speedups rather than contract changes. `get_neighbors`
threshold mode is the smaller, better-scoped item and should come first.
