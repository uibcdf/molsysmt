# concatenate_structures.ipynb Governance Guide

This document defines micro-governance rules for the `concatenate_structures.ipynb` tutorial unit (`msm.concatenate_structures`).

## Scope & Compliance

- **Master Governance**: Inherits all standard rules from `docs/content/user/tools/AGENTS.md` and `docs/content/user/tools/basic/AGENTS.md`.
- **Cell Structure**:
  1. `remove-input` code cell.
  2. Intro block: Title `# Concatenate structures`, `versionadded 1.0.0`, collapsible `API documentation` box dropdown.
  3. `## Basic usage` header + opening sentence *"Let's show how this function works with alanine dipeptide..."*.
  4. Code cell: `import molsysmt as msm`.
- **H2 Headings**:
  - `## Basic usage`
  - `## Selecting specific structures to concatenate`
  - `## Specifying output form`
  - `## Concatenating structural subsets`
- **Admonitions**: `API documentation`, `{tip}`, and `{seealso}` are collapsible dropdowns.
- **See Also**: Collapsible dropdown listing referenced tools in exact order of appearance (`build_peptide`, `translate`, `info`, `view`, `get_form`).
