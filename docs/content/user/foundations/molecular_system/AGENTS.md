# Section: The Molecular System Directives (`AGENTS.md`)

This guide governs all content under `docs/content/user/foundations/molecular_system/`.

## 🧭 Subdirectory Purpose & Scope
Define the core data model of MolSysMT across 4 foundational units: formal definition of a molecular system, physical items and representation forms classification, orthogonal element hierarchy (atom, group, component, molecule, chain, entity, bioassembly), and molecular attributes.

## 📄 Pages List & Paired Micro-`AGENTS.md` Files
- `index.md` ➔ `index.AGENTS.md`: Group landing page with `toctree`.
- `definition.ipynb` ➔ `definition.AGENTS.md`: Formal definition of a Molecular System.
- `forms.ipynb` ➔ `forms.AGENTS.md`: Distinguishing items from representation forms, and catalog of supported forms.
- `elements.ipynb` ➔ `elements.AGENTS.md`: Orthogonal element hierarchy.
- `attributes.ipynb` ➔ `attributes.AGENTS.md`: Attribute getters, query mechanisms, and property types.

## 📐 Editorial & Style Standards
- **Concise & General Section Titles**: Headings (`H2`, `H3`) in notebooks must be brief, crisp, and direct (typically 2 to 4 words).
- **MyST Anchors & References**: Use MyST anchors for targets (e.g. `(Introduction_Forms)=`, `(Introduction_Attributes)=`) and `{ref}` for cross-links.
- **Offline Dataset Rule**: Access datasets locally via `msm.systems` (e.g. `msm.systems['T4 lysozyme L99A']['181l.bcif.gz']`).
- **Pre-execution Policy**: Pre-execute updated notebooks via `python docs/execute_notebooks.py -f [notebook_path]` before committing.
