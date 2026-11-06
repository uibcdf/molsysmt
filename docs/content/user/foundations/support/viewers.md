(user-foundations-support-viewers)=
# Viewers

MolSysMT provides unified 3D visualization capabilities through `msm.view()`, supporting native and third-party rendering backends across interactive notebooks, JupyterLab, and web environments.

---

## Supported 3D Rendering Backends

| Viewer Backend | Description | Environment | Support Level |
| :--- | :--- | :--- | :--- |
| **MolSysViewer** | Native web-based 3D visualization widget | Jupyter Notebook, JupyterLab, Web | Native Default (`default_viewer`) |
| **NGLView** | Interoperable widget backend using NGL | Jupyter Notebook, JupyterLab | Soft Dependency Integration |

The public `msm.view()` routes are `viewer='MolSysViewer'` and
`viewer='NGLView'`. Omitting this argument uses MolSysViewer. An explicit
`viewer=None` reads `msm.configure.default_viewer`. A selected unavailable
dependency raises a native diagnostic; another backend is never selected silently.

An absent molecular system (`None`) creates an empty workspace in either runtime
backend. It does not create a zero-atom molecular system. Without a source,
`selection` and `structure_indices` can be `'all'`, `None` or flat empty sequences;
expressions and explicit indices have no source axis and are rejected before
creation. With a molecular source, its extraction and backend loading requirements
still apply. The caller owns the returned widget and closes it when finished.
Python construction is distinct from browser rendering and session persistence.
