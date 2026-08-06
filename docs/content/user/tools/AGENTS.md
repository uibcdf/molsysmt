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


## Boundaries and scope

- Tools documentation is about **how to use** functions effectively, not about their internal implementation or development details.
- If content becomes heavily focused on algorithms or internal design, consider moving or duplicating that material into developer documentation instead.
