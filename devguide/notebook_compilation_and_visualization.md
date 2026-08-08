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
python docs/execute_notebooks.py -q -n 12 -r docs/content/user
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

1. **Exporting HTML Views with Shared Runtime and Transparent Background**:
   ```python
   view.export.html(
       "docs/_static/views/1brs.html",
       shared_runtime="docs/_static",
       background="transparent",
   )
   ```
   - **`background="transparent"`**: Mandatory default for all documentation views. Ensures instant 0ms dark/light theme transitions without visual lag or blink, and allows seamless integration across light/dark modes, cards, and admonition containers.

2. **Placing the Shared Runtime and Error Handling (`docs/conf.py`)**:
   In `docs/conf.py`, the `builder-inited` event automatically extracts the exact runtime asset from the installed `molsysviewer` package into `docs/_static/`:
   ```python
   def _place_runtime(app):
       from pathlib import Path
       from molsysviewer.tools import export_runtime_asset
       export_runtime_asset(str(Path(__file__).parent / "_static"))

   def setup(app):
       app.connect('builder-inited', _place_runtime)
   ```
   > **Note**: `_place_runtime` intentionally raises on failure so missing runtime assets stop the build immediately rather than producing a site with blank frames. `docs/_static/viewer.js` is listed in `.gitignore` to prevent committing 6MB binaries into Git history.

3. **Embedding in Notebooks and Markdown (`msv.tools.embed_iframe` & `MSM_DOCS_NOTEBOOK`)**:
   To prevent relative path calculation errors (`../..`) across deeply nested subdirectories:
   - `docs/execute_notebooks.py` exports `env["MSM_DOCS_NOTEBOOK"] = str(notebook_path)` during pre-execution.
   - `molsysmt.basic.viewer.molsysviewer` consumes `MSM_DOCS_NOTEBOOK` and calls:
     ```python
     import molsysviewer as msv

     msv.tools.embed_iframe(
         "docs/_static/views/1brs.html",
         path=os.environ.get("MSM_DOCS_NOTEBOOK"),
     )
     ```
   - **In Jupyter Notebooks (`.ipynb`)**: Executing this in a cell renders the interactive 3D view directly.
   - **In Markdown Pages (`.md`)**: The same function returns the `<iframe>` HTML string with the relative `src` path pre-calculated for copy-pasting.
   - **CSS Container Styling (`docs/_static/custom.css`)**: In dark mode, `html[data-theme="dark"] .bd-content div.cell_output .text_html:has(iframe)` sets `background-color: transparent !important` and `padding: 0 !important`, integrating iframe view containers flush with the page background.

### **C. Capabilities and Boundaries of Exported Scenes**
- **Fully Supported Client-Side**: Loaded structures, selections, color maps, representations, overlays, annotations, measurements, camera controls, trajectory playback, and pop-out window.
- **Requires Python Kernel (Not Available in Exported Views)**: Selection callbacks back to Python, `on_click`/`on_hover` Python hooks, and loading new datasets on the fly. Compose the full scene in Python before exporting.

---

### **D. The `msm.view()` Notebook Illusion Pattern (`MSM_VIEWS_FROM_HTML_FILES`)**

To maintain clean, elegant documentation, tutorial notebooks display standard `msm.view(...)` calls to readers without exposing embedding helper code.

1. **Pre-generation Script**:
   Static HTML views are pre-generated via dedicated scripts under `docs/generate_static_views/` using `view.export.html(..., background="transparent", shared_runtime="docs/_static")`.

2. **Hidden Target Assignment Cell (`remove-input` tag)**:
   Immediately before an `msm.view(...)` cell, a hidden code cell tagged with `remove-input` defines the target view file:
   ```python
   molsysviewer_htmlfile = '_static/views/<target_file>.html'
   ```
   Sphinx strips input for this cell from compiled HTML due to the `remove-input` tag.

3. **Pre-Execution Interception (`docs/execute_notebooks.py`)**:
   During notebook pre-execution, `docs/execute_notebooks.py` exports two environment variables:
   - `MSM_VIEWS_FROM_HTML_FILES=True`
   - `MSM_DOCS_NOTEBOOK=<absolute path to the notebook>`

   **The path must be absolute.** `embed_iframe` computes one path relative to
   another and requires both to be named from the same place. `jupyter nbconvert
   --execute` runs the kernel with the notebook's own directory as the working
   directory, so a relative value is resolved against the notebook rather than
   against the directory the script was invoked from, and the prefix is counted
   twice. On 2026-08-08 that produced `../_static/views/…` for a page at the site
   root and nine `../` for a page four directories deep — see §E.

4. **Frame Stack Interception in `molsysmt.view()`**:
   When `msm.view(...)` executes:
   - It inspects the caller frame stack for `molsysviewer_htmlfile`.
   - It pops `molsysviewer_htmlfile` from local scope to prevent namespace pollution.
   - It invokes `molsysviewer.tools.embed_iframe(htmlfile, path=MSM_DOCS_NOTEBOOK)` to generate the relative `<iframe>` output.
   - If `MSM_VIEWS_FROM_HTML_FILES=True` is enabled but no target file is in scope, `msm.view()` raises a `RuntimeError` to prevent silent fallback to live widgets.

### **E. Two failure modes this pipeline makes invisible**

Both were found on 2026-08-08, when the documentation was published for the first
time since January. Neither is exotic and both will recur, because the pipeline is
built in a way that hides them.

**1. A local preview served at the root cannot validate a site published under a
path prefix.**

`python -m http.server --directory docs/_build/html` makes the build directory the
server root, and a server clamps any attempt to escape its own root: a request for
`/../_static/views/x.html` is normalised to `/_static/views/x.html` and answered
with 200. The published site is not at a root — it lives at
`www.uibcdf.org/molsysmt/` — so the same `../` escapes to `/_static/…` at the domain
root, which is a real and different location, and GitHub answers 404.

A path that climbs above the site root is therefore **invisible locally by
construction and broken in production**. This is exactly how the `msm.view()`
iframes reached the published site broken: locally they had always resolved.

When a link or asset path is what you are checking, the local server does not
answer the question. Read the emitted `src`/`href` and confirm it never climbs
above the site root:

```bash
grep -oE '(src|href)="\.\./[^"]*"' docs/_build/html/index.html   # must return nothing at the root
```

**2. Notebook outputs are produced on one machine and reviewed by nothing.**

Because `nb_execution_mode = "off"` (§2.A), what the site publishes is whatever was
stored in the `.ipynb` the last time somebody ran `execute_notebooks.py`. Anything
environment-dependent at that moment — a path, a library version, an HTML class, a
widget's serialisation — is frozen into a committed artefact, and no gate in CI ever
re-derives or checks it. The build cannot fail on a wrong stored output, because it
never computes the right one.

Two consequences worth keeping in mind:

- the machine that executes notebooks is part of the documentation toolchain, not
  an interchangeable detail;
- a fix that changes what `msm.view()`, `msm.info()` or any other rich output emits
  does not reach the site until the affected notebooks are re-executed, or their
  outputs are repaired deliberately. The archived report on the `Styler` zebra
  striping records the same lesson from the other direction.

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
   The invocation directory no longer changes the result: `MSM_DOCS_NOTEBOOK` is
   absolute (§3.D).
5. Verify local HTML compilation with `make -C docs html SPHINXOPTS="-j 12"`.
   If you also preview it with a local server, remember what that preview cannot
   see (§3.E): serve it to check content and rendering, not paths.
6. Commit and push. **Publication is not automatic on push**: the `Documentation`
   workflow runs on a published release or on `workflow_dispatch`, and takes about
   three minutes. Trigger it with
   `gh workflow run sphinx_docs_to_gh_pages.yaml --ref main` and confirm the result
   on the published URL, which is `http://www.uibcdf.org/molsysmt/` — lower case,
   and not the `https://uibcdf.org/MolSysMT` that several project files still name.
