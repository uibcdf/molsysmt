---
summary: make_bioassembly tutorial 3D representations render incomplete cartoons or omit generated assemblies in MolSysViewer
issue: uibcdf/molsysmt#163
status: resolved
opened: 2026-08-17
closed: 2026-08-19
verification: measured
severity: medium
area: [build, docs]
guard:
normative: devguide/BUILDER_API.md
blocked_by: []
supersedes: []
---

# `make_bioassembly` tutorial 3D representations render incomplete cartoons or omit generated assemblies in MolSysViewer

**Reported:** 2026-08-17 during User Guide audit of `docs/content/user/tools/build/make_bioassembly.ipynb`.
**Status:** Open defect under investigation.

## What

In `docs/content/user/tools/build/make_bioassembly.ipynb`, 3D static views rendered by MolSysViewer exhibit representation defects:
1. In the first example (`1OUT`), not all protein chains render with standard cartoon representations.
2. In the second example (`2BUK`), after calling `msm.build.make_bioassembly(molsys, bioassembly='1')`, the viewer output displays all water molecules and the original asymmetric unit protein, but fails to render the newly generated biological assembly symmetry copies.

## How

This behavior stems from either `make_bioassembly` entity/chain attribute propagation on symmetry copies or how the MolSysViewer adapter maps secondary structure and cartoon representations across multi-chain biological assemblies.

## Why

Biological assembly construction is a core feature for building macromolecular complexes. Users must be able to visually verify that symmetry transformations generate the complete quaternary assembly.

## Resolution — 2026-08-19

Neither half of this report is a MolSysMT defect. Both were measured before deciding.

### `1OUT`: not a defect, a miscount

The report expects every chain to render as a cartoon. Only two of the six are
protein:

| chain | secondary structure | cartoon |
| --- | --- | --- |
| 0 | 109 H, 33 C | yes, 142 groups |
| 1 | 114 H, 32 C | yes, 146 groups |
| 2, 3 | one `NA` group each | no — these are the two small molecules |
| 4, 5 | 81 and 92 `NA` groups | no — these are the waters |

`msm.get(molsys, element='molecule', molecule_type=True)` returns 2 proteins, 2 small
molecules and 173 waters. Four chains carry nothing a cartoon can be built from, and
not drawing them is correct. What was read as a rendering defect is the six chains
being counted as if all were protein.

### `2BUK`: real, and not ours

`make_bioassembly` does generate the copies. Measured:

| | atoms | chains | proteins | ions | waters |
| --- | --- | --- | --- | --- | --- |
| asymmetric unit | 1 588 | 5 | 1 | 3 | 158 |
| assembly | 95 280 | 300 | 60 | 180 | 9 480 |

Exactly 60x throughout, transformed rather than stacked — molecule centres at
`[4.66, 4.85, -0.54]`, `[2.66, 2.47, -0.77]` and `[0.82, 2.50, 1.76]` nm, the set
spanning 19.7 nm, which is an icosahedral capsid. Secondary structure is assigned to
all of them: 4 500 C, 1 260 H, 5 280 E, exactly 60x the asymmetric unit's 75/21/88.

The viewer receives all of it: `atom_mask` `True` for 95 280 atoms,
`visible_atom_indices` of length 95 280, all 85 620 protein atoms among them. The
exported HTML is 21.4 MB against ~6.7 MB for the page's other views, so the data
reaches the export rather than being truncated.

Filed as [`uibcdf/molsysviewer#64`](https://github.com/uibcdf/molsysviewer/issues/64).

The observation that closed the diagnosis came from the maintainer: the waters of
every copy *do* render. Waters are drawn as points and proteins as cartoon, and both
exist in the data, so the difference is in the representation path and not in what
was loaded. Had the copies been missing, the waters would have been missing too.

### What was refuted

*`make_bioassembly` fails to generate the symmetry copies.* It generates all 60, with
transformed coordinates and assigned secondary structure.

*Entity or chain attribute propagation on symmetry copies is a candidate cause.* The
report offered this or the viewer's representation mapping as alternatives. The
propagation is correct; only the second remains.

### Collateral finding, not part of this report

`msm.structure.get_secondary_structure` returns `numpy.str_`, not `str`. That is the
family of `uibcdf/molsysmt#165`, arriving from `molsysmt.structure` rather than from
`get()`. The #165 sweep covered `get()` only and recorded its 45 combinations as a
lower bound; this is a confirmed instance outside it, and belongs with
[`uibcdf/molsysmt#172`](https://github.com/uibcdf/molsysmt/issues/172) or a sweep of
its own.
