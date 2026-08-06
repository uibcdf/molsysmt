# User Guide Tools Agents Guide

This guide is for agents editing the **Tools** section of the User Guide under
`docs/content/user/tools`.

## Purpose and organization

- Each tools subdirectory (`basic`, `build`, `topology`, `structure`, `pbc`,
  `physchem`, `hbonds`, `molecular_mechanics`, `element`, `form`, `thirds`)
  groups tutorials for related functions.
- The main index `tools/index.md` presents these groups as a grid of cards and a hidden toctree; maintain this structure when adding new groups.

## 📄 Pages List & Paired Micro-`AGENTS.md` Files

- `index.md` ➔ `index.AGENTS.md`: Tools section landing page featuring 4-column card grid and hidden `toctree`.


## Per-group indexes

- Files like `basic/index.md`, `structure/index.md`, `topology/index.md`, etc., should:
  - Briefly describe the purpose of that group of tools.
  - List or link to key function tutorials within the group.
- When adding new tool notebooks, update the corresponding group index to include them where appropriate.

## Tool notebooks

- Each tool notebook (`*.ipynb`) represents a 1:1 tutorial unit for a public surface function and MUST follow the **Standard Architectural Pattern**:
  1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
  2. **Cell 2 (Markdown)**: Anchor `(Tutorial_[FunctionName])=`, Title `# [FunctionName]`, italic gerund summary `*[Action summary...]*`, narrative intro, optional Foundations `{hint}`, and `:::{versionadded} 1.0.0`.
  3. **Cell 3 (Markdown)**: Section `## How this function works` with `{admonition} API documentation` containing `{func}` link to the API doc.
  4. **Cells 4+ (Code/Markdown)**: Executable examples using bundled datasets (`msm.systems`).
  5. **Final Cell (Markdown)**: `{seealso}` admonition pointing to related tools or Cookbook recipes.
- **Canonical Variable Naming Policy**: Single molecular systems MUST be named `molsys` (never `mol`); multiple systems MUST be named `molsys_A`, `molsys_B`, `molsys_C`, etc.
- Avoid duplicating large docstring examples; tutorials should complement them with more narrative and context.


## Boundaries and scope

- Tools documentation is about **how to use** functions effectively, not about their internal implementation or development details.
- If content becomes heavily focused on algorithms or internal design, consider moving or duplicating that material into developer documentation instead.
