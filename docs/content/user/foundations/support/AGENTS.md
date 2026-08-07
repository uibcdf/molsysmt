# Section: Support & Coverage Directives (`AGENTS.md`)

This guide governs all content under `docs/content/user/foundations/support/`.

## 🧭 Subdirectory Purpose & Scope
Cover the form-agnostic matrix: supported in-memory object classes, disk file formats, physical-chemical metadata/forcefields, and 3D visualization engines.

## 📄 Pages List & Paired Micro-`AGENTS.md` Files
- `index.md` ➔ `index.AGENTS.md`: Group landing page with `toctree`.
- `supported_forms.md` ➔ `supported_forms.md.AGENTS.md`: Native and third-party in-memory forms.
- `supported_files.md` ➔ `supported_files.md.AGENTS.md`: Disk file formats and streaming handlers.
- `supported_physchem.md` ➔ `supported_physchem.md.AGENTS.md`: Forcefields, water models, and mechanics metadata.
- `supported_viewers.md` ➔ `supported_viewers.md.AGENTS.md`: 3D rendering backends (MolSysViewer, NGLView, Py3Dmol).

## 📐 Foundations Editorial & Style Standards
- **Conceptual Scope**: Pages in `foundations/` explain conceptual architecture, design principles, and coverage matrices. They do NOT document specific function API signatures, nor do they include `tools/` artifacts such as `:::{versionadded}`, top italic gerund summaries (`*Doing...*`), or API function `{seealso}` boxes.
- **Published Table Formatting Standard**: All tables MUST expand to full line width (`class="table"`, `width: 100%`), feature zebra striping, and have all headers and cells left-aligned (`text-align: left`).
- **Concise Section Titles**: Headings (`H2`, `H3`) must be brief, crisp, and direct (typically 2 to 4 words).
- **Nested Toctree Chaining**: References to index pages in `toctree` directives MUST use relative index paths without `.md` extensions (e.g. `support/index`).
