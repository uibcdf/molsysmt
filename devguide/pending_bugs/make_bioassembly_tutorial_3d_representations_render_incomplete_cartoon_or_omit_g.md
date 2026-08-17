---
summary: make_bioassembly tutorial 3D representations render incomplete cartoons or omit generated assemblies in MolSysViewer
issue: uibcdf/molsysmt#163
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
