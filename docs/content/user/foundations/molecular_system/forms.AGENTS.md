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
