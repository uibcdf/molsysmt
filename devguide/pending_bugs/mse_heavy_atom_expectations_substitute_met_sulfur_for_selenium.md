---
summary: MSE heavy-atom expectations substitute MET sulfur for selenium
issue: uibcdf/molsysmt#227
status: open
opened: 2026-09-22
closed:
severity: high
verification: reproduced
area: [build]
guard:
normative:
blocked_by: []
supersedes: []
---

# MSE heavy-atom expectations substitute MET sulfur for selenium

**Reported:** 2026-09-22, during the MolSysMT–DockingMT chemical preparation review.
**Status:** Open pre-1.0 defect.

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
