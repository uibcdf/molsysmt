# User Guide Foundations Agents Guide

This guide governs the development, editorial style, and structural standards for the **Foundations** section of the User Guide located under `docs/content/user/foundations`.

All human contributors and AI agents working on Foundations content must strictly adhere to these guidelines.

---

## 🧭 Purpose & Audience

- **Target Audience:** MolSysMT users (scientists, computational biologists, developers) seeking to master the constitutional principles and architecture of the toolkit.
- **Tone & Style:** English only, short direct sentences in second person ("you"), scientific rigor, and explicit physical units (nm, ps, radians, elementary charge).
- **Scope Boundary:** Focus on core concepts, data models, selections, units, and performance. Implementation details of internal functions belong under `docs/content/developer`.
- **Index Page Introductory Style:** The main Foundations portal (`docs/content/user/foundations/index.md`) MUST begin with a 2-paragraph conceptual overview explaining the framework's form-agnostic philosophy and architectural pillars before presenting the navigation cards.
- **Subdirectory Naming Policy:** Subdirectories under `docs/content/user/foundations` MUST NOT use leading number prefixes (e.g. use `entrance/`, NOT `01_entrance/`). Non-numbered paths ensure modularity and prevent cascade refactoring when reordering or inserting chapters.
- **Chapter Navigation Layout Policy:** Sub-portal index pages listing individual tutorial pages (`[Subdirectory]/index.md`) MUST use a clean bulleted list format.
  - **Section Header**: MUST use `## **Contents**` (plural).
  - **No Badges or Cards**: Cards, grids (`::::{grid}`), and badges (`{bdg-*}`) MUST NOT be used in unit lists to maintain a clean, uncluttered visual aesthetic.

---

## 📊 Published Table Formatting Standard

All published tables across the **Foundations** section (both static Markdown tables and dynamically generated notebook tables) MUST adhere to the following visual standards:

1. **Full Line Width (`class="table"`)**: Tables MUST expand to fill 100% of the available content width (`width: 100%`) using the standard `class="table"` HTML attribute.
2. **Left-Aligned Alignment**: All table headers (`<th>`) and cell text (`<td>`) MUST be strictly left-aligned (`text-align: left`).
3. **Zebra Striping**: Tables MUST feature alternating row shading (zebra coloring) that adapts cleanly to both light and dark documentation themes.
4. **Notebook Table Rendering**: In Jupyter notebooks, dynamic catalog or summary tables MUST be rendered via explicit HTML `<table class="table">` output (with code cells tagged with `"tags": ["remove-input"]` when showcasing clean references, such as in `demo_systems.ipynb` and `forms.ipynb`), avoiding pandas `.dataframe` inline compression and right-alignment.

---

## 🏛️ Section Structure & Thematic Subdirectories

Foundations is organized into **8 thematic subdirectories**, each with its own `index.md` creating a 2-level navigation hierarchy:

1. `entrance/`: Mission, installation, first steps, toolbox overview, and demo systems.
2. `molecular_system/`: Definition, items & forms, elements, and attributes.
3. `native_world/`: Native representations (`molsysmt.MolSys`, `molsysmt.Topology`), H5MSM file format, and ViewerJSON.
4. `language/`: Selection Language grammar and syntactic rules.
5. `performance/`: Memory management, big data scaling, lazy loading, and parallelization.
6. `governance/`: Physical quantities, units, precision policies, configuration options, and SMonitor.
7. `support/`: Agnostic compatibility matrix across forms, files, force fields, and external libraries.
8. `ecosystem/`: 3D Viewers, MolSysViewer, and third-party package bridges.

---

## 🧬 Governance & Micro-`AGENTS.md` Policy

1. **Subdirectory Governance (`[Subdirectory]/AGENTS.md`):**  
   Every subdirectory (e.g. `entrance/`, `molecular_system/`) MUST contain an `AGENTS.md` file specifying its local domain context, purpose, and page list.

2. **File Micro-Governance (`[filename].AGENTS.md`):**  
   Every published notebook or markdown file (e.g., `index.ipynb`, `definition.ipynb`) MUST be paired with a micro-governance file `[filename].AGENTS.md`.

3. **Content Protection Contract:**  
   The micro `[filename].AGENTS.md` file serves as a contract defining:
   - Frozen, inviolable content (essential concepts, code examples, PDB IDs, admonitions).
   - MyST section anchors (e.g. `(user-foundations-entrance)=`).
   - Required function links (`{func}`) and tutorial admonitions (`:::{seealso}`).

Rule resolution hierarchy:
`Root AGENTS.md` ➔ `docs/AGENTS.md` ➔ `docs/content/user/AGENTS.md` ➔ `foundations/AGENTS.md` ➔ `[Subdirectory]/AGENTS.md` ➔ `[filename].AGENTS.md` (Most specific wins).
