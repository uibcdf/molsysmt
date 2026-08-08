# Section: Supported Directives (`AGENTS.md`)

This guide governs all content under `docs/content/user/foundations/support/`.

## 🧭 Subdirectory Purpose & Scope
Cover the form-agnostic matrix: data forms (classes, files, strings), physical-chemical data, molecular mechanics, selection syntaxes, and 3D visualization engines.

## 📄 Pages List & Paired Micro-`AGENTS.md` Files
- `index.md` ➔ `index.AGENTS.md`: Support landing page with `toctree`.
- `forms/index.md` ➔ `forms/index.AGENTS.md`: Data forms index.
- `forms/classes.md` ➔ `forms/classes.md.AGENTS.md`: In-memory object classes matrix.
- `forms/files.md` ➔ `forms/files.md.AGENTS.md`: Disk file forms matrix.
- `forms/strings.md` ➔ `forms/strings.md.AGENTS.md`: String forms matrix.
- `physchem.md` ➔ `physchem.md.AGENTS.md`: Physical-chemical data.
- `molecular_mechanics.md` ➔ `molecular_mechanics.md.AGENTS.md`: Molecular mechanics parameters and models.
- `selection_syntaxes.md` ➔ `selection_syntaxes.md.AGENTS.md`: Selection syntaxes and shortcuts.
- `viewers.md` ➔ `viewers.md.AGENTS.md`: 3D visualization engines.

## 📐 Foundations Editorial & Style Standards
- **Concise Section Titles**: Headings (`H2`, `H3`) must be brief, crisp, and direct (typically 2 to 4 words).
- **Published Table Formatting Standard**: All tables MUST expand to full line width (`class="table"`, `width: 100%`), feature zebra striping, and have all headers and cells left-aligned (`text-align: left`).
- **Nested Toctree Chaining**: References to index pages in `toctree` directives MUST use relative index paths without `.md` extensions (e.g. `forms/index`).
