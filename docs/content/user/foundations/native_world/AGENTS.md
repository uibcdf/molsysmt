# Section: Native World Directives (`AGENTS.md`)

This guide governs all content under `docs/content/user/foundations/native_world/`.

## 🧭 Subdirectory Purpose & Scope
Cover native object representations, containers, data dictionaries, file handlers, and storage formats.

## 📄 Pages List & Paired Micro-`AGENTS.md` Files
- `index.md` ➔ `index.AGENTS.md`: Native World main portal.
- `classes/index.md` ➔ `classes/index.AGENTS.md`: Native Python classes & declarative dictionaries.
- `files/index.md` ➔ `files/index.AGENTS.md`: Native storage formats (`file:h5msm`).
- `file_handlers/index.md` ➔ `file_handlers/index.AGENTS.md`: Native streaming file handlers.

## 📐 Foundations Editorial & Style Standards
- **Title Names**: Class page titles MUST use short names without `molsysmt.` prefix (e.g. `# MolSys`, `# Topology`).
- **Balanced Section Headings**: Section titles MUST be clear, 2-to-3 word headings without `&` (`## Overview and Role`, `## Internal Attributes`, `## Declarative Schema`, `## Internal Staging Tables`, `## Staging Operations`, `## Usage and Workflow`, `## Invariants and Performance`, `## API Documentation`).
- **Faithful Code Alignment**: Internal attribute tables MUST 100% faithfully match Python implementation attributes and dtypes (`Atoms_DataFrame`, `Bonds_DataFrame`, `_FRAME_ATTRIBUTES`, etc.).
- **No Redundant Serialization Sections**: Non-dictionary container units (`MolSys`, `Topology`, `Structures`, `MolecularMechanics`) MUST NOT include a separate serialization section; serialization is documented in their paired `*Dict` units.
- **Published Table Formatting Standard**: All tables MUST expand to full line width (`class="table"`, `width: 100%`), feature zebra striping, and have all headers and cells left-aligned (`text-align: left`).
- **Nested Toctree Chaining**: References in `index.md` MUST omit `.md` extensions for proper Sphinx hierarchy cascading.
