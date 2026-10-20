# Micro-Governance: `forms.ipynb` (`forms.AGENTS.md`)

This micro-governance contract governs [`docs/content/user/foundations/molecular_system/forms.ipynb`](forms.ipynb).

---

## 🔒 Directives

1. **Title & MyST Anchor**:
   - Title MUST be `# Items and Forms`.
   - MUST preserve top anchor `(Introduction_Forms)=` for cross-link stability.

2. **Conceptual Distinction (Item vs Form)**:
   - Must explain the core distinction between an **Item** (concrete data container) and a **Form** (data type schema tag).
   - Demonstrates inspecting an item's form using `{func}`molsysmt.basic.get_form``.

3. **Dynamic Table Rendering**:
   - Supported forms MUST be rendered programmatically via `{func}`molsysmt.supported.forms`` filtered by `form_type` (`'file'`, `'class'`, `'string'`).
   - Catalog tables render 2 columns: `['Form', 'Info']` (omitting `Type` and `Dependency`).
   - Section titles for catalog categories are `### Files`, `### Classes`, and `### Strings`.

## Public capability data

Preserve the executed capability example using public lists/DataFrames and the
index/columns/data dictionary. Declared conversion routes do not certify that
every optional provider or molecular input supports execution.
