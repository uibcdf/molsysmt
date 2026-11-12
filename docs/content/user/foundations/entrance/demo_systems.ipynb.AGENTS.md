# Micro-Governance: `demo_systems.ipynb` (`demo_systems.ipynb.AGENTS.md`)

This micro-governance contract governs [`docs/content/user/foundations/entrance/demo_systems.ipynb`](demo_systems.ipynb).

---

## 🔒 Frozen & Inviolable Content

1. **Format Policy & Automated Catalog Synchronization**:
   - MUST remain a Jupyter Notebook (`.ipynb`) containing an executable Python code cell (tagged `remove-input`) that dynamically queries `molsysmt.systems.categories` and `molsysmt.systems.info` upon pre-execution (`docs/execute_notebooks.py`).
   - The notebook automatically compiles and refreshes all category subsections, 2-line system headers, and file-level explanation tables directly from the Python backend definition in [`molsysmt/systems.py`](../../../../../molsysmt/systems.py).

2. **Mandatory MyST Section Anchor**:
   - `(user-foundations-entrance-demo-systems)=`

3. **Variable Naming Policy**:
   - Molecular system variables MUST be named `molsys` (NOT `mol`).

4. **Code Hiding Policy (`remove-input`)**:
   - The generator cell rendering the catalog MUST feature `"metadata": {"tags": ["remove-input"]}` to completely remove the cell input from published documentation HTML without showing collapsible source blocks.

5. **Inviolable Catalog Architecture**:
   - **Section Heading**: Must be titled `## Complete Catalog of Bundled Systems`.
   - **Category Subsections (H3)**: Grouped by category (Dipeptides, Small Proteins, Complexes, Lipids/Membranes, Small Molecules, Toy & Synthetic Models).
   - **2-Line System Header**: Line 1: `**Title** | msm.systems['keyword']`, Line 2: `*Summary...*`.
   - **File Explanation Tables**: 2-column native HTML tables (`File String`, `Contents & Usage Explanation`) detailing exact contents and purpose for every file.
   - **Offline Accessibility Note**: Must include the `{admonition}` note box highlighting offline dataset availability.

## Verified catalog limits

- Keep molecular identity and numerical descriptions consistent with the
  deposited records or stored axis metadata. Structure counts and amino-acid
  counts are separate facts; never infer one from a filename or collection key.
- Preserve distinct file realizations within a collection and the supported
  legacy-read versus current-write H5MSM distinction. Bundled data are offline;
  this does not promise that every tutorial/provider workflow is offline.
- The native query example reports general group counts. Keep the dynamic
  catalog generator and its hidden-input tag; generate output by actual notebook
  execution rather than manually replacing rendered tables.

- Changes to imported catalog metadata require `--force` for the selected notebook; an unchanged generator fingerprint or upgraded legacy mark is not evidence of a new execution.
