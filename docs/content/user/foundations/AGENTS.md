# User Guide Foundations Agents Guide

This guide governs the development, editorial style, and structural standards for the **Foundations** section of the User Guide located under `docs/content/user/foundations`.

All human contributors and AI agents working on Foundations content must strictly adhere to these guidelines.

---

## 🧭 Purpose & Audience

- **Target Audience:** MolSysMT users (scientists, computational biologists, developers) seeking to master the constitutional principles and architecture of the toolkit.
- **Tone & Style:** English only, short direct sentences in second person ("you"), scientific rigor, and explicit physical units (nm, ps, radians, elementary charge).
- **Scope Boundary:** Focus on core concepts, data models, selections, units, and performance. Implementation details of internal functions belong under `docs/content/developer`.
- **Index Page Introductory Style:** The main Foundations portal (`docs/content/user/foundations/index.md`) MUST begin with a 2-paragraph conceptual overview explaining the framework's form-agnostic philosophy and architectural pillars before presenting the navigation cards.

---

## 🏛️ Section Structure & Thematic Subdirectories

Foundations is organized into **8 thematic subdirectories**, each with its own `index.md` creating a 2-level navigation hierarchy:

1. `01_entrance/`: Mission, installation, first steps, toolbox overview, and demo systems.
2. `02_molecular_system/`: Definition, description/normalization, items, forms, elements, and attributes.
3. `03_native_world/`: Native representations (`molsysmt.MolSys`, `molsysmt.Topology`), H5MSM file format, and ViewerJSON.
4. `04_language/`: Selection Language grammar and syntactic rules.
5. `05_performance/`: Memory management, big data scaling, lazy loading, and parallelization.
6. `06_governance/`: Physical quantities, units, precision policies, configuration options, and SMonitor.
7. `07_support/`: Agnostic compatibility matrix across forms, files, force fields, and external libraries.
8. `08_ecosystem/`: 3D Viewers, MolSysViewer, and third-party package bridges.

---

## 🧬 Governance & Micro-`AGENTS.md` Policy

1. **Subdirectory Governance (`[Subdirectory]/AGENTS.md`):**  
   Every subdirectory (e.g. `01_entrance/`, `02_molecular_system/`) MUST contain an `AGENTS.md` file specifying its local domain context, purpose, and page list.

2. **File Micro-Governance (`[filename].AGENTS.md`):**  
   Every published notebook or markdown file (e.g., `index.ipynb`, `definition.ipynb`) MUST be paired with a micro-governance file `[filename].AGENTS.md`.

3. **Content Protection Contract:**  
   The micro `[filename].AGENTS.md` file serves as a contract defining:
   - Frozen, inviolable content (essential concepts, code examples, PDB IDs, admonitions).
   - MyST section anchors (e.g. `(user-foundations-01-entrance)=`).
   - Required function links (`{func}`) and tutorial admonitions (`:::{seealso}`).

Rule resolution hierarchy:
`Root AGENTS.md` ➔ `docs/AGENTS.md` ➔ `docs/content/user/AGENTS.md` ➔ `foundations/AGENTS.md` ➔ `[Subdirectory]/AGENTS.md` ➔ `[filename].AGENTS.md` (Most specific wins).
