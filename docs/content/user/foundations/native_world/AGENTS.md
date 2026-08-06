# Section: The Native World Directives (`AGENTS.md`)

This guide governs all content under `docs/content/user/foundations/native_world/`.

## 🧭 Subdirectory Purpose & Scope
Cover native MolSysMT data structures and storage formats: the unified container `molsysmt.MolSys`, the native topology container `molsysmt.Topology`, the high-performance HDF5-based storage format `file:h5msm`, and the 3D visualization schema `molsysmt.ViewerJSON`.

## 📄 Pages List & Paired Micro-`AGENTS.md` Files
- `index.md` ➔ `index.AGENTS.md`: Group landing page with `toctree`.
- `molsysmt_MolSys.ipynb` ➔ `molsysmt_MolSys.AGENTS.md`: Native unified container class.
- `molsysmt_Topology.ipynb` ➔ `molsysmt_Topology.AGENTS.md`: Native topology representation.
- `file_h5msm.ipynb` ➔ `file_h5msm.AGENTS.md`: High-performance HDF5-based storage format.
- `molsysmt_ViewerJSON.ipynb` ➔ `molsysmt_ViewerJSON.AGENTS.md`: Lightweight JSON view schema.

## 📐 Foundations Editorial & Style Standards
- **Conceptual Scope**: Pages in `foundations/` explain conceptual architecture, concepts, and data models for readers. They do NOT document specific function API signatures, nor do they include `tools/` artifacts such as `:::{versionadded}`, top italic gerund summaries (`*Doing...*`), or API function `{seealso}` boxes.
- **Published Table Formatting Standard**: All tables MUST expand to full line width (`class="table"`, `width: 100%`), feature zebra striping, and have all headers and cells left-aligned (`text-align: left`).
- **Concise Section Titles**: Headings (`H2`, `H3`) must be brief, crisp, and direct (typically 2 to 4 words).
- **MyST Anchors & References**: Use MyST anchors for targets (e.g. `(user-foundations-03-native-world)=`, `(user-foundations-native-world-molsys)=`) and `{ref}` for cross-links.
- **Offline Dataset Rule**: Access datasets locally via `msm.systems` (e.g. `msm.systems['T4 lysozyme L99A']['181l.bcif.gz']`).
- **Pre-execution Policy**: Pre-execute updated notebooks via `python docs/execute_notebooks.py -f [notebook_path]` before committing.
