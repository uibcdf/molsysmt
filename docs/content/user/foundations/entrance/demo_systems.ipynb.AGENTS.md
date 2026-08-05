# Micro-Governance: `demo_systems.ipynb` (`demo_systems.ipynb.AGENTS.md`)

This micro-governance contract governs [`docs/content/user/foundations/entrance/demo_systems.ipynb`](demo_systems.ipynb).

---

## 🔒 Frozen & Inviolable Content

1. **Format Policy**:
   - MUST remain a Jupyter Notebook (`.ipynb`) containing Python code cells that dynamically query `molsysmt.systems.categories` and `molsysmt.systems.info` to render categorized catalog tables.

2. **Mandatory MyST Section Anchor**:
   - `(user-foundations-entrance-demo-systems)=`

3. **Variable Naming Policy**:
   - Molecular system variables MUST be named `molsys` (NOT `mol`).

4. **Code Hiding Policy**:
   - The generator cell rendering the category tables MUST feature `"metadata": {"tags": ["hide-input"]}` to keep the Python execution hidden in published HTML documentation.

5. **Inviolable Technical Directives**:
   - **Invocation Syntax Explanation**: Must explicitly demonstrate how to inspect system names (`list(msm.systems.keys())`), retrieve file paths (`msm.systems['Trp-Cage']['1l2y.h5msm']`), and pass them into tools (`msm.convert()`).
   - **Categorized Catalog Tables**: Must render separate HTML tables by category (Dipeptides, Small Proteins, Complexes, Lipids/Membranes, Small Molecules, Toy Models).
   - **Offline Accessibility Note**: Must include the `{admonition}` note box highlighting offline dataset availability.
