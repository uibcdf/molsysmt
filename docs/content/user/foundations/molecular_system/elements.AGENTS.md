# Micro-Governance: `elements.ipynb` (`elements.AGENTS.md`)

This micro-governance contract governs [`docs/content/user/foundations/molecular_system/elements.ipynb`](elements.ipynb).

---

## 🔒 Directives

1. **Title & MyST Anchor**:
   - Title MUST be `# Elements`.
   - MUST preserve top anchor `(Introduction_Elements)=` for cross-link stability.

2. **Orthogonal Element Hierarchy**:
   - Primary hierarchy: `atom ➔ group ➔ molecule ➔ entity ➔ system`.
   - Orthogonal atom-level associations: `atom ➔ component` and `atom ➔ chain`.
   - Must define all 7 elements (`atom`, `group`, `molecule`, `entity`, `system`, `component`, `chain`).

3. **Interactive Inspection**:
   - Must demonstrate interactive element inspection with `{func}`molsysmt.basic.info`` using bundled local datasets (e.g. `msm.systems['T4 lysozyme L99A']['181l.bcif.gz']`).
