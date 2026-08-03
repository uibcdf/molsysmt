# Notebook Compilation, Timestamp Tracking, and MolSysViewer Integration

This document defines the normative architectural contract for notebook pre-execution, timestamp tracking, Sphinx web compilation, and **MolSysViewer** 3D visualization integration in MolSysMT.

---

## 1. Architectural Overview and Design Principles

The documentation pipeline resolves three core engineering requirements:

1. **Deterministic Remote CI/CD**: Remote GitHub Actions builds must remain fast, lightweight, and crash-free. Web compilation (`make html`) does not execute Python code or heavy simulations in the cloud.
2. **Incremental Local Pre-Execution**: Developers executing notebooks locally only re-run notebooks that have actually been modified in their working session, preserving compute resources and time.
3. **Clutter-Free 3D Visualization**: Tutorial pages present clean, interactive 3D molecular views powered by **MolSysViewer** without full GUI editing toolbars interfering with the narrative.

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. LOCAL WORKSTATION                                                   │
│    Developer writes/edits .ipynb tutorials using `msm.view()`.         │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 2. INCREMENTAL PRE-EXECUTION                                           │
│    `python docs/execute_notebooks.py -n 12 -r docs/`                   │
│    - Hybrid Git status / commit timestamp modification detection.      │
│    - Embeds anywidget WebGL state into notebook JSON metadata.          │
│    - Automatically sanitizes JSON schema (guarantees outputs: []).     │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 3. SPHINX WEB COMPILATION (LOCAL & CI/CD)                              │
│    `make html SPHINXOPTS="-j 12"`                                      │
│    - `nb_execution_mode = "off"` in `docs/conf.py`.                    │
│    - `myst_nb` + `anywidget` render static HTML5 WebGL containers.      │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 4. GITHUB PAGES PUBLICATION                                            │
│    - Instant gh-pages deployment without active Python kernel requirement.│
│    - Full client-side interactive WebGL rendering via Mol* in browser. │
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

## 3. MolSysViewer Integration & Static View Generation

### **A. Architecture & `anywidget` Protocol**
- **Default Viewer**: `msm.view(molecular_system)` invokes `molsysviewer.new_view(...)` by default.
- **Widget Representation**: `molsysviewer.MolSysView` wraps `molsysviewer.widget.MolSysViewerWidget`, inheriting from `anywidget.Widget`.
- **State Serialization**: `anywidget` serializes the Mol* (Molstar) 3D scene, atomic coordinates, representations, and camera state into the notebook's cell output (`application/vnd.jupyter.widget-view+json`) and notebook metadata (`metadata.widgets`).

### **B. `mode="lite"` Static HTML Export (`write_html`)**
While interactive Jupyter sessions load the full MolSysViewer GUI (with editing toolbars and selection trees), documentation tutorial pages require clean, uncluttered figures.

1. **Static View Generator (`docs/generate_static_views/`)**:
   Standalone scripts pre-render clean views into [`docs/_static/views/`](../docs/_static/views/) using:
   ```python
   view = msm.view(molecular_system, selection='molecule_index==0')
   view.write_html("../_static/views/1BRS_molecule_index_zero.html", title="1BRS Molecule Index 0", mode="lite")
   ```
2. **`mode="lite"` Characteristics**:
   - Removes floating GUI toolbars and editing panels.
   - Retains canvas controls (Reset, Fullscreen, Spin, Swing).
   - Bundles a lightweight, self-contained Mol* WebGL viewer.
3. **User-Facing Tutorial Cell**:
   Notebooks display clean, idiomatic user code:
   ```python
   msm.view(molecular_system, selection='molecule_index==0')
   ```

---

## 4. Maintenance Checklist for Developers

When adding or modifying notebooks:

1. Edit the notebook (`.ipynb`) in your local Jupyter environment.
2. Run `python docs/execute_notebooks.py -r docs/` to pre-execute modified notebooks.
3. Verify local HTML compilation with `make -C docs html SPHINXOPTS="-j 12"`.
4. Check that `git status` includes `.ipynb` and `.nbconvert.last_run` files while ignoring `.nbconvert.log`.
5. Commit and push: GitHub Actions will publish the static site to `gh-pages` within seconds.
