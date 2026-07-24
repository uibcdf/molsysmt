# Bug: `get_sasa._is_orthogonal` tests a box length, so the orthogonal fast path is dead

**Status:** open (found 2026-07-24 while porting the SASA cell-list kernels to Rust)
**Severity:** performance only — results are correct, but the cheap branch is unreachable
**Scope:** `molsysmt/lib/structure/get_sasa.py`

## The defect

```python
def _is_orthogonal(box_s):
    tol = 1e-10
    return (
        abs(box_s[0, 1]) < tol and abs(box_s[0, 2]) < tol and
        abs(box_s[1, 0]) < tol and abs(box_s[1, 2]) < tol and
        abs(box_s[2, 0]) < tol and abs(box_s[2, 2]) < tol   # <-- should be [2, 1]
    )
```

The last term tests `box_s[2, 2]`, which is the **z box length**, not the off-diagonal
`box_s[2, 1]`. A real box always has `box_s[2, 2] >> 1e-10`, so the function can never
return `True`: **`_is_orthogonal` is always false**, and `_mic_wrap_vector` always takes
the triclinic branch — even for a cubic box.

The equivalent helpers in `neighbor_list.py` and `get_contacts_cell_list.py` test
`box_s[2, 1]` correctly, which is what makes this identifiable as a typo rather than a
deliberate choice.

## Impact

Correctness is unaffected: the triclinic wrap is general and gives the right answer for
orthogonal boxes too. The cost is that every orthogonal-box SASA calculation pays for the
general path — a 3x3 Cramer inverse plus a fractional round-trip per distance evaluation —
instead of three `floor` operations.

## Fixing it changes results at the noise floor

The two branches are mathematically identical for an orthogonal box but not bit-identical:
the orthogonal branch divides (`dx / L`) while the triclinic one multiplies by a reciprocal
built from Cramer's rule (`dx * inv00`).

Measured on a probe of 20000 displacements over a cubic box: **11094/20000 samples differ,
max |diff| ≈ 1.78e-15**. Propagated into SASA values for a 250-atom system:
**max |diff| ≈ 4.4e-16, relative ≈ 4.4e-16** — machine epsilon, with no occlusion decision
flipping (a flip would have shown up as a ~1e-3 jump).

So the fix is scientifically identical but will perturb the last bits of stored reference
values. Any regression test pinned to exact bytes on an orthogonal box needs re-baselining
at a scientific tolerance.

## Suggested fix

1. Change `box_s[2, 2]` to `box_s[2, 1]`.
2. Re-baseline any exact-value SASA fixtures to a tolerance (1e-9 is ample; the change is
   at 1e-16).
3. Consider factoring the three copies of `_is_orthogonal` (`get_sasa.py`,
   `neighbor_list.py`, and the MIC helpers) into one shared implementation so a typo in one
   cannot diverge from the others again.

## Status in the Rust migration

The Rust port in `experiment/rust-numba-pilot` **uses the corrected check**. The policy
there is: replicate the oracle where it is right, correct it where it is wrong, and report.
Consequently `get_mic_sasa_cell_list` is compared against Numba at scientific tolerance
(1e-9) rather than bit-for-bit on orthogonal boxes; the divergence is documented in
`src/sasa.rs` and measured above. Compare with
`dihedral_angles_broadcast_mismatch_pbc.md`, where the oracle is not merely slow but
undefined.
