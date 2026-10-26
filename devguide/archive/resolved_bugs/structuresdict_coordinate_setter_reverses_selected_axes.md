---
summary: StructuresDict coordinate setter reverses selected structure and atom axes.
issue: uibcdf/molsysmt#472
status: resolved
opened: 2026-10-26
closed: 2026-10-26
severity: high
verification: reproduced
area: [form, structure]
guard: tests/form/molsysmt_StructuresDict/test_coordinate_set_axes.py
normative:
blocked_by: []
supersedes: []
---

# StructuresDict coordinate setter reverses selected structure and atom axes

**Reported:** 2026-10-26, during the general-form ownership regression for
uibcdf/molsysmt#467. This defect is independent of centered wrapping.

## What

Public coordinate edits with explicit atom and structure lists apply the outer
index product backwards. A four-structure, six-atom system selected at atoms
[0, 1, 2, 3] and structures [3, 1, 3] receives a valid (3, 4, 3) block, but the
adapter attempts assignment into a (4, 3, 3) population. Public wrapping rejects
both centered and uncentered dictionary cases. Equal dimensions can conceal
the axis error and edit the wrong population.

## How

`form/molsysmt_StructuresDict/set.py::set_coordinates_to_atom` uses
`np.ix_(indices, structure_indices)` against the structure-first coordinate
array. Use the actual structure-first axis contract, preserving list order,
repetitions, quantities and unselected coordinates. No geometry or selection
algorithm belongs in this adapter correction.

## Why

This is a reusable public setter used by multiple geometry editors. Fixing a
wrapping consumer alone would hide the general defect. Native MolSys and
Structures controls pass this uncentered population test; the failure is not
a Rust wrapping or Viewer rendering error.

## Acceptance criteria

Execute public setter guards with different-sized and square explicit axes,
nonconsecutive/repeated selections, all-axis controls and nm/pm policies.
Compare with independently assigned intended positions and unchanged boxes.
The dictionary centered/uncentered wrapping integration must also pass.

## Resolution — 2026-10-26

The adapter indexes coordinates with np.ix_(structure_indices, atom_indices).
No consumer compensation, transposition heuristic, coordinate computation or
index-order change is introduced. Public setter documentation explains the
structure-first Cartesian population and stored-unit conversion.

The twelve-case public setter guard compares all intended coordinates with
explicit independent assignments, covering rectangular/square selections,
ordered/repeated positions, all-axis controls and nm/pm policies. Six cases
failed under the original adapter, including a silent square-population
mismatch; six controls passed. The dictionary integration cases in the centered
wrapping guard additionally cover both wrappers and unchanged source/destination
ownership. Original boxes and unselected coordinates remain unchanged.

Foundations and [native structural rules](../../native_structures_contract.md)
retain the public axis contract. This general fix is separate from the centered
wrapping original-target defect in uibcdf/molsysmt#467.

## Qualification receipt — 2026-10-26

The integrated PBC/centering/translation/dictionary/argument/documentation
selection passes **1,121 tests** in 45.92 seconds with `--receptor=llm -n 12`,
without skips (13 intentional legacy-H5MSM warnings). Four source modules pass
all 27 doctest examples. All five modified executable notebooks run successfully.
The Cookbook change is explanatory prose; its pre-existing solvation workflow
was not newly executed. Ruff and format checks, 251-function docstring validation
and all fourteen fast repository gates pass. Incremental Sphinx HTML completes
without errors and with 29 existing heading/toctree warnings; no warning-free
full build or installed release qualification is claimed.

Commands, environment, tested source hashes, fixture bindings and limitations
are retained in the [PBC repair receipt](../../../devtools/data/pbc_repairs_20261026.json).
