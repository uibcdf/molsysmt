# contains.ipynb Governance Guide

This document defines micro-governance rules for the `contains.ipynb` tutorial unit (`msm.contains`).

## Scope & Compliance

- **Master Governance**: Inherits all standard rules from `docs/content/user/tools/AGENTS.md` and `docs/content/user/tools/basic/AGENTS.md`.
- **Cell Structure**:
  1. `remove-input` code cell.
  2. Intro block: Title `# Contains`, `versionadded 1.0.0`, collapsible `API documentation` box dropdown.
  3. `## Basic usage` header + opening sentence *"Let's show how this function works using the T4 lysozyme dataset (`181l.bcif.gz`):"*.
  4. Code cell: `import molsysmt as msm`.
  5. Code cell calling `msm.systems[...]`.
  6. Collapsible `{note}` dropdown: `Demo Systems Catalog`.
- **H2 Headings**:
  - `## Basic usage`
- **Admonitions**: `API documentation`, `{tip}`, `{note}`, and `{seealso}` are collapsible dropdowns.
- **See Also**: Collapsible dropdown listing referenced tools in exact order of appearance (`get`, `convert`, `info`, `select`).
