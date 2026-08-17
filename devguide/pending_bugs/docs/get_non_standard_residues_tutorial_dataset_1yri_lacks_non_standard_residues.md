---
summary: get_non_standard_residues tutorial dataset 1YRI lacks non-standard residues
issue: uibcdf/molsysmt#164
status: open
opened: 2026-08-17
closed:
verification: asserted
severity: medium
area: [build, docs]
guard:
normative:
blocked_by: []
supersedes: []
---

# `get_non_standard_residues` tutorial dataset `1YRI` lacks non-standard residues

**Reported:** 2026-08-17 during User Guide audit of `docs/content/user/tools/build/get_non_standard_residues.ipynb`.
**Status:** Open defect under investigation.

## What

In `docs/content/user/tools/build/get_non_standard_residues.ipynb`, PDB entry `1YRI` is used as the demonstration dataset. However, `1YRI` does not contain any non-standard residues (`msm.build.get_non_standard_residues` returns `{}`).

As a result, the tutorial notebook fails to demonstrate how `get_non_standard_residues` identifies and reports non-standard amino acid or nucleotide residues.

## How

The tutorial dataset needs to be replaced with a PDB structure containing known non-standard residues (such as post-translationally modified amino acids `PTR`, `SEP`, `TPO` or non-standard nucleotides).

## Why

Tool tutorial notebooks must provide clear, functional demonstrations of their target function's output so readers can understand expected return values.
