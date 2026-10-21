# Micro-Governance: info.ipynb

## Purpose
Governance rules and frozen contracts for `docs/content/user/tools/basic/info.ipynb` (`msm.basic.info`).

## Cell Sequence & Inviolable Order
1. **Cell 1 (Code, `"remove-input"`)**: Warning suppression (`import warnings; warnings.filterwarnings('ignore')`).
2. **Cell 2 (Markdown - Introductory Header Block)**:
   - Anchor `(Tutorial_Info)=`
   - H1 Title `# Info`
   - Italic summary `*Displaying summary information about a molecular system and its elements.*`
   - Narrative intro paragraph explaining dataframe output across element levels.
   - Collapsible `{hint}` dropdown linked to `{ref}`Introduction_Elements`.
   - Version admonition `:::{versionadded} 1.0.0 :::`
   - Collapsible API documentation box `:::{admonition} API documentation \n :class: dropdown`.
3. **Cell 3 (Markdown - First Real H2 Opener)**:
   - Header H2 `## Basic usage`
   - Opening sentence introducing `181L`.
4. **Cell 4 (Code)**:
   - `import molsysmt as msm`
5. **Cells 5+**: Practical examples showing summary tables at `atom`, `group`, `component`, `molecule`, `chain`, `entity`, and `system` levels.
6. **Final Cell (Markdown)**:
   - Collapsible `{seealso}` dropdown listing related tools and Foundations in strict chronological order of first appearance.

## Scoped summary contract

Preserve the executed mask example and distinguish group masks from atom masks.
The default is a Styler; DataFrame and dictionary records are explicit output
choices. System-summary masks use the atom scope. Native info shares the validated basic contract and table implementation,
using known native providers for explicit index requests.

Preserve the native-repr example: it is bounded human inspection, not an info
table, validity check or serialization API. Missing axes and empty axes differ.
