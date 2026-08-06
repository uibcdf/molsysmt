# Section: The Native World Directives (`AGENTS.md`)

This guide governs all content under `docs/content/user/foundations/native_world/`.

## 🧭 Subdirectory Purpose & Scope
Cover native MolSysMT data structures, containers, file handlers, and storage formats across 15 dedicated native form units.

## 📄 Pages List & Paired Micro-`AGENTS.md` Files
- `index.md` ➔ `index.AGENTS.md`: Group landing page with `toctree`.
- `molsysmt_MolSys.ipynb` ➔ `molsysmt_MolSys.AGENTS.md`: Native unified container class.
- `molsysmt_MolSysBuilder.ipynb` ➔ `molsysmt_MolSysBuilder.AGENTS.md`: Editable native builder class.
- `molsysmt_MolSysDict.ipynb` ➔ `molsysmt_MolSysDict.AGENTS.md`: Declarative system dictionary.
- `molsysmt_Topology.ipynb` ➔ `molsysmt_Topology.AGENTS.md`: Native topology container.
- `molsysmt_TopologyDict.ipynb` ➔ `molsysmt_TopologyDict.AGENTS.md`: Declarative topology dictionary.
- `molsysmt_Structures.ipynb` ➔ `molsysmt_Structures.AGENTS.md`: Native structures container.
- `molsysmt_StructuresDict.ipynb` ➔ `molsysmt_StructuresDict.AGENTS.md`: Declarative structures dictionary.
- `molsysmt_MolecularMechanics.ipynb` ➔ `molsysmt_MolecularMechanics.AGENTS.md`: Native mechanics container.
- `molsysmt_MolecularMechanicsDict.ipynb` ➔ `molsysmt_MolecularMechanicsDict.AGENTS.md`: Declarative mechanics dictionary.
- `file_h5msm.ipynb` ➔ `file_h5msm.AGENTS.md`: High-performance HDF5 binary storage format.
- `molsysmt_H5MSMFileHandler.ipynb` ➔ `molsysmt_H5MSMFileHandler.AGENTS.md`: H5MSM streaming file handler.
- `molsysmt_PDBFileHandler.ipynb` ➔ `molsysmt_PDBFileHandler.AGENTS.md`: Native PDB file handler.
- `molsysmt_CIFFileHandler.ipynb` ➔ `molsysmt_CIFFileHandler.AGENTS.md`: Native mmCIF file handler.
- `molsysmt_GROFileHandler.ipynb` ➔ `molsysmt_GROFileHandler.AGENTS.md`: Native GRO file handler.
- `molsysmt_ViewerJSON.ipynb` ➔ `molsysmt_ViewerJSON.AGENTS.md`: Lightweight JSON view schema.

## 📐 Foundations Editorial & Style Standards
- **Conceptual Scope**: Pages in `foundations/` explain conceptual architecture, concepts, and data models for readers. They do NOT document specific function API signatures, nor do they include `tools/` artifacts such as `:::{versionadded}`, top italic gerund summaries (`*Doing...*`), or API function `{seealso}` boxes.
- **Published Table Formatting Standard**: All tables MUST expand to full line width (`class="table"`, `width: 100%`), feature zebra striping, and have all headers and cells left-aligned (`text-align: left`).
- **Concise Section Titles**: Headings (`H2`, `H3`) must be brief, crisp, and direct (typically 2 to 4 words).
- **MyST Anchors & References**: Use MyST anchors for targets (e.g. `(user-foundations-03-native-world)=`) and `{ref}` for cross-links.
- **Offline Dataset Rule**: Access datasets locally via `msm.systems` (e.g. `msm.systems['T4 lysozyme L99A']['181l.bcif.gz']`).
- **Pre-execution Policy**: Pre-execute updated notebooks via `python docs/execute_notebooks.py -f [notebook_path]` before committing.
