# Section: Native File Handlers Directives (`AGENTS.md`)

This guide governs all content under `docs/content/user/foundations/native_world/file_handlers/`.

## 🧭 Subdirectory Purpose & Scope
Cover native low-level Python I/O handler classes that parse records and manage file streams (`PDBFileHandler`, `H5MSMFileHandler`, `GROFileHandler`, `CIFFileHandler`).

## 📄 Pages List & Paired Micro-`AGENTS.md` Files
- `index.md` ➔ `index.AGENTS.md`: File handlers landing page with `toctree`.
- `molsysmt_PDBFileHandler.md` ➔ `molsysmt_PDBFileHandler.md.AGENTS.md`: PDB file handler (`# PDBFileHandler`).
- `molsysmt_H5MSMFileHandler.md` ➔ `molsysmt_H5MSMFileHandler.md.AGENTS.md`: H5MSM binary handler (`# H5MSMFileHandler`).
- `molsysmt_GROFileHandler.md` ➔ `molsysmt_GROFileHandler.md.AGENTS.md`: GRO file handler (`# GROFileHandler`).
- `molsysmt_CIFFileHandler.md` ➔ `molsysmt_CIFFileHandler.md.AGENTS.md`: mmCIF file handler (`# CIFFileHandler`).

## 📐 Foundations Editorial & Style Standards
- **Title Names**: Page titles MUST use class short names without `molsysmt.` prefix (e.g. `# PDBFileHandler`).
- **Native File Handler Structure Standard**: File handler units MUST follow the 4-section layout:
  1. `## Overview and Handler Role`
  2. `## Class Attributes and Parsed Records`
  3. `## Practical Usage and Streaming Workflow`
  4. `## Performance and I/O Invariants`
- **Nested Toctree Chaining**: References in `index.md` MUST omit `.md` extensions for proper Sphinx hierarchy cascading.
