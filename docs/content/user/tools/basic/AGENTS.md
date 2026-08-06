# Sub-Portal Governance: `tools/basic/` (`AGENTS.md`)

This guide governs all content under `docs/content/user/tools/basic/`.

---

## 🧭 Subdirectory Purpose & Scope
Houses tutorial units for basic core operations in MolSysMT: loading, inspecting, converting, copying, selecting, comparing, adding, and displaying molecular systems in a form-agnostic manner. Every public surface function in `molsysmt.basic` corresponds 1:1 to a dedicated tutorial unit notebook (`*.ipynb`).

## 📄 Pages List & Paired Micro-`AGENTS.md` Files
- `index.md` ➔ `index.AGENTS.md`: Index portal with 2-column function catalog table and hidden `toctree`.

---

## 📐 Standard Architectural Pattern for Tool Tutorial Units (`*.ipynb`)

All tool tutorial units in `tools/basic/` (and across all `tools/` subdirectories) MUST adhere to the following unified cell sequence, tone, and structural invariants:

### 1. Initial Setup Cell (Code, Tagged `"remove-input"`)
- Must be the very first cell in the notebook.
- Contains warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
- Tagged with `"remove-input"` in metadata so code is hidden during HTML rendering.

### 2. Title, Anchor, and Conceptual Overview (Markdown)
- **MyST Anchor**: `(Tutorial_[FunctionName])=` or `(user-tools-basic-[function-name])=`
- **Title H1**: `# [FunctionName]`
- **Italic Summary**: `*[Gerund action description of what the tool does...]*`
- **Conceptual Intro**: Explains what the function does, its role in MolSysMT's form-agnostic philosophy, and typical use cases.
- **Foundations Link (Optional)**: Optional `{hint}` admonition linking to relevant Foundations sections (e.g. Molecular Systems, Forms, Attributes).
- **Version Added**: `:::{versionadded} 1.0.0`

### 3. API Documentation Reference (Markdown)
- **Header H2**: `## How this function works`
- **Admonition Box**:
  ```markdown
  ```{admonition} API documentation
  Follow this link for a detailed description of the input arguments, raised errors, and returned objects of this function:{func}`molsysmt.basic.[function_name]`.
  ```
  ```

### 4. Executable Hands-On Examples (Code & Markdown)
- Organized under descriptive H2 / H3 section headers (e.g., `## Basic Usage`, `## Advanced Filtering`).
- Uses pre-packaged datasets from `molsysmt.systems` (e.g. `msm.systems['Trp-Cage']['1l2y.h5msm']`) to ensure offline repeatability.
- **Canonical Variable Naming Policy**:
  - A single molecular system MUST be named **`molsys`** (never `mol`).
  - Multiple systems MUST be named **`molsys_A`**, **`molsys_B`**, **`molsys_C`**, etc.
- **3D Visualization & MolSysViewer Integration**:
  - 3D interactive views MUST use **MolSysViewer** (never legacy NGLView HTML exports).
  - Every embedded view requires a static generator script in `docs/generate_static_views/[name].py` exporting to `docs/_static/views/[name].html`.
  - In the notebook setup cell preceding `msm.view(...)` (tagged `"remove-input"`), declare:
    `molsysviewer_htmlfile = '_static/views/[name].html'` (do NOT hardcode `../../../../` relative jumps; `molsysviewer.py` automatically resolves the path relative to `MSM_DOCS_NOTEBOOK`).

### 5. Related Tools & References (Markdown)
- Concludes with a `{seealso}` admonition pointing to related tools or Cookbook recipes.

---

## ✍️ Editorial & Narrative Style Guide (Modeled after `add.ipynb` & `append_structures.ipynb`)

To maintain complete narrative consistency across all tool tutorials, contributors MUST follow this 7-point editorial flow:

1. **Context & Pre-conditions Setup**:
   - Introduce toy systems cleanly (using `msm.build.build_peptide` or `msm.systems`).
   - Explain *why* pre-processing operations are performed (e.g., translating systems via `msm.structure.translate` before adding them to prevent spatial overlap).

2. **The "Before & After" Verification Pattern**:
   - Inspect the state of the target system **before** mutation using `msm.info()`.
   - Run the target tool function.
   - Re-inspect state **after** execution with `msm.info(..., element='system')` to explicitly highlight modified atom/group/component counts or structure counts.

3. **Visual Confirmation via Interactive 3D View**:
   - Complement tabular inspection with an interactive 3D view (`msm.view()`). Encourage the user to interact with the 3D canvas (e.g. "Try rotating and zooming to observe...").

4. **In-Place vs. Out-of-Place (`in_place`) Behavior**:
   - Explicitly contrast default mutation (`in_place=True`) against new object creation (`in_place=False` yielding `molsys_D`).
   - Verify immutability of source systems using `msm.get(..., attribute=True)`.

5. **Strategic Admonition Boxes**:
   - **`{tip}`**: Use for top-level alias reminders (e.g., `msm.add` vs `msm.basic.add`).
   - **`{warning}`**: Use for structural constraints, structure matching rules (`structure_indices`), or attribute drops (`StructuralAttributeDropWarning`).

6. **Axis Differentiation & MyST Syntax Precision**:
   - Ensure explanatory text and subsequent `msm.get()` calls explicitly match the target axis being mutated (e.g. querying `n_structures=True` for structure-axis tools like `append_structures`, vs `n_peptides=True` for topology-axis tools like `add`).
   - Always format MyST function references with backticks: ``{func}`molsysmt.basic.[function]` `` (never un-backticked `{func}molsysmt.basic.[function]`).

7. **Clean Import Patterns & Cross-Sectional Link Rules**:
   - Access catalog systems directly via `msm.systems[...]` after `import molsysmt as msm`. Do not add separate imports like `from molsysmt import systems`.
   - Cross-sectional links in `{seealso}` pointing to demo systems MUST use `../../foundations/entrance/demo_systems.ipynb` (reflecting the sub-portal layout under `foundations/entrance/`).
