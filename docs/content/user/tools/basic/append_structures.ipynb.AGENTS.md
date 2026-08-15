# append_structures.ipynb Governance Guide

This document defines micro-governance rules for the `append_structures.ipynb` tutorial unit (`msm.append_structures`).

## Scope & Compliance

- **Master Governance**: Inherits all standard rules from `docs/content/user/tools/AGENTS.md` and `docs/content/user/tools/basic/AGENTS.md`.
- **Cell Structure**:
  1. `remove-input` code cell.
  2. Intro block: Title `# Append structures`, `versionadded 1.0.0`, collapsible `API documentation` box dropdown.
  3. `## Basic usage` header + opening sentence *"Let's show how this method works with alanine dipeptide..."*.
  4. Code cell: `import molsysmt as msm`.
- **H2 Headings**:
  - `## Basic usage` (combines in-place and out-of-place `in_place=False`)
  - `## Appending selected structures`
  - `## Appending structural subsets`
- **Admonitions**: `API documentation`, `{tip}`, and `{seealso}` are collapsible dropdowns; `{warning}` is non-collapsible.
- **See Also**: Collapsible dropdown listing referenced tools in exact order of appearance (`build_peptide`, `translate`, `info`, `view`, `get`, `concatenate_structures`, `extract`).
