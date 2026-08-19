---
summary: get_non_standard_residues tutorial dataset 1YRI lacks non-standard residues
issue: uibcdf/molsysmt#164
status: resolved
opened: 2026-08-17
closed: 2026-08-19
verification: reproduced
severity: medium
area: [build, docs]
guard:
normative: docs/content/user/tools/build/get_non_standard_residues.ipynb.AGENTS.md
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

## Resolution — 2026-08-19

Reproduced before fixing: `msm.build.get_non_standard_residues` on `1YRI` returns
`{}`, so the page demonstrated the function by showing it find nothing.

The demonstration system is now `1ATP`, cAMP-dependent protein kinase, which carries
two real post-translational modifications — `TPO` at residue id 197 in the activation
loop and `SEP` at 338 in the turn motif. The call returns `{182: 'THR', 323: 'SER'}`.

That output is worth more than a non-empty result. It shows the function's actual
contract, which the page never stated: the mapping goes from the index of the
non-standard residue to **the standard residue it stands for**, not to its own name.
`TPO` is reported as `THR`. The markdown cell now says so, because a reader seeing
`'THR'` next to a residue named `TPO` would otherwise read it as a bug.

`1ATP` also ships as a bundled demo system, so the page no longer fetches from the
PDB to run.

Two conditions any future replacement must meet are frozen in
`get_non_standard_residues.ipynb.AGENTS.md`: it ships with MolSysMT, and it actually
contains non-standard residues. The second is the one `1YRI` failed, and nothing in
the page's structure would have caught it — the cell ran without error and produced
an empty dictionary.

Candidates checked among the bundled systems: T4 lysozyme, TcTIM, Trp-Cage, chicken
villin HP35, Hexokinase 2, Barnase-Barstar, Met-enkephalin, 1YCR, 1CEN and 2HGR all
return `{}`. `1ATP` was the only one that qualified.
