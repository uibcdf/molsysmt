# Micro-Governance: `attributes.ipynb` (`attributes.AGENTS.md`)

This micro-governance contract governs [`docs/content/user/foundations/molecular_system/attributes.ipynb`](attributes.ipynb).

---

## 🔒 Directives

1. **Title & MyST Anchor**:
   - Title MUST be `# Attributes`.
   - MUST preserve top anchor `(Introduction_Attributes)=` for cross-link stability.

2. **Core Narrative & Functionality**:
   - Explains the non-exclusive attribute layers (*Topological*, *Structural*, *Mechanical*, *Chemical State*).
   - Explains form vs. system attribute presence and the role of `{func}`molsysmt.basic.has_attribute``.

3. **Programmatic Attribute Catalog**:
   - Section MUST be titled `## Attributes you can get`.
   - The complete catalog of 118 attributes MUST be generated programmatically from `molsysmt.attribute.attributes` via a hidden code cell (`"tags": ["remove-input"]`).
   - Renders a clean full-width HTML table (`class="table"`, `justify='left'`, 100% width) without scroll containers.
