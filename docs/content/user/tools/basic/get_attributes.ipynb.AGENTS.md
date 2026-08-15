# get_attributes.ipynb Governance Guide

This document defines micro-governance rules for the `get_attributes.ipynb` tutorial unit (`msm.get_attributes`).

## Scope & Compliance

- **Master Governance**: Inherits all standard rules from `docs/content/user/tools/AGENTS.md` and `docs/content/user/tools/basic/AGENTS.md`.
- **Cell Structure**:
  1. `remove-input` code cell.
  2. Intro block: Title `# Get attributes`, collapsible `{hint}`, `versionadded 1.0.0`, collapsible `API documentation` box dropdown.
  3. `## Basic usage` header + opening sentence *"Let's show how this function works using an OpenMM Topology converted from PDB `181L`:"*.
  4. Code cell: `import molsysmt as msm`.
- **H2 Headings**:
  - `## Basic usage`
- **Admonitions**: `API documentation`, `{hint}`, `{tip}`, `{note}`, and `{seealso}` are collapsible dropdowns.
- **See Also**: Collapsible dropdown listing referenced Foundations sections and tools in exact order of appearance (`Introduction_Forms`, `Introduction_Attributes`, `convert`, `set`, `has_attribute`).
