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
  5. **Final Cell (Markdown)**: `{seealso}` admonition pointing to related tools using MyST `{ref}` anchors (e.g. `{ref}`Tutorial_Build_peptide`) rather than relative `.ipynb` file paths.
- **Canonical Variable Naming Policy**: Single molecular systems MUST be named `molsys` (never `mol`); multiple systems MUST be named `molsys_A`, `molsys_B`, `molsys_C`, etc.
- **Offline Dataset Rule**: Access datasets locally via `msm.systems` (e.g. `msm.systems['T4 lysozyme L99A']['181l.bcif.gz']`) instead of calling network-fetching PDB identifiers (e.g. `pdb_id:181L`), guaranteeing offline execution stability.
- **3D Visualizations**: Embedded 3D views MUST use **MolSysViewer** with static generator scripts in `docs/generate_static_views/[name].py` exporting to `docs/_static/views/[name].html`. Preceding setup cells declare `molsysviewer_htmlfile = '_static/views/[name].html'` without hardcoding `../../../../` relative jumps.
- **Editorial & Narrative Flow (Modeled after add.ipynb)**: Always include context/pre-condition setup, "Before & After" state inspection with `msm.info()`, 3D visual confirmation with `msm.view()`, `in_place` vs out-of-place comparison, and strategic `{tip}` / `{warning}` admonitions.
- **Pre-execution & HTML Output Policy**: When code cells or Python outputs are added or modified (such as `msm.info()` tables), pre-execute only the target notebook via `python docs/execute_notebooks.py -f [notebook_path]` before committing to capture Pandas Styler CSS formatting. Pure Markdown or narrative edits do not require re-executing code cells. Never manually inject truncated static HTML strings.
- **Concise & General Section Titles Rule**: Headings (`H2`, `H3`) in tool tutorial notebooks must be brief, crisp, and direct (typically 2 to 4 words). Avoid verbose subtitles or specific domain-restricted jargon in headings when a broader term applies (e.g. use `### Topology and structures` instead of `### Topology and trajectory`, and `## Single item` instead of `## Basic Conversion: Converting a single item`). Let the introductory narrative under the heading clarify specific use cases like trajectories, NMR ensembles, or conformational sets.
- **Manifest Tracking**: When auditing and updating a tool tutorial notebook, record its status under `reviewed_units` within `docs/docs_manifest.yml`.
- Avoid duplicating large docstring examples; tutorials should complement them with more narrative and context.


## Admonition & See Also Collapsible Dropdown Rules

All tool tutorial notebooks (`*.ipynb`) MUST adhere strictly to the following admonition styling and `{seealso}` rules:

1. **Collapsible Dropdowns (`:class: dropdown`)**:
   - **API Documentation Reference**: The `API documentation` box MUST be placed directly in the introductory header section under `:::{versionadded}` as a collapsible dropdown:
     ```markdown
     :::{admonition} API documentation
     :class: dropdown

     Follow this link for a detailed description of the input arguments, raised errors, and returned objects of this function: {func}`molsysmt.basic.[function_name]`.
     :::
     ```
   - **`{tip}` Boxes**: Must be collapsible dropdowns (`:::{tip}
:class: dropdown`).
   - **`{seealso}` Box**: Must be a collapsible dropdown (`:::{seealso} Related Tools & References
:class: dropdown`).

2. **Non-Collapsible Warnings (`{warning}`)**:
   - **`{warning}` Boxes**: MUST NOT be collapsible (`:::{warning}`). Structural constraints, data drop warnings, and critical safety rules must remain open and immediately visible to the reader.

3. **`{seealso}` Formatting & Content Rules**:
   - **Title**: `:::{seealso} Related Tools & References
:class: dropdown`.
   - **Filtered Content**: Include ONLY MolSysMT functions in `tools/` that are actually used or referenced within that tutorial unit.
   - **Order of Appearance**: Entries MUST appear in the exact chronological order of their first appearance in the notebook code or text.
   - **Explicit Function Reference**: Each entry MUST state the tool title link, a short action description, and the explicit function name with `{func}`:
     `- {ref}\`Tutorial_[FunctionName]\`: [Short action description...] with {func}\`molsysmt.[module].[function]\`.`
     *(Example: `- {ref}\`Tutorial_Build_peptide\`: Build natural peptides with or without terminal caps with {func}\`molsysmt.build.build_peptide\`.)*

## Boundaries and scope

- Tools documentation is about **how to use** functions effectively, not about their internal implementation or development details.
- If content becomes heavily focused on algorithms or internal design, consider moving or duplicating that material into developer documentation instead.
