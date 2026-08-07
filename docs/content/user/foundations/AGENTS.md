# Section: Foundations Governance Directives (`AGENTS.md`)

This guide governs the development, editorial style, and structural standards for the **Foundations** section of the User Guide located under `docs/content/user/foundations`.

---

## 🧭 Scope & Purpose

The **Foundations** section introduces the core conceptual principles, architectural invariants, and high-performance design that enable MolSysMT to operate seamlessly across different molecular structures, file formats, and computational tools.

---

## 🔒 General Principles & Editorial Standards

1. **Conceptual Focus Over Function Manuals**:
   - Foundations pages explain *how MolSysMT works under the hood* (data models, form philosophy, unit safety, selection grammar, performance engine).
   - They do NOT serve as function manuals for specific `msm.*` tools.
   - Do NOT include `tools/` artifacts on Foundations pages:
     - NO `:::{versionadded}` directives.
     - NO top italicized gerund summaries (`*Doing...*`).
     - NO API function `{seealso}` boxes.

2. **Index Page Introductory Style**:
   - The main Foundations portal (`docs/content/user/foundations/index.md`) MUST begin with a 2-paragraph conceptual overview explaining the framework's form-agnostic philosophy and architectural pillars before presenting the navigation cards.

3. **Subdirectory Naming Policy**:
   - Subdirectories under `docs/content/user/foundations` MUST NOT use leading number prefixes (e.g. use `entrance/`, NOT `01_entrance/`). Non-numbered paths ensure modularity and prevent cascade refactoring when reordering or inserting chapters.

4. **Table Presentation Standard**:
   - All published tables MUST expand to 100% linewidth (`class="table"`), feature zebra striping, and have all headers and cells left-aligned (`text-align: left`).

5. **Terminology Standard**:
   - Avoid "trajectory analytics"; use "molecular structures sequence analytics" or "spatial calculations" to reflect that MolSysMT handles structure sequences from any source.

6. **Nested Toctree Chaining & Navigation**:
   - In `toctree` directives, references to sub-portal index pages MUST omit `.md` extensions (e.g. use `entrance/index`, `performance/index`) to ensure Sphinx cascades the navigation hierarchy properly and displays full breadcrumbs and left-sidebar Section Navigation across all child documents.
