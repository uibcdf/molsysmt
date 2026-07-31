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

## 📚 Central Function Inventory & Function Mentions Policy

All MolSysMT functions used in the course are inventoried in [`docs/content/course/function_inventory.yml`](function_inventory.yml), which tracks `first_introduced_in` for every API call.

1. **First-Time Hint Admonitions (`:::{hint}`):**  
   A `:::{hint}` admonition box explaining a function's purpose **must appear ONLY in the module where the function is introduced for the VERY FIRST TIME in the entire course**. Subsequent modules using the same function do not repeat the hint box.
   
   *Example MyST Syntax (in first-occurrence module):*
   ```markdown
   :::{hint}
   **msm.convert()**: Converts a molecular system between any of the 89 supported forms in memory or on disk. See API doc: {func}`molsysmt.basic.convert`.
   :::
   ```

2. **Standard Function Links in Narrative Text:**  
   For standard mentions of functions in text, use **Option A (MyST Native Role)**: `{func}~molsysmt.basic.convert`.

3. **Information Badges & Reference Citations (`<sup>[ℹ️](URL)</sup>`):**  
   When a sentence, factual claim, or statement requires explicit reference support, a citation, or a supplemental link, append a clickable superscript info icon:
   - Example: *"MolSysMT supports 89 distinct forms across files and libraries<sup>[ℹ️](https://www.uibcdf.org/MolSysMT/)</sup>."*

---

## 🔗 End-of-Unit "See Also" Section & Admonition

Every module **must** end with a `## See Also` section, formatted as a MyST `:::{seealso}` admonition box. This section must contain:
1. Direct links to the API documentation of **all** MolSysMT functions featured in the module (using `{func}` roles).
2. Direct cross-references to related course modules or user guide foundations.

*Example MyST Syntax:*
```markdown
## See Also

:::{seealso}
**API Documentation for Functions in this Unit:**
- {func}`molsysmt.basic.convert` — Form conversion engine.
- {func}`molsysmt.basic.get` — Topology and coordinate query engine.

**Related Course Modules & Guides:**
- Next Module: {ref}`course-core-02`
- User Guide: {ref}`user-foundations`
:::
```

---

## 🏷️ Section Anchors & Hyperlink Policy

To ensure stable cross-referencing and seamless compilation (whether embedded in Sphinx or published as an independent web application):

1. **Explicit Section Anchors:**  
   Every unit and every major section within a unit **must** define an explicit MyST anchor label immediately preceding its heading.  
   Format convention: `(course-[path]-[module_number]-[section_slug])=`  
   Examples:
   - Module top anchor: `(course-core-01)=`
   - Section anchor: `(course-core-01-learning-outcomes)=`
   - Section anchor: `(course-core-01-supported-forms)=`
2. **Cross-Referencing:**  
   Use `{ref}` roles for internal linking to ensure Sphinx/MyST validates target existence during build (e.g., `{ref}`(course-core-01-supported-forms)``).
3. **External & Temporary Web Links:**  
   When referencing documentation sections whose final independent web URLs are still pending decision, use the main documentation site as a temporary fallback and log the item in `docs/content/course/pending_fixes/`.

---

## 📐 Canonical Notebook Structure (7 Obligatory Sections)

Every course notebook (`*.ipynb`) **must** contain the following 7 sections in order, unless an explicit exception is declared in its corresponding micro `XX_Name.AGENTS.md`:

1. **`# [Module Number]. [Title]`**  
   Header cell with clear title matching `course_manifest.yml`, preceded by its top-level anchor `(course-[path]-[module_number])=`.
2. **`## Learning Outcomes`**  
   Bullet list of 3-4 specific skills or concepts mastered in this module.
3. **`## Working System & Prerequisites`**  
   Explicit declaration of the molecular system(s) loaded (e.g., T4 Lysozyme `181L`, Trp-Cage `1L2Y`).
4. **`:::{admonition} API Documentation`**  
   MyST admonition linking directly to official MolSysMT API functions covered.
5. **`## Conceptual Background & Hands-on Examples`**  
   Narrative explanation interleaved with executable, clean Python code cells and `:::{hint}` function admonitions (only for first-occurrence functions).
6. **`## Check Your Understanding`**  
   A practical challenge or mini-exercise for the user to solve.
7. **`## See Also`**  
   `:::{seealso}` admonition containing API links for featured functions and next course modules.

---

## 🔒 Inviolable Technical Invariants

* **Explicit Physical Units:** All physical quantities must include units explicitly (e.g., `'1.2 nm'`, `'100 ps'`, `'300 kelvin'`).
* **Unified API Priority:** Always prefer high-level, form-agnostic MolSysMT functions (`msm.get()`, `msm.convert()`, `msm.select()`, `msm.build.*`).
* **No Hardcoded Absolute Paths:** Never use absolute paths (e.g., `/home/user/...`). Use `msm.systems[...]` or course-relative paths.
* **Clean Notebook Output:** Notebooks committed to the repository must be pre-cleansed (reset execution counters, clear transitory output if required) via `devtools/polish_notebooks.py`.

---

## 🧬 Micro-`AGENTS.md` Inheritance Model

Each notebook file (e.g., `01_The_Form_Agnostic_Philosophy.ipynb`) **must** have a paired micro-governance file alongside it with the exact name:
`[Notebook_Name].AGENTS.md` (e.g., `01_The_Form_Agnostic_Philosophy.AGENTS.md`).

The micro-`AGENTS.md` file defines:
- **Mandatory Systems:** Specific PDB IDs, filenames, or selections that MUST be preserved in examples.
- **Key Functions:** Functions that must be showcased and tracked in `function_inventory.yml`.
- **First-Occurrence Directives:** Mandatory introductory notes for first-time imports or submodules.
- **Editorial Exceptions:** Explicit waivers for any of the 7 canonical sections (e.g., "Exception: This module omits the 'Check Your Understanding' section").

---

## 🛠️ Course Tooling & Tracking

* `docs/content/course/function_inventory.yml`: Central inventory mapping functions, summaries, and `first_introduced_in` module path.
* `docs/content/course/devtools/`: Contains `validate_course.py`, `polish_notebooks.py`, and `execute_notebooks.py`.
* `docs/content/course/pending_proposals/`: Tracks proposals for course enhancements.
* `docs/content/course/pending_fixes/`: Tracks pending editorial and technical fixes (e.g., temporary external links).
