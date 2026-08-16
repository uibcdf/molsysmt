# get_label.ipynb Governance Guide

This document defines micro-governance rules for the `get_label.ipynb` tutorial unit (`msm.get_label`).

## Scope & Compliance

- **Master Governance**: Inherits all standard rules from `docs/content/user/tools/AGENTS.md` and `docs/content/user/tools/basic/AGENTS.md`.
- **Cell Structure**:
  1. `remove-input` code cell.
  2. Intro block: Title `# Get label`, collapsible `{hint}`, `versionadded 1.0.0`, collapsible `API documentation` box dropdown.
  3. `## Basic usage` header + opening sentence *"Let's show how this function works using a PDB structure (`1BRS`):"*.
  4. Code cell: `import molsysmt as msm`.
- **H2 Headings**:
  - `## Basic usage`
- **Admonitions**: `API documentation`, `{hint}`, `{tip}`, and `{seealso}` are collapsible dropdowns.
- **See Also**: Collapsible dropdown listing referenced Foundations sections and tools in exact order of appearance (`Introduction_Elements`, `Introduction_Attributes`, `convert`).
