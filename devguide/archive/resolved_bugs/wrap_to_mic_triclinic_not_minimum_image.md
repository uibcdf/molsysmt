# Bug: `wrap_to_mic` does not return the minimum image on triclinic boxes

**Status:** **RESOLVED by the Rust-only cut (archived 2026-07-28).**
**Severity when open:** wrong results — silently returned a non-minimal image, by whole box lengths
**Scope when open:** `molsysmt/lib/pbc/wrap_to_mic.py`, both
`wrap_to_mic_vector_single_structure` and the whole-system `wrap_to_mic`

> ## Resolution
>
> The defective 27-image search existed only in the Numba implementation, which
> Segment D removed. The Rust replacement in `rust/src/pbc.rs` routes every
> minimum-image wrap through the shared reduced-cell mechanism (`mic::mic_vector`),
> which searches around the *wrapped* candidate rather than around the original
> vector, and is therefore minimal on triclinic boxes as well as orthogonal ones.
>
> The related completeness work on the cell list and cell-list SASA is recorded in
> [`triclinic_cell_list_completeness.md`](../resolved_proposals/triclinic_cell_list_completeness.md),
> validated against an all-pairs ±2 ground truth and the brute-force SASA on mild and
> heavily skewed boxes.
>
> Everything below is the original report, retained for provenance. It describes the
> deleted Numba implementation and does not describe current behaviour.

## Symptom

`wrap_to_mic` is supposed to apply the minimum image convention. On an **orthogonal** box
it does. On a **triclinic** box it usually does not.

Measured on `box = [[6,0,0], [1.5,6.5,0], [0.8,1.1,7]]` with 300 random vectors drawn
from `uniform(-20, 20)` (i.e. a few box lengths outside the cell):

| implementation | returns the minimum image |
|---|---|
| orthogonal branch | always |
| triclinic branch (current) | **55/300** |

The failures are not marginal: the returned vector can be a whole box length longer than
the true minimum image.

## Cause

The triclinic branch does two things, and they do not compose:

```python
vaux[0]=vaux[0]-np.floor(vaux[0])       # wrap to the [0,1) fractional cell
...
dmin=dot_product(output,output)
for ii in [-1,0,1]:
    vaux=vector+ii*box[0,:]             # <-- images of the ORIGINAL vector
    ...
```

1. The fractional wrap uses `floor(x)`, which lands in the **primitive cell** `[0,1)`.
   The minimum image needs the *centred* cell `[-0.5, 0.5)`, i.e. `floor(x + 0.5)` — which
   is exactly what the orthogonal branch a few lines above does.
2. The 27-image search that follows iterates over images of **`vector`**, the original
   input, not of the wrapped candidate. When the input lies several box lengths outside
   the cell, all 27 candidates are equally far away, so the corner-cell wrap from step 1
   wins by default and the search cannot repair it.

## Evidence that this is a defect, not a design choice

`unwrap.py`, in the same package, faces the identical problem and **gets it right**: it
wraps with `round()` (equivalent to the centred `floor(x+0.5)`) and then searches the 27
images *of the wrapped delta*:

```python
vaux[0]=vaux[0]-round(vaux[0])
...
vmin=delta
for kk in [-1,0,1]:
    vaux=delta+kk*tmp_box[0,:]          # images of the WRAPPED delta
```

So the correct pattern already exists in the codebase, one file away.

## Suggested fix

Searching around the wrapped candidate is sufficient on its own; centring the fractional
wrap as well is redundant but makes the two branches consistent and shrinks the search:

| variant | minimum image |
|---|---|
| current | 55/300 |
| `floor(x+0.5)` only | 260/300 |
| **search around the wrapped vector** | **300/300** |
| both | 300/300 |

Add a regression test asserting the minimum-image property directly (for every returned
`w`, no `w + i*a + j*b + k*c` with `i,j,k ∈ {-1,0,1}` is shorter) on **both** box types —
the current suite has nothing that would have caught this.

Note a remaining limitation, shared with `unwrap` and not addressed by the fix: a ±1 shell
is only exhaustive for reasonably conditioned cells. A strongly skewed box needs a reduced
(Niggli) cell for a general guarantee.

## Status in the Rust migration

The Rust port in `experiment/rust-numba-pilot` **searches around the wrapped candidate**,
so it returns the minimum image in all sampled cases. Per the migration policy (bit-parity
is the gate only where the oracle is defined), the parity assertion for
`wrap_to_mic` + triclinic is therefore replaced by a property assertion, and the test
fails loudly if upstream is ever fixed:

```python
assert numba_ok < len(vectors), (
    "upstream now returns the minimum image on triclinic boxes -- the bug this "
    "divergence works around has been fixed, so drop the correction in pbc.rs and "
    "restore plain parity")
```

Related: `sasa_is_orthogonal_typo.md`, `dihedral_angles_broadcast_mismatch_pbc.md`.


## Update (2026-07-25): fixed on the wrap-based Rust paths

The Rust MIC now uses a reduced-cell minimum image (`mic::mic_vector`) on every wrap-based
kernel — distances, angles, dihedrals, set/shift dihedral ops. On those paths the bug is
fixed: the reduced cell finds the true minimum image (validated against a ±2 all-pairs
ground truth), where the ±1 (27-image) search could miss a second-neighbour image. The grid-based cell list and cell-list SASA are **now also fixed** (perpendicular-thickness
grid sizing + lattice fractional binning + reduced-cell wrap), validated against an all-pairs
±2 ground truth and the brute-force SASA; see the resolved
[`triclinic_cell_list_completeness.md`](../resolved_proposals/triclinic_cell_list_completeness.md).
The whole Rust MIC surface is now correct on triclinic boxes.
