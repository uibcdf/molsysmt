---
summary: Native system B-factor queries ignore selected structures.
issue: uibcdf/molsysmt#384
status: resolved
opened: 2026-10-13
closed: 2026-10-13
severity: medium
verification: reproduced
area: [basic, form, attribute]
guard: tests/form/molsysmt_MolSys/test_b_factor_structure_selection.py
normative:
blocked_by: []
supersedes: []
---

# Native system B-factor queries ignore selected structures

**Reported:** ElastNetMT cache regression work, uibcdf/elastnetmt#27.
**Status:** Resolved. The selected structure axis is now forwarded without replacement; closure evidence follows below.

## What

After appending a second structure to a PDB-origin MolSys,
`msm.get(molsys, structure_indices=0, b_factor=True)` returns a quantity of
shape `(2, n_atoms)`, while selected coordinates have shape `(1, n_atoms, 3)`.

## How

`molsysmt/form/molsysmt_MolSys/get_structural_attributes.py` hard-codes
`structure_indices='all'` in `get_b_factor_from_system` instead of forwarding
its argument. The downstream Structures getter already selects both axes.
Correct delegation at the MolSys boundary; do not introduce a second slicer.

## Why

Consumers receive unrelated structures and can spuriously invalidate cached
analyses. Reordering, repetitions and empty requested axes must retain their
public query semantics and physical units.

## Evidence and scope

Reproduced on `a462b49c5566e8de993f83825576dc3860e9cfb1`, Linux, Python
3.14.7, with the bundled 181L PDB, public append/set/get and distinct numerical
B factors in two structures. This is system-level MolSys delegation, not a
failure of the downstream atom/Structures getter. B factors have length-squared
units. Missing values remain None. No coordinate or chemical data is changed.

## Acceptance criteria

Distinct-value controls check scalar, nonconsecutive, reordered, repeated and
empty structure selections, with and without atom selections and mixed
coordinate/B-factor queries. Public extract and H5MSM round trips agree with
the query. A non-default unit policy preserves values in explicit nm squared.

## Resolution and verification — 2026-10-13

The MolSys system-level getter forwards structure_indices to the existing Structures getter. Distinct values, scalar/nonconsecutive/repeated/empty structure selections, mixed coordinate queries, extraction, changed length policy and public H5MSM round trips are protected by the named regression module. No new slicing or geometry kernel was introduced.

Executed source verification on Linux/Python 3.14.7, Pandas 2.3.3: the 455-test combined regression scope passes with 12 workers and pytest-receptor, including form setters/getters, digestion, edits/invalidation, structure axes, mixed attribute delivery and strict API docstring rendering. A supplementary 18-case atom-ID module also covers final full-column scalar broadcasting. Public get/set doctests pass. The new lightweight recipe and new independent Toolbox/course sections execute with the development Python 3.14; unrelated legacy sections were preserved without reexecution. Foundations and the documentation manifest are updated. Sphinx HTML compilation succeeds with existing warning debt under uibcdf/molsysmt#144. Ruff, public docstring validation and the fast repository gates pass.

This corrects existing pre-1.0 contracts. No frozen artifact, tag, package coordinate or provider floor is changed. Exact replacement-candidate qualification remains owned by uibcdf/molsysmt#334.
