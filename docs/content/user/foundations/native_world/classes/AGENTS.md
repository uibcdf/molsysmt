# Section: Native Classes Directives (`AGENTS.md`)

This guide governs all content under `docs/content/user/foundations/native_world/classes/`.

## 🧭 Subdirectory Purpose & Scope
Cover the 10 native Python classes and declarative dictionaries representing molecular systems, topology, structures, molecular mechanics, and graphics schemas.

## 📄 Pages List & Paired Micro-`AGENTS.md` Files
- `index.md` ➔ `index.AGENTS.md`: Group landing page with `toctree`.
- `molsysmt_MolSys.md` ➔ `molsysmt_MolSys.md.AGENTS.md`: Native unified system.
- `molsysmt_MolSysBuilder.md` ➔ `molsysmt_MolSysBuilder.md.AGENTS.md`: Staging builder container.
- `molsysmt_MolSysDict.md` ➔ `molsysmt_MolSysDict.md.AGENTS.md`: Declarative system dict.
- `molsysmt_Topology.md` ➔ `molsysmt_Topology.md.AGENTS.md`: Native topology container.
- `molsysmt_TopologyDict.md` ➔ `molsysmt_TopologyDict.md.AGENTS.md`: Declarative topology dict.
- `molsysmt_Structures.md` ➔ `molsysmt_Structures.md.AGENTS.md`: Native structures container.
- `molsysmt_StructuresDict.md` ➔ `molsysmt_StructuresDict.md.AGENTS.md`: Declarative structures dict.
- `molsysmt_MolecularMechanics.md` ➔ `molsysmt_MolecularMechanics.md.AGENTS.md`: Native mechanics container.
- `molsysmt_MolecularMechanicsDict.md` ➔ `molsysmt_MolecularMechanicsDict.md.AGENTS.md`: Declarative mechanics dict.
- `molsysmt_ViewerJSON.md` ➔ `molsysmt_ViewerJSON.md.AGENTS.md`: 3D graphics JSON schema.

## 📐 Foundations Editorial & Style Standards
- **Conceptual Scope**: Pages in `foundations/` explain conceptual architecture, design principles, and native class schemas. They do NOT document specific function API signatures, nor do they include `tools/` artifacts such as `:::{versionadded}`, top italic gerund summaries (`*Doing...*`), or API function `{seealso}` boxes.
- **Published Table Formatting Standard**: All tables MUST expand to full line width (`class="table"`, `width: 100%`), feature zebra striping, and have all headers and cells left-aligned (`text-align: left`).
- **Standardized 5-Section Layout**: Title/Anchor, Overview/User Role, Internal Architecture/Attributes Table, Declarative Serialization/Builder Staging, Invariants/Performance & API Reference Link.
- **Nested Toctree Chaining**: References in `index.md` MUST omit `.md` extensions for proper Sphinx hierarchy cascading.
