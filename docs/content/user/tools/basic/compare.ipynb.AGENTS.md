# compare.ipynb Governance Guide

This document defines micro-governance rules for the `compare.ipynb` tutorial unit (`msm.compare`).

## Scope & Compliance

- **Master Governance**: Inherits all standard rules from `docs/content/user/tools/AGENTS.md` and `docs/content/user/tools/basic/AGENTS.md`.
- **Cell Structure**:
  1. `remove-input` code cell.
  2. Intro block: Title `# Compare`, `versionadded 1.0.0`, collapsible `API documentation` box dropdown.
  3. `## Basic usage` header + opening sentence *"Let's explore how to compare molecular systems using three systems derived from the T4 lysozyme dataset (`181l.bcif.gz`):"*.
  4. Code cell: `import molsysmt as msm`.
- **H2 Headings**:
  - `## Basic usage`
  - `## Comparing selections`
  - `## Comparing structures`
- **Admonitions**: `API documentation`, `{tip}`, and `{seealso}` are collapsible dropdowns.
- **See Also**: Collapsible dropdown listing referenced tools in exact order of appearance (`convert`, `extract`, `info`).
