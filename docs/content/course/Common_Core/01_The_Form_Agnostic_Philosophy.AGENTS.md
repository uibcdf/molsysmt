# Module 01 Directives (`01_The_Form_Agnostic_Philosophy.AGENTS.md`)

This file contains the micro-governance rules and content constraints for **Module 01: The Form-Agnostic Philosophy**.

---

## 🏷️ Section Anchors
- **Primary Top-Level Anchor:** `(course-core-the-form-agnostic-philosophy)=`
- **Learning Outcomes Anchor:** `(course-core-the-form-agnostic-philosophy-learning-outcomes)=`
- **See Also Anchor:** `(course-core-the-form-agnostic-philosophy-see-also)=`

---

## 🧠 Core Pedagogical Objectives & Frozen Content (Inviolable)

1. **Formal Definition of Form (Glossary Box):**
   - Must contain the explicit `Glossary: Form` info admonition defining a **Form** as any specific way molecular data is stored or represented (PDB file, MDTraj object, MolSys native object).
2. **The 4-Path Universal Sampler (Specialized Paths Preview):**
   - The code example in Section 1 **must** use `msm.get_form()` on 1 representative system from each of the 4 specialized paths:
     - 🔬 Alzheimer: `'pdb_id:2BEG'`
     - ♻️ Enzyme: `systems['TcTIM']['1tcd.h5msm']`
     - 💊 Antiviral: `systems['Barnase-Barstar']['barnase_barstar.h5msm']`
     - ⚡ Biophysics/Membrane: `systems['POPC membrane']['popc_membrane.dcd']`
   - *No contributor may replace these 4 systems with generic or unrelated PDBs.*
3. **Challenge 1 System Requirement (T4 Lysozyme PDB ID):**
   - The final challenge **must** strictly suggest loading the T4 Lysozyme using its PDB ID: `'pdb_id:181L'` (or `'181L'`) and converting it into an amino acid sequence string (`to_form='string:amino_acids_3'`).
4. **Mandatory Key Takeaways:**
   - The final summary block ("In MolSysMT, everything is a System. The Form is just the container...") is mandatory and must not be altered in scope or deleted.

---

## 🎨 Admonition Placement Rules
- `:::{tip}` (alias `msm`) and `:::{note}` (`systems` catalog) **must be placed immediately below the import code cell**.
- `:::{hint}` for `msm.get_form()` **must be placed immediately below the universal sampler code cell**.
- `:::{hint}` for `msm.convert()` **must be placed immediately below the conversion code cell**.
- `:::{hint}` for `msm.info()` **must be placed immediately below the report output text**.
- `:::{seealso}` **must be placed at the end of the module** without a redundant `## See Also` heading.

---

## 🔒 Mandatory Functions Introduced (Do Not Remove)
This module introduces the following 3 fundamental functions for the very first time in the curriculum. **No contributor or agent may remove or replace any of these 3 function mentions**:
1. `{func}~molsysmt.basic.get_form` — Identifies the underlying form of any molecular item.
2. `{func}~molsysmt.basic.convert` — Converts between supported forms.
3. `{func}~molsysmt.basic.info` — Displays a human-readable summary of the system's contents.

---

## 📌 Tracked Pending Fixes
- **Supported Forms Link:** The link to supported forms currently uses the main documentation site as a temporary fallback. See [`docs/content/course/pending_fixes/unit_01_supported_forms_link.md`](../pending_fixes/unit_01_supported_forms_link.md).
