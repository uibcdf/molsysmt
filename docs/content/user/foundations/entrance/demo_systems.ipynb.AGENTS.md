# Micro-Governance: `demo_systems.ipynb` (`demo_systems.ipynb.AGENTS.md`)

This micro-governance contract governs [`docs/content/user/foundations/entrance/demo_systems.ipynb`](demo_systems.ipynb).

---

## 🔒 Frozen & Inviolable Content

1. **Format Policy**:
   - MUST remain a Jupyter Notebook (`.ipynb`) containing Python code cells that dynamically query `molsysmt.systems` and render the full catalog table.

2. **Mandatory MyST Section Anchor**:
   - `(user-foundations-entrance-demo-systems)=`

3. **Inviolable Technical Directives**:
   - **Invocation Syntax Explanation**: Must explicitly demonstrate how to inspect system names (`list(msm.systems.keys())`), retrieve file paths (`msm.systems['Trp-Cage']['1l2y.h5msm']`), and pass them into tools (`msm.convert()`).
   - **Dynamic Catalog Table**: Must include an executable Python code cell building a Pandas DataFrame table of all available system names, files included, and invocation code examples.
   - **Offline Accessibility Note**: Must include the `{admonition}` note box highlighting offline dataset availability.
