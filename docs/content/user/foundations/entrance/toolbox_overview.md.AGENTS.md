# Micro-Governance: `toolbox_overview.md` (`toolbox_overview.md.AGENTS.md`)

This micro-governance contract governs [`docs/content/user/foundations/entrance/toolbox_overview.md`](toolbox_overview.md).

---

## 🔒 Frozen & Inviolable Content

1. **Format Policy**:
   - MUST remain a pure MyST Markdown (`.md`) page without code cells.

2. **Mandatory MyST Section Anchor**:
   - `(user-foundations-entrance-toolbox-overview)=`

3. **Inviolable Box Sections**:
   - **`## Basic Box`**: Must link to `../../tools/basic/index`.
   - **`## Build Box`**: Must link to `../../tools/build/index`.
   - **`## Structure Box`**: Must link to `../../tools/structure/index` (stipulating nm units, `(n_structures, n_atoms, 3)` shape, 3x3 rotation matrices, precompiled Rust kernels).
   - **`## Topology Box`**: Must link to `../../tools/topology/index`.
   - **`## Elements Box`**: Must link to `../../tools/element/index`.
   - **`## PBC & Physical Mechanics Box`**: Must link to `../../tools/pbc/index`, `../../tools/physchem/index`, and `../../tools/molecular_mechanics/index`.
   - **`## Third-Party Bridges Box`**: Must link to `../../tools/third_party/index`.

4. **Required Navigation Admonition**:
   - Must present the distinction between the **{doc}`Tools User Guide <../../tools/index>`** (tutorials per function) and the **{doc}`Technical API Documentation <../../../../api/index>`** (docstring specifications) inside an `{admonition}` note box at the end of the page.
