# add.ipynb Governance Guide

This document defines micro-governance rules for the `add.ipynb` tutorial unit (`msm.add`).

## Scope & Compliance

- **Master Governance**: Inherits all standard rules from `docs/content/user/tools/AGENTS.md` and `docs/content/user/tools/basic/AGENTS.md`.
- **Cell Structure**:
  1. `remove-input` code cell.
  2. Intro block: Title `# Add`, `versionadded 1.0.0`, collapsible `API documentation` box dropdown.
  3. `## Basic usage` header + opening sentence *"Let's show how this function works with three peptides..."*.
  4. Code cell: `import molsysmt as msm`.
- **H2 Headings**:
  - `## Basic usage` (combines in-place and out-of-place `in_place=False`)
  - `## Adding selected elements`
  - `## Specifying structure indices`
  - `## What is kept and what is dropped` (includes `### Refusing instead of dropping`)
- **Admonitions**: `API documentation`, `{tip}`, and `{seealso}` are collapsible dropdowns; `{warning}` is non-collapsible.
- **See Also**: Collapsible dropdown listing referenced tools in exact order of appearance (`build_peptide`, `translate`, `info`, `view`, `get`, `select`, `concatenate_structures`, `convert`, `merge`).
