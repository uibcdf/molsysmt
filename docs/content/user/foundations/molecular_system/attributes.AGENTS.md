# Micro-Governance: `attributes.ipynb` (`attributes.AGENTS.md`)

This micro-governance contract governs [`docs/content/user/foundations/molecular_system/attributes.ipynb`](attributes.ipynb).

---

## 🔒 Directives

1. **Title & MyST Anchor**:
   - Title MUST be `# Attributes`.
   - MUST preserve top anchor `(Introduction_Attributes)=` for cross-link stability.

2. **Attribute Layers**:
   - Explains the four non-exclusive attribute layers (*Topological*, *Structural*, *Mechanical*, *Chemical State*).

3. **Form & System Attribute Support**:
   - Demonstrates checking form attribute capabilities using `{func}`molsysmt.form.has_attribute`` and `{func}`molsysmt.form.get_attributes``.
   - Demonstrates checking system attribute presence using `{func}`molsysmt.basic.has_attribute`` and `{func}`molsysmt.basic.get_attributes``.

4. **Programmatic Attribute Catalog**:
   - The complete catalog of registered attributes MUST be generated programmatically from `molsysmt.attribute.attributes`.
   - Must render a full-width HTML table (`class="table"`, `justify='left'`, 100% width) with `"tags": ["remove-input", "scroll-output"]`.
