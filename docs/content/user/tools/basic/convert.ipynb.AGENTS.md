# convert.ipynb Governance Guide

This document defines micro-governance rules for the `convert.ipynb` tutorial unit (`msm.convert`).

## Scope & Compliance

- **Master Governance**: Inherits all standard rules from `docs/content/user/tools/AGENTS.md` and `docs/content/user/tools/basic/AGENTS.md`.
- **Cell Structure**:
  1. `remove-input` code cell.
  2. Intro block: Title `# Convert`, `{hint}` to `Introduction_Forms`, `versionadded 1.0.0`, collapsible `API documentation` box dropdown.
  3. `## Basic usage` header + opening sentence *"Let's explore how conversion works starting with single-item conversions..."*.
  4. Code cell: `import molsysmt as msm`.
  5. Code cell calling `msm.systems[...]`.
  6. Collapsible `{note}` dropdown: `Demo Systems Catalog`.
- **H2 Headings**:
  - `## Basic usage`
  - `## Multiple items into one`
  - `## One item into multiple`
  - `## Supported conversions`
- **Admonitions**: `API documentation`, `{tip}`, `{note}`, and `{seealso}` are collapsible dropdowns.
- **See Also**: Collapsible dropdown listing referenced tools and Foundations guides in exact order of appearance (`Introduction_Forms`, `user-foundations-entrance-demo-systems`, `info`, `get_form`, `compare`, `concatenate_structures`, `view`).
