# Micro-Governance: `demo_systems.ipynb` (`demo_systems.ipynb.AGENTS.md`)

This micro-governance contract governs [`docs/content/user/foundations/entrance/demo_systems.ipynb`](demo_systems.ipynb).

---

## 🔒 Frozen & Inviolable Content

1. **Format Policy**:
   - MUST remain a Jupyter Notebook (`.ipynb`) containing Python code cells that dynamically query `molsysmt.systems.categories` and `molsysmt.systems.info` to render category subsections, compact system headers, and file-level explanation tables.

2. **Mandatory MyST Section Anchor**:
   - `(user-foundations-entrance-demo-systems)=`

3. **Variable Naming Policy**:
   - Molecular system variables MUST be named `molsys` (NOT `mol`).

4. **Code Hiding Policy (`remove-input`)**:
   - The generator cell rendering the catalog MUST feature `"metadata": {"tags": ["remove-input"]}` to completely remove the cell input from published documentation HTML without showing collapsible source blocks.

5. **Inviolable Catalog Architecture**:
   - **Section Heading**: Must be titled `## Complete Catalog of Bundled Systems`.
   - **Category Subsections (H3)**: Grouped by category (Dipeptides, Small Proteins, Complexes, Lipids/Membranes, Small Molecules, Toy & Synthetic Models).
   - **Compact System Header**: Single-line paragraph header combining title in bold, keyword in code, and summary in italics (e.g. `**Trp-Cage TC5b Mini-Protein** (msm.systems['Trp-Cage']): 20-residue synthetic mini-protein...`).
   - **File Explanation Tables**: 2-column native HTML tables (`File String`, `Contents & Usage Explanation`) detailing exact contents and purpose for every file.
   - **Offline Accessibility Note**: Must include the `{admonition}` note box highlighting offline dataset availability.
