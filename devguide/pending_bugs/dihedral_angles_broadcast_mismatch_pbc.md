# Bug: broadcast-shaped `angles` reads out of bounds on the periodic path of `set_dihedral_angles`

**Status:** open (found 2026-07-24 while porting these kernels to Rust)
**Severity:** silent wrong results or crash — Numba `njit` does not bounds-check by default
**Scope:** `molsysmt.structure.set_dihedral_angles` (public) and the `lib` kernels it dispatches to

## Symptom

`molsysmt.structure.set_dihedral_angles` documents its `angles` argument as:

> must be **compatible with** shape `(n_structures, n_quartets)`

i.e. broadcast-compatible. The value is passed straight through
(`angles = np.asarray(puw.get_value(angles, to_unit='radians'), dtype=np.float64)`)
with no `broadcast_to`, and then dispatched to one of two kernels depending only on
whether the system has a box:

| branch | kernel | broadcasting |
|---|---|---|
| no PBC | `lib.structure.set_dihedral_angles` | **yes** — `inc_structures`/`inc_angles` collapse to index 0 when `angles.shape[0]==1` or `angles.shape[1]==1`, reading `angles[ll, mm]` |
| PBC | `lib.structure.set_mic_dihedral_angles` | **no** — indexes `angles[ii, aa]` directly |

So an `angles` array of shape `(1, n_quartets)` applied to a system with
`n_structures > 1`:

- works as documented when the system has **no** box;
- indexes `angles[ii, aa]` with `ii >= 1` when the system **has** a box.

Because these kernels are `njit` without `boundscheck`, that out-of-range read is not an
`IndexError`: it reads adjacent memory. The result is silently wrong coordinates, or a
crash, depending on the allocation.

The two call sites are a dozen lines apart in the same function
(`molsysmt/structure/set_dihedral_angles.py`), so the behaviour of a documented input
flips purely on the presence of a box.

## Second, related asymmetry (no user impact today)

The four `lib` variants do not agree on how structures are selected either:

| kernel | args | structures processed |
|---|---|---|
| `set_dihedral_angles` | 4 | all |
| `set_mic_dihedral_angles` | 5 | all |
| `shift_dihedral_angles` | 5 | subset via `structure_indices` |
| `shift_mic_dihedral_angles` | 6 | subset via `structure_indices` |

Only the `shift_*` kernels accept `structure_indices` — and **those two kernels have no
callers anywhere outside `lib/`**: the public `structure.shift_dihedral_angles` computes
the current angles, adds the shifts and delegates to `set_dihedral_angles`. So the only
variants offering structure selection are dead code, while the ones actually used cannot
restrict to a subset.

## Suggested fix (scope)

1. **Decide one broadcasting contract** and apply it to both `set_*` kernels — either
   both broadcast, or neither does and the caller normalises with `np.broadcast_to`
   before dispatch. Normalising in the public function is the smaller, safer change and
   removes the branch-dependent behaviour entirely.
2. **Add regression tests** covering `angles` of shape `(1, n_quartets)`,
   `(n_structures, 1)` and `(n_structures, n_quartets)` on both the PBC and non-PBC
   paths — currently nothing exercises the broadcast shapes on the periodic branch.
3. **Resolve the dead `shift_*` kernels**: delete them, or wire them up and harmonise
   `structure_indices` across all four.
4. Consider enabling `boundscheck` in debug/test builds for the `lib` kernels so this
   class of defect fails loudly instead of reading adjacent memory.

## Note for the Rust migration

The Rust ports in `experiment/rust-numba-pilot` **replicate this asymmetry faithfully**,
including the broadcasting in the vacuum kernel and its absence in the periodic one. That
is deliberate: bit-for-bit parity against the Numba oracle is the safety mechanism of the
migration, so behaviour changes must not be smuggled in inside a port. Fix this upstream
first; the ports then follow the corrected behaviour.
