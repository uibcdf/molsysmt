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

4. **Code Hiding Policy (`remove-input`)**:
   - The generator cell rendering the category tables MUST feature `"metadata": {"tags": ["remove-input"]}` to completely remove the cell input from published documentation HTML without showing collapsible source blocks.

5. **Inviolable Technical Directives**:
   - **Invocation Syntax Explanation**: Must explicitly demonstrate how to inspect system keys (`list(msm.systems.keys())`), retrieve file paths (`msm.systems['Trp-Cage']['1l2y.h5msm']`), and pass them into tools (`msm.convert()`).
   - **Section Heading**: Must be titled `## Complete Catalog of Bundled Systems`.
   - **Table Columns & Layout**: Column headers MUST be `Key`, `Description`, `Files Included`.
   - **Key Format**: System keys MUST be formatted as Python strings (e.g. `'Trp-Cage'`).
   - **Files Included Format**: File names in the `Files Included` column MUST be displayed **one per line** (`<br>` separated).
   - **Offline Accessibility Note**: Must include the `{admonition}` note box highlighting offline dataset availability.
