---
summary: Add compact='molecule' to the wrapping functions
issue: uibcdf/molsysmt#173
status: open
opened: 2026-08-19
closed:
verification: measured
area: [pbc, api]
guard:
normative:
blocked_by: []
supersedes: []
---

# Add `compact='molecule'` to the wrapping functions

**Reported:** 2026-08-19, while replacing `keep_covalent_bonds` with `compact` in
`msm.pbc.wrap_to_pbc` and `msm.pbc.wrap_to_mic`. Post-1.0 by decision: the argument
ships with `False` and `'component'`, and adding a value to it later is additive.
**Status:** open proposal.

## What

`compact` names the element kept whole when wrapping. It accepts `False` and
`'component'`; `'molecule'` is missing and is a different answer, not a synonym.

```python
>>> msm.pbc.wrap_to_pbc(molsys, compact='molecule')
ArgumentError: Error in argument 'compact' with value 'molecule'.
```

## How

The wrapping kernels reconstruct blocks from the bond graph:
`reconstruct_and_wrap_covalent_blocks` receives `bonded_pairs` and
`_connected_blocks` walks them into connected components. Compacting by molecule
needs the same reconstruction over a different partition — grouping by
`molecule_index` rather than by connectivity — so the algorithm is reusable and the
work is in supplying the partition, not in the traversal.

That is an assessment from reading the code, not a measurement. Whether the kernel
takes a partition cleanly or assumes edges throughout has not been verified.

## Why

The two units genuinely differ, and a covalent component can be larger than a
molecule. Measured on `1ATP`:

```
components: 102 | molecules: 108
components spanning more than one molecule: 1
  component 0 -> molecules [0, 2, 3, 4, 39, 53, 86]
                 types ['protein', 'ion', 'ion', 'small molecule', 'water', 'water', 'water']
```

One covalent component holds the kinase, two magnesium ions, the ATP and three
waters, joined through metal coordination. With `compact='component'` that whole set
translates as one piece; with `compact='molecule'` each part moves on its own. Both
are legitimate and a user cannot currently ask for the second.

Across the bundled systems the two coincide more often than not — T4 lysozyme,
TcTIM, Barnase-Barstar and 2HGR all report equal counts — which is why
`'component'` is the right default and why this is not urgent.

## What is measured and what is assumed

Measured, on this checkout, over the bundled demo systems:

| system | components | molecules |
| --- | --- | --- |
| T4 lysozyme L99A | 141 | 141 |
| TcTIM | 167 | 167 |
| Barnase-Barstar | 2 | 2 |
| 2HGR | 24 | 24 |
| **1ATP** | **102** | **108** |

Assumed:

- That supplying a molecule partition to the existing reconstruction is
  straightforward. Read from the code, not executed.

## What was refuted

*`compact='atom'` is the natural name for the non-compacting case.* It reads as
"compact the atom", which means nothing. `compact=False` says what happens.

*Component and molecule are the same thing in practice, so one value suffices.* They
coincide in four of five bundled systems and differ in the fifth, where a single
component spans seven molecules.

## Scope and exclusions

Covers `compact` in `msm.pbc.wrap_to_pbc` and `msm.pbc.wrap_to_mic`.

Excludes the other elements of the hierarchy — `group`, `chain`, `entity`. They are
expressible in the same enum and nobody has asked for them; adding one later is
additive in exactly the way this proposal is.

Excludes the degenerate case, already settled: a system with no bonds has one
component per atom, so `compact='component'` equals `compact=False` there, and that
is the answer rather than an error.

## Acceptance criteria

- `compact='molecule'` translates each molecule as one unit and leaves no bond
  stretched within a molecule.
- On `1ATP`, `compact='component'` and `compact='molecule'` produce measurably
  different coordinates, since component 0 spans seven molecules.
- A test covering that difference. Names the `guard` field.

## Dependencies and risks

Additive: no existing call changes meaning, and `False` and `'component'` keep their
behaviour. This is why it was safe to defer past 1.0 while renaming the argument was
not — the rename and the default change are breaking changes on `stable` symbols and
had to happen before the tag.

## Provenance

Host: this development checkout, molsysmt at `a085b67b6`. Python 3.13.14. Systems:
the bundled demo set. 2026-08-19.
