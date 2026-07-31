# MolSysMT Master Course Guidelines & Governance (`AGENTS.md`)

This guide governs the development, editorial style, and structural standards for all modules in **"The Four Paths of the MolSysMT's Master"** course located under `docs/content/course/`.

All human contributors and AI agents working on course content must strictly adhere to these guidelines.

---

## 🧭 Course Philosophy & Pedagogical Style

1. **Spiral Learning:** Each phase builds progressively on previous concepts, introducing higher levels of abstraction and complexity.
2. **Narrative & Problem-First:** Every module must contextualize *why* a function or concept is used in computational structural biology before demonstrating code.
3. **Second-Person Tone:** Direct, clear, and encouraging ("you", "your").
4. **Form-Agnostic Paradigm:** Showcase MolSysMT's ability to seamlessly handle multiple forms (files, MDTraj, OpenMM, RDKit, native objects) without forcing manual conversions.
5. **First-Occurrence Annotations:** The first time a package convention (e.g., `import molsysmt as msm`) or a core submodule (e.g., `molsysmt.systems`) is introduced in the course, the module **must** include an explicit introductory note and link to its documentation.

---

## 🎨 Editorial Design & Admonition Placement Rules

1. **Discourse-Thread Admonition Placement (End-of-Thread Rule):**  
   Admonition boxes (`:::{tip}`, `:::{note}`, `:::{hint}`) **must never be placed mid-sentence or mid-paragraph** interrupting the narrative flow. They must always be positioned at the **end of their respective code cell or narrative thread**, acting as a natural concluding note.

2. **Synthetic Learning Outcomes Subsection:**  
   The `### 🎯 Learning Outcomes` subsection must not be an isolated, heavy wall of text. It must be rendered as a **compact, schematic list of 3-4 short bullet points** positioned at the end of the introductory narrative block, immediately preceding Section 1.

3. **Function Mention Formatting vs. MyST Roles:**  
   - In standard narrative text, mention functions using clean code formatting (e.g., `msm.get_form()`, `msm.convert()`).
   - In `:::{hint}` and `:::{seealso}` boxes, use proper MyST role syntax with backticks (`{func}`molsysmt.basic.get_form``) so Sphinx compiles direct hyperlinks to the API documentation.

4. **No Redundant Headers Before Admonitions:**  
   Do not place a Markdown heading (e.g., `## See Also`) directly above an admonition block of the same type (`:::{seealso}`). Sphinx/MyST automatically renders the admonition header.

5. **Executed Output Preservation Policy:**  
   All course notebooks committed to the repository must have their cell outputs pre-executed and saved (`jupyter nbconvert --execute --inplace`) so Sphinx builds render rich printed outputs and HTML tables (e.g., `msm.info()` report tables).

---

## 📚 Central Function Inventory & Function Mentions Policy

All MolSysMT functions used in the course are inventoried in [`docs/content/course/function_inventory.yml`](function_inventory.yml), which tracks `first_introduced_in` for every API call.

1. **First-Time Hint Admonitions (`:::{hint}`):**  
   A `:::{hint}` admonition box explaining a function's purpose **must appear ONLY in the module where the function is introduced for the VERY FIRST TIME in the entire course**. Subsequent modules using the same function do not repeat the hint box.
   
   *Example MyST Syntax (positioned BELOW code cell):*
   ```markdown
   :::{hint}
   **msm.convert()**: Converts a molecular system between any of the 89 supported forms in memory or on disk. See API doc: {func}`molsysmt.basic.convert`.
   :::
   ```

2. **Information Badges & Reference Citations:**  
   When a statement requires reference support, use standard Markdown links or citations without cluttering the main text.

---

## 🔗 End-of-Unit "See Also" Admonition

Every module **must** end with a `:::{seealso}` admonition box (preceded by its anchor `(course-[path]-[module_number]-see-also)=`). Do not add a redundant `## See Also` heading above it.

*Example MyST Syntax:*
```markdown
(course-core-01-see-also)=
:::{seealso}
**API Documentation for Functions in this Unit:**
- {func}`molsysmt.basic.convert` — Form conversion engine.
- {func}`molsysmt.basic.get` — Topology and coordinate query engine.

**Related Course Modules & Guides:**
- Next Module: [Module 2: Native Forms and The Trinity](../00_Common_Core/02_Native_Forms_and_The_Trinity.ipynb)
- User Guide: {ref}`user-foundations`
:::
```

---

## 🏷️ Section Anchors & Hyperlink Policy

To ensure stable cross-referencing and seamless compilation:

1. **Explicit Section Anchors:**  
   Every unit and every major section within a unit **must** define an explicit MyST anchor label immediately preceding its heading.  
   Format convention: `(course-[path]-[module_number]-[section_slug])=`  
   Examples:
   - Module top anchor: `(course-core-01)=`
   - Section anchor: `(course-core-01-learning-outcomes)=`
   - Section anchor: `(course-core-01-see-also)=`
2. **Cross-Referencing:**  
   Use `{ref}` roles for internal linking to ensure Sphinx/MyST validates target existence during build (e.g., `{ref}`(course-core-01-learning-outcomes)``).

---

## 📐 Canonical Notebook Structure

Every course notebook (`*.ipynb`) **must** follow this layout unless an explicit exception is declared in its corresponding micro `XX_Name.AGENTS.md`:

1. **Top Anchor & Title:** `(course-[path]-[module_number])=` and `# Module X: Title`
2. **Introductory Narrative & Glossary / Portals**
3. **`### 🎯 Learning Outcomes` Subsection** (3-4 schematic bullets)
4. **Numbered Sections (`### 1. ...`, `### 2. ...`)** interleaved with code cells and concluding admonitions at thread endings
5. **`### 🏆 Challenge X: Title` & ````{key-takeaway}`**
6. **`:::{seealso}` Admonition** (with `(course-[path]-[module_number]-see-also)=` anchor)

---

## 🔒 Inviolable Technical Invariants

* **Explicit Physical Units:** All physical quantities must include units explicitly (e.g., `'1.2 nm'`, `'100 ps'`, `'300 kelvin'`).
* **Unified API Priority:** Always prefer high-level, form-agnostic MolSysMT functions (`msm.get()`, `msm.convert()`, `msm.select()`, `msm.build.*`).
* **No Hardcoded Absolute Paths:** Never use absolute paths. Use `msm.systems[...]` or course-relative paths.

---

## 🧬 Micro-`AGENTS.md` Inheritance Model

Each notebook file (e.g., `01_The_Form_Agnostic_Philosophy.ipynb`) **must** have a paired micro-governance file alongside it with the exact name:
`[Notebook_Name].AGENTS.md` (e.g., `01_The_Form_Agnostic_Philosophy.AGENTS.md`).

Rule resolution hierarchy:
`Root AGENTS.md` ➔ `docs/AGENTS.md` ➔ `docs/content/course/AGENTS.md` ➔ `[Notebook_Name].AGENTS.md` (Most specific wins).

---

## 🛠️ Course Tooling & Tracking

* `docs/content/course/function_inventory.yml`: Central inventory mapping functions, summaries, and `first_introduced_in` module path.
* `docs/content/course/devtools/`: Contains `validate_course.py`, `polish_notebooks.py`, and `execute_notebooks.py`.
* `docs/content/course/pending_proposals/`: Tracks proposals for course enhancements.
* `docs/content/course/pending_fixes/`: Tracks pending editorial and technical fixes.
