(user-foundations-support-viewers)=
# Viewers

MolSysMT provides unified 3D visualization capabilities through `msm.view()`, supporting native and third-party rendering backends across interactive notebooks, JupyterLab, and web environments.

---

## Supported 3D Rendering Backends

| Viewer Backend | Description | Environment | Support Level |
| :--- | :--- | :--- | :--- |
| **MolSysViewer** | Native web-based 3D visualization widget | Jupyter Notebook, JupyterLab, Web | Native Default (`default_viewer`) |
| **NGLView** | Interoperable widget backend using NGL | Jupyter Notebook, JupyterLab | Soft Dependency Integration |
| **Py3Dmol** | Lightweight WebGL-based viewer | Jupyter Notebook, Google Colab | Soft Dependency Integration |

Backend selection is controlled by passing `viewer='MolSysViewer'`, `viewer='NGLView'`, or `viewer='Py3Dmol'` to `msm.view()`. The global default viewer backend can be configured at runtime via `msm.configure.default_viewer`.
