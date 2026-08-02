# Module 02 Directives (`02_Native_Forms_and_The_Trinity.AGENTS.md`)

This file contains the micro-governance rules and content constraints for **Module 02: Native Forms**.

---

## 🏷️ Section Anchors
- **Primary Top-Level Anchor:** `(course-core-02)=`
- **Learning Outcomes Anchor:** `(course-core-02-learning-outcomes)=`
- **See Also Anchor:** `(course-core-02-see-also)=`

---

## 🧠 Core Pedagogical Objectives & Content Constraints

1. **Native Forms Concept (Glossary Box):**
   - Must contain the explicit `Glossary: Native Form` info admonition defining native forms as data structures built directly within MolSysMT (`molsysmt.MolSys`, `molsysmt.Topology`, `molsysmt.Structures`, `molsysmt.TopologyDict`, `file:h5msm`).
   - **No "Trinity" references:** `molsysmt.MolSys` is an orchestrator of modular domain component objects (`topology`, `structures`, `molecular_mechanics`, and expanding). Metadata consists of system attributes, not a separate component object.
2. **Native Orchestrator (`molsysmt.MolSys`):**
   - Demonstrates converting `systems['T4 lysozyme L99A']['181l.bcif.gz']` to `'molsysmt.MolSys'`.
3. **Modular Domain Component Objects:**
   - Demonstrates accessing `molsys.topology` (`molsysmt.Topology`), `molsys.structures` (`molsysmt.Structures`), and `molsys.molecular_mechanics` (`molsysmt.MolecularMechanics`).
4. **High-Performance Persistence (`H5MSM`):**
   - Demonstrates inspecting `systems['T4 lysozyme L99A']['181l.h5msm']`.
5. **Specialty Native Forms (`TopologyDict`, `StructuresDict`, `MolSysDict`):**
   - Demonstrates lightweight dictionary forms.
6. **Challenge 2 System Requirement (SARS-CoV-2 Protease):**
   - The challenge suggests loading the SARS-CoV-2 Protease from its PDB ID (`'pdb_id:6LU7'`), converting it to `'molsysmt.MolSys'`, inspecting its components, and converting to `'molsysmt.TopologyDict'`.

---

## 🎨 Admonition Placement Rules
- `:::{hint}` for native objects / conversion functions **must be placed immediately below their respective code cells**.
- `:::{seealso}` **must be placed at the end of the module** without a redundant `## See Also` heading.

---

## 🔒 Native Forms Introduced
- `molsysmt.MolSys` — Native in-memory orchestrator object.
- `molsysmt.Topology` — Native topology hierarchy object.
- `molsysmt.Structures` — Native structural array object.
- `molsysmt.MolecularMechanics` — Native molecular mechanics object.
- `molsysmt.TopologyDict`, `molsysmt.StructuresDict`, `molsysmt.MolSysDict` — Lightweight native dictionary forms.
- `file:h5msm` — Native disk HDF5 container.
