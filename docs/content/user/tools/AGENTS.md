# User Guide Tools Agents Guide

This guide is for agents editing the **Tools** section of the User Guide under `docs/content/user/tools`.

## Purpose and organization

- Each tools subdirectory (`basic`, `build`, `topology`, `structure`, `pbc`, `physchem`, `hbonds`, `molecular_mechanics`, `element`, `form`, `thirds`) groups tutorials for related functions.
- The main index `tools/index.md` presents these groups as a grid of cards and a hidden toctree; maintain this structure when adding new groups.

## 📄 Pages List & Paired Micro-`AGENTS.md` Files

- `index.md` ➔ `index.AGENTS.md`: Tools section landing page featuring 4-column card grid and hidden `toctree`.

## Per-group indexes

- Files like `basic/index.md`, `structure/index.md`, `topology/index.md`, etc., should briefly describe the purpose of that group of tools and list or link to key function tutorials within the group.

## Standard Architectural Pattern for Tool Notebooks (*.ipynb)

Every tool tutorial unit (`*.ipynb`) represents a 1:1 tutorial for a public surface function and MUST adhere strictly to the following cell sequence and layout rules:

1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_[FunctionName])=`
   - H1 Title `# [FunctionName]`
   - Italic gerund summary `*[Action summary...]*`
   - Narrative intro paragraph explaining function role.
   - Version admonition `:::{versionadded} 1.0.0
:::`
   - Collapsible API documentation box:
     ```markdown
     :::{admonition} API documentation
     :class: dropdown

     Follow this link for a detailed description of the input arguments, raised errors, and returned objects of this function: {func}`molsysmt.[module].[function_name]`.
     :::
     ```
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2: `## Basic usage`
   - Opening sentence introducing the practical dataset: *"Let's show how this function works with..."*
4. **Cell 4 (Code - Library Import)**:
   - `import molsysmt as msm`
5. **Cells 5+ (Code/Markdown)**: Executable examples using bundled datasets (`msm.systems`) or peptides (`msm.build.build_peptide`).


- **Demo Systems Note Rule**: Whenever a tutorial notebook uses bundled datasets via `msm.systems`, include a collapsible `{note}` dropdown (`:class: dropdown`) right after the code cell that first calls `msm.systems`:
  ```markdown
  :::{note} Demo Systems Catalog
  :class: dropdown

  This tutorial uses demonstration datasets provided by MolSysMT. To explore the full catalog of bundled systems, forms, and file paths, visit the {ref}`Demo Systems <user-foundations-entrance-demo-systems>` guide.
  :::
  ```

## Admonition & Section Heading Rules

- **Clean Section Headings**: Headings (`H2`, `H3`) MUST NOT contain parentheses or parameter names (e.g. use `## Creating a new system` instead of `## Creating a new system (in_place=False)`).
- **Collapsible Dropdowns (`:class: dropdown`)**:
  - **API Documentation Reference**: Placed in the intro header block as a collapsible dropdown (`:class: dropdown`).
  - **`{tip}`, `{hint}` & `{hint}` Boxes**: Must be collapsible dropdowns (`:::{tip}
:class: dropdown`).
  - **`{seealso}` Box**: Must be a collapsible dropdown (`:::{seealso} Related Tools & References
:class: dropdown`).
- **Non-Collapsible Warnings (`{warning}`)**:
  - **`{warning}` Boxes**: MUST NOT be collapsible (`:::{warning}`). Structural constraints, data drop warnings, and safety rules must remain open and immediately visible to the reader.

## `{seealso}` Formatting & Content Rules

- **Title**: `:::{seealso} Related Tools & References
:class: dropdown`.
- **Filtered Content**: Include ONLY MolSysMT functions in `tools/` that are actually used or referenced within that tutorial unit.
- **Order of Appearance**: Entries MUST appear in the exact chronological order of their first appearance in the notebook code or text.
- **Explicit Function Reference**: Each entry MUST state the tool title link, a short action description, and the explicit function name with `{func}`:
  `- {ref}\`Tutorial_[FunctionName]\`: [Short action description...] with {func}\`molsysmt.[module].[function]\`.`

## Boundaries and scope

- Tools documentation is about **how to use** functions effectively, not about internal implementation or development details.
