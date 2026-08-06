# Section: The Molecular System Directives (`AGENTS.md`)

This guide governs all content under `docs/content/user/foundations/molecular_system/`.

## 🧭 Subdirectory Purpose & Scope
Define the core data model of MolSysMT across 4 foundational units: formal definition of a molecular system, physical items and representation forms classification, orthogonal element hierarchy (atom, group, component, molecule, chain, entity, bioassembly), and molecular attributes.

## 📄 Pages List & Paired Micro-`AGENTS.md` Files
- `index.md` ➔ `index.AGENTS.md`: Group landing page with `toctree`.
- `the_molecular_system.md` ➔ `the_molecular_system.md.AGENTS.md`: Formal definition of a Molecular System.
- `forms.ipynb` ➔ `forms.AGENTS.md`: Distinguishing items from representation forms, and catalog of supported forms.
- `elements.ipynb` ➔ `elements.AGENTS.md`: Orthogonal element hierarchy.
- `attributes.ipynb` ➔ `attributes.AGENTS.md`: Attribute getters, query mechanisms, and property types.

## 📐 Foundations Editorial & Style Standards
- **Conceptual Scope**: Pages in `foundations/` explain conceptual architecture, concepts, and data models for readers. They do NOT document specific function API signatures, nor do they include `tools/` artifacts such as `:::{versionadded}`, top italic gerund summaries (`*Doing...*`), or API function `{seealso}` boxes.
- **Published Table Formatting Standard**: All tables MUST expand to full line width (`class="table"`, `width: 100%`), feature zebra striping, and have all headers and cells left-aligned (`text-align: left`).
- **Concise Section Titles**: Headings (`H2`, `H3`) must be brief, crisp, and direct (typically 2 to 4 words).
- **MyST Anchors & References**: Use MyST anchors for targets (e.g. `(user-foundations-molecular-system-definition)=`, `(Introduction_Forms)=`, `(Introduction_Attributes)=`) and `{ref}` for cross-links.
- **Offline Dataset Rule**: Access datasets locally via `msm.systems` (e.g. `msm.systems['T4 lysozyme L99A']['181l.bcif.gz']`).
- **Pre-execution Policy**: Pre-execute updated notebooks via `python docs/execute_notebooks.py -f [notebook_path]` before committing.
