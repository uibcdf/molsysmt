# MolSysMT Master Course Guidelines & Governance (`AGENTS.md`)

This guide governs the development, editorial style, and structural standards for all modules in **"The Four Paths of the MolSysMT's Master"** course located under `docs/content/course/`.

All human contributors and AI agents working on course content must strictly adhere to these guidelines.

> **Golden Reference Model:** Module 01 ([`00_Common_Core/01_The_Form_Agnostic_Philosophy.ipynb`](00_Common_Core/01_The_Form_Agnostic_Philosophy.ipynb)) and Module 02 ([`00_Common_Core/02_Native_Forms.ipynb`](00_Common_Core/02_Native_Forms.ipynb)) are the canonical reference models for all 54 modules in the course. Every new or updated module must mirror their exact visual, structural, and editorial pattern.

---

## 🧭 Course Philosophy & Pedagogical Style

1. **Spiral Learning Across Modules:** The curriculum is organized into 54 thematic **Modules**.
2. **Terminology Standard ("Module"):** Always refer to course units and lessons as **Modules** (e.g., `Module 01: The Form-Agnostic Philosophy`, `Module 05: Molecular Anatomy`), maintaining a consistent naming convention across the entire codebase. Quedan prohibidos los términos "Phase" o "Unit".
3. **Mandatory Hyperlink Cross-References:** Any reference in narrative text, admonitions, or seealso blocks to another Module or User Guide page **MUST be formatted as an active, clickable hyperlink** (e.g., `[Module 05: Molecular Anatomy](../00_Common_Core/index.md)` or `{ref}`/`{doc}` roles).
4. **Narrative & Problem-First:** Every module must contextualize *why* a function or concept is used in computational structural biology before demonstrating code.
5. **Second-Person Tone:** Direct, clear, and encouraging ("you", "your").
6. **Form-Agnostic Paradigm:** Showcase MolSysMT's ability to seamlessly handle multiple forms (files, MDTraj, OpenMM, RDKit, native objects) without forcing manual conversions.
7. **First-Occurrence Annotations:** The first time a package convention (e.g., `import molsysmt as msm`) or a core submodule (e.g., `molsysmt.systems`) is introduced in the course, the module **must** include an explicit introductory note and link to its documentation.

---

## 🎨 Editorial Design & Heading Hierarchy Rules

1. **Heading Hierarchy & Visual Balance:**
   - Notebook Main Title: `# Module X: Title` (H1).
   - Main Sections: `### 1. Section Title` (H3).
   - Subsections: `#### Subsection Title` (H4).
   - **Do NOT use `##` (H2)** for section headers in notebooks, as Sphinx Book Theme renders H2 headings with oversized typography.

2. **Collapsible Learning Outcomes Admonition (`:class: dropdown`):**  
   The Learning Outcomes section must be formatted as a collapsible dropdown admonition positioned at the end of the introductory block:
   ```markdown
   ```{admonition} 🎯 Learning Outcomes
   :class: dropdown

   By the end of this module, you will be able to:
   - Outcome 1...
   ```

3. **Mandatory Collapsible Admonitions (`:class: dropdown`) & Custom Titles:**  
   - **ALL** admonition boxes across the course (`:::{hint}`, `:::{tip}`, `:::{note}`, `:::{info}`, `:::{seealso}`, and ````{admonition}`) **MUST incorporate `:class: dropdown`** so that they render as collapsible toggle blocks via `sphinx-togglebutton`.
   - To specify a **custom title** for a collapsible note or admonition (e.g. `Terminology Note: "Group" vs. "Residue"`), use the generic MyST syntax:
     ```markdown
     ```{admonition} Terminology Note: "Group" vs. "Residue"
     :class: dropdown note

     Content goes here...
     ```
     ```

4. **Discourse-Thread Admonition Placement (End-of-Thread Rule):**  
   Admonition boxes (`:::{tip}`, `:::{note}`, `:::{hint}`) **must never be placed mid-sentence or mid-paragraph** interrupting the narrative flow. They must always be positioned at the **end of their respective code cell or narrative thread**, acting as a natural concluding note.

5. **Function Mention Formatting vs. MyST Roles:**  
   - In standard narrative text, mention functions using clean code formatting (e.g., `msm.get_form()`, `msm.convert()`).
   - In `:::{hint}` and `:::{seealso}` boxes, use proper MyST role syntax with backticks (`{func}`molsysmt.basic.get_form``) so Sphinx compiles direct hyperlinks to the API documentation.

6. **No Redundant Headers Before Admonitions:**  
   Do not place a Markdown heading (e.g., `## See Also`) directly above an admonition block of the same type (`:::{seealso}`). Sphinx/MyST automatically renders the admonition header.

7. **Executed Output Preservation Policy:**  
   All course notebooks committed to the repository must have their cell outputs pre-executed and saved (`jupyter nbconvert --execute --inplace`) so Sphinx builds render rich printed outputs and HTML tables (e.g., `msm.info()` report tables).

8. **Concise, Clear, and Direct Headings:**  
   Module titles and section headings **must be as short, clear, and direct as possible**. Avoid overly long or convoluted titles, and avoid unnecessary conjunctions or symbols (such as overusing ampersands `&` when simple phrasing works better). Headings should be immediate and clean to read at a glance in the navigation TOC.

---

## 📚 Central Function Inventory & Function Mentions Policy

All MolSysMT functions used in the course are inventoried in [`docs/content/course/function_inventory.yml`](function_inventory.yml), which tracks `first_introduced_in` for every API call.

1. **First-Time Hint Admonitions (`:::{hint}`):**  
   A `:::{hint}` admonition box explaining a function's purpose **must appear ONLY in the module where the function is introduced for the VERY FIRST TIME in the entire course**. Subsequent modules using the same function do not repeat the hint box.
   
   *Example MyST Syntax (positioned BELOW code cell with dropdown class):*
   ```markdown
   :::{hint}
   :class: dropdown
   **msm.convert()**: Converts a molecular system between any of the 89 supported forms in memory or on disk. See API doc: {func}`molsysmt.basic.convert`.
   :::
   ```

2. **Information Badges & Reference Citations:**  
   When a statement requires reference support, use standard Markdown links or citations without cluttering the main text.

---

## 🔗 End-of-Module "See Also" Admonition

Every module **must** end with a collapsible `:::{seealso}` admonition box (preceded by its anchor `(course-[path]-[module_number]-see-also)=`). Do not add a redundant `## See Also` heading above it.

*Example MyST Syntax:*
```markdown
(course-core-01-see-also)=
:::{seealso}
:class: dropdown
**API Documentation for Functions in this Unit:**
- {func}`molsysmt.basic.convert` — Form conversion engine.
- {func}`molsysmt.basic.get` — Topology and coordinate query engine.

**Related Course Modules & Guides:**
- Next Module: [Module 2: Native Forms](../00_Common_Core/02_Native_Forms.ipynb)
- User Guide: {ref}`user-foundations`
:::
```

---

## 🏷️ Section Anchors & Hyperlink Policy

To ensure stable cross-referencing and seamless compilation:

1. **Explicit Section Anchors:**  
   Every module and every major section within a module **must** define an explicit MyST anchor label immediately preceding its heading.  
   Format convention: `(course-[path]-[module_number]-[section_slug])=`  
   Examples:
   - Module top anchor: `(course-core-01)=`
   - Section anchor: `(course-core-01-learning-outcomes)=`
   - Section anchor: `(course-core-01-see-also)=`
2. **Cross-Referencing:**  
   Use `{ref}` or Markdown links for internal linking to ensure readers can click directly to target modules or documentation pages.

---

## 📐 Canonical Notebook Structure

Every course notebook (`*.ipynb`) **must** follow this layout unless an explicit exception is declared in its corresponding micro `XX_Name.AGENTS.md`:

1. **Top Anchor & Title:** `(course-[path]-[module_number])=` and `# Module X: Title`
2. **Introductory Narrative & Glossaries / Portals** (with `:class: dropdown`)
3. **`> **🎯 Learning Outcomes**` Blockquote** (3-4 schematic bullets with vertical gray line)
4. **Numbered Sections (`### 1. ...`, `### 2. ...`)** interleaved with code cells and concluding admonitions (with `:class: dropdown`) at thread endings
5. **`### 🏆 Challenge X: Title` & ````{key-takeaway}`**
6. **`:::{seealso}` Admonition** (with `:class: dropdown` and `(course-[path]-[module_number]-see-also)=` anchor)

---

## 🔒 Inviolable Technical Invariants

* **Explicit Physical Units:** All physical quantities must include units explicitly (e.g., `'1.2 nm'`, `'100 ps'`, `'300 kelvin'`).
* **Unified API Priority:** Always prefer high-level, form-agnostic MolSysMT functions (`msm.get()`, `msm.convert()`, `msm.select()`, `msm.build.*`).
* **No Hardcoded Absolute Paths:** Never use absolute paths. Use `msm.systems[...]` or course-relative paths.

---

## 🧬 Micro-`AGENTS.md` Scope & Inheritance Model

1. **Role of Micro-`AGENTS.md`:** Each notebook file (e.g., `02_Native_Forms.ipynb`) **must** have a paired micro-governance file alongside it (`02_Native_Forms.AGENTS.md`).
2. **Content Protection Contract:** The micro `[Notebook_Name].AGENTS.md` file does **NOT** repeat global editorial or structural rules. Its sole purpose is to serve as a **domain content-protection contract**, listing the mandatory sections, essential explanations, and specific concepts that must be preserved when any contributor refines or updates the notebook.

Rule resolution hierarchy:
`Root AGENTS.md` ➔ `docs/AGENTS.md` ➔ `docs/content/course/AGENTS.md` ➔ `[Notebook_Name].AGENTS.md` (Most specific wins).

---

## 🛠️ Course Tooling & Tracking

* `docs/content/course/function_inventory.yml`: Central inventory mapping functions, summaries, and `first_introduced_in` module path.
* `docs/content/course/devtools/`: Contains `validate_course.py`, `polish_notebooks.py`, and `execute_notebooks.py`.
* `docs/content/course/pending_proposals/`: Tracks proposals for course enhancements.
* `docs/content/course/pending_fixes/`: Tracks pending editorial and technical fixes.
