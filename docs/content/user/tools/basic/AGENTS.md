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

### 5. Related Tools & References (Markdown)
- Concludes with a `{seealso}` admonition pointing to related tools or Cookbook recipes.
