# copy.ipynb Governance Guide

This document defines micro-governance rules for the `copy.ipynb` tutorial unit (`msm.copy`).

## Scope & Compliance

- **Master Governance**: Inherits all standard rules from `docs/content/user/tools/AGENTS.md` and `docs/content/user/tools/basic/AGENTS.md`.
- **Cell Structure**:
  1. `remove-input` code cell.
  2. Intro block: Title `# Copy`, `versionadded 1.0.0`, collapsible `API documentation` box dropdown.
  3. `## Basic usage` header + opening sentence *"Let's show how this function works using a PDB structure (`181L`):"*.
  4. Code cell: `import molsysmt as msm`.
- **H2 Headings**:
  - `## Basic usage`
- **Admonitions**: `API documentation`, `{tip}`, and `{seealso}` are collapsible dropdowns.
- **See Also**: Collapsible dropdown listing referenced tools in exact order of appearance (`convert`, `info`, `compare`).
