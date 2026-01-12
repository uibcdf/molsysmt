# User Guide Tools Agents Guide

This guide is for agents editing the **Tools** section of the User Guide under
`docs/content/user/tools`.

## Purpose and organization

- Each tools subdirectory (`basic`, `build`, `topology`, `structure`, `pbc`,
  `physchem`, `hbonds`, `molecular_mechanics`, `element`, `form`, `thirds`)
  groups tutorials for related functions.
- The main index `tools/index.md` presents these groups as a grid of cards and a hidden toctree; maintain this structure when adding new groups.

## Per-group indexes

- Files like `basic/index.md`, `structure/index.md`, `topology/index.md`, etc., should:
  - Briefly describe the purpose of that group of tools.
  - List or link to key function tutorials within the group.
- When adding new tool notebooks, update the corresponding group index to include them where appropriate.

## Tool notebooks

- Each tool notebook (`*.ipynb`) should:
  - Introduce the function(s) it covers, with a short gerund-style summary consistent with the function docstring.
  - Show minimal, focused examples using small systems (for example, those from `molsysmt.systems`).
  - Clearly state expected inputs, outputs, units, and typical usage patterns.
  - Include an `API documentation` admonition with a `{func}` link to the corresponding API page.
  - Optionally, end with a `seealso` admonition pointing to related tools or Cookbook recipes, using labeled sections and `{ref}` roles where possible instead of direct file paths.
- Avoid duplicating large docstring examples; tutorials should complement them with more narrative and context.

## Boundaries and scope

- Tools documentation is about **how to use** functions effectively, not about their internal implementation or development details.
- If content becomes heavily focused on algorithms or internal design, consider moving or duplicating that material into developer documentation instead.
