# Section: Native Classes Directives (`AGENTS.md`)

This guide governs all content under `docs/content/user/foundations/native_world/classes/`.

## 🧭 Subdirectory Purpose & Scope
Cover the 10 native Python classes and declarative dictionaries representing molecular systems, topology, structures, molecular mechanics, and graphics schemas.

## 📄 Pages List & Paired Micro-`AGENTS.md` Files
- `index.md` ➔ `index.AGENTS.md`: Group landing page with `toctree`.
- `molsysmt_MolSys.md` ➔ `molsysmt_MolSys.md.AGENTS.md`: Native unified system (`# MolSys`).
- `molsysmt_MolSysBuilder.md` ➔ `molsysmt_MolSysBuilder.md.AGENTS.md`: Staging builder container (`# MolSysBuilder`).
- `molsysmt_MolSysDict.md` ➔ `molsysmt_MolSysDict.md.AGENTS.md`: Declarative system dict (`# MolSysDict`).
- `molsysmt_Topology.md` ➔ `molsysmt_Topology.md.AGENTS.md`: Native topology container (`# Topology`).
- `molsysmt_TopologyDict.md` ➔ `molsysmt_TopologyDict.md.AGENTS.md`: Declarative topology dict (`# TopologyDict`).
- `molsysmt_Structures.md` ➔ `molsysmt_Structures.md.AGENTS.md`: Native structures container (`# Structures`).
- `molsysmt_StructuresDict.md` ➔ `molsysmt_StructuresDict.md.AGENTS.md`: Declarative structures dict (`# StructuresDict`).
- `molsysmt_MolecularMechanics.md` ➔ `molsysmt_MolecularMechanics.md.AGENTS.md`: Native mechanics container (`# MolecularMechanics`).
- `molsysmt_MolecularMechanicsDict.md` ➔ `molsysmt_MolecularMechanicsDict.md.AGENTS.md`: Declarative mechanics dict (`# MolecularMechanicsDict`).
- `molsysmt_ViewerJSON.md` ➔ `molsysmt_ViewerJSON.md.AGENTS.md`: 3D graphics JSON schema (`# ViewerJSON`).

## 📐 Foundations Editorial & Style Standards
- **Title Names**: Page titles MUST use class short names without `molsysmt.` prefix (e.g. `# MolSys`, `# Topology`).
- **Balanced Section Headings**: Section titles MUST be clear, informative, 2-to-3 word headings without `&` (`## Overview and Role`, `## Internal Attributes`, `## Declarative Schema`, `## Internal Staging Tables`, `## Staging Operations`, `## Usage and Workflow`, `## Invariants and Performance`, `## API Documentation`).
- **Faithful Code Alignment**: Attribute tables MUST 100% faithfully reflect actual source code implementation (`Atoms_DataFrame`, `Bonds_DataFrame`, `_FRAME_ATTRIBUTES`, etc.).
- **No Redundant Serialization Sections**: Non-dictionary container units (`MolSys`, `Topology`, `Structures`, `MolecularMechanics`) MUST NOT include a separate serialization section; serialization is documented in their paired `*Dict` units.
- **Published Table Formatting Standard**: All tables MUST expand to full line width (`class="table"`, `width: 100%`), feature zebra striping, and have all headers and cells left-aligned (`text-align: left`).
- **Nested Toctree Chaining**: References in `index.md` MUST omit `.md` extensions for proper Sphinx hierarchy cascading.
