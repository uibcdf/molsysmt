# Section: Native Files Directives (`AGENTS.md`)

This guide governs all content under `docs/content/user/foundations/native_world/files/`.

## 🧭 Subdirectory Purpose & Scope
Cover native file formats engineered for high-performance storage, binary chunking, and trajectory streaming (`.h5msm`).

## 📄 Pages List & Paired Micro-`AGENTS.md` Files
- `index.md` ➔ `index.AGENTS.md`: Native files landing page with `toctree`.
- `file_h5msm.md` ➔ `file_h5msm.md.AGENTS.md`: Native HDF5 persistence format (`# h5msm`).

## 📐 Foundations Editorial & Style Standards
- **Title Names**: Page titles MUST use format short names without `file:` prefix (e.g. `# h5msm`).
- **Native File Structure Standard**: Native file format units MUST follow the 4-section layout:
  1. `## Overview and Format Purpose`
  2. `## HDF5 Layout and Dataset Schema`
  3. `## Read, Write, and Streaming Operations`
  4. `## Performance and Storage Invariants`
- **Nested Toctree Chaining**: References in `index.md` MUST omit `.md` extensions for proper Sphinx hierarchy cascading.
