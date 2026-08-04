# Notebook Compilation, Timestamp Tracking, and MolSysViewer Integration

This document defines the normative architectural contract for notebook pre-execution, timestamp tracking, Sphinx web compilation, and **MolSysViewer** 3D visualization integration in MolSysMT.

---

## 1. Architectural Overview and Design Principles

The documentation pipeline resolves three core engineering requirements:

1. **Deterministic Remote CI/CD**: Remote GitHub Actions builds must remain fast, lightweight, and crash-free. Web compilation (`make html`) does not execute Python code or heavy simulations in the cloud.
2. **Incremental Local Pre-Execution**: Developers executing notebooks locally only re-run notebooks that have actually been modified in their working session, preserving compute resources and time.
3. **Reproducible 3D HTML Visualization**: Tutorial pages present clean, interactive 3D molecular views powered by **MolSysViewer** using local, version-locked runtime assets without depending on active Python kernels or external CDNs.

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. LOCAL WORKSTATION                                                   │
│    Developer composes scene and exports HTML via:                      │
│    `view.export.html("docs/_static/views/1brs.html",                   │
│                     shared_runtime="docs/_static")`                    │
│    Embeds in notebook using `msv.tools.embed_iframe(...)`.             │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 2. SPHINX BUILD ASSET HOOK (`docs/conf.py`)                            │
│    `builder-inited` hook calls `export_runtime_asset("docs/_static")`.  │
│    Places version-exact `viewer.js` runtime into `_static` (gitignored).│
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 3. SPHINX WEB COMPILATION (LOCAL & CI/CD)                              │
│    `make html SPHINXOPTS="-j 12"`                                      │
│    - `nb_execution_mode = "off"` in `docs/conf.py`.                    │
│    - Renders static HTML5 iframe containers referencing `_static`.    │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 4. GITHUB PAGES PUBLICATION                                            │
│    - Instant gh-pages deployment without active Python kernel requirement.│
│    - Shared runtime cached across all documentation pages.             │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Notebook Execution & Timestamp Lifecycle

### **A. Configuration: `nb_execution_mode = "off"`**
In [`docs/conf.py`](../docs/conf.py), `MyST-NB` is configured with:
```python
nb_execution_mode = "off"
```
During Sphinx HTML compilation (`make html`), Sphinx **does not execute any Python cells**. It reads the pre-rendered cell outputs (plots, HTML widgets, tables) directly embedded in the `.ipynb` JSON file.

> [!IMPORTANT]
> **VISUALIZATION BACKEND POLICY**:
> **MolSysViewer** is the mandatory default 3D viewer across all MolSysMT documentation notebooks and tutorials. **NGLView** is used ONLY in pages specifically dedicated to explaining or demonstrating NGLView integration, its usage, or its features.
> 
> > [!WARNING]
> > **CRITICAL WARNING REGARDING MASS RE-EXECUTION**:
> > `msm.basic.view(...)` defaults to `viewer='MolSysViewer'`. Existing notebooks in `docs/content/` contain `msm.view(...)` calls without an explicit `viewer` argument. Re-executing these notebooks prematurely without export will switch their outputs to live `MolSysViewer` widgets, which **will fail to render on a static site without a running Python kernel**.
> > 
> > Migration strategy for general notebooks:
> > - Export static HTML scenes via `view.export.html(..., shared_runtime="docs/_static")` and embed via `msv.tools.embed_iframe(...)`.
> > - Explicitly set `viewer='NGLView'` ONLY on notebooks specifically dedicated to teaching NGLView.

### **B. Pre-Execution Script: `docs/execute_notebooks.py`**
Developers run [`docs/execute_notebooks.py`](../docs/execute_notebooks.py) to pre-execute modified notebooks before committing:
```bash
python docs/execute_notebooks.py -n 12 -r docs/content/user
```

### **C. Hybrid Modification Tracking Logic**
For any notebook `example.ipynb`:
1. **Timestamp File (`example.nbconvert.last_run`)**: Stores the UTC timestamp of the last successful local execution.
2. **Active Local Working Session (`git status`)**:
   - If `example.ipynb` has uncommitted local changes (tracked modified `M` or untracked `??`), the script compares the filesystem modification time (`st_mtime`) against `last_run`.
   - It executes the notebook ONCE, updates `last_run`, and skips it on subsequent runs in the same session.
3. **Fresh Clones & Branch Checkouts (`git log`)**:
   - On a fresh `git clone` or `git checkout`, Linux resets `st_mtime` to the current time.
   - If `git status` is clean, the script compares the **last Git commit timestamp** (`git log -1 --format=%ct`) against `last_run`. Since no new commits occurred, it skips all unchanged notebooks instantly.

### **D. JSON Schema Integrity (`outputs: []`)**
`myst_nb` requires every code cell in `.ipynb` v4 format to contain an `outputs` array. `execute_notebooks.py` automatically sanitizes all code cells, guaranteeing `"outputs": []` is present and preventing Sphinx `AttributeError: outputs` build failures.

### **E. Git Logging Policy**
- **Tracked in Git**: `*.nbconvert.last_run` timestamp files must be committed so execution timestamps are preserved across machines.
- **Ignored in `.gitignore`**: Transient execution logs `*.nbconvert.log` and `notebook_errors.log` are ignored in `.gitignore`.

---

## 3. MolSysViewer Integration & Static HTML Export Protocol

### **A. Live Widgets vs. Static HTML Export**
- **Live Widgets (`MolSysViewerWidget` / `anywidget`)**: Require an active Python kernel WebSocket connection to request their JavaScript runtime. Live widgets do NOT rehydrate on static web pages without a Python kernel.
- **Static HTML Export (`view.export.html`)**: Generates version-locked, static HTML views that run entirely client-side via Mol* (Molstar) in the browser without network calls or active kernels.

### **B. Shared Runtime Asset Protocol (`shared_runtime`)**

To avoid bundling multi-megabyte JS runtimes into every single exported HTML file:

1. **Exporting HTML Views with Shared Runtime**:
   ```python
   view.export.html("docs/_static/views/1brs.html", shared_runtime="docs/_static")
   ```
   This generates a lightweight HTML scene file that references the shared runtime JS asset in `docs/_static/`. Browsers download the runtime once and cache it across all documentation pages.

2. **Placing the Shared Runtime in Sphinx Build (`docs/conf.py`)**:
   In `docs/conf.py`, the `builder-inited` event automatically extracts the exact runtime asset from the installed `molsysviewer` package into `docs/_static/`:
   ```python
   def _place_runtime(app):
       from pathlib import Path
       from molsysviewer.tools import export_runtime_asset
       export_runtime_asset(str(Path(__file__).parent / "_static"))

   def setup(app):
       app.connect('builder-inited', _place_runtime)
   ```
   > **Note**: `docs/_static/viewer.js` and `docs/_static/molsysviewer*` are listed in `.gitignore` to prevent committing 6MB binaries into Git history.

3. **Embedding in Notebooks and Markdown (`msv.tools.embed_iframe`)**:
   To prevent relative path calculation errors (`../..`) across deeply nested subdirectories:
   ```python
   import molsysviewer as msv

   msv.tools.embed_iframe(
       "docs/_static/views/1brs.html",
       path="docs/content/user/my_page.ipynb",
   )
   ```
   - **In Jupyter Notebooks (`.ipynb`)**: Executing this in a cell renders the interactive 3D view directly.
   - **In Markdown Pages (`.md`)**: The same function returns the `<iframe>` HTML string with the relative `src` path pre-calculated for copy-pasting. Avoiding manual `../` calculations prevents silent embedding failures where the export and build succeed but readers see an empty frame.

### **C. Capabilities and Boundaries of Exported Scenes**
- **Fully Supported Client-Side**: Loaded structures, selections, color maps, representations, overlays, annotations, measurements, camera controls, trajectory playback, and pop-out window.
- **Requires Python Kernel (Not Available in Exported Views)**: Selection callbacks back to Python, `on_click`/`on_hover` Python hooks, and loading new datasets on the fly. Compose the full scene in Python before exporting.

---

## 4. Maintenance Checklist for Developers

When adding or modifying notebooks:

1. Edit the notebook (`.ipynb`) in your local Jupyter environment.
2. If using MolSysViewer for documentation:
   - Compose the scene in Python.
   - Export via `view.export.html("docs/_static/views/<name>.html", shared_runtime="docs/_static")`.
   - Embed using `msv.tools.embed_iframe(...)`.
3. If using NGLView, ensure `viewer='NGLView'` is explicitly passed to `msm.view(..., viewer='NGLView')`.
4. Run `python docs/execute_notebooks.py -r docs/` to pre-execute modified notebooks.
5. Verify local HTML compilation with `make -C docs html SPHINXOPTS="-j 12"`.
6. Commit and push: GitHub Actions will publish the static site to `gh-pages` within seconds.
