# `get_dihedral_quartets(with_blocks=True)` raises on ragged block sets

**Reported:** 2026-08-03, found while renaming `get_covalent_chains`. Pre-existing:
the failing line is untouched by that work.

**Status:** **RESOLVED (archived 2026-08-03).** See *Resolution*.

**Severity:** the documented `with_blocks` option of a stable public function was
unusable on any real system. No incorrect result: it raised.

## Reproduction

```python
import molsysmt as msm
from molsysmt import systems

molsys = msm.convert(systems['T4 lysozyme L99A']['181l.h5msm'])
msm.topology.get_dihedral_quartets(molsys, phi=True)                    # -> (161, 4), fine
msm.topology.get_dihedral_quartets(molsys, phi=True, with_blocks=True)  # -> ValueError
```

```
ValueError: setting an array element with a sequence. The requested array has an
inhomogeneous shape after 1 dimensions. The detected shape was (161,) + inhomogeneous part.
```

## Cause

`molsysmt/topology/get_dihedral_quartets.py:95`:

```python
all_blocks.append(np.array(blocks))
```

`blocks` is a list with one entry per quartet, and each entry is a list of sets of
atom indices of differing sizes. NumPy refuses to build an array from ragged nested
sequences, and has done since it stopped accepting them silently as `dtype=object`.

## Impact

`with_blocks=True` is how a caller obtains the two groups of atoms that move when a
dihedral angle is rotated, which is the reason `get_covalent_blocks` accepts
`remove_bonds` at all. `molsysmt.structure.set_dihedral_angles` does not go through
this path — it calls `get_covalent_blocks` directly — so rotation still works. It is
the public convenience that is broken.

The documentation advertises the option:
`docs/content/user/tools/topology/get_dihedral_quartets.ipynb` describes
`with_blocks` and shows it in use.

## Resolution

`np.array(blocks)` is gone: `all_blocks.append(blocks)` keeps the plain list. The
structure is ragged by nature — each quartet's blocks have different sizes — and both
consumers index it by quartet and then by block, which a list already supports. The
docstring now states the shape instead of leaving it to `np.array`.

On T4 lysozyme, `phi=True, with_blocks=True` returns 161 quartets and 161 block
entries. **158 quartets split into two blocks and 3 into one, and those 3 are the
prolines**: cutting the N-CA bond of a proline disconnects nothing because its ring
holds the two halves together. That is the chemically correct answer, and the
regression test asserts it by name rather than accepting any count.

Guarded by `tests/topology/get_dihedral_quartets/test_get_dihedral_quartets_with_blocks.py`,
which also reproduces the exact indexing the tutorial uses, `phi_blocks[2][0]`.

## Acceptance

- `get_dihedral_quartets(molsys, phi=True, with_blocks=True)` returns the quartets
  and the per-quartet blocks on T4 lysozyme.
- The return type of the blocks is stated in the docstring. Sets of atom indices are
  not a rectangular array, so either an object array or a list of lists of sets has
  to be chosen deliberately rather than fall out of `np.array`.
- A regression test covers a system where quartets have blocks of different sizes,
  which is every real one.
- The notebook cell that shows `with_blocks` executes.
