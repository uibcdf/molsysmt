---
summary: MSE heavy-atom expectations substitute MET sulfur for selenium
issue: uibcdf/molsysmt#227
status: resolved
opened: 2026-09-22
closed: 2026-09-28
severity: high
verification: reproduced
area: [build]
guard: tests/build/get_missing_heavy_atoms/test_get_missing_heavy_atoms.py::test_modified_residues_do_not_inherit_parent_heavy_atom_templates
normative:
blocked_by: []
supersedes: []
---

# MSE heavy-atom expectations substitute MET sulfur for selenium

**Reported:** 2026-09-22, during the MolSysMT–DockingMT chemical preparation review.
**Status:** Resolved 2026-09-28.

## What

`get_expected_heavy_atoms('MSE', present_atom_names=...)` returns `SD` and
omits `SE` for a chemically correct MSE residue; structural repair may then
diagnose the wrong atom.

## How

Keep sequence-level MSE→MET replacement separate from residue-specific chemical expectations. Use the MSE chemical component or report it unassessed until a chemically faithful template exists.

## Why

MSE has a selenium atom named SE; reporting the methionine sulfur atom SD as expected changes element identity in an existing public build path. This is a pre-1.0 scientific correctness defect.

## What is measured and what is assumed

**Reproduced:**

```bash
PYTHONDONTWRITEBYTECODE=1 python -c "from molsysmt.element.group.amino_acid import get_expected_heavy_atoms; print(sorted(get_expected_heavy_atoms('MSE', ['N','CA','C','O','CB','CG','SE','CE'])))"
```

Output: `['C', 'CA', 'CB', 'CE', 'CG', 'N', 'O', 'OXT', 'SD']`.
The [RCSB MSE chemical component](https://files.rcsb.org/ligands/view/MSE.cif)
lists atom `SE` with element selenium and no `SD` atom.
**Assumed:** Scientific generality beyond the bounded fixtures is not established.

## What was refuted

MSE→MET is valid as a requested standard-residue replacement in get_non_standard_residues; it is not a valid default chemical template for preserving an MSE residue.

## Scope and exclusions

Correct existing chemical expectations and downstream missing-atom reporting for MSE; audit other parent aliases such as SEP/PTR for the same failure mode. General repair of modified residues remains a separate proposal.

## Acceptance criteria

- A real MSE atom inventory containing SE is not diagnosed as missing SD, and its selenium identity is retained.
- Unsupported modified residues report unassessed rather than a fabricated parent-residue atom inventory; regression tests cover MSE and at least one modified parent alias.

## Dependencies and risks

Related tracked work: uibcdf/molsysmt#218.

## Provenance

Local checkout `e9df1d1bd`, Linux 7.0.0-28-generic x86_64, Python 3.13.14,
2026-09-22. No timing or geometric-accuracy measurement was made.

## Resolution — 2026-09-28

Heavy-atom expectations now use an exact residue chemical template. The
sequence-level MSE→MET and SEP→SER aliases no longer supply atom inventories.
`get_expected_heavy_atoms()` returns `None` for unsupported modified residues,
including MSE and SEP. `get_missing_heavy_atoms()` skips those unassessed
residues instead of reporting MET sulfur or SER atoms, and native
`add_missing_heavy_atoms()` does not add those atoms. An empty missing-atom
mapping therefore does not certify that every residue is complete. Structured
assessment coverage remains tracked in uibcdf/molsysmt#218; residue-specific
repair remains tracked in uibcdf/molsysmt#228.

The guard builds MSE with `SE` and SEP with phosphate atoms, then verifies that
the public missing-atom and native repair paths neither report nor add parent
residue atoms. An adjacent direct-helper test verifies the explicit `None`
assessment result for both modifications.
