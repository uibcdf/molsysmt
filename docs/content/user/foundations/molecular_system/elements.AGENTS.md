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

3. **Interleaved Interactive Inspection**:
   - Each element subsection (`### Atom`, `### Group`, `### Component`, `### Molecule`, `### Chain`, `### Entity`, `### System`) MUST interleave its conceptual description directly with its corresponding `{func}`molsysmt.basic.info`` interactive output using a local bundled dataset (`msm.systems['T4 lysozyme L99A']['181l.bcif.gz']`).
